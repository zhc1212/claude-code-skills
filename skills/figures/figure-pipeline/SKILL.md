---
name: figure-pipeline
description: "Fixes the figures of a compiled paper against figure-audit's findings: edits the figure sources in a staging copy, regenerates, recompiles, proves the plotted data unchanged, and verifies every fix with a figure-audit Recheck before writing back. Use after figure-audit reports Blocking or Major findings, for a visible defect (legend over data, clipped labels, text too small after scaling, Type 3 fonts), to redesign a plot or redraw a diagram that misses the top-venue bar or looks generated ('改成顶会风格', '去AI味', '重画方法图'), or when the user says 'fix the figures', 'fix the audit findings', 'figure pipeline', '修图', '修图流程', '按审计修图', '把图都修好', '统一图风格', '修复审美问题'. Not for report-only audits (figure-audit), new figures (paper-figure, nature-figure), or AI illustrations (paper-illustration)."
argument-hint: "[paper-dir or main.tex path] [finding IDs]"
---

# Figure Pipeline: Repair → Regenerate → Verify

figure-audit judges; figure-pipeline repairs. Every judgement here (what is wrong, whether a fix
worked) comes from figure-audit's checks and its Recheck mode. This skill owns the rest: which
findings to fix, where their sources are, the smallest edit, regeneration, compilation, the
data-preservation guard, and the loop. A fix counts as done when a measurement and the audit
protocol say so: models that check their own edits without an external signal tend to make
things worse (Huang et al., ICLR 2024; Kamoi et al., TACL 2024), and edits that touch data fail
most often (ChartEditBench 2026).

## Protocol

```
0. Intake:   a current figure-audit report and the findings to fix
1. Stage:    a frozen copy of the paper, its generators and inputs; the baseline capture
2. Plan:     per finding, the source, the recipe and the expected change
3. Repair:   edit, regenerate under the guard, attribute every change
4. Verify:   compile the staged paper, figure-audit Recheck; at most 2 rounds
5. Promote:  write back what changed, after checking nothing moved underneath
6. Report
```

Paths: `<skill-dir>` is this skill's directory; figure-audit is its sibling `<skill-dir>/../figure-audit`.

## 0. Intake

1. **Report**: work from a figure-audit report whose `Input` sha256 matches the PDF in hand.
   - No report: run figure-audit Full first (精益求精 when the user asks for the highest bar).
   - Hash mismatch: the PDF changed after the audit; run figure-audit again.
   - A report in an older format (no IDs or header): normalize it. Confirm its recorded hash
     matches the PDF, assign IDs by figure-audit's Finding IDs rule, add the header, and mark the
     report "normalized". If the hash cannot be confirmed, re-run figure-audit instead.
2. **Select** findings by ID:
   - Blocking and Major: selected by default.
   - Minor: when the user picks them or asks to fix all findings.
   - `[taste]`: only when the user asks for that aesthetic change; a top-venue request asks for
     the ones that name a row.
   - Findings naming a top-venue row (`B1`, `G2`; the audit writes the row id after the tag): all
     of them when the user asks for top-venue quality or says the figures look generated;
     otherwise by severity.
   - REVIEW NEEDED: settle it with the user first, else leave it unselected.
   - A finding that needs a scientific decision (a denominator, an interval definition, a claim
     in the text) goes to the user as a question; it is not a figure repair.

3. **Route** each selected ID by its source, from the audit's Assets table: generator, FigureSpec,
   inline TikZ, native vector file, redraw, or none. Stage and Plan follow the route.

Done when every selected ID is listed with its severity, who selected it and its route.

## 1. Stage

Repair a frozen copy, since other sessions may rebuild the paper or edit its inputs meanwhile.
Commands are in `references/staging.md`.

1. Copy the paper directory and the generator sources into `<run>/tree`, keeping
   repository-relative paths.
2. Baseline capture in the tree for matplotlib generators: `figure_guard.py capture <run>/cap0 --root
   <run>/tree -- <generator>` with the project's interpreter. Other routes, R included, take the
   asset's sha256 and its 300 dpi crop as the baseline; a redraw adds the content inventory (Plan). A missing input stops the generator: copy that file in at
   the same relative path and re-run. `reads.json` is then the input set; confirm the repository
   holds the same bytes.
3. Every output must be reproduced; the capture marks one that is not, so capture the baseline
   once, in the fresh tree. An unreproduced figure means the paper shows something the generator
   no longer makes: stop and ask, because the audit judged the committed figure.
4. Compile the tree with the project's own build command. `paper-compile` starts with
   `latexmk -C`, which wipes build state, so use the project command directly. The staged PDF's
   `figure_text_audit.py` rows must equal the report's Measurements.
