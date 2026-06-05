---
name: fix-issue-batch
description: Batch-process open GitHub issues — check quality and fix each one sequentially. Use when user says "批量处理", "batch fix", "fix all issues", or wants to process multiple issues at once.
user_invocable: true
---

# Fix Issue Batch

Batch-process multiple open GitHub issues: check quality, implement fixes, create PRs.

## Invocation

- `/fix-issue-batch` — process all open issues
- `/fix-issue-batch bug` — process only issues labeled "bug"
- `/fix-issue-batch 42 43 44` — process specific issues

## Step 1: List Issues

```bash
# All open issues
gh issue list --state open --json number,title,labels --limit 50

# Or filtered by label
gh issue list --state open --label "bug" --json number,title,labels --limit 50
```

Present the list and confirm with the user which issues to process.

## Step 2: Process Each Issue

For each selected issue, sequentially:

### 2a. Check Quality
Run `/check-issue $ISSUE` to validate readiness.

- If **READY** → proceed to 2b
- If **NEEDS WORK** → skip, report, move to next issue

### 2b. Fix
Run `/fix-issue $ISSUE` to:
1. Analyze the issue
2. Implement the fix
3. Create a PR

### 2c. Log Result

Track progress:
```
| Issue | Title | Status | PR |
|-------|-------|--------|------|
| #42 | Fix whitening bug | PR #45 created | #45 |
| #43 | Add Mistral support | Skipped: needs info | - |
| #44 | Update eval metrics | PR #46 created | #46 |
```

## Step 3: Report Summary

After processing all issues, present:
- Total issues processed
- PRs created
- Issues skipped (with reasons)
- Any issues that failed
