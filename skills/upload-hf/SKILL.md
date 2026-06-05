---
name: upload-hf
description: Prepare, upload, verify, or audit ML model artifacts on HuggingFace Hub. Use when the user mentions HuggingFace, Hugging Face, HF Hub, Model Hub, huggingface_hub, huggingface-cli, push_to_hub, repo_id, model card, uploading checkpoints/weights/tokenizers/adapters/LoRA to HF, or Chinese phrases like 上传到HuggingFace, 传到HF, 推到Hub, 发布模型到HF, 上传模型, HF上传进度. Also use when checking what's already uploaded, creating manifests, or diagnosing upload speed. Do NOT trigger for generic "upload model" without HF context, or for S3, GCS, W&B Artifacts, ModelScope, or GitHub Releases.
user-invocable: true
---

# Upload Models to HuggingFace Hub

Publishing model weights is a side-effecting, potentially public action. Always confirm with the user before creating repos, making things public, or overwriting remote files.

## Step 0: Discover Project Tooling

Before doing anything else, check what the project already has:

```bash
# Project-specific upload scripts
find . -maxdepth 3 -name "*hf*upload*" -o -name "*upload*hf*" 2>/dev/null
# Manifests
ls manifests/*.yaml 2>/dev/null
# Existing HF config
cat .huggingface/config.json 2>/dev/null
# README with upload instructions
grep -l "huggingface\|push_to_hub\|upload" README.md Makefile 2>/dev/null
```

If the project has upload tooling, prefer it. If not, use `huggingface_hub` Python API directly. Do not copy scripts from other repositories without asking.

## Step 1: Figure Out What to Upload

Infer from context before asking:
- Just finished compression/training -> model is in output dir
- Mentions a paper -> check `manifests/` for a batch manifest
- Says "all models" or "batch" -> use manifest mode

Only ask if genuinely ambiguous.

## Step 2: Preflight Checks

Run before any upload. Read `references/preflight.md` for the full checklist.

**Quick version:**
1. **Auth**: `huggingface-cli whoami` or `HfApi().whoami()` -- verify token has write scope
2. **Token source**: use `HF_TOKEN` env var or `~/.cache/huggingface/token`. **NEVER hardcode tokens** in scripts.
3. **Repo**: does it exist? If not, confirm repo_id, org/namespace, visibility (public/private), license
4. **Files**: inventory what's being uploaded -- count, total size, artifact type (full model / LoRA / quantized / tokenizer-only)
5. **Required files**: `config.json` present? Shard index matches shard files? Tokenizer files if applicable?
6. **Exclusions**: skip optimizer states, scheduler states, trainer state, `.cache`, wandb, `*.tmp`, `*.lock`
7. **Symlinks**: check `find <dir> -type l` -- symlinks break `upload_large_folder` and `upload_folder` silently
8. **Model card**: `README.md` with HF frontmatter exists?

## Step 3: Strip Proxy + Choose Backend (MANDATORY)

Claude Code injects `http_proxy=127.0.0.1:<port>` into all child processes. This throttles large file uploads to 1-4 KB/s and causes finalization stalls at 99%.

### Backend choice: LFS+hf_transfer (recommended) vs xet

| Backend | Speed | Reliability | Finalization hang? |
|---------|-------|-------------|-------------------|
| **LFS + hf_transfer** (recommended) | 8-15 MB/s | **100% success** | No |
| hf_xet | 40-70 MB/s burst | **~50% hang on >10G files** | Yes (CLOSE-WAIT, unrecoverable without OS kill) |

**Default to LFS + hf_transfer.** xet is faster but its Rust finalization randomly hangs on large files (>10G) with TCP connections stuck in CLOSE-WAIT. SIGALRM cannot interrupt it (Rust blocks Python signals). Even with subprocess timeout + retry, ~50% of large files fail all 3 attempts. LFS is 4-5x slower but has 0% hang rate — net faster for batch uploads.

Only use xet for: single small files (<5G) where speed matters and you can manually retry.

### Proxy stripping

**Both layers are required** -- `env -u` for native HTTP clients, `os.environ.pop()` for Python-level clients:

Launch wrapper (ALWAYS use this):
```bash
nohup env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
  -u all_proxy -u ALL_PROXY -u CLAUDE_PROXY_URL -u CLAUDE_PROXY_PORT \
  HF_HUB_DISABLE_XET=1 HF_HUB_ENABLE_HF_TRANSFER=1 \
  PYTHONUNBUFFERED=1 \
  python upload_script.py > upload_$(date +%Y%m%d_%H%M%S).log 2>&1 &
echo "PID: $!"
```

Python preamble (ALWAYS include at the top of every upload script, before any imports):
```python
import os
for var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
            "all_proxy", "ALL_PROXY", "CLAUDE_PROXY_URL", "CLAUDE_PROXY_PORT"]:
    os.environ.pop(var, None)
os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
```

If you must use xet (small files, speed-critical), replace the two env vars with:
```python
os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"
os.environ["HF_XET_CACHE"] = "/tmp/hf-xet-cache"
```
And use the `env -u` wrapper with `HF_XET_HIGH_PERFORMANCE=1 HF_XET_CACHE=/tmp/hf-xet-cache` instead.

