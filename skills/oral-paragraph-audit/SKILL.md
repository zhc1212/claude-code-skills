---
name: oral-paragraph-audit
description: "Paragraph-level prose-quality audit for ML/NLP papers targeting top venues ('oral' = top-venue prose bar, not spoken language). Use when user says '检查一下这段', 'audit this paragraph', 'oral quality check', '帮我看看这段写的怎么样', '检查写作质量', '帮我改段落', '写作审查', 'paragraph quality', 'review this paragraph', or pastes one to several paragraphs of a paper draft and asks whether they read well. Not for grammar-only proofreading, translation, whole-paper outlining, full-section drafting, or abstract/intro structure (use abstract-intro-audit)."
---

# Oral-Level Paragraph Audit

Audit a paper paragraph against the oral bar: a reviewer understands every
sentence on first read, with no re-reading, looking back, or guessing. Checks
1–5 zoom out one reading scale at a time: sentence, sentence pair, paragraph,
adjacent paragraphs, whole paper. Checks 6–9 apply at every scale: register,
section conventions, claims, and formulas. The principles behind the checks,
with sources, are in `references/writing-philosophy.md`.

## Scope

Audit one paragraph, or several paragraphs in turn. Checks 4 and 5 read the
other paragraphs and sections as context; when auditing a paragraph from a
file, read the paragraphs before and after it.

**Minimal-change rule**: prefer the smallest edit that fixes the issue. Do not
rewrite wholesale unless sentence order or claim structure is broken. When a
fix changes the paragraph count or a heading, show it as `Restructure
(proposal):` an old → new outline, and keep each Revised text within the
current paragraph.

