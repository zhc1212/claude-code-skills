---
name: codex-debug-pair
description: "Cross-model pair-debugging: when Claude encounters a non-trivial bug, both Claude and Codex (GPT via MCP) independently form hypotheses about the root cause, then compare and synthesize. Leverages different training distributions to expand the hypothesis search space and avoid confirmation bias. Use when user says \"codex debug\", \"codex help debug\", \"cross-model debug\", \"pair debug with codex\", \"codex一起debug\", \"让codex帮我找bug\", \"codex调试\", \"两个模型调试\", \"codex帮我排查\", \"两个模型一起调试\". Not for code review (/codex-review), implementation (/codex-tdd-implementer), or debate (/codex-debate). Not for trivial bugs (typos, import errors, missing semicolons) that don't benefit from cross-model hypothesis diversity."
---

# Codex Debug Pair

Cross-model pair-debugging for non-trivial bugs. Claude and Codex form
independent blind hypotheses about the root cause, then compare and
synthesize. This works because Claude and GPT have different training
distributions and different blind spots -- a hypothesis that one model
misses, the other often catches. The protocol is designed to prevent
anchoring: Codex never sees Claude's hypotheses, and synthesis happens
only after both complete.

Not every bug needs this. Typos, import errors, and obvious shape
mismatches are faster to fix directly. Use this when the root cause is
genuinely unclear, the bug involves numerical instability, unexpected
model behavior, or when a first debugging attempt already failed.

## Protocol Overview

```
1. Gather bug context (error, logs, recent changes, affected code)
2. Claude forms 3-5 independent hypotheses (shown to user, hidden from Codex)
3. Build neutral evidence packet (error + context, NOT Claude's hypotheses)
4. Codex forms blind independent hypotheses via MCP
5. Compare: both-flagged = high priority; unique = new leads
6. Design verification experiments for top hypotheses
7. Execute tests, update hypothesis confidence
8. Present root cause or escalate if unresolved after 2 rounds
```

## Phase 1: Bug Context Gathering

Collect everything relevant before forming hypotheses. Thorough context
prevents both models from wasting rounds on hypotheses that a quick
`git log` or stack trace would have ruled out.

1. **Error signal**: exact error message, stack trace, or anomalous output.
   If the user provided a partial trace, ask for the full one -- truncated
   traces hide the actual failure site.

2. **Reproduction**: what command triggers the bug, how reliably, any
   conditions (specific GPU, specific model size, specific ratio).

3. **Recent changes**: `git log --oneline -10` and `git diff HEAD~3` to
   identify what changed near the failure window.

4. **Affected code**: read the files at the failure site. Follow the call
   chain up and down one level -- bugs often live in the caller or the
   callee, not the function that throws.

5. **Expected vs actual**: what should happen, what happens instead, and
   how the user knows it's wrong (metric, assertion, visual output).

If genuinely ambiguous, ask ONE clarifying question. Otherwise start.

## Phase 2: Claude's Independent Hypotheses

Form 3-5 hypotheses BEFORE any interaction with Codex. This order is
non-negotiable: if you build the Codex prompt first, you unconsciously
frame the evidence toward your own suspicions, which defeats the
independence that makes cross-model debugging valuable.

