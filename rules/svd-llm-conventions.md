---
globs: "*.py"
---
# SVD-LLM Python Conventions

## Project Structure
- `src/compress/` — compression algorithms (whitening, SVD truncation)
- `src/model/` — model loading, CompressedLinear layer replacement
- `src/data/` — calibration data, fine-tuning datasets
- `src/finetune/sequential_lora.py` — two-stage Sequential LoRA fine-tuning
- `src/eval/` — perplexity and downstream task evaluation
- `scripts/` — CLI entry points (compress.py, finetune.py, eval_model.py)
- `tests/` — pytest tests

## Code Style
- Python 3.10+, linted with `ruff`
- Use type hints for function signatures
- Follow existing patterns — check similar files before writing new code

## Testing
- Unit tests: CPU-only, no model downloads — run with `pytest tests/ -m "not integration"`
- Integration tests: require GPU + model weights — mark with `@pytest.mark.integration`
- Test config in `tests/conftest.py`

## Key Abstractions
- `CompressedLinear(nn.Module)`: two sequential linear layers (B: r×n, A: d×r) replacing original weight
- `compute_rank()` in `src/model/loader.py`: determines per-layer rank allocation
- Calibration: 256 samples (default) from WikiText-2, covariance computed per sub-layer

## Common Commands
```bash
# Lint
ruff check .

# Unit tests
pytest tests/ -m "not integration" -v

# Compress
python scripts/compress.py --model_path <path> --method svd_llm_w --ratio 0.2 --save_path outputs/

# Evaluate
python scripts/eval_model.py --model_path <path> --eval perplexity --datasets wikitext2
```
