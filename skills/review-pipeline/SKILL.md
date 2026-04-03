---
name: review-pipeline
description: Use when triaging open PRs — review, fix issues, and prepare for merge
user_invocable: true
---

# Review Pipeline

Triage open PRs: review code, fix CI/review issues, and prepare for merge.

## Invocation

- `/review-pipeline` — review the next open PR
- `/review-pipeline 42` — review PR #42

## Step 1: Pick PR

If no PR number provided:

```bash
gh pr list --state open --json number,title,author,createdAt,reviews --limit 20
```

Pick the oldest PR without an approving review.

## Step 2: Review

Run `/review-implementation` on the PR's branch:

```bash
gh pr checkout $PR
```

Then execute the review-implementation skill.

## Step 3: Fix Issues

If issues found, run `/fix-pr` to:
1. Address review comments
2. Fix CI failures
3. Fill test coverage gaps

## Step 4: Final Check

```bash
# Verify all checks pass
gh pr checks "$PR"

# Verify tests pass locally
ruff check . && pytest tests/ -m "not integration" -v
```

## Step 5: Recommend Action

Present to user:
- **Ready to merge** — all checks pass, code reviewed, tests adequate
- **Needs changes** — list specific issues that remain
- **Needs discussion** — design questions that need team input

If ready, suggest running `/final-review` for the merge decision.