5. Record the repository hashes of every file the run may write back (`baseline.sha256`), the
   paths it will create (a redraw's native source), which must not exist yet, and the hashes of
   the TeX sources the Recheck reads (`text.sha256`).

Done when the staged paper compiles, every output is reproduced, the rows match, and both hash
files exist.

## 2. Plan

For each selected finding, fill one row:

| ID | Source (file:function) | Recipe | Expected outputs | Expected categories |
|----|------------------------|--------|------------------|---------------------|

- **Source**: trace `\includegraphics` to the asset, then route by source type:

  | Source | Repair route |
  |---|---|
  | Python generator, matplotlib (one script or many) | Edit the generator, regenerate under the guard |
  | R or another plotting library | Edit the generator, regenerate; check the source diff (Repair, last paragraph) |
  | FigureSpec JSON (`figure-spec`) | Edit the JSON, validate, re-render |
  | Inline TikZ/pgfplots | Edit the TeX; verify on the compiled page |
  | Hand-drawn vector (Inkscape, draw.io) | Edit the native file, keeping entities and connections |
  | Diagram whose drawing is the defect (slide canvas, G5–G7) | Redraw (below), once the user approves it |
  | AI illustration, or no source | Redraw when the user approves one; otherwise BLOCKED: a repair brief for the user or `paper-illustration` |

- **Recipe**: from `references/repair-recipes.md`, by check. The audit's fix text is the target;
  the recipe is the method.
- **Expected outputs**: the figures the edit should change. An edit to a shared style block or
  helper puts every consumer in the set, so prefer the local edit unless the finding is a
  figure-set (Check 16) one.
- **Expected categories**: what the guard should report, e.g. a renamed label is TEXT, a marker
  change is STYLE, an added axis note is TEXT.

- **Representation changes**: a fix that changes how values are shown (a G1 encoding removed,
  points taken off a shared row, a fitted line added for B1) or redraws a diagram cannot pass the
  DATA rule. An annotation stating the claim (B1 text, an arrow with its number) is TEXT and
  NUMERIC and follows the normal rules. Record the user's approval in the row, then plan it as one of these:
  - **Redesign of a data plot**: Expected categories names the invariant before the edit, as
    inventory keys or a `points` call: "`figure_guard.py points cap0 capN --axis x --rows` equal" for
    marks dodged in y within category rows, "`ax0.coll0.array` unchanged" for a restyled heatmap.
    `points` identifies a series by colour (and with `--rows`, its row), so it holds only where each
    colour is one entity: entities that share a colour on one row need their own check, as do a
    deliberate recolour, a row moved on purpose (its whole multiset moves with its tick label) and
    the pairing a claim rests on. Artists the edit removes (a min–max segment, a per-seed copy) are
    listed by key as the authorised change.
  - **Redraw of a diagram**: route to `figgenie:figgenie-paper-diagram` (ML and systems method
    figures), `nature-figure`'s vector-schematic route (Nature family) or `/drawio-skill` (the user
    wants draw.io); that skill's brief gate is the approval. The guard does not apply: Expected
    categories holds the content inventory of the old figure, every component, edge, label and
    formula. Formulas use the paper's macros, checked with `notation-audit`. For a LaTeX PDF from
    FigGenie, run `export_pdf.py` on `fig.svg`: the font-embedded `fig.final.svg` exports Type 3.

Done when every selected ID has a full row.

## 3. Repair

Make the smallest edit per finding in the tree, regenerate under the guard, and compare with the
baseline:

```bash
python <skill-dir>/scripts/figure_guard.py capture <run>/capN --root <run>/tree -- <generator>
python <skill-dir>/scripts/figure_guard.py compare <run>/cap0 <run>/capN
```

Read every line of the comparison:

- **DATA**: plotted values changed. Revert the edit, unless it belongs to a planned
  representation change (Plan): then every DATA key is one of its listed removals or is covered by
  its invariant, and the invariant check's output goes into the report's Guard column.
- **NUMERIC**: a number in figure text was gained or lost. Each one must appear in the finding's
  fix and match its source (a table, the text, a data file) before you continue. Exit status 1
  means "needs attribution", not "revert".
- **TEXT, AXES**: attribute each change to a selected ID. Tick labels that follow a deliberate
  range change belong to that finding.
- **STYLE**: expected inside the expected-change set. A `.overplot` entry is a line added or
  removed over points its colour already draws; confirm it is the intended overlay.
- **Outside the expected-change set**: an output that is not byte-identical gets an explanation
  or the edit is reverted.
- **Saved on one side only, or UNEXPLAINED** (bytes differ, inventory equal): investigate before
  continuing.

The guard reads matplotlib figures. For any other source, inspect the full source diff for
changed values, filtering, normalisation, intervals and numeric labels, and record the guard's
absence under Coverage.

Done when every difference in the comparison is attributed to a selected ID.

## 4. Verify

1. Compile the staged paper with the project command.
2. Run figure-audit **Recheck** with the baseline report, the staged PDF, and the affected assets:
   the expected-change set, every output the comparison shows changed, and any figure whose page
   or neighbours moved. Recheck in 精益求精 when the user asked for it, so Codex reviews the
   affected figures blind.