Each hypothesis follows this structure. Bare claims ("it's probably a
shape mismatch") hide the reasoning chain and make it impossible to
design targeted verification. The structure forces specificity.

```
### H{N}: {one-line hypothesis}
**Evidence**: {what in the logs/code/behavior points to this}
**Mechanism**: {how this root cause produces the observed symptoms}
**Confidence**: {high / medium / low} because {reason for confidence level}
**Falsifier**: {a specific test or observation that would rule this out}
```

Example for an SVD-LLM numerical bug:

```
### H1: Covariance not normalized before whitening
**Evidence**: PPL is 14.2 instead of expected ~6.1; whitening.py L38
  receives (XtX, N) tuple but caller passes XtX without dividing by N
**Mechanism**: unnormalized covariance inflates eigenvalues, causing
  whitening matrix S to over-scale, which distorts the SVD truncation
**Confidence**: high -- because the covariance normalization gotcha is
  documented in compression-api.md and this exact pattern caused a
  prior bug (project_phase2_v3_results.md)
**Falsifier**: print XtX.max() before and after normalization; if
  values are already O(1), this hypothesis is wrong
```

Record hypotheses privately -- do not show to user yet. The user sees
them AFTER Phase 3 packet construction. Do NOT include them in the
Codex prompt.

## Phase 3: Neutral Evidence Packet

Build the neutral evidence packet FIRST, then show Claude's hypotheses
to the user. This order prevents user feedback from biasing the packet.
The packet contains facts, not interpretations -- it must be frozen
before the user sees Claude's hypotheses and reacts to them.

**Include:**
- Error message and full stack trace
- Relevant code snippets (functions at the failure site, callers, callees)
- Recent git changes near the failure
- Expected vs actual behavior
- Environment details (GPU, model, ratio, dtype) when relevant
- What has already been tried and failed (if any prior debugging)

**Exclude:**
- Claude's hypotheses or suspicions
- Claude's interpretation of why specific code is suspicious
- Leading questions that telegraph a particular root cause

The packet should be factual substrate that any competent debugger could
use as a starting point. If you catch yourself writing "this suggests
that..." or "notably, this line...", you're editorializing -- rewrite
as neutral description.

## Phase 4: Codex Blind Hypotheses

Send the evidence packet to Codex via `mcp__codex__codex` with
`config: {"reasoning_effort": "xhigh"}`. The high reasoning effort is
worth it here because hypothesis generation benefits from deeper
exploration of the search space.

```
## Independent Bug Investigation

### Bug Report
{error message, stack trace, reproduction steps}

### Affected Code
{relevant code snippets}

### Recent Changes
{git log / diff excerpts}

### Expected vs Actual
{what should happen vs what happens}

### Prior Attempts
{what debugging has been tried, if any}

### Task
You are investigating this bug independently. Another model has also
formed hypotheses, but you will not see them until after you submit
yours. This independence is deliberate -- different models catch
different failure modes.

Form 3-5 hypotheses about the root cause. For each:
- **Hypothesis**: one-line description
- **Evidence**: what in the code/logs/behavior supports this
- **Mechanism**: how this root cause produces the observed bug
- **Confidence**: high / medium / low, with reasoning
- **Falsifier**: a specific test that would rule this out

Also provide:
- **Most likely root cause**: your top pick and why
- **What you would test first**: the single most informative experiment
```

Save the `threadId` -- follow-up rounds use `mcp__codex__codex-reply`.

If Codex MCP is unavailable (connection error, timeout), tell the user
and offer to proceed as solo debugging with Claude's hypotheses only.

## Phase 5: Cross-Model Synthesis

Compare Claude's and Codex's hypothesis sets. Sort into three buckets.
The bucket determines priority because convergent diagnosis from
independent sources is stronger evidence than a single model's guess.

### Bucket 1: Both-Flagged (high priority)

Hypotheses where both models independently identified the same root
cause or closely related mechanisms. These go to the top of the
verification queue because independent convergence is strong signal.

For each: note how the two framings differ -- sometimes one model's
version is more precise or testable than the other's.

### Bucket 2: Codex-Only (new lead)

Hypotheses Codex raised that Claude missed. These are the primary value
of cross-model debugging -- they expand the search space into areas
Claude's training distribution underweights. Present them with Codex's
evidence and assess whether Claude finds them plausible on re-examination.

### Bucket 3: Claude-Only (re-examine)

Hypotheses Claude raised that Codex missed. Re-examine each one: is
there a reason Codex might have missed it (e.g., it requires domain
knowledge about SVD numerics that GPT may underweight), or did Claude
over-index on a red herring? Adjust confidence accordingly.

### If No Hypotheses Overlap

If Claude and Codex produced entirely different hypothesis sets (zero
both-flagged), this is informative, not alarming -- it means the two
models explored different parts of the search space. Rank all hypotheses
by `confidence x falsifier speed` (high confidence + fast falsifier =
test first). The fastest experiment to run should go first regardless
of which model proposed it.

### Synthesis Output

Present to the user:

```
## Cross-Model Hypothesis Comparison

### Both flagged (high priority):
- {hypothesis} -- Claude: {confidence}, Codex: {confidence}
  Nuance: {how the two framings differ}

### Codex-only (new leads):
- {hypothesis} -- Codex: {confidence}
  Claude's assessment: {plausible / skeptical, with reason}

### Claude-only (re-examined):
- {hypothesis} -- Claude: {confidence, possibly adjusted}
  Why Codex may have missed: {reason}

### Recommended verification order:
1. {hypothesis} -- test: {falsifier} -- expected result: {what confirms/denies}
2. ...
```

## Phase 6: Verification Experiments

Design concrete tests for the top 2-3 hypotheses. Each test should be
a specific action with a predicted outcome that distinguishes between
root causes. Vague tests ("add some logging") waste rounds -- be precise
about what to log, where, and what value range confirms vs denies.

```
### Experiment {N}: Test {hypothesis}
**Action**: {exact code change, print statement, or command}
**Executor**: {Claude (local command/print) | user (GPU experiment) | user (manual check)}
**Predicted if true**: {specific output or behavior}
**Predicted if false**: {specific output or behavior}
**Estimated time**: {how long this takes to run}
```

Claude executes print-statement tests and local assertions directly.
GPU experiments, model loading, and commands requiring specific hardware
need the user to run them.

Prefer experiments that are:
- **Fast**: minutes, not hours. If a full model eval takes 2 hours,
  find a proxy (single-layer check, small calibration set).
- **Discriminating**: a result that rules out multiple hypotheses at
  once is better than one that only tests a single hypothesis.
- **Non-destructive**: don't modify production code or overwrite
  experiment results. Use temporary print statements, assertions,
  or separate test scripts.

Execute the top experiment. After results arrive, update hypothesis
confidence levels and report to the user.

If the first experiment is conclusive, present the root cause and
proposed fix. If inconclusive, run the next experiment.

## Phase 7: Convergence or Escalation

### If root cause identified:

Present the finding with full evidence chain:

```
## Root Cause Identified

**Bug**: {one-line description}
**Root cause**: {what is actually wrong}
**Evidence chain**:
1. {observation} -- established in Phase 1
2. {hypothesis} -- flagged by {Claude / Codex / both}
3. {experiment result} -- confirmed in Phase 6

**Proposed fix**: {specific code change}
**Verification**: {how to confirm the fix works}

Identified by: {Claude-only / Codex-only / both models converged}
```

If appropriate, send the root cause to Codex via `mcp__codex__codex-reply`
for a sanity check on the proposed fix. This is optional -- use it when
the fix touches numerical code, concurrency, or other areas where a
second opinion on the fix itself (not just the diagnosis) adds value.

### If unresolved after 2 verification rounds:

Escalate to the user with the full hypothesis ledger rather than
grinding through low-confidence guesses. Continued rounds with no
convergence waste time and can introduce false confidence.

```
## Escalation -- Root Cause Not Converged

**Rounds completed**: {N}
**Hypotheses tested**: {list with results}
**Remaining candidates**: {hypotheses not yet falsified, with confidence}

**Recommended next steps**:
- {most informative experiment we haven't tried}
- {alternative approach: e.g., bisect, minimal repro, different model}
- {external resource: e.g., library issue tracker, paper reference}

**Full hypothesis ledger**:
| # | Hypothesis | Source | Confidence | Status |
|---|-----------|--------|------------|--------|
| H1 | ... | Both | high->low | Falsified by experiment 1 |
| H2 | ... | Codex | medium | Open -- not yet tested |
| ... | ... | ... | ... | ... |
```

## Saving the Debug Session

For non-trivial bugs (2+ phases, multiple hypotheses), save the session to
`docs/debug-sessions/{date}-{slug}.md` with: evidence packet, hypothesis
ledger (both models), verification results, and resolution. This helps
when similar bugs recur -- the ledger is a searchable diagnostic record.

## Behavioral Rules

- **Independence is the protocol's value**: Claude's hypotheses stay
  private from Codex. Codex's prompt contains only the neutral evidence
  packet. If you include Claude's suspicions in the Codex prompt, you
  reduce the protocol to a single-model debug session with extra latency.

- **Evidence over plausibility**: a hypothesis that sounds reasonable but
  cites no specific code line or log entry is weaker than an awkward
  hypothesis backed by a concrete observation. Tag confidence honestly.

- **Concede when falsified**: if an experiment rules out your top
  hypothesis, update confidence immediately and say what changed. Clinging
  to a falsified hypothesis wastes verification rounds.

- **Falsifiers are mandatory**: every hypothesis needs a specific test
  that would rule it out. Unfalsifiable hypotheses ("something is wrong
  with the model") are not hypotheses -- they are complaints. Rewrite
  them with specificity or drop them.

- **Fast experiments first**: order verification by time-to-result, not
  by hypothesis confidence. A 30-second print-statement test that rules
  out a medium-confidence hypothesis is better than a 2-hour eval run
  that tests the top hypothesis.

## Codex MCP

- **First call**: `mcp__codex__codex` with `config: {"reasoning_effort": "xhigh"}`
- **Follow-ups**: `mcp__codex__codex-reply` with saved `threadId` + `prompt`
- Starting a fresh `mcp__codex__codex` mid-session erases Codex's memory
  of the evidence packet and prior hypotheses -- always use the reply
  endpoint after the first call
- On MCP error (including initial connection failure): tell the user, ask
  whether to retry or proceed with Claude-only debugging
