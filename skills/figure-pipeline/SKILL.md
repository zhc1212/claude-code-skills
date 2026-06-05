---
name: figure-pipeline
description: "Use when figures have overlapping legends, clipped labels, Type 3 font warnings, text too small after LaTeX scaling, cross-panel label spillover, or any visual quality issue before paper submission. Also use when user says '修图流程', 'figure pipeline', '图审计修复', 'fix all figures', '把图都修好', 'audit and fix figures', '图有问题帮我修'. Not for generating figures from scratch (use nature-figure or paper-figure), or report-only audit without fixing (use figure-audit)."
argument-hint: "[paper-dir or main.tex path]"
---

# Figure Pipeline: Audit → Fix → Verify Loop

Closed-loop figure quality pipeline for conference papers. Finds issues, fixes plot scripts, regenerates figures, and re-verifies — iterating until clean or max rounds reached.

## When to Use

- All figures are generated and placed in the paper
- Before submission, after content is finalized
- When the user says "把图修好", "fix the figures", "figure pipeline"
- After receiving reviewer feedback about figure quality

## Pipeline Architecture

```
Stage 1: Programmatic Pre-checks (one-shot)
         │
    ┌──> Stage 2: Visual Audit (find issues)
    │         │
    │    Stage 3: Auto-Fix (edit scripts, regenerate)
    │         │
    │    Stage 4: VLM Verify (Read fixed figure PDFs)
    │         │
    │    Still issues? ──yes──┘
    │         │
    │        no
    │         │
    └── Final Report
```

**Exit states** (the loop terminates with one of these):
- **PASS**: Stage 4 returns all issues RESOLVED, no NEW issues, AND final compiled PDF re-verified
- **BLOCKED**: issue requires user judgment (venue rule ambiguity, missing raw data, design choice) — escalate with description
- **FAIL_AFTER_BUDGET**: max 2 iterations reached with unresolved issues — list remaining by severity

**Anti-oscillation**: track each issue by ID (e.g., `fig2-check3b-label-spillover`). If fixing issue A creates issue B, and fixing B recreates A, exit with BLOCKED after detecting the cycle. Don't silently loop.

**Stale asset guard**: after Stage 3 regeneration, verify the compiled PDF actually includes the new figure (check file modification timestamp vs compile timestamp).

## Stage 1: Programmatic Pre-checks

Run these commands once before visual inspection. They catch issues faster and more reliably than eyeballing.

1. **Font embedding**: `pdffonts main.pdf` — flag any Type 3 fonts (desk rejection risk)
2. **Figure format scan**: `find figs/ -name "*.jpg" -o -name "*.jpeg"` — JPEG data plots should be PDF vector
3. **PDF file size**: `ls -lh main.pdf` — flag if >50MB
4. **Raster DPI**: for PNG/TIFF figures, `identify -verbose <file> | grep Resolution` — must be >=300 DPI
5. **pdf.fonttype check**: grep plot scripts for `pdf.fonttype` — must be 42 for all matplotlib scripts

If Stage 1 finds blocking issues (Type 3 fonts, missing fonttype=42), fix them before entering the loop.

## Stage 2: Visual Audit

For each figure in the paper:

### 2a. Read the figure

Use the Read tool on the individual figure PDF file (not the compiled paper page). This gives full resolution for spotting overlap.

### 2b. Multi-panel decomposition

For multi-panel figures, evaluate EACH panel independently. Don't glance at the whole figure — trace every element in every panel.

### 2c. Run the 11-point checklist

| # | Check | What to verify |
|---|-------|---------------|
| 1 | Font embedding | Zero Type 3, all embedded, TrueType 42 |
| 2 | Text size | All text >= 7pt after LaTeX scaling. Formula: `rendered_pt = source_pt × (latex_width / source_width)` |
| 3a | Legend-data overlap | Trace every curve/bar through the legend bbox — if ANY data passes through, flag MAJOR |
| 3b | Cross-panel spillover | Labels near panel edges intruding into adjacent panel's axis area |
| 3c | Label-axis clipping | Labels anchored near axis min/max getting cut off |
| 3d | In-element annotations | Text inside bars/slices — sufficient contrast? Fits without touching edges? |
| 4 | Color + print robustness | Grayscale distinguishable? Line style/marker varies? No pure red-green? No rainbow/jet? |
| 5 | Layout & sizing | Width matches float type, panel labels present and consistent, no excessive whitespace |
| 6 | Data integrity | Axis labels with units, legend complete, spot-check 2-3 values against tables |
| 7 | Caption quality | Self-contained, ends with takeaway, numbers match, panels described |
| 8 | Table headers | Direction arrows (↑/↓), units, bold consistency, decimal precision |
| 9 | Cross-references | Every figure/table referenced in text, no orphan floats |
| 10 | Venue compliance | No in-figure title, DPI >= 300, file format appropriate |
| 11 | Anti-patterns | Dynamite plots, 3D charts, pie >5 slices, dual-axis without color separation, truncated y-axis without notation |
| 12 | Panel design coherence | Do panels belong together? See criteria below |
| 13 | Uncertainty representation | Error bars/bands present where data supports them? See criteria below |
| 14 | Claim-data consistency | Do textual claims ("best", "outperforms") match the visual/table data? |

