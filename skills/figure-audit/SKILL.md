---
name: figure-audit
description: "Audits the figures and tables of a compiled paper PDF for print readability, submission compliance, aesthetics, and consistency across the figure set, measuring rendered text from the PDF itself. Proactively trigger after any figure regeneration, figsize change, or plotting-script edit. Use when the user says 'audit figures', 'figure quality check', 'figure aesthetics', '检查图的质量', '图有没有问题', '图好不好看', '审美', '风格统一', 'table质量', '检查字体', '精益求精', '100% submission-ready'. Report-only. Not for generating figures (nature-figure, paper-figure), fixing them (figure-pipeline), the visual design of a standalone image (how-to-review-figure), or paragraph writing (oral-paragraph-audit)."
---

# Figure & Table Audit for Papers

> Codex calls (`codex exec`, `codex exec resume`) follow `../shared-references/codex-cli.md`.

Audit what the reviewer sees: the compiled PDF, at print size, in context. Measure what can be
measured, judge the rest against a cited principle, and label the remainder as taste. This skill
reports; `figure-pipeline` fixes.

## Audit Modes

### Quick (~5 min)
Phase 1 only: fonts, rendered text sizes, raster resolution, file size. A mid-editing spot
check. It certifies nothing about overlap, encoding or aesthetics.

### Full (30–60 min)
Phases 1–3: Checks 1–16 on every figure and table. For pre-submission.

### 精益求精 (Full + Codex)
Full, then a blind Codex review of the rendered pages and an adjudication round (Phase 4). For
when the user demands the highest bar.

### Recheck (after a repair)
Run by `figure-pipeline`, or after any manual fix. Inputs: the baseline report, the candidate PDF,
and the affected assets. Phase 1 runs on the whole candidate PDF; Phases 2–3 apply every
applicable check to each affected figure and to any figure whose placement, caption or citing
sentences changed; Check 16 covers the full set. Every other figure inherits its baseline verdicts
only when its file bytes, its script row (page, width, scale, sizes), its caption and its citing
sentences are all unchanged and the rubric hash matches. Each baseline ID gets RESOLVED, PERSISTS
or REVIEW NEEDED; new findings get new IDs. In 精益求精, Phase 4 covers the affected figures, and
the others inherit independent review only from a baseline blind review under the same rubric
hash. A Recheck by the session that made the fix is protocol-bound verification anchored on the
measurements; independence comes only from Phase 4.

## Protocol

```
0. Freeze:   audit a snapshot of the PDF, never the live file
1. Phase 1:  Measure (pdffonts, scripts/figure_text_audit.py, formats, size)
2. Phase 2:  Per-figure inspection, Checks 3–15, under the viewing protocol
3. Phase 2b: Figure-set review, Check 16, once per paper
4. Phase 3:  Verification pass: every finding re-seen, every check given a disposition
5. Phase 4:  (精益求精) blind Codex review, then adjudication
6. Report, then hand off to figure-pipeline
```

## Phase 1: Measure

0. **Freeze**: copy the PDF into a run directory and take every measurement, render, crop and
   Codex input from that copy, since a concurrent build can replace the live file mid-audit.
   Record the original path, the snapshot path and the full `sha256sum`, plus the rubric hash:
   `cat <skill-dir>/SKILL.md <skill-dir>/references/*.md <skill-dir>/scripts/figure_text_audit.py | sha256sum | cut -c1-12`.
