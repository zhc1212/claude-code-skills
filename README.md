# zhc-skills

Dr. Zhang's own research workflow skills for Claude Code — originals only. Third-party skills are never copied in; they live as independent plugin installs or clones under `compact/.claude/skill-sources/` (manifest: `compact/.claude/skills/SOURCES.md`).

## What This Plugin Does

60 original skills (v1.0.10, provenance-audited 2026-07-19):

- **Cross-model debate** — structured Claude+Codex deliberation (codex-debate, codex-debug-pair, codex-experiment-critic, codex-paper-adversary, codex-skill-optimizer)
- **Experiment management** — GPU job orchestration on A800 (run-experiment, run-gpu-experiment, run-pipeline, monitor-experiment, collect-results, analyze-results, experiment-bridge, experiment-plot-advisor, upload-hf)
- **Paper writing (legacy)** — plan-to-submission pipeline (paper-plan, paper-write, paper-compile, write-paper-section, shorten-latex, audits, templates). Legacy: maintained third-party stacks (claude-scientific-writer, /ars-*, ai-research, nature-skills) are the primary paper stack; these remain for workflow-specific use.
- **Figure pipeline** — generation, audit, captioning (figure-pipeline, figure-designer, figure-spec, figure-audit, gen-figure-caption, gen-table-caption, typst-drawing)
- **Idea & research** — ideation, literature, novelty check (idea-creator/discovery/evaluator, novelty-check, research-lit, research-pipeline, research-review, vibe-research-workflow)
- **Utilities** — weekly-report, translate-zh-en, feishu-notify, tutorial, decision-mapping, meta-optimize

Provenance: 4 adapted hybrids (paper-write, paper-plan, paper-figure, citation-verification) carry PROVENANCE headers naming their upstream sources. 20 third-party imports were removed 2026-07-19.

## Workspace Configuration

This repository also tracks the portable parts of the workspace that uses these skills:

- [`workspace/CLAUDE.md`](workspace/CLAUDE.md) — project-level operating rules, with machine- and user-specific values replaced by placeholders.
- [`workspace/SKILL_SOURCES.md`](workspace/SKILL_SOURCES.md) — the 66 third-party skills currently exposed in the workspace, recorded as upstream repositories and symlink targets. Their source is never vendored here.

Copy and adapt these files into a project-level `.claude/` setup; do not treat the example infrastructure names as live configuration.

## Installation

Install from this repository as a Claude Code marketplace/plugin, then enable third-party sources separately according to [`workspace/SKILL_SOURCES.md`](workspace/SKILL_SOURCES.md).

## Ecosystem (complements, does not duplicate)

Active plugins: ecc (engineering; blocker hooks disabled via ECC_DISABLED_HOOKS), claude-scientific-writer, academic-research-skills, ai-research-skills ×3, superpowers, planning-with-files, codex.
Skill-sources clones: mattpocock-skills, nature-skills, sci-brain-repo, khazix-skills.

## Update Ritual

Any content change here → bump `version` in BOTH `plugin.json` and `marketplace.json` (and their `.claude-plugin/` copies), commit, push — else the installed plugin cache silently stays stale. Cache rebuilds on next Claude Code session.
