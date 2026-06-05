---
name: codex-tdd-implementer
description: "Delegates coding to Codex via two-phase TDD — Claude writes the spec and reviews, Codex writes tests (Phase A) then implementation (Phase B) in gated sessions. Use when user says 让codex写代码, 交给codex, codex来实现, codex来写, 让codex帮我写, codex帮我实现, codex来搞, codex来做, have codex implement, delegate to codex, let codex do it, let codex handle this, codex TDD, codex implement this, 交给codex做, codex写测试再实现, let GPT write this. Also trigger when the user wants cross-model TDD collaboration, asks Codex to build or fix a feature, or wants test-driven implementation with an independent model. Not for code review (/codex-review), debate (/codex-debate), or quick one-shot questions (/codex consult)."
---

# Codex TDD Implementer

Claude writes the spec and reviews. Codex writes tests (Phase A) and
implementation (Phase B) in separate, gated sessions. Claude gates the
transition — no implementation starts until the tests pass Claude's quality
review.

This works because Codex-A (test writer) and Codex-B (implementer) run in
isolated sessions — neither sees the other's reasoning. Claude's gate catches
tautological tests before they reach the implementer. The result: tests that
genuinely constrain the implementation, not tests shaped by foreknowledge of
how to pass them.

**Hands off while Codex works.** Claude edits only specs, review notes, and
orchestration — never test or implementation files. Mixed authorship creates
ambiguous blame when tests fail. After failed recovery attempts, tell the user
and offer to take over.

**Bundled resources:**
- `references/codex-prompts.md` — MCP call templates and Codex prompt text
- `references/recovery-matrix.md` — failure diagnosis and recovery actions

**Project context**: Before writing any spec, check for project-specific test
infrastructure (conftest.py, markers, import patterns, test commands). Include
relevant patterns in the spec's Constraints section so Codex doesn't reinvent
or contradict existing conventions.

## Decision Flow

Classify by **risk first**, LOC second. A 15-line function touching GPU memory
is riskier than a 150-line data formatter.

**Risk flags** (any one → HIGH-RISK): math/numerical, public API change, data
mutation, concurrency, security, GPU memory, model loading, evaluation pipeline.

```
HIGH-RISK  (any risk flag, OR >100 LOC)
  → Preflight → Spec (user confirms) → Phase A (RED) → gate → Phase B (GREEN)
    → dual review (Claude + Codex read-only) → iterate

NORMAL     (no risk flags, 20-100 LOC, 1-3 files)  [default]
  → Preflight → Spec (user sees, auto-proceed) → Phase A → gate → Phase B
    → Claude review → Done

TINY       (<20 LOC, single file, mechanical, no risk flags)
  → Single Codex call (test + impl) → Claude diff check → Done
```

## Preflight

1. **MCP check** — `mcp__codex__codex` + `mcp__codex__codex-reply` available?
   If not, offer to implement directly.
2. **Branch** — confirm not on main/master (or get user approval).
3. **Snapshot** — `BASELINE_COMMIT=$(git rev-parse HEAD)`,
   `git stash create "codex preflight"`.
4. **Allowed write set** — list exact files Codex may touch. Everything else
   is off-limits.

## Spec

The spec is the only context Codex receives — be precise and complete. Vague
specs produce vague tests, and the adversarial split amplifies spec flaws.

```
## Task
[What to build/fix and why — one paragraph]

## Allowed Write Set
- test: [exact paths]
- impl: [exact paths]
- forbidden: data/*, models/*, results/*, paper/*

## Acceptance Criteria
- [Concrete, numbered assertions and edge cases]

## Constraints
- Python 3.10+, pytest, type hints
- TEST_CMD: [project test command]
```

**Good spec vs bad spec:**

| Bad | Good | Why |
|-----|------|-----|
| "Add caching" | "Add LRU cache (maxsize=128) to `get_covariance()`. Cache key: `(layer_idx, name)`. Return cached tensor on hit." | Codex can't infer cache strategy, size, or key from "add caching" |
| "Handle edge cases" | "Return empty tensor `(0, d)` when input batch is empty. Raise ValueError when rank < 1." | Codex needs exact behavior, not a vague directive |
| "Fix the compression bug" | "In `compress_linear_whitening_from_covariance`, when the Cholesky fallback triggers, the regularized matrix isn't re-normalized. Divide by N after adding eps to the diagonal." | Codex can't debug — it needs the root cause and the fix |

### Spec Preview

Always show the spec to the user before sending to Codex. The user catches
wrong acceptance criteria, missed edge cases, and incorrect assumptions that
Claude's self-review would miss — LLMs are often confidently wrong about
their own understanding.

- **HIGH-RISK / unclear scope / public API / user-visible behavior change**:
  Block and wait for explicit user confirmation.
- **NORMAL / TINY with clear requirements**: Show the spec as
  "Here's what I'm sending to Codex" and proceed unless the user objects.

## Phase A — RED (Codex writes tests)

See `references/codex-prompts.md` for the MCP call template. Codex writes
failing tests only — no implementation files.

### Claude's Quality Gate

Run these checks before Phase B. Bad tests waste everyone's time — Codex-B
will spend rounds trying to pass unfixable or meaningless tests.

