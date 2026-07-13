¶ Experiments / Scale Generalization

**Section role**: claim→evidence→extension structure — this ¶ serves as the scale-generalization results presentation. **MAJOR**: S1 abdicates the topic position to structural narration.

**Strengths**: S3 pairs a concrete mechanism (applying the method) with specific numbers (42.1 → 11.4) — exactly the claim-first, number-second Experiments pattern. S4 adds a crisp scope statement with count and ceiling.

---

```
 0. Preflight:  No section context provided — section inferred as Experiments
                (quantitative results, model-scale sweep). Role: present
                scale-generalization evidence. MAJOR: S1 is a structural
                signpost, not a claim; misaligns with Experiments
                claim-first convention.

 1. Structure:  S1 message: "Having established X... we now turn to
                evaluating performance across model scales."

                S1: STRUCTURAL SIGNPOST — recaps prior paragraph conclusion
                    and narrates paper structure. Wastes topic position.
                    [MAJOR — Step A violation]
                S2: Claim (improvements over baselines). Should be S1.
                S3: Evidence (LLaMA-7B numbers).
                S4: Extension (five architectures, 13B ceiling).
                S5: New sub-claim (higher compression ratios → larger gains)
                    + participial tail introducing a second topic
                    (model scale × low-rank quality). Two distinct claims
                    that cannot unify under either S1 or S2. [MAJOR — Step C]
                S6: Final sentence. "contributes to our understanding" and
                    "underscore the crucial importance" are empty analytic
                    moves — neither specifies WHAT is now understood nor
                    advances beyond what S2 already asserted. [MAJOR — Step D]
```

**Fix S1:**
- **Original**: "Having established the effectiveness of our whitening-based approach in the previous section, we now turn to evaluating its performance across different model scales."
- **Revised**: "Our whitening-based approach generalizes across model scales, consistently outperforming all evaluated baselines on WikiText-2."
- **Why**: The paragraph's actual claim belongs in the topic position; structural narration wastes the reader's strongest attention slot.

**Fix S2:** Once S1 carries the claim, S2 becomes redundant. Fold its content into S1 (done above) and delete S2, or replace with a table reference cue: "Table X summarizes results on five architectures."

**Fix S5 (second sub-claim):** The compression-ratio finding is a distinct result — it belongs in its own paragraph with its own S1.

**Fix S6:**
- **Original**: "Taken together, these results underscore the crucial importance of spectral restructuring for efficient language model compression."
- **Revised**: "These results show that spectral restructuring is the primary driver of compression gains across scales and compression budgets."
- **Why**: The original gives no analytic content beyond re-asserting importance; the revision specifies the mechanism claim the evidence actually supports.

---

```
 2. Density:    S1: ~filler — mechanical signpost, advances no argument.
                S2: +new (WikiText-2 claim introduced). But see Check 6:
                    "remarkable" unsupported.
                S3: +new (LLaMA-7B numbers, 42.1 → 11.4).
                S4: +new (five-architecture robustness).
                S5: +new (compression-ratio trend) + ~filler participial tail
                    ("which contributes to our understanding of how model
                    scale interacts with low-rank approximation quality"
                    — no new information, just announces that information exists).
                S6: ~filler ("Taken together, these results underscore the
                    crucial importance of X" restates S2's claim without
                    analytic advancement).

                MAJOR: S1 and S6 are deletable; S5 tail is deletable.
```

---

```
 3. Claims:     S2: "remarkable improvements" — booster, not a problem by
                    itself, but S2 needs a table/figure reference.
                    [Needs verification — table not available]
                S3: "significantly better than all competing methods" —
                    TWO issues:
                    (a) "significantly" implies statistical significance;
                        use "substantially" or cite the margin explicitly.
                    (b) "all competing methods" — scope requires table ref
                        or explicit list. [MAJOR: scope qualifier missing]
                S4: "robust across five architectures up to 13B parameters"
                    — "five architectures" and "13B" need table/figure ref.
                    [Needs verification — table not available]
                S5: "improvements become more pronounced for higher
                    compression ratios" — no inline numbers, no figure ref.
                    Unsupported claim. [MAJOR: evidence missing]
                S5 tail: "model scale interacts with low-rank approximation
                    quality" — S5's main clause is about compression ratios;
                    the tail shifts to model scale. These are different
                    variables. Logic inconsistency. [MAJOR]
```

**Fix S3 scope:**
- **Original**: "which is significantly better than all competing methods"
- **Revised**: "outperforming all baselines in Table X by at least Y ppl"
- **Why**: "All competing methods" is unfalsifiable without explicit scope; the margin makes the claim refutable.

**Fix S5:**
- **Original**: "Additionally, we observe that the improvements become more pronounced for higher compression ratios, which contributes to our understanding of how model scale interacts with low-rank approximation quality."
- **Revised**: "At higher compression ratios, the perplexity gap widens (Figure X), indicating that spectral restructuring becomes increasingly critical as the low-rank budget tightens."
- **Why**: Removes throat-clearing ("we observe that"), replaces missing evidence (Figure X placeholder), corrects the variable confusion (compression budget, not model scale), and converts the participial tail into a falsifiable mechanism claim.

---