**Check 12 — Panel Design Coherence** (multi-panel figures only):

Panels in the same figure should pass at least 2 of these 4 coherence tests:

1. **Shared axis**: panels share an independent variable (x-axis) or dependent variable (y-axis), enabling direct visual comparison
2. **Causal/temporal link**: one panel explains WHY the other looks the way it does (e.g., temperature schedule → rank movement)
3. **Zoom relationship**: one panel is a detail/aggregate of the other (e.g., representative trajectories → spaghetti overview)
4. **Synthesis requirement**: the reader MUST see both panels to reach the figure's conclusion — neither stands alone

Flag as MAJOR if:
- Panels share no axis, no causal link, and each is self-contained — they should be separate figures
- Panel (b) is essentially a different experiment that happens to use the same data source
- The caption has to make a stretch to connect the two panels ("additionally", "separately")

Flag as MINOR if:
- Panels are related but loosely — reader could understand each without the other, though co-location adds convenience

Acceptable patterns:
- Same metric, different conditions (ρ=0.4 vs ρ=0.6) ✅
- Individual vs aggregate view of same data ✅
- Main result + mechanism/explanation ✅
- Heatmap + marginal summary ✅
- Small multiples (same metric across categories) ✅

**Check 13 — Uncertainty Representation** (data-driven, not prescriptive):

