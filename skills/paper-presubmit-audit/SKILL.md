---
name: paper-presubmit-audit
description: Use for final pre-submission audit of ML/NLP conference papers (EMNLP, NeurIPS, ICML, ACL, ICLR). Trigger when the user says "pre-submission check", "final check before submission", "submission-ready", "投稿前检查", or when the paper is near-final and needs a comprehensive quality pass. Runs 14 checks covering compilation, page count, section ordering, float layout, anonymization, symbols, acronyms, cross-references, captions, figures, number precision, hyphenation, terminology consistency, and content red-line logic check. Do not use for paragraph-level writing quality (use oral-paragraph-audit) or figure generation (use nature-figure).
---

# Paper Pre-Submission Audit

Comprehensive pre-submission checklist for ML/NLP conference papers. Run once when the paper is near-final — catches issues that paragraph-level editing misses.

## When to Use

- Paper is drafted and polished, ready for submission
- After all content edits are done, before uploading to OpenReview/ARR/CMT
- When the user asks for a "final check" or "submission-ready" audit

## How to Run

Launch **parallel subagents** for all 14 checks simultaneously — they are independent. Each reads main.tex and/or references.bib. Aggregate results into a single report.

## The 14 Checks

### 1. Compilation and Page Count

Run `latexmk -pdf` and verify:
- **Zero errors** in compilation
- **Zero undefined references** (`grep 'undefined' main.log`)
- **Main body ≤ venue page limit** (EMNLP: 8 pages; NeurIPS: 9; ICML: 8). Limitations, References, and Appendix do not count. Check by reading the PDF and finding which page Conclusion ends on.
- **Conclusion fits on last allowed page** — if even one line overflows, flag as BLOCKING
- **Zero overfull hbox warnings** wider than 1pt (check `main.log`)

### 2. Section Ordering

Verify venue-standard section order:
- EMNLP/ACL: ... → Conclusion → Limitations* → Acknowledgments* → References → Appendix (Limitations is `\section*{}`, unnumbered, does not count toward page limit)
- NeurIPS/ICML: ... → Conclusion → References → Appendix (Broader Impact may be required)

### 3. Float Layout

Check that every table and figure appears on the same page (or facing page) as the text that first references it:
- Move `table*`/`figure*` earlier in the source so LaTeX floats it to the right page
- Verify `figure` vs `figure*` matches the actual figure width
- **Algorithm references**: every `\begin{algorithm}` should be cited via `Algorithm~\ref{alg:...}` somewhere in the text

### 4. Anonymization (Double-Blind)

Verify the paper does not reveal author identity:
- Author line says "Anonymous Authors" (not real names)
- No GitHub/HuggingFace URLs, model repo links, or code release URLs
- No self-citations with "we" or "our" referring to prior work
- No file paths, machine usernames, or institutional references
- Acknowledgments commented out or suppressed

### 5. Symbol Definitions

Every math symbol must be defined at or before its first use in the body (abstract definitions do not carry over):
- Greek letters (ρ, τ, λ, σ) — each needs an inline explanation at first use
- Matrix/vector notation (W, A, B, d, n, r) — dimensions stated
- Custom notation (f_ℓ, h^orig, h^comp) — defined with "let" or equivalent
- Operator names (\argmin, etc.) — standard ones are OK, custom ones need definition

Flag any symbol used before definition, or used without ever being defined.

### 6. Acronym Definitions

Every abbreviation must be expanded at first use in the body (abstract is a separate document):
- Technical: SVD, MLP, OOD, MSE, KL, LM, etc.
- Dataset: PTB (Penn Treebank), C4, etc.
- Method-specific: CF, SI, LA, etc.

Check: grep all uppercase 2-5 letter sequences, verify each has a parenthetical expansion before or at first body use.

### 7. Cross-Reference Correctness

- Every `\ref{}` resolves (no "??" in compiled output)
- Every `\cite{}` has a matching bib entry
- Text claims match cited tables/figures (e.g., "listed in Table 1" → verify the item is actually in Table 1)
- Section references point to correct sections
- No orphan bib entries (defined but never cited)
- Every `\begin{algorithm}`, `\begin{table}`, `\begin{figure}` is referenced at least once

### 8. Caption Quality

For every table and figure caption:
- **Self-contained**: can a reader understand it without the main text?
- **Ends with takeaway**: the last sentence states what the reader should conclude from the figure/table, not just what it shows
- **Key symbols defined**: if caption uses ρ, L1/L2/L3, or abbreviations, are they explained?
- **Ends with period**: every caption must end with punctuation
- **Consistent style**: all captions use sentence case (not title case)

### 9. Table Header Quality

For every table:
- **Direction arrows**: columns with "better = higher" or "better = lower" should have ↑ or ↓
- **Units in headers**: every numerical column should have units (M, GB, ms, tok/s, %) either in the header or caption
- **Arrow consistency**: if some tables have arrows and others don't, flag
- **Task set differences**: if different tables report "Avg." over different task sets, each caption must state which tasks are included

