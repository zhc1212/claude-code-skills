---
name: deai-latex
description: >-
  Use when the text is English LaTeX prose from an academic paper (any section) and the user wants AI writing style removed: "去AI味", "de-AI", "deai", "remove AI style", "AI tells", "reads like ChatGPT", "润色", "改一下文字", "polish prose", or after pasting ChatGPT/Claude-generated paper text. Also reach for it from /oral-paragraph-audit Check 6. For prose that is not from a paper (blog, essay, fiction, docs, email) use /humanizer instead, including when the user says "humanize" or "让文字更自然".
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

## Invocation Modes

**Pasted text (default).** Deliver the two-part output below.

**File mode.** The user points at a `.tex` file. Rewrite the prose in place, leaving math, macros, `\cite`/`\ref`, environments, and comments untouched. Report a short summary rather than pasting the file back.

**Embedded mode.** This skill is being applied as one step of a larger audit (e.g. `/oral-paragraph-audit` Check 6). You are the same agent doing both, so there is no hand-off: work the catalogue over the passage and carry forward the rewritten LaTeX plus, for each pattern you hit, its category and the phrase that triggered it. The caller needs those phrases as evidence and needs to see whether the hits cluster in one sentence or scatter across the passage — a bare count cannot show either. Skip the two-part output format below.

---

## Editing Procedure

1. Identify the paper section (abstract, intro, method, experiment, related work, limitation, conclusion).
2. Preserve all technical claims, variables, citations, numbers, comparisons, and scope qualifiers.
3. Edit only sentences that match a listed pattern or contain vague/inflated wording.
4. Prefer smaller edits over full rewrites.
5. After rewriting, verify that no claim became stronger, broader, or less precise than the original.

---

## Constraints

### 1. Vocabulary and Phrasing

Prefer plain, precise academic words. Avoid overused AI vocabulary.

**Watchlist** (flag when vague or inflated, not mechanically): leverage, delve into, tapestry, accentuate, amplify, underscore, unveil, nuanced, profound, pivotal, foster, harmonize, transcend, elucidate, substantiate, seamless, intricate, crucial, landscape (abstract), interplay, showcase, garner, enduring, vibrant, quietly, gate/gated/gating (figurative only: "gates access to", "gated behind")

Gating mechanisms, gated units, MoE gates, and gate operations are technical terms. Default to keeping them; flag only the figurative use.

**Common replacements**: leverage → use, delve into → investigate, tapestry → context, elucidate → explain, substantiate → support, showcase → show, crucial → important

Replace only when the word sounds inflated, vague, or less precise than a simpler alternative. If the word is precise in context, keep it.

**Copula avoidance:** AI substitutes elaborate constructions for simple "is/are/has". "serves as a warm-start" → "is a warm-start". "stands as a key contribution" → "is a key contribution". Restore the copula.

**Inflated significance:** "plays a crucial/vital/key role in" → "contributes to" or just state the effect directly. "a wide range/variety of tasks" → "tasks" or "several tasks".

**Vague achievement claims:** Replace generic phrases with concrete claims tied to actual results. Avoid: "remarkable success", "significant improvements", "comprehensive experiments", "state-of-the-art performance", "sheds light on", "bridges the gap", "opens new avenues", "extensive experiments demonstrate". If the text provides numbers, use them. If not, narrow the claim.

**Boosters and stakes-raisers:** boosters (really, very, hugely, remarkably, strikingly, notably), stakes-raisers (Unsurprisingly, Interestingly, Indeed, Of course, Naturally), filler adverbs (crucially, importantly, genuinely, honestly, straightforward), promotional adjectives (novel, unique, important contribution). Let the evidence carry the weight.

**Weasel attributions:** "Experts argue", "Observers have noted", "Industry reports suggest", "several studies" when few are cited. Name the source or cut the claim. Never decorate an unsupported claim to look sourced.

**Authority tropes:** "The real question is", "at its core", "fundamentally", "in reality", "what really matters", "the deeper issue". These pretend to cut through noise before restating an ordinary point.

**Aphorism formulas:** "X is the Y of Z", "X is not a tool but a mirror", "the language of", "the currency of", "the architecture of". Replace the formula with the concrete claim it gestures at.

