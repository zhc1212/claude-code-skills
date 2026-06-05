---
name: review-implementation
description: Use after implementing any code change to verify completeness and correctness before committing
user_invocable: true
---

# Review Implementation

Performs two review passes to verify code quality and completeness:
- **Structural review** — checks completeness against the plan or issue requirements
- **Quality review** — DRY, KISS, test quality, code style

## Invocation

- `/review-implementation` — auto-detect from git diff
- `/review-implementation generic` — code quality only (no structural checklist)

## Step 1: Gather Context

```bash
# Get the diff to review
BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo master)
git diff "$BASE"...HEAD --stat
git diff "$BASE"...HEAD

# Check for linked PR/issue
gh pr view --json number,title,body 2>/dev/null
```

## Step 2: Structural Review

Check:
1. All files mentioned in the plan/issue are addressed
2. New functions have appropriate tests
3. Imports and dependencies are correct
4. No accidentally committed debug code or print statements
5. Type hints are consistent with existing code style

## Step 3: Quality Review

Check:
1. **DRY** — no duplicated logic
2. **KISS** — no over-engineering
3. **Test quality** — meaningful assertions, edge cases covered
4. **Style** — matches existing codebase conventions (ruff-compliant)
5. **Security** — no hardcoded secrets, no unsafe operations

## Step 4: Address Findings

1. **Fix automatically** — clear issues (missing imports, style violations, obvious bugs)
2. **Report to user** — ambiguous issues, design decisions, anything needing user input

## Step 5: Verify

```bash
# Run lint and tests
ruff check .
pytest tests/ -m "not integration" -v
```

## Step 6: Present Consolidated Report

```
## Review: [Description]

### Structural Completeness
| # | Check | Status |
|---|-------|--------|
...

### Code Quality
- DRY: OK / ...
- KISS: OK / ...
- Test quality: OK / ...

### Build Status
- `ruff check .`: PASS / FAIL
- `pytest tests/`: PASS / FAIL

### Fixes Applied
- [list of issues automatically fixed]

### Remaining Items (needs user decision)
- [list of issues that need user input]
```
