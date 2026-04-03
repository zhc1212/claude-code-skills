---
name: compress
description: Compress an LLM using SVD-LLM whitening + truncation. Use when user says "压缩模型", "compress", "run compression", or wants to apply SVD compression to a model.
user_invocable: true
---

# Compress Model

Run SVD-LLM compression on a specified model.

## Steps

1. Ask the user for parameters (if not provided):
   - `--model_path`: HuggingFace model path or local path (default: `jeffwan/llama-7b-hf`)
   - `--method`: compression method — `svd_llm_w` (whitening + SVD truncation)
   - `--ratio`: compression ratio 0.0–1.0 (e.g., 0.2 = 20% parameters removed)
   - `--save_path`: output directory (default: `outputs/<model>_<method>_<ratio>`)

2. Run the compression:
```bash
python scripts/compress.py \
    --model_path <model_path> \
    --method <method> \
    --ratio <ratio> \
    --save_path <save_path>
```

3. After compression completes, report:
   - Output path and size
   - Suggest running `/eval-model` to evaluate the compressed model
