---
name: codex-review
description: "Cross-model adversarial code review via Codex MCP: Codex reads the repo itself, findings pass an oracle + materiality gate, and everything else goes to a ledger. Audit-only by default; fixing requires the user to ask for it, and runs at most two Codex rounds. Use when the user wants Codex to review code, a branch, a PR, or a commit range — \"codex review\", \"让codex review这个PR/分支\", \"codex审代码\", or \"keep fixing until codex is happy\". Not for papers (/codex-paper-adversary), a known bug (/codex-debug-pair), experiment design (/codex-experiment-critic), architecture debate (/codex-debate), standards+spec review (/code-review), or the ML-paper score loop (/auto-review-loop)."
---

# Codex Review

Adversarial code review from GPT via Codex MCP. GPT and Claude have different
blind spots, and Codex reading the repo itself sees what a curated diff would
hide. But an LLM asked to find problems always finds one more: every finding
becomes a fix, fixes breed defects, and the change never ships. The gate and the
round cap below end that loop.

## Modes and round budget

| Mode | When | Codex rounds | Edits |
|---|---|---|---|
| **audit** (default) | The user asked for a review | 1 | None to code or tests |
| **remediation-loop** | The user asked to fix findings, or to iterate until clean | 2: the full sweep, then one delta round over the fixes | Material blockers only |

- **A round is one Codex MCP call**: `codex` for round 1, `codex-reply` for
  round 2. Claude's blind pass, evidence attempts, class sweeps and fixes are not
  rounds.
- Round 2 runs only if a fix followed round 1.
- **Fixes applied in response to round 2 ship without cross-model re-review**,
  and the report says so. A third round happens only when the user asks for it
  by name, having seen the round-2 ledger.
- Work arriving after the loop stopped is a **new review** with its own
  snapshot, ledger, budget and round 1, scoped to the new delta.
- A material blocker found in audit mode is reported with an offer to fix; the
  fixing waits for the user.
