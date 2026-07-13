---
name: codex-review
description: Sends code to GPT via Codex MCP for independent cross-model review with blind Claude pre-scan and structured synthesis. ONLY trigger when the user explicitly mentions "codex" in the context of review — e.g. "codex review", "/codex-review", "让codex看看", "codex帮我review", "让codex审一下", "codex check my code", "codex看一下代码", "codex帮我检查". Do NOT trigger on generic "review", "review my code", "review my changes", "superpower review", or any review request without the word "codex" — those belong to superpowers:requesting-code-review, review-implementation, or final-review. Not for debate (/codex-debate) or implementation delegation (/codex-tdd-implementer).
---

# Codex Code Review

Get an independent code review from GPT via Codex MCP — a second opinion
from a different model family. The cross-model architecture catches failure
modes that self-review misses, because Claude and GPT have different training
distributions and different blind spots.

The protocol adds a blind Claude quick-scan before the Codex call, then
synthesizes both perspectives. This is not redundant work — research shows
multi-pass review increases recall by over 100% even with the same model.

## Review Modes

### Default: `git diff HEAD`
When the user says `/codex-review` with no arguments:
1. Run `git diff HEAD` (uncommitted changes, staged + unstaged)
2. If empty, check branch:
   - **Feature branch**: resolve base branch (see below), run
     `git diff --find-renames <base>...HEAD`
   - **Default branch**: tell user "No uncommitted changes to review"

### With paths: `git diff HEAD -- <paths>`
When the user specifies files (e.g., `/codex-review src/compress/whitening.py`):
1. Run `git diff HEAD -- <paths>`
2. For **untracked** files (not in git), read the full file content instead
3. For **deleted** files, include the deletion diff only
4. For files with **no changes**, tell the user — don't send an empty diff

### Branch mode
When the user says "review branch", "review this branch", "review 分支":
1. Resolve base branch, run `git diff --find-renames <base>...HEAD`
2. If the diff is empty, tell the user "No changes on this branch relative
   to {base}" — don't send an empty diff to Codex

### Resolving base branch
Use this chain, stop at first success:
1. User explicitly specified a base → use it
2. `git rev-parse --abbrev-ref @{upstream}` → use upstream tracking branch
3. `git rev-parse --verify origin/HEAD` → use default remote branch
4. `git rev-parse --verify origin/main` → use `main`
5. `git rev-parse --verify origin/master` → use `master`

## Step 1: Collect Intent Context

Before building the prompt, gather the author's intent so the reviewer can
distinguish deliberate choices from oversights. Intent reduces false positives
but can also cause anchoring — handle it as evidence to test, not truth.

1. **Uncommitted changes**: `git log -1 --format=%B` for recent commit message.
   If the user described their goal in conversation, use that as primary intent.
2. **Branch mode**: `git log --format="- %s" <base>...HEAD` for all commit
   messages on the branch.
3. **With paths**: same as (1), plus conversation context if provided.

If no meaningful intent is found (commit message is just "wip"), note
`Intent: not provided` — don't fabricate one.

## Step 2: Claude Blind Quick-Scan

Before calling Codex, Claude scans the diff and records its top 3-5 concerns.
This takes ~30 seconds and creates an independent hypothesis set.

**Rules:**
- Do NOT include Claude's concerns in the Codex prompt — independence is the
  point. If Codex sees Claude's flags, it anchors on them.
- Keep it quick: top risks, not a full review. Think "what would I flag in
  a 30-second glance?"
- Record concerns privately — do not output them to the user yet.
  They're used in the synthesis step, not shown until then.

## Step 3: Prepare the Diff

**Redact secrets**: Before sending anything, scan for patterns like `sk-`,
`ghp_`, `token=`, API keys, passwords. Replace with `[REDACTED]`.

**Prefer diffs over full files**: Diffs give change context and are more
token-efficient.

**Exclude by default**: `*.md`, `*.json`, `*.yaml`, `*.log`, `__pycache__/`,
`*.pyc`, binary files.

### Large Diff Strategy

- **Under 800 changed lines**: Send in a single Codex call.
- **Over 800 lines**: Split into subsystem groups by risk priority, run
  independent review calls per group, then a synthesis pass to dedup and rank.