**Excessive hedging:** "could potentially possibly be argued that X might have some effect" → "X may affect Y". One hedge carries the uncertainty; three signal evasion. A caveat that exists only to repair an earlier overstatement ("achieves state-of-the-art results, although performance may vary across settings") means the claim above it is too strong: narrow the claim and drop the caveat.

**Speculative gap-filling:** "it is believed that", "likely", "presumably" used to cover something the text does not know. State what is not known, or cut the sentence. In a paper this is a credibility failure, not a style one.

**Latinate over Anglo-Saxon** when no precision is gained: utilise → use, demonstrate → show, commence → start, regarding → about. Technical terms are exempt.

**Verb nominalization:** "the examination of X" → "examining X" or "X examines".

**Overclaim verbs:** prove, demonstrate conclusively, definitively, "the cause" → prefer "consistent with", "indicates", "the evidence supports".

### 2. Structure

- **Avoid unnecessary prose lists.** Convert `\itemize`/`\enumerate` to paragraphs when they merely split ordinary prose into bullets. Preserve lists that serve a conventional function: contributions, assumptions, algorithm steps, experimental settings, or limitations.
- **Remove mechanical connectives:** "First and foremost", "It is worth noting that", "Additionally", "Furthermore", "Moreover" at sentence starts. Also "In recent years" / "Recent advances in" openers — delete and start with the actual subject.
- **Trim vague participial tails.** Remove or rewrite sentence-final `-ing` clauses when they merely restate the result ("demonstrating the effectiveness of..."). Keep them when they express a precise mechanism, condition, or consequence.
- **Reduce em dashes (—):** Replace with commas, parentheses, or subordinate clauses. More than one per paragraph is the practical ceiling.
- **Reduce semicolons (;):** AI overuses semicolons to join parallel clauses. Human authors more often split into two sentences or use a conjunction. More than two per paragraph is the practical ceiling.
- **Reduce explanatory parenthetical clutter.** Keep standard academic parentheses for citations, acronyms, dataset details, and short clarifications. Rewrite only parentheticals that interrupt the sentence or hide important content (e.g., "the method (which uses SVD) achieves..." → "the SVD-based method achieves...").
- **Reduce rule-of-three:** AI forces ideas into groups of three to appear comprehensive. Two is fine. Four is fine. Don't force three.
- **Remove negative parallelisms:** "not only X but also Y" → "X and Y" or two sentences. "it's not just about X, it's about Y" → state Y directly.
- **Rewrite tailing negations.** A clipped fragment tacked onto a sentence instead of a real clause: "the allocator needs no separate pass, no extra tuning" → "the allocator needs neither a separate pass nor extra tuning".
- **Collapse false ranges.** "from X to Y" only when X and Y sit on one meaningful scale. "from architecture search to quantization" is a list, not a range — write it as one.
- **Fix synonym cycling:** AI rotates synonyms to avoid repetition (method/approach/technique/framework for the same concept). Pick one term and use it consistently throughout the paper. Consistent terminology is clearer than elegant variation.
- **Repeated sentence openings.** Three or more consecutive sentences that start with the same subject ("The model first ... The model then ... The model finally ...") outside a contribution list or abstract. A first/then/finally march of same-length sentences is the same pattern. Merge the sentences, begin with the action, or change the subject where the referent allows. Do not rotate in synonyms for the subject; that trades this tell for the one above. The remaining sentence may still start with "The model".
- **Reduce paired adjectives:** "robust and effective", "efficient and scalable" — pick the more precise one. If both matter, they deserve separate evidence, not a conjunction.
- **Verb doublets.** "generated and amplified", "designed and developed", "analyzed and evaluated" — pick one. Two near-synonyms joined by "and" is AI hedging.
- **Shorten redundant metadiscourse.** "In this paper, we propose" is fine once (it marks the background-to-contribution transition), but don't repeat it. "This section describes" → often deletable. "The rest of this paper is organized as follows" → shorten or remove.
- **Cut fragmented headers.** A `\paragraph{}` or `\subsection{}` followed by one sentence that restates the heading before the real content starts. The heading already said it.
- **Ground evaluation language in evidence.** If the text says a method is "effective", "efficient", or "robust", keep the claim only when surrounding text provides evidence. Otherwise, rewrite as a concrete measured result or narrow the claim.
- **Uniform sentence length.** If all sentences in a paragraph are within ±5 words of each other, vary the rhythm — mix short punchy sentences (8-12 words) with longer ones (20-30 words).
- **Passive voice clusters.** A single passive is fine. Three consecutive passives signal AI. Rewrite at least one with an active subject.
- **Manufactured punchlines.** A run of short declaratives stacked for drama ("The cap was gone. No floor. No ceiling.") reads engineered. One short sentence for emphasis is fine; three in a row is a tell.
- **Result-first → claim-first.** In Discussion/Conclusion, if a sentence leads with a number ("55% of the reduction..."), rewrite to lead with the insight ("block-internal coupling accounts for most of the reduction").
- **Keep commentary out of Results.** Interpretation of the data belongs in Discussion.
- **Drop generic positive conclusions.** "This opens exciting avenues for future work" → end on the last concrete finding, or name the actual direction.
- **Describe the method, not the revision.** Prose that narrates a change ("we replaced the earlier penalty with a softmax") belongs in a response letter, not in Method. Say what the method is. Version-scoped text (changelogs, rebuttals) is exempt.
- **Editorial scar tissue.** "A tempting/naive/obvious approach would be X, but ..." where X is never evaluated, cited, or mentioned again. The sentence records a drafting decision, not a result. A sound engineering reason for rejecting X ("prohibitively expensive") does not make X a finding; if the comparison matters, it belongs in the experiments with a number. State the actual design and its constraint directly. Keep X when it is a baseline in the tables, an ablation, or a cited method the paper positions against.
- **Shadowboxing.** "To be clear, we do not claim ...", "This is not to say ...", "We are not arguing that ..." answering an objection nobody raised: the denied topic appears nowhere else in the paper. Cut it, or state the positive claim it hides. Keep a scope statement that qualifies a claim the text actually makes, an objection a cited work raises, or a limitation the paper then addresses.
- **Avoid formulaic limitation sections.** "Despite these promising results, several challenges remain" → state the specific limitation and its consequence.
- **Informal intensifiers.** "well beyond", "quite", "really", "very", "highly" — remove when they add emphasis without precision. "well beyond the calibration set" → "outside the calibration set".
- **Cut filler phrases.** "in order to" → "to". "due to the fact that" → "because". "at this point in time" → "now". "in the event that" → "if". "has the ability to" → "can". "it is important to note that the data shows" → "the data shows".
- **Tense discipline.** Present tense for findings and established facts, past tense for events and procedures. Both tenses in one paragraph are correct when a past procedure yields a present finding ("we trained X; the profile transfers"); flag MINOR only when the same event or claim switches tense without cause.

