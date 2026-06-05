---
name: codex-debate
description: Conducts structured multi-round debates between Claude and Codex (GPT via MCP) on research directions, code architecture, experiment design, or technical tradeoffs. Elicits independent blind opening positions using Toulmin argumentation, identifies cruxes, requires steel-manning before rebuttals, and synthesizes a consensus or documented disagreement with calibrated confidence. Use whenever the user wants two models to deliberate — triggers on "和codex讨论", "codex debate", "codex brainstorm", "让codex和你辩", "多轮探讨", "头脑风暴codex", "cross-model debate", "codex discuss", "两个模型讨论", "让两个模型辩一下", "两个AI讨论", "pros and cons with codex", "和codex头脑风暴", "codex 你怎么看" (when back-and-forth is intended). Not for code review (/codex-review) or quick one-shot questions (/codex consult).
---

# Codex Debate

Stress-test technical decisions by eliciting independent positions from Claude and
Codex, identifying cruxes, and producing either a justified consensus or a clear
record of unresolved tradeoffs. The protocol uses Toulmin argumentation and
calibrated confidence to ensure reasoning quality, not just persuasive prose.

## Protocol Overview

```
1. Gather context → build neutral evidence packet
2. Claude forms Toulmin-structured position (shown to user, hidden from Codex)
3. Codex forms BLIND independent position (evidence packet + topic only)
4. (Optional) Codex requests one round of targeted raw evidence
5. Compare → identify cruxes → build crux ledger → user checkpoint
6. Focused rounds on cruxes (expect 2-3, max 6)
7. Stop as soon as a stopping condition is met
8. Pre-synthesis check → user checkpoint → synthesize
```

## Evidence Tiers

Tag every substantive claim with a source-type label and short provenance.
This prevents "paper-backed" from meaning anything from "directly replicated"
to "vaguely inspired by." Five tiers:

| Tier | Meaning | Example |
|------|---------|---------|
| `code-inspected` | Verified by reading source | `[code-inspected: whitening.py L42 Cholesky retry]` |
| `experiment-backed` | Your own experiment (local run, ablation) | `[experiment-backed: SVD-LLM ablation table 3, this repo]` |
| `paper-backed` | Someone else's published finding | `[paper-backed: Du et al. 2023, direct multi-agent debate result]` |
| `inference` | Reasoned from known facts | `[inference: rank reduction → capacity loss by parameter count]` |
| `preference` | Taste, style, or priority | `[preference: cleaner API surface]` |

Use inline after each claim. The provenance phrase distinguishes "direct finding"
from "loose analogy" — that distinction matters for deciding how much weight to give.

## Phase 1: Framing

1. **Gather context** relevant to the debate topic:
   - Code: read source files, current architecture, recent changes
   - Research: check docs, papers, experiment results, prior debate records
   - Design: understand constraints, prior decisions, and stakeholder needs

2. If genuinely ambiguous, ask ONE clarifying question. Otherwise start.

3. **Build the neutral evidence packet** for Codex BEFORE forming your own
   position. This order matters: if you form your position first, you risk
   unconsciously cherry-picking evidence for the packet. Include:
   - Topic and decision question
   - Relevant code excerpts (functions, signatures, data flow)
   - Experiment results / metrics if applicable
   - Architecture constraints and prior decisions
   - User-stated goals and priorities
   - Open uncertainties (what is NOT known)

   Exclude: Claude's interpretation or reaction.
   The packet should be factual substrate, not argumentation.

4. **Form Claude's opening position** using Toulmin structure (see below).
   Show it to the user. Do NOT include it — or the user's reaction — in
   Codex's blind-opening prompt. Independence is the entire point: if Codex
   sees Claude's position, anchoring bias makes the debate theater.

### Toulmin Structure for Opening Positions

Each major claim in an opening position follows this structure. The reason for
this structure is that bare claims ("we should use method X") hide the reasoning
path — exposing warrants and falsifiers lets both models attack the actual
logic rather than talking past each other.

```
**Claim**: [the position]
**Grounds**: [evidence supporting it] [evidence-tier tag]
**Warrant**: [why this evidence supports this claim]
**Qualifier**: [confidence: high/medium/low] [conditions under which this holds]
**Falsifier**: [specific evidence that would defeat this claim]
```

## Phase 2: Blind Opening

Send Codex the evidence packet and topic. Via `mcp__codex__codex` with
`config: {"reasoning_effort": "xhigh"}`:

