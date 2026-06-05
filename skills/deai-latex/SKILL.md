---
name: deai-latex
description: Remove AI-generated style from English LaTeX paper text — overused words, mechanical transitions, excessive em-dashes, semicolons, parentheses, listy structure. Triggers on "去AI味", "de-AI", "deai", "remove AI style", "humanize", "让文字更自然", "polish prose", "clean up writing", or when pasting ChatGPT/Claude-generated paper text. Also trigger after /oral-paragraph-audit when Check 6 escalates, or when the user asks to "改一下文字" or "润色" for paper LaTeX.
---

# De-AI LaTeX: Remove AI Writing Patterns from Academic Papers

## Your Task

If user hasn't provided LaTeX yet, ask: **"Please paste your LaTeX text."**

Rewrite LLM-generated mechanical text into natural academic prose for top-venue submission. Preserve technical meaning while removing vague, inflated, or template-like patterns.

**Section awareness**: identify which section the text belongs to (abstract, intro, method, experiments, discussion, conclusion). Different sections have different tolerances:
- **Discussion/Conclusion**: fewer inline numbers, more qualitative language
- **Experiments**: numbers are expected, focus on claim-first structure
- **Abstract**: must be self-contained, no bare math symbols
- **Method**: technical precision matters most, less de-AI needed

---

## Editing Procedure

1. Identify the paper section (abstract, intro, method, experiment, related work, limitation, conclusion).
2. Preserve all technical claims, variables, citations, numbers, comparisons, and scope qualifiers.
3. Edit only sentences that match a listed pattern or contain vague/inflated wording.
4. Prefer smaller edits over full rewrites.
5. After rewriting, verify that no claim became stronger, broader, or less precise than the original.

---

## Constraints

### 1. Vocabulary

Prefer plain, precise academic words. Avoid overused AI vocabulary.

**Watchlist** (flag when vague or inflated, not mechanically): leverage, delve into, tapestry, accentuate, amplify, underscore, unveil, nuanced, profound, pivotal, foster, harmonize, transcend, elucidate, substantiate, seamless, intricate, crucial, landscape (abstract), interplay, showcase, garner, enduring, vibrant

**Common replacements**: leverage → use, delve into → investigate, tapestry → context, elucidate → explain, substantiate → support, showcase → show, crucial → important

Replace only when the word sounds inflated, vague, or less precise than a simpler alternative. If the word is precise in context, keep it.

**Copula avoidance:** AI substitutes elaborate constructions for simple "is/are/has". "serves as a warm-start" → "is a warm-start". "stands as a key contribution" → "is a key contribution". Restore the copula.

**Inflated significance:** "plays a crucial/vital/key role in" → "contributes to" or just state the effect directly. "a wide range/variety of tasks" → "tasks" or "several tasks".

**Vague achievement claims:** Replace generic phrases with concrete claims tied to actual results. Avoid: "remarkable success", "significant improvements", "comprehensive experiments", "state-of-the-art performance", "sheds light on", "bridges the gap", "opens new avenues", "extensive experiments demonstrate". If the text provides numbers, use them. If not, narrow the claim.

### 2. Structure

- **Avoid unnecessary prose lists.** Convert `\itemize`/`\enumerate` to paragraphs when they merely split ordinary prose into bullets. Preserve lists that serve a conventional function: contributions, assumptions, algorithm steps, experimental settings, or limitations.
- **Remove mechanical connectives:** "First and foremost", "It is worth noting that", "Additionally", "Furthermore", "Moreover" at sentence starts. Also "In recent years" / "Recent advances in" openers — delete and start with the actual subject.
- **Trim vague participial tails.** Remove or rewrite sentence-final `-ing` clauses when they merely restate the result ("demonstrating the effectiveness of..."). Keep them when they express a precise mechanism, condition, or consequence.
- **Reduce em dashes (—):** Replace with commas, parentheses, or subordinate clauses.
- **Reduce semicolons (;):** AI overuses semicolons to join parallel clauses. Human authors more often split into two sentences or use a conjunction.
- **Reduce explanatory parenthetical clutter.** Keep standard academic parentheses for citations, acronyms, dataset details, and short clarifications. Rewrite only parentheticals that interrupt the sentence or hide important content (e.g., "the method (which uses SVD) achieves..." → "the SVD-based method achieves...").
- **Reduce rule-of-three:** AI forces ideas into groups of three to appear comprehensive. Two is fine. Four is fine. Don't force three.
- **Remove negative parallelisms:** "not only X but also Y" → "X and Y" or two sentences. "it's not just about X, it's about Y" → state Y directly.
- **Fix synonym cycling:** AI rotates synonyms to avoid repetition (method/approach/technique/framework for the same concept). Pick one term and use it consistently throughout the paper. Consistent terminology is clearer than elegant variation.
- **Reduce paired adjectives:** "robust and effective", "efficient and scalable" — pick the more precise one. If both matter, they deserve separate evidence, not a conjunction.
- **Shorten redundant metadiscourse.** "In this paper, we propose" is fine once (it marks the background-to-contribution transition), but don't repeat it. "This section describes" → often deletable. "The rest of this paper is organized as follows" → shorten or remove.
- **Ground evaluation language in evidence.** If the text says a method is "effective", "efficient", or "robust", keep the claim only when surrounding text provides evidence. Otherwise, rewrite as a concrete measured result or narrow the claim.
- **Uniform sentence length.** If all sentences in a paragraph are within ±5 words of each other, vary the rhythm — mix short punchy sentences (8-12 words) with longer ones (20-30 words).
- **Passive voice clusters.** A single passive is fine. Three consecutive passives signal AI. Rewrite at least one with an active subject.
- **Result-first → claim-first.** In Discussion/Conclusion, if a sentence leads with a number ("55% of the reduction..."), rewrite to lead with the insight ("block-internal coupling accounts for most of the reduction").
- **Informal intensifiers.** "well beyond", "quite", "really", "very", "highly" — remove when they add emphasis without precision. "well beyond the calibration set" → "outside the calibration set".
- **Verb doublets.** "generated and amplified", "designed and developed", "analyzed and evaluated" — pick one. Two near-synonyms joined by "and" is AI hedging.

