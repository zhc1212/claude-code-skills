---
name: oral-paragraph-audit
description: "Audits or rewrites one to several paragraphs of an ML/NLP paper draft against the top-venue ('oral') prose bar: sentence clarity, transitions, paragraph structure, consistency with the rest of the paper, and claim–evidence boundaries. Use when the user asks to check a paper paragraph or whether it reads well or flows (检查一下这段, 帮我看看这段写的怎么样, 衔接顺不顺, audit or review this paragraph), or to rewrite one (帮我改段落, 改一下这段). Not for grammar-only proofreading, translation, whole-paper outlining, full-section drafting, abstract/intro structure (abstract-intro-audit), or a whole-paper defensive-writing sweep (defensive-writing-sweep)."
---

# Oral-Level Paragraph Audit

Audit a paper paragraph against the oral bar: a reader understands every
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

## Procedure

1. Write the Section role line, then run Checks 1–9 in order.
2. Classify every finding by the Severity section below.
3. Provide replacement text with reasoning for Blocking and Major issues. For
   a Minor issue a one-line note suffices when the fix is obvious. Flag every
   Minor even when you don't rewrite it: at oral level they accumulate into
   reader friction. Build every Revised text only from facts in the supplied
   text and in sources you read; a fact the fix needs but the text lacks goes
   in as `[fill: what is needed]`. Keep what the text supplies: a `[fill]`
   stands only for a missing fact, never for content the text already has.
4. Check every Revised text against its Original before output: no claim,
   mechanism, cause, or scope that neither the paragraph nor a source you read
   gives; no boundary the claim does not need (Check 8, Boundaries); the same
   negations, except those in a deleted boundary; each number, citation, and
   macro still attached to its noun. When a Revised text replaces a whole sentence or more, write
   the Original and the final Revised to temp files, run `python3 <this skill's
   directory>/../deai-latex/scripts/audit_style.py compare ORIGINAL REVISED`,
   and resolve each difference and review signal; rerun it after any change.
   A statement that fails the check becomes `[fill: …]`.
5. Whenever you apply Revised texts to a file, in this turn or after the
   author approves them later, recheck before reporting. The
   `compare` report covers protected spans and new content words only; it
   cannot see a lost blank line, a subject–verb gap that grew, or an anaphor
   that now binds to the wrong sentence. Done when: every changed sentence and
   the sentence on each side of it re-pass Checks 1–4; every sentence a clause
   was moved or deleted *out of* still holds for each item it describes; text
   moved *into* another paragraph keeps its numbers, scope, and conditions and
   relates to that paragraph's S1; and the blank lines around the edited span
   match the original. A regression gets its own F-line. The report on the
   applied edits ends with `Recheck: <each changed sentence by location> and
   its neighbours re-passed Checks 1–4; moved into: …; deletion sites: …;
   blank lines match; regressions: F… or none`; a report without this line
   has skipped the step.

## Severity

Give each distinct defect one F-number and one severity, however many checks
it surfaces in. A check line that finds a defect cites its F-number with the
severity ("MAJOR (F2)"); a defect that already has an F-number is cited again,
not re-rated. The Finding summary, written after the F-lines, counts them by
severity.

- **Blocking**: harms the reader's understanding, the paper's credibility, or
  its perceived contribution.
- **Major**: weakens clarity, evidence, or flow but does not invalidate.
- **Minor**: style or polish with low effect on how the paper is judged.

**Severity test**: rate what leaving the text unchanged costs the reader, not
the size of the fix. A Major must name what the reader would misread or fail
to find; a one-word fix is Major when the word changes the claim or the
computation.

