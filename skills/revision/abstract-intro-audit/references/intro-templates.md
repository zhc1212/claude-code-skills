# Introduction Sentence Templates

Source: 956 CVPR 2025/2026 Highlight papers. Organized by structural
component. Frequency counts indicate how many papers used each pattern.

## Background

| Pattern | Frequency |
|---------|-----------|
| `[TASK] plays a crucial/important/vital role in [APPLICATION] and is widely used across [DOMAIN].` | 162 |
| `Recent advances in [TASK] have [RESULT], enabling [APPLICATION].` | 160 |
| `[TASK] is a fundamental/essential task in [FIELD], enabling [APPLICATION].` | 145 |
| `[TASK] has drawn increasing attention due to its broad applications in [APPLICATION].` | 112 |
| `[TASK] aims to [GOAL], which is essential for [APPLICATION].` | 75 |

**Guidance**: Background is ~80 words (1–2 paragraphs). Establish the task's
importance and landscape. The strongest openings connect the task to a
concrete application domain rather than making abstract claims about
importance. Avoid opening with "In this paper, we..." — it wastes the
reader's highest-attention position.

## Task Definition

| Pattern | Frequency |
|---------|-----------|
| `[TASK] aims to [OBJECTIVE].` | 112 |
| `In this paper, we aim to [GOAL].` | 33 |
| `A central challenge in [TASK] is [CHALLENGE].` | 29 |
| `In this work, we focus on [TASK].` | 27 |
| `We define [TASK] as [DEFINITION].` | 21 |

**Guidance**: Task definition is optional (~37 words when present). Include
it when the paper defines a new problem, addresses a non-standard formulation,
or the audience needs disambiguation. For well-known tasks at the target
venue, this section can be absorbed into the background.

## Research Gap

| Pattern | Frequency |
|---------|-----------|
| `Despite [PROGRESS], [ISSUE] remains [PROBLEM_DESCRIPTION].` | 164 |
| `Although [METHOD] have achieved [RESULT], they still struggle with [CAPABILITY].` | 85 |
| `A key challenge in [TASK] is [CHALLENGE], which [EXPLANATION].` | 82 |
| `Although [METHOD] have achieved promising results, they still suffer from [LIMITATION], hindering [APPLICATION].` | 77 |
| `Although [METHOD] perform well in [SETTING], they fail to [REQUIREMENT] in [SCENARIO].` | 62 |

**Guidance**: The research gap is the argumentative core of the introduction
(~155-182 words, ~24% of total). This is where you convince the reviewer that
the problem is real, unsolved, and worth solving. The strongest gaps:
1. Name the specific limitation (not "existing methods have limitations")
2. Explain the root cause (the *because* or *due to* clause)
3. Connect the limitation to practical consequences
4. Build progressively — start broad, narrow to the exact technical gap

A shallow gap is a top rejection signal. If your gap is under 100 words,
it likely needs deepening.

## Related Work Overview

| Pattern | Frequency |
|---------|-----------|
| `[METHOD] [CITATION] utilizes [TECHNIQUE] to [PURPOSE].` | 106 |
| `Current approaches to [TASK] can be broadly categorized into [CATEGORY1] and [CATEGORY2].` | 103 |
| `Recent advances in [TASK] have demonstrated [RESULT] following [PARADIGM].` | 85 |
| `However, [METHOD] suffers from [LIMITATION], leading to [CONSEQUENCE].` | 81 |
| `Early approaches to [TASK] relied on [EARLY_TECHNIQUE], while recent methods leverage [RECENT_TECHNIQUE] to [PURPOSE].` | 67 |

**Guidance**: Related work in the intro (~110-127 words) serves a different
purpose than a standalone Related Work section. Here, it positions your work:
show what has been tried, what each approach's limitation is, and how those
limitations converge toward the gap your work fills. The categorization
pattern (103 occurrences) is effective for organizing the landscape. End
the related work section with the transition to your solution.

## Method Overview

| Pattern | Frequency |
|---------|-----------|
| `To address [CHALLENGE], we propose [METHOD].` | 215 |
| `To address [CHALLENGE], we introduce [METHOD].` | 103 |
| `In this work, we introduce [RESOURCE/METHOD].` | 78 |
| `In this paper, we propose [METHOD/FRAMEWORK] to [GOAL].` | 69 |
| `Building on [INSIGHT], we [ACTION].` | 54 |

**Guidance**: The method overview is the longest intro section (~198-234
words, ~31% of total). It should explain the core idea in enough detail
that the reader understands your approach before reaching the full Method
section. Structure it as: key insight → method name → what it does → how
it works (1-2 key mechanisms) → why it is effective. Avoid technical details
that belong in the Method section (implementation specifics, loss functions,
training procedures).

## Contribution Statement

