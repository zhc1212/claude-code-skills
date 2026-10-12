# Upload Methods

## Method Comparison

| Method | API | Parallel | Symlinks | Resume | path_in_repo | Best for |
|--------|-----|----------|----------|--------|--------------|----------|
| `upload_file` | `api.upload_file()` | No | Yes | skip-existing | Yes | Single files, symlinked dirs |
| `upload_folder` | `api.upload_folder()` | Threads | **NO** | No | Yes | Per-checkpoint batch (with retry) |
| `upload_large_folder` | `api.upload_large_folder()` | Workers | **FAILS** | Metadata | **NO** | Single massive flat dir |

## Battle-Tested Template: Per-Checkpoint upload_folder + Retry

This is the **recommended default** for research model uploads. Based on real-world experience uploading 100+ GB across many checkpoints.

```python
#!/usr/bin/env python3
"""Upload model checkpoints to HuggingFace Hub.

Features: proxy bypass, skip-existing, retry with backoff, dry-run, resume.

Usage:
  # Dry run (show what would be uploaded)
  python upload_hf.py --dry-run

  # Upload all
  nohup env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
    -u all_proxy -u ALL_PROXY -u CLAUDE_PROXY_URL -u CLAUDE_PROXY_PORT \
    HF_XET_HIGH_PERFORMANCE=1 HF_XET_CACHE=/tmp/hf-xet-cache \
    PYTHONUNBUFFERED=1 \
    python upload_hf.py > upload_$(date +%%Y%%m%%d_%%H%%M%%S).log 2>&1 &

  # Resume from checkpoint 5
  python upload_hf.py --start-from 5
"""
import os
import sys
import time
import argparse

# --- PROXY PREAMBLE (before any imports that touch network) ---
for var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
            "all_proxy", "ALL_PROXY", "CLAUDE_PROXY_URL", "CLAUDE_PROXY_PORT"]:
    os.environ.pop(var, None)
os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"
os.environ["HF_XET_CACHE"] = "/tmp/hf-xet-cache"
# --- END PREAMBLE ---

from huggingface_hub import HfApi, list_repo_files

# ===== CONFIGURE THESE =====
REPO_ID = "<owner/repo>"              # e.g. "zhc12/dynrank-compressed-models"
LOCAL_BASE = "<path_to_models_dir>"    # e.g. "/home/user/models/phase5b_llama2"
REPO_PREFIX = "<hf_path_prefix>"       # e.g. "phase5b_llama2"
MAX_RETRIES = 3
# ===========================

IGNORE_PATTERNS = [
    "optimizer.pt", "optimizer_states", "scheduler.pt", "trainer_state.json",
    "v8_best_soft.pt", "factored_weights.pt", "factors.pt",
    "*.tmp", "*.lock", "__pycache__", ".git", "wandb", "runs",
]


def get_uploaded_dirs(api: HfApi) -> set[str]:
    """Get set of already-uploaded checkpoint directory names."""
    uploaded = set()
    for f in list_repo_files(REPO_ID):
        parts = f.split("/")
        if len(parts) >= 2 and parts[0] == REPO_PREFIX:
            uploaded.add(parts[1])
    return uploaded


def get_local_checkpoints() -> list[tuple[str, float]]:
    """Get list of (dirname, size_gb) for local checkpoint dirs."""
    results = []
    for d in sorted(os.listdir(LOCAL_BASE)):
        path = os.path.join(LOCAL_BASE, d)
        if not os.path.isdir(path):
            continue
        size = sum(
            os.path.getsize(os.path.join(path, f))
            for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))
        )
        results.append((d, size / 1024**3))
    return results


def upload_one(api: HfApi, name: str, index: int, total: int) -> bool:
    """Upload one checkpoint dir with retry. Returns True on success."""
    local_dir = os.path.join(LOCAL_BASE, name)
    hf_path = f"{REPO_PREFIX}/{name}"
    size_gb = sum(
        os.path.getsize(os.path.join(local_dir, f))
        for f in os.listdir(local_dir)
        if os.path.isfile(os.path.join(local_dir, f))
    ) / 1024**3

    print(f"\n[{index}/{total}] {name} ({size_gb:.1f} GB)", flush=True)

    for attempt in range(1, MAX_RETRIES + 1):
        t0 = time.time()
        try:
            api.upload_folder(
                repo_id=REPO_ID,
                repo_type="model",
                folder_path=local_dir,
                path_in_repo=hf_path,
                commit_message=f"Upload {name}",
                ignore_patterns=IGNORE_PATTERNS,
            )
            elapsed = time.time() - t0
            speed = size_gb * 1024 / max(elapsed, 1)
            print(f"  DONE in {elapsed:.0f}s ({speed:.1f} MB/s)", flush=True)
            return True
        except Exception as e:
            if attempt < MAX_RETRIES:
                wait = 30 * attempt
                print(f"  Retry {attempt}/{MAX_RETRIES} in {wait}s: {e}", flush=True)
                time.sleep(wait)
            else:
                print(f"  FAILED after {MAX_RETRIES} retries: {e}", flush=True)
                return False


def main():
    parser = argparse.ArgumentParser(description="Upload checkpoints to HuggingFace")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be uploaded")
    parser.add_argument("--start-from", type=int, default=0, help="Resume from index N (0-based)")
    args = parser.parse_args()

    api = HfApi()

    # Discover what needs uploading
    print("Checking remote repo...", flush=True)
    uploaded = get_uploaded_dirs(api)
    local = get_local_checkpoints()
    todo = [(name, size) for name, size in local if name not in uploaded]

    print(f"Local: {len(local)} | Remote: {len(uploaded)} | To upload: {len(todo)}", flush=True)

    if not todo:
        print("Nothing to upload!")
        return

    total_gb = sum(s for _, s in todo)
    print(f"Total: {total_gb:.1f} GB", flush=True)

    if args.dry_run:
        for i, (name, size) in enumerate(todo):
            marker = "SKIP (--start-from)" if i < args.start_from else "UPLOAD"
            print(f"  [{i}] {marker}: {name} ({size:.1f} GB)", flush=True)
        return

    # Upload
    uploaded_count = 0
    skipped_count = 0
    failed_count = 0
    t_start = time.time()

    for i, (name, _) in enumerate(todo):
        if i < args.start_from:
            print(f"  [{i}] SKIP (--start-from): {name}", flush=True)
            skipped_count += 1
            continue

        if upload_one(api, name, i + 1, len(todo)):
            uploaded_count += 1
        else:
            failed_count += 1
            print(f"  Resume with: --start-from {i}", flush=True)

    total_elapsed = time.time() - t_start
    print(f"\n=== COMPLETE ===", flush=True)
    print(f"Uploaded: {uploaded_count} | Skipped: {skipped_count} | Failed: {failed_count}", flush=True)
    print(f"Total time: {total_elapsed / 60:.0f} min", flush=True)


if __name__ == "__main__":
    main()
```

