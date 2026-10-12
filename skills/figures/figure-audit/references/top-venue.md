# Top-venue Bar: Contract, Exemplar Conventions, Generated Look, Diagrams

Reference that A1–A7, Checks 7, 12 and 16 consult when the audit judges whether a figure meets
the top-venue bar. Every entry names its **home** check; a finding keeps that check's ID and tags
its evidence `[exemplar: paper:Fn]` (`aesthetics.md`). Nothing here is a separate check.

## Floor and bar

- **Floor**: what accepted papers show. Measured on the body figures of 16 award papers (NeurIPS
  2025, ICLR 2026, ICML 2025–2026, ACL 2025–2026; 2026-10-12). Of the 63 venue-template figures with
  measurable text: median figure text 5.9 pt, 44 (70%) below 7 pt; text/caption ratio median 0.59,
  17% at 0.8 or more. Median 3 chromatic colours per vector figure; 22 of 96 captions open with a
  claim sentence; figure-level titles, a value on every bar and dual axes all occur.
  Those papers won on content, so the floor does not separate good figures from accepted ones.
- **Bar**: what the designed subset does: Superposition, Diffusion-memorize, Flexibility Trap,
  1000-layer, CollabLLM, RL-Reasoning, and single figures of LLMs-Get-Lost and Hivemind. Tier
  membership is visual judgement; each convention cites its figures so a finding can be checked or
  overridden.
- Measurements and crops, when present: `~/.claude/reference/figure-exemplars/` (private; the crops
  are other authors' figures and stay out of this skill).

## The figure contract (Phase 2, first step)

Per figure, before any check:

```
Claim:      one sentence with a verb, from the caption and the citing paragraph
Task type:  comparison | trend | distribution | matrix | mechanism | architecture | example
Panels:     (multi-panel) a: role, b: role, ...
```

| Task type | The figure shows |
|---|---|
| comparison | methods or conditions against each other, paired or not |
| trend | a response over a continuous or ordered variable (scaling, training, sweeps) |
| distribution | spread of observations (histograms, strips, boxes, violins) |
| matrix | values over two indices (heatmaps, per-layer profiles, confusion matrices) |
| mechanism | how one part works: steps, states, before/after, a worked example |
| architecture | the whole system or method pipeline |
| example | qualitative samples, images, generated text |

Panel roles (Check 12), the smallest sufficient set: setup, representative example, primary
evidence, baseline or control, decomposition, stratification, orthogonal validation, stress test,
boundary or failure case, mechanism (nature-figure `references/multipanel-evidence-architecture.md`).

## Bar conventions (B)

A missing convention is an ISSUE only when its home check's flag condition holds (A2: the key
comparison is demonstrably hard; A7: a label by the wrong referent, legend order unlike the data, a
repeated legend); the exemplar then substantiates it, at the home check's severity. Otherwise record
a Minor `[taste]` suggestion naming the row, which the pipeline applies on a top-venue request.

| # | Convention | Home | Task types | Exemplars |
|---|---|---|---|---|
| B1 | The claim is drawn in data coordinates: a delta arrow with its number, a fitted slope, labelled regimes, a count of paired wins | A2 | comparison, trend | flextrap F8, F5; superpos F1d, F6b; diffmem F1, F3; rlreason F8 |
| B2 | One colour per entity across the paper | A6, 16 | all plots | flextrap F1, F3, F4, F7; rlreason F2–F7, F9; collabllm (schematics and plots) |
| B3 | An ordered variable gets an ordered colour scale: a single-hue ramp, or a perceptually ordered multi-hue map with a colour bar; a signed one, a diverging map centred on zero; categories keep to the few hues they need | A6 | trend, matrix | Single-hue: 1000layer F1, F7, F12; resist F5, F6. Multi-hue with colour bar: superpos F4a. Diverging: superpos F4b (weight decay) |
| B4 | Theory or fit as a dashed dark line, data as markers | A6 | trend | superpos F3b, F4a, F6b; diffmem F3 |
| B5 | Small multiples share style and one legend outside the panels | A7 | comparison, trend | 1000layer F1, F7; flextrap F3, F8; rlreason F2 |
| B6 | Direct labels next to the data, including series-coloured text (outside the Nature family) | A7 | comparison, trend | superpos F1b; diffmem F1; lost F1; hivemind F7, F9 |
| B7 | Figure text near the caption size (ratio ≥ 0.8) | A5 | all | superpos 0.89–1.01; diffmem up to 1.02; polar F3 0.99 |
| B8 | The caption opens with the claim | 7 | all claim figures | superpos 5 of 6; 1000layer 5 of 11; rolldice 5 of 7 |

