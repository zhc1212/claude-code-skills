# Active Third-Party Skill Sources

This is the exposure manifest for the workspace that uses `zhc-skills` v1.0.10. It records the **66** third-party skill symlinks active as of 2026-07-20; upstream repositories remain their sole source of code.

| Upstream | Active skills | Count |
|---|---|---:|
| [mattpocock/skills](https://github.com/mattpocock/skills) | `ask-matt`, `batch-grill-me`, `claude-handoff`, `code-review`, `codebase-design`, `diagnosing-bugs`, `domain-modeling`, `edit-article`, `git-guardrails-claude-code`, `grill-me`, `grill-with-docs`, `grilling`, `handoff`, `implement`, `improve-codebase-architecture`, `loop-me`, `migrate-to-shoehorn`, `obsidian-vault`, `prototype`, `research`, `resolving-merge-conflicts`, `scaffold-exercises`, `setup-matt-pocock-skills`, `setup-pre-commit`, `setup-ts-deep-modules`, `tdd`, `teach`, `to-questionnaire`, `to-spec`, `to-tickets`, `triage`, `wayfinder`, `wizard`, `writing-beats`, `writing-fragments`, `writing-great-skills`, `writing-shape` | 37 |
| [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | `nature-academic-search`, `nature-citation`, `nature-data`, `nature-downloader`, `nature-experiment-log`, `nature-figure`, `nature-literature-pipeline`, `nature-paper-to-patent`, `nature-paper2ppt`, `nature-polishing`, `nature-proposal-writer`, `nature-reader`, `nature-ref-verifier`, `nature-response`, `nature-reviewer`, `nature-shared`, `nature-statistics`, `nature-writing` | 18 |
| [QuantumBFS/sci-brain](https://github.com/QuantumBFS/sci-brain) | `conversation-dump`, `download-ref`, `idea-writer`, `import-dialog`, `incarnate`, `paper-writer`, `researchstyle`, `soul-extraction`, `survey` | 9 |
| [kkkkhazix/khazix-skills](https://github.com/kkkkhazix/khazix-skills) | `neat-freak` | 1 |
| [blader/humanizer](https://github.com/blader/humanizer) | `humanizer` | 1 |

## Local Exposure Pattern

Clone each source under a project-local `.claude/skill-sources/` directory. Expose only directories containing `SKILL.md` as absolute symlinks under `.claude/skills/`; keep asset-only directories unlinked. Maintain a source manifest alongside those links and re-check it after every upstream update.

Keep the sources listed above external to `zhc-skills`. The explicit exception is the `citation-verification` copy documented below; any vendored copy must retain its upstream license and pinned provenance.

## User-level synchronization (2026-09-10)

The v1.0.11 update synchronizes 30 existing skills and their supporting files
from the active user-level `~/.claude/skills/` installation. Generated evaluation
outputs are excluded. The source clone lives at
`~/.claude/skill-sources/zhc-skills/`; pulling that clone does not update the
independent installed copies.

The table above is the historical 2026-07-20 workspace inventory, not a complete
inventory of the current user-level installation. One confirmed source override:

| Active skill | Upstream | Source path | Repository treatment |
|---|---|---|---|
| `citation-verification` | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | `skills/citation-verification/` | Vendored in v1.0.12 by explicit user request. All nine source files match upstream commit `6ed46dac03191c7a734f49ed48b41195012098ff`; the MIT license and [provenance](../skills/citation-verification/PROVENANCE.md) accompany the copy and document three EOF whitespace normalizations. This replaces the older adapted version retained in v1.0.11. |

`run-pipeline` is absent from the active user-level skills directory. Its
repository copy is retained; absence from one installation does not retire it.
Other third-party installations remain external to this repository.

## User-level synchronization (2026-09-29)

The v1.0.13 update synchronizes `deai-latex` and `oral-paragraph-audit` from the
active user-level installation. Six new `oral-paragraph-audit` evaluation
fixtures (08–13) contain unpublished text and stay local; generated evaluation
outputs remain excluded.

Third-party user-level installations were updated from their upstreams the same
day. They remain external to this repository; each installed copy matched its
previous upstream version exactly before the update.

| Upstream | Updated skills | Upstream commit |
|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer) | `humanizer` (v2.11.2 → v3.1.0) | `225a6f3` |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) | `academic-humanizer` (new, v0.3.3) | `94b88b2` |
| [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) | 17 `nature-*` skills | `8488081` |
| [QuantumBFS/sci-brain](https://github.com/QuantumBFS/sci-brain) | `create-advisor`, `how-to-download-ref`, `how-to-flow`, `how-to-review-figure`, `know-me-better`, `survey`, `write-slides` | `855fd57` |
| [kkkkhazix/khazix-skills](https://github.com/kkkkhazix/khazix-skills) | `aihot` | `b81ad3b` |
| [addsumtech/slides_maker](https://github.com/addsumtech/slides_maker) | `slide-maker` | `9fbe0a7` |

Already current: the 12 `fse-*` skills (brycewang-stanford/Awesome-Journal-Skills
`932eb23`) and `se-research-paper-writing`. Not updated: `ppt-master` (skipped),
and skills whose upstream path no longer exists (8 mattpocock skills moved to
deprecated or removed; `how-to-dump-dialog`, `idea-writer`, `import-dialog`,
`soul-extraction`, `survey-writer` removed from sci-brain), whose installed
copies are kept.
