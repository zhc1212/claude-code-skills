---
name: codex-experiment-critic
description: Reviews experimental designs via Codex (GPT) before committing GPU hours. Claude prepares the experiment plan, Codex critiques it blind for confounders, missing baselines, unfair comparisons, information leakage, statistical issues, and logical gaps. Catches invalid designs before expensive execution. Use when user says "codex check experiment", "validate experiment design", "experiment critic", "review my experiment plan", "codex检查实验设计", "实验设计审查", "codex审查实验", "让codex看看实验设计", "实验前检查", "check before I run", "is this experiment valid", "实验有没有问题", "帮我看看实验设计", "codex帮我检查实验". Not for running experiments, analyzing results, writing paper sections, or code review (/codex-review). Not for debate (/codex-debate) or general research review (/research-review).
---

# Codex Experiment Critic

Catch flawed experimental designs before they waste GPU weeks. Claude prepares
the experiment plan, Codex critiques it blind — independent review from a
different model family catches design flaws that self-review misses, because
the plan author's priors suppress counterexamples.

This exists because of concrete past failures: the P1.3 causal probe was
designed incorrectly (WT2 factors in a broken domain regime) and wasted weeks
of researcher time. A 5-minute design review would have caught it.

## Protocol Overview

```
1. Collect experiment plan (from user or conversation)
2. Claude quick-assessment (private — not shared with Codex)
3. Build neutral experiment packet for Codex
4. Codex blind critique (confounders, baselines, fairness, leakage, stats, ablations)
5. Cross-check Claude's assessment vs Codex's critique
6. Present findings with severity/confidence ratings
7. User decides: revise, proceed, or redesign
```

## Phase 1: Collect the Experiment Plan

Extract or ask for these elements. If the user provides a partial plan, ask
for the missing pieces — a critique of an incomplete plan produces vague
findings that waste everyone's time.

| Element | Why needed |
|---------|-----------|
| **Hypothesis** | What the experiment aims to show — without this, "success" is undefined |
| **Method** | Algorithm, pipeline, key hyperparameters |
| **Baselines** | What the results will be compared against |
| **Metrics** | How success/failure is measured |
| **Controls** | What is held constant across conditions |
| **Data** | Training, calibration, evaluation splits — and how they relate |
| **Compute budget** | GPU hours, number of runs — determines what's feasible |
| **Expected outcome** | What result would confirm/refute the hypothesis |

If the plan is already in a file (script, doc, conversation), read it and
extract these elements rather than asking the user to re-state them.

### Provisional Mode

If the user has only a hypothesis and partial method (no baselines/metrics
yet), run the critique in provisional mode rather than blocking. In this
mode:
- Codex critiques what's available and flags "cannot assess" for missing
  elements
- Verdict options become: PROMISING / NEEDS DETAIL / RETHINK (instead of
  APPROVE / REVISE / REDESIGN)
- The output explicitly lists what must be filled in before full critique

This is valuable because early-stage design feedback is cheaper than
post-implementation feedback. Don't gate-keep the critique behind plan
completeness.

## Phase 2: Claude Quick-Assessment

Before calling Codex, form 3-5 private concerns. Focus on the highest-risk
categories. Record them privately — these are hypotheses to cross-check
later, not conclusions.

Focus on:
- Does the hypothesis have a clear falsification criterion?
- Are the baselines actually comparable (same compute, data, tuning)?
- Is there train/test contamination in the data pipeline?
- Are there confounders the method doesn't control for?
- Is the compute budget sufficient for the claimed statistical power?

Do NOT include these concerns in the Codex prompt. Independence is the
point — if Codex sees Claude's flags, it anchors on them instead of
generating its own critique.

## Phase 3: Build the Experiment Packet

Assemble a neutral, factual packet. Include raw details, exclude
interpretation. The packet should let Codex form an independent assessment
without being steered by Claude's framing.