### 10. Figure Print Quality

For every included PDF figure:
- **Fonts**: all embedded, no Type 3 bitmap fonts (run `pdffonts`)
- **Font size**: minimum ≥7pt after LaTeX scaling
- **Overlaps**: text annotations not crossing data lines
- **Width match**: `figure` uses `\columnwidth`, `figure*` uses `\textwidth`

### 11. Number Precision

For every table:
- Decimal places consistent within each column (not 11.4 next to 11.95)
- Percentage format consistent (all "XX.X%" or all integers)
- Bold marking consistent (best value per metric per group)
- No obviously wrong numbers (perplexity < 1, accuracy > 100)

### 12. Spelling and Hyphenation

- Hyphenation consistent: pick one form and use throughout (e.g., "per-matrix" not mixed with "per matrix")
- British/American English consistent (all "-ize" or all "-ise")
- Missing `~` before `\cite` or `\ref` (should be non-breaking space)
- No double spaces in prose

### 13. Terminology Consistency

Technical papers often use the same word (e.g., "layer") with different meanings in different contexts. This check catches terms that shift meaning across the paper.

**Procedure:**
1. Build a **term glossary** from the Method section — extract every technical term the paper defines and its meaning.
2. **Grep every occurrence** of each term and any synonyms. Common ambiguous pairs in ML: layer/block/sub-layer, module/component/projection, per-layer/per-block/per-matrix.
3. For each occurrence, classify: does it match the Method-section definition, or does it shift meaning?
4. **Cross-check against cited methods**: when describing a baseline's approach, verify the terminology matches what the cited paper actually does. Use web search if uncertain — a wrong description of a baseline method is a factual error reviewers will catch.

**Flag as MAJOR** when:
- The same term is used with two different meanings in the same paragraph
- A term describing a baseline's method contradicts what the baseline paper actually does
- An ambiguous term is used without specifying which sense is intended

**Flag as MINOR** when:
- Inconsistent hyphenation (sublayer vs sub-layer) — overlaps with Check 12

### 14. Content Red-Line

High-tolerance, full-paper scan for content-level fatal errors. This check assumes the paper has been through multiple rounds of editing and only flags issues that would confuse a reviewer or undermine credibility. Style preferences are explicitly out of scope.

**Logic contradictions across sections:**
- Statements in one section that directly contradict another (e.g., Method says "we freeze all parameters" but Experiments says "we fine-tune end-to-end")
- A claim in the Abstract/Introduction not supported anywhere in Experiments
- Numbers in Conclusion that don't match the tables (e.g., "reduces perplexity by 3×" when the actual reduction is 2×)

**Terminology drift:**
- A core concept changes name without explanation across sections (e.g., "block-level optimization" in Method becomes "layer-wise refinement" in Experiments — distinct from Check 13 which catches within-section ambiguity; this check catches cross-section drift)

**Severe grammar:**
- Sentences where meaning is genuinely ambiguous due to structural errors (not style issues)
- Missing negation that flips the meaning ("the method does recover" when context requires "does not recover")
- Dangling modifiers that attach to the wrong subject

Flag as **BLOCKING** only. If no issues found, report: "Check 14: PASS — no content-level red flags."

## Output Format

```
# Pre-Submission Audit Report

## Summary
- Checks passed: X/14
- Blocking issues: N
- Major issues: N
- Minor issues: N

## 1. Compilation & page count: [PASS / FAIL]
## 2. Section ordering: [PASS / FAIL]
## 3. Float layout: [PASS / N misplaced floats]
## 4. Anonymization: [PASS / FAIL]
## 5. Symbols: [PASS / N undefined]
## 6. Acronyms: [PASS / N undefined]
## 7. Cross-references: [PASS / N broken]
## 8. Captions: [PASS / N issues]
## 9. Table headers: [PASS / N issues]
## 10. Figures: [PASS / N issues]
## 11. Numbers: [PASS / N precision issues]
## 12. Spelling: [PASS / N inconsistencies]
## 13. Terminology: [PASS / N ambiguous terms]
## 14. Content red-line: [PASS / BLOCKING: ...]
```

Severity labels:
- **Blocking**: will cause desk rejection or reviewer complaint (Type 3 fonts, broken refs, anonymization leak, page overflow)
- **Major**: noticeably unprofessional or factually wrong (inconsistent decimals, undefined symbols, wrong baseline description)
- **Minor**: cosmetic (missing `~` before cite, minor hyphenation)

## Venue-Specific Notes

**EMNLP/ACL**: Limitations section required (unnumbered, after Conclusion, before References). Responsible NLP Research Checklist required as separate form. GPTZero policy: all bib entries scanned — unverifiable references risk desk reject.

**NeurIPS**: Paper checklist required in appendix. Broader Impact statement may be required.

**ICML**: Broader Impact statement required after Conclusion.

**All venues**: References do not count toward page limit. Appendix unlimited but reviewers not required to read it.
