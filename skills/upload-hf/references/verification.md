# Post-Upload Verification (MANDATORY)

Verification is not optional. Always run at least the quick check after every upload.

## Quick Check

```python
from huggingface_hub import HfApi
api = HfApi()
files = api.list_repo_files("<repo_id>")
target = [f for f in files if "<subfolder>" in f]
print(f"{len(target)} files in target subfolder")
```

## Model Integrity Check

Verify each model subfolder has all required files:

```python
from collections import defaultdict

dirs = defaultdict(set)
for f in files:
    parts = f.split("/")
    if len(parts) >= 2:
        key = "/".join(parts[:-1])
        dirs[key].add(parts[-1])

for d in sorted(dirs):
    fnames = dirs[d]
    safetensors = [f for f in fnames if f.endswith(".safetensors")]
    has_config = "config.json" in fnames
    has_index = "model.safetensors.index.json" in fnames
    has_tokenizer = bool(fnames & {"tokenizer.model", "tokenizer.json", "tokenizer_config.json"})

    if safetensors or has_config:
        ok = has_config and (len(safetensors) >= 1 or any(f.endswith(".pt") for f in fnames))
        status = "OK" if ok else "INCOMPLETE"
        print(f"[{status}] {d}: {len(safetensors)} shards, config={has_config}, tokenizer={has_tokenizer}")
```

## Shard Count Validation

For sharded safetensors models, verify shard count matches index:

```python
import json
from huggingface_hub import hf_hub_download

index_path = hf_hub_download("<repo_id>", "<subfolder>/model.safetensors.index.json")
index = json.load(open(index_path))
expected_shards = set(index["weight_map"].values())
actual_shards = [f.split("/")[-1] for f in files if f.startswith("<subfolder>/model-") and f.endswith(".safetensors")]
missing = expected_shards - set(actual_shards)
if missing:
    print(f"MISSING: {missing}")
else:
    print(f"All {len(expected_shards)} shards present")
```

## Checkpoint (.pt) Verification

For DynRank-style hardened checkpoints:

```python
# Verify checkpoint is loadable
ckpt = torch.load(hf_hub_download("<repo_id>", "<path>.pt"), map_location="cpu", weights_only=False)
print(f"Keys: {list(ckpt.keys())}")
if "ranks" in ckpt:
    r = ckpt["ranks"]
    n = len(r) if isinstance(r, (list, dict)) else r.shape[0]
    print(f"Ranks: {n} entries")
if "state_dict" in ckpt:
    print(f"State dict: {len(ckpt['state_dict'])} keys")
```

## Size Comparison

Compare local vs remote file sizes to catch truncated uploads:

```python
from huggingface_hub import HfApi
api = HfApi()
repo_info = api.list_repo_tree("<repo_id>", recursive=True)
remote_sizes = {item.path: item.size for item in repo_info if hasattr(item, 'size')}

# Compare with local
for local_file in Path("<local_dir>").rglob("*"):
    if local_file.is_file():
        repo_path = str(local_file.relative_to("<base>"))
        if repo_path in remote_sizes:
            local_size = local_file.stat().st_size
            remote_size = remote_sizes[repo_path]
            if local_size != remote_size:
                print(f"SIZE MISMATCH: {repo_path} local={local_size} remote={remote_size}")
```
