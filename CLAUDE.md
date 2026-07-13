# CLAUDE.md

## Core Rules

1. **Read before you write.** Read the files you're modifying, follow existing patterns, check imports before introducing libraries. If unsure how something is done here, ask.
2. **State assumptions and tradeoffs.** Don't pick silently among interpretations; for non-trivial choices present 2-3 options with a recommendation.
3. **Minimum code that solves the problem.** No premature abstraction, speculative error handling, or dead configurability. Copy-paste twice before abstracting.
4. **Surgical diffs.** Don't touch what you weren't asked to touch. Match file style. Every changed line must trace to the request.
5. **Verify.** Reproduce bugs in a failing test before fixing. Run existing tests before and after. Report failures honestly.
6. **Debug by investigation, not guessing.** Read the whole error, reproduce first, change one thing at a time, find root cause before workarounds.
7. **No new dependencies** without checking stdlib/existing deps first; justify any addition.
8. **Communicate precisely.** Say what you did and why, flag concerns proactively, state uncertainty as uncertainty, push back once on real risks.

## Research Conventions

Applies to all research codebases under `~/huicheng/`.

- **Experiments are precious**: never overwrite result files. Append timestamps or use unique output dirs.
- **Reproducibility**: always log random seeds, model paths, hyperparameters, and git commit hash.
- **GPU awareness**: check `nvidia-smi` before launching GPU jobs. Use `CUDA_VISIBLE_DEVICES` to avoid conflicts.
- **Long-running jobs**: use `nohup`, `tmux`, or background execution for experiments >5 min. Don't block the session.
- **Model files are large**: never `git add` model weights, checkpoints, or large tensors. Use `.gitignore`.
- **Paper-ready numbers**: when reporting results, always include the exact command to reproduce.
- For non-trivial features: plan first (planner agent), research existing solutions (`gh search code`, PyPI), review after writing (code-reviewer agent), write tests.

## Style Defaults

Override per project in each project's CLAUDE.md.

- Python 3.10+, linted with ruff
- Type hints on function signatures
- No docstrings/comments/type annotations on unchanged code
- Commit format: `<type>: <description>` — types: feat, fix, refactor, docs, test, chore, perf, ci
- PR: analyze full commit history, use `git diff base...HEAD`, include test plan

## Agent Dispatch

Use proactively — don't wait to be asked:

| Agent | When to use |
|-------|-------------|
| **planner** | Complex features, refactoring, architectural changes |
| **code-reviewer** | After writing/modifying code |
| **tdd-guide** | New features, bug fixes (write tests first) |
| **architect** | System design decisions |
| **build-error-resolver** | When build fails |
| **security-reviewer** | Auth, user input, crypto, external API code |

## Cross-Model Collaboration

Codex feedback (via MCP, see `.claude/rules/codex-default.md`) is **advisory, not authoritative**: verify referenced code exists, reason independently, test before committing to a change.

## Environment

```bash
PY=/home/user/huicheng/ENTER/envs/compactifai/bin/python
```

- GPUs: multi-GPU server, use `CUDA_VISIBLE_DEVICES` to select
- Cross-model review: Codex MCP via `/codex-review` skill or Stop hook

## Python Tools

```bash
ruff format                                   # format
ruff check .                                  # lint
pytest tests/ -m "not integration" -v         # unit tests (exclude GPU)
pytest --cov=src --cov-report=term-missing    # coverage
```

GPU/integration tests are marked `@pytest.mark.integration`. Use `$PY` (defined above) as the interpreter.

## API Keys

Semantic Scholar API key is in the `SEMANTIC_SCHOLAR_API_KEY` environment variable (set in `.claude/settings.json` env block — never hardcode it in files). Pass as header: `x-api-key: $SEMANTIC_SCHOLAR_API_KEY`. Use for `/citation-verification` and any academic paper lookup.

## GitHub Issues

Issue format, labels, and milestone conventions are project-specific. See each repo's `CLAUDE.md`.

Triage labels: canonical 5-role vocabulary, label strings equal role names. See `docs/agents/triage-labels.md`.

## Agent Skills

- Issue tracker: GitHub Issues via `gh` CLI (inferred from `git remote`). See `docs/agents/issue-tracker.md`.
- Domain docs: `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