- Audit skips remediation, not the completeness check in [Stop](#6-stop).

## The gate

Paste **this block verbatim** into every Codex prompt and apply it unchanged
during triage. A gate with three wordings has three meanings.

> A finding is a **material blocker** only if all four hold:
>
> 1. **Oracle** — the expected behaviour comes from a source *outside the change
>    under review*: an acceptance criterion, a documented contract, an existing
>    caller, a standard, a domain or mathematical fact, an invariant stated
>    outside this change, or a fixture whose provenance was independently
>    checked. An invariant, comment, or assertion the change itself introduces is
>    **not** an oracle — it is evidence of intent, and if it disagrees with the
>    code it is an internal inconsistency to report, not a truth to conform to.
>    Reviewer preference is never an oracle.
> 2. **Attribution** — the bad state is reachable, and this change caused it, made
>    it newly reachable, or made it materially worse. Merely *noticing* an old
>    defect while reading this change is not attribution.
> 3. **Materiality** — shipping it violates the frozen delivery policy: a stated
>    requirement, a contract/build/deploy something relies on, a supported path
>    that would crash or hang, a corrupted result, security or data risk, or a
>    false claim published in an artifact.
> 4. **Evidence, produced now** — run, not planned. Preferred: a test that fails
>    on the pre-fix state and passes after. Also accepted: a deterministic
>    reproduction, a static contract or data-flow argument over the cited lines, a
>    benchmark against a declared threshold, or an artifact-versus-source
>    comparison. Name the channel; it is the same channel that must be re-run to
>    verify the fix.
>
> Three consequences, all load-bearing:
>
> - **An immaterial finding is not a blocker, red test or not.** Testability
>   measures observability, not severity.
> - **Material, but evidence not yet produced → `candidate`**, not blocker.
>   Producing the evidence is what promotes or dissolves it.
> - **Material, and evidence not producible in this environment → `unresolved
>   risk`**, which the user disposes of. Being unable to reproduce something is
>   never itself proof that the finding is a preference.

Testability screens out nothing: any preference (an input policy, a naming
convention, a default) can be encoded as a red test. The 9-round loop that
motivated this skill went 4, 2, 11, 5, 3, 4, 1, 1, 1 findings, and the last
three were trivially testable and still not worth a round. Materiality is a
judgement call, so it is frozen as the delivery policy in [§0](#0-snapshot)
before round 1, never re-decided per round.

## Ledger

One ledger with **stable ids** from round 1 to the end. A finding stays on it
until it exits its bucket.

| Bucket | Meaning | Exit |
|---|---|---|
| **blocker** | All four gate conditions met | Fix → `resolved` (remediation-loop only) |
| **candidate** | Material claim, evidence not produced yet | Evidence attempt → another bucket. Never expires unattempted |
| **unresolved risk** | Material, evidence not producible here | The user's call; carried until they make it |
| **borderline** | Materiality genuinely arguable under the frozen policy | Reported as `user-decision` |
| **deferred** | Real but immaterial, or out of scope: pre-existing, adjacent, style, speculative callers, missing tests for correct behaviour | Recorded |
| **rejected** | Verified wrong: misread code, false assumption, already handled | Recorded with the quoted code or test that shows it |

Each entry carries a state: `new / carried / resolved / reopened / fix-induced`.
The last two are what make a grinding loop visible.

**The ledger lives on disk.** After every round, write ledger + `threadId` +
round count + snapshot to a scratch file in an already-ignored directory, e.g.
`.claude/codex-review-<branch>.md`. A continuation session resumes with
`codex-reply` and the delta prompt; if the thread is gone, a fresh `codex` call
carries the delta prompt plus the ledger verbatim, and the round count carries
over. One review = one ledger = one thread; concurrent reviews are keyed by
branch.

## Protocol

### 0. Snapshot

Record once; it stays fixed for the whole review:

- **Tree**: absolute path of the checkout that holds the delta, and its
  `git rev-parse HEAD`. In a worktree flow this is the worktree; the primary
  checkout answers every question about the wrong code.
- **One exact diff command**, endpoints as SHAs, pasted identically everywhere.
  Three-dot (`<merge-base>...HEAD`) when the base may have advanced;
  `<sha>^..<sha>` for a single commit.
- **Untracked delta paths**, listed separately; no `git diff` shows them.
- Dirty state in scope (staged / unstaged / untracked), and whether the relevant
  suite is green before any change.
- **Delivery policy**, the frozen materiality threshold pasted into every prompt:
  - *Acceptance criteria* and the source of each. From repo docs, CI config, or
    the issue: a requirement. From the change's own commit message or
    docstrings: **intent**, so a finding against it is an internal
    inconsistency, still material.
  - *Supported paths*: OS, runtimes, test and lint commands.
  - *Environment and concurrency envelope*: name each axis in or out — umask and
    permissions, read-only or case-insensitive filesystems, concurrent
    processes, two versions of this code meeting mid-upgrade. A finding on an
    unnamed axis defaults to `borderline`.
  - *Exclusions* the user stated.

Findings about code the diff does not touch are **deferred as pre-existing** by
default.

### 1. Claude's blind pass

Write your own candidates **before** reading Codex's output. Triage done after
reading it can only rank Codex's findings, never surface what Codex missed. One
line each:

```
claim | oracle (or: no oracle found) | scenario | evidence route | confidence | falsifier
```

For each dimension in the round-1 prompt, either a candidate or
`no candidate after inspecting <paths / checks>`. Vary the envelope axes, not
only the inputs: a restrictive umask once crashed a change on its first launch,
leaving a zero-byte file that no input-varying pass caught.

### 2. Round 1

Send the [round-1 prompt](#round-1-prompt) with `cwd` = the snapshot tree and let
Codex read; a curated diff defeats the point. Save the `threadId`. Check each
`n-a` against the file inventory yourself: "persistence: n-a" over a diff with a
migration is a false claim.

### 3. Triage

Deduplicate the union of both passes and bucket each item against the gate.

### 4. Attempt the evidence

Every candidate gets an attempt before any fix; the result decides its bucket.
A test needs both:

- **Independent oracle**: the expectation cites a source outside the change. An
  expectation read off the implementation pins nothing, e.g. comparing a sort
  against `sorted()` of the same keys.
- **Sensitivity**: it fails on the pre-fix state. Write it before the fix and
  record the red result.

Non-test channels (static argument, benchmark, artifact comparison) need the same
two: an outside oracle, and a result that differs before and after. Record the
channel; it is the one re-run to verify.

**A finding about a test is discharged by mutation.** Break the code the test
claims to pin and run it: green confirms the finding, red kills it. Mutating
along the envelope axes also finds tests that are missing.

Use a throwaway copy or a temporary `git worktree` for mutation, for a pre-fix
check after a fix is already applied, and for every audit-mode evidence attempt
(audit edits nothing in the shared tree). Never `stash`, `revert`, `checkout`, or
reverse-patch the shared worktree to get a pre-fix state: that moves work that may
belong to another session, and the stash stack is shared across worktrees.

### 5. Remediation

Audit mode goes straight to Stop. In remediation-loop, **read
[remediation.md](remediation.md) before the first fix**; it holds the fix rules,
the class sweep, the round-2 prompt, and what to do at the cap.

### 6. Stop

A review is **complete** when every candidate has been attempted and
re-triaged, and no dimension is `not-assessed`, including any a fix reset.
Remediation-loop additionally needs:

- zero open blockers,
- every `unresolved risk` and `borderline` item disposed of by the user (listing
  one is not disposing of it),
- verification green on the evidence channel used, plus the affected suite, with
  any skipped coverage named.

"This round reported nothing" is not completeness; a thin or timed-out review
reports nothing too. An incomplete audit is reported as **incomplete**, with a
retry or fallback offer, not as a verdict. When round 2 is spent with items still
open, follow the cap rules in [remediation.md](remediation.md#stop-at-the-cap).

**Unattended runs** (hook-driven, nobody to answer): write the full report and
the scratch-file ledger, leave the PR unmerged and the issue open, name the
failed stop condition in both, and move to work that does not depend on this
review. A hook condition like "merge when the review is clean" authorises the
not-merging, not a PR comment.

## Round 1 prompt

```
mcp__codex__codex:
  model: gpt-6-astra
  sandbox: read-only
  cwd: <the tree from the snapshot — the worktree, not the primary checkout>
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    Adversarial code review, round 1. You have read access to this repo — read
    what you need; nothing has been curated for you.

    Tree: <absolute path>. Before reading anything else, run `git rev-parse
    HEAD` there and compare to <sha>. On mismatch, report the mismatch and
    stop: every finding would describe code nobody is shipping.

    Scope: <the one exact diff command, endpoints as SHAs> + untracked: <paths>.
    Code outside that is pre-existing and out of scope unless this change made it
    reachable.

    [paste the gate block verbatim]
    [paste the frozen delivery policy]

    Report in four parts.

    COVERAGE — per dimension: checked / n-a / not-assessed, plus the paths or
      checks you inspected, and for n-a the reason it does not apply. Vary the
      environment and concurrency envelope the policy names, not just the inputs.
      Dimensions: correctness on real inputs; concurrency and ordering; resource
      lifecycle (files, locks, handles, temp dirs); error and partial-failure
      paths; interface contract vs. callers; security and authorisation;
      persistence and migrations; test validity — does each test fail if the
      behaviour it claims to pin is broken, or does it assert whatever the
      implementation happens to do? Performance only if an SLO or complexity
      contract exists.

    MATERIAL — all four gate conditions met, evidence already produced by you.
      Per finding: id, file:line, dimension, one-line claim, the oracle (from
      outside this change), the scenario (input/state/sequence → wrong outcome),
      the consequence under the delivery policy, the evidence you produced and
      how, a falsifier, and FIX DIRECTION.

      FIX DIRECTION is two lines, never a patch: the smallest change that makes
      the scenario come out right, at the level of "which function does what
      differently"; then what it must not break (callers, invariants, tests),
      plus the alternative if there is a real fork. If you cannot name a fix,
      say what makes it hard; the finding still stands.

    CANDIDATE — material if true, but you could not produce the evidence here.
      Same fields, plus the evidence route you would use and why you could not
      run it. A finding whose evidence is only planned belongs here.

    NON-BLOCKING — everything else, one line each. No scenario, no fix
      direction; a finding does not become material by being easy to fix.

    An empty MATERIAL list is a valid and useful verdict; a short one is the
    normal result for a reviewed change. Putting a NON-BLOCKING item in MATERIAL
    is the one outcome that damages this review.
```

## Report

```markdown
## Codex review — round N (<mode>)

**Scope**: <command, SHAs> (+ untracked: <paths>) | **Policy**: <one line, or a link>
**Coverage**: <n> checked, <n> n/a, <n> not assessed <— name them if any
**Ledger**: <n> blockers open, <n> fixed, <n> candidates open, <n> unresolved, <n> borderline, <n> deferred, <n> rejected
**Blockers per round**: 3, 0   ← the convergence trace
**Fix-induced / reopened**: <n> / <n>
**Round budget**: N of <1 audit | 2 remediation> spent <— at the cap, name what is open and offer a third round

### Blockers — evidence produced, not fixed  (audit mode: this is the whole answer; offer the remediation loop)
- **M01** `file:line` — <claim>. Oracle: <source; requirement or intent>.
  Evidence: <channel> — <observed result>. Consequence: <under the policy>.
  Fix direction: <smallest change> — must not break <constraint>. Advisory, not applied.

### Fixed  (remediation-loop only)
- **F01** `file:line` — <claim>. Oracle: <source>. Evidence: <channel> — <pre-fix result, observed>.
  Verified: <same channel re-run> + <suite>. Fix: <what changed>. Cross-reviewed: <round 2 | no — after the final round>.

### Open candidates
- **C01** <claim>. Evidence attempted: <what, and what it showed>. Fix direction: <…>. Advisory, not applied.

### Needs your call
- **U01** <claim>. Material because <consequence>. Evidence not producible here because <why>. Fix direction: <…>.
- **B01** <claim>. Borderline under the policy because <both readings>.

### Deferred — recorded, not published
- **D01** `file:line` — <claim>. Why: immaterial / pre-existing / out of scope.

### Rejected
- **R01** <claim> — wrong because <the code or test that shows it>.
```

The full ledger always goes to the user. Writing it into a PR body, issue
comment, or commit trailer is an external write that needs the user to ask, and
then only the items they accept as real debt go out.

## MCP

**Call shape.** `model` and `sandbox` are top-level parameters of
`mcp__codex__codex`; reasoning effort goes in `config` as
`model_reasoning_effort`. A bare `reasoning_effort` key passes schema validation
(`config` is `additionalProperties: true`) but is silently ignored, leaving the
model default `low` — verified by a live call on 2026-09-04. Use `xhigh`; reserve
`max`/`ultra` for genuinely subtle code. `gpt-6-astra` answered a live call on
2026-09-24; an unsupported model name returns HTTP 400 rather than falling back,
so that error means the pin needs updating, not a transient failure.

**On failure before any edit**: tell the user, offer a Claude-only review, and
name what is lost: cross-model blind-spot coverage, and a reviewer that reads the
repo without Claude choosing what it sees. **Mid-loop, after fixes are applied**:
stop editing, keep the ledger and the last green verification, report both, and
ask whether to retry or finish as an explicitly labelled Claude-only review.
