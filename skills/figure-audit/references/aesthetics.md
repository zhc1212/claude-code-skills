# Aesthetic Principles for Paper Figures (Checks 15–16)

Aesthetics here means *how well a figure's form serves its claim at print size*: what the eye
reads first, how fast the intended comparison decodes, whether the page reads as one family.
Each principle names its evidence and its exceptions, so a finding can cite one and respect the
other.

## Evidence tags and severity caps

Tag every Check 15–16 finding with its basis. Severity follows consequence: **Major** when a
reader at print size misreads the claim or must work noticeably harder to find it; **Minor** for
polish. The tag caps how far a finding may go.

| Tag | Basis | Cap |
|---|---|---|
| `[measured]` | A number from `scripts/figure_text_audit.py`, `pdffonts`, or a geometry auditor; say which figure grouping it measured | Major |
| `[evidence: source]` | An empirical perception study (Cleveland–McGill, Franconeri, Correll, Crameri) | Major |
| `[guideline: source]` | Expert design guidance (Wong, Wilke, Rougier, Tufte) observed in the render | Major |
| `[taste]` | A judgement a competent designer could reasonably decline | Minor |

Venue requirements belong to Check 10, and suspected misrepresentation to Check 14 (substantiate
it there before calling it Blocking). Report one finding once and cross-reference it.

Every principle gets a disposition per figure: PASS, ISSUE, REVIEW NEEDED, or N/A. A REVIEW NEEDED
says what is uncertain and what evidence would settle it (a source file, the author's intent, a
zoomed crop).

Why the caps: multimodal models agree weakly with experts on aesthetics (VisJudge-Bench,
ICLR 2026: correlation 0.18–0.41 on aesthetic dimensions) and misjudge fine geometry such as
touching versus overlapping shapes (Rahmanzadehgervi et al., ACCV 2024). Measure what can be
measured, judge the rest against a cited principle, and mark what remains as taste.

## Viewing protocol

Judge figures the way a reviewer meets them.

1. **In context**: render the page holding the figure (`pdftoppm -cropbox -r 150 -f P -l P -png
   main.pdf /tmp/pg`) and judge the figure against the body text and caption beside it.
2. **Zoomed crops** for geometry (overlap, alignment, line weight): crop at 300 dpi with
   `pdftoppm -cropbox -r 300 -f P -l P -x X -y Y -W W -H H`, where pixels = the script's `rect_pt`
   × 300/72. `rect_pt` is unrotated; on rotated pages crop from the full render instead.
3. **Squint test** for A1: at the in-context render, note which mark the eye lands on first.
4. **Contact sheet** for Check 16: render every figure page at one resolution and tile the figure
   crops at the same physical scale, so sizes compare honestly.

## Check 15 — per-figure principles

### A1. Message and salience
Write the figure's claim in one sentence (caption plus citing paragraph). The marks that carry
it (the *hero*: the key comparison, an effect, an uncertainty, a limitation) are the most
salient; *context* (reference series, scaffolding, gridlines) is visibly quieter.
- Exceptions: parity or benchmark figures where no method should dominate; a salient baseline
  when the baseline is the point; a highlighted non-winner the text discusses.
- Source: Rougier et al. 2014 (rules 2, 9); Wong, "Salience to relevance", *Nat. Methods* 2011;
  Franconeri et al. 2021 (guide the intended comparison).
- Flag when the squint test lands on something the claim does not need, or when highlighting
  contradicts the data (a highlighted method that does not lead, with the text saying it does).
  `[guideline]`, up to Major.

### A2. Encode the key comparison legibly
The comparison the claim rests on should read quickly at print size. Position on a common,
aligned scale reads most precisely; adjacent items on a shared axis compare fastest; a plotted
difference (gain, delta, paired change) spares the reader a subtraction. These are preferences
ranked by evidence, applied to the figure's task.
- Source: Cleveland & McGill 1984; Heer & Bostock 2010; Franconeri et al. 2021 (comparisons
  run at two or three per second).
- Flag only when the key comparison is demonstrably hard: it depends on area, angle or colour
  intensity, on stacked segments off the baseline, or on panels without a shared axis, and the
  render shows the difference is hard to judge. `[evidence]`, up to Major.

### A3. Ink hierarchy and restraint
Ink weight follows importance: data > annotations and reference lines > axes > gridlines.
Gridlines stay light, or absent where the venue asks (Nature). Frames, 3D, shadows, gradients
and textures appear only when they encode data. An annotation, label or pictogram that carries
the message counts as data.
- Source: Tufte, data-ink; Wilke ch. 23 (balance data and context) and ch. 26 (no 3D); Few,
  "The Chartjunk Debate", 2011; Borkin et al. 2016.
- Flag axes or grids as heavy as the data, and 3D or shadows on 2D data (`[guideline]`, Minor;
  Major when they hide data); "could be lighter" (`[taste]`).

### A4. Spatial organisation
Alignment, grouping and whitespace together. Plot areas meant to compare share edges; panel
labels share one position; repeated gutters match; gaps within a group are smaller than gaps
between groups; text clears every edge; axis limits sit near the data unless a zero baseline is
required (Check 6).
- Exceptions: deliberate spanning or hero panels, asymmetric margins that make room for a shared
  legend or colourbar, whitespace that separates groups.
