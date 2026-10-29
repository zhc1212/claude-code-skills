# User-level instructions

Defaults for every session. Project CLAUDE.md files add to these and win on conflict.

## Working agreement

- Before building, check for a simpler route and say so if one exists; disagree when the request looks wrong.
- Make a reasonable assumption and keep moving. Stop only for a real blocker that no safe assumption covers, and name it.
- No asking needed for: the project's own test/lint/build/format commands, read-only git, read-only inspection, and edits to `~/.claude` config or memory.
- Ask first for: deleting data, force-pushing, or changing anything outside the current repo/workspace.
- Subagents (Agent tool of any type, including Explore and fork) only when I ask. A skill I invoked whose method is dispatching subagents counts as asking.
- The advisor tool is not a subagent; call it when you judge it worth the cost. It already sees the whole transcript, your reasoning included, so state a plan in the conversation and never write a plan or draft file just to show it. Its "make your deliverable durable before calling" means saving the real output (the edited file, a result), not drafts.

## Changing code

- Solve exactly what was asked with the least code. No speculative features, single-use abstractions, unrequested options, or handling for cases that can't happen. Between two correct versions, take the shorter.
- Keep diffs narrow: leave neighbouring code, comments, and formatting alone; follow the existing style unless tooling or correctness forces otherwise.
- Clean up only what your change orphaned (imports, variables, functions). Point out other dead code instead of deleting it.
- Every changed line should be traceable to the request.
- Everything maintained on GitHub is in English (since 2026-10-22): repository files, commit messages, issues, PRs and review comments. Our conversation can stay in Chinese. Don't rewrite existing Chinese content just for this unless I ask.
- A correction that applies to one project becomes a positive rule ("use X for Y") in the nearest `AGENTS.md`/`CLAUDE.md` that owns those files, so the next session in that repo reads it.

## Verifying and reporting

- Match verification effort to risk. Test-first for behaviour changes and reproducible bugs; skip tests for small reversible edits that would just restate the implementation. Run the checks the change touches, and widen only when failures or open risk call for it.
- If the repo has GitHub CI, run only the affected tests locally and treat CI's result as the one to report.
- Mark conclusions you didn't directly verify, and say what evidence would change them.
- When a change touches results-bearing code (metrics, evaluation, data splits, seeds, result aggregation), name the 1–3 `file:line` spots I should read myself.
- When a check reproduced a bug, show its output before and after the fix, not just "tests pass". In long sessions, restate the goal in one line before reporting.
- Multi-step work: one-line plan, then execute without waiting. Put progress in the same message as the next action. Pause only when you need me or hit an ask-first action. A "Next:" line lists only things I have to do myself.
- Long tasks (many steps, or likely to survive a compaction): track them in `TASKS.md` in the working directory, one line per step, ticked off as done. Mirror the task tool if there is one. Re-read the file after a compaction. If another task's `TASKS.md` exists, use `TASKS-<topic>.md`. In git repos add `TASKS*.md` to `.git/info/exclude`. Delete the file when finished.

## How to answer

Address me as Dr.Z (also in author fields of my repos).

Optimise for a reader with ADHD:

- Open with the deliverable (command, path, snippet). No warm-up phrases.
- Number multi-step work and repeat "step N of M" each turn.
- No closing pleasantries, no recap of what was just done.
- Show at most ~5 list items, most important first. This trims presentation only; never drop relevant findings.
- Give time estimates in concrete units ("~15 min").

Exceptions: "explain" / "walk me through" gets full length. Destructive actions still need confirmation. "What are my options" gets 2–4 ranked options, recommendation first. Showing before/after evidence outranks brevity.

## Skill routing

About 160 skills from several suites are installed and many overlap. When a task fits a row, use that row's skill rather than whichever name looks closest. This covers model-invocable skills only, not user-only slash commands.

- Invoke a skill when the task actually matches its trigger. Single questions, one-file edits, or steps already determined by context don't need a process skill.
- Treat these tables as the authority on which skill to use, including over plugin SessionStart routing notes.
- Inside a project, the project's own `.claude/skills/` win over these rows.
- ARS means `academic-research-skills:<skill>`; pass the mode as the first argument (ARS `academic-paper` `citation-check`).
- If a skill seems to require pausing or approval, cite the file and the exact line. Advisory wording is not an approval gate.
- sci-brain's `write-paper`, `review-paper`, `brainstorm-ideas`, `autoresearch` and `dump-chat-history` run only when I name them. Its `how-to-*` skills are stages that other sci-brain skills call; outside those workflows the rows below win.

