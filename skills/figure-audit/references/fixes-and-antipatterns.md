# Common Fixes & Known Anti-patterns

## Quick Fix Reference

| Problem | Fix |
|---------|-----|
| Type 3 fonts (matplotlib) | `plt.rcParams['pdf.fonttype'] = 42` |
| Type 3 fonts (R) | `ggsave(..., device = cairo_pdf)` |
| **Text too small (most common)** | **Set `figsize=(5.5, h)` for NeurIPS linewidth, keep fonts 7-9pt.** Alternative: increase source font until `source_pt × (latex_width / source_width) ≥ 7pt` |
| Text overlap | `plt.tight_layout(pad=...)` or manual `bbox_to_anchor` for legend |
| Legend on spaghetti plot | Move outside axes: `bbox_to_anchor=(0.5, -0.15)` or empty adjacent panel |
| Stacked panel legend overlap | Move bottom-panel legend to upper area: `bbox_to_anchor=(0.98, 0.72)` |
| Red-green only | Add `linestyle='--'` for second series, or use Okabe-Ito palette |
| Dual color encoding | Explicitly state what each color means in each panel/element in caption |
| No takeaway in caption | Add one sentence: "[Key finding this figure demonstrates]" |
| Orphan float | Add `Figure~\ref{fig:X}` or `Table~\ref{tab:X}` in the relevant paragraph |
| Missing panel labels | `ax.text(-0.1, 1.05, '(a)', transform=ax.transAxes, fontweight='bold')` |
| Table missing ↑/↓ | Add `$\uparrow$` or `$\downarrow$` to column headers |
| Inconsistent bold | Verify best-per-group is bolded; check across all ratio/model groups |
| Dense horizontal bars (>20) | Increase `height` param, remove `edgecolor`, or aggregate into groups |
| Page reflow after resize | Recompile 2 passes, check page count, verify floats didn't shift |

## Known Anti-patterns (from real audits)

These passed initial audit but were caught by human review. Treat each as a mandatory check.

| Anti-pattern | Why it's missed | How to catch |
|-------------|----------------|-------------|
| **figsize(14,7) at \linewidth** | Looks great in standalone PNG, terrible in PDF | Scale factor audit catches this before visual inspection |
| Legend at `upper right` on trajectory plot | White facecolor looks "clean" in isolation | Trace every curve through the legend bbox region |
| `loc='upper center'` on spaghetti plot | Assumes top of axes is empty | Spaghetti extends everywhere; only outside-axes is safe |
| Legend in bottom panel of stacked figure | Placed near curves on dual-axis panels | τ/schedule/migration curves pass through legend area |
| Annotation near axis min on dumbbell plot | Label looks fine in its own panel | Check: does label extend past spine toward adjacent panel? |
| "mig X%" inside bar chart bars | Seems informative | If label font >50% of bar height, it occludes; move outside |
| 32-layer horizontal bar at \linewidth | Each bar looks fine in full-res PNG | At print scale, each bar <0.07" tall — barely visible |
| Heatmap + marginal bar same colors | Colors seem consistent | List all color encodings; verify caption explains each |
| Claiming "100% confidence" after single pass | Overconfidence after fixing N-1 issues | Re-read every figure PDF after ALL fixes |
| Fixing overlap by shrinking font | Quick fix | Always verify rendered size post-fix: still ≥ 7pt? |
| Resizing one figure causes reflow | Smaller figure → text moves → different float placement | Recompile and check page count after figure changes |
