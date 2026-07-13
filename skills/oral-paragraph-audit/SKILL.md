---
name: oral-paragraph-audit
description: "Paragraph-level academic writing audit for ML/NLP papers targeting top venues. Runs 10 structured checks on topic-support coherence, information density, claim-evidence alignment, transitions, de-AI patterns, section conventions, content boundaries, formula rigor, and terminology consistency. Use when user says '检查一下这段', 'audit this paragraph', 'oral quality check', '帮我看看这段写的怎么样', '检查写作质量', '帮我改段落', '写作审查', 'paragraph quality', 'review this paragraph'. Not for grammar-only proofreading, translation, whole-paper outlining, or full-section drafting."
---

# Oral-Level Paragraph Audit

Structured 10-check review for individual paragraphs in ML/NLP papers. Each
check targets a specific class of issue that top-venue reviewers penalize.

## Writing Philosophy (compact)

Ten principles drive the checks (full rationale with sources in
`references/writing-philosophy.md`):

1. **Every sentence earns its place** — advance argument, introduce evidence, or specify mechanism. *(Checks 2, 6)*
2. **Claims and evidence travel together** — never make the reviewer search. *(Check 3)*
3. **The paragraph is the unit of argument** — S1 states the message, rest proves it. *(Checks 0, 1, 4, 5)*
4. **Content lives in the right section** — correct sentence, wrong place = noise. *(Check 8)*
5. **Do not multiply entities** — every symbol/acronym is a cognitive slot. *(Checks 2, 8, 9)*
6. **Key information lands at the stress position** — sentence endings carry the payload. *(Check 4)*
7. **Each paragraph creates reader value** — report what the reader gains, not what authors did. *(Checks 0, 1, 3)*
8. **Cohesion from logic, not connectors** — Furthermore/Moreover mask gaps; real transitions come from substance. *(Check 4)*
9. **Restrained, evidence-first register** — let evidence carry the weight, not boosters. *(Check 6)*
10. **Paragraphs are vectors, not list items** — contrast, deepen, specify — never juxtapose. *(Check 10)*

Oral quality requires all ten simultaneously. A paragraph with good structure but
low density wastes a well-framed argument on filler. See the full 10-principle
rationale for deeper grounding.

## Scope

Audit one paragraph at a time, or a multi-paragraph excerpt for cross-paragraph
consistency. For multi-paragraph input, run Checks 0–9 on each paragraph
separately, then run Check 10 on the group.

**Context gathering**: when auditing a paragraph from a file, always read the
adjacent paragraphs (preceding and following) to enable Checks 5 and 10.

**Minimal-change rule**: prefer the smallest edit that fixes the issue. Do not
rewrite wholesale unless sentence order or claim structure is broken.

**Zero-skip principle**: every *applicable* check must show work with evidence in
the output. A bare "OK" without showing which sentences were assessed is a failed
audit. Checks that are skipped (no context for Check 5/10, non-technical for
Check 9) should say so explicitly — "skipped" is valid, silence is not.
The goal is zero issues surviving to reviewer.

## Procedure

1. Identify the section type (abstract, intro, related work, method, experiments,
   discussion, conclusion).
2. Run the Preflight + 10 checks in order.
3. Classify findings:
   - **Blocking**: harms reviewer understanding, credibility, or perceived contribution.
   - **Major**: weakens clarity, evidence, or flow but does not invalidate.
   - **Minor**: style or polish with low effect on reviewer judgment.
4. Provide replacement text with reasoning for Blocking and Major issues.
   For Minor issues, replacement is optional when the fix is obvious — a
   one-line note suffices. At oral level, Minor issues accumulate into
   reviewer friction, so flag them even if you don't rewrite.
5. Note what works well — good feedback includes strengths.

## Edge Cases

- **Unknown section**: infer from content; if genuinely ambiguous, ask the user
  or report "Section: inferred as [X]" and proceed.
- **Unavailable tables/figures**: when a claim references a table you cannot
  access, mark as "Needs verification — table not available" rather than
  flagging as unsupported.
- **Rewrite-only request**: if the user asks "帮我改" without wanting a full
  audit, still run the 10 checks internally but present only the revised text
  with a brief severity summary.
