---
name: oral-paragraph-audit
description: "Paragraph-level prose-quality audit for ML/NLP papers targeting top venues ('oral' = top-venue prose bar, not spoken language). Use when user says '检查一下这段', 'audit this paragraph', 'oral quality check', '帮我看看这段写的怎么样', '检查写作质量', '帮我改段落', '写作审查', 'paragraph quality', 'review this paragraph', or pastes one to several paragraphs of a paper draft and asks whether they read well. Not for grammar-only proofreading, translation, whole-paper outlining, full-section drafting, or abstract/intro structure (use abstract-intro-audit)."
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
audit — a pass must name what was assessed (e.g. "Claims: no strong claim
detected; assessed S1–S3. OK"). Checks that are skipped (no context for Check
5/10, non-technical for Check 9) should say so explicitly — "skipped" is valid,
silence is not. The goal is zero issues surviving to reviewer.

**Calibration**: do not invent defects to satisfy a check — an evidence-backed
PASS is a successful audit result, not a failure to find something. A clean
paragraph ends with `0 Blocking / 0 Major` plus the evidence lines showing what
was assessed. A missing citation for a background technique is a finding only
when the text claims novelty or priority (Check 3); a technical description that
could be read as an implicit claim ("we whiten before truncation, reducing the
error from A to B") is audited for well-formedness under Check 9, not as an
unsupported claim under Check 3.

## Procedure

1. Identify the section type (abstract, intro, related work, method, experiments,
   discussion, conclusion).
2. Run the Preflight + 10 checks in order.
3. Classify findings:
   - **Blocking**: harms reviewer understanding, credibility, or perceived contribution.
   - **Major**: weakens clarity, evidence, or flow but does not invalidate.
   - **Minor**: style or polish with low effect on reviewer judgment.

   **Severity test**: a Major must name what the reviewer would misread or
   fail to find. If the smallest fix is a one-clause edit or a word swap, the
   finding is Minor.

   **Blocking defaults** — everything else starts at Major or Minor:
   - Check 3: a strong claim the supplied text neither supports nor scopes
     ("outperforms all", "significantly", "the primary cause").
   - Check 7: an Experiments or Discussion ¶ that opens on a number instead of
     a claim.
   - Check 9: a symbol undefined at first use or carrying two meanings.
   - Check 0: a ¶ whose role contradicts the section's structure.
4. Provide replacement text with reasoning for Blocking and Major issues.
   For Minor issues, replacement is optional when the fix is obvious — a
   one-line note suffices. At oral level, Minor issues accumulate into
   reviewer friction, so flag them even if you don't rewrite.
5. Note what works well — good feedback includes strengths.

## Edge Cases

- **Unknown section**: infer from content; if genuinely ambiguous, ask the user
  or report "Section: inferred as [X]" and proceed.
- **Unavailable evidence (uniform policy)**: when a claim references a table,
  figure, cited paper, or other-section content you cannot access, mark as
  "Needs verification — [source] not available" rather than flagging as
  unsupported. Reserve "unsupported" for claims the *supplied text* fails to
  back.
- **Rewrite-only request**: if the user asks "帮我改" without wanting a full
  audit, still run the 10 checks internally but present only the revised text
  with a brief severity summary.
- **Light review**: if the user asks for a quick look ("快速看一下", "top issues
  only"), run all checks but present only the top 3 highest-severity findings.
- **Long excerpts (>5 paragraphs)**: run each paragraph's checks, then run a
  global Check 10 pass. Audit all paragraphs by default; sample only when the
  user explicitly asks. If output limits prevent completing every paragraph,
  say exactly which paragraphs/checks remain unaudited — never silently sample.
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
**Step B** — For each S(i>1), name its role relative to S1 using the shared
relation labels: **Setup, Evidence, Mechanism, Cause, Consequence, Refinement,
Extension, Contrast, Limitation**. Check 4 uses the same nine labels for
adjacent-sentence relations; do not coin others. Flag MAJOR if a sentence has
no role relative to S1.
**Step C** — If two distinct claims cannot be unified under S1, flag MAJOR:
mixed messages — split. Two claims are distinct when they need different
evidence or lead to different conclusions. Consecutive steps of one procedure,
or a definition followed by the mechanism that refines it, are one message even
when S1 names only the first step; if S1 under-scopes them, flag MINOR and widen
S1 rather than splitting the paragraph.
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

**Baseline accuracy**: verify descriptions of other methods against the cited
paper when it is available; otherwise report "Needs verification — cited source
unavailable" (do not flag as unsupported).

### 4. Sentence-to-Sentence Transitions

Every S(n)→S(n+1) pair needs a nameable logical relation drawn from the shared
labels in Check 1 Step B (Setup, Evidence, Mechanism, Cause, Consequence,
Refinement, Extension, Contrast, Limitation). Check 1 asks how S(i) relates to
S1; this check asks how it relates to the sentence before it.

**Mandatory enumeration**: list every pair with its relation type. Missing one
pair in a 7-sentence abstract means missing ~15% of the checks.

This check flags a missing or masked relation, not narration order. A sentence
that states its own temporal or logical position ("Before truncation, we…",
"Given this bound, …") has named the relation; do not flag it for arriving out
of chronological order.

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

### 6. De-AI Pass (delegated)

`/deai-latex` owns the full pattern catalogue — AI vocabulary, boosters,
stakes-raisers, weasel attributions, authority tropes, aphorism formulas,
copula avoidance, negative parallelism, register violations, hyphenation
position, and the false-positive list that keeps the pass from gutting good
prose. Do not restate it here.

**Procedure.** Load `/deai-latex` in embedded mode and apply its catalogue to
this paragraph yourself — invoking a skill loads its instructions into your own
context, so this is you doing the work, not a call that hands back a result.
Record, for each pattern you hit, its category and the phrase that triggered it.
The zero-skip principle needs those phrases as evidence; a tally is not evidence.

**Severity.** MINOR when hits are isolated. MAJOR when they **cluster** — a
single em dash is nothing, but em dashes plus a forced triple plus an unsupported
booster inside one sentence is a confession. Judge whether the hits pile into the
same sentence or scatter across the paragraph, not how many there are.

**Guardrail.** If a flagged pattern reads clearly in context, keep it.

### 7. Section-Specific Rules

Apply the rules for the identified section type. Read the applicable section's
subsection in `references/section-rules.md` plus the two *(all sections)*
subsections at its end (Footnotes; Number, Unit, and Date Formatting) — not the
rest of the file.

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

Severity: BLOCKING for an undefined or double-used symbol; MAJOR when an
ambiguity changes what is computed (a dimension that does not match its use, an
unstated domain or constraint that alters the result); MINOR for a convention or
wording the reader can resolve from context (Cholesky factor orientation, sum
vs. mean normalization of a loss, "reducing the error from A to B" where A and B
are different objectives).

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
 6. De-AI:      [PASS / MINOR: isolated hits / MAJOR: hits cluster in one sentence]
 7. Section:    [OK / MAJOR: ...]
 8. Boundary:   [OK / MAJOR: S_ belongs in {Experiments/Setup/...}]
 9. Formulas:   [OK / skipped / BLOCKING: symbol X undefined]
10. Consistency: [OK / skipped / MAJOR: terminology drift]

Finding summary: N Blocking / N Major / N Minor
```

Emit every line label above verbatim — `Section role:`, `Strengths:`, and the
eleven numbered check labels through `Finding summary:` — as its own line, with
the colon immediately after the label. Put commentary after the colon, never
between label and colon, and never merge `Section role:` into `0. Preflight:`;
the labels are parsed by downstream tooling.

Severity labels BLOCKING/MAJOR/MINOR are valid in any check — the bracketed
options above are examples, not exhaustive. Count each finding once in the
summary even when it surfaces in multiple checks.

For each issue, provide:
- **Original**: the problematic text
- **Revised**: the replacement
- **Why**: one-sentence reasoning

See `references/examples.md` for good vs bad audit examples. A bare "OK"
without evidence is a failed audit — always show which sentences were assessed.

## After the Audit: Handoff

- **De-AI escalation**: Check 6 already runs `/deai-latex` on this paragraph. If
  the tells cluster across 2+ paragraphs, the problem is the section rather than
  the paragraph — recommend a full-section `/deai-latex` pass.
- **Reflow**: if a rewrite changed length in a page-capped or near-final paper,
  say so and recommend a rebuild. A length change reflows every later page.
- **Figure/table issues**: if Check 3 reveals claim-data mismatches involving
  figures, recommend `/figure-audit` for a visual inspection.
- **Full-paper sweep**: if multiple paragraphs have Blocking issues, suggest
  `/paper-presubmit-audit` for a holistic pass.

Do not auto-invoke other skills. Present findings, let the user decide.

## Reference Files

- `references/writing-philosophy.md` — 10 principles with full rationale and academic sources
- `references/section-rules.md` — detailed per-section conventions (Abstract, Intro, Method, etc.)
- `references/examples.md` — good vs bad audit examples with severity labels
