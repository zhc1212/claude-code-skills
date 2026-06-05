---
name: figure-audit
description: "Use when reviewing a compiled paper PDF for figure/table readability, print quality, or submission compliance — overlapping legends, tiny labels after scaling, Type 3 font warnings, clipped annotations, missing error bars, stale data, orphan floats, or caption/table-header issues. Proactively trigger after ANY figure regeneration, figsize change, or plotting script edit — print-scale issues are invisible until audited. Also use when user says '检查图的质量', 'audit figures', 'figure quality check', '检查字体', '图有没有问题', 'table质量', '精益求精', '100% submission-ready', 'print quality'. Not for generating figures (use nature-figure), fixing figures (use figure-pipeline), or paragraph-level writing (use oral-paragraph-audit)."
---

# Figure & Table Audit for Conference Papers

Systematic quality audit for all figures and tables in a compiled paper. Checks the final PDF output — not the source code — because what matters is what the reviewer sees.

## When to Use

- Paper is near-final, all figures and tables placed
- Before uploading PDF to OpenReview/ARR/CMT
- After changing figure sizes, fonts, or layouts
- After regenerating ANY figure (even one) — reflow can break other figures
- When a collaborator asks "图有没有问题"

## Audit Modes

**Quick audit** (5 min): Phase 1 + Phase 1.5 only. Run `pdffonts`, compute scale factors, flag any figure with scale < 0.7. Good for mid-editing spot checks.

**Full audit** (30-60 min): All phases, all 14 checks. For pre-submission.

**精益求精 audit**: Full audit + Codex cross-review (see Optional section). For when the user demands 100% satisfaction. Target score ≥ 9.0/10 from GPT-5.5.

## How to Run

### Phase 1: Programmatic Pre-checks (automated, before visual inspection)

Run these scripts/commands first — they catch issues faster and more reliably than visual inspection:

1. **`pdffonts main.pdf`** — catches Type 3 fonts globally
2. **Figure file format scan**: `find figs/ -name "*.jpg" -o -name "*.jpeg"` — JPEG data plots should be PDF/PNG
3. **PDF file size**: `ls -lh main.pdf` — flag if >50MB (OpenReview/ARR limit)
4. **Raster resolution check**: for any PNG/TIFF figures, verify ≥300 DPI with `identify -verbose <file> | grep Resolution` (ImageMagick)

### Phase 1.5: Scale Factor Audit (mandatory, before visual inspection)

**This is the single most impactful check.** Most print-readability failures come from large-figsize figures scaled down by LaTeX.

For each figure:
1. Find the source `figsize` in the plotting script (e.g., `figsize=(14, 5)`)
2. Find the LaTeX inclusion width: `\linewidth` (~5.5" NeurIPS/ICLR single-col, ~3.3" two-col), `\textwidth` (same as linewidth for single-col)
3. Compute **scale factor** = `latex_width / figsize_width`
4. Flag any figure with scale factor < 0.7 as **MAJOR** — fonts will shrink >30%

**Automated extraction** (run this one-liner to get all figsize values):
```bash
grep -rn "figsize" paper/*/scripts/*.py | grep -oP 'figsize=\(\K[^)]+' | while read dims; do
  w=$(echo $dims | cut -d, -f1 | tr -d ' '); echo "width=${w}\" → scale=$(echo "5.5/$w" | bc -l | head -c5)";
done
```

**Venue width reference:**

| Venue | \linewidth | \columnwidth (2-col) |
|-------|-----------|---------------------|
| NeurIPS / ICLR (single-col) | 5.50" | — |
| ACL / EMNLP (2-col) | 7.00" | 3.25" |
| Nature (2-col) | 7.09" | 3.50" |
| IEEE (2-col) | 7.00" | 3.50" |

**The 1:1 principle (best practice):** Set `figsize` to match the output width. A `figsize=(5.5, 2.5)` figure included at `\linewidth=5.5"` prints at 1:1 — source font sizes ARE the print sizes. This eliminates the entire class of font-shrinking bugs.

| figsize width | NeurIPS scale | Effective 8pt → | Verdict |
|--------------|---------------|-----------------|---------|
| 5.5" | 1.00 | 8.0pt | Ideal |
| 7.0" | 0.79 | 6.3pt | OK |
| 10.0" | 0.55 | 4.4pt | MAJOR |
| 14.0" | 0.39 | 3.1pt | BLOCKING |

