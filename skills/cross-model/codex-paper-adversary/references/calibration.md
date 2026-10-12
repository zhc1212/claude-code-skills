# Calibration Mode — Post-Submission Accuracy Tuning

After receiving real reviewer feedback, compare Codex's attacks against
actual reviews to calibrate the skill's accuracy over time.

## When to Use

- After receiving reviews from a real submission (OpenReview, ARR, CMT)
- After advisor/collaborator feedback on a draft
- NOT for pre-submission use — this is for tuning, not reviewing

## Protocol

1. User provides real reviewer comments (paste or file path)
2. Claude maps each real reviewer point to Codex attacks:
   - **Hit**: Codex found the same issue → validates the skill
   - **Miss**: real reviewer raised it, Codex didn't → gap to investigate
   - **False alarm**: Codex flagged it, no real reviewer cared → reduce severity
3. Report calibration metrics:
   - Hit rate: what % of real reviewer issues did Codex catch?
   - Miss patterns: what categories of issues does Codex systematically miss?
   - False alarm rate: what % of Codex attacks had no real reviewer counterpart?
   - Severity calibration: did Codex's fatal/major/minor align with reviewer impact?
4. Suggest prompt adjustments if systematic patterns emerge:
   - If misses cluster in a category → add emphasis in prompt template
   - If false alarms cluster → tighten the fatality gates or severity criteria
   - If venue scores are consistently off → adjust the scoring calibration

## Output Format

```
## Calibration Report: {paper} @ {venue}

**Codex review date**: {date} | **Real reviews received**: {date}
**Hit rate**: {X}% ({N}/{M} reviewer points matched)
**False alarm rate**: {Y}% ({K}/{L} Codex attacks with no counterpart)

### Hits (Codex caught it)
| Real Reviewer Point | Codex Attack | Severity Match? |
|---------------------|-------------|-----------------|

### Misses (Codex missed it)
| Real Reviewer Point | Category | Why Codex Missed |
|---------------------|----------|-----------------|

### False Alarms (Codex only)
| Codex Attack | Why No Reviewer Cared |
|-------------|----------------------|

### Recommendations
- {prompt adjustment 1}
- {prompt adjustment 2}
```

## Over Time

Track calibration across submissions. After 3+ calibrations, patterns
become reliable enough to adjust the prompt template permanently.
