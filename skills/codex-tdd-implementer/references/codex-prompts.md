# Codex Prompt Templates

Adapt these templates to the specific task — they're starting points, not rigid formats. The important thing is that Codex receives a clear spec, knows which files it can touch, and reports what happened.

## MCP Call Defaults

All Codex calls share these settings:

```
model: "gpt-5.5"
config: {"reasoning_effort": "xhigh"}
cwd: <current worktree path>
```

Phase-specific settings:

| Phase | sandbox | approval-policy |
|-------|---------|-----------------|
| A (RED) | `workspace-write` | `never` |
| B (GREEN) | `workspace-write` | `never` |
| Tiny | `workspace-write` | `never` |
| Dual review | `read-only` | (not needed) |

## Composing the prompt

The prompt Codex receives is typically: **spec + phase instructions**. Include enough context for Codex to work independently — it can't ask follow-up questions. If the task involves existing code, paste the relevant function signatures or module structure into the spec so Codex knows what it's working with.

## Phase A — RED (test-only)

Codex writes failing tests. It needs to understand the contract but not the implementation strategy — that's the whole point of the separation.

Phase A instructions to append to the spec:

```
You may create and edit test files (tests/* or test_*.py) and fixture/golden
data files. Implementation files are off-limits — the tests should define the
contract, not the solution.

1. Write a failing test for each acceptance criterion in the spec.
2. Run: <TEST_CMD>
3. Confirm the test fails with a behavioral error (AssertionError, ValueError),
   not a setup error (ImportError, SyntaxError). If it's a setup error, fix
   the test file so it can actually run and fail on behavior.

When done, output a fenced JSON block:
{"phase":"red","changed_files":[...],"test_exit_code":1,"failure_summary":"...","failure_type":"behavioral"}
```

Save the returned `threadId` — you need it for Phase B retries and dual review.

## Phase B — GREEN + REFACTOR

Codex implements to pass the failing tests. The Phase B prompt includes specific
artifacts from Phase A, but NOT Phase A's exploratory reasoning — preserving
the adversarial split between test design and implementation.

**Phase B receives:**
- The spec (task, allowed write set, acceptance criteria, constraints)
- Test diff from Phase A (the actual test files)
- RED command output (test failure messages)
- Gate verdict (pass/fail per check — no detailed rationale)
- Spec-test traceability matrix (criterion → test mapping)

**Phase B does NOT receive:**
- Phase A's reasoning or thought process
- Rejected test approaches
- Implementation hints or strategy
- Claude's gate review comments (beyond the verdict)

Phase B instructions:

```
Tests from Phase A are failing. Your job is to make them pass with a correct,
minimal implementation. Do not edit test files — the contract is fixed.

Here is the spec:
<spec>

Here are the failing tests (diff):
<test diff>

Here is the test failure output:
<RED command output>

Traceability: each acceptance criterion maps to these tests:
<spec-test matrix>

1. Write implementation to pass the tests.
2. Run: <TEST_CMD> — confirm all pass.
3. If you see opportunities to simplify without changing behavior, refactor
   and re-run to confirm tests still pass.

When done, output a fenced JSON block:
{"phase":"green","changed_files":[...],"test_exit_code":0,"pass_count":N,"fail_count":0}
```

Save the `threadId` as `PHASE_B_SESSION`.

## Tiny Tier — Single Call

Combines both phases in one session. Codex writes a test, observes it fail, then implements to pass:

```
<spec>

Work in two steps:
1. Write a failing test first. Run it. Confirm it fails on behavior (not imports).
2. Then write the implementation to pass. Run again. Confirm it passes.

Output JSON with both results.
```

## Dual Review (read-only)

For high-risk tasks, Codex reviews the frozen diff independently from Claude. Use `sandbox: "read-only"` — Codex cannot modify files.

```
Review this diff for bugs, numerical issues, edge cases, and test coverage gaps.
Focus on correctness over style.

<paste git diff output>
```

Run this in parallel with Claude's `superpowers:requesting-code-review`.

## Retry via Follow-up

Always resume using the saved threadId — `--resume-last` can pick up an unrelated session:

```
mcp__codex__codex-reply(
  threadId: "<saved session ID>",
  prompt: "The following issues need fixing:\n1. ...\n2. ...\n\nFix and re-run tests."
)
```
