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

## Verifying and reporting

- Match verification effort to risk. Test-first for behaviour changes and reproducible bugs; skip tests for small reversible edits that would just restate the implementation. Run the checks the change touches, and widen only when failures or open risk call for it.
- If the repo has GitHub CI, run only the affected tests locally and treat CI's result as the one to report.
- Mark conclusions you didn't directly verify, and say what evidence would change them.
- When a check reproduced a bug, show its output before and after the fix, not just "tests pass". In long sessions, restate the goal in one line before reporting.
- Multi-step work: one-line plan, then execute without waiting. Put progress in the same message as the next action. Pause only when you need me or hit an ask-first action. A "Next:" line lists only things I have to do myself.
- Long tasks (many steps, or likely to survive a compaction): track them in `TASKS.md` in the working directory, one line per step, ticked off as done. Mirror the task tool if there is one. Re-read the file after a compaction. If another task's `TASKS.md` exists, use `TASKS-<topic>.md`. In git repos add `TASKS*.md` to `.git/info/exclude`. Delete the file when finished.

## How to answer

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
- Treat this table as the authority.
- If a skill seems to require pausing or approval, cite the file and the exact line. Advisory wording is not an approval gate.

| Task | Use |
|---|---|
| Full ML conference paper (NeurIPS/ICML/ACL, LaTeX) | `research-pipeline` orchestrates → `idea-discovery`, `paper-writing`, `paper-write`, `paper-presubmit-audit`. Drafting from my own materials outside the pipeline (incl. non-STEM): `paper-writer` |
| Lift ML/CV/NLP paper quality (claims vs. evidence, reviewer-friendliness) | `research-paper-writing` (not line-level polish) |
| Research ideas | `idea-discovery` (pipeline), `idea-creator`, `idea-evaluator`; `propose` if the output is a GitHub issue. |
| Pre-submission review | `pre-submission-reviewer`, `paper-presubmit-audit`; one harsh reviewer: `reviewer-view-paper` |
| Nature-family journals | `nature-writing`, `nature-reviewer`, `nature-figure`, `nature-literature-pipeline` |
| SE venues (FSE/ICSE/ASE/ISSTA/MSR/TSE/TOSEM) | Content, RQs, threats to validity: `se-research-paper-writing`. FSE mechanics: `fse-*` (`fse-writing-style`, `fse-experiments`, `fse-submission`, `fse-author-response`, `fse-artifact-evaluation`, …); re-check page limits against the live call. FSE/PACMSE uses acmart `acmsmall`, so `paper-write venue: ACM` (sigconf) is the wrong template |
| Figures | Generate: `paper-figure`. Fix visual issues: `figure-pipeline`. AI illustrations: `paper-illustration` |
| De-AI / style polish | Paper prose: `deai-latex` (owns the de-AI catalogue; `oral-paragraph-audit` Check 6 hands off to it). Grant proposals (NSF/NIH/fellowships): `academic-humanizer`, and verify any number it adds. Non-paper prose: `humanizer`. Also `khazix-writer`, `polish-english-paper`, `paper-polish` (grammar/flow, zh→en), `nature-polishing` (Nature register) |
| Literature | Survey-grade report: `deep-research` (use `academic-research-skills:deep-research` only inside an `/ars-*` run). Knowledge-base survey: `survey` → `survey-writer`. Quick related work: `research-lit`. Novelty: `novelty-check`. Non-paper facts into a repo Markdown file: `research` |
| Second model as adversary | `codex-debate`, `codex-paper-adversary`, `codex-debug-pair`, `codex-experiment-critic`, `research-review` |
| Code review | Cross-model, multi-round: `codex-review` (audit-only by default; prefer it when Codex should read the repo, and over `auto-review-loop`, which is for ML-paper scoring). Standards + spec review of a diff: local `code-review` |
| Debugging | `codex-debug-pair` for a second model's hypotheses |
| TDD | `tdd` |
| Writing skills | Design vocabulary: `writing-great-skills`. Inside a plugin: `plugin-dev:skill-development` |
| Slides | pptx: `slide-maker` (default) or `ppt-master` (brand/template workspaces). Typst: `write-slides`. Paper → Chinese deck: `nature-paper2ppt`. Quarto/Beamer layout audit: `visual-audit-slides` |
| TS/frontend engineering | mattpocock suite (`tdd`, `code-review`, `prototype`, …) |

Not installed on this machine: `diagnosing-bugs`, `run-baseline`, `i-have-adhd`, the `ecc`, `ai-research-skills` and `superpowers` plugins (superpowers uninstalled 2026-10-08). Disabled: the `claude-scientific-writer` and `planning-with-files` plugins (`TASKS.md` covers task tracking). Add a row here in the same edit whenever a skill or plugin is added or removed.

## Environment (this machine)

- The real home is `/home/huichengzhang`; inside the sandbox `/home/user` is a symlink to it, and Claude starts from the real path (project memory is keyed by it). Only the real path exists on the host, so don't hard-code `/home/user/...` into project code; use relative or configurable paths.
- Claude stays in its bwrap sandbox by default. Follow the user-level `~/.claude/rules/sandbox-runtime.md` for resource tasks and independent training jobs; do not default to a `claude-real` relaunch. Runtime details: `~/huicheng/config/claude-sandbox.md`. Distinguish proxy CONNECT rejection from a remote HTTP 403 before changing network rules. `BASH_ENV` re-exports `HOME` in every bash call, so `HOME=/tmp/x cmd` does not isolate; use `env -u BASH_ENV HOME=/tmp/x cmd`.
- The sandbox's privacy env vars switch off server feature flags, so a flag-gated feature (e.g. `/advisor`) can look missing. Check for a flag gate before concluding a feature doesn't exist.
- Conda env `compactifai` was relocated, so its entry-point shebangs point at the old path. Use `python3 -m pip` (not `pip`) and `python3 -m <tool>`.
- Plugins need `claude plugin marketplace add` + `claude plugin install`; editing settings.json by hand is not enough.
- The skills are a copy of https://github.com/zhc1212/claude-code-skills. Pulling that repo does not update `~/.claude/skills/`.
- Bash calls starting with `sleep N` need `timeout: (N + 30) * 1000`; for anything past ~560 s use `run_in_background` instead of polling.