Don't blindly require error bars — check whether the data supports them:
- If the paper reports multi-seed results (check tables for ±, std, n=), the corresponding figure should show uncertainty (error bars, bands, or individual seed lines)
- If only single-seed results exist, don't flag missing error bars — flag the paper's experimental design instead (outside this skill's scope)
- Error bars/bands must have their meaning stated: SD, SE, 95% CI, or min-max range
- Spot-check: do the error bar extents visually match the reported ± values in tables?

**Check 14 — Claim-Data Consistency**:

Cross-check textual claims against visual evidence:
- If text says "method A outperforms B", verify A is visually better than B in the figure AND bolded in the table
- If text says "best result", verify bolding is correct — check ALL entries in the comparison group
- If caption quotes a number, verify it matches the plotted value
- Check method naming consistency: same method should have the same name across all figures, tables, and text (e.g., don't mix "DynRank" and "Dynamic Rank")

### 2d. Produce audit report

For each figure, output:
```
Figure N (figs/filename.pdf): [1-line description]
  PASS: [list of passing checks]
  ISSUES:
    - [MAJOR/MINOR] Check 3a: legend at upper-right overlaps L15.up_proj curve at y=1800
    - [MAJOR] Check 2: tick labels ~5pt, below 7pt minimum
```

## Stage 3: Auto-Fix

For each MAJOR issue found in Stage 2:

### 3a. Locate the plot script

Find the Python/R script that generates the figure. Common patterns:
- `paper/*/scripts/plot_*.py`
- `scripts/plot_*.py`
- Check `\includegraphics` paths to trace back to source

### 3b. Apply targeted fix

Based on issue type, apply the minimal edit:

| Issue | Fix strategy |
|-------|-------------|
| Legend overlaps data | Move to `bbox_to_anchor` outside axes, empty panel, or below x-axis |
| Label clips at axis edge | Conditional placement: boundary points get opposite-side labels |
| Cross-panel spillover | Anchor labels at data midpoint, not endpoint; increase `wspace` |
| In-element text overlap | Remove redundant annotations, or move outside with arrow |
| Text too small | Increase font size in rcParams; verify with scaling formula |
| Type 3 fonts | Add `plt.rcParams['pdf.fonttype'] = 42` |
| Anti-pattern detected | Replace chart type (e.g., dynamite → dot plot) |
| Missing uncertainty | Add error bars/bands IF multi-seed data exists; state meaning in caption |
| Claim-data mismatch | Fix bold/text to match actual best values; align method names |
| Grayscale indistinguishable | Add linestyle variation (solid/dashed/dotted) or marker shape |

### 3c. Regenerate

Run the plot script to produce new PDF. Only regenerate figures with issues — don't touch passing figures.

### 3d. Recompile paper

Run `pdflatex` to incorporate the new figures. Verify page count unchanged and no new warnings.

## Stage 4: VLM Verify

This is the critical step that prevents false "PASS" claims.

### 4a. Re-read every modified figure PDF

Use Read tool on each figure PDF that was regenerated in Stage 3. Not just the ones you changed — fixes can introduce new issues.

### 4b. Trace-verify each previous finding

For each issue from Stage 2:
- **Fixed**: mark RESOLVED with evidence ("legend now at bbox_to_anchor=(0.5, -0.2), below all data")
- **Not fixed**: mark PERSISTS
- **New issue introduced**: mark NEW

### 4c. Check for fix-induced regressions

Specifically verify:
- Moving a legend didn't overlap something else
- Font size increase didn't cause text to clip
- Layout change didn't shift other elements

### 4d. Verify final compiled PDF

After verifying individual figures, recompile the paper and Read 2-3 pages of the compiled PDF where modified figures appear. LaTeX scaling, float placement, and stale cache can introduce issues invisible in individual figure PDFs.

### 4e. Decision gate

```
All issues RESOLVED + no NEW + compiled PDF verified?
  → EXIT: PASS

Oscillation detected (A→B→A cycle)?
  → EXIT: BLOCKED — describe the tradeoff, let user decide

Requires user judgment (design choice, venue ambiguity)?
  → EXIT: BLOCKED — describe the decision needed

iteration_count < 2 AND fixable issues remain?
  → CONTINUE: return to Stage 2 with updated issue list (carry issue IDs forward)

iteration_count >= 2?
  → EXIT: FAIL_AFTER_BUDGET — list unresolved issues by severity
```

## Final Report

Use this template:

```
# Figure Pipeline Report

## Summary
- Figures audited: N
- Issues found: N (M major, K minor)
- Issues fixed: N
- Iterations: N
- Status: PASS / BLOCKED / FAIL_AFTER_BUDGET

## Per-Figure Results
### Figure N (filename.pdf)
- Iteration 1: [MAJOR/MINOR] Check Xa: [specific issue description]
  → Fix: [what was changed]
  → Iteration 2: RESOLVED / PERSISTS / NEW
- Final: PASS / NEEDS_REVIEW

## Remaining Issues (if NEEDS_REVIEW)
- Figure N, Check X: [description] — could not auto-fix because [reason]
```

## Common Mistakes

| Mistake | Why it happens | Fix |
|---------|---------------|-----|
| Claiming PASS after fixing N-1 issues | Forgot to re-read the Nth figure | Stage 4 mandates re-reading ALL modified figures |
| Moving legend to `upper right` | Looks clean in isolation | Trace curves through the legend bbox first — trajectory plots have data everywhere |
| Shrinking font to fix overlap | Quick fix, creates new problem | Text below 7pt rendered = new MAJOR issue. Relocate instead of shrink. |
| Only checking the compiled PDF | Lower resolution, scaling artifacts | Read individual figure PDFs for full-resolution inspection |
| Fixing one panel, breaking another | Increased wspace shifted labels | Check adjacent panels after any layout change |
| Regenerating all figures | "Just to be safe" | Only regenerate figures with MAJOR issues — touching passing figures risks regressions |

## Integration with Other Skills

**RELATED SKILL:** `figure-audit` — report-only version (no auto-fix loop). Use when you want an audit report without modifications.

| Skill | Relationship |
|-------|-------------|
| `figure-audit` | Stage 2 is a superset of figure-audit's checks. Use figure-audit for report-only; use figure-pipeline when you also want auto-fix. |
| `nature-figure` / `paper-figure` | Upstream — these generate figures. figure-pipeline quality-checks them after generation. |
| `paper-presubmit-audit` | Parallel — presubmit covers 14 whole-paper checks including anonymization, page count, etc. figure-pipeline goes deeper on figures specifically. |
| `paper-compile` | Called within Stage 3d to recompile after figure regeneration. |

## Gotchas

- **Don't touch figures that PASS.** Only regenerate figures with MAJOR issues. Regenerating a passing figure risks introducing new problems.
- **Verify rendered size, not source size.** A 12pt label in a 10-inch figure scaled to `\columnwidth` (3.3in) becomes ~4pt. Always compute: `rendered_pt = source_pt × (latex_width / source_width)`.
- **Legend placement safe zones differ by chart type.** Line/trajectory plots have data everywhere — only outside-axes placement is safe. Bar charts often have empty vertical space above bars. Heatmaps have no safe interior zone.
- **Two-pass is not optional.** The most common audit failure (from real experience) is claiming PASS after fixing N-1 issues without re-checking the Nth figure. The fix-induced regression is real.
