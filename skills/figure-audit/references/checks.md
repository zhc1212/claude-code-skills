# Figure & Table Audit — Checks 1–14 (Detail)

Checks 15–16 (aesthetics and figure-set coherence) live in `aesthetics.md`. Report each check as
PASS, ISSUE (with severity), REVIEW NEEDED (a candidate the evidence cannot settle), NOT AUDITABLE
(the evidence is missing, e.g. text outlined so it cannot be measured), or N/A.

## 1. Font Embedding and Type

Run `pdffonts main.pdf` and on each figure PDF, then verify:
Attribute each font to a figure or to the body before reporting it (`pdffonts` on the figure
file, or the script's per-figure font list).
- **All fonts embedded**: BLOCKING where the venue requires embedding (`venues.md`), otherwise
  MAJOR, since printers substitute missing fonts.
- **Type 3 fonts**: BLOCKING only for a verified breach of an applicable requirement (Nature's
  TrueType 2/42 rule, a venue checker that rejects them); REVIEW NEEDED when the venue's rule is
  unknown; otherwise report the actual consequence. Matplotlib's Type 3 glyphs are vector and
  print sharply; bitmap Type 3 fonts (old `dvips` PK fonts) blur and are MAJOR anywhere.
- **Font family**: one convention for the whole paper (A5 in `aesthetics.md`); Nature requires
  Arial/Helvetica.

## 2. Text Size Verification

Measure, then read. `scripts/figure_text_audit.py main.pdf --floor F` reports every figure's
rendered sizes, including tick labels (the most common failure) and math sub/superscripts.

- Below the venue floor (`venues.md`): **MAJOR**, naming the glyphs and their sizes.
- Legible but far smaller than the caption: A5 in `aesthetics.md`.
- Figures the script cannot measure (outlined text, rasters, inline TikZ/pgfplots, "captions
  without an included graphic"): estimate from the 300 dpi crop against a known size such as the
  caption, and report REVIEW NEEDED with the estimate.
- Diagnose a failure with `rendered_pt = source_pt × scale`; the script prints the scale.

## 3. Text Overlap and Clipping

The most commonly mis-judged check. Do NOT eyeball — systematically verify.

**3a. Legend-on-data overlap** (most frequent failure):
- Legends at `upper right`, `upper left`, etc. are inside axes — they WILL overlap unless data is absent in that region
- For line/trajectory plots: trace each curve through the legend's bounding box
- For spaghetti/band plots: legends inside axes almost always overlap. Use `bbox_to_anchor` outside axes
- Safe placements: below x-axis, empty subplot panel, or `fig.legend()` outside all axes

**3b. Cross-panel label spillover** (multi-panel figures):
- When `wspace`/`hspace` is small, labels near panel edges intrude into adjacent panels
- Check: is any annotation label closer to the neighboring panel's spine than to its data point?

**3c. Label-axis boundary clipping**:
- Data points near axis min/max create labels that clip against the spine
- Check: is the anchor point within the inner 80% of the axis range?

**3d. In-element annotations**:
- Text inside bars/pie slices must have sufficient contrast AND not overlap element edges
- If bar/slice is too small to contain the label, move it outside with an arrow

## 4. Color Accessibility and Print Robustness

- **Grayscale test**: if two series become indistinguishable in B&W, add line style or marker variation
- **Colorblind-safe palette**: avoid pure red-green. Use Okabe-Ito, Paul Tol, or tableau
- **Perceptually uniform colormaps** for ordered data (viridis, cividis, batlow); rainbow/jet
  distort magnitude (A6)
- **Gridlines, shadows, patterns**: Nature asks for none; at other venues A3 governs

### 4b. Color Semantic Consistency (multi-element figures)

When a figure uses color for DIFFERENT encodings in different panels, the caption
MUST distinguish them. Common failure: heatmap red/blue = diverging values, but
adjacent bar chart red/blue = categories.

Check:
1. List every color encoding in the figure
2. If any color has two meanings, verify the caption explains both
3. Flag as **MAJOR** if ambiguous

## 5. Layout and Sizing

- Width matches float type: `\columnwidth` → `figure`, `\textwidth` → `figure*`
- Panel labels: (a), (b), (c) matching caption. Bold, consistent position (top-left standard)
- **Aspect ratio follows the data**, not a fixed 4:3 or 16:9. Trend plots keep the slopes of
  interest mid-range (banking and arc-length heuristics guide it; 45° is a starting point, not a
  target); parity plots (predicted versus true, method A versus B) are square with equal ranges
  and a diagonal; small multiples share one aspect. Sources: Cleveland 1988; Heer & Agrawala
  2006; Talbot, Gerth & Hanrahan 2011. Minor.
- White space: no excess margins (`tight_layout()` or `bbox_inches='tight'`)
- Spine cleanup: remove top/right spines (community best practice)

## 6. Data Integrity

- Every axis has a label with units in parentheses where applicable
- **Ranges are deliberate**. Bars and filled areas start at zero, since length is the encoding;
  lines, points, intervals and confidence bands may use a narrower range chosen for the effect
  size the claim warrants. Compared panels share a range. Log axes say so. A broken-axis mark does
  not remove the exaggeration a truncated range creates (Wilke ch. 17; Correll, Bertini &
  Franconeri, CHI 2020). MAJOR when the range magnifies an effect beyond the text's claim.
- Legend complete — every data series appears
- Spot-check 2-3 data points against table values. Flag as BLOCKING if mismatch

## 7. Caption Quality

- **Self-contained**: readable without main text
- **States the takeaway** when the figure supports a claim; setup and example figures may
  describe instead
- **Numbers match**: any numbers in caption match the visual data
- **Panel descriptions match panels**: (a)/(b) exist and are labeled
- **Abbreviations defined**

## 8. Table Header Quality

- **Direction arrows**: ↑ or ↓ where a metric's better direction is not obvious to the venue's
  readers (loss, truncation rate, latency); none on counts, configuration values or correlations
- **Units in headers**: every numerical column has units
- **Arrow consistency**: one convention across sibling tables
- **Bold consistency**: where a table ranks methods, the best value per metric per group is
  bolded and correct; ties and unranked tables are exempt
- **Task set documentation**: if "Avg." covers different task sets, each caption states which
- **Decimal precision**: consistent within each column

## 9. Cross-Reference Consistency

- Every figure/table referenced via `\ref{}` at least once
- Every algorithm referenced
- Reference appears before or near the float
- No orphan floats (exist in PDF but never referenced)

## 10. Venue Compliance

- No title inside figure (caption serves as title)
- Resolution at placed size (script's effective DPI): ≥300 for photographs and colour, ≥600 for
  IEEE line art; vector for data plots (`venues.md`)
- Format: PDF/EPS for vector; TIFF/PNG for raster. Avoid JPEG for data plots
- File size under the venue's current limit (`venues.md`; ICML 2026 camera-ready is 20 MB)
- Color mode: RGB for submission
- No outline text (Nature requirement)

## 11. Visualization Anti-patterns

Each item is an inspection trigger: confirm the harm at print size before reporting it.
- **Dynamite plots** (bar + error bar for continuous data): dots, violins or boxes show the
  distribution
- **Rainbow/jet** for ordered data: viridis, cividis, batlow (A6)
- **Overplotting**: when marks hide one another at print size, use density, hexbin or alpha
- **Dual axes**: two scales invite false correspondences that colour cannot fix; prefer aligned
  panels, or justify the shared axis in the caption
- **3D for 2D data**: flat versions
- **Pie charts**: when the slices must be compared, use bars
- **Truncated bars**: bars start at zero (Check 6)

## 12. Panel Design Coherence (multi-panel only)

State the joint reading task: what the reader learns from the panels together that no panel
gives alone. Typical reasons are a shared axis for direct comparison, a causal or temporal link,
a zoom or aggregate relationship, or a synthesis the conclusion needs. One strong reason
suffices.

Flag MAJOR when no joint task exists (the panels are separate figures sharing a float); MINOR
when the task exists but the caption leaves it implicit.

## 13. Uncertainty Representation

Data-driven — don't blindly require error bars:
- Multi-seed results (± in tables, "n=", "seeds") → figure should show uncertainty
- Single-seed → don't flag (experimental design issue, not figure issue)
- When present: meaning stated (SD, SE, 95% CI, min-max)
- Spot-check error bar extents against reported ± values

## 14. Claim-Data Consistency

- "A outperforms B" → A visually better in figure AND bolded in table
- "best" → bolding correct across ALL entries in the group
- Caption quotes a number → matches plotted value
- Method naming consistent across all figures/tables/text
