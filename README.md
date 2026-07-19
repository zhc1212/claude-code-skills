# zhc-skills

Dr. Zhang's own research workflow skills for Claude Code — originals only. Third-party skills are never copied in; they live as independent plugin installs or clones under `compact/.claude/skill-sources/` (manifest: `compact/.claude/skills/SOURCES.md`).

## What This Plugin Does

60 skills (v1.0.6, provenance-audited 2026-07-19):

- **Cross-model debate** — structured Claude+Codex deliberation (codex-debate, codex-debug-pair, codex-experiment-critic, codex-paper-adversary, codex-skill-optimizer)
- **Experiment management** — GPU job orchestration on A800 (run-experiment, run-gpu-experiment, run-pipeline, monitor-experiment, collect-results, analyze-results, experiment-bridge, experiment-plot-advisor, upload-hf)
- **Paper writing (legacy)** — plan-to-submission pipeline (paper-plan, paper-write, paper-compile, write-paper-section, shorten-latex, audits, templates). Legacy: maintained third-party stacks (claude-scientific-writer, /ars-*, ai-research, nature-skills) are the primary paper stack; these remain for workflow-specific use.
- **Figure pipeline** — generation, audit, captioning (figure-pipeline, figure-designer, figure-spec, figure-audit, gen-figure-caption, gen-table-caption, typst-drawing)
- **Idea & research** — ideation, literature, novelty check (idea-creator/discovery/evaluator, novelty-check, research-lit, research-pipeline, research-review, vibe-research-workflow)
- **Utilities** — weekly-report, translate-zh-en, feishu-notify, tutorial, decision-mapping, meta-optimize

Provenance: 4 adapted hybrids (paper-write, paper-plan, paper-figure, citation-verification) carry PROVENANCE headers naming their upstream sources. 20 third-party imports were removed 2026-07-19 (audit record: `compact/docs/debates/2026-07-19-workflow-optimization.md`).

## Installation

Installed locally via directory marketplace (`zhc-skills` entry in `~/.claude/settings.json` pointing at this directory).

## Ecosystem (complements, does not duplicate)

Active plugins: ecc (engineering; blocker hooks disabled via ECC_DISABLED_HOOKS), claude-scientific-writer, academic-research-skills, ai-research-skills ×3, superpowers, planning-with-files, codex.
Skill-sources clones: mattpocock-skills, nature-skills, sci-brain-repo, khazix-skills.

## Update Ritual

Any content change here → bump `version` in BOTH `plugin.json` and `marketplace.json` (and their `.claude-plugin/` copies), commit, push — else the installed plugin cache silently stays stale. Cache rebuilds on next Claude Code session.
