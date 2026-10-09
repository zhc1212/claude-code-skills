# Venue Standards

Every row names its source, the date it was checked, and its strength: **required** (the venue
rejects or asks for a fix), **recommended** (the venue's guidance), or **heuristic** (this skill's
readability default). Venue rules change every cycle: re-read the target's current author
instructions before reporting a required rule, and mark the finding provisional when the live
source is unavailable.

## Widths (planning only)

Audit the width a figure actually has: `scripts/figure_text_audit.py` reports each placed width
and scale. Use this table to plan a `figsize` or to explain a scale. Values measured from the
style files on 2026-10-09 (TeX points, 72.27 pt = 1 in).

| Venue | `\textwidth` | `\columnwidth` | Source |
|---|---|---|---|
| NeurIPS 2025 | 5.50 in | single column | `neurips_2025.sty` |
| ICLR 2025–2027 | 5.50 in | single column | `iclr20xx_conference.sty` |
| ICML 2026 | 6.75 in | 3.25 in | `icml2026.sty` |
| ACL / EMNLP (`acl.sty`) | 6.30 in | 3.03 in | acl-org/acl-style-files |
| IEEE conference (`IEEEtran`) | 7.14 in | 3.49 in | `IEEEtran.cls`; IEEE quotes 7.16 / 3.5 in |
| ACM `sigconf` | 7.01 in | 3.34 in | `acmart.cls` |
| ACM `acmsmall` (TOSEM, PACMSE/FSE) | 5.48 in | single column | `acmart.cls` |
| Nature | 183 mm (7.20 in) | 89 mm (3.50 in); height ≤ 170 mm | Nature figure guide (required) |

**The 1:1 principle**: author each figure at its placed width, so a font size in the plotting
script is the printed size. Rendered size = source size × scale.

## Rendered text floor

| Venue | Rule | Strength | Source |
|---|---|---|---|
| Nature family | Text 5–7 pt; panel labels 8 pt bold lowercase; sans-serif (Arial/Helvetica) | required | [Nature figure specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/), checked 2026-10-09 |
| IEEE Transactions | Labels about 8–10 pt; subfigure labels 8 pt | recommended | IEEE Transactions template; some journals (e.g. TPEL) require ≥ 8 pt |
| ML venues (NeurIPS, ICML, ICLR, ACL) | No stated minimum; use ≥ 7 pt rendered, 8–9 pt preferred | heuristic | this skill |
| Any venue | Figure text near the caption size (A5 in `aesthetics.md`) | heuristic | Wong, "Typography", 2011 |

Sub- and superscripts count: mathtext sets scripts near 0.7× the parent, so a 7 pt label can
carry a 4.9 pt script. The script measures them directly.

## Fonts

| Venue | Rule | Strength | Source |
|---|---|---|---|
| Nature family | Embedded TrueType 2 or 42; no outlined text | required | Nature figure specifications |
| ICML 2026 | "There is no Type 3 font check" | required (absence) | [ICML 2026 author instructions](https://icml.cc/Conferences/2026/AuthorInstructions), checked 2026-10-09 |
| IEEE | All fonts embedded in EPS/PS/PDF figures | required | IEEE Author Center |
| Other venues | Check the current CFP or PDF checker (ACL `aclpubcheck`, ACM TAPS, IEEE PDF eXpress) | verify | — |

Type 3 fonts from matplotlib are vector glyph programs, not bitmaps; they print sharply but
may fail a venue's checker and do not search or edit well. Bitmap Type 3 fonts come from old
`dvips` pipelines and do blur.

| Tool | Embeds TrueType (Type 42) |
|---|---|
| matplotlib | `plt.rcParams['pdf.fonttype'] = 42` |
| R / ggplot2 | `ggsave(..., device = cairo_pdf)` |
| TikZ / PGF | Uses the document's fonts; no extra step |
| Inkscape | Save as PDF with fonts embedded (not converted to paths, for Nature) |

## Raster resolution (at placed size)

| Venue | Rule | Strength | Source |
|---|---|---|---|
| Nature family | Photographs ≥ 300 dpi; 450 dpi or more preferred | required / recommended | Nature figure specifications |
| IEEE | Colour/greyscale ≥ 300 dpi; line art ≥ 600 dpi | required | IEEE Author Center |
| ICML 2026 | Vector graphics for line and bar plots | recommended | ICML 2026 author instructions |
| Any venue | Data plots as vector; raster only for images | heuristic | Wilke ch. 27 |

The script reports effective DPI as pixels ÷ placed inches; resolution metadata in the file
does not matter, and upsampling adds no detail.

## File size

| Venue | Limit | Source |
|---|---|---|
| ICML 2026 | Submission 50 MB; camera-ready 20 MB | ICML 2026 author instructions |
| Nature | Check the journal's submission system | — |
| Others | Read the current CFP; OpenReview venues set their own limits | — |
