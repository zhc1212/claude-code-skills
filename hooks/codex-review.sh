#!/bin/bash
# Stop hook: run one Codex review per response if code files changed.

set -euo pipefail

# Global temp file list for trap-based cleanup
_TMPFILES=()
_mktmp() { local f; f=$(mktemp); _TMPFILES+=("$f"); echo "$f"; }
trap 'rm -f "${_TMPFILES[@]}" 2>/dev/null' EXIT

INPUT=$(cat)
CWD=$(printf '%s' "$INPUT" | python3 -c 'import json, sys; print(json.load(sys.stdin).get("cwd", "."))')
STOP_ACTIVE=$(printf '%s' "$INPUT" | python3 -c 'import json, sys; print(str(json.load(sys.stdin).get("stop_hook_active", False)).lower())')

if [ "$STOP_ACTIVE" = "true" ] || [ ! -d "$CWD" ]; then
    exit 0
fi

cd "$CWD"

MARKER_FILE="$CWD/.claude/hooks/state/changed_files.txt"
if [ ! -f "$MARKER_FILE" ]; then
    exit 0
fi

# Atomically move marker to a temp file immediately, so even if the
# review times out or crashes, the marker won't remain to re-trigger.
MARKER_WORKING=$(_mktmp)
mv "$MARKER_FILE" "$MARKER_WORKING" 2>/dev/null || exit 0

mapfile -t RAW_FILES < <(sort -u "$MARKER_WORKING")
if [ "${#RAW_FILES[@]}" -eq 0 ]; then
    exit 0
fi

# Group files by their git worktree so each group is diffed against
# the correct HEAD.  For each file we resolve its absolute path, then
# use `git -C <dir> rev-parse --show-toplevel` to find the worktree root.
# Files that don't belong to any worktree are silently skipped.

GROUPS_JSON=$(_mktmp)
CWD="$CWD" python3 - "$MARKER_WORKING" "$GROUPS_JSON" <<'PYGROUP'
import json, os, pathlib, subprocess, sys

marker_path = sys.argv[1]
output_path = sys.argv[2]
cwd = pathlib.Path(os.environ["CWD"]).resolve()

with open(marker_path) as f:
    raw_files = sorted(set(line.strip() for line in f if line.strip()))