**Fix:** Either reduce `figsize` to ≤ venue linewidth, or proportionally increase all font sizes so `source_pt × scale ≥ 7pt`.

### Phase 2: Visual Inspection (per-figure, using Read tool on figure PDFs)

For each figure:
1. **Read the individual figure PDF** with the Read tool — not just the compiled paper page. This gives higher resolution for spotting overlap.
2. **Multi-panel decomposition**: for multi-panel figures, evaluate EACH panel independently. Don't just glance at the whole figure — trace every element in every panel.
3. Run the checks below on each figure; run checks 7-10 on each table.

### Phase 3: Two-Pass Verification (mandatory)

After fixing any issues found in Phase 2:
1. **Re-read every modified figure PDF** — not just the ones you changed. Fixes can introduce new issues (e.g., moving a legend may now overlap a different element).
2. **Trace-verify Check 3** (overlap): for each legend and annotation, mentally trace every data series/curve/bar through the label's bounding box. If you can't confidently say "no data passes through this region," flag it.
3. Never claim "PASS" or "100% confidence" without completing this second pass.

For papers with many figures (>5), launch parallel subagents — one per page.

## Relationship to Other Skills

- **`paper-presubmit-audit`** does a quick 1-line-per-figure scan across 13 checks. This skill goes deeper per figure.
- **`nature-figure`** generates figures. This skill audits existing ones.
- **`oral-paragraph-audit`** audits text. This skill audits visual elements.

Run `figure-audit` when you want a thorough visual quality pass; run `paper-presubmit-audit` when you want a fast full-paper sweep.

## The 14 Checks

### 1. Font Embedding and Type

Run `pdffonts main.pdf` and verify:
- **Zero Type 3 bitmap fonts** — these look blurry in print and cause desk rejection at some venues
- **All fonts embedded** — no "not embedded" in the output
- **Font family**: sans-serif (Arial/Helvetica) for data figures is the community standard. Serif (Times) is acceptable for text-heavy diagrams if it matches the paper body
- **TrueType 42 only**: Nature requires TrueType 2 or 42; most CS venues accept any embedded font

**Fixes by tool:**

| Tool | Fix |
|------|-----|
| matplotlib | `plt.rcParams['pdf.fonttype'] = 42` |
| Tikz/PGF | Already vector; no Type 3 risk |
| PPT/Keynote | Export as PDF/SVG; avoid EMF |
| Inkscape | File → Document Properties → ensure fonts embedded |
| R/ggplot2 | `ggsave(..., device = cairo_pdf)` |

### 2. Text Size Verification

This is a concrete, measurable check — not a subjective impression.

**Venue-specific minimums** (after LaTeX scaling to final PDF size):

| Venue | Minimum | Recommended | Panel labels |
|-------|---------|-------------|-------------|
| Nature family | 5 pt | 5-7 pt | 8 pt bold lowercase |
| NeurIPS/ICML/ICLR | 7 pt | 8-9 pt | — |
| ACL/EMNLP | 7 pt | 8-9 pt | — |
| General rule | 6 pt | 8 pt | Match caption size |

**How to verify**: the actual rendered size depends on both the source figure's font size and the LaTeX scaling factor. A 12pt label in a 10-inch-wide matplotlib figure scaled to `\columnwidth` (3.3 inches) becomes ~4pt — below minimum.

Formula: `rendered_pt = source_pt × (latex_width / source_width)`

Check these elements in every figure:
- Axis labels
- Tick labels (often the smallest text — most common failure)
- Legend text
- Annotation text
- Panel labels (a), (b), (c)

Flag as **MAJOR** if any text is below venue minimum. Flag as **MINOR** if text is legible but noticeably smaller than caption text.

### 3. Text Overlap and Clipping

This is the most commonly mis-judged check. Do NOT eyeball and guess — systematically verify each sub-item. When in doubt, flag it; false positives are cheap, missed overlaps go to reviewers.

For each figure in the PDF:
- **No text-on-text overlap**: axis labels not clipping tick labels, legend not overlapping data points, annotation arrows not crossing text
- **No clipped text**: labels not cut off at figure edges (missing `tight_layout()`)
- **Contrast**: text readable against its background (no light gray text on white, no dark text on dark fill)

