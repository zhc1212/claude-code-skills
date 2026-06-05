# Claude Code Skills

253 skills, 79 commands, 81 agents, 16 hooks, 4 rule sets for [Claude Code](https://claude.ai/code).

Organized around an academic ML research workflow — from literature search to camera-ready PDF — with cross-model collaboration (Claude + GPT-5.5), automated review loops, and full project management.

Built on [Everything Claude Code (ECC)](https://github.com/anthropics/claude-code) with plugins from [Superpowers](https://github.com/obra/superpowers-marketplace), [Anthropic](https://github.com/anthropics/skills), [OpenAI Codex](https://github.com/openai/codex-plugin-cc), [gstack](https://github.com/garrytan/gstack), and community repos.

## What's Different About This Collection

Most skill repos are loose collections. This one is **workflow-tested** across 6 months of daily use on a real ML research project (LLM compression via SVD). The skills are organized by how they chain together in practice, not by abstract categories.

Lessons learned:
- **Cross-model review catches real bugs.** GPT-5.5 reviews Claude's code (and vice versa) via Codex MCP. Different blindspots surface different issues. The `codex-debate` skill formalizes this into multi-round adversarial discussion with Toulmin argumentation and calibrated confidence.
- **Cross-model adversarial paper review finds what self-review misses.** `codex-paper-adversary` sends paper sections to GPT with a mandate to REJECT, grounded in real venue reviewer standards (Quality/Clarity/Significance/Originality). Claude evaluates each attack independently — the combination catches blind spots neither model finds alone.
- **Automated polish loops work.** `oral-paragraph-audit → deai-latex → paper-compile → repeat` reliably improves paper quality. The `auto-paper-improvement-loop` automates 2 rounds of GPT-5.5 review → Claude fix → recompile.
- **De-AI is a separate, critical step.** ML reviewers can spot AI-generated prose. `deai-latex` removes the telltale patterns (em dashes, semicolons, "notably", "leveraging", participial tails) that `nature-polishing` alone won't catch.
- **Figure quality breaks at LaTeX scaling.** Fonts look fine in matplotlib but become unreadable after `\includegraphics[width=0.48\textwidth]`. The `figure-audit → figure-pipeline` pair catches this before submission.
- **TDD delegation to Codex works.** Claude writes specs and reviews, Codex writes tests then implementation in gated phases. Different sessions prevent the test-writer from fitting tests to the implementation.
- **Experiment design review saves GPU weeks.** `codex-experiment-critic` catches confounders, missing baselines, and information leakage before expensive execution — one bad design cost us weeks on the P1.3 causal probe.

---

## Research-to-Submission Pipeline

```
① Ideation → ② Literature → ③ Experiments → ④ Figures → ⑤ Writing → ⑥ Polishing → ⑦ Review → ⑧ Submission
```

### ① Ideation

| Skill | Trigger | What it does |
|---|---|---|
| `idea-creator` | "找idea" | Generate and rank research ideas given a direction |
| `idea-discovery` | "找idea全流程" | Full pipeline: literature → idea generation → novelty check → review |
| `novelty-check` | "查新", "有没有人做过" | Verify idea novelty against recent literature |
| `brainstorming-research-ideas` | "研究方向" | Structured ideation frameworks for high-impact directions |
| `creative-thinking-for-research` | "creative thinking" | Cognitive science frameworks for CS/AI research ideation |

### ② Literature Review

| Skill | Trigger | What it does |
|---|---|---|
| `research-lit` | "find papers", "文献调研" | Search and analyze papers, summarize key ideas |
| `exa-search` | "exa search" | AI-powered web search with content extraction |
| `academic-deep-research` | "深度研究", "systematic review" | 13-agent pipeline (7 modes including PRISMA systematic review) |
| `nature-academic-search` | "学术搜索" | Academic literature search (Nature-style) |
| `nature-reader` | "读论文" | Full-paper Chinese-English side-by-side reader with figure/table awareness |

### ③ Experiments & Results

| Skill | Trigger | What it does |
|---|---|---|
| `run-gpu-experiment` | "跑GPU实验" | Deploy GPU experiments with `nvidia-smi` check, CUDA device selection |
| `run-experiment` | "跑实验" | Run ML experiments (local, remote, Vast.ai, Modal) |
| `monitor-experiment` | "check results" | Monitor running experiments, check progress |
| `collect-results` | "收集结果" | Aggregate results into comparison tables |
| `analyze-results` | "analyze results" | Compute statistics and generate insights |
| `experiment-bridge` | (auto) | Bridge idea discovery → implementation → review loop |
| `upload-hf` | "上传到HF" | Upload checkpoints/LoRA/tokenizers to HuggingFace Hub |

### ④ Figures & Tables

| Skill | Trigger | What it does |
|---|---|---|
| `experiment-plot-advisor` | "绘图推荐", "plot results" | Recommend chart type for conference paper + generate code |
| **`nature-figure`** | "画图", "Nature figure" | Submission-grade matplotlib/ggplot2 figures (sans-serif, TrueType, ≥7pt, PDF) |
| `paper-figure` | "作图" | Publication-quality figures from experiment data |
| `figure-spec` | "架构图", "pipeline图" | Deterministic vector diagrams from structured JSON → editable SVG |
| `paper-arch-diagram` | "框架图" | Architecture / framework diagram generation |
| `paper-illustration` | "AI插图" | AI illustrations via Gemini image generation |
| `gen-figure-caption` | "生成caption" | Generate figure captions |
| `gen-table-caption` | "表格标题" | Generate table captions |

**Figure quality pipeline** (catches issues before submission):

| Skill | Trigger | What it does |
|---|---|---|
| `figure-audit` | "检查图的质量" | Audit compiled PDF for overlapping legends, tiny labels, Type 3 fonts, clipped annotations |
| `figure-pipeline` | "修图流程" | Fix all audit findings: re-export, adjust scaling, replace fonts |

### ⑤ Writing

| Skill | Trigger | What it does |
|---|---|---|
| `paper-plan` | "写大纲" | Structured outline from experiment results |
| `write-paper-section` | "写论文段落" | Write or improve a single section (method, experiments, results) |
| `ml-paper-writing` | "写论文" | NeurIPS/ICML/ICLR/ACL templates, citations, checklists |
| `systems-paper-writing` | "写系统论文" | Systems venues (OSDI/SOSP/ASPLOS) blueprint |
| `research-paper-writing` | "improve writing" | Section-level writing quality: structure, flow, claim-evidence |
| `nature-writing` | "Nature风格" | Full Nature-style writing with section guides |
| `nature-polishing` | "润色" | Nature-leaning prose with Academic Phrasebank |
| `translate-zh-en` | "翻译" | Chinese academic draft → publication-quality English |

### ⑥ Polishing

| Skill | Trigger | What it does |
|---|---|---|
| **`oral-paragraph-audit`** | "检查段落" | 8-check audit: claim-first structure, density, transitions, de-AI, section role |
| **`deai-latex`** | "去AI味" | Remove AI patterns: watchlist words, em dashes, semicolons, participial tails |
| `humanizer` | "humanize" | Universal AI-trace removal (any text, not just LaTeX) |
| `polish-english-paper` | "polish" | Paragraph-level English grammar and style |
| `shorten-latex` | "缩短" | Compress paragraphs to fit page limits |
| `paper-compile` | "编译" | LaTeX → PDF with auto-error-fix |

**Recommended polish loop:** `oral-paragraph-audit → deai-latex → paper-compile → repeat`

### ⑦ Review

| Skill | Trigger | What it does |
|---|---|---|
| `reviewer-view-paper` | "模拟审稿", "帮我挑刺" | Single harsh reviewer, top-venue style |
| `academic-paper-reviewer` | "review my paper" | Multi-perspective: EIC + 3 peer reviewers + Devil's Advocate |
| `research-review` | "review research" | Deep critical review from GPT-5.5 via Codex MCP |
| `codex-review` | "codex review" | Send paper/code to GPT-5.5 for independent review |
| **`codex-paper-adversary`** | "codex审我的论文" | Cross-model hostile review: GPT finds reasons to REJECT, grounded in venue standards |
| `auto-paper-improvement-loop` | "自动改论文" | GPT-5.5 reviews → Claude fixes → recompile (2 autonomous rounds) |
| `auto-review-loop` | "review loop" | Codex reviews → Claude fixes → re-reviews until convergence |
| `nature-response` | "回复审稿" | Draft reviewer response letters |

### ⑧ Pre-Submission

| Skill | Trigger | What it does |
|---|---|---|
| **`paper-presubmit-audit`** | "投稿前检查" | 14-check audit: compilation, pages, anonymization, symbols, cross-refs, figures, numbers |
| `nature-citation` | "引用格式" | Citation formatting and compliance |
| `nature-data` | "数据报告" | Data presentation and statistical reporting |
| `visual-audit-slides` | "检查slides" | Adversarial layout audit for Quarto/Beamer decks |
| `nature-paper2ppt` | "做PPT" | Convert paper to Nature-style Chinese PPTX |
| `presenting-conference-talks` | "做slides" | Beamer + PPTX + speaker notes from paper |

### End-to-End Pipelines

| Skill | What it chains |
|---|---|
| `research-pipeline` | idea discovery → implementation → review loop → paper writing |
| `academic-pipeline` | research → write → integrity check → review → revise → re-review → finalize (10 stages) |
| `paper-writing` | paper-plan → paper-figure → paper-write → paper-compile → auto-improvement |
| `idea-discovery` | literature → idea generation → novelty check → research review |

---

## Cross-Model Collaboration (Claude + GPT-5.5)

All Codex skills use GPT-5.5 with xhigh reasoning via [Codex MCP](https://github.com/openai/codex-plugin-cc). Every skill follows a **blind independence protocol** — Codex never sees Claude's analysis until synthesis, preventing anchoring bias.

| Skill | Trigger | What it does |
|---|---|---|
| **`codex-debate`** | "codex debate", "和codex讨论" | Multi-round blind debate with Toulmin argumentation: independent positions → crux identification → steel-manning → consensus or documented disagreement. Evidence tiers and calibrated confidence throughout. |
| **`codex-tdd-implementer`** | "让codex写代码" | Two-phase TDD delegation: Claude writes spec + reviews, Codex writes tests (Phase A) then implementation (Phase B) in gated sessions. Risk-tiered quality gates with mutation-lite checking. |
| **`codex-paper-adversary`** | "codex审我的论文", "hostile review" | Standards-bound hostile review: two-axis attack schema (category + dimension), Fair Target Lock, 6 fatality gates, venue-calibrated scoring (NeurIPS 1-6 / ICLR 1-10), strongest rejection narrative, rebuttal gate. |
| **`codex-debug-pair`** | "codex debug", "codex一起debug" | Cross-model pair debugging: independent blind hypotheses → 3-bucket synthesis (both-flagged / Codex-only / Claude-only) → verification experiments → convergence or escalation. |
| **`codex-experiment-critic`** | "codex检查实验设计" | Experiment design blind critique: 9 categories (confounders, leakage, baselines, stats, ...) → APPROVE/REVISE/REDESIGN verdicts. Provisional mode for early-stage plans. |
| **`codex-skill-optimizer`** | "优化skill", "评估skill" | Meta-skill: domain research → blind debate → consensus → apply → 10-dimension audit scorecard. Used to optimize itself and all other codex skills. |
| `codex-review` | "codex review", "让codex看看" | Blind pre-scan + cross-check synthesis for code review |
| `auto-review-loop` | "review loop" | Codex reviews → Claude fixes → re-reviews until convergence |
| `auto-paper-improvement-loop` | "自动改论文" | GPT-5.5 reviews paper → Claude fixes → recompile (2 rounds) |
| `research-review` | "review research" | Deep critical review from GPT-5.5 |

---

## Infrastructure Skills

### Superpowers (12 skills)

Meta-workflow from [obra/superpowers](https://github.com/obra/superpowers-marketplace). Enforces discipline: plan before code, test before ship, verify before claim.

| Skill | When |
|---|---|
| `brainstorming` | Before any creative work |
| `writing-plans` | Before multi-step implementation |
| `test-driven-development` | Before writing code |
| `systematic-debugging` | Before proposing fixes |
| `verification-before-completion` | Before claiming done |
| `requesting-code-review` | After completing features |
| `dispatching-parallel-agents` | 2+ independent tasks |
| `executing-plans` | Running plans with quality gates |

### GSD — Get Stuff Done (68 skills)

Full project management inside Claude Code. Plan → execute → ship with atomic commits and state tracking.

| Stage | Key Skills |
|---|---|
| Start | `gsd-new-project`, `gsd-new-milestone`, `gsd-explore` |
| Plan | `gsd-discuss-phase`, `gsd-plan-phase`, `gsd-quick` |
| Execute | `gsd-execute-phase`, `gsd-fast`, `gsd-autonomous` |
| Quality | `gsd-code-review`, `gsd-validate-phase`, `gsd-secure-phase` |
| Ship | `gsd-ship`, `gsd-pr-branch`, `gsd-verify-work` |
| Track | `gsd-progress`, `gsd-stats`, `gsd-health` |
| Debug | `gsd-debug`, `gsd-forensics`, `gsd-undo` |

### Gstack v1.55.0 (from [garrytan/gstack](https://github.com/garrytan/gstack))

Developer tooling: code quality, review, debugging, retrospectives.

| Skill | What it does |
|---|---|
| `review` | Pre-landing PR review (SQL safety, trust boundaries) |
| `health` | Code quality dashboard → 0-10 score |
| `investigate` | Systematic root-cause debugging (no fixes without root cause) |
| `retro` | Weekly engineering retrospective |
| `plan-eng-review` | Lock in architecture before coding |
| `ship` | Ship workflow with quality gates |
| `browse` | Browser automation via Browserbase |

### GitHub Workflow

| Skill | Trigger | What it does |
|---|---|---|
| `check-issue` | "检查issue" | Review issue quality before implementation |
| `fix-issue` | "fix issue" | Analyze issue, implement fix, create PR |
| `fix-issue-batch` | "批量处理" | Batch-process open issues |
| `issue-to-pr` | "issue to PR" | Create PR from issue |
| `project-pipeline` | "pick an issue" | End-to-end: pick issue → implement → PR |
| `release` | "发版" | Bump version, tag, publish |

### Productivity

| Skill | What it does |
|---|---|
| `pua` | Motivational pressure mode when stuck |
| `caveman` | Ultra-compressed communication (−75% tokens) |
| `grill-me` | Stress-test a plan through relentless questioning |
| `tdd` | Test-driven development enforcement |
| `feishu-notify` | Send notifications to Feishu/Lark |
| `weekly-report` | Generate 周报 in QuAIR LaTeX template |

---

## Also Included

| Category | Count | Contents |
|---|---|---|
| Commands | 79 | Slash commands for code review, build, test, deploy across languages |
| Agents | 81 | Specialized subagents (planner, code-reviewer, security-reviewer, etc.) |
| Hooks | 16 | Pre/post hooks for commits, reviews, state tracking |
| Rules | 4 | Project conventions (Python style, Typst drawing, Codex defaults, user profile) |

---

## Installation

```bash
git clone https://github.com/zhc1212/claude-code-skills.git
cd claude-code-skills

# Install everything
cp -r skills/ ~/.claude/skills/
cp -r commands/ ~/.claude/commands/
cp -r agents/ ~/.claude/agents/
cp -r rules/ ~/.claude/rules/
cp -r hooks/ ~/.claude/hooks/

# Or install selectively
cp -r skills/deai-latex ~/.claude/skills/
cp -r skills/oral-paragraph-audit ~/.claude/skills/
cp -r skills/codex-debate ~/.claude/skills/
```

### Prerequisites

| Dependency | For | Install |
|---|---|---|
| [Codex MCP](https://github.com/openai/codex-plugin-cc) | Cross-model skills (codex-review, codex-debate, etc.) | `claude plugins install codex@openai-codex` |
| [Superpowers](https://github.com/obra/superpowers-marketplace) | Meta-workflow discipline | `claude plugins install superpowers@claude-plugins-official` |
| [gstack](https://github.com/garrytan/gstack) | Developer tooling | See gstack README |

## Credits

- [Everything Claude Code](https://github.com/anthropics/claude-code) — plugin infrastructure
- [Superpowers](https://github.com/obra/superpowers-marketplace) — meta-workflow skills
- [garrytan/gstack](https://github.com/garrytan/gstack) — development workflow
- [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) — Nature-style academic skills
- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) — academic pipeline
- [Orchestra-Research](https://github.com/Orchestra-Research/AI-Research-SKILLs) — ML paper writing
- [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) — section-level writing
- [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers) — matplotlib figure templates
- [runtsang/RebuttalStudio](https://github.com/runtsang/RebuttalStudio) — reviewer response generation
- [OpenAI Codex](https://github.com/openai/codex-plugin-cc) — cross-model collaboration

## License

MIT