1. **Fonts**: `pdffonts main.pdf`, and on each figure file to attribute a font (Check 1).
2. **Rendered text**:
   ```bash
   python3 <skill-dir>/scripts/figure_text_audit.py main.pdf --floor F   # add --json for crop rects
   ```
   `F` is the venue floor from `references/venues.md` (Nature 5; ML venues 7 as a heuristic).
   Needs PyMuPDF (`python3 -m pip install pymupdf`). Per figure (panels under one caption are
   grouped) it reports page, caption, files, LaTeX scale, visible width, rendered text
   min/median/max, the glyphs below the floor, text and math fonts, effective raster DPI, and
   notes (stretched, clipped, no extractable text, off page). Then the figure-set summary,
   captions without an included graphic, and below-floor text outside figures.
   - The script reads text drawn as text. A caption without an included graphic is either a text
     float (a listing or algorithm: its text is page text, so read its sizes and margins from that
     page directly) or inline TikZ/pgfplots. Inline graphics, outlined glyphs ("no extractable
     text") and text inside rasters need a visual estimate against the caption size: report those
     as REVIEW NEEDED with the estimate.
   - Without PyMuPDF, estimate scale as placed width ÷ the figure PDF's page width (`pdfinfo`) and
     mark Check 2 as estimated.
   - To diagnose a small-text failure: rendered = source × scale; author at the placed width
     (the 1:1 principle in `references/venues.md`).
3. **Formats**: `find figs/ -name "*.jpg" -o -name "*.jpeg"`; data plots belong in vector PDF.
4. **File size**: `ls -lh main.pdf` against the venue's current limit.

## Phase 2: Per-figure Inspection

Follow the viewing protocol in `references/aesthetics.md`: the page render in context, 300 dpi
crops for geometry, the squint test for salience. Judge each panel of a multi-panel figure
separately. Run Checks 7–10 on each table. For papers with more than five figures, one subagent
per page may run Phase 2 in parallel.

| # | Check | Applies to | Key signal | Defined in |
|---|-------|-----------|------------|------------|
| 1 | Font embedding | Figs | Not embedded; Type 3 where the venue rejects it | checks.md |
| 2 | Text size | Figs | Rendered glyph below the venue floor (measured) | checks.md |
| 3 | Overlap/clipping | Figs | Legend on data, cross-panel spillover, clipped labels | checks.md |
| 4 | Colour accessibility | Figs | Colour-only cues, red-green, grayscale collapse | checks.md |
| 4b| Colour semantics | Multi-element | One colour, two meanings within a figure | checks.md |
| 5 | Layout/sizing | Figs | Width mismatch, panel labels, aspect from the data | checks.md |
| 6 | Data integrity | Figs | Missing labels/units, deliberate ranges, values vs tables | checks.md |
| 7 | Caption quality | Both | Not self-contained; takeaway missing on a claim figure | checks.md |
| 8 | Table headers | Tables | Directional arrows, units, bold, precision | checks.md |
| 9 | Cross-references | Both | Unreferenced floats | checks.md |
| 10| Venue compliance | Both | Required venue rules (resolution, format, size) | checks.md, venues.md |
| 11| Anti-patterns | Figs | Inspection triggers: dynamite, dual axes, 3D, pies | checks.md |
| 12| Panel coherence | Multi-panel | No joint reading task | checks.md |
| 13| Uncertainty | Figs | Multi-seed data without intervals; undefined intervals | checks.md |
| 14| Claim-data match | Both | Text claim not visible in the figure or table | checks.md |
| 15| Aesthetic principles | Figs | A1–A7: salience, encoding, ink, space, type, colour, labels | aesthetics.md |
| 16| Figure-set coherence | Paper | Fonts, role sizes, entity mapping, quantities across figures | aesthetics.md |

Give Check 15 one disposition per principle, A1 through A7, with its evidence tag.

## Phase 2b: Figure-set Review (Check 16)

After every figure has been inspected, build the contact sheet and compare the figures as a set,
starting from the script's figure-set summary. Each finding names two or more figures and the
conflicting mapping.

## Phase 3: Verification Pass

1. **Trace-verify Check 3**: for each legend and annotation, trace every data series through
   its bounding box on the 300 dpi crop.
2. **Re-see every ISSUE**: reopen the crop and confirm the defect is where the finding says;
   move what you cannot confirm to REVIEW NEEDED.
3. **Account for coverage**: every applicable check and principle has a disposition, and every
   figure the script could not measure is listed.

The pass ends when all three hold.

## Phase 4: Codex Review (精益求精)

Give Codex what a reviewer sees, before it sees any of Claude's findings.

1. **Inputs per figure**: the in-context page render and the figure crop (PNG), its caption, the
   sentences citing it, its line from the script, and the venue.
2. **First call**: `codex exec` with `model: gpt-6-astra` and
   `config: {"model_reasoning_effort": "xhigh"}`; attach images with repeated `-i FILE` placed
   before `-o FILE`. Save the `threadId`. If the prompt points Codex at this rubric, give the
   absolute paths of this skill's files and tell it to ignore any installed copy of figure-audit
   (a Codex home can hold an older one); record the rubric hash it was given.
   ```
   You review the figures of a {venue} paper at print size. For each figure, using the attached
   page render and crop, report findings on: readability at print size, overlap and clipping,
   whether the key comparison reads quickly, salience versus the caption's claim, ink hierarchy,
   alignment and spacing, typography, colour, labels and legends, and consistency with the other
   figures. For each finding give the figure and panel, the location, what you see, why it
   matters for a reader, and a fix. Mark judgements a competent designer could decline as taste.
   Say what you could not judge from the images.
   ```
3. **Adjudicate**: `codex exec resume <threadId>` with Claude's findings. For every disagreement,
   reopen the crop. Agreed findings stand. A side may change its verdict only by naming something
   in the crop or the rubric the other missed; bare agreement does not count, since an informed,
   resumed thread drifts toward deference. Disputes still open become REVIEW NEEDED with both
   readings. A resumed exchange is adjudication, not a second blind review.
4. **Stop** when every figure's findings are adjudicated. Scores, if Codex gives them, are
   `[taste]` and never the stopping rule.
5. **Codex unavailable**: say so and deliver a single-model report labelled as such.

## Output Format

```
# Figure & Table Audit Report

Input: [original path] → snapshot [run]/main.pdf, sha256 [full] | Venue: … | Floor: F pt
Mode: Quick / Full / 精益求精 / Recheck | Rubric: figure-audit [12 hex] | Baseline: [report, for Recheck]
Independent review: Codex blind under rubric [12 hex] / none

## Summary
- Figures: N (graphic) + N text floats | Tables: N
- Blocking: N | Major: N | Minor: N | Review needed: N | Not auditable: N

## Assets
| Key | Label | Files | Page |

## Measurements (scripts/figure_text_audit.py)
| Fig | Page | Files | Scale | Width | Text pt min/med/max | < floor | Fonts |

## Figure 1 (page P): [one-sentence claim]
1–14: PASS except the IDs below / N/A: [checks]
15: A1 … A7 dispositions, each with its tag
- `hero-6-log-axis` ISSUE (Minor) [guideline: source]: what, where, why → fix
- `hero-A1-salience` REVIEW NEEDED: what would settle it
...

## Table 1 (page P)
7–10, 14: ...

## Figure Set (Check 16)
| ID | Property | Status | Figures involved | Evidence |

## Dispositions (Recheck only)
| ID | Baseline | Now | Evidence |

## Coverage
- Not measured by the script: [figures and why]
- Newly observed: [figures] | Inherited from baseline: [figures]
- Codex review: [done / affected figures only / unavailable]
```

**Finding IDs**: `<asset>-<check>-<slug>`, where asset is the float's `\label` without its prefix
(`fig:hero` → `hero`), else the graphic's file stem, else `figN`/`tabN`; `set` for a figure-set
finding, which lists its figures. Check is 1–14, 3a–3d, A1–A7 or 16. One defect gets one ID even
when it cites several checks, and keeps it for life: a Recheck reuses baseline IDs and mints new
ones only for new findings. `figure-pipeline` selects and tracks findings by these IDs.

**Status**: PASS, ISSUE, REVIEW NEEDED, NOT AUDITABLE (evidence missing), N/A.

**Severity** (for ISSUE):
- **Blocking**: a verified breach of an applicable venue requirement, or a substantiated
  correctness failure (wrong data, misrepresentation, broken reference).
- **Major**: at print size the reader misreads, cannot read, or must work noticeably harder.
- **Minor**: polish. `[taste]` findings stay Minor.

## After the Audit: Handoff

1. BLOCKING or MAJOR findings: suggest `/figure-pipeline`, which takes this report as its issue
   list and fixes them.
2. Only MINOR: list the findings with their recipes (`figure-pipeline/references/repair-recipes.md`)
   and let the user choose which to fix.
3. After any fix: Recheck, since fixes reflow pages and shrink fonts.

Present findings and leave the plotting scripts untouched; the user decides.

## Audit Discipline

- **Measure before judging**: run the script before reading a single figure, so a size verdict
  rests on a number.
- **Cite the principle**: every Check 15–16 finding carries its tag and source; taste is labelled
  taste.
- **Uncertainty is a status**: when unsure, report REVIEW NEEDED with what would settle it. A
  missed overlap reaches reviewers; an unlabelled guess costs the author a wasted fix.
- **Cross-panel and cross-figure checks are mandatory** wherever they apply.

## Reference Files

- `references/checks.md`: Checks 1–14 in detail, and the status vocabulary
- `references/aesthetics.md`: Checks 15–16, evidence tags, viewing protocol, contested points
- `references/venues.md`: widths, floors, fonts, resolution and size limits, each with source and
  strength
- `references/pitfalls.md`: defects that passed earlier audits, and how to catch them
- `scripts/figure_text_audit.py`: rendered text, scale, fonts and raster DPI per figure
- `scripts/test_figure_text_audit.py`: regression test with LaTeX fixtures; run it after editing the script