**Zero-skip principle**: in the Audit output shape, every applicable check
shows its work. A pass names what was assessed ("Claims: no strong claim
detected; assessed S1–S3. OK"); a bare "OK" is a failed audit. A check that
does not apply says "skipped" and why. Skipped is valid, silence is not.

**Calibration**: do not invent defects to satisfy a check — an evidence-backed
PASS is a successful audit result. A clean paragraph ends with `0 Blocking /
0 Major` plus the evidence lines. A missing citation for a background technique
is a finding only when the text claims novelty or priority (Check 8); a
technical description that could be read as an implicit claim ("we whiten
before truncation, reducing the error from A to B") is audited for
well-formedness under Check 9, not as an unsupported claim under Check 8.

## Procedure

1. Write the Section role line, then run Checks 1–9 in order.
2. Classify findings. Give each distinct defect one F-number and one severity,
   however many checks it surfaces in:
   - **Blocking**: harms reviewer understanding, credibility, or perceived contribution.
   - **Major**: weakens clarity, evidence, or flow but does not invalidate.
   - **Minor**: style or polish with low effect on reviewer judgment.

   **Severity test**: rate what leaving the text unchanged costs the reader,
   not the size of the fix. A Major must name what the reviewer would misread
   or fail to find; a one-word fix is Major when the word changes the claim or
   the computation.

   **Blocking defaults** — everything else starts at Major or Minor:
   - Section role: a ¶ that does another section's job, or whose `\paragraph{}`
     heading names a job the body does not do.
   - Check 7: an Experiments or Discussion ¶ that opens on numbers whose metric
     or claim the reader cannot tell. A number-first opening the reader can map
     to a claim is rated by the severity test.
   - Check 8: a strong claim the supplied text neither supports nor scopes
     ("outperforms all", "significantly", "the primary cause").
   - Check 9: a symbol undefined at first use or carrying two meanings.

   **Anchors**:
   | Case | Severity |
   |---|---|
   | A dropped "not", a wrong dimension, a number attached to the wrong model | Major or Blocking, though the fix is one word |
   | "reducing the error from A to B" where A and B are different objectives | Minor (Check 9) |
   | A claim unscoped in S1 that later sentences of the ¶ narrow | Minor |
   | A detail the ¶ lacks that another part of the paper may give (seed, split, harness) | Needs verification (Edge Cases), not a finding |
   | A clear, correct paragraph | 0 Blocking / 0 Major, with the evidence lines |
3. Provide replacement text with reasoning for Blocking and Major issues. For
   a Minor issue a one-line note suffices when the fix is obvious. Flag every
   Minor even when you don't rewrite it: at oral level they accumulate into
   reviewer friction.
4. Check every Revised text against its Original before output: no claim,
   mechanism, cause, or scope that neither the paragraph nor a source you read
   gives; the same negations; each number, citation, and macro still attached
   to its noun. When a Revised text replaces a whole sentence or more, write
   the Original and the final Revised to temp files, run `python3 <this skill's
   directory>/../deai-latex/scripts/audit_style.py compare ORIGINAL REVISED`,
   and resolve each difference and review signal; rerun it after any change.
   A statement that fails the check becomes `[fill: …]`.

## Edge Cases

- **Unavailable evidence (uniform policy)**: when a claim references a table,
  figure, cited paper, or other-section content you cannot access, mark as
  "Needs verification — [source] not available" rather than flagging as
  unsupported. Reserve "unsupported" for claims the *supplied text* fails to
  back. The same holds for a detail the ¶ omits that a part of the paper you
  have not read may give; once that part is read and lacks it, it is a finding.
- **Light review**: if the user asks for a quick look ("快速看一下", "top issues
  only"), run all checks but present only the top 3 highest-severity findings.
- **Long excerpts (>5 paragraphs)**: audit every paragraph, then run Check 5
  once over the whole excerpt. Sample only when the user explicitly asks. If
  output limits prevent completing every paragraph, say exactly which
  paragraphs/checks remain unaudited — never silently sample.
- **LaTeX-heavy input**: preserve all macros, `\cite{}`, `\ref{}`, `\label{}`,
  custom commands, and math environments in revised text. Rewrite only the
  prose within them.
- **Non-English draft** (e.g., Chinese): run the checks on the content logic
  but skip Check 6, which is English-specific. Note this in the output.

## The Checks

### Section role (before Check 1)

Name the section type (abstract, intro, related work, method, experiments,
discussion, conclusion; if unstated, infer it from content and say so), the
section's structure (progressive, parallel, claim→evidence, setup→derivation),
and this ¶'s role in it. The section type selects Check 7's rules and the
exceptions in Check 3a, so this line comes first. Flag a paragraph that does
another section's job (a Method mechanism inside Related Work, a result in the
Introduction's opening), and a `\paragraph{}` heading that names a job the
body does not do.

### 1. Sentence

Within each sentence:
- **Subject–verb gap**: report the largest gap between a main subject's head
  noun and its verb, and flag every gap over seven words. For a coordinated
  subject, count from the first conjunct's head noun.
- **Stress position**: the sentence end carries its new information. Flag an
  end that holds old information, a bare citation tail, or a modifier attached
  to the wrong noun.
- **"this"**: use it only as an adjective ("this bound").

A reorder is MINOR unless the misreading changes the claim.

### 2. Transitions (sentence pair)

Name the relation of every S(n)→S(n+1) pair; a 7-sentence paragraph has six
pairs, and each unnamed pair is a skipped check. Use only these nine labels,
which Check 3a also uses: **Setup, Evidence, Mechanism, Cause, Consequence,
Refinement, Extension, Contrast, Limitation**.

**Topic position**: S(n+1) opens on information the reader already has,
usually what S(n) ended on. A cited work named as an instance of a category S1
introduced counts as known. When S(n+1) opens on new material and the link to
S(n) arrives later, flag it and move the linking phrase to the front.

**Gap-masking connectors**: Furthermore, Additionally, Moreover, In addition
assert a relation without naming it. Remove the connector and read the pair:
if the relation is real, replace the connector with it; if not, the sentences
need restructuring. Flag MAJOR when the connector masks a genuine gap.

This check flags a missing or masked relation, not narration order. A sentence
that states its own temporal or logical position ("Before truncation, we…",
"Given this bound, …") has named the relation.

### 3. Paragraph

**3a Structure.** S1 states the paragraph's message; every later sentence
supports it.
- **Step A** — S1 states a claim or setup, not raw data, and does not recap
  the previous paragraph's conclusion: that spends the reader's strongest
  attention position on information they already have.
- **Step B** — Label each S(i>1) by its relation to S1, using Check 2's nine
  labels. Flag MAJOR if a sentence has no relation to S1.
- **Step C** — Two claims that cannot be unified under S1: flag MAJOR, mixed
  messages — split. Claims are distinct when they need different evidence or
  lead to different conclusions. Consecutive steps of one procedure, or a
  definition followed by the mechanism that refines it, are one message even
  when S1 names only the first step; if S1 under-scopes them, flag MINOR and
  widen S1 rather than splitting the paragraph.
- **Step D** — The final sentence interprets, concludes, or advances. An empty
  conclusion ("this contributes to our understanding of X" without saying
  what) is MAJOR.

Dataset/Setup and Limitations paragraphs are factual or enumerative by design:
S1 need not state a claim, and Step D is relaxed.

**3b Density.** Tag every sentence `+new` (adds information), `=echo`
(restates an earlier sentence), or `~filler` (adds nothing). A sentence earns
its place by advancing the argument, introducing evidence, or specifying a
mechanism; one that does none is deletable. Red flags:
- Participial tails that echo the main clause
- Boilerplate formalisms (move to the appendix)
- Discussion with >3 inline numbers
- **Mechanical signposts**: "In what follows…", "Having established X, we now
  turn to Y", "This section discusses…", "This raises the question of…" —
  they narrate the paper's structure instead of advancing the argument
- **Throat-clearing**: "It is important to note that…", "It should be
  mentioned that…", "Worth highlighting is…"
- **Same-paragraph repetition**: a point made 1–2 sentences earlier, restated
  in different words

### 4. ¶ bridge (adjacent paragraphs)

Compare S1 with the last sentence of the previous paragraph. Name the relation
(contrast, specification, deepening, mechanism) and check that the argument
moves forward rather than resetting or circling. Flag MAJOR when consecutive
paragraphs read as a list ("one paragraph on A, one on B, Together these…")
with no relation between them. A `\paragraph{}` heading marks a topic switch;
no bridge needed. Skip when no adjacent paragraph is available.

### 5. Paper (across paragraphs and sections)

**5a Consistency.** One name per concept across paragraphs and sections, no
contradiction between paragraphs, and each acronym used only within the scope
where it is defined. Match every name this ¶ gives the paper's own system or
one of its parts (checker, evaluator, agent, loop) to the name the other
sections use, and report each mismatch. Skip when there is a single ¶ and no
other section.

**5b First use** (runs when other sections are supplied, or when the paragraph
came from a file, in which case grep the source): for each acronym, say where
the paper first spells it out, and for each coined name, where the paper first
defines it. A sentence that uses the acronym without its expansion does not
spell it out. Flag a term never spelled out or defined, or one defined only
after this paragraph uses it.

**5c Placement.** Each sentence has one right place in the paper. Flag a
sentence that belongs in another section: Method content in Experiments,
hyperparameters in Method (they go in Experiments Setup), detailed numerical
comparisons in Related Work (brief prior-work numbers for context are fine).
When other sections are supplied or the paragraph came from a file, also flag
a sentence or argument that another section already states: name both
locations and keep the copy where the claim does its work. An Introduction
preview, a contribution or findings list, a Limitations item, or a Conclusion
that restates the argument in a sentence is not a repeat. A repeated sentence
is MINOR; a repeated argument of several sentences is MAJOR, because in a
page-capped paper it takes space the argument needs.

### 6. De-AI Pass (delegated)

`/deai-latex` owns the full pattern catalogue (inflation, staging, rhythm by
rule, punctuation and connectives against the author's baseline, edit residue,
chat leftovers) and the list of what is not a tell, which keeps the pass from
gutting good prose. Do not restate it here.

**Procedure.** Load `/deai-latex` in embedded mode and apply its catalogue to
this paragraph yourself — invoking a skill loads its instructions into your own
context, so this is you doing the work, not a call that hands back a result.
Record each finding with its family and the phrase that triggered it, and each
dismissed candidate with its reason.
The zero-skip principle needs those phrases as evidence; a tally is not evidence.

**Severity.** MINOR when hits are isolated. MAJOR when they **cluster** — a
single em dash is nothing, but em dashes plus a forced triple plus an unsupported
booster inside one sentence is a confession. Judge whether the hits pile into the
same sentence or scatter across the paragraph, not how many there are.

**Guardrail.** `/deai-latex`'s adjudication step decides which candidates are
findings; a pattern that reads clearly in context is dismissed there, not here.

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

### 8. Claim-Evidence Alignment

Every strong claim needs support within or near the paragraph. Check:
- "X outperforms Y" → table/figure ref or inline number
- "significantly improves" → quantified, not just the word
- "X is the first/novel" → citation gap or novelty argument
- "all / every / never / none" → test it against the paragraph's own examples
  first; one example that breaks it is a contradiction the reader sees on first
  read
- "increasingly / growing / more and more" → evidence of change over time; a
  list of instances shows only that the thing exists

**Scope qualifiers**: strong claims need explicit boundaries. "optimal" →
"optimal for this surrogate". "outperforms all" → add "at every tested ratio".

**Refutable claims** ([SPJ](https://simon.peytonjones.org/great-research-paper/)):
a claim must be specific enough that a reader can tell whether it is true.

**Narrative arc**: if S1 frames a question, the paragraph must answer it by
the final sentence.

**Baseline accuracy**: verify descriptions of other methods against the cited
paper when it is available; otherwise report "Needs verification — cited source
unavailable" (do not flag as unsupported).

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

## Output Format

Pick the shape from the request's verb:
- **Rewrite**: the user asks to change the text (改, 帮我改, 改一下, rewrite,
  fix, polish) and not to check it (检查, 看看, audit, review). Run every check,
  then output only the revised paragraph, the `Finding summary:` line, the
  F-lines as one line each, and `Added facts:`; no check lines and no
  verification notes.
- **Audit**: every other request. Output the template below.

```
¶ [section / heading]

Section role: [section type, structure] — this ¶ serves as [role]. [OK / BLOCKING: role mismatch]
Strengths: [what works well]

 1. Sentence level: largest subject→verb gap S_ ("[head]" … "[verb]", N words); stress position [OK / S_ ends on "[tail]"]
 2. Transitions: S1→S2: [relation]. S2→S3: [...]. ... [OK / MAJOR at S_→S_]
3a. Structure:  S1 message: "[quote]". S2: [relation]. S3: [...]. ... [OK / MAJOR: S_ off-topic]
3b. Density:    S1: [+new]. S2: [...]. ... [OK / MAJOR: S_ echo/filler]
 4. ¶ bridge:   [relation to previous ¶ / skipped (no adjacent ¶)] [OK / MAJOR]
5a. Consistency: [OK / skipped (single ¶, no other section) / MAJOR: terminology drift]
5b. First use:  [TERM → spelled out / defined in §_ / never / skipped (no other part of the paper)]
5c. Placement:  [OK / S_ belongs in {Experiments/Setup/...} / S_ repeats §_]
 6. De-AI:      [PASS / MINOR: isolated hits / MAJOR: hits cluster in one sentence]; baseline: [type and file / none]; findings: ["phrase" (family), …]; dismissed: ["phrase" — reason, …]
 7. Section:    [OK / MAJOR: ...]
 8. Claims:     [OK / MAJOR: "X" unsupported / scope missing]
 9. Formulas:   [OK / skipped / BLOCKING: symbol X undefined]

Finding summary: N Blocking / N Major / N Minor

F1 [BLOCKING / MAJOR / MINOR] (Checks _, _): [the defect, one line]
   [Original / Revised / Why, for Blocking and Major]
F2 ...

Added facts: [none / each statement a Revised text adds]
```

In the Audit shape, emit every labelled line of the template verbatim,
including 3a–3b, 5a–5c, and `Added facts:`, each on its own line, with the
colon immediately after the label. A skipped line still appears, with its
reason. Put commentary after the colon, never between label and colon; the
labels are parsed by downstream tooling.

Severity labels BLOCKING/MAJOR/MINOR are valid in any check — the bracketed
options above are examples, not exhaustive. A check line that finds a defect
cites its F-number with the severity ("MAJOR (F2)"); a defect that already has
an F-number is cited again, not re-rated. The Finding summary counts the
F-lines by severity.

Under each Blocking or Major F-line, provide:
- **Original**: the problematic text
- **Revised**: the replacement, built only from facts in the supplied text and
  in sources you read; a fact the fix needs but the text lacks goes in as
  `[fill: what is needed]`. Keep what the text supplies: a `[fill]` stands
  only for a missing fact, never for content the text already has
- **Why**: one-sentence reasoning

After the last F-line, emit `Added facts:` followed by `none`, or by each
statement about a cited work, a number, or a mechanism that a Revised text makes
and the supplied text does not, so the author can verify it.

See `references/examples.md` for good vs bad audit examples.

## After the Audit: Handoff

- **De-AI escalation**: Check 6 already runs `/deai-latex` on this paragraph. If
  the tells cluster across 2+ paragraphs, the problem is the section rather than
  the paragraph — recommend a full-section `/deai-latex` pass.
- **Reflow**: if a rewrite changed length in a page-capped or near-final paper,
  say so and recommend a rebuild. A length change reflows every later page.
- **Figure/table issues**: if Check 8 reveals claim-data mismatches involving
  figures, recommend `/figure-audit` for a visual inspection.
- **Full-paper sweep**: if multiple paragraphs have Blocking issues, suggest
  `/paper-presubmit-audit` for a holistic pass.

Do not auto-invoke other skills. Present findings, let the user decide.

## Reference Files

- `references/writing-philosophy.md` — the ten principles behind the checks, with academic sources
- `references/section-rules.md` — detailed per-section conventions (Abstract, Intro, Method, etc.)
- `references/examples.md` — good vs bad audit examples with severity labels
