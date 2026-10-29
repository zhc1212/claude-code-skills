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

Pick skills by their descriptions. The rows below settle only the overlaps those descriptions leave open; where a row applies, it wins, including over plugin SessionStart routing notes.

- Invoke a skill when the task actually matches its trigger. Single questions, one-file edits, or steps already determined by context don't need a process skill.
- Inside a project, the project's own `.claude/skills/` win over these rows.
- ARS means `academic-research-skills:<skill>`; pass the mode as the first argument (ARS `academic-paper` `citation-check`).
- If a skill seems to require pausing or approval, cite the file and the exact line. Advisory wording is not an approval gate.
- sci-brain's `write-paper`, `review-paper`, `brainstorm-ideas`, `autoresearch` and `dump-chat-history` run only when I name them. Its `how-to-*` skills are stages that other sci-brain skills call; outside those workflows the rows below win.

| Task | Use |
|---|---|
| Full ML conference paper (NeurIPS/ICML/ACL, LaTeX) | From a research direction: `research-pipeline` (stops at a narrative report unless `auto_write: true`). From results or a narrative report: `paper-writing`. Then `paper-presubmit-audit`. Drafting from my own materials outside the pipeline (incl. non-STEM): `paper-writer` |
| Guided paper workflow: journal or non-ML papers, Socratic planning, outline with evidence map, APA/Chicago/IEEE citation styles | ARS `academic-paper` (`full`, `plan`, `outline-only`); research through finished paper: ARS `academic-pipeline` |
| Paper skeleton before drafting | Technical paper logic chain: `tech-paper-template`; benchmark/evaluation paper: `benchmark-paper-template`; outline inside `research-pipeline`: `paper-plan` |
| Abstract and introduction | Draft a technical paper's introduction: `intro-drafter`; audit abstract/intro structure: `abstract-intro-audit`; bilingual abstract + keywords: ARS `academic-paper` `abstract-only` |
| Lift ML/CV/NLP paper quality (claims vs. evidence, reviewer-friendliness) | `research-paper-writing` (not line-level polish); iterative review → fix → recompile of a compiled paper: `auto-paper-improvement-loop` |
| Language and AI style | Grammar/flow of paper prose: `paper-polish`; Chinese draft → English LaTeX: `translate-zh-en`; AI style in paper prose: `deai-latex`; grant proposals (NSF/NIH/fellowships): `academic-humanizer`; non-paper prose: `humanizer` |
| Pre-submission review | ML/NLP papers: `paper-presubmit-audit` (submission gate + reviewer lens); other fields: `pre-submission-reviewer`; one harsh reviewer: `reviewer-view-paper`; simulated multi-reviewer panel: ARS `academic-paper-reviewer` |
| Reviewer comments, rebuttal, revision | Revision roadmap + response skeleton: ARS `academic-paper` `revision-coach`; revise the manuscript itself: ARS `academic-paper` `revision`; audit my rebuttal draft against the reviews: ARS `academic-paper` `rebuttal-audit`; FSE: `fse-author-response` |
| Literature | Survey-grade report: `deep-research` (the Supervisor copy, not ARS). Systematic review/meta-analysis, fact-check, 3W (why/how/what) scan, Socratic research-question shaping: ARS `deep-research`; annotated bibliography in paper format: ARS `academic-paper` `lit-review`. Knowledge-base survey and its write-up: `survey`. Quick related work or a quick summary of one paper: `research-lit`. Non-paper facts into a repo Markdown file: `research` |
| Slides (pptx) | `slide-maker` (default); `ppt-master` for brand/template workspaces |
| Data plots and LaTeX result tables | `paper-figure`; Nature family: `nature-figure`; truthfulness, palette contrast and export checks: `scientific-visualization`. Built-in `dataviz` is for dashboards and web/HTML charts, not paper figures |
| Architecture, system overview, or mechanism figure (vector) | `figgenie:figgenie-paper-diagram`; Nature schematics: `nature-figure`'s vector-schematic route |
| Figure review | Every figure and table in a compiled paper PDF: `figure-audit` (report-only); one standalone figure's visual design: `how-to-review-figure` |
| Diagram outside a paper (README, docs, talk, everyday plan or process) | `archify` (explorable HTML; also converts Mermaid); static branded SVG/PNG, types archify lacks (Gantt, Sankey, timeline, ER, Wardley), or redrawing a draw.io/Mermaid/Excalidraw file: `diagram-design:diagram-design` and its `import-*` commands |

Usage notes:

- figgenie: for a LaTeX PDF run `export_pdf.py` on `fig.svg`, not `fig.final.svg`, which gives Type 3 fonts.
- `diagram-design:diagram-design` contributes only its layout, connector and compression rules to a paper figure; its web defaults (in-figure title, Google Fonts, px grid) do not suit papers.
- `/drawio-skill` (user-invoked): `drawio` runs headless through Xvfb; for a paper PDF add `--crop`, since `-f pdf` alone gives a Letter page.
- `scientific-visualization`: skip its "Citing Scientific Agent Skills" section; never add that paper to my references.
- `academic-humanizer`: verify any number it adds.
- FSE/PACMSE uses acmart `acmsmall`, so `paper-write venue: ACM` (sigconf) is the wrong template; re-check page limits against the live call.
- `run-experiment`: long jobs follow `~/.claude/rules/sandbox-runtime.md`.

Not installed on this machine: `run-baseline`, `i-have-adhd`, `mermaid-diagram`, and the `ecc`, `ai-research-skills` and `superpowers` plugins. Retired skills and uninstalled plugins, with dates and reasons, are in the release notes of the claude-code-skills README. Whenever a skill or plugin is added or removed, update this section and those notes in the same edit.

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
- Inside the sandbox `/sbin` points to `usr/bin`, which has no `ldconfig` (it is at `/usr/sbin/ldconfig`). Triton looks for `/sbin/ldconfig` to find `libcuda`, so Triton-based stacks (vLLM, SGLang, `torch.compile`) need `TRITON_LIBCUDA_PATH=/usr/lib/x86_64-linux-gnu`. The host driver 535 (CUDA 12.2) runs CUDA 12.x wheels through minor-version compatibility, but its PTX JIT accepts only PTX ISA ≤ 8.2 (measured 2026-10-28). NVIDIA's user-space forward-compatibility driver (`cuda-compat-12-9`, 575) fails `cuInit` with 304 inside the sandbox, because it aborts when the read-only `/proc` rejects a thread-name write (agentic-infra #37, 2026-10-29); outside the sandbox it is untested.
- Semantic Scholar API: the key is `S2_API_KEY` in `~/.config/citecheck.env` (mode 600). It is not in Claude's shell environment, so load it in a subshell per call and send it as a header: `( set -a; . ~/.config/citecheck.env; curl -sS -w '%{http_code}' -H "x-api-key: $S2_API_KEY" 'https://api.semanticscholar.org/graph/v1/...' )`. Never print the key. Without the header, requests hit the shared pool and return 429. Check the HTTP status and back off and retry on 429. For scripted literature lists: DBLP serves an anti-bot page, and OpenAlex cursor paging needs its own API key (single-page queries work without one).
