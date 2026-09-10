---
name: paper-presubmit-audit
description: Use for final pre-submission audit of ML/NLP conference papers (AAAI, EMNLP, NeurIPS, ICML, ACL, ICLR). Trigger when the user says "pre-submission check", "final check before submission", "submission-ready", "投稿前检查", or when the paper is near-final and needs a comprehensive quality pass. Runs 18 checks covering build integrity and page budget, PDF package mechanics, submission-policy compliance, anonymization, notation, cross-references, citation fidelity, bibliography quality, float layout, captions and headers, figure quality and accessibility, equation and theorem mechanics, artifact traceability, experimental validity, appendix-body protocol consistency, terminology, prose mechanics, and content red-line logic. Do not use for paragraph-level writing quality (use oral-paragraph-audit) or figure generation (use nature-figure).
---

# Paper Pre-Submission Audit

Run once when the paper is near-final, after content edits and before upload. It
catches what paragraph-level editing cannot see: cross-document inconsistency,
compiled-output defects, and claims that outrun their evidence.

## Two Rules That Override Everything Else

**1. Verify every finding before acting on it.** Recompute from the source artifact
or the compiled PDF before changing any number or claim. A confidently-worded
finding can be wrong, and applying its fix then *introduces* a defect. (Real case:
"three orders of magnitude" → "over two orders" was correct arithmetic against the
wrong residual; the original was right.) When a finding and the document disagree,
*both* may be wrong — check the artifact, not just the two claims.

**2. Re-run the affected check after every fix.** Fixes are not idempotent:
- Ragged-line fixes *relocate* the ragged line rather than remove it (Check 17).
- Any length change reflows pages and can move the page-limit boundary.
- Correcting a number often leaves a stale quantifier around it. (Real case: "All
  methods share ... 6.48 B parameters" — the number was corrected for *one* method
  and the quantifier stayed, so the fix made a new false claim.)
- A deletion can orphan the antecedent of a pronoun in the next sentence, which
  compiles without warning.

Audit → fix → rebuild → re-audit the touched checks. Report the final state.

## Step 0: Build the Venue Profile

Page limits, required sections, and format rules change by year and by track.
**Do not audit against remembered rules.** Fetch this submission's CFP and
style-file docs and record: the content page limit *and what counts toward it*;
where references, limitations, and impact statements sit; whether the supplement is
a separate upload and when it is due; the anonymity and preprint regime; required
statements and which are separate forms; format prohibitions; upload size and page
size. None of these is guessable — a venue may allow a 9-page PDF while permitting
only 7 pages of content, so content on page 8 violates a limit the page count
satisfies.

Encode the page rule as a **script gate the build fails on**, so Rule 2 re-runs it
after every edit. If the CFP is unavailable, say so, state what you assumed, and
mark every venue-dependent finding provisional.

## How to Run

Delegate the reading-heavy judgment checks (7, 10, 13, 14, 15, 16, 17, 18) to
parallel subagents; do the mechanical ones yourself with grep/python. Every
subagent gets these constraints:
- **No LaTeX compiler.** One build lock per directory; concurrent compiles corrupt
  `.aux`/`.bbl` and produce phantom undefined-reference errors. Read the built PDF.
- **No edits.** Agents report, the orchestrator fixes — serializing fixes is what
  makes Rule 2 enforceable.
- **An evidence-backed PASS is a successful result.** Name what was inspected.
- **Do not modify source unless the user asked for fixes.** An "audit" or "check"
  request often authorizes inspection only. In report-only mode, record the proposed
  fix and use the `proposed` disposition rather than `fixed`.
- Receive the source layout explicitly: which line ranges are body, which are
  supplement, which PDF is which.

## Multi-Document Papers

When the paper and supplement are separate uploads — even from one `.tex` — each is
standalone to the reader:
- Every acronym expanded and every symbol defined in **each** PDF. Watch for a
  symbol whose first supplement appearance is inside a float on page 1, above the
  prose that would define it.
- Cross-document `\ref`s render as bare "Table A9"; state once where they live. A
  label defined in one document and referenced only from the other is correct by
  design; referenced from neither, it is dead.
- Where the venue profile permits an unlimited supplement, page count stops being a
  constraint but reviewer attention and the supplement's own float queue do not.

## The 18 Checks

### 1. Build Integrity, Page Budget, Section Order
- Zero compiler errors and zero undefined references. Overfull hboxes: use whatever
  the venue specifies; absent a rule, ~1pt is a readability heuristic, not a gate.