Papers: superpos arXiv 2505.10465 · diffmem 2505.17638 · flextrap 2601.15165 · 1000layer
2503.14858 · collabllm 2502.00640 · lost 2505.06120 · hivemind 2510.22954 · rlreason 2504.13837 ·
polar 2505.16932 · rolldice 2504.15266 · resist ACL Anthology 2025.acl-long.1141.

## Generated-look signals (G)

A **generated look** is form that no design decision explains: an encoding the claim never uses,
a default left in, decoration. It reads as unreviewed output, and reviewers discount the figure
for it. Each signal is a finding under its home check. The finding cites the bar figure that shows
the alternative (the Cite column, or the exemplar viewed in the comparison); with no such contrast
it is `[guideline]` and takes no generated-look severity (SKILL.md, Severity). With the contrast it
may reach Major even where the home check caps its own flags at Minor (G2 under A7).

| # | Signal | Home | Fix | Cite | Provenance |
|---|---|---|---|---|---|
| G1 | Identity encoding the claim does not use: a marker shape per seed or run, jitter, per-unit colours | A1, A6 | One filled marker per series; separate points only where they would touch | One marker per series: superpos F1b, rlreason F8; spread as a band: 1000layer F1, F7, diffmem F3; shape used only when the claim needs it: superpos F6b (datasets), F8 (regimes) | author feedback on a paper's figures, 2026-10-12 ("AI味") |
| G2 | Ordinal or index legend entries ("1st/2nd/3rd seed", "run 0–4") | A7 | Drop the key with the encoding; name real entities | Legends name values: 1000layer F1 (Depth 4–64), F7 (batch 128–2048); rlreason F8 (GRPO-step150–450) | the same feedback |
| G3 | A caption that lists every encoding ("circles: …; squares: …; segments: …") | 7 | Open with the claim; name only encodings the figure cannot show | 0 of 96 award captions list every encoding; 12 name one or two | award-paper captions |
| G4 | A reference line or band without a label; one grey with several meanings | A7, 4b | Label it directly or in the legend; one meaning per neutral | Labelled on the line: diffmem F3 (n = n\*(p), τ = 8τ_gen), superpos F6a (slope triangles), rlreason F8 (ΔSE); in the legend: superpos F4a ("Theory") | the same feedback |
| G5 | A slide-canvas drawing scaled into the column: LaTeX scale below about 0.6, a 16:9 page, Office fonts (Calibri, Cambria Math) | A5, 2 | Redraw at the placed width (figure-pipeline redraw route) | Bar text/caption ratio 0.89–1.01 (superpos); FigGenie exemplars print at 6.5–7 pt | 1:1 principle (`venues.md`) |
| G6 | Boxed bold section headers; containers filled as dark as their contents or nested past three levels; every element framed | A3 | Outline containers, or a fill lighter than the children; titles as plain text in the container's headroom | The FigGenie exemplar viewed in the comparison | nature-figure vector rules: outline-only as the safe default, no container darker than its children, nesting ≤ 3, titles in the headroom |
| G7 | Clip-art that carries nothing (a document glyph for "data", robot heads) | A3 | Remove it, or draw the object itself (a matrix, a token row) | The exemplar viewed in the comparison | Contested points: embellishment |
| G8 | Equal panels for unequal evidence; a mirror layout repeating one comparison per metric | A1, 12 | Give the primary evidence the space; one role per panel | The exemplar viewed in the comparison | nature-figure evidence architecture |

