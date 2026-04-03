---
globs: "tests/*.py"
---
# SVD-LLM Testing Patterns

Quick reference for writing and editing tests.

## Test Infrastructure

### Markers
- Default: CPU-only unit tests — run with `pytest tests/ -m "not integration"`
- `@pytest.mark.integration`: requires GPU + model weights — skipped unless `--run-integration`

### Fixtures (`conftest.py`)
- `model_path` (session scope): from `--model-path` CLI arg or `SVD_LLM_MODEL_PATH` env var — skips if unset

### Running Tests
```bash
pytest tests/ -m "not integration" -v          # unit tests only
pytest tests/ -m "integration" --run-integration --model-path <path>  # GPU tests
pytest tests/test_whitening.py -v -k "cholesky" # specific test
```

## Test Patterns

### Unit Tests (CPU, no model downloads)
```python
def test_something():
    # Create small random tensors to simulate weights/activations
    W = torch.randn(64, 32)
    X = torch.randn(100, 32)
    # Call the function under test
    result = some_function(W, X)
    # Assert shapes, values, properties
    assert result.shape == (64, 32)
    torch.testing.assert_close(result, expected, atol=1e-5, rtol=1e-5)
```

### Integration Tests (GPU + real model)
```python
@pytest.mark.integration
def test_compression_e2e(model_path):
    model, tokenizer = load_model(model_path, device_map="auto")
    # ... run compression and verify
```

## Key Test Files

| File | Tests |
|------|-------|
| `test_whitening.py` | Cholesky math, S @ S_inv ≈ I, whitened covariance ≈ I |
| `test_replace.py` | CompressedLinear forward, merge, save/reload checkpoint |
| `test_calibration.py` | Data loading, covariance shape, hook registration |
| `test_model_loader.py` | load_model, compute_rank, get_linear_layers |
| `test_perplexity.py` | Perplexity evaluation logic |
| `test_downstream.py` | Downstream task evaluation |
| `test_e2e.py` | Full compress → merge → save → reload pipeline |
| `test_sequential.py` | Sequential LoRA stages |
| `test_manifold_opt.py` | Manifold optimization (recent) |

## Gotchas

- **No model downloads in unit tests**: use `torch.randn` to create fake weights/activations
- **assert_close not allclose**: use `torch.testing.assert_close()` (PyTorch 2.x) not `torch.allclose()`
- **Covariance symmetry**: when creating test covariance matrices, use `X.T @ X` to guarantee PSD
- **conftest path hack**: `sys.path.insert(0, ...)` in conftest.py — imports use `from src.xxx import yyy`
- **CI runs CPU only**: never assume CUDA in non-integration tests
