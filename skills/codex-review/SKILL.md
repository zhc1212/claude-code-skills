---
name: codex-review
description: Send code to GPT-5.4 via Codex MCP for cross-model review. ONLY trigger when the user explicitly mentions "codex" in the context of review — e.g. "codex review", "/codex-review", "让codex看看", "codex帮我review". Do NOT trigger on generic "review", "review my code", "review my changes", "superpower review", or any review request that does not contain the word "codex" — those belong to superpowers:requesting-code-review, review-implementation, or final-review.
---

# Codex Code Review

Get an independent code review from GPT-5.4 via Codex MCP — a second opinion from a different model than the one writing the code.

## Review Modes

The skill supports several modes, determined by user input:

### Default: `git diff HEAD`
When the user just says `/codex-review` with no arguments:
1. Run `git diff HEAD` (uncommitted changes, staged + unstaged)
2. If empty, check branch:
   - **Feature branch**: resolve base branch (see below), run `git diff --find-renames <base>...HEAD`
   - **Default branch**: tell user "No uncommitted changes to review"

### With paths: `git diff HEAD -- <paths>`
When the user specifies files (e.g., `/codex-review src/compress/whitening.py`):
1. Run `git diff HEAD -- <paths>` to get diff for those files
2. For **untracked** files (not in git), read the full file content instead
3. For **deleted** files, include the deletion diff only

### Branch mode
When the user says "review branch", "review this branch", "review 分支":
1. Resolve base branch, run `git diff --find-renames <base>...HEAD`

### Resolving base branch
Use this chain, stop at first success:
1. User explicitly specified a base → use it
2. `git rev-parse --abbrev-ref @{upstream}` → use upstream tracking branch
3. `git rev-parse --verify origin/HEAD` → use default remote branch
4. `git rev-parse --verify origin/main` → use `main`
5. `git rev-parse --verify origin/master` → use `master`

## Build the Review Prompt

Construct the prompt based on which files are touched. The review should be ML/numerics-focused since this is the SVD-LLM compression library.

```
You are a senior ML systems reviewer. Review the following code changes.

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

[DIFF HERE]

Return in this format:
- **Verdict**: LGTM | Findings | Needs more context
- **Reviewed scope**: files and line ranges reviewed
- **Findings** (if any): [severity: high/medium/low] path:line — issue / why it matters / suggested fix
- **Open questions**: anything you'd want to clarify with the author
- **Omitted scope**: files skipped due to truncation (if any)
```

## Call Codex MCP

```
mcp__codex__codex(
  prompt: <review prompt>,
  profile: "review"
)
```

The `review` profile sets reasoning effort to `medium`.

If Codex MCP is unavailable (connection error, timeout), tell the user explicitly rather than silently failing.

## Handling Large Diffs

- Budget: ~600-800 changed lines. Preserve full hunk boundaries — don't cut mid-function.
- If over budget, prioritize by risk:
  1. `src/compress/`, `src/model/` — core math, highest risk
  2. `src/finetune/`, `src/eval/` — training/eval correctness
  3. `scripts/` — CLI and orchestration
  4. `tests/` — test coverage
  5. Everything else
- Note omitted files in the prompt so the reviewer knows the scope.
- Exclude by default: `*.md`, `*.json`, `*.yaml`, `*.log`, `__pycache__/`, `*.pyc`, binary files.

## Present Results

Show the review output clearly. After presenting:
- If findings exist, offer to fix them (but don't auto-fix)
- If LGTM, relay the message concisely
- If scope was truncated, mention what was skipped

## Important

- **Redact secrets**: Before sending, scan for patterns like `sk-`, `ghp_`, `token=`, API keys. Replace with `[REDACTED]`.
- **Don't auto-fix**: Present findings to the user first. Only fix if they agree.
- **Diff over full-file**: Always prefer sending diffs over full file contents — diffs give the reviewer change context and are more token-efficient.
