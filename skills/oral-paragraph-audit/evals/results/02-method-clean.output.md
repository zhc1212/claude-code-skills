¶ Method — Low-Rank Decomposition with Activation Whitening

**Section role**: Setup→derivation structure. This ¶ serves as the foundational method definition: introduce decomposition, select rank, motivate whitening objective. Role is appropriate; no heading mismatch.

**Strengths**: S1 is clean and precisely typed (dimensions given for all three matrices). S2 is self-contained — $\rho$ formula requires no outside reference to verify. The paragraph is dense with zero filler. Three-sentence compactness is laudable.

---

```
 0. Preflight:  skipped (no surrounding section context provided)

 1. Structure:  S1 message: "We decompose each weight matrix W into
                two low-rank factors A and B such that W ≈ AB."
                S2: Refinement — specifies rank r via ρ. OK.
                S3: Mechanism — introduces whitening preprocessing. OK role,
                    but MAJOR (Step A + Step D): S1 does not preview whitening
                    as part of this method, so S3 arrives as a surprise.
                    Final clause ("where S is the Cholesky factor…") is a
                    definition tag, not an analytic close. The paragraph ends
                    suspended — no sentence interprets why the whitened
                    objective is preferred or what it achieves.
                → MAJOR: S3 introduces an unannounced component; final
                  sentence has no interpretive close.

 2. Density:    S1: +new (W, A, B, r, decomposition). OK.
                S2: +new (ρ, rank selection formula). OK.
                S3: +new (whitening operation, whitened objective, S). OK.
                No echo, no filler. Density: good.

 3. Claims:     S3 claims whitening "reduc[es] the approximation error from
                ‖W − AB‖_F to ‖S⁻¹W − S⁻¹AB‖_F."
                → MAJOR: these are two different norms (different metrics),
                  not the same quantity before and after an improvement.
                  The paragraph does not reduce one to the other — it changes
                  the optimization objective. "Reducing error" implies a
                  scalar improvement claim; this needs either a citation or
                  rephrasing as "we optimize the whitened objective … in
                  place of ‖W − AB‖_F."
                  No citation for the whitening approach (e.g., ASVD,
                  SVD-LLM) — reviewers will expect one here.

 4. Transitions: S1→S2: Refinement (S2 specifies r from S1). Clear. OK.
                S2→S3: Temporal ordering marker ("Before truncation").
                → MAJOR: the temporal marker exposes an execution-order
                  inversion. S3 says whitening happens *before* truncation,
                  but S1–S2 describe truncation without mentioning whitening.
                  The algorithm flow is: whiten → decompose/truncate, yet
                  the paragraph describes decompose → select rank → whiten
                  (before truncation). Logical order and narrative order are
                  reversed, which confuses the reader about when whitening
                  occurs in the pipeline.
                  Additionally, "truncation" is introduced in S3 without
                  having been named in S1–S2 (S1 says "decompose," not
                  "truncate"). Minor terminological gap.

 5. ¶ bridge:   skipped (no preceding paragraph provided)

 6. De-AI:      A. No AI fingerprints detected. Sentence lengths vary
                   (long/medium/very long). OK.
                B. No boosters or stakes-raisers. OK.
                C. Register clean. OK.
                D. S3 is structurally overloaded: main clause + participial
                   consequence ("reducing the approximation error from…") +
                   definition clause ("where S is…") — three layers in one
                   sentence. MINOR: recommend splitting.

 7. Section:    Method convention = definition → equation → interpretation.
                S1 and S2 follow this. S3 gives definition + equation but
                no interpretation — no sentence explains *how* A and B are
                obtained from the whitened objective (SVD? ALS?). A NeurIPS
                reviewer will ask what algorithm solves the minimization.
                → MAJOR: missing solver specification.

 8. Boundary:   All content belongs in Method. ρ definition appropriate
                here. No results or hyperparameter values present. OK.

 9. Formulas:   → BLOCKING (two issues):

                (i) Left vs. right whitening inconsistency.
                The stated motivation is "equalize the contribution of each
                *input* dimension." Equalizing input contributions requires
                right-multiplying W by a function of the input covariance Σ_x
                (e.g., optimizing ‖(W − AB)S‖_F or ‖WS − ABS‖_F, where
                Σ_x = SS^T). The formula given, ‖S⁻¹W − S⁻¹AB‖_F, is
                left-multiplication by S⁻¹ — this rescales *rows* of W
                (output dimensions), not columns (input dimensions). The
                formula is inconsistent with the stated motivation.

                (ii) Covariance matrix never introduced.
                S is defined as "the Cholesky factor of the covariance
                matrix," but no symbol for the covariance is given, and
                "covariance" is ambiguous (input activations? output
                activations?). The reader cannot recover Σ from the text.

                → MINOR: ρ = 1 − r(d+n)/(dn) is negative when
                r > dn/(d+n) (the harmonic mean of d and n). The valid
                domain of r is not stated. Rare in practice but technically
                the formula is unbounded below.

10. Consistency: skipped (single paragraph)
```

---

## Issues with Replacements

### BLOCKING — Formula: left-whitening vs. input contribution equalization

**Original**: "we whiten the activation covariance to equalize the contribution of each input dimension, reducing the approximation error from $\|W - AB\|_F$ to $\|S^{-1}W - S^{-1}AB\|_F$ where $S$ is the Cholesky factor of the covariance matrix."

