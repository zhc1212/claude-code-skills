---
name: experiment-plot-advisor
description: Recommend optimal academic chart types for ML experiment results and generate publication-quality matplotlib/seaborn plotting code. Use when user has experiment data and needs figure recommendations for NeurIPS/ICML/ICLR/ACL papers.
version: 1.0.0
tags: [Visualization, Plotting, Matplotlib, Seaborn, NeurIPS, ICML, Academic, Experiment Results]
---

# Experiment Plot Advisor

Analyze experiment data or purpose, recommend the best chart type from the academic chart library, then generate publication-quality Python plotting code.

## When to Activate

- User says "画图", "绘图推荐", "plot results", "visualize experiments", "what chart should I use"
- User pastes experiment data (CSV, table, numbers) and wants a figure
- User asks how to present results for a paper submission

## Workflow

### Phase 1: Data Analysis & Recommendation

Analyze the user's data and recommend 1-2 chart types from the Academic Chart Library below. Output the recommendation in this exact format:

```
## Recommendation

### 1. [Chart Name]

**Core Rationale:** [Why this chart best supports the academic narrative]

**Visual Design Spec:**
- **Axes:** X = [meaning + unit], Y = [meaning + unit]
- **Scale Treatment:** [Break axis / log scale / normalize — or "none needed"]
- **Statistical Elements:** [Error bars / confidence intervals / significance markers — or "single-run, not applicable"]
- **Color & Style:** [Specific palette + line style suggestions]
```

### Phase 2: Code Generation

After the user confirms the recommendation (or immediately if the data is unambiguous), generate a self-contained Python script that:

1. Uses matplotlib + seaborn (no other plotting libraries)
2. Produces a publication-ready figure (300 DPI, PDF/PNG output)
3. Uses LaTeX-compatible fonts when available
4. Follows the style conventions below

## Academic Chart Library

### I. Numerical & Performance Comparison

| # | Chart | When to Use |
|---|-------|-------------|
| 1 | **Grouped Bar Chart (vertical)** | Standard SOTA comparison. Few methods, short labels. |
| 2 | **Horizontal Bar Chart** | Many methods or long method names. Avoids x-axis label overlap. |
| 3 | **Pareto Front** | Trade-off between two competing metrics (accuracy vs speed). Points on the frontier are optimal. |
| 4 | **Radar Chart** | Multi-dimensional capability profile (speed, accuracy, memory, robustness). |
| 5 | **Stacked Bar Chart** | Breakdown of a total metric (e.g., total time = load + inference + postprocess). |

### II. Trends & Convergence

| # | Chart | When to Use |
|---|-------|-------------|
| 6 | **Line Chart with Confidence Band** | Training loss/accuracy over steps. Semi-transparent shading for std/CI from multiple runs. |
| 7 | **Line Chart with Inset Zoom** | Models converge closely — embed a zoomed sub-plot on the final epoch region. |
| 8 | **Scatter + Fit** | Discrete data with underlying trend. Add regression line to reveal linear/nonlinear patterns. |

### III. Classification Evaluation

| # | Chart | When to Use |
|---|-------|-------------|
| 9 | **ROC Curve** | Binary classification, balanced classes. TPR vs FPR trade-off. |
| 10 | **Precision-Recall Curve** | Imbalanced classes. More informative than ROC when positives are rare. |

### IV. Data Relationships & Matrices

| # | Chart | When to Use |
|---|-------|-------------|
| 11 | **Heatmap** | Matrix data: confusion matrix, multi-model × multi-task performance, correlation matrix. |
| 12 | **Scatter Plot** | Two continuous variables (predicted vs actual). Add diagonal reference line. |
| 13 | **Bubble Chart** | Scatter + third dimension (bubble size = param count or FLOPs). |

### V. Statistical Distributions

| # | Chart | When to Use |
|---|-------|-------------|
| 14 | **Violin Plot** | Better than box plot. Shows probability density shape (e.g., bimodal distributions). |
| 15 | **Box Plot** | Distribution range, median, outliers across groups. |
| 16 | **Donut / Pie Chart** | Category proportions (error type distribution). Prefer donut over pie. |

### VI. Composite Layouts

| # | Chart | When to Use |
|---|-------|-------------|
| 17 | **Dual Y-Axis** | Two metrics with different units on one figure (left: accuracy, right: memory). |
| 18 | **Bar + Line Combo** | Background (bar = sample count) + foreground (line = accuracy). Long-tail analysis. |
| 19 | **Facet Grid** | Too many variables for one plot. Split into matrix of small multiples sharing axes. |

## Recommendation Constraints

1. **Library First:** Always pick from the 19 types above. Only suggest alternatives if none fits AND the alternative meets top-venue standards.
2. **Statistical Rigor:** If data has multiple runs or variance info, require error bars or confidence intervals. If single-run, do not force them.
3. **Scale Adaptation:** When inter-group differences are extreme (e.g., 0-10 vs 70-80), recommend exactly one:
   - **Break axis** — preserve raw value intuition
   - **Log scale** — data spans orders of magnitude
   - **Normalization** — focus on relative improvement
4. **Visual Logic:** Long labels → horizontal bars. Multiple metrics with different units → dual Y-axis. Many conditions → facet grid.

## Plotting Style Conventions

```python
# Standard preamble for all generated plots
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np

# Publication defaults
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': 'serif',
})

# Try LaTeX rendering (graceful fallback)
try:
    plt.rcParams['text.usetex'] = True
    plt.rcParams['font.serif'] = ['Times New Roman', 'Computer Modern']
except:
    plt.rcParams['text.usetex'] = False
```

### Color Palettes

| Scenario | Palette | Code |
|----------|---------|------|
| <=6 methods comparison | Tab10 subset | `plt.cm.tab10(range(n))` |
| Sequential/gradient | Blues or Viridis | `sns.color_palette("Blues", n)` |
| Diverging (pos/neg) | RdBu | `sns.color_palette("RdBu", n)` |
| Ours vs baselines | Ours=red/orange, baselines=grays/blues | Custom list |
| Highlight one method | One saturated + rest desaturated | `[highlight] + [sns.desaturate(c, 0.5) for c in rest]` |

### Line Styles for Grayscale Compatibility

```python
LINESTYLES = ['-', '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 2))]
MARKERS = ['o', 's', '^', 'D', 'v', 'P']
```

## Output Requirements

1. The generated script must be **self-contained** — paste data inline, no external file dependencies.
2. Save figure as both PDF and PNG: `plt.savefig('figure.pdf')` and `plt.savefig('figure.png', dpi=300)`.
3. Figure size: default `(7, 5)` for single plots, `(10, 4)` for wide comparisons, `(7, 7)` for square matrices.
4. Always include a legend unless the chart is self-explanatory (e.g., single-series heatmap).
5. All text in English. Use LaTeX math notation for formulas: `r'$\alpha$'`.