| Pattern | Frequency |
|---------|-----------|
| `To the best of our knowledge, [METHOD] is the first [APPROACH] that [KEY_IDEA].` | 7 |
| `We summarize our contributions as follows:` | 7 |
| `In summary, our key contribution is [CONTRIBUTION].` | 6 |
| `The main contribution of this work lies in [CONTRIBUTION].` | 5 |
| `To the best of our knowledge, this work makes the first attempt to [GOAL].` | 3 |

**Guidance**: The contribution statement is the transition sentence before the
bullet-point contribution list. Keep it brief — one sentence is enough. The
"summarize our contributions as follows:" pattern is the most neutral and
widely used. Use "first" claims sparingly and only when verifiable.

## Itemized Contributions

| Pattern | Frequency |
|---------|-----------|
| `Our contributions are as follows: • We introduce [METHOD], a novel [FRAMEWORK] for [TASK]. • We design [MODULE/STRATEGY] to [PURPOSE].` | 380 |
| `Our contributions are summarized as follows: • To the best of our knowledge, [METHOD] is the first [APPROACH] for [TASK]. • We [ACTION] to [PURPOSE].` | 94 |
| `Our contributions are as follows: • We [ANALYZE/IDENTIFY/REVEAL] [PROBLEM/LIMITATION] and propose [METHOD] to address it. • We [DESIGN/INTRODUCE/PROPOSE] [MODULE/FRAMEWORK] to [PURPOSE].` | 84 |
| `Our contributions are as follows: • We introduce [DATASET/BENCHMARK], a [ADJECTIVE] dataset/benchmark for [TASK]. • We propose [METHOD] to [PURPOSE].` | 67 |
| `Our main contributions are summarized as follows: • We propose [METHOD] to [TASK]. • We introduce [METHOD] for [TASK].` | 55 |

**Guidance**: Itemized contributions appear in ~96% of the top structural
patterns — this is the single most expected component. Typical count: 3–4
bullets (~100 words total). Each bullet should:
1. Start with a verb (introduce, design, propose, demonstrate, provide)
2. Be specific enough that a reviewer can verify it in the paper
3. Cover method, key mechanism, and experimental validation

Common pitfalls:
- Vague bullets ("We conduct extensive experiments") — rewrite as "We evaluate
  [METHOD] on [BENCHMARKS] and show [SPECIFIC RESULT]"
- Too many bullets (>5) — consolidate related contributions
- Missing experimental contribution — almost always the last bullet

## Result Highlights

| Pattern | Frequency |
|---------|-----------|
| `We demonstrate [METHOD]'s effectiveness through extensive experiments on [BENCHMARKS], outperforming [BASELINE] and achieving [RESULT].` | 284 |
| `We evaluate [METHOD] on [BENCHMARK] and find that [RESULT]. Our analysis reveals [FINDING].` | 65 |
| `By introducing [METHOD], we achieve the best [METRIC1] and [METRIC2] in [BENCHMARK1] and state-of-the-art performance in [BENCHMARK2] in a zero-shot manner.` | 42 |
| `We achieve [METRIC] of [VALUE] on [BENCHMARK], which is [RESULT] points higher than [BASELINE], with only [RESOURCE] parameters.` | 36 |
| `We evaluate [METHOD] on [BENCHMARKS] and show that it consistently outperforms [BASELINE] across all metrics, achieving [RESULT].` | 33 |

**Guidance**: Result highlights in the intro should be brief (~32 words).
This is a preview, not a full results section. Include one headline number
and the key benchmark. Avoid repeating the abstract's results verbatim —
the intro version should be slightly more narrative ("Our method achieves X,
demonstrating that Y approach is effective for Z").

## Significance

| Pattern | Frequency |
|---------|-----------|
| `Our [METHOD] demonstrates strong potential for [TASK], highlighting its broader impact on [DOMAIN].` | 39 |
| `Analysis of [METHOD] reveals [INSIGHTS], confirming that [PRINCIPLE].` | 31 |
| `Additionally, we [CONTRIBUTION], which [BENEFIT].` | 24 |
| `Beyond [ASPECT], our [METHOD] offers [ADVANTAGE], such as [DETAILS].` | 18 |
| `To the best of our knowledge, this is the first [TASK] that [CONTRIBUTION].` | 16 |

**Guidance**: Optional. When present, it adds broader impact, generalizability,
or additional contributions beyond the main story.

## Paper Organization

| Pattern | Frequency |
|---------|-----------|
| `The paper is organized as follows: [RESOURCE].` | 6 |
| `Scope of this Work. We focus on [SETTING].` | 3 |
| `Code is available at [RESOURCE].` | 1 |

**Guidance**: Rare in CVPR papers. Only include if the paper structure is
non-standard and the reader benefits from a roadmap. Code availability is
better placed in the abstract's significance section or as a footnote.
