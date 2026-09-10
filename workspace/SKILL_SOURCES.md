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

Do not vendor these sources into `zhc-skills`: provenance, licenses, and update history remain upstream.

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
| `citation-verification` | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | `skills/citation-verification/` | The active `SKILL.md` matches this upstream clone byte for byte. Keep this third-party installation separate; the older adapted skill in this repository is retained. |

`run-pipeline` is absent from the active user-level skills directory. Its
repository copy is retained; absence from one installation does not retire it.
Other third-party installations remain external to this repository.
