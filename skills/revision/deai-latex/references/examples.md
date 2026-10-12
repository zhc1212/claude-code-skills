# Worked examples

Before/after pairs for the catalogue families in `SKILL.md`, plus a rewrite that fails the meaning check and two passages that stay unchanged. The size of each edit is the point: the smallest change that removes the finding. Each After draws only on its Before; where it needs more, the example shows where that comes from.

## Inflation: inflated claim → plain, at the same scope
Before: "Large language models have achieved remarkable success across a wide range of tasks, but existing methods suffer from crucial limitations in efficiency."
After: "Large language models perform well on many tasks, but existing methods have limited efficiency."
Reason: The source names no task, cost, or input, so the rewrite names none. "Inference cost for long inputs" would be a new claim; a specific enters only when the passage already states it.

## Inflation: measured connective and vocabulary → direct
Before: "Additionally, our method leverages block-level decomposition to facilitate more efficient compression."
After: "Our method uses block-level decomposition for more efficient compression."

## Inflation: weasel attribution → the source the text gives
Before: "Experts argue that activation-aware rank search is the stronger approach~\cite{asvd}."
After: "\citet{asvd} argue that activation-aware rank search is the stronger approach."
Reason: The citation is the source the text gives, so the claim is attributed to it and keeps its wording. Without a citation, the sentence stays and the log flags it as needing a source; naming a plausible paper would be a new claim.

## Staging: interpreting participial tail → trim
Before: "L2 reduces perplexity from 42.1 to 19.3, demonstrating the effectiveness of the proposed optimization."
After: "L2 reduces perplexity from 42.1 to 19.3."

## Staging: fragmented header → cut the warm-up
Before: "\paragraph{Module type is the supported resolution.} Which types receive rank is load-bearing. A budget-matched permutation..."
After: "\paragraph{Module type is the supported resolution.} A budget-matched permutation..."

## Staging: scar tissue and shadowboxing → state the design
Before: "An obvious approach would be to retrain the tokenizer on the target domain, but this discards the pretrained embeddings, so we keep the original vocabulary. This is not to say that domain-specific tokenizers are never worthwhile."
After: "We keep the original vocabulary so that the pretrained embeddings are not discarded."
Reason: Tokenizer retraining is never evaluated or cited, so the rejection is drafting residue; the disclaimer answers an objection the text never raised.

## Punctuation: consequence tail → split without a connective
Before: "The profiler runs once per build, so its cost is shared by every test in that build."
After: "The profiler runs once per build. Its cost is shared by every test in that build."
Reason: The second sentence follows its cause, so the link survives. "Its cost is therefore shared …" would trade the tail for a connective, which step 6 counts.

## Edit residue: merged sentences → the author's split
Author's draft: "The cache is rebuilt after every schema change. Stale entries are never served."
Model's edit: "The cache is rebuilt after every schema change; as a result, stale entries are never served."
After: the author's two sentences.
Reason: The semicolon and "as a result" were added by the edit and say nothing the order did not already say.

## A rewrite that fails the meaning check → revert
Author: "Layers may reuse established pruning criteria. The search may also propose new masks."
Rejected rewrite: "Layers may reuse established pruning criteria or search-proposed masks, so the method covers both known and new sparsity patterns."
Reason: The merge joins two author sentences, and ", so the method covers both known and new sparsity patterns" is a consequence the source never states. Step 5 reverts it, and step 6 would have caught the new ", so" tail. The author's two sentences stay.

## Already natural → keep unchanged
Before: "We use singular value decomposition (SVD) to initialize the low-rank factors."
After: [unchanged]
Reason: The sentence is direct, technical, and natural.

## Contribution list → keep
Before: "Our contributions are: \begin{itemize} \item A block-wise SVD initialization. \item A calibration strategy. \item Evaluation on five benchmarks. \end{itemize}"
After: [unchanged, unless the user asks for paragraph form]
Reason: Contribution lists are standard in introductions.
