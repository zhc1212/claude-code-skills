---
name: tutorial
description: Interactive tutorial — walk through SVD_LLM compression, evaluation, and fine-tuning step by step. Use when user says "教程", "tutorial", "how to use", "getting started", or is new to the project.
user_invocable: true
---

# SVD_LLM Tutorial

Interactive walkthrough of the SVD_LLM compression pipeline.

## Step 1: Overview

Explain the SVD_LLM method:
1. **Data-aware whitening**: Collect activation covariance from calibration data, apply Cholesky whitening to decorrelate weight dimensions
2. **SVD truncation**: Decompose whitened weights via SVD, keep top-r singular values
3. **CompressedLinear**: Replace original `nn.Linear(d, n)` with two smaller layers `B(r, n)` and `A(d, r)`
4. **Sequential LoRA** (optional): Two-stage fine-tuning to recover accuracy

## Step 2: Quick Start (CPU Demo)

Walk through a minimal example:

```bash
# Check environment
python3 -c "import torch; print(f'PyTorch {torch.__version__}')"
python3 -c "import transformers; print(f'Transformers {transformers.__version__}')"

# Run unit tests to verify setup
pytest tests/ -m "not integration" -v --co  # list tests without running
pytest tests/test_whitening.py -v           # run whitening tests
```

## Step 3: Compression (GPU Required)

```bash
# Compress LLaMA-7B at 20% ratio
python scripts/compress.py \
    --model_path jeffwan/llama-7b-hf \
    --method svd_llm_w \
    --ratio 0.2 \
    --save_path outputs/llama7b_w_20

# Note: requires ~30GB VRAM on A100
```

Explain the key parameters:
- `--method svd_llm_w`: whitening + SVD truncation (the supported method)
- `--ratio 0.2`: remove 20% of parameters

## Step 4: Evaluation

```bash
# Perplexity on WikiText-2
python scripts/eval_model.py \
    --model_path outputs/llama7b_w_20 \
    --eval perplexity \
    --datasets wikitext2

# Downstream tasks
python scripts/eval_model.py \
    --model_path outputs/llama7b_w_20 \
    --eval downstream \
    --tasks openbookqa arc_easy winogrande hellaswag piqa
```

## Step 5: Fine-tuning (Optional)

```bash
# Sequential LoRA to recover accuracy
python scripts/finetune.py \
    --model_path jeffwan/llama-7b-hf \
    --ratio 0.2 \
    --save_path outputs/llama7b_lora_20
```

## Step 6: Understanding the Code

Guide through key source files:
- `src/compress/whitening.py` — the core algorithm
- `src/model/replace.py` — `CompressedLinear` layer
- `src/model/loader.py` — rank computation
- `src/data/calibration.py` — calibration data collection
- `src/eval/perplexity.py` — perplexity evaluation

## Step 7: Next Steps

Suggest:
- Try different compression ratios (0.2, 0.4, 0.6)
- Explore experimental compression approaches (see `CLAUDE.md` for status)
- Read `docs/technical_report.md` for mathematical details
- Check `IDEA_REPORT.md` for active research directions
