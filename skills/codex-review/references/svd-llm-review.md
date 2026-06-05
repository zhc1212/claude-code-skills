# SVD-LLM Review Profile

Domain-specific review checks for the SVD-LLM compression library. Load this
profile when reviewing code in the SVD_LLM repository.

## Priority Areas

Append these to the generic review prompt's "Prioritize" section:

```
SVD-LLM specific checks:
- Tensor shape / device / dtype mismatches across compression pipeline
- Numerical stability (Cholesky decomposition, SVD truncation, division by zero)
- GPU memory management (large tensor allocations, missing cleanup, device transfers)
- Reproducibility (unseeded randomness, nondeterministic ops)
- Evaluation/calibration data leakage between train/test splits
```

## Path-Specific Checks

Append these to the review prompt:

```
Path-specific SVD-LLM checks:
- src/compress/, src/model/: rank math, shape invariants, whitening correctness,
  CompressedLinear layout (`.first` = B applied first, `.second` = A applied second),
  covariance normalization (XtX/N before passing to whitening functions)
- src/finetune/: gradient flow, train/eval mode switching, optimizer state
  persistence, checkpoint correctness, manifold constraints
- src/eval/, scripts/: metric correctness, dataset leakage, CLI argument schema
  compatibility, perplexity calculation
- tests/: weak assertions (assert shape but not values), missing edge cases,
  mismatch between test coverage and touched behavior, CPU-only requirement
  for unit tests (@pytest.mark.integration for GPU tests)
```

## Gotchas to Flag

These are known sources of bugs in this codebase — flag if touched:

- CompressedLinear `.first`/`.second` naming follows execution order, not
  matrix notation — confusion here causes silent wrong results
- Covariance must be divided by N before passing to `compress_linear_whitening_from_covariance`
- Must call `merge_compressed_model()` before `save_pretrained()` — CompressedLinear
  state_dict is incompatible with HuggingFace
- Cholesky fallback in `compute_whitening_matrix_from_covariance` has retry
  logic that must be preserved
- `compute_rank()` clamps to `max(1, r)` — never returns 0
- All whitening/SVD operations cast to float32 internally
