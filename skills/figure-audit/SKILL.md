---
name: figure-audit
description: "Audits compiled paper PDFs for figure/table readability, print quality, and submission compliance. Proactively trigger after ANY figure regeneration, figsize change, or plotting script edit — print-scale issues are invisible until audited. Use when user says '检查图的质量', 'audit figures', 'figure quality check', '图有没有问题', 'table质量', '精益求精', '100% submission-ready', 'print quality', '检查字体'. Not for generating figures (use nature-figure), fixing figures (use figure-pipeline), or paragraph-level writing (use oral-paragraph-audit)."
---

# Figure & Table Audit for Conference Papers

Systematic quality audit for all figures and tables in a compiled paper.
Checks the final PDF output — not the source code — because what matters
is what the reviewer sees.

## When to Use

- Paper near-final, all figures and tables placed
- Before uploading PDF to OpenReview/ARR/CMT
- After changing figure sizes, fonts, or layouts
- After regenerating ANY figure — reflow can break other figures
- When a collaborator asks "图有没有问题"

## Audit Modes

### Quick (5 min)
Phase 1 + Phase 1.5 only. Run `pdffonts`, compute scale factors, flag
any figure with scale < 0.7. Good for mid-editing spot checks.
No Phase 2 visual inspection, no Phase 3 verification.

### Full (30-60 min)
All phases, all 14 checks. Phase 3 two-pass verification is mandatory.
For pre-submission.

### 精益求精 (Full + Codex)
Full audit + Codex cross-review (see Codex MCP section). Phase 3
mandatory. Target score ≥ 9.0/10 from GPT. For when the user demands
100% satisfaction.

## Protocol

```
1. Phase 1:   Programmatic pre-checks (pdffonts, format, size, DPI)
2. Phase 1.5: Scale factor audit (figsize vs LaTeX linewidth) — MOST IMPACTFUL
3. Phase 2:   Visual inspection per figure (14 checks) — Full/精益求精 only
4. Phase 3:   Two-pass verification (re-read after fixes) — Full/精益求精 only
5. Present:   Audit report with severity labels
6. Handoff:   Guide user to figure-pipeline for fixes
```

## Phase 1: Programmatic Pre-checks

Run before visual inspection — faster and more reliable:

1. **`pdffonts main.pdf`** — catches Type 3 fonts globally
2. **Figure format scan**: `find figs/ -name "*.jpg" -o -name "*.jpeg"` — JPEG data plots should be PDF/PNG
3. **PDF file size**: `ls -lh main.pdf` — flag if >50MB (OpenReview/ARR limit)
4. **Raster DPI**: for PNG/TIFF, verify ≥300 DPI with `identify -verbose <file> | grep Resolution`

## Phase 1.5: Scale Factor Audit

**The single most impactful check.** Most print-readability failures come
from large-figsize figures scaled down by LaTeX.

For each figure:
1. Find source `figsize` in the plotting script
2. Find LaTeX inclusion width (see `references/venues.md` for venue widths)
3. Compute **scale factor** = `latex_width / figsize_width`
4. Flag any figure with scale < 0.7 as **MAJOR**

**Figsize extraction** (adapt path to your project):
```bash
grep -rn "figsize" <your_figure_scripts_dir>/*.py | grep -oP 'figsize=\(\K[^)]+' | while read dims; do
  w=$(echo $dims | cut -d, -f1 | tr -d ' '); echo "width=${w}\" → scale=$(echo "5.5/$w" | bc -l | head -c5)";
done
```

**The 1:1 principle:** Set `figsize` to match output width. A `figsize=(5.5, 2.5)`
at `\linewidth=5.5"` prints at 1:1 — source font sizes ARE print sizes.

**Fix:** Either reduce `figsize` to ≤ venue linewidth, or proportionally
increase all font sizes so `source_pt × scale ≥ 7pt`.

## Phase 2: Visual Inspection (14 Checks)

For each figure, read the individual figure PDF (not just the compiled
paper page). For multi-panel figures, evaluate EACH panel independently.
Run checks 7-10 on each table.

For papers with many figures (>5), launch parallel subagents — one per page.

### Check Summary (detail in `references/checks.md`)

| # | Check | Applies to | Key signal |
|---|-------|-----------|------------|
| 1 | Font embedding | Figs | Type 3 in `pdffonts` = BLOCKING |
| 2 | Text size | Figs | `rendered_pt = source_pt × scale` < 7pt = MAJOR |
| 3 | Overlap/clipping | Figs | Legend on data, cross-panel spillover, clipped labels |
| 4 | Color accessibility | Figs | Red-green only, rainbow/jet, grayscale test |
| 4b| Color semantics | Multi-element | Same color = different meaning across panels |
| 5 | Layout/sizing | Figs | Width mismatch, missing panel labels, excess whitespace |
| 6 | Data integrity | Figs | Missing axis labels, stale/wrong data vs caption |
| 7 | Caption quality | Both | Not self-contained, no takeaway, numbers mismatch |
| 8 | Table headers | Tables | Missing ↑/↓, units, bold consistency, decimal precision |
| 9 | Cross-references | Both | Orphan floats, unreferenced figures/tables |
| 10| Venue compliance | Both | Resolution, format, file size, no in-figure title |
| 11| Anti-patterns | Figs | Dynamite plots, 3D for 2D, overplotted scatter |
| 12| Panel coherence | Multi-panel | Panels pass ≥2 of 4 relatedness tests |
| 13| Uncertainty | Figs | Multi-seed → error bars; single-seed → don't flag |
| 14| Claim-data match | Both | "A > B" in text → A visually better + bolded |

