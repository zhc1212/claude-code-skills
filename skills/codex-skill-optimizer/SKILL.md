---
name: codex-skill-optimizer
description: "Use when evaluating, auditing, or improving any Claude Code skill — whether project-local or global. Runs a cross-model optimization pipeline: domain research, blind Claude+Codex debate, consensus-driven rewrites, and structured final audit. Triggers on \"evaluate skill\", \"optimize skill\", \"audit skill\", \"improve skill\", \"skill quality check\", \"评估skill\", \"优化skill\", \"skill审查\", \"检查skill质量\", or when the user points at a SKILL.md and wants it improved. Not for creating skills from scratch (use /skillify or /document-skills:skill-creator) or for debating non-skill topics (/codex-debate)."
---

# Codex Skill Optimizer

Evaluate and improve any Claude Code skill through cross-model research,
blind debate, and structured audit. This skill was itself built using this
process — every step below was validated on 6 real skills in a single session,
with all 6 debates converging in round 1.

The core insight: Claude and Codex independently identify ~70% of the same
issues (validating those problems are real), but each finds ~30% unique
insights the other misses. Combined with domain research and a structured
audit, this catches problems that no single-pass review would find.

## When to Use

- Evaluating a new skill someone else wrote
- Auditing an existing skill for quality gaps
- Optimizing a skill after initial creation
- Bringing an old skill up to current standards
- After creating a skill with /skillify or /document-skills:skill-creator

## When NOT to Use

- Creating a skill from scratch — use /document-skills:skill-creator or /skillify
- Debating a non-skill topic — use /codex-debate
- Quick one-off skill check — just read the SKILL.md and comment

## Protocol

```
1. Read + analyze the target skill
2. Research domain best practices (background agent)
3. Claude forms independent position (3-5 claims, not shown to Codex)
4. Build neutral evidence packet → Codex blind review
5. Compare → crux ledger → 1 focused round (usually sufficient)
6. Synthesize consensus → concrete change list
7. Apply changes
8. Final audit (10-dimension scorecard)
9. Fix audit findings → done
```

## Step 1: Read and Analyze

Read the target skill completely — SKILL.md and all reference files.
Record initial observations:

- Line count (target: under 500 for SKILL.md)
- Description quality (third-person? triggers? negative boundaries?)
- Structure (clear phases? numbered steps? templates?)
- WHY explanations (every rule should explain its reasoning)
- Voice (imperative? no bare MUSTs?)
- Cross-file consistency (do references match SKILL.md claims?)

Also read the skill's neighboring skills to understand trigger boundaries —
the most common skill defect is overlapping triggers with a sibling.

## Step 2: Domain Research

Launch a background research agent to find best practices relevant to the
skill's domain. This grounds the debate in evidence rather than opinion.

