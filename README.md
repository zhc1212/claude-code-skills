# zhc-skills

Dr. Zhang's user-level Claude Code configuration and research workflow skills. This repository snapshots the active user-level skills, including third-party copies and their supporting resources. See the [snapshot notes](workspace/USER_LEVEL_SYNC.md), [source inventory](workspace/USER_SKILLS_MANIFEST.json), and [third-party licenses](workspace/third-party-licenses/).

## What This Plugin Does

159 bundled skills (v1.0.15): 158 active user-level skills plus the retained `run-pipeline` skill. The original research bundle covers:

- **Cross-model debate** — structured Claude+Codex deliberation (codex-debate, codex-debug-pair, codex-experiment-critic, codex-paper-adversary, codex-skill-optimizer)
- **Experiment management** — GPU job orchestration on A800 (run-experiment, run-gpu-experiment, run-pipeline, monitor-experiment, collect-results, analyze-results, experiment-bridge, experiment-plot-advisor, upload-hf)
- **Paper writing (legacy)** — plan-to-submission pipeline (paper-plan, paper-write, paper-compile, write-paper-section, shorten-latex, audits, templates). Legacy: maintained third-party stacks (claude-scientific-writer, /ars-*, ai-research, nature-skills) are the primary paper stack; these remain for workflow-specific use.
- **Figure pipeline** — generation, audit, captioning (figure-pipeline, figure-designer, figure-spec, figure-audit, gen-figure-caption, gen-table-caption, typst-drawing)
- **Idea & research** — ideation, literature, novelty check (idea-creator/discovery/evaluator, novelty-check, research-lit, research-pipeline, research-review, vibe-research-workflow)
- **Utilities** — weekly-report, translate-zh-en, feishu-notify, tutorial, decision-mapping, meta-optimize

Provenance: 3 adapted hybrids (paper-write, paper-plan, paper-figure) carry PROVENANCE headers naming their upstream sources. `citation-verification` is an MIT-licensed copy from Galaxy-Dawn/claude-scholar, with source provenance and three EOF whitespace normalizations recorded separately. 20 third-party imports were removed 2026-07-19.

The snapshot also includes the installed engineering, Nature, FSE, slide, and writing suites. Third-party files retain their own licenses, including MIT, Apache-2.0, and CC BY-NC-SA-4.0; the bundle is not uniformly MIT licensed. Historical updates below describe earlier releases.

## Workspace Configuration

This repository tracks both the user-level snapshot and the earlier portable workspace example:

- [`workspace/USER_CLAUDE.md`](workspace/USER_CLAUDE.md) — the exact active `~/.claude/CLAUDE.md` snapshot, including user-specific routing and paths.
- [`workspace/CLAUDE.md`](workspace/CLAUDE.md) — project-level operating rules, with machine- and user-specific values replaced by placeholders.
- [`workspace/SKILL_SOURCES.md`](workspace/SKILL_SOURCES.md) — current source policy and the historical third-party workspace inventory.

Use `USER_CLAUDE.md` for a user-level restore and adapt `workspace/CLAUDE.md` for a project-level setup; see the [snapshot notes](workspace/USER_LEVEL_SYNC.md).

## figure-audit and figure-pipeline — v1.0.19

`figure-audit` adds an aesthetics layer (`references/aesthetics.md`: principles A1–A7 with evidence tags and
severity caps), a figure-set coherence check (Check 16), a script that measures rendered text size, scale and fonts
from the compiled PDF (`scripts/figure_text_audit.py`, with a regression test), and a Recheck mode that verifies a
repair. Reports now record the PDF's SHA-256, a rubric hash and permanent finding IDs. `fixes-and-antipatterns.md`
becomes `pitfalls.md`; the fix recipes move to figure-pipeline.

`figure-pipeline` is rewritten around that report: it repairs a staged copy of the paper, regenerates under
`scripts/figure_guard.py`, which sorts every change into DATA, NUMERIC, TEXT, AXES or STYLE and fails on changed plotted
values, verifies each fix with a figure-audit Recheck in at most two rounds, and checks the repository hashes before
writing back. Both skills were tested on fixtures and accepted on a real paper with a Codex cross-review.
`workspace/USER_CLAUDE.md` adds the note that Codex loads its own skill copies.

## writing-for-agents — v1.0.18

`writing-great-skills` is replaced by its upstream successor `writing-for-agents` (mattpocock/skills renamed
and restructured it), which the updated `ask-matt` refers to. `codex-skill-optimizer` and
`workspace/USER_CLAUDE.md` point to the new name.

## Upstream Skill Updates — v1.0.17

Synchronized from the user level on 2026-10-08:
- 23 third-party skills updated to their current upstream: `ppt-master` 6.7.0 (the local removal of
  `scripts/gemini_watermark_remover.py` is kept, see its `INSTALL_NOTE.txt`), `archify` 3.0, `slide-maker` 5.7.0,
  `aihot`, `nature-figure`, `nature-reviewer`, `nature-academic-search`, and 16 mattpocock skills (`ask-matt`,
  `claude-handoff`, `code-review`, `codebase-design`, `domain-modeling`, `grilling`, `handoff`, `implement`,
  `improve-codebase-architecture`, `setup-matt-pocock-skills`, `tdd`, `teach`, `to-tickets`, `triage`, `wayfinder`,
  `wizard`). Upstream heads are recorded in `workspace/USER_SKILLS_MANIFEST.json`.