**3a. Legend-on-data overlap** (most frequent failure):
- Legends at `upper right`, `upper left`, `lower left` etc. are inside the axes — they WILL overlap with data unless the data is absent in that region. Do not assume white `facecolor` makes overlap acceptable; it still occludes the data the reader needs to see.
- For line/trajectory plots: trace each curve through the legend's bounding box region. If ANY curve passes through where the legend sits, flag as MAJOR.
- For spaghetti/band plots: legends inside axes almost always overlap. Prefer `bbox_to_anchor` outside the axes or in an empty adjacent panel.
- Safe placements: below x-axis (`bbox_to_anchor=(0.5, -0.2)`), empty subplot panel, or `fig.legend()` outside all axes.

**3b. Cross-panel label spillover** (multi-panel figures):
- When `wspace`/`hspace` is small, labels/annotations near the edge of one panel can visually intrude into the adjacent panel's axis area.
- Check: for each annotation label, is any part of the text closer to the neighboring panel's axis spine than to the data point it annotates? If yes, flag as MAJOR.
- Common trigger: dumbbell/dot plots with outlier data points far from the cluster — the label extends beyond the panel's visual boundary.

**3c. Label-axis boundary clipping**:
- Data points near axis min/max create labels that clip against the spine or extend outside `bbox_inches='tight'`.
- Check each annotation: is the anchor point within the inner 80% of the axis range? If not, verify the label doesn't clip.
- Fix: use conditional placement (move label to opposite side for boundary points), or add `ax.margins()` padding.

**3d. In-element annotations**:
- Text placed inside bars, pie slices, or filled regions must have sufficient contrast AND not overlap with the element's edges or neighboring elements.
- If the bar/slice is too small to contain the label without touching edges, move the label outside with an arrow or remove it entirely.

### 4. Color Accessibility and Print Robustness

