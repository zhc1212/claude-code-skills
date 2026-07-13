# Audit Examples

## Good Audit — Experiments Paragraph (thorough, zero-skip compliant)

Input:
> "42.1 drops to 19.1 after block optimization and 11.4 after full-model optimization.
> The gains are robust across five architectures. This demonstrates the effectiveness
> of our approach."

```
¶ Experiments / Overall Performance

Section role: Claim→Evidence — this ¶ serves as opening claim. BLOCKING: opens with data, not claim
Strengths: concrete numbers, clear progression across levels

1. Structure:   S1 message: "42.1 drops to 19.1..." — raw data, no claim.
               S2: Extension (adds scope). S3: ~filler (restates S1-S2 vacuously).
               BLOCKING — S1 leads with data, not claim. S3 off-topic.
2. Density:     S1: +new. S2: +new (adds architecture scope). S3: ~filler.
               MAJOR — S3 is vacuous restatement.
3. Claims:      "robust" — unsupported (no table ref). "effectiveness" — vague, not refutable.
               MAJOR — no scope qualifier.
4. Transitions: S1→S2: Extension (adds scope). S2→S3: Consequence (but vacuous).
               MAJOR at S2→S3 — "This demonstrates" adds no information.
5. ¶ bridge:    skipped (no preceding context)
6. De-AI:       "robust" (watchlist), "demonstrates the effectiveness" (participial tail),
               "This demonstrates" (bare pronoun). MAJOR — 3 AI patterns in 3 sentences.
7. Section:     BLOCKING — experiments ¶ must open with claim, not data.
8. Boundary:    S1-S2: OK. S3: generic, belongs nowhere. MINOR.
9. Formulas:    skipped
10. Consistency: skipped (single ¶)
```

Fixes:
- **Original**: "42.1 drops to 19.1 after block optimization and 11.4 after full-model optimization."
- **Revised**: "The three-level chain outperforms all SVD-family baselines, reducing WikiText-2 perplexity from 42.1 to 11.4 on LLaMA-7B (Table 1)."
- **Why**: claim-first structure; table ref grounds the evidence.

- **Original**: "The gains are robust across five architectures. This demonstrates the effectiveness of our approach."
- **Revised**: "The gains hold across five architectures up to 13B parameters (Table 2)."
- **Why**: "robust" → "hold" (precise); S3 deleted (adds nothing).

## Good Audit — Method Paragraph with Formula (exercises Checks 8 and 9)

Input:
> "The low-rank factors {A_j, B_j} are warm-started from L2 and updated end-to-end,
> while all other parameters remain frozen. The objective is min -∑ log p(x|...) where
> p is the compressed model's next-token probability computed with all weights W_j
> replaced by A_j B_j as the trainable variables."

```
¶ Method / L3 Objective

Section role: Setup→Derivation — formulation paragraph. OK.
Strengths: clear objective, notation defined.

1. Structure:   S1: "factors are warm-started and updated end-to-end"
               S2: Evidence (formal objective). OK.
2. Density:     S1: +new. S2: +new but tail =echo ("computed with all weights W_j
               replaced by A_j B_j" restates what the formula shows). MINOR.
3. Claims:      No empirical claims. OK.
4. Transitions: S1→S2: Refinement (S1 says what's optimized, S2 formalizes). OK.
5. ¶ bridge:    skipped (no preceding context)
6. De-AI:       PASS.
7. Section:     Definition → equation → interpretation. OK.
8. Boundary:    S1 "warm-started from L2" — MAJOR: implementation detail, Experiments Setup.
               S2 objective — OK for Method.
9. Formulas:    Loss lacks 1/N normalization (sum vs average ambiguous). MINOR.
10. Consistency: skipped (single ¶)
```

Fix:
- **Original**: "are warm-started from L2 and updated end-to-end"
- **Revised**: "are the trainable parameters, updated end-to-end"
- **Why**: "warm-started from L2" is Experiments Setup, not Method definition.

## Bad Audit (shallow, unhelpful — NEVER do this)

```
¶ Experiments
1. Structure: mixed
2. Density: could be improved
3. Transitions: mostly OK
4. De-AI: some issues
8. Boundary: fine
9. Formulas: N/A
```

This diagnoses nothing and provides no fixes. Always name the exact sentence, the
exact problem, and the exact replacement. A bare "OK" without evidence is a failed audit.
