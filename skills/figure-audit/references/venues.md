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
| NeurIPS 2025–2026 | 5.50 in | single column | `neurips_2025.sty`, `neurips_2026.sty` |
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
| ICML 2026 | Figure text no smaller than the caption (9 pt) | recommended | [Accessible papers guidance](https://icml.cc/Conferences/2024/AccessiblePapersAndTalks), linked from the 2026 author instructions, checked 2026-10-12 |
| CVPR | Figure fonts match the body text; readers cannot zoom | recommended | `sec/2_formatting.tex`, github.com/cvpr-org/author-kit, checked 2026-10-12 |
| NeurIPS 2026, ICLR 2027, ACL | No stated minimum | — | style files and formatting guides, checked 2026-10-12 |
| ML venues | Floor ≥ 7 pt rendered (below: Check 2, Major); bar ≥ 0.8× caption (A5, B7) | heuristic | this skill; award-paper measurements in `top-venue.md` |

Caption sizes: ICML 2026 9 pt (`icml2026.sty`), ACL 10 pt (`acl.sty`), NeurIPS 2026 body size 10 pt
(its sty sets no caption font; inferred).

Sub- and superscripts count: mathtext sets scripts near 0.7× the parent, so a 7 pt label can
carry a 4.9 pt script. The script measures them directly.

## Lines, captions and colour

| Venue | Rule | Strength | Source |
|---|---|---|---|
| NeurIPS 2026 | Artwork "neat, clean, and legible"; lines dark enough to reproduce; legible printed in black/white or colour; sample caption: "Explain what the figure shows and add a key take-away message" | recommended | `neurips_2026.tex` in the official formatting zip, checked 2026-10-12 |
| ICLR 2027 | NeurIPS wording, plus "art work should not be hand-drawn" | recommended | `iclr2027_conference.tex`, github.com/ICLR/Master-Template, checked 2026-10-12 |
| ICML 2026 | Lines dark and ≥ 0.5 pt; no text on a grey background; label every component, name each axis, a legend describing each curve; no title inside the figure | recommended | `example_paper.tex` §Figures in `icml2026.zip`, checked 2026-10-12 |
| ICML 2026 | Do not rely on colour alone: combine shapes, positions, line types; add alternative text to all figures and tag the PDF | recommended | Accessible papers guidance, checked 2026-10-12 |
| ACL / ARR | "grayscale readability is strongly encouraged"; no colour-only distinctions | recommended | `formatting.md`, github.com/acl-org/acl-style-files, checked 2026-10-12 |
| CVPR | Line widths that render in print; not colour alone (red vs green): add a second discriminative feature | recommended | `sec/2_formatting.tex`, CVPR author kit, checked 2026-10-12 |

## Fonts

| Venue | Rule | Strength | Source |
|---|---|---|---|
| Nature family | Embedded TrueType 2 or 42; no outlined text | required | Nature figure specifications |
| ICML 2026 | "There is no Type 3 font check" | required (absence) | [ICML 2026 author instructions](https://icml.cc/Conferences/2026/AuthorInstructions), checked 2026-10-09 |
| IEEE | All fonts embedded in EPS/PS/PDF figures | required | IEEE Author Center |
| NeurIPS 2026 | Only Type 1 or embedded TrueType fonts; a file with Type 3 or non-embedded TrueType fonts is sent back for fixing | required | `neurips_2026.tex` §Preparing PDF files, checked 2026-10-12 |
| ACL / ARR | Embed all necessary fonts | required | `formatting.md`, acl-style-files, checked 2026-10-12 |
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