### Additional Watchlist

These patterns are not errors by themselves. Edit them only when they are vague, repeated, or disconnected from concrete technical content:

- Generic openings: "Recent advances...", "In recent years..."
- Inflated claims: "remarkable success", "significant improvement", "comprehensive experiments"
- Vague problem framing: "suffers from limitations", "bridges the gap"
- Empty future work: "explore more robust and general methods" → name the actual direction
- Repeated contribution framing: multiple variants of "we propose/show/demonstrate" in the same paragraph

### 3. Formatting

- Avoid decorative bold or italic emphasis in body text. Preserve formatting for mathematical notation, defined terms, dataset/model names, or venue/style requirements.
- Keep LaTeX clean. Don't introduce unnecessary commands.
- Preserve math in `$...$` and `\(...\)`.
- Escape special characters (`%`, `_`, `&`).

### 4. Modification Threshold (Critical)

- **Less is more.** If the input already reads naturally with no AI signatures, keep the original.
- **Positive feedback.** Explicitly acknowledge high-quality input.
- **Never change for the sake of changing.** Every edit must genuinely improve readability.
- **Do not make prose artificially plain.** Technical writing should be clear, not casual.

### 5. Edge-Case Guardrails

- Preserve lists that serve a conventional paper function: contributions, assumptions, algorithm steps, experimental settings, limitations.
- Preserve parentheses used for citations, acronyms, mathematical notation, dataset details.
- Preserve transitions that clarify argument structure, especially in related work and theory sections ("in contrast", "more recently" can be legitimate).
- Do not weaken or strengthen claims. Keep the original scope unless the text clearly supports a narrower rewrite.
- Semicolons and parentheses in mathematical exposition are fine. Focus on prose punctuation.

### 6. Output Format

- **Part 1 [LaTeX]**: The rewritten English LaTeX (or original if no changes needed).
- **Part 2 [Modification Log]**:
  - If modified: briefly list which mechanical patterns were fixed.
  - If unchanged: output "[PASS] The original text reads naturally with no obvious AI patterns. Recommend keeping as-is."

---

## Examples

### Inflated claim → concrete
Before: "Large language models have achieved remarkable success across a wide range of tasks, but existing methods suffer from crucial limitations in efficiency."
After: "Large language models perform well on many NLP tasks, but their inference cost remains high for long-context inputs."

### Mechanical transition → direct
Before: "Furthermore, our method leverages block-level decomposition to facilitate more efficient compression."
After: "Our method uses block-level decomposition for more efficient compression."

### Vague participial tail → trim
Before: "L2 reduces perplexity from 42.1 to 19.3, demonstrating the effectiveness of the proposed optimization."
After: "L2 reduces perplexity from 42.1 to 19.3."

### Already natural → keep unchanged
Before: "We use singular value decomposition (SVD) to initialize the low-rank factors."
After: [unchanged]
Reason: The sentence is direct, technical, and natural.

### Contribution list → keep
Before: "Our contributions are: \begin{itemize} \item A block-wise SVD initialization. \item A calibration strategy. \item Evaluation on five benchmarks. \end{itemize}"
After: [unchanged, unless the user asks for paragraph form]
Reason: Contribution lists are standard in introductions.

---

## Self-Check Before Output

1. **Naturalness:** Does it sound like a person wrote it? Read it aloud mentally.
2. **Necessity:** Does every edit genuinely improve readability? (Swapping synonyms for no reason → revert.)
3. **Claim preservation:** Did any technical claim become stronger or weaker? If so, revert that edit.