```
 4. Transitions: S1→S2: "Furthermore" asserts extension but S2 is the
                         paragraph's actual claim — the true relation is
                         Setup→Claim. "Furthermore" masks this. [MAJOR]
                 S2→S3: "Specifically" — Specification. Correct. [OK]
                 S3→S4: No connector. S3 (LLaMA-7B) → S4 (five architectures)
                         is an implicit Extension/Generalization. Logical and
                         readable. [OK, minor: "This advantage holds across..."
                         would make the extension explicit]
                 S4→S5: "Additionally" — masks genuine gap. S4 is about
                         architectural breadth; S5 introduces a new finding
                         (compression-ratio trend). These are parallel
                         findings, not extensions of each other. Removing
                         "Additionally" exposes the gap. [MAJOR]
                 S5→S6: "Taken together" — flagged opener (Check 6D).
                         Relation is Summary. The summary adds no new logical
                         step: it simply restates importance. [MINOR — see
                         Check 6]
```

**Fix S1→S2 connector:** Once S1 is rewritten as the claim, S2 becomes the evidence sentence and "Furthermore" is eliminated.

**Fix S4→S5:** The compression-ratio finding requires a new topic sentence in its own paragraph. If kept in this paragraph, "Additionally" must be replaced with a sentence that names why the finding is shown here: e.g., "Beyond architectural breadth, the gap also scales with compression budget:"

---

```
 5. ¶ bridge:   Skipped — no preceding paragraph provided.

 6. De-AI:      A. AI fingerprints:
                   "Having established X, we now turn to Y" (S1) —
                   canonical AI-signpost construction. [MAJOR — see Check 1]
                   "we observe that" (S5) — throat-clearing. Delete.

                B. Boosters/stakes-raisers:
                   "remarkable improvements" (S2) — booster; let numbers carry
                   weight. [MINOR]
                   "significantly better" (S3) — ambiguous (statistical vs
                   colloquial). [MINOR: use "substantially" or quantify margin]
                   "crucial importance" (S6) — booster. [MINOR: delete;
                   the evidence demonstrates importance without annotation]
                   "contributes to our understanding" (S5) — stakes-raiser
                   that promises insight but delivers none. [MAJOR — see S5 fix]

                C. Register:
                   "utilising" (S3) → "using". No precision gained from
                   Latinate form. [MINOR]
                   "demonstrates" (S2) → "shows" is simpler; borderline.
                   [MINOR]

                D. Structural noise:
                   "Taken together," (S6) — flagged opener. [MINOR: delete]
                   "Furthermore," (S2) — gap-masking connector. [MAJOR: see
                   Check 4]
                   "Additionally," (S5) — gap-masking connector. [MAJOR: see
                   Check 4]

                Tense: present throughout for findings. Consistent. [OK]

                De-AI escalation: Check 6 surfaces 2+ MAJOR issues (S1
                signpost, "Furthermore", "Additionally", participial
                stakes-raiser). Recommend running /deai-latex on the full
                Experiments section for a systematic pass.

 7. Section:    Experiments rule: claim-first, not number-first.
                S1 violates this: structural narration before any claim.
                [MAJOR — already addressed in Check 1]
                S3 correctly leads with the mechanism ("reduces perplexity")
                then numbers — local OK.
                S5: editorializing ("contributes to our understanding") in
                Results belongs in Discussion. [MAJOR — see Check 8]

 8. Boundary:   S5 tail ("which contributes to our understanding of how
                model scale interacts with low-rank approximation quality")
                — interpretive insight belongs in Discussion, not Results.
                [MAJOR]
                All other sentences present results or robustness evidence —
                correct Experiments content.

 9. Formulas:   Skipped — no mathematical notation in this paragraph.

10. Consistency: Skipped — single paragraph, no adjacent context provided.
```

---

## Revised Paragraph (minimal-change)

> Our whitening-based approach consistently outperforms all evaluated baselines on WikiText-2 across model scales. On LLaMA-7B, using our method reduces perplexity from 42.1 to 11.4 (Table X), outperforming all baselines by at least [Y] ppl. The gains hold across five architectures up to 13B parameters. At higher compression ratios, the perplexity gap widens (Figure X), indicating that spectral restructuring becomes increasingly critical as the low-rank budget tightens.

*(The compression-ratio finding in S5 is strong enough to open its own paragraph with a proper claim sentence. Splitting is recommended if space allows.)*

---

## Issue Summary

| # | Severity | Issue |
|---|----------|-------|
| S1 | **MAJOR** | Mechanical signpost wastes topic position |
| S2 | **MAJOR** | "Furthermore" masks Setup→Claim relation; "remarkable" unsupported |
| S3 | **MAJOR** | "all competing methods" lacks scope qualifier; "significantly" ambiguous |
| S4→S5 | **MAJOR** | "Additionally" masks a genuine gap between two distinct sub-findings |
| S5 | **MAJOR** | Compression-ratio claim unsupported (no ref/numbers); variable confusion (compression ratio ≠ model scale) |
| S5 tail | **MAJOR** | Interpretive content belongs in Discussion |
| S6 | **MAJOR** | Empty analytic conclusion; "Taken together" flagged opener; "crucial" booster |
| S3 | Minor | "utilising" → "using" |
| S2 | Minor | "demonstrates" → "shows" |

**Recommendation**: Check 6 surfaces 2+ MAJOR de-AI issues — consider running `/deai-latex` on the full Experiments section.