- 21 skills that call Codex move from the Codex MCP tools to `codex exec` / `codex exec resume`, following
  `shared-references/codex-cli.md`.
- The superpowers plugin was uninstalled: `workspace/USER_CLAUDE.md` drops its routing rows, and
  `codex-debug-pair` and `codex-skill-optimizer` no longer point to `superpowers:*` skills.

## Skill Evaluation Fixes — v1.0.16

Synchronized `codex-debate`, `oral-paragraph-audit`, `deai-latex` and the new `shared-references/codex-cli.md`
from the user level on 2026-10-02, after a Claude–Codex evaluation of the three skills:
- `deai-latex`: `audit_style.py compare` now reports changed command names and flags removed negations and
  numbers or citation keys in a new order. Eight new tests cover these, plus `[fill: …]` placeholders and
  saved-baseline header lines. Step 1 names three reference types, the third being a co-written style
  reference the user picks, and reuses saved baselines from `~/.claude/deai-baselines/`. A PASS states what
  the passage was checked against.
- `oral-paragraph-audit`: severity follows the consequence for the reader, with anchors. Revised text is
  checked against the original before output, and `[fill]` stands only for missing facts. A detail another
  section may give is Needs verification. The eval oracle is corrected, the cache keys on the references,
  `deai-latex` and the model, and the advisory judge sees the task.
- `codex-debate`: every Codex prompt is read-only. The exchange is saved to disk, and decision-bearing
  citations are verified before synthesis. Round 3 or later needs a stated purpose. Codex calls go through
  the CLI (`shared-references/codex-cli.md`).

This is a partial sync. The CLI migration of the other Codex-calling skills is installed at the user level
but not included here.

## User-Level Snapshot — v1.0.15

Synchronized all 158 readable user-level skills and `~/.claude/CLAUDE.md` on 2026-10-01. The snapshot includes third-party skills, templates, scripts, and licenses; `slide-maker` is materialized from its symlink. The broken `run-baseline` symlink, nested Git metadata, caches, generated evaluation results, and unpublished `oral-paragraph-audit` fixtures 08–13 are excluded. Existing `run-pipeline` and project-level workspace configuration are retained. See [snapshot notes](workspace/USER_LEVEL_SYNC.md) for restore instructions and limitations.

## deai-latex Review Fixes — v1.0.14

Fixed two contradictions in `deai-latex` found in review:
- The step-5 word trace no longer reverts the plain word that replaces a flagged one, as long as it adds no new entity, property, relation, quantity, or hedge.
- Two worked examples invented technical detail; they now follow the preservation rules.

Baselines now record their provenance (named by the user, or tied to the author by history) and their scope (same section type first). The deai-mark evidence carries a not-peer-reviewed label. A stdlib `scripts/audit_style.py` computes the step-1 counts and allowances, printing each match in context. It also checks math, citation keys, references, and numbers across a rewrite, and flags new content words.

## User-Level Sync — v1.0.13

Synchronized `deai-latex` and `oral-paragraph-audit` from the active user-level
installation on 2026-09-29. `deai-latex` now audits paper prose against the
author's own writing (audit, adjudicate, minimal edit, verify meaning and style),
groups its catalogue by what the model is doing, and keeps its worked examples in
`references/examples.md`. `oral-paragraph-audit` carries the user-level revision
of its checks and references. Six new evaluation fixtures contain unpublished text
and stay local; generated evaluation outputs are excluded as before. Third-party
updates made the same day are recorded in
[`workspace/SKILL_SOURCES.md`](workspace/SKILL_SOURCES.md).

## Citation Verification Sync — v1.0.12

Replaced the older adapted `citation-verification` with the active user-level
version: `SKILL.md`, four reference documents, and the scripts README plus three
Python reference implementations. All nine source files match the pinned upstream
commit; packaging only removes extra EOF blank lines from three reference documents.
The accompanying MIT license, attribution, and hashes are in
[`skills/citation-verification/PROVENANCE.md`](skills/citation-verification/PROVENANCE.md).

## User-Level Sync — v1.0.11

Synchronized 30 existing skills and supporting references/evaluation fixtures
from the active user-level installation on 2026-09-10, including Codex model
configuration and writing/review guidance. Generated evaluation outputs are not
included. The active third-party `citation-verification` override and the
retained, locally absent `run-pipeline` are documented in
[`workspace/SKILL_SOURCES.md`](workspace/SKILL_SOURCES.md).

## Installation

Install from this repository as a Claude Code marketplace/plugin. The user-level skill copies are now included; independently installed plugins and parked skills are outside this snapshot. Avoid enabling duplicate copies of the same skills. For restoring the user-level configuration and skills directly, see [snapshot notes](workspace/USER_LEVEL_SYNC.md).

## Ecosystem (complements, does not duplicate)

The following describes the historical workspace ecosystem; plugin settings are not included in the snapshot.

Active plugins: ecc (engineering; blocker hooks disabled via ECC_DISABLED_HOOKS), claude-scientific-writer, academic-research-skills, ai-research-skills ×3, superpowers, planning-with-files, codex.
Skill-sources clones: mattpocock-skills, nature-skills, sci-brain-repo, khazix-skills.

## Update Ritual

Any content change here → bump `version` in BOTH `plugin.json` and `marketplace.json` (and their `.claude-plugin/` copies), commit, push — else the installed plugin cache silently stays stale. Cache rebuilds on next Claude Code session.
