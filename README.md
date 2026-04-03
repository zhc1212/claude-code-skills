# Claude Code Skills Collection

A curated collection of **191 skills**, **68 commands**, **36 agents**, and **rules** for [Claude Code](https://claude.ai/code).

## Contents

| Directory | Count | Description |
|-----------|-------|-------------|
| `skills/` | 191 | Deep, actionable skill files for specific tasks |
| `commands/` | 68 | Slash commands (e.g., `/commit`, `/review`) |
| `agents/` | 36 | Specialized sub-agents (code-reviewer, tdd-guide, etc.) |
| `rules/` | 18 dirs | Coding standards per language + common rules |
| `hooks/` | 4 | Pre/post tool-use hooks |
| `scripts/` | 6 | Orchestration and setup scripts |

## Skill Categories

**Research & Writing**: academic-paper, academic-deep-research, research-lit, paper-write, ml-paper-writing, brainstorming-research-ideas, creative-thinking-for-research, ...

**Development Patterns**: python-patterns, golang-patterns, rust-patterns, kotlin-patterns, springboot-patterns, django-patterns, laravel-patterns, frontend-patterns, backend-patterns, ...

**Testing**: tdd-workflow, python-testing, golang-testing, rust-testing, kotlin-testing, cpp-testing, e2e-testing, ...

**Code Review**: code-review (command), security-review, python-reviewer, go-reviewer, rust-reviewer, cpp-reviewer, ...

**DevOps & Deployment**: docker-patterns, deployment-patterns, dmux-workflows, autonomous-loops, ...

**Content & Media**: article-writing, crosspost, x-api, fal-ai-media, manim-video, video-editing, pixel-art, ...

**Security**: security-review, security-scan, django-security, laravel-security, springboot-security, ...

**AI/ML**: compress, finetune, eval-model, run-gpu-experiment, orchestra-lm-evaluation-harness, ...

## Rules

Language-specific coding standards extending a common base:

- `rules/common/` — Universal principles (coding-style, testing, security, git-workflow)
- `rules/zh/` — Chinese translations
- `rules/typescript/`, `rules/python/`, `rules/golang/`, `rules/rust/`, `rules/kotlin/`, `rules/swift/`, `rules/php/`, `rules/cpp/`, `rules/java/`, `rules/csharp/`, `rules/perl/`

## Installation

Copy the directories you need into your `~/.claude/` directory:

```bash
# Clone
git clone https://github.com/zhc1212/claude-code-skills.git
cd claude-code-skills

# Install everything
cp -r skills/ ~/.claude/skills/
cp -r commands/ ~/.claude/commands/
cp -r agents/ ~/.claude/agents/
cp -r rules/ ~/.claude/rules/
cp -r hooks/ ~/.claude/hooks/
cp -r scripts/ ~/.claude/scripts/

# Or install selectively
cp -r skills/python-patterns ~/.claude/skills/
cp -r skills/tdd-workflow ~/.claude/skills/
cp -r rules/common ~/.claude/rules/
```

## License

MIT
