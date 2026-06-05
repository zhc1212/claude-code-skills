---
name: dev-setup
description: Interactive wizard to install and configure all development tools for new contributors
user_invocable: true
---

# Dev Setup

Interactive wizard that helps new contributors install and configure all tools needed for the SVD_LLM project.

## Step 1: Dependencies Checklist

Check if `.claude/skills/dev-setup/dependencies.md` exists and has content.

- **If it exists**, ask the user:
  > "Found existing dependencies checklist. Use it as-is, or rescan project files for changes?"
  - **Use existing** → read `dependencies.md` and proceed to Step 2
  - **Rescan** → scan project files (see Scan Targets below), overwrite `dependencies.md`, then proceed

- **If it does not exist**, scan project files and generate `dependencies.md`. Then proceed.

### Scan Targets

When scanning, read these files for tool references:

- `pyproject.toml` — Python dependencies, build config, tool settings
- `.github/workflows/*.yml` — CI tools, Python version, installed packages
- `scripts/*.py` — CLI entry points, required libraries
- `scripts/*.sh` — Shell scripts, CUDA requirements
- `tests/conftest.py` — test fixtures, markers

Organize tools into three tiers in `dependencies.md`:
- **Core** — needed to run compression and evaluation (Python, PyTorch, transformers, datasets)
- **Dev** — needed for development (ruff, pytest, git, gh)
- **Optional** — nice to have (CUDA toolkit, accelerate, peft for LoRA)

Each tool needs: name, check command, install command, purpose.

## Step 2: Detect Platform

```bash
uname -s
python3 --version
nvidia-smi 2>/dev/null || echo "No GPU detected"
```

- Check Python version (requires 3.10+)
- Check CUDA availability and version
- Detect OS for platform-specific instructions

## Step 3: Install Core Dependencies

```bash
# Check if in a virtual environment
python3 -c "import sys; print(sys.prefix != sys.base_prefix)"

# If not, suggest creating one
python3 -m venv .venv
source .venv/bin/activate

# Install project in dev mode
pip install -e ".[dev]"
```

If `pip install` fails, walk through common issues:
- Missing CUDA toolkit for PyTorch
- Incompatible Python version
- Missing system libraries

## Step 4: Install Dev Tools

```bash
# Verify ruff (linter)
ruff --version || pip install ruff

# Verify pytest
pytest --version || pip install pytest

# Verify gh CLI (for PR workflows)
gh --version || echo "Install from https://cli.github.com/"
```

## Step 5: Auth and Configuration

### 5a: GitHub CLI auth

```bash
gh auth status
```

If not authenticated, run `gh auth login`.

### 5b: Repo access

```bash
gh repo view --json name
```

## Step 6: Verification

Run the full check:

```bash
# Lint
ruff check .

# Unit tests (CPU-only, no GPU required)
pytest tests/ -m "not integration" -v
```

### Troubleshooting Common Failures

| Failure | Fix |
|---------|-----|
| `ruff check` fails | Run `ruff check --fix .` to auto-fix |
| Import errors in tests | Missing dependency — run `pip install -e ".[dev]"` |
| CUDA not found | Install PyTorch with correct CUDA version from pytorch.org |
| `transformers` version mismatch | `pip install --upgrade transformers` |

If all checks pass, print:
> "Setup complete! All tools installed and verified. You're ready to contribute."
>
> ## Quick Reference
> - `ruff check .` — lint
> - `pytest tests/ -m "not integration"` — run unit tests
> - `python scripts/compress.py --help` — compression CLI
> - `python scripts/eval_model.py --help` — evaluation CLI
