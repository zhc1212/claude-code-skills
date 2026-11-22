# Debate Protocol

Shared by `codex-debate` (Claude and Codex), `agy-debate` (Claude and Carbon) and `tri-debate` (Claude, Codex and
Carbon). The entry skill names the participants; "the opponent" below means each external participant. The entry
skills refer to section names here; when renaming one, update them in the same edit.

Stress-test technical decisions by eliciting independent positions from Claude and
the opponent, identifying cruxes, and producing either a justified consensus or a clear
record of unresolved tradeoffs. The protocol uses Toulmin argumentation and
calibrated confidence to ensure reasoning quality, not just persuasive prose.

## Participants

| | Codex | Carbon |
|---|---|---|
| Model | `gpt-6.2-astra`, `model_reasoning_effort` `xhigh` | Gemini 4 Carbon, effort `high` |
| First call | [`codex-cli.md`](codex-cli.md): `codex exec` with `model: gpt-6.2-astra`, `config: {"model_reasoning_effort": "xhigh"}` and, for a repository topic, `cwd: <repository root>` | [`agy-cli.md`](agy-cli.md): its call form, without `--conversation` |
| Later calls | `codex exec resume` with the saved `threadId` | the same call form with `--conversation <conversation_id>` |
| Read-only line | `Read-only: analyse and report; do not create, modify, or delete any file.` | the read-only line in `agy-cli.md` |
| Exchange files | `thread_id`; `r{N}-codex.md` (the `-o` file) | `conversation_id`; `r{N}-agy.json`, its `.response` saved as `r{N}-agy.md` |
| Ledger label | `X:` | `G:` |
| Record line | `Codex: gpt-6.2-astra, xhigh, thread {threadId}` | `agy: gemini-4-carbon, high, conversation {conversation_id}` |
| Evidence access | opens the repository through `cwd` | opens files only by exact path; see "Evidence access" in `agy-cli.md` |

Claude's ledger label is `C:`. Every prompt to an opponent, first and follow-up, carries its read-only line (the
`{read-only line}` slot in the templates): Codex has write access inside the Claude sandbox, and agy has it
without its deny settings. A fresh first call mid-debate erases the opponent's memory of earlier
rounds; after the first call, always resume.

### Carbon rules

- **Verify on arrival.** Each round, open every checkable claim from Carbon that bears on a
  crux (file:line, quoted code, citation, number, API name) before it enters the crux ledger.
  Until opened it is `unverified`, and an unverified claim leaves every crux status unchanged.
  A `code-inspected` tag on a path outside the packet counts as `inference` until you open it.
- **Widen the option space.** Add this section to Carbon's blind-opening request, after `## Risks`:

  ```
  ## Alternatives Outside the Framing
  [at least one option the question does not list, with its strongest case]
  ```

  Treat a surviving alternative as a new crux.

## Protocol Overview

```
1. Gather context → build neutral evidence packet
2. Claude forms Toulmin-structured position (shown to user, hidden from the opponent)
3. The opponent forms a BLIND independent position (evidence packet + topic only)
4. (Optional) The opponent requests one round of targeted raw evidence
5. Compare → identify cruxes → build crux ledger → proceed
6. Focused rounds on cruxes (expect 2-3, max 6)
7. Stop as soon as a stopping condition is met
8. Pre-synthesis check → synthesize (user can interrupt anytime)
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
     (the repository's `docs/debates/` and the scratch debates directory)
   - Design: understand constraints, prior decisions, and stakeholder needs

2. If genuinely ambiguous, ask ONE clarifying question. Otherwise start.

3. **Build the neutral evidence packet** for the opponent BEFORE forming your own
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
   the opponent's blind-opening prompt. Independence is the entire point: if the opponent
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

Send the opponent the evidence packet and topic through its first call (see
Participants), so it can open the code and results the packet cites:

```
## Independent Position Request: {topic}

{read-only line}

### Evidence Packet
{neutral evidence packet from Phase 1}

### Task
Form your independent position on this question. This is round 1 of a
multi-round debate — you will see the other views later.

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

Save the opponent's thread or conversation id; every later round resumes it.

Keep the exchange on disk as it happens, in a persistent directory outside the
repository, e.g. `~/.claude/projects/<project-key>/scratch/debates/{date}-{topic-slug}/`:
`packet.md`, the id file, and per round `r{N}-prompt.md` (written before
sending; `r{N}-prompt-{codex|agy}.md` when prompts differ) and the reply files
from Participants, with the blind opening as round 0. Give the CLIs real paths
(`realpath -m`).
Outside the repository, because packets often carry unpublished numbers and the
repository may be shared; not `/tmp`, which inside the sandbox is per-session
tmpfs. The saved document links here instead of reconstructing the exchange.

### Optional Context Follow-Up