Reviewers with color vision deficiency (8% of men) should be able to distinguish all data series. Figures may also be printed in B&W.
- **Grayscale test**: if two data series become indistinguishable in B&W, the figure needs line style variation (solid/dashed/dotted) or marker shape variation. This is not optional — reviewers print papers.
- **Colorblind-safe palette**: avoid pure red-green distinctions. Safe defaults: Okabe-Ito, Paul Tol, or [matplotlib's tableau palette](https://matplotlib.org/stable/gallery/color/named_colors.html)
- **No rainbow/jet colormaps** for sequential data — use viridis, plasma, or single-hue gradients
- **No background gridlines, drop shadows, or patterns** — Nature explicitly prohibits these

### 4b. Color Semantic Consistency (multi-element figures)

When a single figure uses color for DIFFERENT encodings in different panels or elements, the caption MUST explicitly distinguish them. This is a frequent source of reviewer confusion.

Common failure: a heatmap panel uses a diverging colormap (red = positive, blue = negative) while an adjacent marginal bar chart colors bars by category (red = type A, blue = type B). The reader sees "red" and "blue" and assumes the same encoding — but they're different.

**Check:**
1. List every color encoding in the figure (what does each color MEAN?)
2. If any color appears with two different meanings, verify the caption explains both
3. Flag as **MAJOR** if the caption doesn't distinguish, or if the dual encoding is genuinely confusing

**Good example (from real fix):** "Heatmap color encodes signed Δr (red = increase, blue = decrease). Right marginal bars are colored by module family (red = attention, blue = MLP); bar direction encodes the sign."

### 5. Layout and Sizing

- **Width matches float type**: `\columnwidth` figures use `figure`, `\textwidth` figures use `figure*`. Mismatch = wasted space or unreadable text
- **Panel labels**: multi-panel figures have (a), (b), (c) matching the caption. Labels are bold, consistent position (top-left is standard)
- **Aspect ratio**: 4:3 or 16:9 for data plots unless data demands otherwise
- **White space**: no excessive margins (matplotlib: `tight_layout()` or `bbox_inches='tight'`)
- **Spine cleanup**: remove top/right spines for cleaner data plots (community best practice from [matplotlib_for_papers](https://github.com/jbmouret/matplotlib_for_papers))

### 6. Data Integrity

- **Axis labels present**: every axis has a label with units in parentheses where applicable
- **Axis ranges reasonable**: no misleading truncated axes unless explicitly noted (broken axis notation)
- **Legend complete**: every data series in the plot appears in the legend
- **No stale/wrong data**: spot-check 2-3 data points against the corresponding table values in the paper. If a caption says "PPL drops from 42.1 to 11.4" but the figure shows different values, flag as BLOCKING

### 7. Caption Quality

For every figure AND table caption:
- **Self-contained**: can a reader understand it without the main text?
- **Ends with takeaway**: the last sentence states what the reader should conclude, not just describe what's shown
- **Numbers match**: any numbers quoted in the caption match the visual data
- **Panel descriptions match panels**: if caption mentions "(a)" and "(b)", they exist and are labeled
- **Abbreviations defined**: if caption uses abbreviations not yet defined in the paper, flag

### 8. Table Header Quality

For every table:
- **Direction arrows**: columns where "higher is better" or "lower is better" have ↑ or ↓ in the header
- **Units in headers**: every numerical column has units (M, GB, ms, tok/s, %) either in header or caption
- **Arrow consistency**: if some tables have arrows and others don't, flag as MAJOR
- **Bold consistency**: best value per metric per group is bolded; verify bolding is correct
- **Task set documentation**: if different tables report "Avg." over different task sets, each caption must state which tasks are included
- **Decimal precision**: consistent within each column (not 11.4 next to 11.95)

### 9. Cross-Reference Consistency

- **Every figure and table is referenced** in the text via `\ref{}` at least once
- **Every algorithm is referenced** — orphan Algorithm boxes are a common oversight
- **Reference appears before or near the float**: a Figure 5 referenced only in the Appendix but placed on page 4 is misplaced
- **No orphan floats**: figures/tables that exist in the PDF but are never referenced in text

### 10. Venue Compliance

- **No title inside figure**: the caption serves as the title (some venues explicitly prohibit in-figure titles)
- **Resolution**: raster images at ≥300 DPI (≥450 DPI for Nature); vector preferred for all data plots
- **File format**: PDF or EPS for vector; TIFF or PNG for raster. Avoid JPEG for data plots (lossy compression creates artifacts)
- **File size**: total PDF under venue limit (typically 50MB for ARR/OpenReview)
- **Color mode**: RGB for submission (Nature auto-converts to CMYK for print)
- **No outline text**: Nature specifically requires fonts not be converted to outlines

### 11. Visualization Anti-patterns

Flag these known bad practices — reviewers notice them even if they can't articulate why:

- **Dynamite plots** (bar + error bar for continuous data): use dot plots, violin plots, or box plots instead — bars hide the distribution
- **Rainbow/jet colormaps** for sequential data: use perceptually uniform colormaps (viridis, plasma, cividis)
- **Overplotted scatterplots**: if >1000 points overlap into a solid blob, use density plots, hex bins, or alpha blending
- **Dual-axis plots without clear visual separation**: if two y-axes share the x-axis, ensure colors are maximally distinct and each axis label matches its series color
- **3D plots for 2D data**: 3D bar charts, 3D pie charts — these distort perception. Use flat versions
- **Pie charts with >5 slices**: consider horizontal bar chart instead
- **Truncated y-axis without notation**: if y-axis doesn't start at 0 and this could mislead, flag unless broken-axis notation is used

### 12. Panel Design Coherence (multi-panel figures only)

Do the panels belong in the same figure? Panels should pass at least 2 of these 4 tests:

1. **Shared axis** — panels share x or y variable for direct comparison
2. **Causal/temporal link** — one panel explains WHY the other looks that way
3. **Zoom relationship** — detail vs aggregate of the same data
4. **Synthesis requirement** — reader MUST see both to reach the conclusion

Flag MAJOR if panels share no axis, no causal link, and each is self-contained. Flag MINOR if related but loosely coupled.

### 13. Uncertainty Representation

Data-driven — don't blindly require error bars. Check whether the data supports them:
- If the paper reports multi-seed results (look for ± in tables, "n=", "seeds"), the figure should show uncertainty (error bars, bands, or seed lines)
- If only single-seed, don't flag — that's an experimental design issue, not a figure issue
- When present: meaning must be stated (SD, SE, 95% CI, min-max)
- Spot-check error bar extents against reported ± values

### 14. Claim-Data Consistency

- Text says "A outperforms B" → verify A is visually better in figure AND bolded in table
- Text says "best" → verify bolding is correct across ALL entries in the group
- Caption quotes a number → verify it matches the plotted value
- Method naming consistent across all figures/tables/text (don't mix "DynRank" / "Dynamic Rank")

## Output Format

```
# Figure & Table Audit Report

## Summary
- Figures audited: N
- Tables audited: N
- Blocking issues: N
- Major issues: N
- Minor issues: N

## Scale Factor Summary
| Figure | figsize | Scale | Effective 8pt → | Verdict |
|--------|---------|-------|-----------------|---------|
| Fig 1  | (10, 4) | 0.55  | 4.4pt           | MAJOR   |
| Fig 2  | (5.5,2) | 1.00  | 8.0pt           | OK      |
| ...    |         |       |                 |         |

## Figure 1 (page P): [description]
Scale:     [figsize → scale factor → effective minimum pt]
1. Fonts:      [PASS / BLOCKING: Type 3 found in ...]
2. Text size:  [PASS / MAJOR: tick labels ~Xpt, below 7pt minimum]
3. Overlap:    [PASS / MAJOR: legend overlaps data at ...]
4. Color:      [PASS / MINOR: red-green distinction in ...]
4b. Semantics: [PASS / MAJOR: dual color encoding not explained in caption]
5. Layout:     [PASS / MAJOR: ...]
6. Data:       [PASS / BLOCKING: caption says X, figure shows Y]
7. Caption:    [PASS / MAJOR: no takeaway]
8. Table hdr:  [skipped — figure]
9. Cross-ref:  [PASS / MAJOR: never referenced in text]
10. Compliance: [PASS / MINOR: ...]
11. Anti-pat:  [PASS / MINOR: dual y-axis without color separation]
12. Coherence: [PASS / MINOR: panels loosely coupled]
13. Uncert.:   [PASS — single seed, no error bars expected]
14. Claims:    [PASS / BLOCKING: text says A>B but figure shows B>A]

## Table 1 (page P): [description]
7. Caption:    [PASS / MAJOR: ...]
8. Table hdr:  [PASS / MAJOR: missing ↓ on PPL column]
9. Cross-ref:  [PASS]
10. Compliance: [PASS]
14. Claims:    [PASS / BLOCKING: bold on wrong entry]

## Figure 2 (page P): [description]
...
```

Severity labels:
- **Blocking**: will cause desk rejection or visible error (Type 3 fonts, wrong data, orphan float)
- **Major**: noticeably unprofessional (text overlap, text below minimum size, missing units, no takeaway in caption)
- **Minor**: cosmetic (slightly small text, suboptimal color, missing tight_layout, rainbow colormap)

## Common Fixes (Quick Reference)

| Problem | Fix |
|---------|-----|
| Type 3 fonts (matplotlib) | `plt.rcParams['pdf.fonttype'] = 42` |
| Type 3 fonts (R) | `ggsave(..., device = cairo_pdf)` |
| **Text too small (most common)** | **Best: set `figsize=(5.5, h)` for NeurIPS linewidth, keep fonts at 7-9pt.** Alternative: `rendered_pt = source_pt × (latex_width / source_width)` — increase source font until rendered ≥ 7pt |
| Text overlap | `plt.tight_layout(pad=...)` or manual `bbox_to_anchor` for legend |
| Legend on spaghetti plot | Move outside axes: `bbox_to_anchor=(0.5, -0.15)` or use empty adjacent panel |
| Stacked panel legend overlap | Move bottom-panel legend to upper area: `bbox_to_anchor=(0.98, 0.72)` |
| Red-green only | Add `linestyle='--'` for second series, or use Okabe-Ito palette |
| Dual color encoding in caption | Explicitly state what each color means in each panel/element |
| No takeaway in caption | Add one sentence: "[Key finding this figure demonstrates]" |
| Orphan float | Add `Figure~\ref{fig:X}` or `Table~\ref{tab:X}` in the relevant paragraph |
| Missing panel labels | `ax.text(-0.1, 1.05, '(a)', transform=ax.transAxes, fontweight='bold')` |
| Table missing ↑/↓ | Add `$\uparrow$` or `$\downarrow$` to column headers |
| Inconsistent bold | Verify best-per-group is bolded; check across all ratio/model groups |
| Dense horizontal bars (>20 bars) | Increase `height` param, remove `edgecolor`, or aggregate into groups |
| Page reflow after resize | Recompile 2 passes, check page count, verify no floats shifted to wrong page |

## Known Anti-patterns (from real audits)

These are failure modes that passed initial audit but were caught by human review. Treat each as a mandatory check.

| Anti-pattern | Why it's missed | How to catch |
|-------------|----------------|-------------|
| **figsize(14,7) at \linewidth** | Looks great in standalone PNG, terrible in PDF | Phase 1.5 scale factor audit catches this before visual inspection |
| Legend at `upper right` on trajectory plot | White facecolor looks "clean" in isolation | Trace every curve through the legend bbox region |
| `loc='upper center'` on spaghetti plot | Assumes top of axes is empty | Spaghetti extends everywhere; only outside-axes placement is safe |
| Legend in bottom panel of stacked figure | Placed near curves on dual-axis panels | τ/schedule/migration curves pass through the legend area at step 600-900 |
| Annotation near axis min on dumbbell plot | Label looks fine in the panel that contains it | Check: does the label extend past the axis spine toward adjacent panel? |
| "mig X%" inside bar chart bars | Seems informative | If label font is >50% of bar height, it occludes the bar; remove or move outside |
| 32-layer horizontal bar at \linewidth | Each bar looks fine in full-res PNG | At print scale, each bar is <0.07" tall — barely visible |
| Heatmap + marginal bar using same colors for different encodings | Colors seem consistent | List all color encodings; verify caption explains each one |
| Claiming "100% confidence" after single visual pass | Overconfidence after fixing N-1 issues | Re-read every figure PDF after ALL fixes; never claim confidence without second pass |
| Fixing overlap by shrinking font | Makes text unreadable (<7pt after LaTeX scaling) | Always verify rendered size post-fix: `rendered_pt = source_pt × (latex_width / source_width)` |
| Resizing one figure causes page reflow | Smaller figure → text moves → different float placement → extra page | Always recompile and check page count after figure changes |

## Optional: Cross-Model Review via Codex

For 精益求精 quality, send figure descriptions to GPT-5.5 via Codex MCP for an independent review. GPT catches issues that visual inspection misses (semantic inconsistencies, information density, print-scale readability predictions from descriptions alone).

**When to use:** when the user asks for "100% submission-ready" or "精益求精", or when the figure count is >6.

**Prompt template** (adapt per paper):
```
You are a NeurIPS/ICLR figure quality reviewer. Score each figure 1-10 for publication quality.
For each figure I describe: content, font sizes, figsize, scale factor at \linewidth.

[Fig N: description with fonts, figsize, scale factor, panel count]

Review criteria per figure:
1. Will ALL text be readable when printed at venue column/page width?
2. Any legend overlapping with data or axis labels?
3. Color-blind accessible? Sufficient contrast?
4. Consistent styling across figures?
5. Information density: cluttered or sparse?
6. Missing labels, units, or panel indicators?

Score each 1-10, then overall. For each weakness, specify EXACT fix.
```

**Iteration protocol:**
1. Round 1: describe all figures → get scores and issues
2. Fix scale-factor issues first (biggest impact, fixes multiple figures at once)
3. Round 2: re-describe fixed figures → get new scores
4. Round 3+: fix remaining issues → re-score
5. **Stop when:** overall ≥ 9.0 AND no figure below 8.0, OR max 4 rounds reached

**Typical progression:** 7.5-8.0 (Round 1) → 8.0-8.5 (Round 2, scale fixes) → 8.5-9.0 (Round 3, remaining fixes) → 9.0+ (Round 4, polish).

**Key insight from experience:** GPT can predict print-scale readability from figsize + font size descriptions alone — you don't need to send images. Describe the numbers, let GPT do the math.

## Audit Discipline

- **Two-pass rule**: after fixing figures, re-read every figure PDF a second time. The first pass finds obvious issues; the second pass catches issues introduced by fixes (e.g., moved legend now overlaps something else).
- **Never claim PASS on Check 3 without tracing**: for each legend/annotation, mentally trace all data series through the label's bounding box. If you can't confidently say "no data passes through this region," flag it.
- **Cross-panel check is mandatory for multi-panel figures**: always verify labels/annotations near panel edges.

Sources:
- [Nature figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
- [matplotlib_for_papers](https://github.com/jbmouret/matplotlib_for_papers)
- [NeurIPS 2026 formatting](https://neurips.cc/Conferences/2026/MainTrackHandbook)
