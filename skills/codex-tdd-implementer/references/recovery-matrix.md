# Recovery Matrix

Reference for diagnosing Codex failures. Consult when things go wrong —
don't run through this as a checklist on every invocation.

## Quick Dispatch

| Failure | Signal | Action |
|---------|--------|--------|
| Setup error | ImportError, SyntaxError | Fix spec imports/paths, retry |
| Weak tests | Tests pass for wrong impl | "Add value assertions for X", retry |
| Spec unclear | Codex asks questions or misses intent | Revise spec, retry |
| MCP/env | Timeout, git conflict | Fix env, retry same phase |
| Partial impl | Some tests pass, some fail | Send failing output via codex-reply |

## Rules

- **Max 1 retry in FAST mode.** If Codex can't solve it in 2 calls, tell
  the user and offer Claude-only implementation. Claude implementing directly
  is cheaper than orchestrating multiple Codex retries.
- **Max 2 retries per phase in ADVERSARIAL mode.** Then escalate to user.
- **Environment retries** (MCP timeout, git conflict) don't count toward
  the retry budget.
- **Reclassify after failure.** If the first diagnosis didn't fix it,
  re-read the logs and pick a different category. Don't spend two retries
  on the same diagnosis without new evidence.