After the opponent's opening, if it explicitly requests specific missing evidence
(e.g., "I need to see the actual function signature for X"), provide it as
raw artifacts — code snippets, metrics, file paths — without interpretation.
Limit to ONE follow-up exchange. If its request is broad ("tell me more
about the architecture"), provide the most relevant excerpts and move on.
This gives the opponent a fair shot without turning the debate into a Q&A loop.

## Phase 3: Crux Identification

Compare the blind positions. Identify cruxes — claims where changing one
side's view would likely change the final recommendation. Ignore surface
disagreements that don't affect the decision.

Build and maintain a **crux ledger**:

| Crux | Claude | {one column per opponent} | Confidence | Evidence needed | Status |
|------|--------|-------|------------|----------------|--------|
| ... | view + tier | view + tier | C: med / X: high (labels from Participants) | ... | open / resolved / user-dependent / experiment-needed / stalemated |

### Immediate Agreement Protocol

If all participants agree on all major points, this might be genuine consensus
or sycophantic convergence. Check before moving on:

- **Both high confidence + high-stakes decision** (architecture, research
  direction, experiment budget, paper claim, irreversible change):
  Switch to red-team mode. Send the opponent: "We agree on [X]. Your job now
  is to find the strongest case AGAINST this position. Attack assumptions,
  find failure modes, identify what we might be missing."
  Research shows cross-model sycophancy can cause "disagreement collapse"
  where both models converge on a wrong answer (arXiv 2509.23055) — this
  step exists to catch that.

- **Otherwise**: Report the agreement to the user and ask whether they want
  a devil's advocate round or are satisfied with the consensus.

If cruxes exist (the common case), skip this section and proceed directly
to the user checkpoint below.

### User Checkpoint 1 (optional)

After crux identification, briefly present the crux ledger inline (positions,
agreements, cruxes) and **proceed directly to Round 1** without waiting for
user input. The user can interrupt at any point if they want to steer.

Then send Round 1 (see Two-Party Round Messages).

## Phase 4: Focused Rounds

Each round uses a lighter **delta format** — only new decision-relevant claims
need full warrant + qualifier + falsifier. Concessions and restatements are
free-form. This keeps the debate focused without making every message a form.

### 4a. Analyze honestly

- **Steel-man first**: before countering any claim, restate the opponent's strongest
  version of the argument. Identify the specific warrant or assumption you dispute.
- Which challenges landed? Concede immediately — say what convinced you and
  update your confidence.
- Where is the opponent weak? Challenge with tagged evidence.
- Update the crux ledger.

### 4b. Report to user (one paragraph)

> **Round N**: {Opponent} challenged [X] — conceded [confidence: high→low] because [reason].
> Defending [Y] [confidence: high] with [counter-evidence]. Cruxes resolved: [A]. Open: [B].

### 4c. Send the next round (see Two-Party Round Messages)

## Phase 5: Stopping Conditions

Stop as soon as one is met. Running extra rounds past convergence wastes
tokens and can degrade quality through repetition.

1. **Consensus** — all participants agree on recommendation and main reasons.
2. **Decision-ready tradeoff** — disagreement remains, but the crux is a user
   preference or external constraint. Present both options with tradeoffs.
3. **Evidence-needed** — remaining crux requires an experiment, benchmark, or
   code inspection. Specify exactly what to test.
4. **Stalemate** — two consecutive rounds with no change in crux status,
   confidence levels, evidence citations, or newly identified falsifiers.
   Document each view.

A useful documented disagreement is better than artificial agreement.

## Phase 6: Pre-Synthesis Check

Before summarizing, verify:
- Every crux has a final status in the ledger
- Every decision-bearing or disputed file:line citation, from any participant, has
  been opened and checked; one that cannot be checked is labelled unverified and
  the recommendation says it depends on it
- The recommended action follows from resolved cruxes (not from rhetoric)
- Empirical claims are supported or labeled as hypotheses
- Unresolved disagreements are preserved, not smoothed into fake consensus
- Confidence labels reflect actual evidence, not persuasive momentum

## Phase 7: Synthesis

### User Checkpoint 2 (optional)

Proceed directly to synthesis without waiting for user input.
The user can interrupt if they want to override cruxes.

### Chat summary (always)

```markdown
## Debate Result: {topic}

**Rounds**: {N} | **Outcome**: {consensus / tradeoff / evidence-needed / stalemate}

**Conclusion**: {1-2 sentences}

**Key insights**:
- {insight} — raised by {participant}, survived because {reason} [{evidence tier}]

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

Write `debate.md` in the exchange directory when:
- The debate ran 3+ rounds, OR
- It affects code/research direction materially, OR
- The user explicitly asks for a record

Copy it to the repository's `docs/debates/{date}-{topic-slug}.md` when the
project already keeps debate records there and nothing in it is unpublished.
Template: see [debate-record-template.md](debate-record-template.md)

## Behavioral Rules

- Form a real position and defend it — but concede immediately when evidence
  or assumptions shift. State what convinced you.
- Steel-man before counter-arguing. Attacking a straw-man version wastes rounds
  and degrades trust.
- Tag evidence with tiers. Rhetorical confidence without evidence backing is
  a signal to distrust, not to defer.
- Separate empirical disagreements ("X is faster" — testable) from preference
  disagreements ("X is more elegant" — taste). Flag which is which.
- Challenge flawed premises from any participant or the user. Deference to authority
  produces worse outcomes than honest disagreement.
- Track confidence changes explicitly. If you went from high to low on a claim,
  say so and say why — this is the most valuable signal in the debate.

## Two-Party Round Messages

With one opponent, Claude's reply travels inside the next prompt. Expect 2-3 rounds. Continue to 6 only while crux statuses are still changing.
Before round 3 and each later round, name the crux it can resolve and whether
raw evidence (reading the code, a run) would resolve it more cheaply; if
neither, stop.

Round 1, after crux identification:

```
## Round 1 — Claude's Position + Crux Analysis

{read-only line}

### Claude's Opening Position
{Toulmin-structured claims, now revealed}

### Agreements
{where both models align}

### Cruxes
{specific cruxes framed as testable claims with evidence tiers}

### Steel-Man of {Opponent}'s Position
{restate the opponent's strongest arguments in their best light — then identify
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

Each later round:

Summarize prior rounds instead of pasting full transcripts.

```
## Round {N} — Claude's Response

{read-only line}

### Steel-Man
[the opponent's strongest current argument, restated]

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

## Failures

On a CLI error its CLI reference does not resolve (not signed in, network, initial connection failure): tell the user, ask whether
to retry or summarize current state. If the opponent is unreachable before the
debate starts, offer to proceed as a solo analysis instead.