Research prompt template (adapt to the skill's domain):

```
Research [DOMAIN] best practices for AI-assisted [SKILL TOPIC]. I need:
1. What the literature says about [SPECIFIC ASPECT]
2. Community patterns and tools for [SPECIFIC WORKFLOW]
3. Common failure modes and how to prevent them
4. Any comparative studies or benchmarks
Under 400 words, focus on actionable findings not vague summaries.
```

The research agent returns while Claude forms its position (Step 3) —
they run in parallel to save time.

## Step 3: Claude's Independent Position

Form 3-5 specific improvement claims BEFORE any interaction with Codex.
This order matters: if you build the Codex prompt first, you frame the
evidence toward your own analysis, defeating the independence that makes
cross-model optimization valuable.

Each claim follows this structure:

```
**Claim N**: [specific improvement]
**Grounds**: [evidence from the skill, research, or standards]
**Warrant**: [why this evidence supports this change]
**Qualifier**: [confidence: high/medium/low + conditions]
**Falsifier**: [what would make this change unnecessary]
```

**Good claim**: "Gate #6 should check spec-test alignment because LLM-generated tests often have high coverage but low mutation score (ASE 2025) — 5 acceptance criteria with 3 tests = 2 untested requirements."

**Bad claim**: "The skill could be better organized." (vague, no evidence, no falsifier)

Show claims to the user. Do NOT include them in Codex's prompt.

## Step 4: Codex Blind Review

Build a neutral evidence packet containing:
- The target skill's full content
- Known weaknesses from Step 1 analysis
- Research findings from Step 2
- Skill craftsmanship standards (below)
- The skill's context (what project, what ecosystem)

Exclude: Claude's position, Claude's specific claims, user reactions.

Send via `mcp__codex__codex` with `config: {"reasoning_effort": "xhigh"}`:

```
## Independent Skill Review: {skill name}

### Skill Content
{full SKILL.md + reference file summaries}

### Known Weaknesses
{from Step 1 analysis — factual observations, not Claude's opinions}

### Research Findings
{from Step 2}

### Quality Standards
- Under 500 lines, progressive disclosure to references
- Third-person description with "Use when..." triggers + negative boundaries
- Imperative voice, WHY over MUST for every rule
- Confidence calibration on findings
- Blind independence in cross-model protocols
- Evidence-grounded claims with falsifiers
- xhigh reasoning, threadId for follow-up
- Edge case handling, cross-file consistency

### Task
Form your independent position on how to optimize this skill. For each
claim: Claim, Grounds, Warrant, Qualifier, Falsifier. Also provide
Assumptions, What Would Change My Mind, and Risks.
```

Save the `threadId`.

## Step 5: Compare and Debate

Compare Claude's claims (Step 3) with Codex's claims (Step 4). Build a
crux ledger:

| Crux | Claude | Codex | Status |
|------|--------|-------|--------|
| ... | view | view | open / resolved |

From seed runs (6 skills), the pattern was:
- ~70% of claims overlap (both independently identified) → high confidence
- ~15% are Codex-only → new insights Claude missed
- ~15% are Claude-only → re-examine, sometimes valuable, sometimes noise
- Most debates converged in 1 round, but add rounds for unresolved cruxes

Send Round 1 to Codex via `mcp__codex__codex-reply`: reveal Claude's
position, steel-man Codex's strongest points, identify specific cruxes,
and ask targeted questions on open disagreements.

If all cruxes resolve in Round 1 (the common case), proceed to synthesis.
If not, continue focused rounds until convergence or 3 rounds max.

## Step 6: Synthesize and Apply

Produce a concrete numbered list of changes from the debate consensus.
Each change should specify: what to change, where, and why (from the
debate evidence).

Apply all changes to the skill files. For large skills, use Edit for
surgical changes. For complete rewrites, use Write.

After applying, verify line counts are still under 500.

## Step 7: Final Audit

The audit catches edge cases, cross-file consistency issues, and
craftsmanship problems that debates miss (debates focus on big
architectural decisions; audits focus on details).

### "Good Enough" Gate

If the initial analysis (Step 1) shows all dimensions are strong and no
safety, triggering, or structural issues exist, report: "Skill is already
well-optimized. No substantive changes recommended." and present the
scorecard without running the full debate pipeline. Optimization without
real issues creates churn.

### Adaptive Scoring

Score across 10 dimensions. Mark dimensions as N/A when they don't apply
(e.g., MCP Integration for non-Codex skills, Follow-Up for one-shot skills):

| Dimension | What to check |
|-----------|---------------|
| Description / Triggering | Third-person, char count, trigger coverage (EN+ZH), negative boundaries, pushiness |
| Structure | Flow correctness, phase sequencing, mode consistency |
| Instruction Clarity | Imperative voice, WHY count, zero bare MUSTs |
| Domain Quality | Skill-specific: review format, debug protocol, etc. |
| Edge Cases | What's handled, what's not, edge case table |
| Cross-File Consistency | References align with SKILL.md, shared terminology |
| Safety | Secrets, consent, destructive operations |
| Follow-Up | threadId preserved, follow-up modes documented |
| MCP Integration | xhigh config, error handling, initial failure path |
| Craftsmanship | Line count, progressive disclosure, organization |

For each dimension: score 1-10, note issues found. Fix all issues
scoring below 9.

Present a final scorecard to the user:

```
## Final Scorecard: {skill name} v{N}

{lines} lines SKILL.md | {ref lines} lines references | {total} total

| Dimension | Score | Notes |
|-----------|-------|-------|
| ... | X/10 | ... |
| **Overall** | **X/10** | |
```

## Step 8: Fix, Verify Consistency, and Confirm

Apply fixes for all audit findings. Then run a consistency checklist:

- Line counts still under 500?
- Description still matches body content (no stale references)?
- Reference files still align with SKILL.md claims?
- All cross-skill boundary references still valid?
- Skill appears in the available skills list?

Report completion with before/after summary (lines, score, key changes).

## Craftsmanship Standards (reference)

These standards apply to all skills in this ecosystem:

**Description**: Third-person ("Sends...", "Reviews...", not "Send...",
"Review..."). Start with what it does, then "Use when..." triggers.
Include EN + ZH trigger phrases. Explicit "Not for..." negative
boundaries referencing sibling skills.

**Body**: Imperative voice. Every rule explains WHY. No bare MUST/ALWAYS
without reasoning. Progressive structure (high at boundaries, light in
middle). Evidence-grounded claims with confidence + falsifiers.

**MCP**: `config: {"reasoning_effort": "xhigh"}`. Save threadId. Handle
initial connection failure. Reply endpoint for follow-ups.

**Organization**: SKILL.md under 500 lines. Reference files for domain
detail, categories, templates. Lean body, rich references.

## Codex MCP

- **First call**: `mcp__codex__codex` with `config: {"reasoning_effort": "xhigh"}`
- **Follow-ups**: `mcp__codex__codex-reply` with saved `threadId`
- On MCP error: tell user, offer Claude-only audit (still valuable, just
  not cross-model validated)
