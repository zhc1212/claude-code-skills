# zhc-skills

Dr. Zhang's user-level Claude Code configuration and research workflow skills. This repository snapshots the active user-level skills, grouped by scenario, including third-party copies and their supporting resources. See the [snapshot notes](workspace/USER_LEVEL_SYNC.md), [source inventory](workspace/USER_SKILLS_MANIFEST.json), and [third-party licenses](workspace/third-party-licenses/).

## Skills by scenario

158 skills in 15 scenario folders, `skills/<scenario>/<skill>/`, plus 5 [project-scoped skills](#project-scoped-skills) in `project-skills/<project>/`. *User-invoked* skills run only as `/name`; the rest also load when a task matches.

[Ideas and literature](#ideas-and-literature) · [Experiments](#experiments) · [Drafting a paper](#drafting-a-paper) · [Figures and tables](#figures-and-tables) · [Revising a draft](#revising-a-draft) · [Review before submission](#review-before-submission) · [Second model as adversary](#second-model-as-adversary) · [Nature-family journals](#nature-family-journals) · [Software-engineering venues](#software-engineering-venues) · [Slides and reports](#slides-and-reports) · [General writing](#general-writing) · [Software engineering](#software-engineering) · [Planning and decisions](#planning-and-decisions) · [Agent setup, memory and knowledge](#agent-setup-memory-and-knowledge) · [Utilities](#utilities) · [Project-scoped skills](#project-scoped-skills)

### Ideas and literature

选题与文献. Find and test research ideas, read the literature, run the end-to-end research pipeline. `skills/ideas-literature/`

| Skill | Use it for |
|---|---|
| `idea-creator` | Generate and rank research ideas for a direction |
| `idea-discovery` | From a broad direction to validated, pilot-tested ideas |
| `idea-evaluator` | Score an idea on five dimensions and fit to the student |
| `idea-writer` | Ideas report or proposal-style research plan |
| `novelty-check` | Check an idea against recent literature |
| `research-lit` | Quick related work: find, read and summarise papers |
| `research` | Answer a question from primary sources into a Markdown note |
| `deep-research` | Survey-grade investigation with verified citations |
| `survey` | Survey a topic into a knowledge base |
| `survey-writer` | Survey or SOTA report from a populated knowledge base |
| `how-to-download-ref` | Add arXiv IDs or DOIs to a knowledge base (metadata, PDFs, BibTeX) |
| `hv-analysis` | Horizontal–vertical (synchronic/diachronic) analysis of a topic |
| `vibe-research-workflow` | Rules for AI-assisted coding, figures and writing that keep you in charge |
| `research-pipeline` | End to end: idea discovery → experiments → auto review → paper |
| `auto-review-loop` | Multi-round external review of a project, fixing until it passes |

### Experiments

实验. Run, monitor and analyse GPU experiments; publish models. `skills/experiments/`

| Skill | Use it for |
|---|---|
| `run-experiment` | Deploy experiments to local, remote, Vast.ai or Modal GPUs |
| `monitor-experiment` | Check progress and output of running experiments |
| `collect-results` | Aggregate results into comparison tables |
| `analyze-results` | Statistics, comparisons and insights from results |
| `experiment-bridge` | Implement an experiment plan, deploy it, collect first results |
| `upload-hf` | Upload and verify model artifacts on the Hugging Face Hub |

### Drafting a paper

写论文. Outline and draft a paper, translate a Chinese draft, compile LaTeX. `skills/drafting/`

| Skill | Use it for |
|---|---|
| `paper-plan` | Outline from review conclusions and results |
| `paper-write` | Draft LaTeX section by section from an outline |
| `paper-writing` | Pipeline: outline → figures → sections → compile |
| `paper-writer` | Draft prose from the author's own materials, any field |
| `intro-drafter` | Introduction along a six-paragraph flow |
| `tech-paper-template` | Logical skeleton of a technical paper |
| `benchmark-paper-template` | Structure of a benchmark or evaluation paper |
| `translate-zh-en` | Chinese draft → publication-quality English LaTeX |
| `paper-compile` | Compile LaTeX, fix errors, verify the PDF |

### Figures and tables

图表. Make plots and diagrams, then audit and fix them against venue rules and the top-venue bar. `skills/figures/`

| Skill | Use it for |
|---|---|
| `figure-audit` | Audit a compiled paper's figures: readability, venue rules, top-venue bar |
| `figure-pipeline` | Fix audited figures in a staged copy, prove the data unchanged, recheck |
| `figure-designer` | Design the core figures: motivating example, overview, results |
| `figure-spec` | Architecture and workflow diagrams from JSON to editable SVG |
| `paper-figure` | Plots and tables from experiment results |
| `paper-illustration` | AI-generated method illustrations (Gemini) |
| `paper-arch-diagram` | Image-model prompts for architecture figures |
| `experiment-plot-advisor` | Choose a chart type for experiment data |
| `gen-figure-caption` | English figure captions from Chinese descriptions |
| `gen-table-caption` | English table captions from Chinese descriptions |
| `scientific-visualization` | Truthful, accessible data figures; palette and export checks |
| `drawio-skill` | Editable draw.io diagrams with native export *(user-invoked)* |
| `drawio-reconstruction` | Rebuild a reference image as an editable draw.io file |
| `archify` | Architecture and flow diagrams as interactive HTML/SVG |
| `typst-drawing` | Typst + CeTZ figures, diagrams and plots |
| `how-to-review-figure` | Judge a figure's design against a rubric |

### Revising a draft

修改与润色. Paragraph- and paper-level revision: prose bar, defensive writing, notation, de-AI, polish. `skills/revision/`

| Skill | Use it for |
|---|---|
| `oral-paragraph-audit` | Audit or rewrite paragraphs against the top-venue prose bar |
| `defensive-writing-sweep` | List defensive (boundary) writing across a draft |
| `notation-audit` | Symbols, acronyms and equation numbers across a paper |
| `abstract-intro-audit` | Abstract and introduction structure against CVPR Highlight papers |
| `deai-latex` | Remove AI writing style from paper prose |
| `paper-polish` | Grammar, flow and tone, meaning preserved |
| `polish-english-paper` | Paragraph-level English polishing |
| `academic-humanizer` | Clarity and voice for papers and grant proposals |
| `shorten-latex` | Trim a paragraph to fit the page limit |
| `research-paper-writing` | Structure, flow and reviewer-facing presentation |

### Review before submission

投稿前审查. Whole-paper review, simulated reviewers, citation checks. `skills/review/`

| Skill | Use it for |
|---|---|
| `paper-presubmit-audit` | Submission gate and reviewer lens for ML/NLP papers |
| `pre-submission-reviewer` | Five-dimension pre-submission review, any field |
| `reviewer-view-paper` | One harsh top-venue reviewer |
| `citation-verification` | Verify references and catch fabricated ones |
| `auto-paper-improvement-loop` | Two rounds of external review, fixes and recompile |

### Second model as adversary

跨模型对抗. Claude and Codex (GPT) debate, critique and review independently. `skills/cross-model/`

| Skill | Use it for |
|---|---|
| `codex-debate` | Structured Claude–Codex debate on a decision |
| `codex-debug-pair` | Independent bug hypotheses from both models |
| `codex-experiment-critic` | Codex critiques an experiment plan before GPU hours |
| `codex-paper-adversary` | Codex reviews to reject, venue-calibrated |
| `codex-review` | Cross-model code review; Codex reads the repo |
| `codex-skill-optimizer` | Cross-model audit and improvement of a skill |
| `research-review` | Deep critical review of research by Codex |

### Nature-family journals

Nature 系列. Writing, review, figures, statistics and literature for Nature-family submissions. `skills/nature/`

| Skill | Use it for |
|---|---|
| `nature-academic-search` | Multi-source search and citation management |
| `nature-citation` | Find and verify supporting CNS-family literature |
| `nature-data` | Data and code availability statements |
| `nature-downloader` | Lawful full-text retrieval |
| `nature-experiment-log` | Structured lab-notebook entries |
| `nature-figure` | Figures in Python or R, and vector schematics |
| `nature-literature-pipeline` | Search → score → read → deliver → archive |
| `nature-paper-card` | Deep-reading card for one paper |
| `nature-paper-to-patent` | Chinese invention patent drafts from papers |
| `nature-paper2ppt` | Chinese PPTX from a paper |
| `nature-polishing` | Polish or translate prose in Nature register |
| `nature-proposal-writer` | Research proposals and opening reports |
| `nature-reader` | Aligned bilingual reader for a paper |
| `nature-ref-verifier` | Cross-check references field by field |
| `nature-response` | Responses to reviewers and revision packages |
| `nature-reviewer` | Mock peer review |
| `nature-shared` | Shared references read by the other nature skills |
| `nature-statistics` | Statistical reporting audit |
| `nature-writing` | Manuscript arguments and sections from evidence |

### Software-engineering venues

软件工程会议. ICSE/FSE/ASE papers; the FSE submission cycle end to end. `skills/se-venues/`

| Skill | Use it for |
|---|---|
| `fse-artifact-evaluation` | ACM artifact badges |
| `fse-author-response` | Rebuttals and Major Revision letters |
| `fse-camera-ready` | PACMSE camera-ready |
| `fse-experiments` | Subjects, baselines, statistics and effect sizes |
| `fse-related-work` | Position against the SE literature |
| `fse-reproducibility` | Data availability and runnable anonymised artifacts |
| `fse-review-process` | How FSE reviews work |
| `fse-submission` | HotCRP readiness, page budget, anonymity |
| `fse-supplementary` | Paper body versus artifact and appendix |
| `fse-topic-selection` | FSE or another SE venue? |
| `fse-workflow` | Timeline from venue fit to camera-ready |
| `fse-writing-style` | First-page contribution, RQ contracts, threats to validity |
| `se-research-paper-writing` | Papers for ICSE, FSE, ASE, ISSTA, TSE, TOSEM |

### Slides and reports

幻灯片与报告. Talk decks, deck audits, weekly reports. `skills/slides/`

| Skill | Use it for |
|---|---|
| `slide-maker` | Presentation-grade .pptx decks |
| `ppt-master` | Editable PPTX with brand, style and layout workspaces |
| `write-slides` | Typst + Touying decks for talks |
| `visual-audit-slides` | Layout audit of Quarto or Beamer decks |
| `weekly-report` | Weekly progress report in the QuAIR LaTeX template |

### General writing

通用写作. Articles and non-paper prose. `skills/writing/`

| Skill | Use it for |
|---|---|
| `humanizer` | Remove AI tells from non-paper prose |
| `khazix-writer` | Long-form WeChat articles in Khazix's style |
| `edit-article` | Restructure and tighten an article *(user-invoked)* |
| `writing-beats` | Assemble material into beats *(user-invoked)* |
| `writing-fragments` | Mine raw fragments *(user-invoked)* |
| `writing-shape` | Shape material into an article *(user-invoked)* |

### Software engineering

工程开发. TDD, code review, design, refactoring, repository setup. `skills/engineering/`

| Skill | Use it for |
|---|---|
| `code-review` | Review a diff against repo standards and the spec |
| `codebase-design` | Vocabulary for deep modules and seams |
| `design-an-interface` | Several radically different interface designs |
| `domain-modeling` | Glossary and ADRs for the domain |
| `tdd` | Test-first features and fixes |
| `prototype` | Throwaway prototype for a design question |
| `implement` | Build from a spec or tickets *(user-invoked)* |
| `qa` | Conversational bug reports filed as issues |
| `triage` | Move issues and PRs through triage *(user-invoked)* |
| `request-refactor-plan` | Refactor plan in tiny commits, filed as an issue |
| `improve-codebase-architecture` | Find deepening opportunities *(user-invoked)* |
| `resolving-merge-conflicts` | Resolve a merge or rebase conflict |
| `git-guardrails-claude-code` | Hooks that block dangerous git commands |
| `setup-pre-commit` | Husky, lint-staged, type checks and tests |
| `setup-matt-pocock-skills` | Configure a repo for these engineering skills *(user-invoked)* |
| `setup-ts-deep-modules` | dependency-cruiser for deep TypeScript modules *(user-invoked)* |
| `migrate-to-shoehorn` | Replace `as` in tests with shoehorn |
| `scaffold-exercises` | Course exercise directories |
| `ubiquitous-language` | DDD glossary from the conversation *(user-invoked)* |
| `wizard` | Bash wizard for steps only a human can do |
| `ask-matt` | Which engineering skill fits? *(user-invoked)* |

### Planning and decisions

规划与决策. Interrogate a plan, turn it into specs and tickets. `skills/planning/`

| Skill | Use it for |
|---|---|
| `grill-me` | Relentless interview to sharpen a plan *(user-invoked)* |
| `grill-with-docs` | The same interview, writing ADRs and a glossary *(user-invoked)* |
| `grilling` | Stress-test a plan or idea |
| `batch-grill-me` | Every open question at once, round by round *(user-invoked)* |
| `loop-me` | Interview for workflow specs *(user-invoked)* |
| `decision-mapping` | Loose idea → sequenced investigation tickets *(user-invoked)* |
| `wayfinder` | Work bigger than one session, as decision tickets *(user-invoked)* |
| `to-spec` | Conversation → spec on the issue tracker *(user-invoked)* |
| `to-tickets` | Plan → tracer-bullet tickets with dependencies *(user-invoked)* |
| `to-questionnaire` | An open decision → a questionnaire for someone else *(user-invoked)* |
| `how-to-flow` | Autonomous search toward one hard, testable goal |
| `teach` | Learn a new skill or concept *(user-invoked)* |

### Agent setup, memory and knowledge

智能体与知识管理. Write agent docs, hand off sessions, build research profiles and notes. `skills/agent-tools/`

| Skill | Use it for |
|---|---|
| `writing-for-agents` | Write skills, CLAUDE.md and AGENTS.md |
| `meta-optimize` | Propose skill and workflow changes from usage logs |
| `neat-freak` | Reconcile docs, rules and memory with the code at closeout |
| `handoff` | Handoff document for another agent *(user-invoked)* |
| `claude-handoff` | Hand the conversation to a background agent *(user-invoked)* |
| `create-advisor` | Advisor profile from conversation history |
| `import-dialog` | Import dialog files into advisor profiles |
| `how-to-dump-dialog` | Extract and classify research dialog from session logs |
| `soul-extraction` | Cluster trigger → reaction patterns in dialog reports |
| `know-me-better` | Learn your research style from your papers |
| `obsidian-vault` | Search and organise Obsidian notes |

### Utilities

工具. News, notifications, disk usage. `skills/utilities/`

| Skill | Use it for |
|---|---|
| `aihot` | Chinese AI news from aihot.news |
| `feishu-notify` | Feishu/Lark notifications |
| `storage-analyzer` | Read-only disk usage analysis (macOS, Windows) |

### Project-scoped skills

These serve one project, so they install into that project's `.claude/skills/`, not `~/.claude/skills/`, and stay out of `plugin.json`. `project-skills/<project>/`

| Skill | Project | Use it for |
|---|---|---|
| `propose` | SVD_LLM | Brainstorm a compression method or direction and file it as a GitHub issue |
| `run-gpu-experiment` | SVD_LLM | Launch a compress → finetune → eval run |
| `tutorial` | SVD_LLM | Walkthrough of SVD_LLM compression, evaluation and fine-tuning |
| `write-paper-section` | SVD_LLM | Write or improve one section of the SVD_LLM paper |
| `run-pipeline` | Lean-QIT-Agent | Lean theorem-proving pipeline (Putnam, IMO, QIT); the project tracks a newer copy, which takes precedence |

## Provenance and licenses

Provenance: 3 adapted hybrids (paper-write, paper-plan, paper-figure) carry PROVENANCE headers naming their upstream sources. `citation-verification` is an MIT-licensed copy from Galaxy-Dawn/claude-scholar, with source provenance and three EOF whitespace normalizations recorded separately. 20 third-party imports were removed 2026-07-19.

The snapshot also includes the installed engineering, Nature, FSE, slide, and writing suites. Third-party files retain their own licenses, including MIT, Apache-2.0, and CC BY-NC-SA-4.0; the bundle is not uniformly MIT licensed. Historical updates below describe earlier releases.

## Workspace Configuration

This repository tracks both the user-level snapshot and the earlier portable workspace example:

- [`workspace/USER_CLAUDE.md`](workspace/USER_CLAUDE.md) — the exact active `~/.claude/CLAUDE.md` snapshot, including user-specific routing and paths.
- [`workspace/CLAUDE.md`](workspace/CLAUDE.md) — project-level operating rules, with machine- and user-specific values replaced by placeholders.
- [`workspace/SKILL_SOURCES.md`](workspace/SKILL_SOURCES.md) — current source policy and the historical third-party workspace inventory.

Use `USER_CLAUDE.md` for a user-level restore and adapt `workspace/CLAUDE.md` for a project-level setup; see the [snapshot notes](workspace/USER_LEVEL_SYNC.md).

## Agent-scale review and monitoring — v1.0.25

Lessons from Anthropic's "Redesigning source control" post. codex-review's environment envelope gains a trust-boundary
axis: naming a caller, internal service or input file as trusted makes findings that only re-validate it immaterial.
monitor-experiment reads local `sandbox-job` jobs (`status`, `logs`, and the per-run training log found through the
job's `request.json`) and adds a Watch mode that runs under `/loop`, reports only per-tick changes, and ends the loop
once the job has a final result. `USER_CLAUDE.md` adds two rules: a project-specific correction becomes a "use X for Y"
rule in that project's agent doc, and changes to results-bearing code name the 1–3 lines to read. The manifest hashes
for both skills are updated.

## figure-audit exemplar cards — v1.0.24

figure-audit's exemplar comparison (`references/top-venue.md`) now picks its two or three bar exemplars from the
task-type index of a local exemplar-card file when one is present (each card gives the exemplar's figure contract, its
devices by B/G row and what not to copy), and diagram exemplars from the cards' diagram tier; without the file it falls
back to the B table's plots and FigGenie as before. RL-Reasoning joins the bar tier it was already cited from. The
manifest's `notation-audit` SKILL.md hash is corrected.

## Skill routing by scenario and project-scoped skills — v1.0.23

`workspace/USER_CLAUDE.md` rewrites the skill-routing tables: one row per scenario names a default skill and the
condition for each alternative, figures get their own table by figure type, and ARS (`academic-paper`,
`deep-research`, `sr-screener`, `academic-paper-reviewer`) has rows for planning, abstracts, citation checks, review
responses, format conversion and disclosure. The table was cross-checked against every installed skill and reviewed by
Codex. `propose`, `run-gpu-experiment`, `tutorial` and `write-paper-section` (SVD_LLM) and `run-pipeline`
(Lean-QIT-Agent) move to `project-skills/<project>/` and leave the user-level installation; `polish-english-paper`
drops its pointer to `write-paper-section`.

## figure-audit, figure-pipeline and new figure skills — v1.0.22

`figure-audit` now judges figures against the top-venue bar as well as the floor. Each figure gets a contract
(claim, task type, panel roles); `references/top-venue.md` holds bar conventions B1–B8 and generated-look signals
G1–G8 measured on the body figures of 16 award papers (NeurIPS 2025, ICLR 2026, ICML 2025–2026, ACL 2025–2026),
each citing the figures that show it, an exemplar-comparison step, and diagram readings of A1–A7. Venue rules add
ICML's alternative text and PDF tags and NeurIPS and ACL font embedding; Check 13 asks for the sampling unit,
pairing, estimator and interval method; Check 14 checks what a diagram claims. Exemplar crops are other authors'
figures and stay out of the repository.

`figure-pipeline` adds representation changes: a plot redesign names its invariant before the edit, and
`figure_guard.py points` checks it per series colour (`--rows` also per category row); a diagram redraw goes
through FigGenie, `nature-figure`'s vector route or `drawio-skill` against a content inventory. Each finding is
routed by source at intake, R generators go through the source-diff check, and the promote block exits nonzero
on a moved text, a concurrent change, an existing path or a failed copy. Four Codex review rounds; both
regression suites pass.

`nature-figure` follows upstream `e605b35` (vector-schematic workflow and SVG audit). New third-party skills:
`drawio-skill` (Agents365-ai, MIT, user-invoked) and `scientific-visualization` (K-Dense, MIT; its closing
citation section is removed, see `PROVENANCE.md`); licenses are in `workspace/third-party-licenses/`.
`abstract-intro-audit` adds check 9, contribution order and coverage. `workspace/USER_CLAUDE.md` routes figures
across these skills.

Skills now sit in 15 scenario folders (`skills/<scenario>/<skill>/`), listed in Skills by scenario and in
`plugin.json`; a clean plugin install loads all 163. Restore a skill by copying its folder flat into
`~/.claude/skills/`.

## notation-audit, defensive-writing-sweep, oral-paragraph-audit, paper-presubmit-audit — v1.0.21

Two new candidate-list skills from revising a paper; both edit nothing until the author picks candidates.
`notation-audit` checks a whole LaTeX paper's symbols, acronyms, coined names and equation numbers against four rules
(defined before use, defined once, one meaning per symbol, none the paper does not need) plus variants, typography,
figures, displays and prose. `scripts/symbol_inventory.py` follows `\input`, expands simple macros and lists every
symbol, acronym, coined name and numbered display; `evals/test_inventory.py` holds eleven deterministic regressions.
`defensive-writing-sweep` lists defensive (boundary) writing across a paper, section or appendix.

`oral-paragraph-audit` step 5, the recheck after revisions are applied, now runs whenever they are applied, including
after the author approves them in a later turn, covers text moved into another paragraph, and ends the report with a
`Recheck:` line that names each changed sentence, so a skipped recheck shows. On one paper it found 8 regressions in
211 applied hunks, each of which had passed its own edit check. `notation-audit` and `defensive-writing-sweep` apply
picked candidates through that step. `paper-presubmit-audit` Check 5 runs `notation-audit`; Checks 19–20 adapt
`pre-submission-reviewer`'s review dimensions (see its `PROVENANCE.md`), and it adds an anonymity sweep for
supplementary packages and a hidden-text scan script. `workspace/USER_CLAUDE.md` adds the routing rows.
Evaluation fixtures that quote a paper under review are excluded, as are generated results.

## figure-pipeline — v1.0.20

From further acceptance runs on a paper whose authors were editing the same figure sources concurrently:
`scripts/figure_guard.py` now records marker edge colour, box border colour and width, and annotation arrow style,
which it previously missed (each such change read as UNEXPLAINED; the regression test covers all three), and a line
drawn over points its colour already draws counts as a STYLE overplot, removed as well as added. The promote step
also hashes the TeX the Recheck reads and, when a concurrent edit blocks it, re-stages on the new commit and
re-applies the repair from a script. New recipes: white marker edges sized to keep the coloured area, no entity in a
neutral grey, and a colour-vision simulation before adopting a new entity colour.

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
[`skills/review/citation-verification/PROVENANCE.md`](skills/review/citation-verification/PROVENANCE.md).

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

A synced skill goes back to its own folder, `skills/*/<skill>/`. A new skill gets one scenario folder and a row in Skills by scenario; a new scenario folder also goes into `plugin.json`'s `skills` list (both copies). `shared-references/` is copied into every scenario folder whose skills read `../shared-references/`; change all copies together. Skills that read each other by relative path stay in one folder: the `nature-*` skills with `nature-shared`, `oral-paragraph-audit` with `deai-latex` and `defensive-writing-sweep`, `import-dialog` with `how-to-dump-dialog`.