```
## Independent Position Request: {topic}

### Evidence Packet
{neutral evidence packet from Phase 1}

### Task
Form your independent position on this question. This is round 1 of a
multi-round debate with Claude — you will see Claude's view later.

Structure each major claim as:
- **Claim**: [position]
- **Grounds**: [evidence, tagged as [tier: provenance] — e.g. [paper-backed: Du et al. 2023, direct finding]]
- **Warrant**: [why this evidence supports this claim]
- **Qualifier**: [confidence: high/medium/low] [conditions]
- **Falsifier**: [what evidence would defeat this claim]

Also provide:
## Assumptions
[what you're taking as given]

## What Would Change My Mind
[specific evidence or arguments that would flip your view]

## Risks
[failure modes, edge cases]
```

Save the `threadId` — all subsequent rounds use `mcp__codex__codex-reply`.

### Optional Context Follow-Up

After Codex's opening, if Codex explicitly requests specific missing evidence
(e.g., "I need to see the actual function signature for X"), provide it as
raw artifacts — code snippets, metrics, file paths — without interpretation.
Limit to ONE follow-up exchange. If Codex's request is broad ("tell me more
about the architecture"), provide the most relevant excerpts and move on.
This gives Codex a fair shot without turning the debate into a Q&A loop.

## Phase 3: Crux Identification

Compare both blind positions. Identify cruxes — claims where changing one
side's view would likely change the final recommendation. Ignore surface
disagreements that don't affect the decision.

Build and maintain a **crux ledger**:

| Crux | Claude | Codex | Confidence | Evidence needed | Status |
|------|--------|-------|------------|----------------|--------|
| ... | view + tier | view + tier | C: med / X: high | ... | open / resolved / user-dependent / experiment-needed / stalemated |

### Immediate Agreement Protocol

If both models agree on all major points, this might be genuine consensus
or sycophantic convergence. Check before moving on:

- **Both high confidence + high-stakes decision** (architecture, research
  direction, experiment budget, paper claim, irreversible change):
  Switch to red-team mode. Send Codex: "We agree on [X]. Your job now
  is to find the strongest case AGAINST this position. Attack assumptions,
  find failure modes, identify what we might be missing."
  Research shows cross-model sycophancy can cause "disagreement collapse"
  where both models converge on a wrong answer (arXiv 2509.23055) — this
  step exists to catch that.

- **Otherwise**: Report the agreement to the user and ask whether they want
  a devil's advocate round or are satisfied with the consensus.

If cruxes exist (the common case), skip this section and proceed directly
to the user checkpoint below.

### User Checkpoint 1

After crux identification, present the user with:

