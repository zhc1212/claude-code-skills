# Claude Code Skills Collection

A curated collection of **226 skills**, **68 slash commands**, **36 agents**, and **multi-language rules** for [Claude Code](https://claude.ai/code).

Built on top of [Everything Claude Code (ECC)](https://github.com/anthropics/claude-code) — the most comprehensive plugin system for Claude Code — with additional research, writing, and evaluation skills.

---

## Highlights

### Claude + Codex (GPT-5.4) Cross-Model Collaboration

One of the most powerful patterns in this collection: **use Claude (Opus/Sonnet) as the primary coding agent, with GPT-5.4 via Codex MCP as an independent reviewer and research partner.** Two models catch more bugs than one.

#### OpenAI Official Codex Plugin (`plugins/openai-codex/`)

Included in this repo is OpenAI's official **[codex-plugin-cc](https://github.com/openai/codex-plugin-cc)** — the bridge that enables cross-model collaboration:

| Component | What it does |
|---|---|
| `plugins/openai-codex/skills/codex-cli-runtime` | Core runtime: manages Codex CLI sessions, thread IDs, and result parsing |
| `plugins/openai-codex/skills/gpt-5-4-prompting` | Prompt engineering guide for GPT-5.4 — recipes, anti-patterns, prompt blocks |
| `plugins/openai-codex/skills/codex-result-handling` | Structured handling of Codex review output back into Claude's workflow |
| `plugins/openai-codex/agents/codex-rescue.md` | Delegate stuck tasks to Codex for a second implementation pass |
| `plugins/openai-codex/commands/review.md` | `/codex:review` — send code to GPT-5.4 for independent review |
| `plugins/openai-codex/commands/adversarial-review.md` | Adversarial review mode with structured schema output |
| `plugins/openai-codex/commands/rescue.md` | `/codex:rescue` — hand off debugging or investigation to Codex |
| `plugins/openai-codex/hooks/hooks.json` | Auto-trigger Codex review on git push via Stop hook |

#### Skills Built on Top of Codex

| Skill / Command | What it does |
|---|---|
| `skills/codex-review` | Send `git diff` to GPT-5.4 for independent code review. Supports file-level, branch-level, and full PR review. Triggered by `/codex-review`. |
| `skills/auto-review-loop` | Autonomous multi-round loop: Codex reviews → Claude fixes → Codex re-reviews, until quality converges. |
| `skills/auto-paper-improvement-loop` | GPT-5.4 xhigh reviews your paper → Claude implements fixes → recompile, for 2 rounds of autonomous polishing. |
| `commands/santa-loop.md` | Adversarial dual-review convergence: two independent model reviewers must both approve before code ships. |
| `commands/multi-plan.md` | Multi-model collaborative planning — Claude + Codex jointly design implementation strategy. |
| `commands/multi-execute.md` | Multi-model collaborative execution — parallel implementation with cross-checking. |
| `skills/deep-research-codex-*` | 5-skill deep research pipeline that delegates parallel research threads to Codex agents. |

### Superpowers System

The `superpowers:*` skills form a **meta-workflow layer** that orchestrates how you work, not just what you build:

| Skill | Purpose |
|---|---|
| `superpowers:brainstorming` | Structured ideation before any creative work — features, components, research directions |
| `superpowers:writing-plans` | Create step-by-step implementation plans before touching code |
| `superpowers:executing-plans` | Execute plans with progress tracking and quality gates |
| `superpowers:test-driven-development` | TDD enforcement: write tests first, then implement |
| `superpowers:systematic-debugging` | Root-cause analysis before proposing fixes |
| `superpowers:requesting-code-review` | Trigger code review after completing tasks |
| `superpowers:receiving-code-review` | Process review feedback systematically |
| `superpowers:verification-before-completion` | Final check before claiming work is done |
| `superpowers:dispatching-parallel-agents` | Parallelize independent tasks across sub-agents |
| `superpowers:finishing-a-development-branch` | Decide merge strategy when implementation is complete |
| `superpowers:using-git-worktrees` | Isolate feature work in git worktrees |

### Everything Claude Code (ECC)

This collection is built on ECC's plugin infrastructure:

- **`configure-ecc`** — Interactive installer wizard: selectively install skills, rules, hooks
- **`hooks/hooks.json`** — Pre/post tool-use hooks: auto-format, security scan, commit quality gates, cost tracking, session persistence
- **`scripts/`** — Orchestration scripts for tmux dev servers, worktree management, package manager detection
- **`agents/`** — 36 specialized sub-agents (code-reviewer, security-reviewer, tdd-guide, build-error-resolver, etc.)
- **`commands/`** — 68 slash commands for common workflows (`/plan`, `/verify`, `/tdd`, `/code-review`, etc.)

---

## Academic Research & Paper Writing

A complete pipeline from literature search to camera-ready PDF:

### Research & Ideation

| Skill | Trigger | What it does |
|---|---|---|
| `research-lit` | "find papers", "文献调研" | Search and analyze papers, find related work, summarize key ideas |
| `idea-creator` | "找idea", "brainstorm ideas" | Generate and rank research ideas given a broad direction |
| `idea-discovery` | "idea pipeline" | Full pipeline: literature → idea generation → novelty check → review |
| `novelty-check` | "查新", "novelty check" | Verify idea novelty against recent literature |
| `brainstorming-research-ideas` | "研究方向" | Structured ideation frameworks for high-impact directions |
| `creative-thinking-for-research` | "换个角度想" | Cognitive science frameworks for creative thinking |
| `academic-deep-research` | "deep research", "系统综述" | 13-agent pipeline, PRISMA-compliant systematic review |

### Writing Papers

| Skill | Trigger | What it does |
|---|---|---|
| `ml-paper-writing` | "写论文", "write paper" | **Main skill.** NeurIPS/ICML/ICLR/ACL/AAAI + systems venues. Templates, citations, checklists |
| `systems-paper-writing` | "写系统论文", "OSDI paper" | **Systems venues** (OSDI/SOSP/ASPLOS/NSDI/EuroSys). 12-page blueprint, paragraph-level structure, 4 writing patterns, LaTeX templates |
| `paper-plan` | "写大纲", "outline" | Structured outline from experiment results and review conclusions |
| `paper-write` | "写论文", "draft LaTeX" | Section-by-section LaTeX drafting from an outline |
| `write-paper-section` | "写论文段落", "write section" | Write or improve a single section (method, experiments, results) |
| `research-paper-writing` | "improve writing" | Improve ML/CV/NLP paper quality: structure, flow, reviewer perspective |
| `academic-paper` | "academic paper pipeline" | 12-agent pipeline (v2.4), forced APA7 formatting |
| `academic-pipeline` | "full pipeline" | 9-stage orchestrator: research → write → integrity → review → revise → finalize |
| `paper-writing` | "论文流水线" | Workflow 3: outline → figures → writing → compile, fully automated |
| `doc-coauthoring` | "协作写作", "一起写" | Staged collaboration: collect context → draft per-section → reader test |

### Figures & Tables

| Skill | Trigger | What it does |
|---|---|---|
| `experiment-plot-advisor` | "画图", "绘图推荐", "plot results" | Recommend chart type (19 academic chart types) + generate matplotlib code |
| `paper-figure` | "作图", "generate figure" | Publication-quality figures and tables from experiment results |
| `academic-plotting` | "论文配图" | Two modes: architecture diagrams (Gemini) + data plots (matplotlib) |
| `paper-arch-diagram` | "架构图", "framework diagram" | Generate architecture diagram prompts for image generation tools |
| `canvas-design` | "概念图", "示意图", "poster" | Design-philosophy-driven concept diagrams, output .png/.pdf |
| `gen-figure-caption` | "生成caption", "写图注" | Generate English figure captions from Chinese descriptions |
| `gen-table-caption` | "表格标题", "table caption" | Generate English table captions from Chinese descriptions |

### Language & Polishing

| Skill | Trigger | What it does |
|---|---|---|
| `polish-english-paper` | "润色", "polish", "grammar check" | Paragraph-level English polishing (grammar, style, academic tone) |
| `deai-latex` | "去AI味", "de-AI" | Remove AI writing traces from LaTeX text only |
| `humanizer` | "humanize", "让文字更自然" | **Universal** AI-trace removal for any text format (based on Wikipedia AI writing signals) |
| `shorten-latex` | "缩短", "shorten", "page limit" | Shorten paragraphs to fit page limits while preserving meaning |
| `translate-zh-en` | "翻译", "translate to English" | Chinese academic drafts → publication-quality English LaTeX |

### Review & Quality

| Skill | Trigger | What it does |
|---|---|---|
| `reviewer-view-paper` | "模拟审稿", "reviewer opinion" | Single harsh reviewer perspective, top-venue style |
| `academic-paper-reviewer` | "review my paper" | Multi-perspective: 1 EIC + 3 peer reviewers + 1 meta-reviewer |
| `research-review` | "review my research" | Cross-model deep review via Codex (GPT-5.5) |
| `auto-paper-improvement-loop` | "自动改论文", "auto improve" | GPT-5.5 review → Claude fix → recompile, 2 autonomous rounds |
| `auto-review-loop` | "review loop" | Multi-round: Codex reviews → Claude fixes → Codex re-reviews until convergence |
| `paper-compile` | "编译论文", "compile paper" | Compile LaTeX → PDF, auto-fix errors |

### Presentation & Documents

| Skill | Trigger | What it does |
|---|---|---|
| `presenting-conference-talks` | "做slides", "conference talk" | Generate Beamer slides + PPTX + speaker notes from paper PDF |
| `docx` | "Word文档", ".docx" | Create/edit/redline Word documents with tracked changes |

### Typical Workflows

```
Research:    idea-creator → novelty-check → research-lit
Write:       paper-plan → paper-write → paper-compile
Systems:     systems-paper-writing (structure) + ml-paper-writing (citations/format)
Figures:     experiment-plot-advisor → paper-figure → gen-figure-caption
Polish:      polish-english-paper → deai-latex / humanizer → shorten-latex
Review:      reviewer-view-paper → auto-paper-improvement-loop
Submit:      paper-compile → ml-paper-writing (checklist)
Present:     presenting-conference-talks
```

### Evaluation & Benchmarking

| Skill | What it evaluates |
|---|---|
| `orchestra-lm-evaluation-harness` | 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, ...) |
| `eval-harness` | Formal evaluation framework for Claude Code sessions |

---

## GSD — Get Stuff Done (68 skills)

The largest skill family in this collection. A complete project management system that runs inside Claude Code:

| Stage | Skills |
|---|---|
| **Start** | `gsd-new-project`, `gsd-new-milestone`, `gsd-explore` |
| **Plan** | `gsd-discuss-phase`, `gsd-research-phase`, `gsd-plan-phase`, `gsd-list-phase-assumptions` |
| **Execute** | `gsd-execute-phase`, `gsd-fast`, `gsd-quick`, `gsd-autonomous` |
| **Quality** | `gsd-code-review`, `gsd-code-review-fix`, `gsd-validate-phase`, `gsd-secure-phase`, `gsd-ui-review` |
| **Ship** | `gsd-ship`, `gsd-pr-branch`, `gsd-verify-work` |
| **Track** | `gsd-progress`, `gsd-stats`, `gsd-health`, `gsd-session-report` |
| **Manage** | `gsd-manager`, `gsd-workstreams`, `gsd-thread`, `gsd-pause-work`, `gsd-resume-work` |
| **Maintain** | `gsd-debug`, `gsd-forensics`, `gsd-undo`, `gsd-cleanup` |
| **Docs** | `gsd-docs-update`, `gsd-map-codebase`, `gsd-intel`, `gsd-milestone-summary` |

---

## All Skill Categories

| Category | Count | Key Skills |
|---|---|---|
| **GSD (Get Stuff Done)** | 68 | gsd-autonomous, gsd-plan-phase, gsd-execute-phase, gsd-ship, gsd-debug, gsd-map-codebase |
| **Research & Writing** | 38+ | academic-paper, deep-research, ml-paper-writing, research-lit, idea-creator, novelty-check |
| **Cross-Model (Codex)** | 10+ | codex-review, auto-review-loop, deep-research-codex-*, multi-plan/execute |
| **Superpowers** | 12 | brainstorming, writing-plans, TDD, debugging, code-review, verification |
| **Development Patterns** | 20+ | python/golang/rust/kotlin/swift-patterns, api-design, backend/frontend-patterns |
| **Testing** | 10+ | tdd-workflow, python-testing, e2e-testing, ai-regression-testing |
| **Code Review** | 10+ | security-review, python/go/rust/cpp/kotlin/flutter/java-reviewer |
| **PUA / Motivation** | 9 | pua, pua-en, pua-ja, pua-loop, mama, shot, pro, yes, caveman |
| **Design** | 4 | design-consultation, design-review, design-html, design-shotgun |
| **DevOps** | 5+ | docker-patterns, deployment-patterns, dmux-workflows, autonomous-loops |
| **Content & Media** | 10+ | article-writing, crosspost, x-api, presenting-conference-talks |
| **Security** | 5+ | security-review, security-scan, investigate |
| **Evaluation** | 7 | lm-evaluation-harness, bigcode-harness, nemo-evaluator, eval-harness |
| **Project Ops** | 5+ | health, retro, office-hours, plan-ceo/eng/design-review |

## Rules

Language-specific coding standards extending a common base:

```
rules/
├── common/       # Universal: coding-style, testing, security, git-workflow, agents
├── zh/           # Chinese translations of common rules
├── typescript/   ├── python/    ├── golang/    ├── rust/
├── kotlin/       ├── swift/     ├── php/       ├── cpp/
├── java/         ├── csharp/    └── perl/
```

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
cp -r scripts/ ~/.claude/scripts/
cp -r plugins/openai-codex/ ~/.claude/plugins/openai-codex/  # Codex plugin

# Or install selectively — just copy what you need
cp -r skills/codex-review ~/.claude/skills/
cp -r skills/ml-paper-writing ~/.claude/skills/
cp -r skills/academic-deep-research ~/.claude/skills/
cp -r rules/common ~/.claude/rules/
```

### Codex MCP Setup (for cross-model review)

To enable Claude + GPT-5.4 collaboration, install OpenAI's official [codex-plugin-cc](https://github.com/openai/codex-plugin-cc) (included in `plugins/openai-codex/`), and configure the Codex MCP server in your Claude Code settings.

## Credits

- [Everything Claude Code (ECC)](https://github.com/anthropics/claude-code) by Affaan Mustafa — the plugin infrastructure powering this collection
- [KDense](https://github.com/kdense) — scientific writing and literature review skills
- [Orchestra](https://github.com/orchestra-ai) — evaluation harness and ML paper writing skills

## License

MIT