3. For each selected ID, crop its figure from the baseline and staged PDFs at 300 dpi, each at
   its own page and rectangle since a repair can move it (figure-audit's viewing protocol), and
   keep the pair as evidence.
4. Decide:
   - Every selected ID RESOLVED and no new finding caused by the repair: go to Promote. A new
     finding the repair did not cause (it was in the baseline PDF too) goes into the report for
     the user and does not hold back promotion.
   - A selected ID PERSISTS, or the repair caused a new finding, and this was round 1: back to
     Plan, carrying the IDs.
   - A fix for A recreates B and the fix for B recreates A, or a fix needs the user's judgement:
     BLOCKED, with the trade-off stated.
   - Still open after round 2: BUDGET_EXHAUSTED. Revert the open fixes in the tree, regenerate
     and compile once more, confirm the kept figures match their verified state, and promote
     those whose edits are independent of the reverted ones. An edit that also resolves another
     selected ID stays, and the report says so.

A round is one edit-regenerate-compile-Recheck cycle, including cycles run through another skill.
The Recheck is protocol-bound verification by the session that made the fix, anchored on the
script and the guard; independence comes only from Codex in 精益求精.

## 5. Promote

1. Right before writing, run the promote block (`references/staging.md`). It writes nothing and
   exits nonzero when:
   - `text.sha256` mismatches: the captions or citing sentences moved under the Recheck. Compare
     them for every changed figure and compile a copy of the live paper with the staged files,
     whose rows must equal the staged PDF's; then adopt the live text's hashes, taken before the
     staged files were overlaid, and rerun.
   - `baseline.sha256` mismatches, or a path the run creates now exists: someone changed it since
     staging: BLOCKED. When the other change leaves your edits' meaning intact (a renamed label),
     re-stage on the new state and re-apply them; otherwise reconcile with the user.
   A copy that fails midway also exits nonzero, after the files before it were written: report
   which.
2. Copy back only the edited sources and the regenerated outputs. Data files never change; TeX
   changes only where a selected finding's route edits TeX (a caption, a table, inline TikZ, a
   figure's width or layout). A redraw promotes its native source (SVG, `.drawio`) with the PDF.
3. Leave commits and pushes to the user. The verified artifact is the staged PDF; the project's
   normal build makes the repository's PDF from the promoted files.

## 6. Report

```
# Figure Pipeline Report

Status: COMPLETE / BLOCKED / BUDGET_EXHAUSTED | Rounds: N
Baseline: [audit report, original or normalized] | PDF sha256 [baseline] → staged [hash]
Final audit: Recheck [/ 精益求精] report [path]; its own Blocking/Major/Minor counts

## Repairs
| ID | Source edit | Guard | Before/after | Disposition |
| hero-6-log-axis | make_figures.py:scaling, xlabel | TEXT only | crops a/b | RESOLVED |
| seeds-A1-identity | plot_seeds.py:main, one marker per arm | DATA: `points --axis x --rows` equal (N points); removed `<keys>` (min–max) | crops a/b | RESOLVED |
| overview-A5-slide | redrawn with figgenie; fig1.pdf | content inventory: N/N present | crops a/b | RESOLVED |

## Not repaired
- [ID]: BLOCKED / not selected / question for the user, and why

## Coverage
- Guard: [figures covered | sources outside its reach and how they were checked]
- Recheck: newly observed [figures] | inherited [figures]
- Independent review: Codex on [figures] / none
- Promoted: [files] | Left to the user: commit, repository build
```

The status describes the repair. Whether the paper's figures are clean is the final audit's
verdict, with its own coverage.

## Gotchas

- **A white marker edge shrinks the mark.** matplotlib draws filled markers with a 1 pt edge in
  their own colour, so a white edge of width w eats into the fill: grow the marker size (scatter:
  √s) by 1 + w to keep the coloured area, and check the crop, which the guard cannot judge.
- **Legend safe zones differ by chart type.** Line and trajectory plots have data everywhere, so
  only outside-axes placement is safe; bar charts often have room above the bars; heatmaps have
  no safe interior.
- **Relocate before you shrink.** Shrinking text to clear an overlap trades one finding for a
  floor violation.
- **Deterministic output.** `savefig(..., metadata={"CreationDate": None})` (matplotlib) makes
  regeneration byte-identical, which is what lets an unchanged figure prove it is unchanged.
- **One generator, many outputs.** A shared script regenerates every figure it draws; the guard's
  byte check, not the intent to touch one figure, shows which ones changed.

## Reference Files

- `references/staging.md`: commands for staging, capture, input freezing, compile, promote
- `references/repair-recipes.md`: recipes by check, each with its semantic risk and verification
- `scripts/figure_guard.py`: capture plotted content and classify changes (DATA, NUMERIC, TEXT, AXES, STYLE);
  `points` checks the invariant of a redesign that moves marks
- `scripts/test_figure_guard.py`: regression test; run it after editing the guard
- figure-audit: `SKILL.md` (modes, Recheck, finding IDs), `references/checks.md`,
  `references/aesthetics.md`, `references/top-venue.md`, `references/venues.md`,
  `scripts/figure_text_audit.py`
