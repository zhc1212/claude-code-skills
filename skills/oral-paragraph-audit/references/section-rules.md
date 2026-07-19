# Section-Specific Rules (Check 7 Detail)

## Abstract

Should cover problem, method, main result, and implication (order may vary).

- **No bare math symbols.** Every symbol must be universally standard ($n$, $k$, $\mathcal{O}$)
  or defined in the same sentence. Replace method-specific symbols with prose. Severity: **MAJOR**.
- **No unexplained method-name jargon.** Opaque names from other papers → descriptive phrases.
  Your own method name is fine. Severity: **MAJOR**.
- **Expand all abbreviations** on first use unless universally standard at the target venue.
- **No section or table references** — the abstract is read in isolation.

## Introduction

Progressive: problem → challenge → positioning. Each paragraph carries one message.

- Opening ¶: task importance + landscape (not problem + solution mixed)
- Challenge ¶(s): lead to the EXACT technical challenge solved; do not present naive
  baseline then improve it (makes work look incremental)
- Solution ¶: insight first, then method name, then surprise/key finding
- Final ¶ (or contribution list): Thesis → method sketch → headline number → scope → deepest insight.
  Every contribution claim must be verifiable in Experiments.

## Related Work

One dimension per paragraph, end with gap or positioning. A brief "In contrast, we..."
is acceptable if it clarifies the gap.

**Baseline description accuracy**: when describing what another method does, verify
against the cited paper if available; otherwise mark "Needs verification — cited
source unavailable". Knowledgeable reviewers may have authored the baseline.

## Limitations

Candid tone expected. Claims need not be contribution-forward. Flag only vague hedging
or missing concrete detail.

## Dataset/Setup

Factual and enumerative by design. Check 1 (claim-first) does not apply — focus on
completeness and clarity.

## Method

Definition → equation → interpretation ordering within each math paragraph.
Design paragraphs: motivation → mechanism → advantage. One idea per paragraph.

Hyperparameters (lr, optimizer, steps) do NOT belong here — they go in Experiments Setup.

## Experiments

Claim-first, not number-first. Ablations may open with contrastive finding.
Each experiment paragraph must state what claim it supports and how.

## Discussion

Insight-first, evidence-second. Structure: observation → mechanism → implication.
Numbers should be rare — point to sections/tables instead of re-listing data.

**Unmarked speculation**: if a sentence explains *why* a result occurs, it must be
(a) supported by evidence, (b) cited, or (c) explicitly framed as hypothesis.
Unmarked speculation after a results table is a major source of reviewer distrust.

## Conclusion

Short. Contribution → evidence → finding → punchline.
No problem restatement at S1. Lead with the insight, not the method name.

## Footnotes (all sections)

- ≤ 3 sentences. Longer footnotes should be in the main text or appendix.
- Must add new information (bibliographic detail, technical aside, dataset note).
  Never repeat a main-text argument in a footnote.
- No forward-references to specific content in later sections (light signposting OK).

## Number, Unit, and Date Formatting (all sections)

- Use % consistently (not "percent" in text and % in tables).
- Spell out one through nine in running text; use digits for 10+.
- Always use digits for years, statistics, data values, and measurements.
- Date and number ranges use an unspaced en-dash: 1840–2010, 3–5 layers
  (not hyphen, not spaced en-dash).
- Spaces around = in inline equations: $x = 5$, not $x=5$.
- Figure/table captions: sentence case, no terminal period.
- Source notes: "Author's construction" / "Author's calculations" (not
  "Calculated by the author"). Single source → "Source:", multiple → "Sources:".