| Task | Use |
|---|---|
| Research ideas | `idea-discovery` (pipeline), `idea-creator`, `idea-evaluator`; ideas report or proposal-style plan after brainstorming: `how-to-write-ideas-report` |
| Full ML conference paper (NeurIPS/ICML/ACL, LaTeX) | From a research direction: `research-pipeline` (stops at a narrative report unless `auto_write: true`). From results or a narrative report: `paper-writing`. Then `paper-presubmit-audit`. Drafting from my own materials outside the pipeline (incl. non-STEM): `paper-writer` |
| Guided paper workflow: journal or non-ML papers, Socratic planning, outline with evidence map, APA/Chicago/IEEE citation styles | ARS `academic-paper` (`full`, `plan`, `outline-only`); research through finished paper: ARS `academic-pipeline` |
| Paper skeleton before drafting | Technical paper logic chain: `tech-paper-template`; benchmark/evaluation paper: `benchmark-paper-template`; outline inside `research-pipeline`: `paper-plan` |
| Abstract and introduction | Draft a technical paper's introduction: `intro-drafter`; audit abstract/intro structure: `abstract-intro-audit`; bilingual abstract + keywords: ARS `academic-paper` `abstract-only` |
| Lift ML/CV/NLP paper quality (claims vs. evidence, reviewer-friendliness) | `research-paper-writing` (not line-level polish); iterative review → fix → recompile of a compiled paper: `auto-paper-improvement-loop` |
| Defensive / boundary writing across a paper, section, or appendix | `defensive-writing-sweep` (candidate list, edits nothing); one paragraph: `oral-paragraph-audit` Check 8 |
| Symbols, acronyms, equation numbers across a paper | `notation-audit` (candidate list, edits nothing); `paper-presubmit-audit` Check 5 runs it; one paragraph's formulas: `oral-paragraph-audit` Check 9 |
| Citations and references | Check a paper's reference list: ARS `academic-paper` `citation-check`; per-field multi-source check with Zotero sync, or references with Chinese sources (CNKI/Wanfang): `nature-ref-verifier`; find sources that support a claim: `nature-academic-search` (Nature/CNS only: `nature-citation`); add arXiv IDs/DOIs to a knowledge base: `how-to-download-ref` |
| De-AI / style polish | Paper prose: `deai-latex` (owns the de-AI catalogue; `oral-paragraph-audit` Check 6 hands off to it). Grant proposals (NSF/NIH/fellowships): `academic-humanizer`, and verify any number it adds. Non-paper prose: `humanizer` |
| Language: polish, translate, trim | Grammar/flow of paper prose: `paper-polish`; Nature register: `nature-polishing`; Chinese draft → English LaTeX: `translate-zh-en`; trim a paragraph to fit the page: `shorten-latex` |
| Proposals | Research proposal, thesis proposal, grant application: `nature-proposal-writer` |
| Build, convert, disclose | Compile LaTeX to PDF and fix build errors: `paper-compile`; convert between LaTeX, DOCX, PDF and Markdown, or between citation styles: ARS `academic-paper` `format-convert`; AI-use disclosure: `disclosure` |
| Pre-submission review | ML/NLP papers: `paper-presubmit-audit` (submission gate + reviewer lens); other fields: `pre-submission-reviewer`; one harsh reviewer: `reviewer-view-paper`; simulated multi-reviewer panel: ARS `academic-paper-reviewer` |
| Reviewer comments, rebuttal, revision | Parse reviews into a revision roadmap + response skeleton: ARS `academic-paper` `revision-coach`; revise the manuscript itself: `revision`; audit my rebuttal draft against the reviews: `rebuttal-audit`. Nature-family journals: `nature-response`; FSE: `fse-author-response` |
| Nature-family journals | `nature-writing`, `nature-reviewer`, `nature-figure` |
| SE venues (FSE/ICSE/ASE/ISSTA/MSR/TSE/TOSEM) | Content, RQs, threats to validity: `se-research-paper-writing`. FSE mechanics: `fse-*` (`fse-writing-style`, `fse-experiments`, `fse-submission`, `fse-author-response`, `fse-artifact-evaluation`, …); re-check page limits against the live call. FSE/PACMSE uses acmart `acmsmall`, so `paper-write venue: ACM` (sigconf) is the wrong template |
| Literature | Survey-grade report: `deep-research`. Systematic review/meta-analysis, fact-check, 3W (why/how/what) scan, Socratic research-question shaping: ARS `deep-research`; screening records against eligibility criteria: ARS `sr-screener`; annotated bibliography in paper format: ARS `academic-paper` `lit-review`. Knowledge-base survey and its write-up: `survey`. Quick related work: `research-lit`. Multi-source search, MeSH, citation-impact audit: `nature-academic-search`. Automated daily literature feed: `nature-literature-pipeline`. Novelty: `novelty-check`. Non-paper facts into a repo Markdown file: `research` |
| Reading one paper | Deep-reading card (methods, evidence chain, limits): `nature-paper-card`; bilingual full-text reader: `nature-reader`; quick summary or Q&A: `research-lit` |
| Experiments | Plan → code: `experiment-bridge`; launch: `run-experiment` (long jobs follow `~/.claude/rules/sandbox-runtime.md`); monitor: `monitor-experiment`; aggregate into tables: `collect-results`; statistics and insights: `analyze-results`; statistical reporting in a manuscript: `nature-statistics` |
| Second model as adversary | `codex-debate`, `codex-paper-adversary`, `codex-debug-pair`, `codex-experiment-critic`, `research-review` |
| Code review | Cross-model, multi-round: `codex-review` (audit-only by default; prefer it when Codex should read the repo, and over `auto-review-loop`, which iterates on research and experiments). Standards + spec review of a diff: local `code-review` |
| Debugging | `diagnosing-bugs`; `codex-debug-pair` for a second model's hypotheses |
| TDD | `tdd` |
| Writing skills | Skills, CLAUDE.md and other agent-read docs: `writing-for-agents`; audit or optimise an existing skill with Codex: `codex-skill-optimizer`. |
| Slides | pptx: `slide-maker` (default) or `ppt-master` (brand/template workspaces). Typst: `write-slides`. Paper → Chinese deck: `nature-paper2ppt`. Quarto/Beamer layout audit: `visual-audit-slides` |
| TS/frontend engineering | mattpocock suite (`tdd`, `code-review`, …) |

