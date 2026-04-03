---
name: check-issue
description: Review a GitHub issue for quality — check clarity, reproducibility, and completeness before implementation. Use when user says "检查issue", "check issue", "review issue", or wants to validate an issue before working on it.
user_invocable: true
---

# Check Issue

Review a GitHub issue for quality and readiness before implementation.

## Invocation

- `/check-issue 42` — check issue #42
- `/check-issue` — ask which issue to check

## Step 1: Fetch Issue

```bash
gh issue view $ISSUE --json title,body,labels,comments,author
```

## Step 2: Quality Checklist

Evaluate the issue against these criteria:

### Clarity
- [ ] Problem/feature is clearly described
- [ ] Expected behavior is stated
- [ ] For bugs: steps to reproduce are provided
- [ ] For features: use case is explained

### Completeness
- [ ] Enough context to start implementation
- [ ] Model/method/dataset is specified (if relevant)
- [ ] No ambiguous requirements

### Feasibility
- [ ] Within the scope of SVD_LLM
- [ ] Does not duplicate existing functionality
- [ ] Technical approach is feasible

### Labels
- [ ] Appropriate labels are set (bug, enhancement, etc.)

## Step 3: Report

Present findings:

```
## Issue #N Quality Check

### Title: <title>

| Criterion | Status | Notes |
|-----------|--------|-------|
| Clarity | PASS/FAIL | ... |
| Completeness | PASS/FAIL | ... |
| Feasibility | PASS/FAIL | ... |
| Labels | PASS/FAIL | ... |

### Verdict: READY / NEEDS WORK

### Suggested Improvements (if NEEDS WORK):
- [list of things to fix]
```

## Step 4: Label (if READY)

```bash
gh issue edit $ISSUE --add-label "good-first-issue"  # or "ready"
```

If NEEDS WORK, comment on the issue with the suggested improvements:
```bash
gh issue comment $ISSUE --body "..."
```