### Additional Watchlist

These patterns are not errors by themselves. Edit them only when they are vague, repeated, or disconnected from concrete technical content:

- Generic openings: "Recent advances...", "In recent years..."
- Inflated claims: "remarkable success", "significant improvement", "comprehensive experiments"
- Vague problem framing: "suffers from limitations", "bridges the gap"
- Empty future work: "explore more robust and general methods" → name the actual direction
- Repeated contribution framing: multiple variants of "we propose/show/demonstrate" in the same paragraph
- "taken together" / "Together," as a sentence opener
- "i.e." in running text → a comma, or "namely"

### 3. Formatting

- Avoid decorative bold or italic emphasis in body text. Preserve formatting for mathematical notation, defined terms, dataset/model names, or venue/style requirements.
- Keep LaTeX clean. Don't introduce unnecessary commands.
- Preserve math in `$...$` and `\(...\)`.
- Escape special characters (`%`, `_`, `&`).
- **Curly quotes are a LaTeX defect, not just a tell.** Pasted `"` and `"` render wrong; LaTeX needs `` `` `` and `''`. Convert every one.
- **Sentence case in headings.** AI capitalizes every main word; most venues want sentence case. Match the venue's style file.
- **Hyphenate by position.** Attributive compounds take the hyphen ("a rank-profile transfer"), predicate ones usually drop it ("the profile is rank matched"). AI hyphenates uniformly in both.
- **Number and unit consistency.** Pick `%` or "percent" and hold it; en-dash for ranges (`1840--2010`); digits for 10 and above and for all statistics; words for one through nine in running text; spaces around `=` in inline math.
- **First person** (we/our) is standard in ML/NLP papers. Flag it only where the venue or style guide prohibits it.

### 4. Modification Threshold and False Positives

