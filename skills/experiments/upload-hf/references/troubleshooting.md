# Troubleshooting

## Failure Matrix

| Error | Cause | Fix |
|-------|-------|-----|
| **401 Unauthorized** | Missing/expired token, wrong env var | `huggingface-cli login` or check `~/.cache/huggingface/token` |
| **403 Forbidden** | No write access to org/repo, token lacks write scope | Check `huggingface-cli whoami`, request write access, regenerate token with `write` scope |
| **404 Not Found** | Repo doesn't exist, wrong namespace, private repo | Create repo first or check repo_id spelling |
| **409 Conflict** | Concurrent uploads, branch conflict | Wait and retry, or use `--revision` |
| **429 Rate Limited** | Too many requests | Wait 60s and retry, reduce parallelism |
| **SSL Error** | Corporate proxy, TLS interception | Try `--noproxy '*'`, check certificates |
| **Connection Reset** | Network instability on large files | Retry (skip-existing handles already-uploaded) |
| **413 Payload Too Large** | Single file exceeds limit | Shouldn't happen with LFS, check if LFS configured |

## Stall Patterns (The Big Three)

These are the most common upload issues, ordered by frequency:

### 1. `pre-uploaded: 0/N` for hours (upload_large_folder)

**Root cause**: Xet token expires (~1-2 hours). The Xet backend silently fails to authenticate renewed tokens when `upload_large_folder` runs a long batch. Hashing completes (all files hashed) but pre-upload never starts.

**Diagnosis**:
```bash
# In the log, look for this pattern:
# hashed N/N ... | pre-uploaded: 0/M ... | committed: 0/N
# If pre-uploaded stays at 0 for >30 min after hashing completes, it's stuck.
grep "pre-uploaded: 0/" upload.log | tail -5
```

**Fix**: Kill the process. Switch to per-checkpoint `upload_folder` with retry:
```bash
kill <PID>
# Generate a new script using per-checkpoint upload_folder pattern
```

**Prevention**: For batches >50 GB or >5 checkpoints, always use per-checkpoint `upload_folder` instead of `upload_large_folder`.

### 2. Stuck at 99% (upload_file or upload_folder)

**Root cause**: Proxy vars leaked into the `hf_xet` Rust runtime. Python's `os.environ.pop()` removes vars from Python's dict but NOT from the process-level environment that Rust reads.

**Diagnosis**:
```bash
# Check if proxy vars leaked into the running process
cat /proc/<PID>/environ | tr '\0' '\n' | grep -i proxy
```

**Fix**: Kill the process. Relaunch with `env -u` wrapper (see SKILL.md Step 3).

**Prevention**: ALWAYS use both `env -u` wrapper AND `os.environ.pop()` preamble.

### 3. Stuck at 0% / hashed 0/N (upload_large_folder)

**Root cause**: Directory symlinks. `upload_large_folder` does not follow symlinks -- it hashes 0 files and reports completion.

**Diagnosis**:
```bash
find <upload_dir> -type l | head -5
```

**Fix**: Switch to `upload_file` (handles symlinks) or dereference with `cp -rL`.

## Other Issues

### Upload speed < 500 KB/s

**Most likely cause**: proxy throttling.

Diagnosis:
```bash
echo "proxy: ${http_proxy:-none}"
# Speed test without proxy
curl -s -o /dev/null -w "%{speed_upload}" --noproxy '*' -T /tmp/test https://huggingface.co/api/repos/create
```

Fix: bypass proxy (see `references/upload-speed.md`).

### Upload keeps retrying on a deleted file

Happens when a file listed in the directory scan was deleted after the upload started (e.g., `v8_best_soft.pt` gets cleaned up by the training script).

Fix: kill the upload process and restart. The skip-existing logic handles already-uploaded files.

### Disk fills up during upload

HF's upload creates temporary LFS staging files. For `upload_large_folder`, metadata is in `.cache/huggingface/upload/`.

Fix:
- Monitor with `df -h`
- Upload and delete checkpoints one at a time
- For download-eval-delete: download from HF, eval, delete local copy

### Upload succeeds but model can't be loaded

Check:
1. All shard files present (`model-00001-of-00006.safetensors` etc.)
2. `model.safetensors.index.json` matches actual shards
3. `config.json` has correct `architectures` field
4. For checkpoints (.pt): `torch.load(path, map_location='cpu', weights_only=False)`

### `CommitOperationAdd` with size 0

`upload_folder` resolved a symlink to an empty/invalid target. Use `upload_file` instead, or dereference symlinks first.

### Git LFS errors

```bash
git lfs install
huggingface-cli lfs-enable-largefiles .
```

## Recovery Patterns

### Idempotent re-run (safest)
Re-run the upload script. With skip-existing logic, only missing files upload:
```python
existing = set(api.list_repo_files(REPO_ID))
if repo_path in existing:
    continue  # skip
```

### Resume with --start-from
If the script supports it (battle-tested template does):
```bash
python upload_hf.py --start-from 5  # skip first 5 checkpoints
```

### Partial upload cleanup
Remove partially uploaded files from HF (confirm with user first):
```python
api.delete_file("<path>", repo_id="<repo>", repo_type="model")
```

### Download-eval-delete
When disk is tight but you need to eval uploaded models:
```python
path = hf_hub_download("<repo>", "<path>.pt")
# eval using the cached file
# HF cache handles cleanup
```

## Stall Detection Checklist

When an upload appears stuck, check these in order:

1. **Is the process still running?** `ps aux | grep upload`
2. **Is the log still updating?** `ls -la upload.log` -- check timestamp
3. **What does the last log line say?**
   - `pre-uploaded: 0/N` -> Xet token expired (kill + per-checkpoint retry)
   - `99%` or `100%` -> Proxy leak or finalization (wait 30 min for finalization; if proxy, kill + `env -u`)
   - `hashed 0/N` -> Symlinks (kill + switch to `upload_file`)
   - Speed < 100 KB/s -> Proxy not stripped (kill + `env -u`)
4. **Check process env**: `cat /proc/<PID>/environ | tr '\0' '\n' | grep -i proxy`
