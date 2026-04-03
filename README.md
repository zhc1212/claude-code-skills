# Claude Code Skills Collection

A curated collection of **191 skills**, **68 slash commands**, **36 agents**, and **multi-language rules** for [Claude Code](https://claude.ai/code).

Built on top of [Everything Claude Code (ECC)](https://github.com/anthropics/claude-code) — the most comprehensive plugin system for Claude Code — with additional research, writing, and evaluation skills.

---

## Highlights

### Claude + Codex (GPT-5.4) Cross-Model Collaboration

One of the most powerful patterns in this collection: **use Claude (Opus/Sonnet) as the primary coding agent, with GPT-5.4 via Codex MCP as an independent reviewer and research partner.** Two models catch more bugs than one.

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

| Stage | Skills |
|---|---|
| Literature Search | `research-lit`, `kdense-literature-review`, `kdense-bgpt-paper-search`, `deep-research`, `exa-search` |
| Idea Generation | `brainstorming-research-ideas`, `creative-thinking-for-research`, `idea-creator`, `idea-discovery` |
| Novelty Check | `novelty-check` — verify against recent literature |
| Deep Research | `academic-deep-research` — 13-agent pipeline, PRISMA-compliant systematic review, meta-analysis |
| Paper Planning | `paper-plan` — structured outline from review + experiment results |
| Figure Generation | `paper-figure`, `orchestra-academic-plotting` — publication-quality figures from data |
| Paper Writing | `paper-write`, `ml-paper-writing`, `orchestra-ml-paper-writing`, `research-paper-writing` — section-by-section LaTeX drafting with venue templates (NeurIPS, ICML, ICLR, ACL, AAAI, COLM) |
| Peer Review | `academic-paper-reviewer` — multi-perspective simulated review with dynamic reviewer personas |
| Auto-Improve | `auto-paper-improvement-loop` — GPT-5.4 review → fix → recompile, 2 autonomous rounds |
| Full Pipeline | `academic-pipeline` — 9-stage orchestrator: research → write → integrity → review → revise → finalize |
| LaTeX Compile | `paper-compile` — compile, fix errors, verify output |

### Evaluation & Benchmarking

| Skill | What it evaluates |
|---|---|
| `orchestra-lm-evaluation-harness` | 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, ...) |
| `orchestra-bigcode-evaluation-harness` | Code generation: HumanEval, MBPP, MultiPL-E, 15+ benchmarks |
| `orchestra-nemo-evaluator` | 100+ benchmarks from 18+ harnesses |
| `eval-harness` | Formal evaluation framework for Claude Code sessions |
| `kdense-peer-review` | Structured manuscript/grant review with checklist evaluation |
| `kdense-scientific-critical-thinking` | Evaluate scientific claims and evidence quality |

---

## All Skill Categories

| Category | Count | Key Skills |
|---|---|---|
| **Research & Writing** | 40+ | academic-paper, deep-research, ml-paper-writing, research-lit, idea-creator, novelty-check |
| **Cross-Model (Codex)** | 10+ | codex-review, auto-review-loop, deep-research-codex-*, multi-plan/execute |
| **Superpowers** | 12 | brainstorming, writing-plans, TDD, debugging, code-review, verification |
| **Development Patterns** | 20+ | python/golang/rust/kotlin/swift/django/laravel/springboot-patterns |
| **Testing** | 10+ | tdd-workflow, python/golang/rust/kotlin/cpp-testing, e2e-testing |
| **Code Review** | 10+ | security-review, python/go/rust/cpp/kotlin/flutter/java-reviewer |
| **DevOps** | 5+ | docker-patterns, deployment-patterns, dmux-workflows, autonomous-loops |
| **Content & Media** | 10+ | article-writing, crosspost, x-api, fal-ai-media, manim-video, pixel-art |
| **Security** | 5+ | security-review, security-scan, django/laravel/springboot-security |
| **Evaluation** | 7 | lm-evaluation-harness, bigcode-harness, nemo-evaluator, eval-harness |

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

# Or install selectively — just copy what you need
cp -r skills/codex-review ~/.claude/skills/
cp -r skills/ml-paper-writing ~/.claude/skills/
cp -r skills/academic-deep-research ~/.claude/skills/
cp -r rules/common ~/.claude/rules/
```

### Codex MCP Setup (for cross-model review)

To enable Claude + GPT-5.4 collaboration, configure the Codex MCP server in your Claude Code settings. See the [Codex MCP documentation](https://github.com/openai/codex) for setup instructions.

## Credits

- [Everything Claude Code (ECC)](https://github.com/anthropics/claude-code) by Affaan Mustafa — the plugin infrastructure powering this collection
- [KDense](https://github.com/kdense) — scientific writing and literature review skills
- [Orchestra](https://github.com/orchestra-ai) — evaluation harness and ML paper writing skills

## License

MIT