- **Light review**: if the user asks for a quick look ("快速看一下", "top issues
  only"), run all checks but present only the top 3 highest-severity findings.
- **Long excerpts (>5 paragraphs)**: run each paragraph's checks, then run a
  global Check 10 pass. For very long sections, ask whether to audit all
  paragraphs or sample the most critical ones.
- **No adjacent context**: report "Check 5: skipped (no preceding context)"
  and "Check 10: skipped (single ¶)" — don't fabricate transitions.
- **LaTeX-heavy input**: preserve all macros, `\cite{}`, `\ref{}`, `\label{}`,
  custom commands, and math environments in revised text. Never rewrite LaTeX
  structure — only rewrite the prose within it.
- **Non-English draft** (e.g., Chinese): run checks on the content logic
  (structure, density, claims, transitions) but skip register/de-AI checks
  that are English-specific. Note this in the output.

## The 10 Checks (+ Preflight)

### Preflight: Section Role (Check 0)

Before auditing the paragraph itself, identify its role in the surrounding
section. What structure is the section using? (progressive, parallel,
claim→evidence, setup→derivation) What role does this paragraph play?

Flag when a paragraph's role contradicts the section structure, or a
`\paragraph{}` heading promises one topic but delivers another.

Skip if no section context is available.

### 1. Structure: Topic–Support Coherence

S1 states the paragraph's message. Every subsequent sentence supports it.

**Step A** — Verify S1 states a claim or setup (not raw data). S1 must NOT
recap the previous paragraph's conclusion — that wastes the reader's strongest
attention position on information they already have.
**Step B** — For each S(i>1), name its role: Evidence, Mechanism, Refinement,
Contrast, or Consequence. Flag MAJOR if a sentence has no role relative to S1.
**Step C** — If two distinct claims cannot be unified under S1, flag MAJOR:
mixed messages — split.
**Step D** — Final sentence must be analytic (interprets, concludes, or advances),
not suspended narration. Empty conclusions like "this contributes to our
understanding of X" without saying WHAT → flag MAJOR.

**Section exceptions**: Dataset/Setup and Limitations paragraphs are factual or
enumerative by design — S1 need not state a claim, and Step D is relaxed.

### 2. Information Density

For each sentence: `+new` (adds info), `=echo` (restates prior), `~filler`
(adds nothing). Assess every sentence individually in the output.

Three things a sentence can do: advance argument, introduce evidence, specify
mechanism. A sentence that does none of these is deletable.

Red flags:
- Participial tails echoing main clause
- Boilerplate formalisms (put in appendix)
- Discussion with >3 inline numbers
- **Mechanical signposts**: "In what follows…", "Having established X, we now
  turn to Y", "This section discusses…", "This raises the question of…" —
  these narrate the paper's structure instead of advancing the argument
- **Throat-clearing**: "It is important to note that…", "It should be mentioned
  that…", "Worth highlighting is…"
- **Same-paragraph repetition**: restating a point made 1–2 sentences earlier
  in different words

### 3. Claim-Evidence Alignment

Every strong claim needs support within or near the paragraph. Check:
- "X outperforms Y" → table/figure ref or inline number
- "significantly improves" → quantified, not just the word
- "X is the first/novel" → citation gap or novelty argument

**Scope qualifiers**: strong claims need explicit boundaries. "optimal" →
"optimal for this surrogate". "outperforms all" → add "at every tested ratio".

**Refutable claims** ([SPJ](https://simon.peytonjones.org/great-research-paper/)):
a claim must be specific enough that a reader can tell whether it is true.

**Narrative arc**: if S1 frames a question, the paragraph must answer it by
the final sentence.

**Baseline accuracy**: descriptions of other methods must match cited papers.

### 4. Sentence-to-Sentence Transitions

Every S(n)→S(n+1) pair needs a nameable logical relation: Cause, Contrast,
Evidence, Consequence, Refinement, Extension, Setup, or Limitation.

**Mandatory enumeration**: list every pair with its relation type. Missing one
pair in a 7-sentence abstract means missing ~15% of the checks.

**Gap-masking connectors**: Furthermore, Additionally, Moreover, In addition —
these assert a logical relation exists without naming it. When one appears,
check whether removing it exposes a logical gap between the sentences. If the
connection is real, replace with the actual relation; if not, the sentences
need restructuring. Flag MAJOR when the connector masks a genuine gap.

**Sentence-level clarity**: topic/stress positions (key info at sentence end),
subject-verb proximity, pronoun clarity ("this" only as adjective), verb-early.

### 5. Paragraph-to-Paragraph Transitions

Compare S1 of this paragraph against the final sentence of the previous one.
Check linkage, progressive vs reset, and acceleration (argument moving forward,
not circling). `\paragraph{}` headings handle topic switches — no bridge needed.

Skip if no preceding context available.

### 6. De-AI Pass

Flag when a pattern harms precision, register, or reviewer trust. Respect venue
and author style — these are heuristics for top-venue prose, not universal rules.
Four categories:

**A. AI fingerprints** (patterns that signal machine-generated text):
- Uniform sentence length, synonym cycling, passive clusters
- Paired adjectives, verb doublets, "not only X but also Y"
- Participial tails, forced triples, weak copula

**B. Boosters and stakes-raisers** (inflate importance, undermine credibility):
- Boosters: really, very, hugely, remarkably, strikingly, notably
- Stakes-raisers: Unsurprisingly, Interestingly, Indeed, Of course, Naturally
- Filler adverbs: crucially, importantly, genuinely, honestly, straightforward
- Promotional: novel, unique, important contribution (let evidence speak)

**C. Register violations** (wrong tone for academic prose):
- Latinate over Anglo-Saxon when no precision is gained: utilise → use,
  demonstrate → show, commence → start, regarding → about (technical terms exempt)
- Verb nominalization: "the examination of X" → "examining X" / "X examines"
- Overclaim verbs: prove, demonstrate conclusively, definitively, the cause →
  prefer consistent with, indicates, the evidence supports
- Editorializing in Results: commentary on data belongs in Discussion
- First person (we/our/I): standard in ML/NLP papers — only flag if the venue
  or style guide prohibits it (e.g., some humanities or medical journals)

**D. Structural noise and formatting**:
- >1 em dash per paragraph (use commas or parentheses)
- >2 semicolons per paragraph (prefer full stops)
- Bullet points in prose body text
- i.e. in running text (use commas or namely)
- "taken together", "Together," as sentence opener
- Number/unit consistency: % vs percent (pick one), en-dash for ranges
  (1840–2010, not hyphen), digits for 10+ and statistics, spelled out for
  1–9 in running text, spaces around = in inline equations

**Tense**: present tense for findings and established facts, past tense for
events and procedures. Mixed tense within a paragraph → flag MINOR.

**Guardrail**: if a flagged pattern reads clearly in context, keep it.

### 7. Section-Specific Rules

Apply the rules for the identified section type. See
`references/section-rules.md` for detailed per-section conventions.

Key patterns: Abstract (no bare symbols, no jargon, self-contained), Intro
(progressive: problem→challenge→positioning), Related Work (one dimension/¶,
gap at end), Method (definition→equation→interpretation), Experiments
(claim-first, not number-first), Discussion (insight-first, no unmarked
speculation), Conclusion (short, no problem restatement at S1).

### 8. Content Boundary

Does every sentence belong in this section? Method content in Experiments
is noise. Hyperparameters in Method belong in Experiments Setup. Detailed
numerical comparisons in Related Work often belong in Experiments — but brief
prior-work numbers for context are fine.

### 9. Formula Rigor (Method/Appendix only)

Symbol hygiene (defined near first use, no dual meanings, consistent
subscripts), dimensional consistency, completeness (explicit min/sum/domain),
notation consistency with rest of paper.

Skip for non-technical sections.

### 10. Terminology and Logic Consistency (multi-paragraph)

Terminology stability (same concept, same name), cross-paragraph logic
(no contradictions), one message per paragraph, acronym scope boundaries.

**Paragraph vector relations**: consecutive paragraphs should form vector
relations — contrast, specification, deepening, mechanism — not a parallel
list. Flag MAJOR when paragraphs read as "one paragraph on A, one paragraph
on B, Together these…" without logical progression between them.

Read adjacent paragraphs to check. Skip if truly no surrounding context.

## Output Format

```
¶ [section / heading]

Section role: [structure type] — this ¶ serves as [role]. [OK / MAJOR]
Strengths: [what works well]

 0. Preflight:  [OK / skipped / MAJOR: role mismatch]
 1. Structure:  S1 message: "[quote]"
                S2: [role]. S3: [role]. ... [OK / MAJOR: S_ off-topic]
 2. Density:    S1: [+new]. S2: [...]. ... [OK / MAJOR: S_ echo/filler]
 3. Claims:     [OK / MAJOR: "X" unsupported / scope missing]
 4. Transitions: S1→S2: [relation]. S2→S3: [...]. ... [OK / MAJOR at S_→S_]
 5. ¶ bridge:   [OK / skipped / MAJOR]
 6. De-AI:      [PASS / MINOR: ...]
 7. Section:    [OK / MAJOR: ...]
 8. Boundary:   [OK / MAJOR: S_ belongs in {Experiments/Setup/...}]
 9. Formulas:   [OK / skipped / BLOCKING: symbol X undefined]
10. Consistency: [OK / skipped / MAJOR: terminology drift]
```

For each issue, provide:
- **Original**: the problematic text
- **Revised**: the replacement
- **Why**: one-sentence reasoning

See `references/examples.md` for good vs bad audit examples. A bare "OK"
without evidence is a failed audit — always show which sentences were assessed.

## After the Audit: Handoff

- **De-AI escalation**: if Check 6 surfaces 2+ MAJOR issues, recommend running
  `/deai-latex` on the full section for a comprehensive de-AI pass. Check 6
  is a spot-check, not an exhaustive rewrite tool.
- **Figure/table issues**: if Check 3 reveals claim-data mismatches involving
  figures, recommend `/figure-audit` for a visual inspection.
- **Full-paper sweep**: if multiple paragraphs have Blocking issues, suggest
  `/paper-presubmit-audit` for a holistic pass.

Do not auto-invoke other skills. Present findings, let the user decide.

## Reference Files

- `references/writing-philosophy.md` — 10 principles with full rationale and academic sources
- `references/section-rules.md` — detailed per-section conventions (Abstract, Intro, Method, etc.)
- `references/examples.md` — good vs bad audit examples with severity labels
