---
name: codex-tdd-implementer
description: "Delegates coding to Codex via TDD — Claude writes a compact spec, Codex writes tests then implementation. Two modes: FAST (default, single Codex session) for daily tasks, ADVERSARIAL (isolated Phase A/B) for high-risk code. Designed to minimize Claude token consumption by shifting coding work to Codex. Use when user says 让codex写代码, 交给codex, codex来实现, codex来写, 让codex帮我写, codex帮我实现, codex来搞, codex来做, have codex implement, delegate to codex, let codex do it, let codex handle this, codex TDD, codex implement this, 交给codex做, codex写测试再实现, let GPT write this. Also trigger when the user wants cross-model TDD collaboration, asks Codex to build or fix a feature, or wants test-driven implementation with an independent model. Not for code review (/codex-review), debate (/codex-debate), or quick one-shot questions (/codex consult)."
---

# Codex TDD Implementer

Claude writes a compact spec. Codex writes tests and implementation. Claude
reviews the diff. The goal: shift coding tokens to Codex, keep Claude's
overhead minimal.

Two execution modes, one classification step:

```
Risk flags? (math/numerical, public API, GPU memory, concurrency,
             security, model loading, eval pipeline, >100 LOC)
  YES → ADVERSARIAL (isolated Phase A/B, 4-item gate, dual review)
  NO  → FAST (single Codex call, 2-item check)
```

**Bundled resources:**
- `references/codex-prompts.md` — MCP call templates
- `references/recovery-matrix.md` — failure diagnosis (reference only)

## Preflight (both modes)

1. **MCP check** — `mcp__codex__codex` available? If not, offer to implement directly.
2. **Branch** — confirm not on main/master (or get user approval).
3. **Snapshot** — `BASELINE_COMMIT=$(git rev-parse HEAD)`.
4. **Project context** — check conftest.py, markers, import patterns. Include
   relevant patterns in the spec so Codex doesn't contradict existing conventions.

## Spec

The spec is all Codex receives — be precise but compact. Target ~10 lines.

```
## Task
[What to build/fix — one paragraph]

## Files
- test: [paths]
- impl: [paths]
- off-limits: data/*, models/*, results/*, paper/*

## Criteria
1. [Concrete assertion]
2. [Edge case]
3. [Expected behavior on invalid input]

## Constraints
- Python 3.10+, pytest, type hints
- TEST_CMD: [project test command]
```

Do NOT write traceability matrices, mutation challenges, or multi-paragraph
rationales. The spec should take Claude <200 output tokens.

**Spec preview**: show to user as "Here's what I'm sending to Codex" and
proceed unless they object. Only block for explicit confirmation when the
task involves a public API change or the user's intent is ambiguous.

---

## FAST Mode (default)

For daily tasks: adding a method, writing an eval script, fixing a bug,
plumbing config, data loaders — anything without risk flags.

### Step 1: Single Codex Call

Send spec + instructions in one `mcp__codex__codex` call:

```
<spec>

Work in two steps:
1. Write failing tests first. Run them. Confirm they fail on behavior
   (AssertionError/ValueError), not setup (ImportError/SyntaxError).
2. Implement to pass. Run tests. Confirm all pass.

Output JSON: {"changed_files":[...],"test_exit_code":0,"pass_count":N}
```

See `references/codex-prompts.md` for full template.

### Step 2: Claude Check (2 items only)

Keep Claude's review minimal — this is where token savings come from.

1. **Scope**: `git diff --name-only` — only allowed files changed?
   If Codex touched forbidden files, `git checkout BASELINE -- <files>`.
2. **Tests check behavior**: scan the test diff — do assertions verify
   outputs/values, not internal method calls? If tests only check types/shapes,
   send one follow-up to Codex: "Add value assertions."

That's it. No mutation-lite, no traceability matrix, no diagnostic-message
check. If the tests and implementation look reasonable, done.

### If Codex Didn't Solve It

Don't diagnose and retry in a loop — that burns Claude tokens. Instead:
- If partial (some tests pass): one `mcp__codex__codex-reply` with failing
  test output. One retry, max.
- If tests pass immediately (no RED phase): Codex wrote trivial tests or
  the function already existed. Send follow-up: "Tests should fail before
  implementation — add assertions that verify the new behavior."
- If fundamentally wrong: tell the user what happened, offer to implement
  directly. Claude implementing is cheaper than multiple Codex round-trips
  with Claude orchestration overhead.
- If the task is pure refactoring (no behavior change): skip TDD entirely —
  have Codex refactor, Claude reviews the diff for behavioral equivalence.

---

## ADVERSARIAL Mode (risk flags)

For math/numerical code, GPU memory management, public API changes,
compression algorithms, evaluation pipelines, or anything >100 LOC.

This is the full isolated TDD protocol — worth the overhead because bugs
in these areas are silent and expensive.

### Step 1: Spec (user confirms)

Show spec and wait for explicit user confirmation before proceeding.

### Step 2: Phase A — RED (Codex writes tests only)

Separate `mcp__codex__codex` call. Codex writes failing tests, no impl.
See `references/codex-prompts.md` for the Phase A template.

Save the `threadId`.

### Step 3: Gate (4 items)

| # | Check | Action on failure |
|---|-------|-------------------|
| 1 | `git diff --name-only` shows only test files | `git checkout BASELINE -- <impl files>`, retry |
| 2 | Tests fail with behavioral error, not setup error | Fix spec imports, retry |
| 3 | Tests assert requirements, not implementation internals | Reject: "Assert output values, not internal calls" |
| 4 | Every acceptance criterion has a corresponding test | Send Codex back to add missing tests |

For HIGH-RISK, also run a quick mutation challenge: name one wrong-but-
type-correct behavior, verify tests would catch it. If they wouldn't,
reject with specific feedback.

### Step 4: Phase B — GREEN (Codex implements)

New `mcp__codex__codex` call with: spec + test diff + failure output.
Do NOT include Phase A's reasoning — preserve adversarial isolation.

Verify: tests pass + only allowed files changed.

### Step 5: Review

Run `superpowers:requesting-code-review` on the frozen diff. For critical
code, also run a Codex read-only review in parallel (see prompts reference).

### Recovery

See `references/recovery-matrix.md` for diagnosis → action mapping.
Rule: max 2 retries per phase, then escalate to user.

---

## Cleanup

On abort, only revert Codex-owned changes:
```bash
git checkout ${BASELINE_COMMIT} -- <impl_files>
```

Never `git reset --hard` / `checkout -- .` / `clean -fd`.

## Codex MCP

- **All calls**: `config: {"model": "gpt-5.6-sol", "reasoning_effort": "max"}`
- **FAST**: single `mcp__codex__codex`, save threadId for one follow-up
- **ADVERSARIAL Phase A**: `mcp__codex__codex`, save threadId
- **ADVERSARIAL Phase B**: fresh `mcp__codex__codex` (isolated from A)
- **Retries**: `mcp__codex__codex-reply` with saved threadId
- On MCP error: tell user, offer Claude-only implementation