**Include:**
- Hypothesis (verbatim from user)
- Method description with key hyperparameters
- Baseline descriptions and how they were chosen
- Metrics and success criteria
- Data pipeline (sources, splits, any reuse across stages)
- Control variables
- Compute budget and number of planned runs
- Relevant code paths (function names, not full source — Codex can't run it)
- Domain context (model architecture, compression ratio, task type)
- Known limitations the user has acknowledged

**Exclude:**
- Claude's assessment or concerns
- Leading language ("this seems problematic because...")
- Recommendations or suggested fixes

## Phase 4: Codex Blind Critique

Send via `mcp__codex__codex` with `config: {"reasoning_effort": "xhigh"}`:

```
## Experiment Design Critique

You are a senior ML researcher reviewing an experiment plan before
execution. Your job: find flaws that would invalidate the results or
waste compute. Be thorough and specific — vague concerns are not
actionable.

### Experiment Plan
{neutral experiment packet from Phase 3}

### Critique Checklist
Evaluate each category. For each finding, provide ALL fields:

- **Category**: one of [Confounder | Missing Baseline | Unfair Comparison |
  Information Leakage | Statistical Issue | Reproducibility Gap |
  Compute Efficiency | Ablation Gap | Logical Gap]
- **Severity**: blocking (results would be invalid) | important (weakens
  the claim significantly) | minor (a reviewer would note it but results
  still hold)
- **Confidence**: high (clear from the plan) | medium (likely but depends
  on details not provided) | low (possible concern, need more info)
- **Issue**: what is wrong, in one sentence
- **Evidence**: which specific element of the plan this refers to
- **Suggested fix**: how to address it, concretely
- **Falsifier**: what information or argument would make this criticism
  invalid — include this even for high-confidence findings, because it
  forces precise scoping of the concern

### Categories
See references/critique-categories.md for detailed definitions with examples.
Categories: Confounder, Missing Baseline, Unfair Comparison, Information Leakage,
Statistical Issue, Reproducibility Gap, Compute Efficiency, Ablation Gap, Logical Gap.

### Verdict
After all findings, provide:
- **Overall verdict**: APPROVE (proceed as designed) | REVISE (fix
  specific issues, keep the core design) | REDESIGN (fundamental flaw,
  rethink the approach)
- **Summary**: 2-3 sentences on the overall design quality
- **Top priority**: the single most important thing to fix before running
```

Save the `threadId` — the user may want follow-up clarification.

## Phase 5: Cross-Check

Compare Claude's private quick-assessment with Codex's critique:

- **Both flagged**: High confidence the issue is real. Present as primary
  finding. Note the convergence — independent identification from two
  model families is strong signal.
- **Codex-only**: Present normally. Codex may have caught something
  Claude's priors suppressed — this is the value of cross-model review.
- **Claude-only**: Re-examine against the plan. If the concern is
  substantive and Codex missed it, present it as "Additional concern
  from Claude's pre-assessment" with specific evidence.
- **Neither flagged a category**: Silence is not proof of correctness,
  but no action needed.

Do not manufacture disagreement. If Codex's critique is thorough and
Claude has nothing to add, present Codex's findings without padding.

## Phase 6: Present Findings

Show the user a structured summary, organized by severity:

```markdown
## Experiment Design Critique: {experiment title}

**Verdict**: {APPROVE / REVISE / REDESIGN}

### Blocking Issues
{findings with severity: blocking, sorted by confidence}

### Important Issues
{findings with severity: important}

### Minor Issues
{findings with severity: minor}

### Cross-Model Agreement
- Both models flagged: {list}
- Codex-only: {list}
- Claude-only: {list}

### Recommended Changes
{prioritized, concrete list of changes before running}
```

After presenting:
- If REDESIGN: outline what a valid design would look like
- If REVISE: offer to help fix the specific issues
- If APPROVE: note any minor items to document for the paper

## Phase 7: User Decision

The user decides. Three paths:

1. **Revise**: fix the flagged issues, optionally re-run the critique on
   the revised plan via `mcp__codex__codex-reply` with the saved threadId
2. **Proceed anyway**: the user understands the risks and wants to run —
   acknowledge and note which findings they accepted
3. **Redesign**: go back to hypothesis formulation

Do not pressure the user toward any particular decision. Present the
findings, let them choose.

## Follow-Up

The user can ask to:
- **Clarify a finding**: use `mcp__codex__codex-reply` with the saved
  threadId to ask Codex to elaborate or reconsider
- **Re-critique after revision**: send the updated plan elements to Codex
  for a delta review
- **Challenge a finding**: if the user disagrees, send their reasoning to
  Codex and report whether it changes the verdict

## Behavioral Rules

- Critique the design, not the researcher. Frame findings as "the design
  has X issue" not "you forgot X."
- Every criticism requires a falsifier — this forces specificity and
  prevents vague hand-waving. "This might be a problem" is not a finding.
- Confidence calibration matters: a high-confidence blocking issue and a
  low-confidence minor concern require very different responses from the
  user. Do not flatten them into a generic worry list.
- Do not suggest adding experiments beyond the compute budget. If the
  budget is 10 GPU-hours, suggesting a 100-hour ablation study is not
  actionable. Work within the stated constraints and flag if the budget
  is insufficient for the claimed statistical power.
- Separate "reviewer would ask" from "results would be invalid." Missing
  a nice-to-have ablation is different from having a confounded comparison.

## Codex MCP

- **First call**: `mcp__codex__codex` with `config: {"reasoning_effort": "xhigh"}`
- **Follow-ups**: `mcp__codex__codex-reply` with saved `threadId` + `prompt`
- Starting a fresh `mcp__codex__codex` mid-critique erases Codex's memory of
  the experiment context — always use the reply endpoint after the first call
- On MCP error: tell the user, offer to retry or proceed with Claude-only
  assessment (clearly labeled as single-model, not cross-validated)
