# Remediation loop

Read before the first fix. The budget is two Codex rounds: round 1 is done, and
round 2 is the only review your fixes will get.

## Fix

Fix material blockers only; deferred, borderline and candidate items stay as
recorded. Each fix follows a test written and observed red first (SKILL.md step
4). When a fix touches a dimension, reset that dimension to `not-assessed` until
round 2 accounts for it: round 1's `security: checked` says nothing about
middleware a fix rewrote.

## Class sweep: search wide, fix narrow

For each confirmed blocker ask: **this code answers some question — where else
does it answer the same question?** One defect usually has several shapes, and
re-reading the same file never finds the others. Gate each instance separately
(its own oracle, materiality, scope check). Fix the in-scope instances; record
out-of-scope ones as deferred with the class named.

## Round 2: the delta prompt

Batch every fix into this one call, and send this prompt rather than the round-1
template, which reopens settled code. The delta is usually uncommitted: state how
it is obtained (`git diff`, `git diff --cached`, the untracked list), and leave
the user's index and commit history as they are.

```
mcp__codex__codex-reply:
  threadId: <saved>
  prompt: |
    Delta round — the last of a 2-round budget. Reviewing the fixes applied
    since your last message. Nothing after this round is cross-reviewed: every
    MATERIAL item you report gets fixed with no review after it, so promote only
    what the gate admits, and anything material you leave out ships unreviewed.

    Tree: <absolute path>. Verify `git rev-parse HEAD` there is <current sha —
    fixes have moved it since the snapshot> before reading; on mismatch, report
    and stop.

    Delta: <exact command(s), including uncommitted work> + untracked: <paths>
    Fixes applied: <id → what changed>
    Evidence added: <tests or other channels, with paths>
    Dimensions a fix touched, now reset to not-assessed: <list>

    [paste the gate block verbatim]
    [paste the frozen delivery policy]

    Read whatever you need, including code outside the delta and the other
    members of any class a fix claimed to close. Report outside-delta findings
    only as evidence that a targeted class is not closed, or that the delta
    caused a regression. Settled findings have been ruled on; raise one again
    only if the delta made it material, and say which change did.

    Answer only these four questions.
    1. Did each fix close the class it targeted, or only the reported instance?
       Name the other class members you checked.
    2. Did any fix introduce a new defect, or weaken a check that existed before?
       For each, add FIX DIRECTION (two lines, never a patch: the smallest
       change that rights it, then what that change must not break).
    3. For each new test or evidence artifact: does its expectation come from an
       oracle outside the change, and would it distinguish the pre-fix state from
       the post-fix state? Name any that would pass regardless.
    4. For each dimension listed as reset above: checked / n-a / not-assessed,
       with the paths or checks inspected.
```

Update the ledger scratch file with the round-2 result before acting on it.

## Stop at the cap

When round 2 is spent: attempt the evidence for its candidates and fix its
material blockers. That is the last edit. Then report, without letting a
clean-looking summary imply the SKILL.md stop conditions were met:

- every open blocker, candidate, unresolved risk and `not-assessed` dimension as
  **open at the cap**, not as resolved or absent,
- every fix applied after round 2 as **not cross-reviewed**,
- the affected suite and evidence channels, re-run once more, as what the
  shipped state rests on,
- a one-line offer of a third round, which is the user's call on the ledger in
  front of them.
