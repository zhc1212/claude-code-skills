# Repair Recipes

The audit finding says what is wrong and names the target; the recipe is the smallest edit that
reaches it. Checks are defined in figure-audit (`references/checks.md` for 1–14,
`references/aesthetics.md` for A1–A7 and 16); thresholds live only in its `references/venues.md`.
Every recipe ends with the guard comparison and a Recheck of the affected figures.

Semantic risk names what the guard should catch if the edit goes wrong. A positioned legend or
label is a candidate placement: inspect the 300 dpi crop before accepting it.

## Text, fonts, overlap (Checks 1–3)

| Check | Problem | Smallest edit | Semantic risk |
|---|---|---|---|
| 1 | Type 3 fonts (matplotlib) | `plt.rcParams["pdf.fonttype"] = 42` (and `ps.fonttype`) | None; STYLE only |
| 1 | Type 3 fonts (R) | `ggsave(..., device = cairo_pdf)` | None |
| 1 | Fonts not embedded | Re-export with embedding on; in Inkscape keep text as text | Outlining text makes it unmeasurable |
| 2 | Text below the floor after scaling | Author at the placed width (`figsize` = the width the script reports), keep source sizes; or raise the source size | Changing `figsize` re-flows ticks: AXES changes are expected and attributable |
| 2 | Mathtext scripts below the floor | Raise the parent size, or write the script as plain Unicode (`R²`) | NUMERIC if a digit in a label changes form; check it reads the same |
| 3a | Legend on data | Move outside the axes (`bbox_to_anchor` below or beside), into an empty panel, or replace with direct labels | Re-ordered legend entries are TEXT; entity–colour mapping must not change |
| 3b | Label spills into the next panel | Anchor at the data midpoint; widen `wspace` | Moving an annotation is STYLE; changing its text is TEXT |
| 3c | Label clipped at the axis edge | Place boundary labels on the inner side; `clip_on=False` only with room | Widening limits is AXES and must be attributed |
| 3d | Text inside bars unreadable | Move the label outside the bar; drop a redundant one | Rounding a value label is NUMERIC: keep the precision |

## Colour, layout, data (Checks 4–6)

| Check | Problem | Smallest edit | Semantic risk |
|---|---|---|---|
| 4 | Colour-only cues, red–green, grey collapse | Add line style or marker per series; switch to Okabe–Ito or a perceptually uniform map | Entity–colour mapping must stay consistent across figures (Check 16) |
| 4b | One colour, two meanings | Give the second meaning its own channel; state both in the caption | Caption edit is a TeX change: promote only if selected |
| 5 | Width mismatch with the float | Set `figsize` to the placed width; regenerate | Re-flowed ticks are AXES |
| 5 | Missing or inconsistent panel labels | `ax.text(-0.1, 1.05, "(a)", transform=ax.transAxes, fontweight="bold")`, one helper for all panels | None |
| 6 | Missing axis label or unit | Add the label with its unit in parentheses | TEXT only |
| 6 | Bars not starting at zero | Start the value axis at zero, or change to dots if the range must stay | DATA must not change; AXES does. Changing the mark type is a representation change: user decision |
| 6 | Log axis unlabelled | Add "(log scale)" or "(log₂ scale)" to the axis label | TEXT only |

## Captions, tables, references (Checks 7–9, 14)

These edits are in TeX; promote them only when the finding is selected, and re-check the hash of
the TeX file, which other sessions edit most often.

| Check | Problem | Smallest edit |
|---|---|---|
| 7 | Claim figure without a takeaway | Add one sentence stating what the figure shows |
| 8 | Direction missing on a metric | `$\uparrow$` / `$\downarrow$` in the header, or say it in the caption |
| 8 | Bold not on the true best | Re-bold after checking every entry in the group |
| 9 | Unreferenced float | Add `Figure~\ref{fig:X}` where the text discusses it |
| 14 | Name differs across figures, tables and text | Change the figure's display string to the paper's name (TEXT); the text's wording is the user's |

## Anti-patterns, panels, uncertainty (Checks 11–13)

These change the representation, so the user decides before the edit; the guard will report DATA
and the report records the authorisation.

| Check | Problem | Edit, once authorised |
|---|---|---|
| 11 | Dynamite plot | Dots with intervals, or a strip plot of the observations |
| 11 | Dual axes | Two aligned panels sharing x |
| 12 | Panels with no joint reading task | Split into separate figures |
| 13 | Multi-seed data without intervals | Add intervals of a stated kind (SD, SE, 95% CI) from the data that exist |