- **Less is more.** If the input already reads naturally with no AI signatures, keep the original.
- **Positive feedback.** Explicitly acknowledge high-quality input.
- **Never change for the sake of changing.** Every edit must genuinely improve readability.
- **Do not make prose artificially plain.** Technical writing should be clear, not casual.
- **Look for clusters, not isolated hits.** One em dash means nothing. Em dashes plus a forced triple plus "vibrant landscape" plus an empty future-work sentence is a confession.
- **If a flagged pattern reads clearly in context, keep it.** The watchlists are heuristics for top-venue prose, not rules that outrank the sentence in front of you.

**Not reliable tells on their own** — a careful human writer hits these routinely:
- Polished grammar and consistent style. Many authors are edited; polish is not AI.
- Formal or academic vocabulary. AI overuses *specific* fancy words, not all of them.
- One `however` or `moreover`. These are AI-coded only when piled up.
- Curly quotes alone (every editor auto-curls) or one em dash alone (many authors use them).
- A single short emphatic sentence.
- Dry, plain prose with none of the specific tells above. That is just dry writing.
- A watched phrase inside a quotation, a title, or an example where it is being discussed rather than used. Leave those alone.
- Deliberate repeated openings that build a sequence ("We train. We prune. We retrain."). Change them only when the repetition adds nothing.
- A rejected alternative that the paper evaluates (baseline, ablation) or cites. Only an alternative dismissed in one clause and never seen again is scar tissue.
- A scope statement or limitation a reviewer would plausibly raise about a claim the text makes. Shadowboxing is the denial of a topic that appears nowhere else.

**Signs a human wrote it — lean toward leaving the prose alone:**
- Specific, hard-to-fabricate detail: an exact seed, an odd failure, a named cap that binds.
- Unresolved tension: "we do not claim either route is better; the ordering reverses between ratios."
- Varied sentence length, genuine asides, and self-corrections.
- A scope qualifier the author can defend. Over-editing these flattens exactly what makes a paper credible.

### 5. Edge-Case Guardrails

- Preserve lists that serve a conventional paper function: contributions, assumptions, algorithm steps, experimental settings, limitations.
- Preserve parentheses used for citations, acronyms, mathematical notation, dataset details.
- Preserve transitions that clarify argument structure, especially in related work and theory sections ("in contrast", "more recently" can be legitimate).
- Do not weaken or strengthen claims. Keep the original scope unless the text clearly supports a narrower rewrite.
- Semicolons and parentheses in mathematical exposition are fine. Focus on prose punctuation.
- **Never invent a fact.** The rewrite contains no number, name, citation, or qualifier absent from the source. Trading a vague claim for a specific one needs the specific to come from the source or the user.

### 6. Output Format

- **Part 1 [LaTeX]**: The rewritten English LaTeX (or original if no changes needed).
- **Part 2 [Modification Log]**:
  - If modified: briefly list which mechanical patterns were fixed.
  - If unchanged: output "[PASS] The original text reads naturally with no obvious AI patterns. Recommend keeping as-is."

**In a page-capped or near-final paper, report the net word change and rebuild before calling the rewrite done.** A length change reflows every page after it: the source diff looks local, but it can push content past the page limit or overfull a table cell you never opened. If an add breaks the budget, pay for it by cutting the body prose the add made redundant rather than by weakening the edit.

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

### Weasel attribution → named or cut
Before: "Experts argue that activation-aware rank search is the stronger approach."
After: "ASVD reports that activation-aware rank search outperforms uniform truncation."
Reason: If no such source exists, the claim gets cut rather than attributed to nobody.

### Fragmented header → cut the warm-up
Before: "\paragraph{Module type is the supported resolution.} Which types receive rank is load-bearing. A budget-matched permutation..."
After: "\paragraph{Module type is the supported resolution.} A budget-matched permutation..."

### Scar tissue and shadowboxing → state the design
Before: "An obvious approach would be to retrain the tokenizer on the target domain, but this discards the pretrained embeddings, so we keep the original vocabulary. This is not to say that domain-specific tokenizers are never worthwhile."
After: "We keep the original vocabulary so that the pretrained embeddings remain usable."
Reason: Tokenizer retraining is never evaluated or cited, so the rejection is drafting residue; the disclaimer answers an objection the text never raised. If the comparison is a result, it goes in the experiments with a number.

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
4. **Fabrication:** Does the rewrite state any number, name, citation, or qualifier absent from the source? That is a defect even when it reads better.