- Page rule from the venue profile, enforced as a gate, re-run after every edit.
- **Every fix is a page-budget transaction.** Classify each as cut / neutral / add
  before applying, prefer cuts in the body, and track the running balance — a batch
  of "+3 words" fixes silently overflows.
- Section order per the venue profile.
- `Underfull \vbox` in two-column layouts with floats is normal, not a finding.

### 2. PDF Package Mechanics
- Page size uniform and correct on **every** page; an included figure with a
  different MediaBox can change one.
- Under blind review, inspect `pdfinfo` (Author, Title, Producer, Keywords) for
  identity leakage. These fields need not be empty — they must not identify anyone.
- File size within the upload cap; bloat is usually unsubsetted fonts or rasters.
- All fonts embedded (`pdffonts`: every row `emb yes`). Subsetting is a size
  optimization unless the venue requires it.
- No encryption, forms, or JavaScript; opens without viewer warnings.
- Text extractable (`pdftotext` returns prose) — similarity screening needs it.

### 3. Submission-Policy Compliance
- Required statements present and in the required form: ethics or broader impact,
  reproducibility checklist, limitations, funding and conflicts.
- Dataset and model licenses compatible with the stated use, attributed as required.
  Compatibility is often not decidable from the paper alone: check the supplied
  license records, and otherwise report `not verifiable` rather than noncompliance.
- LLM-assistance disclosure, and human-subjects or annotation statements, where the
  venue requires them.
- Items the venue collects in a **separate form** are author action items, not paper
  findings; list them apart.
- Every item comes from the Step 0 profile. Do not invent requirements; where the
  profile is silent, say so.

### 4. Anonymization
- Author line anonymized, acknowledgments suppressed. Self-citation follows the
  venue's policy; flag only wording that reveals identity ("our previous work"),
  not the citation itself.
- No repo, model-hub, or release URLs that identify the authors. A third-party tool
  URL is not a leak — distinguish the two before reporting.
- No absolute paths, usernames, or institutional strings. Check the **rendered
  PDF**, not only the source, and check figure files (`pdftotext figs/x.pdf -`):
  figures leak because generating scripts embed local names.
- **Expect false positives** — cited authors' surnames match a name grep. Report
  only genuine leaks and say how many you filtered.

### 5. Notation: Symbols and Acronyms
- Every symbol defined at or before first use in each document, with whichever of
  domain, type, shape, or units applies — a dimensionless scalar, an index set, or a
  predicate needs a type, not a dimension.
- **Near-synonym symbols are the high-risk case.** Where a paper distinguishes
  several forms of one quantity (pre-clip, clipped, integer, final), verify each use
  carries the right one and that the distinction is stated where the reader meets
  it. These drift silently under editing.
- Grep for collisions: one letter bound twice with different meanings.
- A footnote marker attached directly to a symbol renders as an exponent.
- Acronyms: grep uppercase 2–5 letter runs, then filter — most hits are LaTeX
  keywords, environment names, cited method names, or field-universal terms. What
  survives is usually real. Systems and tooling acronyms are most-missed, because
  they enter through hyperparameter tables rather than prose.

### 6. Cross-Reference Correctness
- Zero `??`; every `\cite` has a bib entry.
- Orphan bib entries are harmless — BibTeX does not render uncited ones; verify
  against the `.bbl` first. Never-`\ref`'d float labels are the real signal.
- **Verify each reference target contains what the sentence claims.** This finds
  real errors and cannot be automated. Recurring failures: consecutive sentences
  citing one appendix where the second belongs elsewhere; a per-seed claim pointed
  at a figure plotting only a mean; a hardcoded `Figure 3` instead of a `\ref`,
  silently wrong the moment a float is added; a float pointed at by a bare "in this
  table", ambiguous once it moves.

### 7. Citation Fidelity
The `\cite` resolves but the cited work does not support the attached claim.
Reviewers who know the work catch these, and they read as careless.
- For every citation attached to a *characterization* of prior work — its
  objective, mechanism, what it optimizes, what it reports — verify against the
  paper or its official implementation.