| # | Check | Why | Action on failure |
|---|-------|-----|-------------------|
| 1 | `git diff --name-only` shows only test/fixture files | Codex sometimes writes impl "to help" — defeats the adversarial split | `git checkout BASELINE -- <impl files>`, retry |
| 2 | Tests fail with behavioral error (AssertionError, ValueError) | ImportError/SyntaxError means the test can't even run | Clarify imports in the spec and retry |
| 3 | Tests assert requirements, not implementation internals | Tests coupled to `_internal_method()` break on valid refactors | Reject: "Assert the output shape and values instead" |
| 4 | A wrong-but-type-correct impl would fail | Tautological tests give false confidence | Reject: "Any function returning a `(d, r)` tensor passes — add `assert_close` on known values" |
| 5 | Failure messages are diagnostic | Codex-B reads assertion messages to understand intent | Suggest adding `msg=` to assertions if missing |
| 6 | Every acceptance criterion has a corresponding test | Tests can be high-quality individually but miss requirements | Map: criterion → test name → assertion → expected RED failure |
| 7 | Mutation-lite challenge (tiered) | Catches tests that look behavioral but accept wrong implementations | See below |

**Gate #6 — Spec-test traceability**: Build a quick matrix mapping each
numbered acceptance criterion to the test that covers it. If a criterion has
no test, send Codex-A back to add one. This catches the gap between "tests
are good" and "tests are complete."

**Gate #7 — Mutation-lite** (soft for NORMAL, hard for HIGH-RISK): Name a
specific wrong-but-type-correct behavior that would violate an acceptance
criterion, then verify the tests would catch it. Soft = log the concern and
proceed if no obvious weakness; hard = block Phase B until resolved. Format:

> Wrong behavior X would violate criterion Y; test Z fails because assertion
> A checks B.

Trivial mutants ("return None") don't count unless genuinely plausible.
If Claude cannot name a non-trivial wrong behavior, the tests likely need
strengthening.

## Phase B — GREEN + REFACTOR (Codex implements)

Create a restore point — if Phase B damages the tests, you need to recover:
```bash
PHASE_A_STASH=$(git stash create "phase-a-tests")
# Also cp untracked test files to /tmp — git stash only captures tracked files
```

### What Phase B receives

Phase B gets enough to implement, but NOT Phase A's reasoning process. This
boundary preserves the adversarial split — if the implementer sees how the
tests were designed, it can game them.

**Include**: spec, allowed write set, test diff, RED command output (failures),
gate verdict (pass/fail per check — no detailed rationale), spec-test
traceability matrix.

**Exclude**: Phase A's exploratory reasoning, rejected test approaches,
implementation hints, Claude's gate review comments.

See `references/codex-prompts.md` for the template.

**Claude verifies**: run tests locally (confirm pass), check
`git diff --name-only` (only allowed files changed).

## Tiny Tier

For trivial tasks, Codex handles test + implementation in a single session
(see `references/codex-prompts.md`). Claude verifies `git diff` stays within
the allowed set and tests pass. No gate between phases, no dual review.

If the TINY call fails (Codex can't solve it in one session), upgrade to
NORMAL — write a proper spec and run the two-phase protocol.

## Dual Review (HIGH-RISK only)

Run both reviews on the frozen diff — no fixes until both report, so one
reviewer's fix can't invalidate the other's findings.

1. **Claude:** `superpowers:requesting-code-review`
2. **Codex (parallel, read-only):** see `references/codex-prompts.md`

Safety/correctness wins over style. Simpler fix wins ties. Iterate via
`mcp__codex__codex-reply` with the Phase B threadId.

## Recovery

Diagnose before retrying — blind retries burn attempts and can introduce new
issues. See `references/recovery-matrix.md` for the full diagnosis → action
mapping.

**Quick dispatch:**

| Failure type | Signal | Action |
|-------------|--------|--------|
| Syntax/import | ImportError, SyntaxError in test output | Fix spec imports/paths, retry same phase |
| Weak tests | Gate #4/#7 fails | Reject with specific feedback, retry Phase A |
| Spec ambiguity | Codex asks clarifying questions or tests miss intent | Revise spec, restart from Phase A |
| Environment | Timeout, MCP error, git conflict | Fix environment, retry same phase |
| Incomplete impl | Some tests pass, others fail | Send failing test output to Codex-B, retry Phase B |

**Reclassification rule**: After one failed targeted retry, re-read the spec,
test diff, and logs. Choose a different diagnosis or escalate to the user.
Do not spend two retries on the same diagnosis without new evidence.

**Escalation**: After 2 same-diagnosis failures OR 3 total retries in any
phase, tell the user what's failing and offer to take over. Environment
retries (MCP timeout, git conflict) don't count toward the phase retry
budget — they're infrastructure issues, not code issues.

## Cleanup

The user can abort at any point — run cleanup and report what was completed.

Only revert Codex-owned changes. Ask before touching user's pre-existing
dirty state.

```bash
git checkout ${BASELINE_COMMIT} -- <impl_files>
git stash apply ${PHASE_A_STASH}
rm <unauthorized_new_files>
```

Never `git reset --hard` / `checkout -- .` / `clean -fd` — these destroy
user work. Targeted reverts are safer and auditable.
