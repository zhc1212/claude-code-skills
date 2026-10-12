---
name: collect-results
description: Collect and aggregate experiment results into comparison tables. Use when user says "收集结果", "collect results", "汇总", "aggregate results", or wants to compile experiment outputs.
user_invocable: true
---

# Collect Results

Aggregate experimental results from multiple runs into comparison tables.

## Invocation

- `/collect-results` — collect all results from `outputs/`
- `/collect-results --dir <path>` — collect from a specific directory

## Steps

1. Scan for experiment outputs:
```bash
ls outputs/*/
# Each subdirectory should contain a compressed model + eval results
```

2. Run the results collection script:
```bash
python scripts/collect_results.py
```

3. Read and display the generated tables. Expected output format:
   - Model name, compression method, ratio
   - Perplexity (WikiText-2, C4)
   - Downstream task accuracies (if available)

4. Compare against known baselines from `docs/results.md`:
   - Paper-reported results for LLaMA-7B at various ratios
   - Previous reproduction results

5. If the user wants, update `docs/results.md` with the new results.