Read `references/upload-speed.md` for speed diagnosis and testing.

## Step 4: Choose Upload Method

**Decision tree (validated by real-world experience):**

```
Has symlinks? ──yes──> upload_file (per-file, handles symlinks)
     │no
     v
Single small dir (<5 GB)? ──yes──> upload_folder
     │no
     v
Many checkpoints (research batch)? ──yes──> Per-checkpoint upload_folder + retry
     │no                                    (RECOMMENDED for research workflows)
     v
Single massive dir (>50 GB, no symlinks, flat layout matches repo)?
     ──yes──> upload_large_folder(num_workers=4)
     │no
     v
Default: Per-checkpoint upload_folder + retry
```

**Why per-checkpoint `upload_folder` + retry is the default for research:**
- `upload_large_folder` can stall for 10+ hours at `pre-uploaded: 0/N` due to Xet token expiry on long batches
- `upload_large_folder` requires local layout to match repo layout (no `path_in_repo`)
- `upload_large_folder` fails silently on symlinks (0 files hashed, "complete" with nothing uploaded)
- Per-checkpoint upload_folder gives per-model progress, natural resume points, and retry isolation
- Each checkpoint is one commit -- clean git history on HF

| Method | Parallel | Symlinks | Resume | path_in_repo | Best for |
|--------|----------|----------|--------|--------------|----------|
| `upload_file` | No | Yes | skip-existing | Yes | Single files, symlinked dirs |
| `upload_folder` | Threads | **NO** | No | Yes | Per-checkpoint batch (with retry wrapper) |
| `upload_large_folder` | Workers | **FAILS** | Metadata | **NO** | Single massive flat dir, short uploads |

Read `references/upload-methods.md` for method details and the battle-tested template script.

## Step 5: Dry-Run + Confirm

**Always generate and offer dry-run before uploading.**

Show the user:
- Destination repo + visibility
- File list with sizes
- Total size
- Upload method chosen
- Estimated time (use speed table from `references/upload-speed.md`)
- Number of already-uploaded files that will be skipped

Get explicit confirmation before proceeding, especially for public repos.

## Step 6: Upload

Use the battle-tested template from `references/upload-methods.md`. Every generated upload script MUST include:

1. **Proxy preamble** (Step 3) -- `env -u` wrapper + `os.environ.pop()` before imports
2. **Token from env** -- `os.environ.get("HF_TOKEN")` or `HfApi()` auto-detect, NEVER hardcode
3. **Skip-existing logic** -- `list_repo_files()` to build existing set, skip matches
4. **Retry with backoff** -- 3 retries, exponential delay (30s/60s/90s)
5. **Per-item progress** -- `[i/N] name (size)` format with `flush=True`
6. **Speed reporting** -- elapsed time and MB/s per checkpoint
7. **`--dry-run` flag** -- always available
8. **`--start-from` flag** -- resume from index N
9. **Timestamped log** -- `> upload_YYYYMMDD_HHMMSS.log 2>&1`
10. **Summary line** -- total uploaded/skipped/failed counts
11. **Per-file subprocess timeout** (MANDATORY even with LFS) -- wraps each upload in a child process for isolation. With xet, finalization hangs indefinitely (CLOSE-WAIT); with LFS, network stalls are possible. Use `subprocess.run(timeout=3600)` so the OS can kill a stuck child. After timeout-kill, re-check `list_repo_files()` -- the file may have committed before the kill. Template:

```python
import subprocess, sys

def upload_one(local, remote, is_file, timeout_s=3600):
    script = f'''
import os
for v in ["http_proxy","https_proxy","HTTP_PROXY","HTTPS_PROXY",
          "all_proxy","ALL_PROXY","CLAUDE_PROXY_URL","CLAUDE_PROXY_PORT"]:
    os.environ.pop(v, None)
os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import HfApi
api = HfApi()
api.upload_file(path_or_fileobj={local!r}, path_in_repo={remote!r}, repo_id={REPO_ID!r})
print("UPLOAD_SUCCESS")
'''
    try:
        r = subprocess.run([sys.executable, "-u", "-c", script],
                           timeout=timeout_s, capture_output=True, text=True)
        return "UPLOAD_SUCCESS" in r.stdout
    except subprocess.TimeoutExpired:
        return False  # OS killed the child, re-check remote
```

## Step 7: Monitor

For background uploads, provide the tail command:

```bash
tail -f upload_*.log | grep -E --line-buffered "\[|DONE|ERROR|SKIP|FAILED|===|speed"
```

For `upload_large_folder`, watch the periodic status report:
```bash
tail -f upload_*.log | grep -E --line-buffered "hashed|pre-uploaded|committed|Workers"
```

**Stall detection:** if `pre-uploaded: 0/N` hasn't changed for >30 min, the upload is stuck. Kill and switch to per-checkpoint `upload_folder`.

## Step 8: Verify (MANDATORY)

**Always verify after upload completes.** Read `references/verification.md` for the full checklist.

