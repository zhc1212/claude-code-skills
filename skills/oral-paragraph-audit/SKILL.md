---
name: oral-paragraph-audit
description: Use for paragraph-level academic writing audits in ML/NLP papers targeting top venues (EMNLP, NeurIPS, ICML, ACL, ICLR). Trigger when the user asks to review paragraph flow, logic, information density, sentence transitions, claim-first structure, redundancy, formula rigor, content placement, or submission-readiness for a specific paragraph or section excerpt. Also trigger on "检查一下这段", "audit this paragraph", "oral quality check", "帮我看看这段写的怎么样", or any request to review a specific paragraph from a paper. Do not use for grammar-only proofreading, translation, whole-paper outlining, or full-section drafting.
---

# Oral-Level Paragraph Audit

Structured 10-check review for individual paragraphs in ML/NLP papers. Each check targets a specific class of issue that top-venue reviewers penalize.

## Scope

Audit one paragraph at a time, or a multi-paragraph excerpt for cross-paragraph consistency. For multi-paragraph input, run Checks 0–9 on each paragraph separately, then run Check 10 (Terminology and Logic Consistency) on the group. Preserve all technical claims, citations, and scope qualifiers — do not strengthen or weaken claims.

**Context gathering**: when auditing a single paragraph from a file, always read the immediately adjacent paragraphs (preceding and following) to enable Check 5 (¶ bridge) and Check 10 (consistency). Only skip these checks if the paragraph is truly provided in isolation with no file path to read from.

**Minimal-change rule**: prefer the smallest edit that fixes the issue. Do not rewrite a paragraph wholesale unless sentence order or claim structure is broken. If no Blocking or Major issues exist, say so and skip rewrites.

**Zero-skip principle**: this skill targets oral-level quality — the highest tier of academic writing. Every check must be executed thoroughly on every sentence, with evidence shown in the output. Do not shortcut any check with a bare "OK" — show the reasoning. For Check 4 (Transitions), enumerate every S(n)→S(n+1) pair with its relation type. For Check 2 (Density), assess every sentence individually. For Check 3 (Claims), list every claim and its evidence status. A check that says "OK" without showing work is a failed audit. The goal is zero issues surviving to reviewer — if the audit passes, the paragraph should withstand a top-5% reviewer at any ML venue.

## Writing Philosophy

The 10 checks below are not arbitrary style rules — they are grounded in how reviewers actually read papers at top venues.

**The reviewer's situation.** A reviewer handles 3–6 papers per cycle, each in 2–3 hours, alongside their own research deadlines. They are pattern-matching for quality signals. When a paragraph feels unclear, they do not re-read it — they note "writing could be improved" and move on. Every point of friction is a micro-deduction that compounds across the paper. Oral-quality writing eliminates this friction entirely.

**Oral vs. Poster vs. Workshop** — the difference is not vocabulary or polish. It is information architecture:

| Tier | Reader experience |
|------|------------------|
| Workshop | Ideas are present; reader works to extract them |
| Poster | Ideas are clear; reader occasionally re-reads or looks back |
| **Oral** | Ideas land on first read — zero re-reading, zero backtracking, zero guessing |

**Eight principles that drive the checks:**

1. **Every sentence earns its place.** Page limits are hard. A sentence that restates what the reader already knows, or adds vague commentary ("demonstrating the effectiveness"), wastes the reader's limited attention budget. If removing a sentence loses no information, remove it. *(Drives Checks 2, 6)*

2. **Claims and evidence travel together.** When a reviewer reads "X outperforms Y," they immediately look for the number or table reference. If the evidence is two paragraphs away, the claim feels unsupported — even if the data exists elsewhere in the paper. Oral papers never make the reviewer search. *(Drives Check 3)*

3. **The paragraph is the unit of argument.** S1 tells the reader what this paragraph will prove. The rest proves it. A reviewer skimming only the S1 of each paragraph should be able to reconstruct the paper's full argument. If S1 is raw data without a claim, or a transition without a destination, the paragraph fails its structural role. *(Drives Checks 0, 1, 4, 5)*

4. **Content lives in the right place.** A correct sentence in the wrong section is noise. Method explains *what and why*; Experiments explains *how and with what*. Mixing them signals the author cannot separate design from implementation. *(Drives Check 8)*

