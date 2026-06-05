---
name: eval-model
description: Evaluate a compressed/fine-tuned model on perplexity and downstream tasks. Use when user says "评估", "evaluate", "eval", "perplexity", "benchmark", or wants to measure model quality.
user_invocable: true
---

# Evaluate Model

Evaluate a compressed or fine-tuned model.

## Steps

1. Ask the user for parameters (if not provided):
   - `--model_path`: path to the model to evaluate
   - `--eval`: evaluation type — `perplexity`, `downstream`, or both
   - `--datasets`: for perplexity — `wikitext2`, `c4`, or both (default: `wikitext2`)
   - `--tasks`: for downstream — task names (default: `openbookqa arc_easy winogrande hellaswag piqa`)

2. Run evaluation:
```bash
# Perplexity
python scripts/eval_model.py --model_path <path> --eval perplexity --datasets wikitext2 c4

# Downstream tasks
python scripts/eval_model.py --model_path <path> --eval downstream --tasks openbookqa arc_easy winogrande hellaswag piqa
```

3. Report results in a formatted table comparing against known baselines from `docs/results.md`.