Quick version:
```python
from huggingface_hub import HfApi
api = HfApi()
files = api.list_repo_files("<repo_id>")

# Per-subfolder completeness
from collections import defaultdict
dirs = defaultdict(set)
for f in files:
    parts = f.split("/")
    if len(parts) >= 2:
        dirs["/".join(parts[:-1])].add(parts[-1])

for d in sorted(dirs):
    fnames = dirs[d]
    has_config = "config.json" in fnames
    shards = [f for f in fnames if f.endswith(".safetensors")]
    pts = [f for f in fnames if f.endswith(".pt")]
    status = "OK" if (has_config and shards) or pts else "CHECK"
    print(f"[{status}] {d}: {len(shards)} shards, {len(pts)} .pt, config={has_config}")
```

## Step 9: Post-Upload

- Offer to delete local checkpoints (with user approval) to free disk space
- Suggest `/eval-model` to test the uploaded model from HF
- If batch upload, offer to create a manifest for future use

## Safety Rules

- **NEVER hardcode HF tokens** in scripts -- use `HF_TOKEN` env var or `~/.cache/huggingface/token`
- Never create a public repo without explicit confirmation
- Never delete remote files without explicit confirmation
- Never overwrite existing remote files without checking first
- Always dry-run before upload
- Prefer idempotent re-runs (skip already-uploaded files)
- Capture logs to timestamped files for long uploads
- Always verify after upload

## References

Read these when you need deeper guidance on a specific step:

- `references/preflight.md` -- auth, file inventory, artifact type detection, model card
- `references/upload-speed.md` -- proxy diagnosis, speed tests, hf_xet, hf_transfer
- `references/upload-methods.md` -- method comparison, battle-tested template, manifest format
- `references/verification.md` -- remote file listing, integrity checks, shard validation
- `references/troubleshooting.md` -- failure matrix, stall patterns, recovery

## Troubleshooting Quick Reference

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Stuck at 0% (hashed 0/N) | Dir symlinks + `upload_large_folder` | Switch to `upload_folder` per-checkpoint |
| **Stuck at 99%** | **Proxy leak into hf_xet Rust runtime** | **`env -u` at OS level -- `os.environ.pop()` alone is NOT enough** |
| Stuck at 100% for 10+ min | xet finalization hang (CLOSE-WAIT connections) | **Switch to LFS backend** (`HF_HUB_DISABLE_XET=1 HF_HUB_ENABLE_HF_TRANSFER=1`). SIGALRM does NOT work (Rust blocks Python signals). subprocess.run(timeout) can OS-kill but ~50% of >10G files hang all 3 retries. LFS eliminates this entirely. |
| **`pre-uploaded: 0/N` for hours** | **Xet token expires mid-batch** | Kill; switch to per-checkpoint `upload_folder` with retry |
| 1-4 KB/s | Claude Code proxy leak | `env -u` ALL proxy vars including `CLAUDE_PROXY_URL` |
| 100-300 KB/s | Network proxy or xet not enabled | Bypass proxy + `HF_XET_HIGH_PERFORMANCE=1` |
| Speed drops 40->2 MB/s | HF CDN rate limiting | Normal -- sustained 2-15 MB/s |
| Retrying deleted file | File removed after scan | Kill + restart (skip-existing handles it) |
| 401 Unauthorized | Bad/expired token | `huggingface-cli login` |
| 403 Forbidden | No write access | Check token scope + org membership |
| `CommitOperationAdd` size 0 | File was symlink, `upload_folder` followed it wrong | Use `upload_file` or dereference first |

## Performance Notes

### LFS + hf_transfer (recommended)
- `HF_HUB_DISABLE_XET=1` disables xet Rust extension entirely
- `HF_HUB_ENABLE_HF_TRANSFER=1` enables Rust-based LFS transfer (faster than pure Python, no finalization bug)
- Sustained: **8-15 MB/s** (stable, no drops)
- 10G file: ~12-17 min, 13.5G file: ~20-22 min
- **0% hang rate** across 16-checkpoint batch uploads (validated 2026-06)
- Per-checkpoint `upload_folder` with retry: most reliable combo for research batch uploads

### hf_xet (NOT recommended for >10G files)
- `hf_xet` Rust extension reads `/proc/self/environ`, not Python's `os.environ` -- proxy must be stripped with `env -u`
- `HF_XET_HIGH_PERFORMANCE=1` enables fastest transfer mode
- `HF_XET_CACHE=/tmp/hf-xet-cache` prevents re-chunking on NFS/networked storage
- Burst: 40-70 MB/s, but **finalization randomly hangs** on files >10G
- Hang mechanism: TCP connections enter CLOSE-WAIT, Rust code has no timeout, Python signals blocked
- **~50% failure rate** on >10G files even with subprocess timeout + 3 retries (validated 2026-06)
- Xet token expires after ~1-2 hours -- long `upload_large_folder` batches stall with no error

### General
- Hashing 16 GB file: ~30s at ~500 MB/s disk read
- `upload_large_folder` metadata lives in `.cache/huggingface/upload/` -- rerun to resume
- Proxy must ALWAYS be stripped with `env -u` regardless of backend
