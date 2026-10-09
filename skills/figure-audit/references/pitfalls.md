# Audit Pitfalls (from real audits)

These defects passed an initial audit and were caught later by human review. Look for each one
deliberately. Fix recipes live in `figure-pipeline/references/repair-recipes.md`.

| Pitfall | Why it's missed | How to catch |
|-------------|----------------|-------------|
| **figsize(14,7) at \linewidth** | Looks great in standalone PNG, terrible in PDF | `scripts/figure_text_audit.py` reports the rendered sizes before visual inspection |
| Legend at `upper right` on trajectory plot | White facecolor looks "clean" in isolation | Trace every curve through the legend bbox region |
| `loc='upper center'` on spaghetti plot | Assumes top of axes is empty | Spaghetti extends everywhere; only outside-axes is safe |
| Legend in bottom panel of stacked figure | Placed near curves on dual-axis panels | τ/schedule/migration curves pass through legend area |
| Annotation near axis min on dumbbell plot | Label looks fine in its own panel | Check: does label extend past spine toward adjacent panel? |
| "mig X%" inside bar chart bars | Seems informative | If label font >50% of bar height, it occludes; move outside |
| 32-layer horizontal bar at \linewidth | Each bar looks fine in full-res PNG | At print scale, each bar <0.07" tall — barely visible |
| Heatmap + marginal bar same colors | Colors seem consistent | List all color encodings; verify caption explains each |
| Claiming "100% confidence" after single pass | Overconfidence after fixing N-1 issues | Recheck every affected figure after all fixes |
| Fixing overlap by shrinking font | Quick fix | Re-run the script after the fix: still above the venue floor? |
| Resizing one figure causes reflow | Smaller figure → text moves → different float placement | Recheck pages whose floats moved, and the venue page limit |
