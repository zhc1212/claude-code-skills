# Experiment Critique Categories

Nine categories for evaluating ML experiment designs. Each finding in a
critique must be classified into exactly one.

## Confounder

Variables that could explain the results besides the hypothesis.

**Example**: Comparing two compression methods at different ranks — the rank
difference explains the performance gap, not the method itself.

## Missing Baseline

Comparisons a reviewer would expect that are absent from the design.

**Example**: Claiming improvement over vanilla SVD without comparing to other
low-rank methods (ASVD, LoRA-style decomposition, structured pruning at the
same parameter count).

## Unfair Comparison

Apples-to-oranges setups where conditions differ in ways that bias the outcome.

**Example**: Tuning hyperparameters for the proposed method via grid search
but using published defaults for baselines, giving the proposed method an
unearned advantage.

## Information Leakage

Train/test overlap, calibration data reuse, or hyperparameter selection on
evaluation data.

**Example**: Using WikiText-2 for both calibration (computing whitening
statistics) and perplexity evaluation — the compressed model is optimized for
the test distribution.

## Statistical Issue

Insufficient runs, missing error bars, cherry-picked metrics, or single-seed
results presented as general.

**Example**: Reporting perplexity from a single compression run without error
bars, when the calibration data sampling introduces variance across seeds.

## Reproducibility Gap

Unseeded randomness, undocumented hyperparameters, or hardware-dependent
results without disclosure.

**Example**: Compression results that depend on GPU-specific floating-point
behavior (e.g., different Cholesky decomposition results on A100 vs V100)
without noting the hardware.

## Compute Efficiency

Whether this is the cheapest way to test the hypothesis.

**Example**: Running full 7B model compression to test a rank-allocation
heuristic when a 1.3B pilot would answer the question at 1/10 the cost.

## Ablation Gap

Missing ablation dimensions that would isolate individual contributions.

**Example**: Claiming a two-stage method (whitening + truncation) improves
over single-stage without ablating each stage independently to show both
contribute.

## Logical Gap

The results would not actually support the hypothesis even if they come out
as expected.

**Example**: Measuring only perplexity to validate a method claimed to
preserve reasoning ability — perplexity can improve while downstream
reasoning tasks degrade.