**Revised**: "Before decomposition, we prewhiten the input activations: letting $\Sigma = SS^T$ be the Cholesky factorization of the input activation covariance $\Sigma \in \mathbb{R}^{n \times n}$, we instead minimize $\|(W - AB)S\|_F$, which weights each input dimension by its activation variance and yields a smaller reconstruction error in activation space than the unweighted Frobenius objective."

**Why**: Left-multiplying $W$ by $S^{-1}$ rescales output dimensions; equalizing *input* contributions requires right-multiplication by $S$, corresponding to optimizing $\|(W-AB)S\|_F$ in the whitened input basis.

---

### BLOCKING — Formula: covariance undefined

**Original**: "where $S$ is the Cholesky factor of the covariance matrix"

**Revised**: "where $\Sigma = SS^T$ is the Cholesky factorization of the input activation covariance $\Sigma = \mathbb{E}[xx^\top] \in \mathbb{R}^{n \times n}$, estimated from calibration data"

**Why**: $S$ cannot be recovered without defining the covariance matrix (symbol, dimensions, and estimation procedure); "the covariance matrix" is ambiguous in a weight-matrix context.

---

### MAJOR — Structure S1: unannounced component; no interpretive close

**Original S1**: "We decompose each weight matrix $W \in \mathbb{R}^{d \times n}$ into two low-rank factors $A \in \mathbb{R}^{d \times r}$ and $B \in \mathbb{R}^{r \times n}$ such that $W \approx AB$."

**Revised S1**: "We approximate each weight matrix $W \in \mathbb{R}^{d \times n}$ by a rank-$r$ product $W \approx AB$, where $A \in \mathbb{R}^{d \times r}$ and $B \in \mathbb{R}^{r \times n}$, using an activation-weighted objective to account for input covariance."

**Why**: Previewing the whitening motivation in S1 prevents S3 from arriving as a structurally disconnected operation.

**Add a closing sentence after S3**: "We obtain $A$ and $B$ via truncated SVD of the prewhitened matrix $WS$, then recover the original-space factors as $A = U_r$ and $B = \Sigma_r V_r^\top S^{-1}$."

**Why**: Check 7 requires stating the solver; without it, the method is underspecified for reproduction.

---

### MAJOR — Transition S2→S3 + Claim: "reducing error" mischaracterization

**Original**: "…reducing the approximation error from $\|W - AB\|_F$ to $\|S^{-1}W - S^{-1}AB\|_F$…"

**Revised** (after fixing the left/right issue above): "…replacing the Frobenius objective with the activation-weighted norm $\|(W-AB)S\|_F$, which assigns larger penalty to directions of high activation variance \citep{[SVD-LLM or ASVD citation]}."

**Why**: Two different norms cannot be described as one "reducing" to the other; the paragraph is changing the objective, not proving a magnitude bound, and a citation is needed for the whitening strategy.

---

### MINOR — S3 overloaded; split recommended

**Original S3**: one sentence containing main clause + participial consequence + definition clause.

**Suggestion**: Break after the norm expression. End with a period after `$\|S^{-1}W - S^{-1}AB\|_F$` (or the corrected version), then start a new sentence: "$S$ is the lower-triangular Cholesky factor of the input activation covariance $\Sigma$, estimated from a small calibration set."

---

### MINOR — $\rho$ domain

After $\rho = 1 - r(d+n)/(dn)$, add: "where $r \leq dn/(d+n)$ ensures $\rho \geq 0$" — or note this constraint elsewhere.

---

## Revised Paragraph (incorporating all fixes)

```latex
We approximate each weight matrix $W \in \mathbb{R}^{d \times n}$ by a
rank-$r$ product $W \approx AB$, where $A \in \mathbb{R}^{d \times r}$ and
$B \in \mathbb{R}^{r \times n}$, using an activation-weighted objective to
account for input covariance.  The rank $r \leq dn/(d+n)$ is chosen to
satisfy a target compression ratio $\rho = 1 - r(d+n)/(dn)$, the fraction
of parameters removed.  Before decomposition, we prewhiten the input
activations: letting $\Sigma = SS^T$ be the Cholesky factorization of the
input activation covariance $\Sigma = \mathbb{E}[xx^\top] \in \mathbb{R}^{n
\times n}$, estimated from calibration data, we minimize $\|(W - AB)S\|_F$
in place of $\|W - AB\|_F$, weighting each input direction by its activation
variance~\citep{[cite]}.  We obtain $A$ and $B$ via truncated SVD of $WS$
and recover $A = U_r$, $B = \Sigma_r V_r^\top S^{-1}$.
```

---

## Severity summary

| # | Severity | Issue |
|---|----------|-------|
| 9i | **Blocking** | Left-whitening formula inconsistent with stated motivation |
| 9ii | **Blocking** | Covariance matrix $\Sigma$ never defined |
| 3 | **Major** | "Reducing error" mischaracterizes objective substitution; citation missing |
| 4 | **Major** | Narrative order inverts execution order (decompose described before whitening) |
| 7 | **Major** | Solver (truncated SVD) never specified — method underspecified |
| 1 | **Major** | S1 doesn't preview whitening; no interpretive close |
| 9iii | Minor | $\rho$ domain ($r \leq dn/(d+n)$) unstated |
| 6 | Minor | S3 overloaded — split recommended |
