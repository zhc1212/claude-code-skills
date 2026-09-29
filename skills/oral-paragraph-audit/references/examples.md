# Audit Examples

## Good Audit — Experiments Paragraph (thorough, zero-skip compliant)

Input:
> "42.1 drops to 19.1 after block optimization and 11.4 after full-model optimization.
> The gains are robust across five architectures. This demonstrates the effectiveness
> of our approach."

```
¶ Experiments / Overall Performance

Section role: Experiments, claim→evidence — this ¶ serves as the opening claim. OK.
Strengths: concrete numbers, clear progression across levels

 1. Sentence level: largest subject→verb gap S1 ("42.1" … "drops", 0 words); stress position
               S3 ends on "our approach" (old information). S3 uses "This" as a pronoun.
               MAJOR (F2).
 2. Transitions: S1→S2: Extension (adds scope). S2→S3: Consequence, but vacuous —
               "This demonstrates" adds no information. MAJOR (F2).
3a. Structure:  S1 message: "42.1 drops to 19.1..." — raw data, no claim. BLOCKING (F1).
               S2: Extension (adds scope). S3: restates S1-S2 vacuously. MAJOR (F2).
3b. Density:    S1: +new. S2: +new (adds architecture scope). S3: ~filler. MAJOR (F2).
 4. ¶ bridge:   skipped (no adjacent ¶)
5a. Consistency: skipped (single ¶, no other section)
5b. First use:  skipped (no other part of the paper)
5c. Placement:  S1-S2: OK. S3: generic, belongs nowhere. MAJOR (F2).
 6. De-AI:      "robust" (S2, watchlist), "demonstrates the effectiveness" (S3, vague
               achievement claim). One hit per sentence, no cluster. MAJOR (F3), MAJOR (F2).
 7. Section:    Experiments ¶ must open with a claim, not data. BLOCKING (F1).
 8. Claims:     "robust" — no table ref, no scope qualifier. MAJOR (F3).
               "effectiveness" — vague, not refutable. MAJOR (F2).
 9. Formulas:   skipped (no formula)

Finding summary: 1 Blocking / 2 Major / 0 Minor

F1 BLOCKING (Checks 3a, 7): S1 opens on data, not a claim.
   - **Original**: "42.1 drops to 19.1 after block optimization and 11.4 after full-model optimization."
   - **Revised**: "Each optimization level lowers [fill: metric]: from 42.1 to 19.1 after block optimization and to 11.4 after full-model optimization ([fill: table ref])."
   - **Why**: claim-first structure; the table ref grounds the evidence.
F2 MAJOR (Checks 1, 2, 3a, 3b, 5c, 6, 8): S3 restates S1–S2 and adds nothing.
   - **Original**: "This demonstrates the effectiveness of our approach."
   - **Revised**: [delete]
   - **Why**: the sentence carries no claim a reader could check.
F3 MAJOR (Checks 6, 8): "robust" is unsupported and unscoped.
   - **Original**: "The gains are robust across five architectures."
   - **Revised**: "The gains hold across five architectures ([fill: table ref])."
   - **Why**: "hold" states what was measured; the table ref supports it.

Added facts: none
```

## Good Audit — Method Paragraph with Formula (exercises Checks 5c and 9)

Input:
> "The low-rank factors {A_j, B_j} are warm-started from L2 and updated end-to-end,
> while all other parameters remain frozen. The objective is min -∑ log p(x|...) where
> p is the compressed model's next-token probability computed with all weights W_j
> replaced by A_j B_j as the trainable variables."

```
¶ Method / L3 Objective

Section role: Method, setup→derivation — formulation paragraph. OK.
Strengths: clear objective, notation defined.

 1. Sentence level: largest subject→verb gap S1 ("factors" … "are", 1 word); stress position
               S2 ends on "as the trainable variables", which S1 already said. MINOR (F2).
 2. Transitions: S1→S2: Refinement (S1 says what's optimized, S2 formalizes). OK.
3a. Structure:  S1: "factors are warm-started and updated end-to-end"
               S2: Evidence (formal objective). OK.
3b. Density:    S1: +new. S2: +new but tail =echo ("computed with all weights W_j
               replaced by A_j B_j" restates what the formula shows). MINOR (F2).
 4. ¶ bridge:   skipped (no adjacent ¶)
5a. Consistency: skipped (single ¶, no other section)
5b. First use:  skipped (no other part of the paper)
5c. Placement:  S1 "warm-started from L2" — implementation detail, Experiments Setup.
               MAJOR (F1). S2 objective — OK for Method.
 6. De-AI:      PASS.
 7. Section:    Definition → equation → interpretation. OK.
 8. Claims:     No empirical claims. OK.
 9. Formulas:   Loss lacks 1/N normalization (sum vs average ambiguous). MINOR (F3).

Finding summary: 0 Blocking / 1 Major / 2 Minor

F1 MAJOR (Check 5c): "warm-started from L2" is Experiments Setup, not Method definition.
   - **Original**: "are warm-started from L2 and updated end-to-end"
   - **Revised**: "are the trainable parameters, updated end-to-end"
   - **Why**: the initialization is a training choice; Method defines what is optimized.
F2 MINOR (Checks 1, 3b): cut the S2 tail "computed with all weights W_j replaced by A_j B_j as the trainable variables"; the formula and S1 already say it.
F3 MINOR (Check 9): state whether the loss is a sum or a mean over tokens.

Added facts: none
```

## Bad Audit (shallow, unhelpful — NEVER do this)

```
¶ Experiments
 2. Transitions: mostly OK
3a. Structure: mixed
3b. Density: could be improved
5c. Placement: fine
 6. De-AI: some issues
 9. Formulas: N/A
```

This diagnoses nothing and provides no fixes. Always name the exact sentence, the
exact problem, and the exact replacement. A bare "OK" without evidence is a failed audit.
