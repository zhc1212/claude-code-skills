# Preflight Checks

Run all of these before uploading.

## 1. Authentication

```bash
huggingface-cli whoami
```

Or in Python:
```python
from huggingface_hub import HfApi
api = HfApi()
info = api.whoami()
print(f"User: {info['name']}, Orgs: {[o['name'] for o in info.get('orgs', [])]}")
```

If 401: `huggingface-cli login` or check `~/.cache/huggingface/token`. Token must have **write** scope.

**Token sources (in order of preference):**
1. `HF_TOKEN` env var (set in shell or `.env`)
2. `~/.cache/huggingface/token` (written by `huggingface-cli login`)
3. `HfApi()` auto-detects from the above

**NEVER hardcode tokens in scripts.** Hardcoded tokens in upload scripts are a security risk -- they end up in git history and logs.

## 2. Repository

```python
try:
    api.repo_info(repo_id, repo_type="model")
    print("Repo exists")
except Exception:
    print("Repo does not exist — will need to create")
```

Before creating, confirm with user:
- `repo_id` (namespace/name)
- Visibility (public/private)
- License (apache-2.0, mit, cc-by-4.0, etc.)

## 3. Artifact Type Detection

| Type | Required files | Optional |
|------|---------------|----------|
| Full Transformers model | `config.json`, `*.safetensors` or `pytorch_model*.bin`, shard index | tokenizer files, generation_config.json |
| LoRA/PEFT adapter | `adapter_config.json`, `adapter_model.safetensors` | README with base model |
| Quantized (GPTQ/AWQ) | `config.json`, `quantize_config.json`, weights | |
| GGUF | `*.gguf` | README with quant details |
| Tokenizer only | `tokenizer.model` or `tokenizer.json`, `tokenizer_config.json` | |
| Checkpoint (.pt) | `*.pt` file with rank/state_dict | train.log, rank_trajectory |

## 4. File Inventory

```python
from pathlib import Path
upload_dir = Path("<dir>")
files = list(upload_dir.rglob("*"))
real_files = [f for f in files if f.is_file()]
symlinks = [f for f in files if f.is_symlink()]
total_size = sum(f.stat().st_size for f in real_files) / (1024**3)
print(f"Files: {len(real_files)}, Symlinks: {len(symlinks)}, Total: {total_size:.1f} GB")
```

## 5. Exclusion List

Always skip:
- `optimizer.pt`, `optimizer_states/`
- `scheduler.pt`
- `trainer_state.json`
- `*.tmp`, `*.lock`
- `.cache/`, `wandb/`, `runs/`
- `factored_weights.pt`, `factors.pt`
- `v8_best_soft.pt` (intermediate checkpoint that gets deleted)
- `__pycache__/`, `.git/`

## 6. Model Card

If `README.md` doesn't exist, generate a minimal one:

```markdown
---
license: apache-2.0
tags:
  - compressed
  - svd
pipeline_tag: text-generation
---

# Model Name

Compressed with [method] at compression ratio ρ=[ratio].

## Usage

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("repo_id", subfolder="path")
tokenizer = AutoTokenizer.from_pretrained("repo_id", subfolder="path")
```
```

## 7. Shard Validation

For sharded models, verify index matches actual files:

```python
import json
index = json.load(open("model.safetensors.index.json"))
expected = set(index["weight_map"].values())
actual = set(f.name for f in Path(".").glob("model-*.safetensors"))
missing = expected - actual
extra = actual - expected
if missing: print(f"MISSING shards: {missing}")
if extra: print(f"EXTRA shards: {extra}")
```
