---
name: add-model
description: Add support for a new LLM architecture (e.g., Mistral, Phi, Qwen). Use when user says "添加模型", "add model", "support new model", or wants to extend SVD_LLM to a new architecture.
user_invocable: true
---

# Add Model Support

Add SVD-LLM compression support for a new LLM architecture.

## Step 1: Identify the Model

Ask the user (if not provided):
- Model name and HuggingFace path (e.g., `mistralai/Mistral-7B-v0.1`)
- Model architecture family (LLaMA-like, GPT-like, etc.)

## Step 2: Analyze Architecture

```bash
# Check the model's architecture
python3 -c "
from transformers import AutoConfig
config = AutoConfig.from_pretrained('<model_path>')
print(config.architectures)
print(config.model_type)
print(f'Hidden size: {config.hidden_size}')
print(f'Num layers: {config.num_hidden_layers}')
print(f'Num heads: {config.num_attention_heads}')
"
```

Identify which linear layers need compression:
- Attention: `q_proj`, `k_proj`, `v_proj`, `o_proj`
- MLP: `gate_proj`, `up_proj`, `down_proj` (or equivalent)

## Step 3: Update Model Loader

Edit `src/model/loader.py`:
1. Add the new model type to `load_model()` if it needs special handling
2. Update `compute_rank()` if the layer structure differs from LLaMA
3. Ensure the layer name patterns in `replace.py` cover the new architecture's linear layers

## Step 4: Update Layer Replacement

Edit `src/model/replace.py`:
1. Verify `CompressedLinear` replacement works with the new architecture's linear layers
2. Add any architecture-specific layer name patterns

## Step 5: Test

```bash
# Unit test (CPU, mock model)
pytest tests/ -m "not integration" -v -k "model"

# Integration test (GPU, real model) — if available
pytest tests/ -m "integration" -v -k "model"
```

## Step 6: Validate Compression

Run a quick compression + eval cycle:
```bash
python scripts/compress.py --model_path <new_model> --method svd_llm_w --ratio 0.2 --save_path outputs/test_new_model
python scripts/eval_model.py --model_path outputs/test_new_model --eval perplexity --datasets wikitext2
```

## Step 7: Document

Update `README.md` with the new supported model in the compatibility table.