- Source: Wong, "Gestalt principles" parts 1–2, *Nat. Methods* 2010; Wong, "Negative space" and
  "Layout", 2011.
- Measure with `nature-figure/scripts/audit_panel_alignment.py` when the matplotlib/R source can
  be run (1.5 pt tolerance, `[measured]`); otherwise inspect zoomed crops (`[guideline]`).
- Flag misaligned comparable edges, ambiguous grouping, or crowding. Minor; Major when the
  grouping misleads. Large empty regions alone are `[taste]`.

### A5. Typographic hierarchy
Text of one role (panel label, axis label, tick label, legend, annotation) shares one size,
weight and family; roles keep a visible order (panel labels ≥ axis labels ≥ tick labels).
Figure text sits close to the caption size so the figure reads as part of the page. The paper
follows one family convention (sans throughout as Nature requires, or the body family); bold,
italic and a math fallback (STIX, Computer Modern) belong to that family, and metric-compatible
clones count as one (Liberation Serif, Nimbus Roman, TeX Gyre Termes and Times all read as Times). Casing and number
formats stay consistent; units sit in parentheses; text is black or grey (Nature: no coloured
text).
- Source: Wong, "Typography", *Nat. Methods* 2011; Wilke ch. 24 (use larger axis labels); Nature
  figure specifications.
- Measure with `scripts/figure_text_audit.py`: `families`, `math_fonts`, and the size list with
  samples identify roles (`[measured]`).
- Flag one role at several sizes, tick labels larger than axis labels, a second text family, or
  figure text far below the caption (median under about 0.7× caption). Minor; text below the
  venue floor is Check 2.

### A6. Colour discipline
Palette type matches the data: qualitative for categories, sequential for magnitude, diverging
around a meaningful midpoint (zero, chance, a baseline), cyclic for phase or direction.
Continuous maps are perceptually uniform (viridis, cividis, batlow). Categories stay
distinguishable; grey can carry context and an accent the claim. Colour is paired with marker,
line style, position or a direct label. An entity keeps one colour.
- Source: Crameri, Shephard & Heron, *Nat. Commun.* 2020; Okabe & Ito palette; Wong, "Color
  coding", *Nat. Methods* 2010; Wilke ch. 19–20.
- Verify contrast and grayscale separation with K-Dense `palette_audit.py` when hex values are
  known, or compare a grayscale render (`pdftoppm -gray`).
- Flag a diverging map without a meaningful centre, a non-uniform map on ordered data, colour as
  the only cue, or one colour with two meanings (`[evidence]`, Major); more hues than the
  categories need (`[taste]`, Minor).

### A7. Labels and legends
Each label sits nearest its referent. With a few series, direct labels at line ends or beside
groups spare legend lookups; when they would crowd or collide, one legend outside the data,
ordered like the data and shared across panels that repeat it, reads better.
- Source: Rougier et al. 2014 (rule 8); Wilke ch. 20; Franconeri et al. 2021 (lookups load
  working memory).
- Flag a label nearer the wrong referent, legend order that differs from visual order, or a
  repeated identical legend (`[guideline]`, Minor); "could be direct-labelled" (`[taste]`).

## Check 16 — figure-set coherence (paper level)

The figures of one paper read as one family. Run this once per paper, after the per-figure
checks, on the contact sheet and the script's figure-set summary.

| Property | Pass | Evidence |
|---|---|---|
| Text family | One family across figures (style variants and a math fallback included) | script `main_families` `[measured]` |
| Text sizes by role | Tick labels match tick labels, axis labels match axis labels, across figures | script sizes with samples `[measured]`; a `median_spread` above about 1.5 pt is the trigger to compare roles |
| Entity mapping | Each method, dataset or condition keeps one colour, marker, line style and name | contact sheet `[guideline]` |
| Comparable quantities | Same units, transforms, axis direction and scale where figures are compared | contact sheet `[guideline]` |
| Uncertainty | One encoding and one stated definition for the same kind of interval | captions and render `[guideline]` |
| Line weights and panel labels | Data lines, axes and panel-label style match | zoomed crops `[guideline]` |

Each Check 16 finding names at least two figures and the conflicting mapping. Severity: an entity
that changes colour or marker between figures, or a changed uncertainty definition, is Major,
since readers carry meanings between figures; a colour or marker reused for a different entity
while another channel still tells them apart is Minor, as are other differences. Different figure
types (schematic versus plot) may differ in layout.

- Source: Wong, "Layout", 2011; Franconeri et al. 2021 (consistent conventions reduce decoding
  effort); nature-figure unified-family rule.

## Contested points: context, not defects

- **Embellishment**: pictograms or annotations that carry the message are acceptable (Bateman
  2010; Borkin 2016; Few 2011). Flag only decoration that carries nothing.
- **Gridlines**: light gridlines are acceptable at ML venues; Nature asks for none.
- **Serif versus sans**: either passes when one convention holds for the whole paper and the
  venue allows it.
- **Rainbow maps**: no on ordered magnitude; for cyclic or categorical data, judge whether the
  palette is cyclic and its categories distinguishable, not whether it is a rainbow.
- **Zero baselines for lines and intervals**: not required (Check 6).
