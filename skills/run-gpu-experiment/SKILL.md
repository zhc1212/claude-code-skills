---
name: run-gpu-experiment
description: Launch a full compress → finetune → eval experiment on GPU. Use when user says "跑实验", "run experiment", "full pipeline", "launch experiment", or wants to run end-to-end compression experiments.
user_invocable: true
---

# Run GPU Experiment

Launch a full SVD-LLM experiment pipeline: compress → (optional) finetune → evaluate.

## Steps

1. Ask the user for experiment configuration:
   - Model: which LLM to compress
   - Method: `svd_llm_w` (the supported CLI method)
   - Ratios: list of compression ratios (e.g., `0.2 0.4 0.6 0.8`)
   - Fine-tune: whether to apply Sequential LoRA after compression
   - GPU: which GPU to use (check with `nvidia-smi`)

2. Generate a shell script under `scripts/` following the pattern of existing `run_*.sh` files:
```bash
#!/bin/bash
export CUDA_VISIBLE_DEVICES=<gpu_id>

for ratio in <ratios>; do
    python scripts/compress.py --model_path <model> --method <method> --ratio $ratio --save_path outputs/<name>_${ratio}
    python scripts/eval_model.py --model_path outputs/<name>_${ratio} --eval perplexity --datasets wikitext2 c4
done
```

3. Launch with `nohup` or `tmux` for long-running experiments.

4. Suggest using `/collect-results` or `nvidia-smi` / `tail -f nohup.out` to check progress.