5. **Formulas must be locally readable.** A reviewer should understand every symbol in a formula without flipping back. Undefined symbols, inconsistent subscripts, or implicit summations break trust in the technical work. *(Drives Check 9)*

6. **Do not multiply entities beyond necessity.** Every symbol, acronym, subscript convention, and terminology variant is a cognitive slot the reader must maintain. If two names refer to the same object (P_ℓ and P_{ℓ+1} for the same probe), pick one. If a shorthand saves three characters but introduces ambiguity (σ for softmax when σ also means singular value), spell it out. If a concept can be described in prose, do not introduce notation for it. This applies everywhere: Method (symbols), Related Work (taxonomy axes), Experiments (metric names), Abstract (jargon). *(Interacts with all checks, especially 2, 8, 9)*

7. **Each paragraph must create reader value.** A paragraph that only reports what the authors did — without explaining why that fact matters to the target community — is dead weight. Before auditing structure or style, ask: what reader-relevant problem, uncertainty, or decision does this paragraph help resolve? If the answer is "none," no amount of polish will save it. An Experiments paragraph listing three datasets and two metrics is not valuable until it tells the reader what question the experiment answers. *(Drives Checks 0, 1, 3; inspired by [McEnerney's reader-value framework](https://henryleach.com/2016/05/the-craft-of-writing-effectively/))*

8. **The most important information lands at the end of the sentence.** Readers assign extra weight to whatever occupies the "stress position" — the end of a clause or sentence ([Gopen & Swan, 1990](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf)). A sentence that buries its key number or finding in the middle and trails off with a qualifier wastes its strongest structural slot. Conversely, putting context and setup at the beginning ("topic position") lets the reader orient before encountering the payload. *(Drives Check 4, interacts with Check 1)*

These principles interact: a paragraph with good structure (Principle 3) but low density (Principle 1) wastes a well-framed argument on filler. A dense paragraph with decoupled claims (Principle 2) is informative but unconvincing. A well-structured paragraph with buried findings (violating Principle 8) forces the reader to re-scan for the point. A paragraph with good structure, density, and evidence that nevertheless fails to address a reader-relevant question (violating Principle 7) is technically correct but strategically useless. Oral quality requires all eight simultaneously.

## Procedure

1. Identify the section type (abstract, intro, related work, method, experiments, discussion, conclusion).
2. Run the 10 checks in order (Check 0 first if section context available; Check 9 only for Method/Appendix paragraphs with formulas).
3. Classify findings by severity:
   - **Blocking**: likely harms reviewer understanding, credibility, or perceived contribution.
   - **Major**: noticeably weakens clarity, evidence, or flow but does not invalidate the paragraph.
   - **Minor**: style or polish issue with low effect on reviewer judgment.
4. Provide replacement text with brief reasoning for **all** issues (Blocking, Major, AND Minor). At oral level, Minor issues accumulate into reviewer friction — they deserve concrete fixes, not just flags.
5. Show the work for every check. A check that outputs bare "OK" without evidence (e.g., which sentences were assessed, which pairs were compared) is incomplete. The audit output IS the proof that every sentence was examined.
6. Note what works well — good feedback includes strengths, not just problems.

## The 10 Checks

### 0. Section Role: Where Does This Paragraph Fit?

*Does this paragraph help the section do its job?* (Distinct from Check 7 "does it follow section conventions" and Check 8 "does every sentence belong here".)

Before auditing the paragraph itself, identify its role in the surrounding section or subsection. Ask:
- What is this section's logical structure? (parallel, progressive, chronological, contrastive)
- What role does this paragraph play? (opening claim, supporting evidence, hedge/limitation, transition, summary)
- Does the paragraph's role follow logically from the previous paragraph and lead into the next?

Common section structures and expected paragraph roles:

| Structure | Typical sections | Paragraph sequence |
|-----------|-----------------|-------------------|
| **Progressive** (A→B→C) | Discussion, Intro | observation → mechanism → implication |
| **Parallel** (A, B, C) | Related Work, Ablations | each ¶ covers one independent dimension |
| **Claim→Evidence** | Experiments subsections | claim ¶ → supporting ¶s with data |
| **Setup→Derivation** | Method | motivation → formulation → interpretation |

Flag when:
- A paragraph's role contradicts the section's structure (e.g., a parallel section has a paragraph that assumes the previous paragraph's conclusion)
- A `\paragraph{}` heading promises one topic but the content delivers another
- The section mixes structures without signaling the shift

If only one paragraph is provided without section context, report "Check 0: skipped (no section context)."

### 1. Structure: Topic–Support Coherence (总分结构)

Every paragraph must have a clear **topic–support** structure: S1 states the paragraph's message, and every subsequent sentence supports, refines, or provides evidence for that message. This is the single most important structural property of oral-quality writing — a reviewer skimming only the S1 of each paragraph should be able to reconstruct the paper's full argument.

**Step A — Verify S1 states the message:**

| Section | Good S1 | Acceptable alternative |
|---------|---------|----------------------|
| Experiments | Claim: "Our method outperforms all baselines" | Contrastive: "Skipping X preserves Y but degrades Z" |
| Discussion | Insight: "Error X is the dominant source" | — |
| Conclusion | Contribution: "We showed that X is the mechanism" | — |
| Method | Setup: "To close this gap, we jointly optimize..." | Definition: "Let f denote the block function..." |
| Related Work | Taxonomy: "Prior methods vary along three axes" | Gap: "None of these approaches optimizes at block scope" |
| Abstract | Achievement: "We build X" | Problem S1 OK if S2 immediately pivots |
| Intro ¶final | Thesis: "We argue that the unit should be..." | — |
| Comparison ¶ | Positioning + question: "X is the closest prior method, making it a test of..." | Contrastive: "Unlike X, our approach..." |

Not rigid: setup→claim ("Prior work assumes X. We show Y.") is fine. Flag only when S1 is raw data with no framing.

**Step B — Verify every sentence supports S1:**

For each S(i) where i > 1, name its role relative to S1:

| Role | Description | Example |
|------|-------------|---------|
| Evidence | Provides data, numbers, or table refs supporting S1's claim | "Table 2 confirms a 4.9% improvement." |
| Mechanism | Explains why or how S1's claim holds | "This occurs because frozen factors cannot compensate..." |
| Refinement | Adds nuance, scope, or condition to S1 | "The effect is strongest at ρ=0.6." |
| Contrast | Shows what does NOT work, strengthening S1 by elimination | "In contrast, uniform allocation degrades to 12.26." |
| Consequence | States what follows from S1 | "This makes the profile a reusable primitive." |

Flag **MAJOR** when a sentence cannot be assigned any of these roles relative to S1 — it is off-topic and either belongs in a different paragraph or should be deleted. A paragraph with two unrelated claims in S1 and S4 should be split into two paragraphs.

**Step C — Check for mixed messages:**

If the paragraph has two distinct claims that cannot be unified under S1's message, flag **MAJOR: mixed messages — split into separate paragraphs**. A single paragraph should carry one argument, not two.

### 2. Information Density

For each sentence: does it add something the reader does not already know from (a) this paragraph, or (b) other sections? Assess every sentence individually — in the output, mark each as `+new` (adds information), `=echo` (restates prior sentence), or `~filler` (adds no information).

**Red flags**:
- A sentence restating what the previous sentence already implied (`=echo`)
- Participial tails echoing the main clause ("...demonstrating the effectiveness of...") (`~filler`)
- Unchanged repetition of a claim across sections (repetition is fine when the function changes: motivation in intro, evidence in experiments, interpretation in discussion)
- **Boilerplate formalisms** ([Farquhar](https://sebastianfarquhar.com/on-research/2024/11/04/how_to_write_ml_papers/)): restating standard definitions readers already know (e.g., the RL formalism, the transformer architecture) belongs in an appendix, not in the body — "put this in Appendix A and reference it"
- **Metadiscourse repetition**: "In this paper, we propose" is fine once; repeating it across intro, method, and conclusion is wasted words

**Number density**: Discussion/Conclusion with >3 inline numbers is result-recapping, not interpreting. Replace with qualitative language + table/figure refs.

### 3. Claim-Evidence Alignment

Every strong claim needs support within or near the paragraph:

| Claim type | Required support |
|-----------|-----------------|
| "X outperforms Y" | Table/figure ref or inline number |
| "X is essential/necessary" | Ablation ref or contrastive evidence |
| "X is the first/only/novel" | Citation gap or explicit novelty argument |
| "significantly improves" | Quantified improvement, not just the word |

**Overclaim watchlist**: "solves", "significantly", "dramatically", "universal", "robust" — flag when used without evidence or scope control in the same paragraph.

**Scope qualifier check**: strong claims need explicit scope boundaries. Common fixes:
- "optimal" → "optimal for this surrogate" (specify which objective)
- "cannot recover" → "did not recover under the tested configurations" (empirical, not universal)
- "is essential" → "is essential at ρ=0.6; the gap narrows at lower compression" (state conditions)
- "outperforms all baselines" → add "at every tested ratio" or "on LLaMA-7B" (bound the claim)
- "X causes Y" → "X correlates with Y" unless a controlled intervention proves causation (observing A and B together is correlation, not cause)

A claim without scope reads as universal — reviewers will find the counterexample you didn't mention.

**Narrative arc completion**: if S1 frames a research question or comparison ("X is a natural test of whether..."), the paragraph must answer it by the final sentence. A framing sentence that opens a question without closing it leaves the reader suspended — they expected a resolution and got none. This is distinct from claim-evidence alignment: even if every claim has evidence, the paragraph fails if it doesn't answer the question it posed.

**Refutable claims** ([SPJ](https://simon.peytonjones.org/great-research-paper/), [Lipton](https://www.approximatelycorrect.com/2018/01/29/heuristics-technical-scientific-writing-machine-learning-perspective/)): a claim must be specific enough that a reader can tell whether it is true. "Our method is effective" is not refutable. "Our method reduces WikiText-2 perplexity by 2× at ρ=0.6 on LLaMA-7B" is. Flag vague praise masquerading as a contribution.

**Explanation vs speculation**: if the paragraph explains *why* a result occurs ("the improvement suggests the model learns better compositional structure..."), the explanation must be either (a) directly supported by evidence in this paragraph, (b) cited, or (c) explicitly framed as a hypothesis ("we conjecture that..."). Unmarked speculation after a results table is a common source of reviewer distrust, especially in Discussion and Analysis paragraphs.

**Baseline description accuracy**: when a sentence describes what another method does (e.g., "Method X optimizes per-layer"), the description must match what the cited paper actually does. Inaccurate descriptions of baselines are factual errors that knowledgeable reviewers — who may have authored the baseline — will catch. If unsure about a baseline's exact mechanism, flag as "Needs verification" rather than guessing.

### 4. Sentence-to-Sentence Transitions

Every S(n) → S(n+1) pair needs a nameable logical relation:

| Relation | Typical signals |
|----------|----------------|
| Cause | thus, so, because |
| Contrast | but, however, yet, while |
| Evidence | as shown in, Table X confirms |
| Consequence | therefore, as a result |
| Refinement | specifically, in particular |
| Extension | also, the same pattern |
| Setup | given X, starting from |
| Limitation | however, this does not capture |

Flag only when the relation is unclear or forces the reader to infer a missing step. Good prose often has implicit continuity — do not insert explicit connectors where none are needed.

**Mandatory enumeration**: list every S(n)→S(n+1) pair with its relation type in the output. Do not summarize as "OK" without showing the work. Missing one pair in a 7-sentence abstract means missing ~15% of the checks; in a 15-sentence method paragraph, it means a potential logical gap goes undetected. Every pair, every time.

**Sentence-level clarity** ([Gopen & Swan](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf), [Ethan Perez](https://ethanperez.net/easy-paper-writing-tips/)): beyond transitions, audit each sentence for these micro-level properties:

- **Topic and stress positions**: sentence beginnings ("topic position") should provide context or old information. Sentence endings ("stress position") should carry the new, emphasized material. Key numbers and findings must land at or near the sentence end. Anti-pattern: "Accuracy improves by 15% when using attention" → Better: "When using attention, accuracy improves by 15%."
- **Subject-verb proximity** (Gopen & Swan principle 1): keep subject and verb close. A long modifier between them forces the reader to hold the subject in memory. Anti-pattern: "The model, which was trained on 256 calibration samples from WikiText-2 with a sequence length of 2048, achieves..." → Better: "The model achieves... (trained on 256 WT2 samples, seqlen 2048)."
- **Pronoun clarity** (Perez): minimize bare pronouns ("this", "it", "these"). Use "this" only as an adjective — "this result", "this pattern" — never standalone. Anti-pattern: "This shows that..." → Better: "This ablation shows that..."
- **Verb-early** (Perez): position the main verb early in the sentence. Late verbs force the reader to hold unresolved structure. Anti-pattern: "The gap between the static allocation and the post-training optimum, which widens as factors improve under optimization, is..." → restructure so verb arrives sooner.

Flag as MINOR unless the issue forces re-reading — then MAJOR.

### 5. Paragraph-to-Paragraph Transitions

Compare S1 of the current paragraph against the final sentence of the previous paragraph. If the previous paragraph is not available, report "skipped (no preceding context)."

A `\paragraph{}` heading handles topic switches — no bridge sentence needed. Otherwise, verify:

- **Linkage**: S1 of the new paragraph references a concept, result, or term from the previous paragraph's final sentence (explicit) or from its established topic (implicit). If neither, the transition is a jump.
- **Progressive vs. reset**: in progressive sections (Intro, Discussion), each ¶ should build on the previous one. A paragraph that resets the topic without signaling ("Separately,...", "A second consideration is...") feels disjointed.
- **Acceleration**: the argument should feel like it's moving forward, not circling. If S1 of the new paragraph could have been S1 of the previous paragraph (i.e., they're at the same level of the argument), flag — one of them should be subordinated or deleted.

### 6. De-AI Pass

Flag only when a pattern harms precision, rhythm, or reviewer trust — not mechanically.

- **Watchlist words** (flag when vague, not every occurrence): leverage, delve, crucial, pivotal, landscape, underscore, showcase, nuanced, profound, foster, vibrant, elucidate, seamless, intricate
- **Em dashes**: >1 per paragraph is a yellow flag
- **Negative parallelism**: "not only X but also Y" → usually cleaner as "X and Y"
- **Participial tails**: sentence-final "-ing" that merely restates the result → trim
- **Weak copula**: "serves as" / "stands as" when "is" is more direct
- **Throat-clearing**: "It is worth noting that" → delete filler
- **Forced triples**: AI groups items in threes for false comprehensiveness
- **Semicolon overuse**: AI text overuses semicolons to join parallel clauses. Human authors split into two sentences or use a conjunction. Flag >2 semicolons per paragraph in prose (math/caption semicolons are fine)
- **Uniform sentence length**: if all sentences in the paragraph are within ±5 words of each other, the rhythm is monotonous — vary by mixing short (8-12 words) with longer sentences (20-30 words)
- **Synonym cycling**: AI rotates near-synonyms to avoid repetition (method/approach/technique/framework for the same concept). In academic writing, consistent terminology is clearer than elegant variation — pick one term, use it everywhere
- **Passive voice clusters**: a single passive is fine; three consecutive passives signal AI and weaken agency. Rewrite at least one with an active subject
- **Paired adjectives**: "robust and effective", "efficient and scalable" — pick the more precise one. If both matter, they deserve separate evidence, not a conjunction
- **Informal intensifiers**: "well beyond", "quite", "very", "highly", "really" — remove when they add emphasis without precision
- **Verb doublets**: "generated and amplified", "designed and developed" — pick one; two near-synonyms joined by "and" is AI hedging

**Guardrail**: if a flagged pattern reads clearly and precisely in context, keep it.

**Escalation**: if Check 6 surfaces 2+ MAJOR issues, recommend running `/deai-latex` on the full section for a comprehensive de-AI pass — Check 6 is a spot-check, not an exhaustive rewrite tool.

### 7. Section-Specific Rules

**Abstract**: Should cover problem, method, main result, and implication, but order may vary. In addition to the general checks, apply these abstract-specific rules:

- **No bare math symbols.** Every symbol in the abstract must be either (a) universally standard (e.g., $n$, $k$, $\mathcal{O}$) or (b) defined in the same sentence. Symbols defined only in the Method section (e.g., $r_{\max}$, $\tau$, $B_{\text{target}}$) are bare — replace with prose ("full-rank", "temperature", "parameter budget"). Severity: **MAJOR** — bare symbols force the reader to guess or skip.
- **No unexplained method-name jargon.** Specific method names from other papers (e.g., "ASVD", "Dobi-SVD", "FermiGrad") are opaque to readers unfamiliar with those works. Replace with descriptive phrases ("all tested static allocation methods", "prior sensitivity-based profiles") unless the method name IS the contribution being compared (i.e., the paper's own method name is fine). Severity: **MAJOR** — the abstract must be self-contained; a reader should not need to know the related work to understand the comparison.
- **Expand all abbreviations** on first use unless universally standard in the target venue (LLM, SVD, PPL are standard at ML venues; STRS, OOD, STE are not).
- **No section or table references** (`\S\ref{...}`, `Table~\ref{...}`). The abstract is read in isolation (search results, proceedings index).

**Introduction**: Progressive structure: problem → challenge → positioning. Each paragraph carries one message.
- Opening ¶: task importance + landscape (not problem + solution mixed together).
- Challenge ¶(s): lead to the EXACT technical challenge solved; do not present naive baseline then improve it (this makes work look incremental).
- Solution ¶: insight first, then method name, then surprise/key finding.
- Final ¶ (or contribution list): Thesis → method sketch → headline number → scope → deepest insight. Every contribution claim must be verifiable in Experiments.

**Related Work**: One dimension per paragraph, end with gap or positioning. A brief positioning sentence ("In contrast, we...") is acceptable if it clarifies the gap. Check **baseline description accuracy**: when describing what another method does, the description must match what the cited paper actually does — knowledgeable reviewers (who may have authored the baseline) will catch inaccuracies.

**Limitations**: Candid tone expected. Claims need not be contribution-forward. Flag only vague hedging or missing concrete detail.

**Dataset/Setup**: Factual and enumerative by design. Check 1 (claim-first) does not apply — focus on completeness and clarity.

**Method**: Definition → equation → interpretation ordering within each math paragraph. Design paragraphs: motivation → mechanism → advantage. One idea per paragraph. Check that hyperparameters (lr, optimizer, steps) are NOT here — they belong in Experiments Setup.

**Experiments**: Claim-first, not number-first. Ablations may open with contrastive finding. Each experiment paragraph must state what claim it supports and how.

**Discussion**: Insight-first, evidence-second. Structure: observation → mechanism → implication. Numbers should be rare — point to sections/tables instead of re-listing data. Flag **unmarked speculation**: if a sentence explains *why* a result occurs, it must be either (a) supported by evidence in the paragraph, (b) cited, or (c) explicitly framed as a hypothesis ("we conjecture that..."). Unmarked speculation after a results table is a major source of reviewer distrust.

**Conclusion**: Short. Contribution → evidence → finding → punchline. No problem restatement at S1. Lead with the insight, not the method name.

### 8. Content Boundary

*Does every sentence belong in this section?* (Check 0 asks whether the paragraph serves the section's argument; Check 7 asks whether it follows conventions; Check 8 asks whether individual sentences are placed in the right section.)

Each section has a defined scope. Content outside that scope is noise — it distracts the reviewer and signals that the author does not know what goes where. This check asks: does every sentence in this paragraph belong in this section?

| Section | Belongs | Flag if present |
|---------|---------|----------------|
| **Method** | Definitions, formulas, motivation for design choices, algorithms, notation | Hyperparameters (lr, optimizer, steps), hardware, dataset sizes, specific benchmark numbers, evaluation protocol |
| **Experiments Setup** | Datasets, metrics, baselines, hyperparameters, hardware, evaluation protocol | New notation, method motivation, proofs, design rationale |
| **Experiments Results** | Claims with table/figure refs, comparisons, analysis of numbers | Method definitions, setup details already stated, re-derivation of formulas |
| **Related Work** | Prior methods, taxonomy, gap statement, positioning | Own method details, own experimental numbers |
| **Introduction** | Problem, motivation, headline numbers (1-2), contributions list | Full method derivation, detailed comparisons, hyperparameters |
| **Abstract** | Problem, approach (one sentence), main result, implication | Notation, detailed method, per-table breakdowns |
| **Conclusion** | Contributions, key findings, limitations, future work | New results not in Experiments, new method details |

Boundary violations are contagious — one misplaced sentence invites more. Flag early.

**Common violations from real editing sessions:**
- Method paragraph listing optimizer and learning rate (belongs in Experiments Setup)
- Method paragraph citing specific perplexity numbers as motivation (use qualitative language: "far above the dense model" instead of "42.1 vs 5.68")
- Experiments paragraph re-defining notation already established in Method
- Algorithm pseudocode including experimental hyperparameters as REQUIRE parameters

### 9. Formula Rigor (Method and Appendix only)

Skip this check for non-technical sections. When auditing a paragraph that contains or references mathematical formulas, verify:

**Symbol hygiene:**
- Every symbol is defined near its first use in the paragraph (within the same paragraph or the immediately preceding one), or was defined earlier in the section and is being reused consistently. When prior context is unavailable, flag as "Needs context — cannot verify" rather than Blocking
- No symbol is used with two different meanings (e.g., σ for both softmax and singular value)
- Subscript/superscript notation is consistent across all equations in the paragraph (e.g., do not mix $P_\ell$, $P_{\ell+1}$, and $P_k$ for the same object)

**Dimensional consistency:**
- Matrix-vector products have compatible shapes (state shapes if not obvious: "where $W \in \mathbb{R}^{m \times n}$ and $h \in \mathbb{R}^n$")
- Outputs of operations match expected types (softmax → probability simplex, norm → scalar)

**Completeness:**
- Optimization objectives show what is being optimized over (missing $\min_\theta$ or $\sum_i$)
- Averaging/summation over data points is explicit, not implicit (a bare $D_\text{KL}$ without $\frac{1}{N}\sum_i$ is ambiguous)
- The domain/range of functions is clear from context or stated

**Notation consistency with the rest of the paper:**
- If the paper defines $\bar{h} := \text{RMSNorm}(h)$ in one place, do not switch to $\text{LayerNorm}$ notation elsewhere
- Composition operators are consistent ($\circ$ vs $\cdot$ vs juxtaposition)
- Bold/non-bold distinction for vectors/scalars is maintained if established

Flag BLOCKING when a reviewer reading only this paragraph would be confused about what a symbol means, or would conclude the formula has a dimensional error.

### 10. Terminology and Logic Consistency (multi-paragraph only)

When auditing a single paragraph, read the immediately adjacent paragraphs (preceding and following) to check terminology and logic consistency — paragraphs in a section are not isolated. Only skip if no surrounding context is available at all. When auditing multiple paragraphs or a full section:

**Terminology stability**: flag when the same concept is called by different names across paragraphs (e.g., "rank profile" in ¶1 vs "allocation vector" in ¶3 vs "rank distribution" in ¶5). Pick one term and use it consistently. Synonym cycling is a common AI writing pattern AND a common source of reviewer confusion.

**Cross-paragraph logic**: flag contradictions between paragraphs (e.g., Method says "freeze parameters" but Discussion says "co-adapt end-to-end"). Also flag when a claim in one paragraph undermines or contradicts evidence in another.

**One message per paragraph**: verify that each paragraph carries exactly one message. If a paragraph has two distinct claims, it should be split. If two paragraphs make the same claim, one should be deleted or merged.

**Acronym scope**: abbreviations must be expanded at first use in each major scope boundary (abstract is a separate scope from body; appendix is a separate scope from main text).

## Output Format

For each paragraph:

```
¶ [section / heading]

Section role: [structure type] — this ¶ serves as [role]. [OK / MAJOR: role mismatch]
Strengths: [what works well]

1. Structure:   S1 message: "[quote S1's claim]"
               S2: [role]. S3: [role]. ... Sn: [role].
               [OK / MAJOR: S_ off-topic / mixed messages]
2. Density:     S1: [+new/=echo/~filler]. S2: [...]. ... Sn: [...].
               [OK / MAJOR: S_ repeats ...]
3. Claims:      [OK / MAJOR: "X" unsupported / scope missing]
4. Transitions: [enumerate every pair:]
               S1→S2: [relation]. S2→S3: [relation]. ... S(n-1)→S(n): [relation].
               [then: OK / BLOCKING at S_→S_: ...]
5. ¶ bridge:    [OK / skipped / MAJOR: ...]
6. De-AI:       [PASS / MINOR: ...]
7. Section:     [OK / MAJOR: ...]
8. Boundary:    [OK / MAJOR: S_ belongs in {Experiments/Setup/...}]
9. Formulas:    [OK / skipped / BLOCKING: symbol X undefined / notation inconsistent]
10. Consistency: [OK / skipped (single ¶) / MAJOR: terminology drift / logic contradiction]
```

For each BLOCKING/MAJOR fix, provide:
- **Original**: the problematic text
- **Revised**: the replacement
- **Why**: one-sentence reasoning

## Examples

### Good audit (thorough, zero-skip compliant):

Input (Experiments):
> "42.1 drops to 19.1 after block optimization and 11.4 after full-model optimization. The gains are robust across five architectures. This demonstrates the effectiveness of our approach."

```
¶ Experiments / Overall Performance

Section role: Claim→Evidence — this ¶ serves as opening claim. BLOCKING: opens with data, not claim
Strengths: concrete numbers, clear progression across levels

1. Structure:   S1 message: "42.1 drops to 19.1..." — raw data, no claim.
               S2: Extension (adds scope). S3: ~filler (restates S1-S2 vacuously).
               BLOCKING — S1 leads with data, not a claim. S3 off-topic (generic praise).
2. Density:     S1: +new. S2: +new (adds architecture scope). S3: ~filler ("demonstrates effectiveness" adds nothing).
               MAJOR — S3 is vacuous restatement of S1-S2.
3. Claims:      "robust" — unsupported (no table ref, no scope). "effectiveness" — vague, not refutable.
               MAJOR — "robust" used without evidence; no scope qualifier.
4. Transitions: S1→S2: Extension (adds scope). S2→S3: Consequence (but vacuous).
               MAJOR at S2→S3 — "This demonstrates" adds no information.
5. ¶ bridge:    skipped (no preceding context)
6. De-AI:       "robust" (watchlist), "demonstrates the effectiveness" (participial tail), "This demonstrates" (bare pronoun).
               MAJOR — 3 AI patterns in 3 sentences.
7. Section:     BLOCKING — experiments ¶ must open with claim, not data.
8. Boundary:    S1: Experiments (OK). S2: Experiments (OK). S3: could be anywhere — generic.
               OK for S1-S2. MINOR for S3 (vacuous, belongs nowhere).
9. Formulas:    skipped (no formulas)
10. Consistency: skipped (single ¶)
```

- **Original**: "42.1 drops to 19.1 after block optimization and 11.4 after full-model optimization."
- **Revised**: "The three-level chain outperforms all SVD-family baselines, reducing WikiText-2 perplexity from 42.1 to 11.4 on LLaMA-7B (Table 1)."
- **Why**: claim-first structure; table ref grounds the evidence.

- **Original**: "The gains are robust across five architectures. This demonstrates the effectiveness of our approach."
- **Revised**: "The gains hold across five architectures up to 13B parameters (Table 2)."
- **Why**: "robust" → "hold" (precise); S3 deleted (adds nothing).

### Good audit — Method paragraph with formula (exercises Checks 8 and 9):

Input (Method):
> "The low-rank factors {A_j, B_j} are warm-started from L2 and updated end-to-end, while all other parameters remain frozen. The objective is min -∑ log p(x|...) where p is the compressed model's next-token probability computed with all weights W_j replaced by A_j B_j as the trainable variables."

```
¶ Method / L3 Objective

Section role: Setup→Derivation — formulation paragraph. OK.
Strengths: clear objective, notation defined.

1. Structure:   S1 message: "factors are warm-started and updated end-to-end"
               S2: Evidence (states the formal objective).
               OK — setup then formalization.
2. Density:     S1: +new. S2: +new but tail is =echo ("computed with all weights W_j replaced by A_j B_j" restates what the formula shows).
               MINOR — trim redundant tail.
3. Claims:      No empirical claims. OK.
4. Transitions: S1→S2: Refinement (S1 says what's optimized, S2 formalizes the objective). OK.
               Sentence clarity: S2 subject-verb gap is wide ("The objective is min -∑ log p(x|...) where p is..."). Verb "is" arrives early — OK. But S1 has "warm-started from L2" as a bare claim without "how" — Setup/Experiments boundary.
5. ¶ bridge:    skipped (no preceding context)
6. De-AI:       No watchlist words. No passive clusters. PASS.
7. Section:     Definition → equation → interpretation. OK.
8. Boundary:    S1 "warm-started from L2" — MAJOR: implementation detail belongs in Experiments Setup.
               S2 objective definition — OK for Method.
9. Formulas:    Loss lacks 1/N normalization (sum vs average ambiguous). MINOR.
10. Consistency: skipped (single ¶)
```

- **Original**: "are warm-started from L2 and updated end-to-end"
- **Revised**: "are the trainable parameters, updated end-to-end"
- **Why**: "warm-started from L2" is Experiments Setup, not Method definition.

### Bad audit (shallow, unhelpful — avoid this):

```
¶ Experiments
1. Structure: mixed
2. Density: could be improved
3. Transitions: mostly OK
4. De-AI: some issues
8. Boundary: fine
9. Formulas: N/A
```

This audit diagnoses nothing specific and provides no fixes. Always name the exact sentence, the exact problem, and the exact replacement.
