# Upload Speed Diagnosis

## Step 1: Check for Proxy

Proxies can throttle HF uploads by 10-100x. This is the single most common cause of slow uploads.

```bash
echo "http_proxy: ${http_proxy:-not set}"
echo "https_proxy: ${https_proxy:-not set}"
echo "CLAUDE_PROXY_URL: ${CLAUDE_PROXY_URL:-not set}"
```

**Claude Code always sets `http_proxy=127.0.0.1:<port>`.** This proxy handles Claude's API calls (small JSON) and will destroy upload speeds (1-4 KB/s for large files). It MUST be stripped.

## Step 2: Speed Test -- Proxy vs Direct

```bash
dd if=/dev/urandom of=/tmp/hf_speed_test bs=1M count=5 2>/dev/null

echo "WITH proxy:"
curl -s -o /dev/null -w "  speed: %{speed_upload} B/s (%{time_total}s)\n" \
  -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  -T /tmp/hf_speed_test "https://huggingface.co/api/repos/create" --max-time 60

echo "WITHOUT proxy:"
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
  curl -s -o /dev/null -w "  speed: %{speed_upload} B/s (%{time_total}s)\n" \
  -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
  -T /tmp/hf_speed_test "https://huggingface.co/api/repos/create" --max-time 60

rm /tmp/hf_speed_test
```

## Step 3: Decision

| With proxy | Without proxy | Action |
|-----------|--------------|--------|
| ~300 KB/s | ~5 MB/s | **Bypass proxy** (most common) |
| ~300 KB/s | ~300 KB/s | Network limit, not proxy |
| ~5 MB/s | ~5 MB/s | No proxy issue |

## Bypassing Proxy

**Two layers required** -- `env -u` for Rust runtime, `os.environ.pop()` for Python HTTP clients:

### Layer 1: OS-level (for hf_xet Rust backend)

```bash
env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
    -u all_proxy -u ALL_PROXY -u CLAUDE_PROXY_URL -u CLAUDE_PROXY_PORT \
    python upload.py
```

### Layer 2: Python-level (for requests/urllib3)

At the very top of the script, **before any imports**:
```python
import os
for var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
            "all_proxy", "ALL_PROXY", "CLAUDE_PROXY_URL", "CLAUDE_PROXY_PORT"]:
    os.environ.pop(var, None)
os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"
os.environ["HF_XET_CACHE"] = "/tmp/hf-xet-cache"
```

**Why both?** `hf_xet` is a Rust native extension that reads `/proc/self/environ` at initialization. Python's `os.environ.pop()` modifies a Python dict, not the process-level environment. Without `env -u`, the Rust runtime sees the proxy and uploads stall at 99%.

### Verification

After starting the upload process, verify proxy is stripped:
```bash
cat /proc/$(pgrep -f upload)/environ | tr '\0' '\n' | grep -i proxy
# Should return nothing
```

## Step 4: Check xet Backend

`hf_xet` is the current recommended fast backend (2025+), replacing `hf_transfer`.

```bash
python -c "import hf_xet; print('hf_xet: available')" 2>/dev/null || echo "hf_xet: NOT installed (pip install hf_xet)"
python -c "import hf_transfer; print('hf_transfer: available (legacy)')" 2>/dev/null
```

**Recommended env vars:**
```bash
export HF_XET_HIGH_PERFORMANCE=1     # Enable high-performance xet backend
export HF_XET_CACHE=/tmp/hf-xet-cache  # Local SSD cache (important on NFS)
unset HF_HUB_ENABLE_HF_TRANSFER     # Don't use legacy alongside hf_xet
```

## Step 5: HF Mirror (China)

`hf-mirror.com` can help for downloads but rarely helps uploads (uploads go to HF's LFS regardless).

```bash
curl -s -o /dev/null -w "%{time_total}s\n" https://hf-mirror.com/api/whoami-v2
curl -s -o /dev/null -w "%{time_total}s\n" https://huggingface.co/api/whoami-v2
```

## Expected Speeds

| Connection | Upload speed | 16 GB checkpoint |
|-----------|-------------|-----------------|
| University/lab (direct + hf_xet) | 10-50 MB/s burst, 2-15 MB/s sustained | 15-60 min |
| University/lab (direct, no xet) | 5-15 MB/s | 20-60 min |
| Home broadband | 1-5 MB/s | 1-4 hours |
| **Through Claude Code proxy** | **0.001-0.004 MB/s** | **50-200 hours** |
| Through other proxy | 0.1-0.5 MB/s | 9-40 hours |

Note: HF CDN rate-limits after initial burst. 40+ MB/s for the first ~1 GB, then 2-15 MB/s sustained is normal with `hf_xet`.
