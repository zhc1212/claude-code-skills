---
name: final-review
description: Interactive maintainer review for PRs — assess completeness, quality, test coverage, then merge or hold
user_invocable: true
---

# Final Review

Interactive maintainer review for PRs before merging. Ensures the PR is complete, well-tested, and ready for production.

## Invocation

- `/final-review` — review the current branch's PR
- `/final-review 42` — review PR #42

## Step 1: Gather PR Context

```bash
PR=${1:-$(gh pr view --json number -q '.number')}
gh pr view "$PR" --json title,body,files,commits,reviews,statusCheckRollup,mergeable
gh pr diff "$PR"
```

## Step 2: Checklist

Go through each item interactively with the user:

### 2a. CI Status
- All CI checks passing?
- If not, identify failures and suggest fixes

### 2b. Code Review
- All review comments addressed?
- Any unresolved threads?

### 2c. Completeness
- Does the PR do what the linked issue/description says?
- Are all edge cases handled?
- Is there adequate test coverage for new code?

### 2d. Quality Assessment

Rate the PR:
- **A** — Excellent: clean, well-tested, production-ready
- **B** — Good: minor issues that don't block merge
- **C** — Needs work: significant issues to address before merge
- **D** — Reject: fundamental problems, needs redesign

### 2e. Test Verification

```bash
# Run tests locally
ruff check .
pytest tests/ -m "not integration" -v
```

## Step 3: Decision

Present findings and ask the user:

> **Merge**, **Hold** (needs changes), or **Close** (reject)?

- **Merge**: `gh pr merge "$PR" --squash --delete-branch`
- **Hold**: List required changes, suggest running `/fix-pr`
- **Close**: Explain reasoning, close with `gh pr close "$PR"`