## upload_file (for symlinked directories)

When files are symlinks or you need per-file `path_in_repo` control:

```python
import os
for k in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
          "all_proxy", "ALL_PROXY", "CLAUDE_PROXY_URL", "CLAUDE_PROXY_PORT"]:
    os.environ.pop(k, None)

from pathlib import Path
from huggingface_hub import HfApi

REPO_ID = "<owner/repo>"
LOCAL_BASE = Path("<local_dir>")

api = HfApi()
existing = set(api.list_repo_files(REPO_ID))

for f in sorted(LOCAL_BASE.rglob("*")):
    if not f.is_file():
        continue
    repo_path = str(f.relative_to(LOCAL_BASE.parent))
    if repo_path in existing:
        continue
    size_gb = f.stat().st_size / (1024**3)
    print(f"  UPLOAD: {repo_path} ({size_gb:.1f} GB)", flush=True)
    try:
        api.upload_file(
            path_or_fileobj=str(f),
            path_in_repo=repo_path,
            repo_id=REPO_ID,
            repo_type="model",
        )
        print(f"    OK", flush=True)
    except Exception as e:
        print(f"    FAILED: {e}", flush=True)
```

## upload_large_folder (single massive directory)

Only use when:
- Single flat directory (no subdirs needed in repo)
- No symlinks (verify with `find <dir> -type l`)
- Upload will finish within ~1 hour (Xet token expiry)

```python
api.upload_large_folder(
    folder_path="<local_dir>",
    repo_id=REPO_ID,
    repo_type="model",
    num_workers=4,
    print_report_every=60,
)
```

**Known issues:**
- Silently hashes 0 files on directory symlinks -- no error, just "complete"
- `pre-uploaded: 0/N` stall for hours when Xet token expires mid-batch
- Does NOT support `path_in_repo` -- local layout must match repo
- Metadata for resume lives in `.cache/huggingface/upload/`

## upload_folder

Good for per-checkpoint uploads. Can stall 10-30 min at 100% on finalization for 10+ GB files.

```python
api.upload_folder(
    folder_path="<local_dir>",
    repo_id=REPO_ID,
    repo_type="model",
    path_in_repo="<subfolder>",
    commit_message="Upload <name>",
    ignore_patterns=["*.tmp", "*.lock", "__pycache__", "*.log"],
)
```

**Does NOT work with symlinks.** Verify: `find <dir> -type l | head -5`

## Batch Upload with Manifest (YAML)

For projects with many models organized by paper tables:

```yaml
repo_id: <owner/repo>
base_dir: ../models/compressed
readme: model-card.md
models:
  - { local: llama2-7b/r04, remote: llama2_7b/r04 }
  - { local: llama2-7b/r06, remote: llama2_7b/r06 }
```

Run: `python scripts/upload_hf_models.py --manifest manifests/<name>.yaml`

## Exclusion Patterns

Always skip these:
- `optimizer.pt`, `optimizer_states/` -- training-only
- `scheduler.pt`, `trainer_state.json` -- training-only
- `v8_best_soft.pt` -- intermediate checkpoint
- `factored_weights.pt`, `factors.pt` -- intermediate
- `*.tmp`, `*.lock` -- temporary
- `.cache/`, `wandb/`, `runs/` -- logging
- `__pycache__/`, `.git/` -- metadata

## Launch Pattern

**ALWAYS use this wrapper** when launching from Claude Code:

```bash
nohup env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
  -u all_proxy -u ALL_PROXY -u CLAUDE_PROXY_URL -u CLAUDE_PROXY_PORT \
  HF_XET_HIGH_PERFORMANCE=1 HF_XET_CACHE=/tmp/hf-xet-cache \
  PYTHONUNBUFFERED=1 \
  python upload.py > upload_$(date +%Y%m%d_%H%M%S).log 2>&1 &
echo "PID: $!"
```

Monitor: `tail -f upload_*.log | grep -E --line-buffered "\[|DONE|ERROR|SKIP|FAILED|==="`