# Map each file to its git worktree root
groups = {}  # worktree_root -> [abs_path, ...]
for raw in raw_files:
    candidate = pathlib.Path(raw)
    if not candidate.is_absolute():
        candidate = cwd / candidate
    candidate = candidate.resolve()
    # Find the git worktree root for this file
    try:
        result = subprocess.run(
            ["git", "-C", str(candidate.parent), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            continue
        wt_root = result.stdout.strip()
    except Exception:
        continue
    # Check file exists or is git-tracked in that worktree
    try:
        tracked = subprocess.run(
            ["git", "-C", wt_root, "ls-files", "--error-unmatch",
             str(candidate.relative_to(wt_root))],
            capture_output=True, timeout=5
        )
        is_tracked = tracked.returncode == 0
    except Exception:
        is_tracked = False
    if candidate.is_file() or is_tracked:
        groups.setdefault(wt_root, []).append(str(candidate))

with open(output_path, 'w') as f:
    json.dump(groups, f)
PYGROUP

GROUPS=$(cat "$GROUPS_JSON")
if [ "$GROUPS" = "{}" ]; then
    exit 0
fi

# Build unified diff and file list across all worktree groups
DIFF=""
CHANGED_FILES=""
SAFE_EXTS="py|js|ts|tsx|jsx|rs|go|java|c|cpp|h|hpp|sh|tex|css|html"
VALID_FILES=()

while IFS= read -r wt_root; do
    mapfile -t wt_files < <(WT_ROOT="$wt_root" python3 -c "import json,sys,os; [print(f) for f in json.load(sys.stdin).get(os.environ['WT_ROOT'],[])]" <<< "$GROUPS")
    if [ "${#wt_files[@]}" -eq 0 ]; then continue; fi

    # Compute relative paths for this worktree
    REL_PATHS=()
    for abs_file in "${wt_files[@]}"; do
        REL_PATHS+=("${abs_file#$wt_root/}")
        VALID_FILES+=("$abs_file")
    done

    # Get branch name for context
    WT_BRANCH=$(git -C "$wt_root" branch --show-current 2>/dev/null || echo "detached")
    CHANGED_FILES+="[${WT_BRANCH}] $(printf '%s, ' "${REL_PATHS[@]}" | sed 's/, $//')
"

    # Diff against the correct HEAD in the correct worktree
    WT_DIFF=$(git -C "$wt_root" diff HEAD -- "${REL_PATHS[@]}" 2>/dev/null || true)
    if [ -n "$WT_DIFF" ]; then
        DIFF+="$WT_DIFF
"
    else
        # Fallback: file snapshots for safe extensions
        for abs_file in "${wt_files[@]}"; do
            rel="${abs_file#$wt_root/}"
            if [[ "$rel" =~ \.(${SAFE_EXTS})$ ]] && [[ ! "$rel" =~ (\.env|credentials|secret|\.key|\.pem|\.p12|config|settings|seed) ]]; then
                DIFF+="=== FILE SNAPSHOT (${WT_BRANCH}): $rel ===
$(sed -n '1,100p' "$abs_file")
"
            fi
        done
    fi
done < <(printf '%s' "$GROUPS" | python3 -c "import json,sys; [print(k) for k in json.load(sys.stdin)]")

if [ -z "$DIFF" ]; then
    exit 0
fi

# Collect intent context: recent commit messages as author's intent
INTENT=""
while IFS= read -r wt_root; do
    WT_BRANCH=$(git -C "$wt_root" branch --show-current 2>/dev/null || echo "detached")
    # Check if on a feature branch (not main/master)
    if git -C "$wt_root" rev-parse --verify origin/main >/dev/null 2>&1; then
        DEFAULT_REF="origin/main"
    elif git -C "$wt_root" rev-parse --verify origin/master >/dev/null 2>&1; then
        DEFAULT_REF="origin/master"
    else
        DEFAULT_REF=""
    fi
    MERGE_BASE=""
    if [ -n "$DEFAULT_REF" ]; then
        MERGE_BASE=$(git -C "$wt_root" merge-base "$DEFAULT_REF" HEAD 2>/dev/null || true)
    fi
    # On a feature branch if DEFAULT_REF exists and current branch differs
    DEFAULT_BRANCH_NAME="${DEFAULT_REF#origin/}"
    if [ -n "$MERGE_BASE" ] && [ "$WT_BRANCH" != "$DEFAULT_BRANCH_NAME" ]; then
        # Feature branch: collect all commit messages since divergence
        BRANCH_MSGS=$(git -C "$wt_root" log --format="- %s" "${MERGE_BASE}..HEAD" 2>/dev/null | head -10)
        if [ -n "$BRANCH_MSGS" ]; then
            INTENT+="[${WT_BRANCH}] Branch commits:
${BRANCH_MSGS}
"
        fi
    fi
    # Always include latest commit message as context
    LATEST_MSG=$(git -C "$wt_root" log -1 --format="%s" 2>/dev/null || true)
    if [ -n "$LATEST_MSG" ] && [ -z "$INTENT" ]; then
        INTENT+="[${WT_BRANCH}] Latest commit: ${LATEST_MSG}
"
    fi
done < <(printf '%s' "$GROUPS" | python3 -c "import json,sys; [print(k) for k in json.load(sys.stdin)]")

if [ -z "$INTENT" ]; then
    INTENT="Not provided."
fi

DIFF_TMPFILE=$(_mktmp)
printf '%s\n' "$DIFF" | sed -n '1,600p' > "$DIFF_TMPFILE"
python3 - "$DIFF_TMPFILE" <<'PY'
import re
import sys

with open(sys.argv[1], 'r') as f:
    text = f.read()
patterns = [
    (re.compile(r'(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*["\']?[A-Za-z0-9_\-\/+=]{8,}["\']?'), r'\1=[REDACTED]'),
    (re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----', re.S), '[REDACTED PRIVATE KEY]'),
    (re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}'), '[REDACTED TOKEN]'),
    (re.compile(r'(?i)(aws[_-]?access|aws[_-]?secret)[_-]?\w*\s*[:=]\s*["\']?[A-Za-z0-9/+=]{16,}["\']?'), r'\1=[REDACTED]'),
    (re.compile(r'sk-[A-Za-z0-9]{20,}'), '[REDACTED API KEY]'),
    (re.compile(r'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}'), '[REDACTED JWT]'),
]
for pattern, repl in patterns:
    text = pattern.sub(repl, text)
with open(sys.argv[1], 'w') as f:
    f.write(text)
PY
DIFF=$(cat "$DIFF_TMPFILE")

PROMPT_TMPFILE=$(_mktmp)
cat > "$PROMPT_TMPFILE" <<PROMPT_EOF
You are a senior ML systems reviewer. Review the following code changes.

## Author's Intent
${INTENT}
Use this to distinguish deliberate design choices from accidental omissions.
Flag cases where the code contradicts the stated intent.

Prioritize:
- Likely bugs and regressions
- Tensor shape / device / dtype mismatches
- Numerical stability issues (Cholesky, SVD, division by zero)
- GPU memory blowups (large allocations, missing cleanup)
- Missing tests for touched behavior
- Reproducibility mistakes (unseeded randomness, nondeterministic ops)
- Evaluation/calibration data leakage

Path-specific checks:
- src/compress/, src/model/: rank math, shape invariants, whitening correctness
- src/finetune/: grad flow, train/eval mode, optimizer state, checkpoint correctness
- src/eval/, scripts/: metric correctness, dataset leakage, CLI schema compatibility
- tests/: weak assertions, missing edge cases, mismatch with touched behavior

Ignore pure style nits unless they hide a real bug.

Changed files (branch shown in brackets):
${CHANGED_FILES}

Diff:
${DIFF}

Return in this JSON format (MANDATORY — your entire response must be valid JSON):
{"verdict": "LGTM" or "findings" or "needs_context", "reviewed_scope": "files reviewed", "findings": [{"severity": "high/medium/low", "location": "path:line", "issue": "description", "fix": "suggestion"}], "open_questions": ["question"], "omitted_scope": "files skipped if any"}
PROMPT_EOF

REVIEW_OUTPUT=""
if command -v codex &>/dev/null; then
    TMP_OUTPUT=$(_mktmp)
    # Try with review profile (medium reasoning effort); fall back to default if profile missing
    if timeout 90 codex exec --full-auto --profile review -C "$CWD" -o "$TMP_OUTPUT" - < "$PROMPT_TMPFILE" >/dev/null 2>&1; then
        REVIEW_OUTPUT=$(cat "$TMP_OUTPUT")
    elif timeout 90 codex exec --full-auto -C "$CWD" -o "$TMP_OUTPUT" - < "$PROMPT_TMPFILE" >/dev/null 2>&1; then
        REVIEW_OUTPUT=$(cat "$TMP_OUTPUT")
    fi
fi

# Marker already removed at the top; just exit if no review output
if [ -z "$REVIEW_OUTPUT" ]; then
    exit 0
fi

REVIEW_DIR="$CWD/.claude/reviews"
mkdir -p "$REVIEW_DIR"
REVIEW_FILE="$REVIEW_DIR/$(date +%Y%m%d_%H%M%S).md"
cat > "$REVIEW_FILE" <<REVIEW_EOF
# Code Review - $(date '+%Y-%m-%d %H:%M:%S')

## Changed Files
${CHANGED_FILES}

## Review
${REVIEW_OUTPUT}
REVIEW_EOF

REVIEW_TMPFILE=$(_mktmp)
printf '%s' "$REVIEW_OUTPUT" > "$REVIEW_TMPFILE"
FILES_TMPFILE=$(_mktmp)
printf '%s' "$CHANGED_FILES" > "$FILES_TMPFILE"

DECISION=$(python3 - "$REVIEW_TMPFILE" <<'PY'
import json, sys, re

with open(sys.argv[1]) as f:
    text = f.read()

# Try to parse structured JSON response
try:
    # Strip markdown code fence if present, then parse JSON
    stripped = re.sub(r'^```(?:json)?\s*', '', text.strip())
    stripped = re.sub(r'\s*```$', '', stripped.strip())
    data = json.loads(stripped)
    verdict = data.get("verdict", "").lower()
    findings = data.get("findings", [])
    has_high = any(f.get("severity") == "high" for f in findings)
    if verdict == "lgtm" and not has_high:
        print("approve")
    else:
        print("block")
except (json.JSONDecodeError, AttributeError):
    # Fallback: simple heuristic on raw text
    lower = text.lower()
    print("approve" if "lgtm" in lower and "high" not in lower else "block")
PY
)

PAYLOAD_TMPFILE=$(_mktmp)
python3 - "$REVIEW_TMPFILE" "$FILES_TMPFILE" "$REVIEW_FILE" "$DECISION" "$PAYLOAD_TMPFILE" <<'PY'
import json
import sys

with open(sys.argv[1]) as f:
    review = f.read()
with open(sys.argv[2]) as f:
    files = f.read()
review_file = sys.argv[3]
decision = sys.argv[4]
output_path = sys.argv[5]

prefix = "Codex review gate triggered for:\n" + files + "\n\n"
suffix = f"\n\nReview saved to: {review_file}"
if decision == "approve":
    reason = prefix + review + suffix
else:
    reason = prefix + review + "\n\nResolve the review findings before finishing this turn." + suffix

with open(output_path, 'w') as f:
    json.dump({"decision": decision, "reason": reason}, f)
PY

cat "$PAYLOAD_TMPFILE"
# All temp files cleaned up by EXIT trap
