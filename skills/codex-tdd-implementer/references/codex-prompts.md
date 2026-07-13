# Codex Prompt Templates

## MCP Defaults

```
model: "gpt-5.5"
config: {"reasoning_effort": "xhigh"}
cwd: <current worktree path>
sandbox: "workspace-write"
approval-policy: "never"
```

## FAST Mode — Single Call

```
<spec>

Work in two steps:
1. Write failing tests first. Run: <TEST_CMD>
   Confirm they fail on behavior (AssertionError, ValueError),
   not setup (ImportError, SyntaxError). Fix setup issues before proceeding.
2. Implement to pass the tests. Run: <TEST_CMD>
   Confirm all pass. Refactor if you see obvious simplifications.

When done, output a fenced JSON block:
{"changed_files":[...],"test_exit_code":0,"pass_count":N,"fail_count":0}
```

## ADVERSARIAL Mode — Phase A (test-only)

```
<spec>

You may create and edit test files only. Implementation files are off-limits.

1. Write a failing test for each acceptance criterion.
2. Run: <TEST_CMD>
3. Confirm tests fail with behavioral errors, not setup errors.

When done, output JSON:
{"phase":"red","changed_files":[...],"test_exit_code":1,"failure_summary":"..."}
```

## ADVERSARIAL Mode — Phase B (implementation)

Phase B gets the spec + test artifacts, but NOT Phase A's reasoning.

```
Tests from Phase A are failing. Make them pass with a correct, minimal
implementation. Do not edit test files.

Spec:
<spec>

Failing tests (diff):
<test diff>

Test failure output:
<RED output>

1. Implement to pass.
2. Run: <TEST_CMD> — confirm all pass.
3. Refactor if obvious, re-run to confirm.

Output JSON:
{"phase":"green","changed_files":[...],"test_exit_code":0,"pass_count":N}
```

## Read-Only Review (ADVERSARIAL dual review)

```
Review this diff for bugs, numerical issues, edge cases, and test gaps.
Focus on correctness over style.

<git diff output>
```

Use `sandbox: "read-only"`.

## Follow-Up (retry)

Use saved threadId via `mcp__codex__codex-reply`:

```
These tests still fail:
<failing test output>

Fix the implementation and re-run.
```