- For every citation attached to a *general claim* ("X is a known failure mode of
  Y"), check whether the cited work makes that claim or merely instantiates Y.
  Foundational papers are routinely miscited for critiques that appeared later.
- Where a comparison table marks a competitor's property "not reported", confirm it
  truly is; marking a documented property unreported understates a competitor.
- Re-examine every inference *downstream* of a mischaracterization.

### 8. Bibliography Quality
- Every entry carries the fields the style needs; no `??`, empty braces, or stray
  LaTeX in the rendered output; no duplicate entries under different keys.
- Prefer the published version where one exists, unless the preprint is materially
  different or the claim depends on it. Mixing the two arbitrarily is the finding.
- Copy every field from one canonical record rather than assembling them, so venue
  names, years, and author lists stay internally consistent.
- Capitalization protected where the style lowercases titles.
- Its line breaking belongs to the style file: report defects, do not fix them by
  editing the style file.

### 9. Float Layout
- Same-page-or-next placement is a useful diagnostic, not a pass condition. Map
  float page and first-reference page via `pdftotext` — never infer from source
  order — and report the distance rather than a verdict.
- A float whose reference is on its own page is ideal, not a defect — count
  same-page mentions before reporting detachment.
- Every algorithm `\ref`'d within its own document; float width macro matches the
  single- or double-column environment.
- A full-width float in a two-column layout can strand itself pages from its
  mention; check whether a single-column version fits, which usually fixes it.

### 10. Captions and Table Headers
- Captions self-contained enough to make the float interpretable alone, and stating
  the result the float supports where there is one. A caption that gives only
  provenance leaves a skimming reviewer with no conclusion; a caption for a purely
  descriptive float legitimately has no takeaway to state.
- Symbols and abbreviations in a caption reachable within the same document.
- Direction arrows where better-is-higher or better-is-lower, especially where
  same-direction columns sit beside one of the opposite direction.
- Units in header or caption; state which binary prefix and match the artifact.
- Arrow, unit, and bold-marking consistency **across** sibling tables.
- Absence of markers is right for correlations, digests, configuration values, and
  category labels; absence of bold is right where values tie or the table reports
  deltas. Say why rather than flagging blindly.
- Each average over a task set names the tasks included.

### 11. Figure Print Quality and Accessibility
- Zero Type 3 fonts, verified with `pdffonts` on each figure *and* the final PDFs.
  Plotting libraries emit them by default, so make this a build gate.
- Effective font size after LaTeX scaling: use the venue's minimum where it states
  one, otherwise ~7pt as a readability heuristic. Compute it — scale = target width
  from the `\includegraphics` call ÷ native page width of the figure PDF, effective
  = authored size × scale — and report the minimum with the scale you used.
- Automatic sub- and superscripts are set well below the base size, so a figure
  whose base size passes can have every subscript fail. **Measure the ratio in this
  file** rather than assuming one; it depends on the authoring tool and the font.
- Colour distinguishable in greyscale and under common colour-vision deficiencies;
  never colour alone to carry a distinction — pair it with marker, linestyle, or
  direct labelling. Check the legend's own contrast.
- No annotation/data overlap; no text clipped at the bounding box.

### 12. Equation and Theorem Mechanics
- Displayed equations punctuated as part of the sentence containing them.
- Numbered equations that are never referenced: flag for review, since numbering
  usually signals an intent to reference. This is house style, not correctness.
- **Units and shape are separate audits.** Check unit consistency across both sides
  where the quantities carry units, and shape/type compatibility at every product's
  inner dimension where they are matrices or tensors. Do not conflate them.
- Every index range, summation set, and optimization domain either explicit or
  unambiguous from notation already established.
- Theorems: assumptions stated in the statement rather than only in the proof; every
  symbol in the statement bound; the conclusion following from the stated
  assumptions, and the conditions for applying the result actually satisfied where
  the paper applies it. BLOCKING only when a central claim rests materially on a
  result whose assumptions the paper's own setting violates.
- The relation symbol must match the intended claim — identity, definition,
  approximation, or measured equality. An empirical regularity written as an
  identity is a real error even when the numbers agree; "accuracy $= 82\%$" is not.
- State what you could not verify. A nontrivial proof may warrant `not fully
  verified` rather than a pass or a finding.

### 13. Artifact Traceability and Number Precision
A reviewer who recomputes one number and gets a different answer distrusts every
number. Artifact availability is **per statistic, not per paper**: recompute every
printed statistic — mean, standard deviation, percentage, delta — for which the raw
inputs and the aggregation definition both exist, not spot-checks. For the rest the
check becomes traceability: the number names a source, and any that cannot be traced
is disclosed or dropped. Report the split.
- **Rounding**: recompute from full-precision values, never from printed ones.
- **Aggregate presented as per-instance**: "costs 6.7% in all three seeds" when 6.7%
  is the mean and the per-seed values are 5.4 / 8.9 / 5.9.
- **Comparator substitution**: two numbers each correct against a different
  comparator, reported side by side with one comparator stated, are wrong together.
- **Stated bounds**: a claimed `≥ 0.76` is violated by a printed `0.758`. Prefer the
  exact value to a rounded bound; it is usually the same length.
- **Scope creep**: a value measured at one setting, introduced with "throughout".
- **Untraceable numbers**: write "Not verifiable from available artifacts", then drop
  or footnote it. Where the document already discloses unpreserved provenance
  somewhere, follow that precedent rather than inventing a second one.
- **Superseded values**: do not quote an old single-run value beside new multi-seed
  means. If two campaigns disagree *in sign*, that is adverse — disclose it, refuse
  to pool them, narrow the claim, and tell the author before rewriting any narrative
  around it.
- Decimal places consistent within a column.

**Automated consistency scans here are mostly false positives.** Exclude
configuration tables, header rows, and spanned cells first, then check whether the
"inconsistent" values are different quantities on different rows.

### 14. Experimental Validity
Checks 1–13 verify the paper describes its experiments accurately. This one asks
whether the experiments support the claim at all; internal consistency does not
repair a confounded comparison.
Sort every observation into **verified defect**, **undocumented — the paper does not
say**, or **not establishable from the supplied artifacts**. Reporting the third as
the first is the failure mode of this check.
- **Split identity**: for the paper's own controlled comparisons, require the same
  evaluation split, tokenization, windowing, and metric definition across arms, or a
  demonstrated equivalence. Numbers taken from the literature may follow another
  protocol — then the requirement is that they be labelled non-comparable, not that
  they match.
- **Selection leakage**: whether checkpoint selection, hyperparameter search, or
  early stopping touched the test split, or used a validation split differing
  between arms.
- **Comparable budgets**: budgets appropriate to the claim, matched where matching
  is feasible, and disclosed or justified where they differ. A sweep run on the
  proposed method and not on the baseline is an asymmetry to record, not
  automatically a defect.
- **Contamination**: usually not provable absent from a paper and its source.
  Classify as documented-clean, evidenced-risk, or unknown. Also check whether
  calibration or few-shot data overlaps the evaluation data, which often *is*
  checkable.
- **Claim scope vs. evidence scope**: an n=1 ordering presented as a ranking, one
  architecture family as general, two ratios as a trend, a correlation as a cause.
- BLOCKING only for a *verified*, material confound under a headline claim. The
  remedy may be narrowing the claim or rerunning; say which, and do not assume
  narrowing is always available.

### 15. Appendix–Body Protocol Consistency
- Every protocol the body states matches the appendix: sample and step counts,
  seeds, splits, optimizer and its precision, early-stopping rule.
- A number appearing in both places is identical. Grep each body *number* in the
  appendix rather than trusting they were written together.
- Where the appendix documents an exclusion — a dropped run, an infeasible arm — the
  body's counts reflect it.
- Where the appendix reports a superseding campaign, the body does not quote the
  older value without disclosure (Check 13).
- Reviewers need not read the appendix, so the body must carry enough to interpret
  every headline claim. Detailed protocols and proofs may still live in the appendix.

### 16. Terminology Consistency
- Build a glossary from the Method section; grep every occurrence and synonym;
  classify each as consistent or meaning-shifted.
- Ambiguous families to expect: layer/block/sublayer, module/component/projection,
  per-layer/per-block/per-matrix, arm/configuration/condition.
- **MAJOR** when one term carries two meanings in one paragraph, an ambiguous term is
  used without specifying the sense, or a term describing a baseline contradicts what
  the baseline does (overlaps Check 7).
- Check cross-section *drift*: a concept renamed between Method and Experiments.
- A term used dozens of times and never defined is worth a parenthetical at first
  use — unless it is field-standard for this venue's readers, in which case it is not
  a finding. Say which judgement you made.

### 17. Ragged Paragraph Endings
A paragraph whose final rendered line holds one or two words leaves a visible gap a
reviewer sees before reading a word. Worth a dedicated check because it is invisible
in the source.

**Measure geometrically, not with plain `pdftotext`** — its default mode merges some
rendered lines, so it both misses real cases and invents fake ones. Use
`pdftotext -bbox-layout` for per-line bounding boxes, group lines into `<block>`s,
and compute `width(last line) / max(line width in block)`. Flag below 0.35 with at
most 4 words (detection threshold); aim for at least 0.5 after the fix (target
threshold). Those two numbers are the only ones — do not introduce a third.
- Restrict to prose: exclude blocks under three lines, blocks whose max width is
  well below the text measure (table cells), equation and algorithm interiors, and
  the bibliography. Verify the last line holds a real word before reporting.
- **Derive the sizing constants from this document**: measure = max line width in
  body blocks; character width ≈ measure ÷ mean characters per full line. Never
  carry these numbers in from another paper.
- **Size the edit or you will just move the problem.** A ±1-word change relocates
  which word is orphaned. Remove at least the full width of the offending line, or
  add enough to fill it past half.
- Page-capped documents: prefer cuts in the body and re-run the page gate after
  each, since a cut is the only fix guaranteed not to break it. Adds are allowed
  while the gate still passes — this is the same cut/neutral/add accounting as
  Check 1, not a stricter rule.
- Some blocks are out of scope: bibliography entries belong to the style file, and
  some rendered braces are an algorithm package's comment delimiters, not bugs. Say
  which cases you left and why.
- Re-measure after fixing (Rule 2). Expect two or three iterations.

### 18. Prose Mechanics and Content Red-Line
Mechanics, reported as counts with the worst examples rather than exhaustively:
hyphenation unified per family; British/American consistency; missing `~` before
`\cite`/`\ref` — but a non-breaking space in a narrow table cell prevents a needed
line break, so verify context before adding one; double spaces; doubled words. Grep
specifically for doubled negations: a hand-edit replacing "not already X" with "not
yet X" yields "not not yet X", which compiles and inverts the meaning.

Content red-line, **BLOCKING only**, style out of scope:
- **Logic contradictions across sections**: a parameter frozen in Method and trained
  in Experiments; a universal claim contradicted by a run reported elsewhere; a
  bound violated by a printed value. Grep universal quantifiers — "every", "all
  reported", "always", "never" — and test each against the exceptions; this is the
  most productive single query in the audit.
- **Abstract and Introduction claims with no support**: enumerate every quantitative
  claim and locate its table, figure, or appendix. Report any whose support is
  absent, weaker, or about something else.
- **Conclusion numbers** matching the tables.
- **Severe grammar** only where meaning is genuinely ambiguous, a negation is missing
  or doubled, or a modifier attaches to the wrong subject. Read recently hand-edited
  regions with extra care — these cluster there, and the audit's own fixes are hand
  edits.

## Output Format

```
# Pre-Submission Audit Report

## Summary
Checks passed: X/18 (run: N, deferred: N, not applicable: N)
Blocking: N | Major: N | Minor: N
Findings raised: N | verified: N | fixed: N | proposed: N | rejected: N | deferred: N
Venue profile: [source, or "assumed — findings provisional"]

## Per-check results
1..18, each naming what was inspected

## Disposition ledger
| # | Check | Finding | Severity | Disposition | Evidence |
```

Every finding raised anywhere gets a row, including those that did not survive:
- `verified` — confirmed real and deliberately left unchanged; say why.
- `fixed` — changed, with the re-run that confirms it (Rule 2).
- `proposed` — the fix is written out but not applied, in report-only mode.
- `rejected` — with the recomputation showing the finding was wrong. A deliverable,
  not an aside: acting on it would have inserted a defect.
- `deferred` — with a reason and an owner.

A check counts as passed only if it ran to a conclusion. One that could not be
completed is `deferred` or `not applicable` in the header count, never a pass.

Close with **author action items** (separate-form and policy items that are not
paper edits) and the **final build state**: page count, where references begin,
undefined-reference and Type 3 counts, figure minimum effective font size, and
ragged-ending count before → after.

Severity:
- **Blocking**: desk-reject or certain reviewer complaint — format prohibition,
  broken refs, anonymization leak, page overflow, a number contradicting its
  artifact, a headline claim resting on a confounded comparison.
- **Major**: unprofessional or factually wrong — undefined symbol, miscited
  baseline, mean reported as per-instance, body/appendix protocol mismatch.
- **Minor**: cosmetic — missing `~`, hyphenation, a caption that only describes.

Never modify a venue-provided `.sty` or `.bst`. Where a defect belongs to the style
file, report it and stop.