Split priority:
1. Core logic (highest risk — compression, model, math)
2. Training/eval correctness
3. CLI/orchestration
4. Tests
5. Everything else

Each sub-call is a fresh `mcp__codex__codex` call (independent, no shared
thread) with the full intent context but only its subsystem's diff. Note
omitted scope in each call. If a sub-call fails (MCP error), retry once,
then skip that subsystem and note it as unreviewed. After all sub-calls
complete, dedup by merging findings that reference the same code location,
and pick the higher-confidence version when two calls flag the same issue
differently.

### Project-Specific Review Profile

Check if `references/svd-llm-review.md` exists (or equivalent for the current
project). If present, load and append its domain-specific checks to the review
prompt. This keeps the core skill generic while adding project expertise.

## Step 4: Build the Review Prompt

```
You are a senior systems reviewer. Review the following code changes.

## Author's Intent
[INTENT — commit messages, user-stated goal, or "Not provided."]
Use this to distinguish deliberate design choices from accidental omissions.
Verify that the code actually implements the stated intent — 45% of AI-authored
PRs have descriptions inconsistent with the actual code changes.

[PROJECT-SPECIFIC CHECKS IF LOADED]

Prioritize:
- Likely bugs and regressions
- Type/shape/device/dtype mismatches
- Numerical stability issues
- Memory management problems
- Missing tests for touched behavior
- Reproducibility mistakes (unseeded randomness, nondeterministic ops)

Ignore pure style nits unless they hide a real bug.

[DIFF HERE]

For each finding, return:
- **Severity**: high / medium / low (how bad if true)
- **Confidence**: high / medium / low (how likely this is actually a bug)
- **Path:line**: where
- **Issue**: what's wrong
- **Evidence**: why you believe this from the diff
- **Why actionable**: what the author should do
- **Falsifier**: what evidence would make this NOT a bug (required for
  medium/low confidence findings)

Also return:
- **Verdict**: LGTM | Findings | Needs more context
- **Reviewed scope**: files and line ranges reviewed
- **Open questions**: anything you'd want to clarify with the author
- **Omitted scope**: files skipped (if any)
```

## Step 5: Call Codex MCP

```
mcp__codex__codex(
  prompt: <review prompt>,
  config: {"model": "gpt-5.6-sol", "reasoning_effort": "max"}
)
```

Save the `threadId` — the user may want follow-up.

If Codex MCP is unavailable (connection error, timeout), tell the user
explicitly rather than silently failing.

## Step 6: Cross-Check Synthesis

Compare Claude's blind quick-scan with Codex's review:

- **Both flagged**: High confidence. Present as primary findings.
- **Codex-only**: Present normally — Codex may have caught something Claude
  missed (this is the value of cross-model review).
- **Claude-only**: Re-examine against the diff. If Claude's concern is
  substantive and Codex missed it, present it as "Additional concern from
  Claude's pre-scan" with supporting evidence.

Don't manufacture disagreement — if Codex's review is thorough and Claude's
scan found nothing extra, just present Codex's findings.

## Step 7: Present Results

Show the synthesized review clearly. After presenting:
- If findings exist, offer to fix them (but don't auto-fix without consent)
- If LGTM, relay concisely
- If scope was truncated, mention what was skipped
- Mention that follow-up is available: "Ask me to clarify any finding with
  Codex, or re-review after fixes"

## Follow-Up

The user can ask to:
- **Clarify a finding**: Use `mcp__codex__codex-reply` with the saved
  threadId to ask Codex to elaborate or reconsider
- **Re-review after fixes**: Run a new diff and send the delta to Codex
  with context about what was fixed
- **Challenge a finding**: If the user disagrees, send their reasoning to
  Codex and see if it changes the verdict

## Important

- **Don't auto-fix**: Present findings first. Only fix if the user agrees.
- **Diff over full-file**: Always prefer diffs — they give context and save tokens.
- **Independence matters**: Claude's pre-scan stays private from Codex.
  Codex's review stays independent from Claude's concerns. Synthesis
  happens AFTER both complete.
