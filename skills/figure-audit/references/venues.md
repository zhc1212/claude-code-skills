# Venue-Specific Standards

## Page Width Reference

| Venue | \linewidth | \columnwidth (2-col) |
|-------|-----------|---------------------|
| NeurIPS / ICLR (single-col) | 5.50" | — |
| ACL / EMNLP (2-col) | 7.00" | 3.25" |
| Nature (2-col) | 7.09" | 3.50" |
| IEEE (2-col) | 7.00" | 3.50" |

## Font Size Minimums (after LaTeX scaling to final PDF)

| Venue | Minimum | Recommended | Panel labels |
|-------|---------|-------------|-------------|
| Nature family | 5 pt | 5-7 pt | 8 pt bold lowercase |
| NeurIPS/ICML/ICLR | 7 pt | 8-9 pt | — |
| ACL/EMNLP | 7 pt | 8-9 pt | — |
| General rule | 6 pt | 8 pt | Match caption size |

## Scale Factor Impact

| figsize width | NeurIPS scale | Effective 8pt → | Verdict |
|--------------|---------------|-----------------|---------|
| 5.5" | 1.00 | 8.0pt | Ideal |
| 7.0" | 0.79 | 6.3pt | OK |
| 10.0" | 0.55 | 4.4pt | MAJOR |
| 14.0" | 0.39 | 3.1pt | BLOCKING |

**The 1:1 principle:** Set `figsize` to match the output width. A `figsize=(5.5, 2.5)`
figure at `\linewidth=5.5"` prints at 1:1 — source font sizes ARE print sizes.

## Font Embedding Fixes by Tool

| Tool | Fix |
|------|-----|
| matplotlib | `plt.rcParams['pdf.fonttype'] = 42` |
| Tikz/PGF | Already vector; no Type 3 risk |
| PPT/Keynote | Export as PDF/SVG; avoid EMF |
| Inkscape | File → Document Properties → ensure fonts embedded |
| R/ggplot2 | `ggsave(..., device = cairo_pdf)` |

## Resolution Requirements

| Venue | Minimum DPI | Recommended | Notes |
|-------|------------|-------------|-------|
| Nature | 450 DPI | 600 DPI | TIFF preferred for raster |
| NeurIPS/ICML | 300 DPI | 450 DPI | Vector preferred |
| ACL/EMNLP | 300 DPI | 450 DPI | — |
| General | 300 DPI | — | — |

## File Size Limits

| Platform | Limit |
|----------|-------|
| OpenReview | 50 MB |
| ARR/Softconf | 50 MB |
| CMT | 100 MB |
| Nature submission | 30 MB per figure |
