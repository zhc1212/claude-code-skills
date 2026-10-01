# CLAUDE.md

User-level defaults. Merge with project-specific instructions as needed.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear and no assumption is safe, stop and name the blocker. Do not stop for questions an assumption can cover.

Standing permission: run the project's own test, lint, build, and formatting commands, plus read-only git and read-only inspection, without asking. Ask only before external or destructive actions: deleting data, force-pushing, or changing anything outside the current repository or workspace (editing `~/.claude` config and memory is in scope).

Subagents: don't spawn one (Agent tool, any type, including Explore and fork) unless the user asks for it. Do the work in the main session instead. A skill the user invoked that dispatches subagents as its method counts as asking.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- Prefer the shorter version when both are correct.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently, subject to required tooling and correctness.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Scale verification to impact. Write tests first for behavioral changes and reproducible defects, not for every edit — skip tests for reversible, low-impact changes that would only mirror the implementation. Run the checks the change actually affects; broaden or repeat only when new changes, failures, or unresolved risk justify it.

When the repo has GitHub CI, run only the tests the change touches locally; CI owns the full suite, and its verdict is the one to report.

Two reporting rules:
- When a conclusion rests on something you did not directly verify, say so and name what evidence would overturn it.
- If you ran a check that reproduced the defect, show its output before and after the fix — not just "tests pass". On long sessions, restate the current goal in one line before reporting.

For multi-step work, state the plan in one line, then execute it without waiting for confirmation. When a step does not need my input, keep going: put status notes (including "step N of M") in the same message as your next action. Stop and ask only when you cannot continue without me, or before the actions listed in §1. A "Next:" line is for actions only I can take; if you can take it, take it.

For long tasks (many steps, or likely to outlast a context compaction), keep the checklist in `TASKS.md` in the working directory: one line per step, ticked as each finishes. If a task tool is available, the file mirrors it rather than adding a second list to narrate. After a compaction, re-read it instead of the scrollback. If a `TASKS.md` for another task already exists, use `TASKS-<topic>.md`. In a git repo, add `TASKS*.md` to `.git/info/exclude` so it never gets committed; delete the file when the task is done.

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Output Shape

**Lead with the answer. The reader has ADHD.**

The `i-have-adhd` skill's full ruleset is injected every session by its SessionStart hook, gated on `~/.claude/.i-have-adhd-always`. The lines below are the durable subset — they hold for subagents and any context the hook misses:

- First line is the action: command, path, or snippet. No "Let me...", "Great question", "I'll now...".
- Number multi-step work and restate "step N of M" each turn; working memory does not survive a message boundary.
- No closers ("Hope this helps", "Let me know if..."), no recap of what you just did.
- Cap visible lists at ~5 items, most relevant first. Presentation only — never drop relevant findings from analysis, search, or tool results.
- Time estimates in concrete units ("~15 min if tests cover this"), not "some work".

Overrides: "explain" or "walk me through" gets full length; destructive actions still get confirmation; "what are my options" gets 2–4 ranked options with the recommendation first. Section 4 outranks brevity — when a check reproduced the defect, show its output.

## 6. Skill Routing

~158 skills are installed from multiple suites with overlapping triggers. When a task matches a row below, prefer the designated suite; don't pick by fuzzy name match. Rows govern model-invocable skills only; user-only slash commands (`disable-model-invocation: true`) are out of scope.

Invoke a skill when the task matches its trigger, not when a match is merely possible. A single question, a one-file edit, or a step already determined by what you just read needs no process skill. `using-superpowers`' "1% chance → you MUST invoke" is scaffolding for weaker models; this paragraph and the rows below override it. This also overrides its plan-mode brainstorming gate — brainstorm only when the design is genuinely open. It still cedes to user instructions, and the rows decide every head-to-head between a superpowers process skill and a local skill.

Most installed skills reach the session as a bare name, with no description attached. So this table is the routing source of truth, not a tiebreaker, and a bare name is never grounds to rule a skill out — read its SKILL.md before deciding it doesn't fit.

If a skill makes you pause, ask permission, or leave authorized work unfinished, name the file, quote the instruction, and say how it applies. Do not manufacture an approval requirement out of advisory wording.

