# Figure & Table Audit — 14 Checks (Detail)

## 1. Font Embedding and Type

Run `pdffonts main.pdf` and verify:
- **Zero Type 3 bitmap fonts** — blurry in print, desk rejection at some venues
- **All fonts embedded** — no "not embedded" in the output
- **Font family**: sans-serif (Arial/Helvetica) for data figures. Serif (Times) acceptable for text-heavy diagrams if it matches the paper body
- **TrueType 42 only**: Nature requires TrueType 2 or 42; most CS venues accept any embedded font

## 2. Text Size Verification

Concrete, measurable — not a subjective impression.

Formula: `rendered_pt = source_pt × (latex_width / source_width)`

Check these elements in every figure:
- Axis labels, tick labels (most common failure), legend text
- Annotation text, panel labels (a), (b), (c)

Flag as **MAJOR** if any text is below venue minimum (see venues.md).
Flag as **MINOR** if legible but noticeably smaller than caption text.

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
- **No rainbow/jet colormaps** for sequential data — use viridis, plasma, single-hue
- **No background gridlines, drop shadows, or patterns** — Nature prohibits these

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
- Aspect ratio: 4:3 or 16:9 unless data demands otherwise
- White space: no excess margins (`tight_layout()` or `bbox_inches='tight'`)
- Spine cleanup: remove top/right spines (community best practice)

## 6. Data Integrity

- Every axis has a label with units in parentheses where applicable
- Axis ranges reasonable — no misleading truncation unless noted
- Legend complete — every data series appears
- Spot-check 2-3 data points against table values. Flag as BLOCKING if mismatch

## 7. Caption Quality

- **Self-contained**: readable without main text
- **Ends with takeaway**: last sentence states what to conclude
- **Numbers match**: any numbers in caption match the visual data
- **Panel descriptions match panels**: (a)/(b) exist and are labeled
- **Abbreviations defined**

## 8. Table Header Quality

- **Direction arrows**: ↑ or ↓ in headers for metrics
- **Units in headers**: every numerical column has units
- **Arrow consistency**: all tables or none — don't mix
- **Bold consistency**: best value per metric per group is bolded; verify correctness
- **Task set documentation**: if "Avg." covers different task sets, each caption states which
- **Decimal precision**: consistent within each column

## 9. Cross-Reference Consistency

- Every figure/table referenced via `\ref{}` at least once
- Every algorithm referenced
- Reference appears before or near the float
- No orphan floats (exist in PDF but never referenced)

## 10. Venue Compliance

- No title inside figure (caption serves as title)
- Resolution: raster ≥300 DPI (≥450 for Nature); vector preferred for data plots
- Format: PDF/EPS for vector; TIFF/PNG for raster. Avoid JPEG for data plots
- File size under venue limit (typically 50MB)
- Color mode: RGB for submission
- No outline text (Nature requirement)

## 11. Visualization Anti-patterns

- **Dynamite plots** (bar + error bar for continuous data): use dot/violin/box plots
- **Rainbow/jet** for sequential data: use viridis, plasma, cividis
- **Overplotted scatterplots** (>1000 points): use density/hex/alpha
- **Dual-axis without visual separation**: maximize color distinction
- **3D for 2D data**: use flat versions
- **Pie charts >5 slices**: use horizontal bars
- **Truncated y-axis without notation**: flag unless broken-axis notation used

## 12. Panel Design Coherence (multi-panel only)

Panels should pass ≥2 of 4 tests:
1. Shared axis for direct comparison
2. Causal/temporal link
3. Zoom relationship
4. Synthesis requirement — reader MUST see both

Flag MAJOR if 0 tests pass. Flag MINOR if 1 test passes.

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