> **Opening positions**: Claude argues [X], Codex argues [Y].
> Agreement on [A, B]. Cruxes: [C, D].
>
> **Your input** (say "continue" to proceed as-is):
> - Prioritize which cruxes to resolve first?
> - Add constraints or preferences the models should respect?
> - Declare any crux as "user-dependent" (your call, not the models')?

Wait for the user's response. If they provide input, incorporate it into the
crux ledger. If they say "continue" or equivalent, proceed with all cruxes open.

Then send Round 1 via `mcp__codex__codex-reply`:

```
## Round 1 — Claude's Position + Crux Analysis

### Claude's Opening Position
{Toulmin-structured claims, now revealed}

### Agreements
{where both models align}

### Cruxes
{specific cruxes framed as testable claims with evidence tiers}

### Steel-Man of Codex's Position
{restate Codex's strongest arguments in their best light — then identify
which specific warrant or assumption you dispute. Attacking without
steel-manning produces straw-man rebuttals that waste rounds.}

### Counter-Evidence
{evidence tagged with tiers}

### Questions
{1-2 targeted questions on open cruxes}

Respond with:
- Steel-man Claude's strongest point before countering
- Which cruxes you accept or contest, and why
- Updated confidence levels with reasoning
- Whether any of Claude's points changed your view
```

## Phase 4: Focused Rounds

Expect 2-3 rounds. Continue to 6 only while crux statuses are still changing.

Each round uses a lighter **delta format** — only new decision-relevant claims
need full warrant + qualifier + falsifier. Concessions and restatements are
free-form. This keeps the debate focused without making every message a form.

### 4a. Analyze honestly

- **Steel-man first**: before countering any claim, restate Codex's strongest
  version of the argument. Identify the specific warrant or assumption you dispute.
- Which challenges landed? Concede immediately — say what convinced you and
  update your confidence.
- Where is Codex weak? Challenge with tagged evidence.
- Update the crux ledger.

### 4b. Report to user (one paragraph)

> **Round N**: Codex challenged [X] — conceded [confidence: high→low] because [reason].
> Defending [Y] [confidence: high] with [counter-evidence]. Cruxes resolved: [A]. Open: [B].

### 4c. Send next round via `mcp__codex__codex-reply`

Summarize prior rounds instead of pasting full transcripts.

```
## Round {N} — Claude's Response

### Steel-Man
[Codex's strongest current argument, restated]

### Concessions
[what changed, what convinced you, updated confidence]

### Defended Points
[what you hold, tagged evidence]
[for NEW claims: warrant + qualifier + falsifier]

### Counter-Challenges
[rebuttals with evidence tiers + falsifiers]

### Crux Ledger Update
[current status + confidence levels]

### Questions
[1-2 targeted questions to advance open cruxes]
```

## Phase 5: Stopping Conditions

Stop as soon as one is met. Running extra rounds past convergence wastes
tokens and can degrade quality through repetition.

1. **Consensus** — both models agree on recommendation and main reasons.
2. **Decision-ready tradeoff** — disagreement remains, but the crux is a user
   preference or external constraint. Present both options with tradeoffs.
3. **Evidence-needed** — remaining crux requires an experiment, benchmark, or
   code inspection. Specify exactly what to test.
4. **Stalemate** — two consecutive rounds with no change in crux status,
   confidence levels, evidence citations, or newly identified falsifiers.
   Document both views.

A useful documented disagreement is better than artificial agreement.

## Phase 6: Pre-Synthesis Check

Before summarizing, verify:
- Every crux has a final status in the ledger
- The recommended action follows from resolved cruxes (not from rhetoric)
- Empirical claims are supported or labeled as hypotheses
- Unresolved disagreements are preserved, not smoothed into fake consensus
- Confidence labels reflect actual evidence, not persuasive momentum

## Phase 7: Synthesis

### User Checkpoint 2

Before writing the final summary, present the crux ledger with final statuses
and ask:

> Any cruxes you want to override or comment on before I summarize?

Wait for the user's response. If they have input, incorporate it.
If they say "continue" or equivalent, proceed to summary.

### Chat summary (always)

```markdown
## Debate Result: {topic}

**Rounds**: {N} | **Outcome**: {consensus / tradeoff / evidence-needed / stalemate}

**Conclusion**: {1-2 sentences}

**Key insights**:
- {insight} — raised by {Claude/Codex}, survived because {reason} [{evidence tier}]

**Positions that changed**:
- {who} conceded {what} because {evidence} [confidence: {old}→{new}]

**Crux ledger** (final):
| Crux | Resolution | Confidence | Deciding evidence |
|------|-----------|------------|------------------|
| ... | ... | ... | ... [{tier}] |

**Unresolved** (if any):
- {crux} — resolve by {experiment/benchmark/user decision}

**Recommended action**: {concrete next step}
```

### Saved document (conditional)

Write to `docs/debates/{date}-{topic-slug}.md` when:
- The debate ran 3+ rounds, OR
- It affects code/research direction materially, OR
- The user explicitly asks for a record

Create `docs/debates/` if it doesn't exist.
Template: see [references/consensus-template.md](references/consensus-template.md)

## Behavioral Rules

- Form a real position and defend it — but concede immediately when evidence
  or assumptions shift. State what convinced you.
- Steel-man before counter-arguing. Attacking a straw-man version wastes rounds
  and degrades trust.
- Tag evidence with tiers. Rhetorical confidence without evidence backing is
  a signal to distrust, not to defer.
- Separate empirical disagreements ("X is faster" — testable) from preference
  disagreements ("X is more elegant" — taste). Flag which is which.
- Challenge flawed premises from Codex or the user. Deference to authority
  produces worse outcomes than honest disagreement.
- Track confidence changes explicitly. If you went from high to low on a claim,
  say so and say why — this is the most valuable signal in the debate.

## Codex MCP

- **First call**: `mcp__codex__codex` with `config: {"reasoning_effort": "xhigh"}`
- **Follow-ups**: `mcp__codex__codex-reply` with saved `threadId` + `prompt`
- Starting a fresh `mcp__codex__codex` mid-debate erases Codex's memory of
  prior rounds — always use the reply endpoint after the first call
- On MCP error (including initial connection failure): tell the user, ask
  whether to retry or summarize current state. If Codex is unreachable before
  the debate starts, offer to proceed as a solo analysis instead