**Floor habits** are not generated-look signals: award papers show them, so their home check
sets the severity. A figure-level title over a whole figure (Check 10; imperfective F2; panel
headings naming a benchmark or a panel's content, as in nsa F1, are fine), a value on every bar
(A3; imperfective F1, F3, hivemind F10, F11), dual y-axes (Check 11; imperfective F2, maskeddiff F3).
The default matplotlib palette is not a signal either: bar-tier figures use tab10 too.

## Diagrams (mechanism, architecture)

The award set holds few diagrams (superpos F1a, F1c; lost F7, in the appendix) and did not grade
them. These readings of A1–A7 come from nature-figure's
`references/vector-schematic-style-rules.md` and FigGenie's corpus of 1,055 rated architecture
figures from systems venues (OSDI, NSDI, SOSP, ASPLOS 2023–2026); its numbers describe that
corpus, not ML venues.

- **A1**: one point the figure argues. The new component carries the single accent; existing parts
  are grey or pale, external ones white with a grey outline. Component state the method depends on
  (new or existing, frozen or updated, training-only or inference-only) is encoded and keyed. The
  main path is the heaviest line; in a walkthrough, circled step numbers match the caption. An
  unnumbered comparison, state machine or cutaway is not a defect (FigGenie).
- **A2** (mechanism): the arrangement follows what the reader must see. A difference: side by side
  on a shared skeleton. One object changing: states in sequence, identity kept. Conditions: a state
  or decision diagram. A request through the system: a trace over the structure. Inside one
  component: an anatomy or a worked example with real values. Exemplars: vLLM (arXiv 2309.06180)
  Fig 6, logical and physical blocks joined by the block table; FlashAttention (NeurIPS 2022) Fig 1,
  memory hierarchy → tiling → measured runtime; Transformer (NeurIPS 2017) Figs 1–2, overview then
  the inside of attention.
- **A3**: containers outline-only by default; a fill is fine when it marks a group and stays lighter
  than its children. Nesting at most three levels; repetition as `×N`; no gradients, shadows or 3D.
- **A4**: equal gaps on a common grid; one reading direction, with the main path monotone along it.
  No line passes through a label, and arrows end on a container boundary only when the whole group
  is the endpoint.
- **A5**: authored at the placed width (single column ≈ 240 pt, labels 6.5–7 pt, strokes ≈ 0.6 pt
  in FigGenie's corpus), text at or above the venue floor, one family. Labels and formulas use the
  paper's terms and symbols; `notation-audit` confirms them.
- **A6**: every fill carries a role and is keyed by a label, the caption or a legend within one
  box-width; dashed lines carry one meaning per figure. Colour count is contested (FigGenie's good
  figures use a median of 6 fills; nature-figure allows two saturated fills plus one accent): audit
  keying and consistency, not the count.
- **A7**: every directed edge has an arrowhead, each arrow style means one thing (data, control,
  gradient or update), and labels sit by their referent.
- In FigGenie's corpus, weak figures are under-invested (no colour system, no arrowheads, no step
  markers), not dense or small-typed; a dense diagram is not a finding unless the reader loses the
  main path.
- With no matching exemplar (FigGenie's corpus holds systems papers, so ML method figures often have
  none), G5–G7 are `[guideline]`; G5 keeps Check 2's measured Major when text is below the floor.
- Correctness of what a diagram says (edges, branches, worked examples) is Check 14.
- Measure: `figure_text_audit.py` gives text size and scale for any placed PDF;
  `nature-figure/scripts/audit_svg_schematic.py` checks an SVG at final size; FigGenie's
  `scripts/lint.py` checks its own SVGs.

## Exemplar comparison (Phase 2, after the checks)

Models agree weakly with experts on aesthetics and correct named violations more reliably than
they detect them (`aesthetics.md`, Why the caps), so judge against named conventions and a
reference figure.

1. From the contract's task type, pick two or three bar exemplars of that task: from the task-type
   index of `~/.claude/reference/figure-exemplars/cards.md` when present (each card gives the
   exemplar's contract, its devices by B/G row and what not to copy), otherwise plots from the B
   table (a crop from `~/.claude/reference/figure-exemplars/crops/` when present, otherwise the
   figure in the arXiv PDF); diagrams from the cards' diagram tier or with FigGenie's
   `scripts/find_exemplars.py --domain … --content … --semantics …` (its `print.png`). When none
   fits (off-domain matches only), record that and the reason; the rows then carry their home
   checks' tags.
2. View the figure's crop beside them at the same physical scale.
3. Give every B row listed for the task type, and every G row, a disposition under its home check:
   PASS, ISSUE (`[exemplar: paper:Fn]`, or the home tag without a fitting exemplar), REVIEW NEEDED,
   or N/A. The report's `Bar:` line per figure records them.
4. Exemplars are the bar, not a template: a finding names the device to adopt (a delta arrow, a
   direct label), never "make it look like Fn".

Done when every applicable B row and every G row has a disposition for every figure.
