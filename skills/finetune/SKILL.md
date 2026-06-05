---
name: finetune
description: Fine-tune a compressed model using Sequential LoRA. Use when user says "微调", "finetune", "lora", "fine-tune", or wants to recover accuracy after compression.
user_invocable: true
---

# Sequential LoRA Fine-tuning

Fine-tune a compressed model to recover accuracy using two-stage Sequential LoRA.

## Steps

1. Ask the user for parameters (if not provided):
   - `--model_path`: original (uncompressed) model path
   - `--ratio`: compression ratio used during compression
   - `--save_path`: output directory for fine-tuned model

2. Run fine-tuning:
```bash
python scripts/finetune.py \
    --model_path <model_path> \
    --ratio <ratio> \
    --save_path <save_path>
```

3. After fine-tuning completes, report results and suggest `/eval-model`.
