---
name: project-pipeline
description: Pick an open issue, implement it, and create a PR — end-to-end issue-to-merge workflow
user_invocable: true
---

# Project Pipeline

End-to-end workflow: pick an issue → implement → create PR → review.

## Invocation

- `/project-pipeline` — pick the next open issue
- `/project-pipeline 42` — process issue #42

## Step 1: Pick Issue

If no issue number provided:

```bash
# List open issues, sorted by priority labels
gh issue list --state open --json number,title,labels --limit 20
```

Present the list and let the user choose, or auto-pick the oldest unassigned issue.

## Step 2: Assign and Branch

```bash
# Assign to self
gh issue edit $ISSUE --add-assignee @me

# Create branch
git checkout -b "fix-$ISSUE-$(echo "$TITLE" | tr '[:upper:] ' '[:lower:]-' | head -c 30)"
```

## Step 3: Implement

Use `/issue-to-pr $ISSUE --execute` to:
1. Fetch issue context
2. Write implementation plan
3. Execute the plan
4. Review the implementation

## Step 4: Create PR and Review

1. Push and create PR (done by issue-to-pr)
2. Run `/review-implementation` for quality check
3. Fix any issues found
4. Report PR URL to user

## Step 5: Post-merge Cleanup

After the PR is merged:
```bash
CURRENT_BRANCH=$(git branch --show-current)
git checkout master
git pull
git branch -d "$CURRENT_BRANCH"
```