**Calibration**: do not invent defects to satisfy a check — an evidence-backed
PASS is a successful audit result. A clean paragraph ends with `0 Blocking /
0 Major` plus the evidence lines. A missing citation for a background technique
is a finding only when the text claims novelty or priority (Check 8); a
technical description that could be read as an implicit claim ("we whiten
before truncation, reducing the error from A to B") is audited for
well-formedness under Check 9, not as an unsupported claim under Check 8.

**Defaults by check.** Rate each finding from its check's row. A case the
table does not list, and a number-first opening the reader can map to a claim,
are rated by the severity test.

| Check | Blocking | Major | Minor |
|---|---|---|---|
| Section role | a ¶ that does another section's job; a `\paragraph{}` heading naming a job the body does not do | | |
| 1 Sentence | | a misreading that changes the claim or the computation; a hidden premise the paper later contradicts or a later ¶ relies on | other reorder, wording, referent, and hidden-premise findings |
| 2 Transitions | | a connector masking a genuine gap | |
| 3a Structure | | a sentence with no relation to S1; two messages in one ¶; an empty final sentence | a progressive chain whose S1 states only the first link; an S1 that under-scopes consecutive steps |
| 3b Density | | a sentence that is echo or filler | a filler phrase inside a sentence that earns its place |
| 4 ¶ bridge | | consecutive ¶s that read as a list; a gap or claim resting on a premise no earlier ¶ states | |
| 5a Consistency | | a word whose two senses change a number's object | a word with two senses in the reader's view |
| 5c Placement | | an argument of several sentences that another section already states | a repeated sentence |
| 6 De-AI | | hits that cluster in one sentence | isolated hits |
| 7 Section | an Experiments or Discussion ¶ that opens on numbers whose metric or claim the reader cannot tell | | |
| 8 Claims | a strong claim the supplied text neither supports nor scopes ("outperforms all", "significantly", "the primary cause") | a class that includes the paper's own method; a citation assigned to the wrong category; a standalone defensive boundary, or one that retreats from a supported claim | one citation list shared by several adjectives; a redundant qualifier inside a correct sentence |
| 9 Formulas | a symbol undefined at first use or carrying two meanings | an ambiguity that changes what is computed (a dimension that does not match its use, an unstated domain or constraint that alters the result) | a convention or wording the reader can resolve from context (factor orientation, sum vs. mean normalization) |

**Anchors**:
| Case | Severity |
|---|---|
| A dropped "not", a wrong dimension, a number attached to the wrong model, setting, or aggregation (a range across settings readable as a range across seeds) | Major or Blocking, though the fix is one word |
| "reducing the error from A to B" where A and B are different objectives | Minor (Check 9) |
| A claim unscoped in S1 that later sentences of the ¶ narrow | Minor |
| A detail the ¶ lacks that another part of the paper may give (seed, split, harness) | Needs verification (Edge Cases), not a finding |
| A clear, correct paragraph | 0 Blocking / 0 Major, with the evidence lines |

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
- **Wording**: the verb fits its object ("score weights *with* proxies" is a
  stretch; "rank by a proxy computed on weights" is not); no content word
  appears twice in one sentence ("differentiable gates make the loss
  differentiable"); a quantity named in prose carries the right unit ("rank
  shares that sum to the parameter budget" adds ranks to parameters — a wrong
  dimension, rated by the Anchors).
- **Referents**: every anaphor ("it", "there", "the same setting", "the
  methods above") binds to the candidate a first-time reader would pick, which
  is usually the nearest. When the nearest candidate is the wrong one, flag it.
- **Hidden premise**: the sentence reads correctly only if the reader already
  holds an unstated fact ("Even per-matrix optimal truncation…" presumes
  Eckart–Young).

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
need restructuring. Flag the connector when it masks a genuine gap.

This check flags a missing or masked relation, not narration order. A sentence
that states its own temporal or logical position ("Before truncation, we…",
"Given this bound, …") has named the relation.

### 3. Paragraph

**3a Structure.** S1 states the paragraph's message; every later sentence
supports it. First name the paragraph's organization: claim→support (总分),
progressive chain (each sentence starts from the previous one's end; 递进),
parallel list, or setup→derivation. A progressive chain is valid. When its S1
states only the first link and the chain ends on a claim S1 does not
anticipate (a gap, a challenge), flag it and offer a topic S1 that states
where the chain ends.
- **Step A** — S1 states a claim or setup, not raw data, and does not recap
  the previous paragraph's conclusion: that spends the reader's strongest
  attention position on information they already have.
- **Step B** — Label each S(i>1) by its relation to S1, using Check 2's nine
  labels. Flag a sentence that has no relation to S1.
- **Step C** — Two claims that cannot be unified under S1 are mixed messages:
  split. Claims are distinct when they need different evidence or
  lead to different conclusions. Consecutive steps of one procedure, or a
  definition followed by the mechanism that refines it, are one message even
  when S1 names only the first step; if S1 under-scopes them, flag it and
  widen S1 rather than splitting the paragraph.
- **Step D** — The final sentence interprets, concludes, or advances. An empty
  conclusion ("this contributes to our understanding of X" without saying
  what) is a finding.

Dataset/Setup and Limitations paragraphs are factual or enumerative by design:
S1 need not state a claim, and Step D is relaxed. A contribution list is audited
item by item instead: the bold title is that item's S1, Step C applies to the
item, and the title covers every sentence under it.

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
moves forward rather than resetting or circling. Flag consecutive
paragraphs that read as a list ("one paragraph on A, one on B, Together these…")
with no relation between them. A `\paragraph{}` heading marks a topic switch;
no bridge needed. Skip when no adjacent paragraph is available.

When the next ¶ is available, also look forward: the sentence that states the
next ¶'s gap or main claim must not rest on a premise that neither this ¶ nor
an earlier one states (a gap "chosen during recovery" when no ¶ has said that a
recovery stage exists). A term the next ¶ uses before defining
it stays with 5b.

### 5. Paper (across paragraphs and sections)

**5a Consistency.** One name per concept across paragraphs and sections,
modifiers included ("soft prefix gates" here, "differentiable prefix gates" in
the abstract), and one concept per word within the reader's view: adjacent
sentences and the items of one list ("frozen" profile in one item, "frozen"
factors in the next); flag a word with two senses there. Also: no
contradiction between paragraphs, and each acronym used only within the scope
where it is defined. Match every name this ¶ gives the paper's own system or
one of its parts (checker, evaluator, agent, loop) to the name the other
sections use, and report each mismatch. With a single ¶ and no other section,
run only the within-view part and mark the cross-section part skipped.

**5b First use** (runs when other sections are supplied, or when the paragraph
came from a file, in which case grep the source): for each acronym, say where
the paper first spells it out, for each coined name, where the paper first
defines it, and for each symbol or clipped term in a non-technical section ("ρ"
or "pre-clip" in an Introduction), where it is defined. A sentence that uses the acronym without its expansion does not
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
that restates the argument in a sentence is not a repeat. A repeated argument
takes page space the argument needs.

### 6. De-AI Pass (delegated)

`/deai-latex` owns the full pattern catalogue (inflation, staging, rhythm by
rule, punctuation and connectives against the author's baseline, edit residue,
chat leftovers) and the list of what is not a tell, which keeps the pass from
gutting good prose. Do not restate it here.

**Procedure.** Load `/deai-latex` in embedded mode once per conversation; on
later paragraphs apply the catalogue already in this window. Apply it to this
paragraph yourself — invoking a skill loads its instructions into your own
context, so this is you doing the work, not a call that hands back a result.
Record each finding with its family and the phrase that triggered it, and each
dismissed candidate with its reason.
The zero-skip principle needs those phrases as evidence; a tally is not evidence.

**Clustering.** A single em dash is nothing, but em dashes plus a forced triple
plus an unsupported booster inside one sentence is a confession. Judge whether the hits pile into the
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
- "all / every / never / none / each / existing methods" → test it against the
  paragraph's own examples first, then against each cited work, using the
  paper's own comparison table or Related Work when the cited source is
  unavailable; one example that breaks it is a contradiction the reader sees on
  first read. A class the sentence describes ("differentiable allocators") must
  exclude the method the paper proposes; when it includes it, the sentence is
  false as written
- "increasingly / growing / more and more" → evidence of change over time; a
  list of instances shows only that the thing exists

**Boundaries**: a claim is as wide as its evidence. Its boundary is the scope
words that make the sentence true ("optimal for this surrogate", "on WT2 in
every seed"), stated once, inside the claim. A sentence the evidence supports
for one model, setting, or metric but states generally is unscoped: add the
scope words. A number whose model, setting, metric, or aggregation the reader
cannot tell from its sentence and ¶ is a finding; when it is attached to the
wrong one, the Anchors rate it.

Everything beyond that writes for an anticipated reviewer instead of the
reader: a sentence on what the result does not show ("does not establish", "we
do not claim"), a doubt the evidence does not raise, a generic scope ("in the
evaluated settings"), "should be read as X rather than Y", a qualifier that
repeats a scope the ¶ already states, an unfavourable side result the claim's scope already excludes,
or an untested explanation attached to one. Such a boundary leaves the reader's
understanding unchanged and lowers their confidence in a result the evidence
supports. Test each boundary by deleting it. If the claim it qualifies stays
true on the paper's evidence, the boundary is defensive: delete it. If that
claim becomes false, the boundary is part of the claim: fold it into the
claim's scope words, once in the reader's view. Dropping a reported result is the author's call:
the F-line names the result. A Limitations ¶ states grounded limits by design
and is exempt.

**Refutable claims** ([SPJ](https://simon.peytonjones.org/great-research-paper/)):
a claim must be specific enough that a reader can tell whether it is true.

**Narrative arc**: if S1 frames a question, the paragraph must answer it by
the final sentence. A question posed for later (an Introduction's research
questions) instead names, or is answered by, the contribution item or section
that answers it.

**Baseline accuracy**: verify descriptions of other methods against the cited
paper when it is available; otherwise report "Needs verification — cited source
unavailable" (do not flag as unsupported). Each citation sits on the category
or adjective it supports: one citation list shared by several adjectives leaves
the reader unable to map them; once split, each assignment must match the
paper's own description of that work.

### 9. Formula Rigor (Method/Appendix only)

Symbol hygiene (defined near first use, no dual meanings, consistent
subscripts), dimensional consistency of the formulas (units named in prose are
Check 1's Wording), completeness (explicit min/sum/domain),
notation consistency with rest of paper.

Skip for non-technical sections.

## Output Format

Pick the shape from the request's verb:
- **Rewrite**: the user asks to change the text (改, 帮我改, 改一下, rewrite,
  fix, polish) and not to check it (检查, 看看, audit, review). Run every check,
  then output exactly four parts, in this order, and end there: the revised
  paragraph, the F-lines one line each, the `Finding summary:` line, and
  `Added facts:`. The checks speak through the F-lines; the Section role,
  check lines, and ledger belong to the Audit shape. This shape overrides the
  zero-skip principle and the Handoff notes: a check with no finding writes
  nothing, and a Needs-verification item or a reflow note becomes one line
  under `Added facts:`.
- **Audit**: every other request. Read `references/audit-format.md` and emit
  its template, every labelled line verbatim.

Both shapes write the F-lines in this form, then the summary line, which
counts the F-lines above it:

```
F1 [BLOCKING / MAJOR / MINOR] (Checks _, _): [the defect, one line]
Finding summary: N Blocking / N Major / N Minor
```

Both end with `Added facts:` followed by `none`, or by each statement about a
cited work, a number, or a mechanism that a Revised text makes and the
supplied text does not, so the author can verify it.

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

- `references/audit-format.md` — the Audit template, ledger, and label rules
- `references/writing-philosophy.md` — the eleven principles behind the checks, with academic sources
- `references/section-rules.md` — detailed per-section conventions (Abstract, Intro, Method, etc.)
- `references/examples.md` — good vs bad audit examples with severity labels
