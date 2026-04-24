# Core Rules

## Output
- Code first, explanation only if non-obvious
- No preamble, no closing fluff
- State the bug, show the fix, stop

## Style
- Python 3.10+, linted with ruff
- Type hints on function signatures
- Prefer editing existing files over creating new ones
- No docstrings/comments/type annotations on unchanged code

## Git
- Commit format: `<type>: <description>` — types: feat, fix, refactor, docs, test, chore, perf, ci
- PR: analyze full commit history, use `git diff base...HEAD`, include test plan

## Workflow
1. Research first — `gh search code`, library docs, PyPI before writing new code
2. Plan first for non-trivial features (use planner agent)
3. Review after writing code (use code-reviewer agent)
4. Test with pytest; use `@pytest.mark.integration` for GPU tests

## Agents (use proactively)
- **planner**: complex features, refactoring, architectural changes
- **code-reviewer**: after writing/modifying code
- **tdd-guide**: new features, bug fixes (write tests first)
- **architect**: system design decisions
- **build-error-resolver**: when build fails
- **security-reviewer**: auth, user input, crypto, external API code

## Python Tools
- Format: `black` / `ruff format`
- Lint: `ruff check .`
- Test: `pytest tests/ -m "not integration" -v`
- Coverage: `pytest --cov=src --cov-report=term-missing`
