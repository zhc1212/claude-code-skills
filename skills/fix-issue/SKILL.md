---
name: fix-issue
description: Analyze a GitHub issue, implement the fix, and create a PR. Use when user says "fix issue", "修bug", or wants to resolve a specific issue.
user_invocable: true
---

# Fix Issue

**This skill delegates to `/issue-to-pr --execute`.**

## Invocation

- `/fix-issue 42` → runs `/issue-to-pr 42 --execute`
- `/fix-issue` → ask which issue, then run `/issue-to-pr $ISSUE --execute`

When invoked, immediately invoke the `issue-to-pr` skill with the `--execute` flag. All steps (fetch, investigate, plan, implement, create PR) are handled there.
