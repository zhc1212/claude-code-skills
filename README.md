# zhc-skills

Dr. Zhang's research workflow skills for Claude Code. Third-party skills normally remain independent plugin installs or source clones. The explicitly vendored `citation-verification` copy includes its upstream license and pinned [provenance](skills/citation-verification/PROVENANCE.md); other external sources are recorded in [workspace/SKILL_SOURCES.md](workspace/SKILL_SOURCES.md).

## What This Plugin Does

60 bundled skills (v1.0.12; original provenance audit 2026-07-19):

- **Cross-model debate** — structured Claude+Codex deliberation (codex-debate, codex-debug-pair, codex-experiment-critic, codex-paper-adversary, codex-skill-optimizer)
- **Experiment management** — GPU job orchestration on A800 (run-experiment, run-gpu-experiment, run-pipeline, monitor-experiment, collect-results, analyze-results, experiment-bridge, experiment-plot-advisor, upload-hf)
- **Paper writing (legacy)** — plan-to-submission pipeline (paper-plan, paper-write, paper-compile, write-paper-section, shorten-latex, audits, templates). Legacy: maintained third-party stacks (claude-scientific-writer, /ars-*, ai-research, nature-skills) are the primary paper stack; these remain for workflow-specific use.
- **Figure pipeline** — generation, audit, captioning (figure-pipeline, figure-designer, figure-spec, figure-audit, gen-figure-caption, gen-table-caption, typst-drawing)
- **Idea & research** — ideation, literature, novelty check (idea-creator/discovery/evaluator, novelty-check, research-lit, research-pipeline, research-review, vibe-research-workflow)
- **Utilities** — weekly-report, translate-zh-en, feishu-notify, tutorial, decision-mapping, meta-optimize

Provenance: 3 adapted hybrids (paper-write, paper-plan, paper-figure) carry PROVENANCE headers naming their upstream sources. `citation-verification` is an MIT-licensed copy from Galaxy-Dawn/claude-scholar, with source provenance and three EOF whitespace normalizations recorded separately. 20 third-party imports were removed 2026-07-19.

## Workspace Configuration

This repository also tracks the portable parts of the workspace that uses these skills:

- [`workspace/CLAUDE.md`](workspace/CLAUDE.md) — project-level operating rules, with machine- and user-specific values replaced by placeholders.
- [`workspace/SKILL_SOURCES.md`](workspace/SKILL_SOURCES.md) — the historical 66-skill third-party workspace inventory, plus later source updates and the explicit citation-verification vendoring exception.

Copy and adapt these files into a project-level `.claude/` setup; do not treat the example infrastructure names as live configuration.

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

Install from this repository as a Claude Code marketplace/plugin, then enable third-party sources separately according to [`workspace/SKILL_SOURCES.md`](workspace/SKILL_SOURCES.md).

## Ecosystem (complements, does not duplicate)

Active plugins: ecc (engineering; blocker hooks disabled via ECC_DISABLED_HOOKS), claude-scientific-writer, academic-research-skills, ai-research-skills ×3, superpowers, planning-with-files, codex.
Skill-sources clones: mattpocock-skills, nature-skills, sci-brain-repo, khazix-skills.

## Update Ritual

Any content change here → bump `version` in BOTH `plugin.json` and `marketplace.json` (and their `.claude-plugin/` copies), commit, push — else the installed plugin cache silently stays stale. Cache rebuilds on next Claude Code session.