| Task | Designated suite / entry points |
|---|---|
| ML conference paper, full pipeline (NeurIPS/ICML/ACL, LaTeX) | zhc suite: `research-pipeline` (orchestrator) → `idea-discovery` / `paper-writing` / `paper-write` / `paper-presubmit-audit`. `paper-writer` (active, not sci-brain's) drafts from the author's own materials outside the pipeline, incl. non-STEM |
| Improve ML/CV/NLP paper quality (reviewer-friendly, claim-support, self-review) | `research-paper-writing` — the quality-lift step, not line-level grammar polish |
| Find / evaluate research ideas | `idea-discovery` (pipeline), `idea-creator`, `idea-evaluator`; `propose` when the outcome is a GitHub issue. `superpowers:brainstorming` is for non-research feature work only, never for paper ideas |
| Paper review / pre-submission check | `pre-submission-reviewer`, `paper-presubmit-audit`, `reviewer-view-paper` (single harsh reviewer) |
| Nature-family journal submission | nature suite: `nature-writing` / `nature-reviewer` / `nature-figure` / `nature-literature-pipeline` |
| SE conference/journal paper (FSE, ICSE, ASE, ISSTA, MSR, TSE, TOSEM) | Section drafting and claim-evidence alignment → `se-research-paper-writing` (Tool Paper vs Empirical Study, RQ map, Threats to Validity). FSE venue mechanics → `fse-*` pack (`fse-writing-style`, `fse-experiments`, `fse-submission`, `fse-author-response` for the PACMSE Major Revision, `fse-artifact-evaluation`, etc.; re-verify page limits against the live call). Note FSE/PACMSE is acmart `acmsmall` single-column, so `paper-write venue: ACM` (sigconf) is the wrong template |
| Paper figures | `paper-figure` (generate), `figure-pipeline` (fix visual issues), `paper-illustration` (AI illustrations) |
| Style polish / de-AI writing | Split by scope, not by trigger word: paper prose (LaTeX or plain) → `deai-latex` (sole owner of the de-AI catalogue; `oral-paragraph-audit` Check 6 delegates to it). Grant proposals (NSF Project Summary/Description, NIH Specific Aims, fellowships) → `academic-humanizer`; it does not take papers, theses, or rebuttals from `deai-latex`, and its claim-evidence edits can add numbers the source lacks, so check every number it introduces. Any non-paper prose → `humanizer`, even when the ask is "de-AI". Also `khazix-writer`, `polish-english-paper`, `paper-polish` (grammar/flow plus zh→en rewrite at submission quality), `nature-polishing` (Nature register only) |
| Deep literature research | ARS plugin `/ars-*`; local `deep-research` for a survey-grade report, `academic-research-skills:deep-research` only inside an ARS run. Knowledge-base survey → `survey` then `survey-writer`; quick related-work lookup → `research-lit`; idea novelty → `novelty-check`; non-paper fact gathering into a repo Markdown file → `research` |
| GPT/codex as adversary | `codex-debate`, `codex-paper-adversary`, `codex-debug-pair`, `codex-experiment-critic`, `research-review` |
| Cross-model code review, rounds until it ships | `codex-review` — audit-only by default; blocking is decided by oracle + materiality, not by testability, and the rest goes to a ledger. Prefer over the local `code-review` (single-model, single-round) when Codex should read the repo itself, and over `auto-review-loop` (ML-paper scoring loop) for anything code |
| Standards + spec review of a diff | local `code-review` (two-axis, parallel sub-agents). The `code-review:code-review` plugin is disabled; `pr-review-toolkit:review-pr` is routed away |
| Debugging | `superpowers:systematic-debugging` for the loop; `codex-debug-pair` when a second model's hypotheses help; `diagnosing-bugs` is parked |
| Test-driven development | `tdd` for TS/frontend; `superpowers:test-driven-development` everywhere else |
| Writing / editing a skill | `writing-great-skills` for design vocabulary; `superpowers:writing-skills` for the verify-before-deploy loop; `plugin-dev:skill-development` only inside a plugin |
| Slides | pptx → `slide-maker` (default) or `ppt-master` (brand/template workspaces); Typst → `write-slides`; paper → Chinese deck → `nature-paper2ppt`; Quarto/Beamer layout audit → `visual-audit-slides` |
| TS/frontend engineering | mattpocock suite: `tdd`, `code-review`, `prototype`, etc. |

Parked duplicates live in `~/.claude/skills-parked/` (not loaded; `mv` back to restore): sci-brain's copies of `paper-writer`/`paper-reviewer`/`brainstorm-ideas`/`autoresearch*` (the active `paper-writer` is a different skill), `diagnosing-bugs`, plus `slide-maker-4.8.0.bak`. "Routed away" means still loaded and listed, but a row above names the skill to use instead.

## 7. Environment

Auto-memory is keyed by launch directory, so the user-level environment facts below are invisible to sessions started in a sub-repo. Before acting, read the matching file in `~/.claude/projects/-home-huichengzhang-huicheng/memory/`:

| Before... | Read | Short version |
|---|---|---|
| non-interactive `claude`, pip/conda installs, Codex launches | `claude-proxy-and-wrapper.md` | `CLAUDE_WRAPPER_ASSUME_Y=Y claude …`; unset proxy vars for installs from domestic mirrors |
| editing settings.json, plugins, MCP, advisor | `claude-code-settings-and-plugins.md` | plugins need `claude plugin install`; hand-editing is not enough |
| adding, pulling, or parking a skill | `skill-suite-provenance.md` | update §6 in the same edit |

A Bash call that starts with `sleep N` needs `timeout: (N + 30) * 1000` in the same call; the default 120 s timeout kills the sleep, not the job. Past `sleep 560`, use `run_in_background` instead of polling.
