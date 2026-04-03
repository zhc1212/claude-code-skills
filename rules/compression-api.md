---
globs: "src/compress/*.py,src/model/*.py"
---
# SVD-LLM Compression API Reference

Quick reference for editing compression and model replacement code.

## Core Pipeline

```
calibration_data → collect_all_layers_covariances() → covariance dict
                                                          ↓
model + covariance + rank → compress_linear_whitening_from_covariance() → (A, B)
                                                                             ↓
                          replace_linear_with_compressed(model, layer_idx, name, A, B) → in-place
                                                                             ↓
                                                    merge_compressed_model(model) → nn.Linear (for saving)
```

## Key Functions

### `src/compress/whitening.py`
- `compute_whitening_matrix_from_covariance(covariance, eps)` → `(S, S_inv)` — Cholesky whitening
- `compute_whitening_matrix(activations, eps)` → `(S, S_inv)` — from raw activations (legacy)
- `compress_linear_whitening_from_covariance(weight, covariance, rank, eps)` → `(A, B)` — main compression

### `src/compress/compress_model.py`
- `compress_model_whitening_only(model, tokenizer, calibration_data, ratio, device)` → model — SVD-LLM(W) full pipeline
- `LINEAR_LAYERS_ORDER` — the 7 linear layers per transformer block, in execution order
- `_get_linear_module(model, layer_idx, linear_name)` → nn.Module

### `src/model/replace.py`
- `CompressedLinear(A, B, bias)` — nn.Module with `.first` (B: r×n) and `.second` (A: d×r)
- `replace_linear_with_compressed(model, layer_idx, linear_name, A, B)` → None (in-place)
- `merge_compressed_model(model)` → model — merge back to nn.Linear before saving

### `src/model/loader.py`
- `load_model(model_path, device_map, dtype)` → `(model, tokenizer)`
- `get_model_config(model_path)` → AutoConfig
- `get_linear_layers(model)` → `[(name, module)]` — skips lm_head
- `compute_rank(d, n, ratio)` → int — `r = max(1, int((1 - ratio) * d * n / (d + n)))`

### `src/data/calibration.py`
- `get_calibration_data(tokenizer, dataset_name, nsamples, seqlen, seed)` → `[tensor(1, seqlen)]`
- `collect_all_layers_covariances(model, data, num_layers, layer_names, device)` → `{(layer_idx, name): (XtX, N)}`

## Layer Naming

7 linear layers per transformer block (`LINEAR_LAYERS_ORDER`):
```
self_attn.q_proj  self_attn.k_proj  self_attn.v_proj  self_attn.o_proj
mlp.gate_proj     mlp.up_proj       mlp.down_proj
```

Access pattern: `model.model.layers[i].self_attn.q_proj`

## Gotchas

- **CompressedLinear layout**: `.first` holds B (r×n, applied first to input), `.second` holds A (d×r, applied second) — naming follows execution order
- **Covariance is XtX not XtX/N**: `collect_all_layers_covariances` returns `(XtX, N)` tuple; divide XtX by N before passing to `compress_linear_whitening_from_covariance` which expects normalized covariance
- **Must merge before saving**: `merge_compressed_model(model)` before `model.save_pretrained()` — CompressedLinear state_dict is incompatible with HuggingFace `from_pretrained()`
- **Cholesky fallback**: `compute_whitening_matrix_from_covariance` retries with extra regularization on `LinAlgError` — if you modify, preserve this fallback
- **Memory**: `compress_model_whitening_only` uses tempdir to stream `(A, B)` pairs to disk — don't try to hold all in memory
- **Rank lower bound**: `compute_rank()` clamps to `max(1, r)` — never returns 0
- **float32 for math**: All whitening/SVD operations cast to float32 internally, regardless of model dtype