## Aesthetic principles (A1–A7) and the figure set (16)

`[taste]` findings change only on the user's request. Prefer edits that keep every coordinate.

| Principle | Problem | Smallest edit | Semantic risk |
|---|---|---|---|
| A1 | Salience off the claim | Emphasise the claimed series (weight, colour, label) and mute context to grey, each grey labelled and used for one meaning | None if values stay; check no other series loses its label |
| A2 | Key comparison hard to read | Direct labels at line ends; annotate the difference the caption claims | NUMERIC for an added difference: it must match the text or table |
| A3 | Heavy non-data ink | Lighten grids and spines; drop frames and backgrounds | STYLE only |
| A4 | Touching or misaligned elements | Move the label or connector; align panels on one grid; for near-tied markers, smaller markers, a distinct line pattern per series, the smaller shape drawn on top, and a thin white edge on filled marks in every plot of the set | Open markers can collide with a fill convention elsewhere in the set (16); jitter changes data positions and needs approval |
| A5 | Flat or broken type hierarchy | One size per role (ticks < labels < panel titles), one weight for emphasis | STYLE only |
| A6 | Palette noise or misleading colour | Fewer hues; one highlight; neutrals for context, a grey entity only when labelled and no other meaning shares its grey | Entity mapping across figures (16); simulate deuteranopia and protanopia on the most crowded region before adopting a new entity colour |
| A7 | Legend far from data, missing key | Direct labels, or a legend in reading order next to the data | TEXT order changes are attributable |
| 16 | Font differs across the set | One `font.family` in a shared style imported by every generator | Every consumer changes: all are in the expected-change set |
| 16 | Same entity, different colour or marker | One `COLORS` / `MARKERS` mapping in the shared style | Same; check no two entities now share a channel |
| 16 | Display name differs | One `LABEL` mapping used by every figure | TEXT only |
| 16 | Same condition, different marker fill | Draw the series open, then append the filled points after every series; add a key in the set's wording | The guard reports appended points as STYLE `.overplot`; points interleaved between series re-key the later lines and read as DATA |

## Top-venue bar (B) and generated-look signals (G)

Entries are defined in figure-audit's `references/top-venue.md`; each finding carries its home
check's ID. Rows marked *representation* follow the Plan's representation-change rule.

| Entry | Problem | Smallest edit | Semantic risk |
|---|---|---|---|
| G1 | Identity encoding the claim does not use | One filled marker per series with a thin white edge; keep points on their row and split vertically only pairs closer than one marker diameter in data units | *Representation*: `figure_guard.py points --axis x --rows` equal; removed artists listed by key |
| G2 | Ordinal or index legend | Remove the entries together with their encoding | TEXT |
| G3 | Caption lists every encoding | Claim first, then the setup, then at most the encodings the figure cannot show | TeX; every number in the caption matches its source |
| G4 | Unlabelled reference line; one grey, two meanings | Label the line directly or in the legend; give the second meaning its own neutral or line style | TEXT, STYLE |
| G5–G7 | Slide-drawn diagram, boxed headers, clip-art | Redraw (SKILL.md, Plan) | Content inventory |
| G8 | Mirror or equal panels | Merge, move a panel to the appendix, or give the primary evidence the width | *Representation*; the user decides |
| B1 | Claim not drawn in the plot | Annotate the quantity the caption claims: a count ("24/24 below the baseline"), a delta with its number, a labelled better side | NUMERIC gained: matches the text or table |
| B3 | Ordered or signed variable in categorical hues | Ordered magnitude: colour by rank from one sequential map. Signed or deviation: a diverging map centred on the meaningful midpoint (zero, a baseline). A colour bar for a continuous variable | STYLE; the centre is the data's midpoint, not the range's; the entity map elsewhere stays (16) |
| B6 | Legend lookups for two to four series | Direct labels at line ends, in the series colour outside the Nature family | TEXT; check collisions on the crop |
| B7 | Figure text below 0.8× the caption | Raise source sizes toward the caption size at the placed width; relocate before you shrink | AXES reflow; Recheck the page |

B2, B4, B5 use the A6, A7 and 16 recipes above; a figure-level title, a value on every bar and dual
axes (floor habits) use the Check 10, A3 and Check 11 recipes.
