---
name: issue-to-pr
description: Use when you have a GitHub issue and want to create a PR with an implementation plan that triggers execution
user_invocable: true
---

# Issue to PR

Convert a GitHub issue into an actionable PR with a plan. Optionally execute the plan immediately.

## Invocation

- `/issue-to-pr 42` — create PR with plan only
- `/issue-to-pr 42 --execute` — create PR, then execute the plan

## Steps

### 1. Parse Input

Extract issue number from arguments:
- `123` → issue #123, plan only
- `123 --execute` → issue #123, plan + execute
- `https://github.com/owner/repo/issues/123` → issue #123

### 2. Fetch Issue Context

```bash
gh issue view $ISSUE --json title,body,labels,comments
```

Present the issue summary to the user. **Review all comments** — contributors may have posted clarifications or corrections.

### 3. Research and Plan

1. Read relevant source files to understand the codebase area affected
2. Write a plan to `docs/plans/YYYY-MM-DD-<slug>.md` covering:
   - What changes are needed
   - Which files to modify/create
   - Test strategy
   - Risk assessment

### 4. Create Branch and PR

```bash
# Create branch
BRANCH="fix-$ISSUE-$(echo "$TITLE" | tr '[:upper:] ' '[:lower:]-' | head -c 40)"
git checkout -b "$BRANCH"

# Stage the plan
git add docs/plans/*.md
git commit -m "Add plan for #$ISSUE: $TITLE"

# Push and create PR
git push -u origin "$BRANCH"
gh pr create --title "Fix #$ISSUE: $TITLE" --body "$(cat <<EOF
## Summary
<Brief description>

Fixes #$ISSUE

## Plan
See docs/plans/ for implementation plan.
EOF
)"
```

### 5. Execute Plan (only with `--execute`)

Skip if `--execute` was not provided.

1. Execute the plan step by step
2. Run `/review-implementation` to verify the code
3. Commit all changes
4. Push

### 6. Report

- PR URL and number
- Implementation summary (if executed)
- Next steps for the user