## Phase 3: Two-Pass Verification (Full/精益求精 only)

After fixing issues from Phase 2:
1. **Re-read every modified figure PDF** — not just the changed ones.
   Fixes can introduce new issues (moved legend overlaps something else).
2. **Trace-verify Check 3**: for each legend/annotation, trace all data
   series through the label's bounding box. If unsure, flag it.
3. Never claim "PASS" without completing this second pass.

## Output Format

```
# Figure & Table Audit Report

## Summary
- Figures audited: N | Tables: N
- Blocking: N | Major: N | Minor: N

## Scale Factor Summary
| Figure | figsize | Scale | Effective 8pt → | Verdict |
|--------|---------|-------|-----------------|---------|

## Figure 1 (page P): [description]
Scale: [figsize → scale → effective min pt]
1. Fonts:    [PASS / BLOCKING]
2. Text:     [PASS / MAJOR: tick labels ~Xpt]
3. Overlap:  [PASS / MAJOR: legend overlaps data at ...]
...
14. Claims:  [PASS / BLOCKING]

## Table 1 (page P): [description]
7. Caption:  [PASS / MAJOR]
8. Headers:  [PASS / MAJOR: missing ↓]
...
```

**Severity labels:**
- **Blocking**: desk rejection or visible error (Type 3, wrong data, orphan float)
- **Major**: noticeably unprofessional (overlap, text below min, missing units)
- **Minor**: cosmetic (slightly small text, rainbow colormap)

## After the Audit: Handoff

This skill finds problems; **figure-pipeline** fixes them.

After presenting the audit report:
1. If BLOCKING or MAJOR issues exist, suggest: "Run `/figure-pipeline` to
   fix these — it reads the audit report and applies fixes automatically."
2. If only MINOR issues, list the fixes inline (see `references/fixes-and-antipatterns.md`)
   and let the user decide whether to address them.
3. After ANY fix, remind the user to re-run at least a Quick audit —
   fixes can introduce new issues (reflow, font shrinkage from resizing).

Do not silently edit plotting scripts. Present findings, user decides.

## Audit Discipline

- **Two-pass rule** (Full/精益求精): after fixing, re-read every figure PDF.
  First pass finds obvious issues; second pass catches issues introduced by fixes.
- **Never claim PASS on Check 3 without tracing**: for each legend/annotation,
  trace all data series through the label's bounding box.
- **Cross-panel check is mandatory for multi-panel figures**.
- **When in doubt, flag it**: false positives are cheap, missed overlaps go to reviewers.

## Reference Files

- `references/checks.md` — detailed 14-check definitions with sub-checks
- `references/venues.md` — venue widths, font minimums, scale tables, DPI requirements
- `references/fixes-and-antipatterns.md` — common fixes + known anti-patterns from real audits

## Codex MCP (精益求精 mode)

For 精益求精 quality, send figure descriptions to GPT via Codex MCP for
independent cross-model review. GPT catches semantic inconsistencies and
predicts print-scale readability from figsize + font descriptions alone.

- **First call**: `mcp__codex__codex` with `config: {"reasoning_effort": "max"}`
- **Follow-ups**: `mcp__codex__codex-reply` with saved `threadId`
- On MCP error: tell user, proceed with Claude-only audit (single-model,
  loses cross-model blind-spot coverage)

**Prompt template** (adapt per paper):
```
You are a figure quality reviewer for {venue}. Score each figure 1-10.
For each figure: content, font sizes, figsize, scale factor at \linewidth.

[Fig N: description with fonts, figsize, scale, panel count]

Review: (1) text readable at print width? (2) legend overlaps? (3) colorblind-safe?
(4) consistent styling? (5) information density? (6) missing labels/units/panels?

Score each 1-10, then overall. For each weakness, specify EXACT fix.
```

**Iteration protocol:**
1. Round 1: describe all figures → scores + issues
2. Fix scale-factor issues first (biggest impact)
3. Round 2: re-describe → new scores
4. Stop when overall ≥ 9.0 AND no figure below 8.0, OR 4 rounds max

**Blind independence**: send raw figure descriptions only. Do NOT include
Claude's audit findings — Codex reviews independently.

Sources:
- [Nature figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
- [matplotlib_for_papers](https://github.com/jbmouret/matplotlib_for_papers)