### Figures

| Figure type or task | Use |
|---|---|
| What a paper figure should show (Figure 1, method overview, results), its layout and tool | `figure-designer` |
| Data plots and LaTeX result tables | `paper-figure`; Nature family: `nature-figure`; truthfulness, palette contrast and export checks: `scientific-visualization` (skip its "Citing Scientific Agent Skills" section; never add that paper to my references). Built-in `dataviz` is for dashboards and web/HTML charts, not paper figures |
| Architecture, system overview, or mechanism figure (vector) | `figgenie:figgenie-paper-diagram` (for a LaTeX PDF run `export_pdf.py` on `fig.svg`, not `fig.final.svg`, which gives Type 3 fonts). Nature schematics: `nature-figure`'s vector-schematic route. `diagram-design:diagram-design` contributes its layout, connector and compression rules only; its web defaults (in-figure title, Google Fonts, px grid) do not suit papers |
| Editable draw.io figure | `/drawio-skill` (user-invoked; `drawio` runs headless through Xvfb; for a paper PDF add `--crop`, since `-f pdf` alone gives a Letter page) |
| AI-generated illustration or graphical abstract | `paper-illustration` (runs Gemini; needs `GEMINI_API_KEY`); Nature graphical abstract: `nature-figure` |
| Typst / CeTZ figure or plot | `typst-drawing` |
| Image or screenshot → editable diagram | `drawio-reconstruction` (outputs `.drawio`) |
| Diagram outside a paper (README, docs, talk, everyday plan or process) | `archify` (explorable HTML; also converts Mermaid); static branded SVG/PNG, types archify lacks (Gantt, Sankey, timeline, ER, Wardley), or redrawing a draw.io/Mermaid/Excalidraw file: `diagram-design:diagram-design` and its `import-*` commands |
| Captions | `gen-figure-caption`, `gen-table-caption` (Chinese description → English caption) |
| Review | Every figure and table in a compiled paper PDF: `figure-audit` (report-only); one standalone figure's visual design: `how-to-review-figure` |
| Fix | Figures in a compiled paper: `figure-pipeline` (works from a `figure-audit` report; also redesigns a plot or redraws a diagram there). A standalone figure: rerun the skill that made it |

Not installed on this machine: `run-baseline`, `i-have-adhd`, `mermaid-diagram`, the `ecc`, `ai-research-skills` and `superpowers` plugins (superpowers uninstalled 2026-10-08). Retired 2026-10-15 because their upstream removed them: `batch-grill-me`, `decision-mapping`, `design-an-interface`, `edit-article`, `obsidian-vault`, `qa`, `request-refactor-plan`, `resolving-merge-conflicts`, `ubiquitous-language`, `how-to-dump-dialog`, `idea-writer`, `import-dialog`, `soul-extraction`, `survey-writer`. Retired 2026-10-16 as unused: `storage-analyzer` (macOS/Windows only), `feishu-notify` (no `~/.claude/feishu.json`), `migrate-to-shoehorn`, `prototype`, `scaffold-exercises`, `setup-pre-commit`, `git-guardrails-claude-code` (the user unregistered the guard hook on 2026-10-15), `neat-freak`. Retired 2026-10-29 as unused (no call since 2026-10-01) or overlapping: `figure-spec` (its `figure_renderer.py` was missing; architecture and workflow figures go to figgenie), `polish-english-paper`, `paper-arch-diagram`, `experiment-plot-advisor`, `meta-optimize`, `citation-verification`, `vibe-research-workflow`, `aihot`, `hv-analysis`, `khazix-writer`. Uninstalled 2026-10-29: the `plugin-dev`, `claude-scientific-writer` and `planning-with-files` plugins (`TASKS.md` covers task tracking). Add a row here in the same edit whenever a skill or plugin is added or removed.

