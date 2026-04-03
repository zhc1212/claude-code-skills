---
name: fix-pr
description: Use when a PR has review comments to address, CI failures to fix, or test coverage gaps to resolve
user_invocable: true
---

# Fix PR

Resolve PR review comments, fix CI failures, and address test coverage gaps for the current branch's PR.

## Step 1: Gather PR State

### 1a. Find the current PR

```bash
PR=$(gh pr view --json number -q '.number' 2>/dev/null)
if [ -z "$PR" ]; then
    echo "No PR found for current branch"
    exit 1
fi
gh pr view "$PR" --json title,url,state,reviews,statusCheckRollup
```

### 1b. Fetch Review Comments

Check ALL sources:

```bash
# Inline review comments
gh api repos/{owner}/{repo}/pulls/$PR/comments --jq '.[].body'

# PR review summaries
gh api repos/{owner}/{repo}/pulls/$PR/reviews --jq '.[] | select(.state != "PENDING") | .body'

# General PR comments
gh api repos/{owner}/{repo}/issues/$PR/comments --jq '.[].body'
```

### 1c. Check CI Status

```bash
gh pr checks "$PR"
```

## Step 2: Triage and Prioritize

Categorize all findings:

| Priority | Type | Action |
|----------|------|--------|
| 1 | CI failures (lint/test) | Fix immediately — blocks merge |
| 2 | User review comments | Address each one — highest review priority |
| 3 | Bot suggestions | Evaluate validity, fix if correct |
| 4 | Test coverage gaps | Add tests for uncovered lines |

**User comments always take priority over bot comments.**

## Step 3: Fix CI Failures

For each failing check:

1. **Lint (ruff)**: Run `ruff check .` locally, fix warnings
2. **Tests**: Run `pytest tests/ -m "not integration" -v` locally, fix failures
3. **Build errors**: Check import/dependency issues

## Step 4: Address Review Comments

For each review comment:

1. Read the comment and the code it references
2. Evaluate if the suggestion is correct
3. If valid: make the fix, commit
4. If debatable: fix it anyway unless technically wrong
5. If wrong: prepare a response explaining why

**Do NOT respond on the PR** — just fix and commit. The user will push and respond.

## Step 5: Commit and Report

After all fixes:

```bash
# Verify everything passes locally
ruff check . && pytest tests/ -m "not integration" -v
```

Commit with a descriptive message:

```bash
git commit -m "fix: address PR #$PR review comments

- [summary of fixes applied]
"
```

Report to user:
- List of review comments addressed (with what was done)
- CI fixes applied
- Any comments left unresolved (with reasoning)