## Environment (this machine)

- The real home is `/home/huichengzhang`; inside the sandbox `/home/user` is a symlink to it, and Claude starts from the real path (project memory is keyed by it). Only the real path exists on the host, so don't hard-code `/home/user/...` into project code; use relative or configurable paths.
- Claude stays in its bwrap sandbox by default. Follow the user-level `~/.claude/rules/sandbox-runtime.md` for resource tasks and independent training jobs; do not default to a `claude-real` relaunch. Runtime details: `~/huicheng/config/claude-sandbox.md`. Distinguish proxy CONNECT rejection from a remote HTTP 403 before changing network rules. `BASH_ENV` re-exports `HOME` in every bash call, so `HOME=/tmp/x cmd` does not isolate; use `env -u BASH_ENV HOME=/tmp/x cmd`.
- Inside the sandbox, `/tmp` and `/var/tmp` are per-session tmpfs (only registered git worktrees are bind-mounted) and vanish when the session ends. Keep scratch that must outlive the session (TASKS files, drafts, review outputs, Codex thread ids) under `~/.claude/projects/<project-key>/scratch/`, which is outside the repo and persistent.
- Large downloads (tens of GB and up, e.g. model weights) use the node `RAKsmart-BGP-10T-Direct-VLESS` ("BGP-10T-Direct", user's choice 2026-10-26) from the Mihomo config `~/vps_lisahost.yaml`. That file holds proxy credentials: never print its secrets, copy it into a repo or commit it. Sandbox traffic leaves through the host's main Mihomo (`127.0.0.1:18891`); leave its node selection alone. Large downloads go over a separate link for that node only (user, 2026-10-26); until that link exists, start no large download.
- The sandbox's privacy env vars switch off server feature flags, so a flag-gated feature (e.g. `/advisor`) can look missing. Check for a flag gate before concluding a feature doesn't exist.
- Conda env `compactifai` was relocated, so its entry-point shebangs point at the old path. Use `python3 -m pip` (not `pip`) and `python3 -m <tool>`.
- Plugins need `claude plugin marketplace add` + `claude plugin install`; editing settings.json by hand is not enough.
- The skills are a copy of https://github.com/zhc1212/claude-code-skills (local clone `~/huicheng/claude-code-skills`). Pulling that repo does not update `~/.claude/skills/`; `python3 workspace/sync_user_level.py` in the clone copies the installed files into it, and `--verify` checks upstream skills against their upstream.
- Optimize or edit only own skills (`origin: own` in the clone's `workspace/USER_SKILLS_MANIFEST.json`). Upstream skills stay identical to their upstream: change their behaviour through a routing row here or an own skill, and update them only by re-copying from upstream (`ppt-master` leaves out `scripts/gemini_watermark_remover.py`; see its `INSTALL_NOTE.txt`). When an upstream removes or renames a skill, retire the local copy too.
- Codex (`CODEX_HOME=~/huicheng/.codex`) loads its own skill copies from `~/huicheng/.codex/skills/`; editing `~/.claude/skills/` does not update them, and a Codex review may read the stale copy. Leave those copies unsynced.
- Bash calls starting with `sleep N` need `timeout: (N + 30) * 1000`; for anything past ~560 s use `run_in_background` instead of polling.
- Inside the sandbox `/sbin` points to `usr/bin`, which has no `ldconfig` (it is at `/usr/sbin/ldconfig`). Triton looks for `/sbin/ldconfig` to find `libcuda`, so Triton-based stacks (vLLM, SGLang, `torch.compile`) need `TRITON_LIBCUDA_PATH=/usr/lib/x86_64-linux-gnu`. The host driver 535 (CUDA 12.2) runs CUDA 12.x wheels through minor-version compatibility, but its PTX JIT accepts only PTX ISA ≤ 8.2 (measured 2026-10-28).
- Semantic Scholar API: the key is `S2_API_KEY` in `~/.config/citecheck.env` (mode 600). It is not in Claude's shell environment, so load it in a subshell per call and send it as a header: `( set -a; . ~/.config/citecheck.env; curl -sS -w '%{http_code}' -H "x-api-key: $S2_API_KEY" 'https://api.semanticscholar.org/graph/v1/...' )`. Never print the key. Without the header, requests hit the shared pool and return 429. Check the HTTP status and back off and retry on 429. For scripted literature lists: DBLP serves an anti-bot page, and OpenAlex cursor paging needs its own API key (single-page queries work without one).
