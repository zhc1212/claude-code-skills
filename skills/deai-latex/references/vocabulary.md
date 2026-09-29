# AI vocabulary, tiered by measured excess (reviewed 2026-09-29)

**r** is the 2024 excess ratio in PubMed abstracts: observed frequency divided by the frequency projected from 2021–2022 (Kobak et al. 2025). It is recomputed from the authors' released counts (`berenslab/llm-excess-vocab`, `results/yearly-counts.csv.gz`) with their formula. Read the tiers with four caveats:
- **Era.** These are ChatGPT-era (2024), biomedical abstracts. Computer science has the highest measured LLM use of any field (Liang et al. 2025), and its excess words may differ.
- **Turnover.** Marker words turn over with each model generation, whoever the provider (Lee 2026). "delve" peaked in early 2024 and has fallen since (Geng & Trotta 2025; Thelwall & Kousha 2026).
- **Word forms.** Each form counts separately: "leveraging" 3.08, "leverage" 1.22. An overused word does not make its synonyms overused.
- **Use in context.** A listed word is a candidate, not a verdict. Replace it only when it is vague or inflated where it stands.
- **Generation vs editing.** The 2026 measurements below come from text a model wrote from a paper's Results section, not from a model polishing an author's draft. Editing leaves a different trace (more function-word filler; Shan et al. 2026), so a direction measured on generation may not hold for polishing.

## Tier 1: r ≥ 2 (replace when vague or inflated)

| Word | r | Plain alternative |
|---|---|---|
| delves / delve | 28.0 / 7.9 | examines, investigates |
| underscores / underscore | 13.8 / 6.7 | shows, confirms |
| showcasing / showcases | 10.7 / 3.8 | showing, shows |
| meticulously | 10.4 | carefully, or cut |
| intricate | 7.4 | complex, or name the structure |
| garnered | 5.3 | received, drew |
| realm | 5.0 | field, area |
| emphasizing | 4.7 | stating, or cut the tail |
| fostering | 3.1 | encouraging, supporting |
| leveraging | 3.1 | using |
| pivotal | 3.1 | central, or state what depends on it |
| aligns | 2.9 | matches, agrees with |
| nuanced | 2.7 | name the distinction |
| notably | 2.6 | cut, or say why it stands out |
| highlighting | 2.6 | showing, or cut the tail |
| bolstered | 2.4 | strengthened, supported |
| seamless | 2.2 | say what needs no manual step |
| unveil | 2.2 | present, report |
| interplay | 2.1 | interaction |
| enduring | 2.1 | lasting |
| valuable | 2.0 | useful, or name the use |

Later practitioner lists for the GPT-4o and GPT-5 eras (Wikipedia "Signs of AI writing") name "emphasizing", "highlighting", "showcasing", "enhance" and "align with". The last two are only Tier 2 in the 2024 counts; the lists report them as current. A 2026 working paper (Lee 2026) reports rising markers from current models: "reconfigured", "foundational", "mere", "predominantly". Treat those as provisional.

## Tier 2: 1.25 ≤ r < 2 (flag only together with another hit in the same sentence)

additionally 1.91 (sentence-initial "Additionally" is the case that matters), align 1.89, **leverage** 1.22 in 2024 but 5.8 in 2026 generation, **foster** 1.23 in 2024 but 6.8 in 2026 generation, sentence-initial **"Importantly,"** (see the 2026 update), comprehensive 1.76, enhance 1.76, elucidate 1.65, substantiate 1.59, showcase 1.59, landscape 1.47 (figurative use only), profound 1.35, vibrant 1.35, robust 1.28 (never as a statistical or technical term).

## Not tells in the counts (r < 1.25): leave them unless the author's baseline says otherwise

significant 1.23, utilize 1.22, demonstrate 1.16, furthermore 1.13, importantly 1.05 (mid-sentence), significantly 1.04, amplify 1.04, regarding 1.03, harmonize 1.02, accentuate 0.97, moreover 0.88, thus 0.83, commence 0.82, therefore 0.79.

"significant" does rise in simulated GPT-3.5 revisions of arXiv abstracts (Geng & Trotta 2024). Treat it as a claim-strength question, not a style question: a non-statistical "significantly" belongs to paper-polish's inflated-claim list.

## 2026 update: current-model measurements

deai-mark (github.com/elK-liang/deai-mark, v2.2, September 2026) compared 879 human biomedical papers (2018 to mid-2022, 17 journals) with abstracts, introductions and discussions that MiniMax M2.7, MiniMax M3 and a GLM-5.3 agent wrote from the same papers' title, keywords and Results. A rule needs a bootstrap 95% CI lower bound of at least 2.0; thresholds were frozen before the AI side was measured. It is generation, biomedical only, and has no GPT, Claude or Gemini data. OpenAI's prompting guide for GPT-6 Astra independently lists "leverage", "foster", "importantly", "it's worth noting" and "genuinely" as slop words for that release (vendor statement, unmeasured).

- **Confirmed:** underscore as a verb (17× in discussions), sentence-initial "Notably," (6.5×), "pave the way" (29×), "open avenues".
- **Raised to Tier 2:** leverage (5.8×), foster (6.8×), sentence-initial "Importantly," (grouped with "Notably," in the 6.5× rule; its own ratio is not reported).
- **Lowered out of Tier 1: crucial.** Human papers use it 3.3–6.7× as often as these models, and "play a (crucial) role" 2–4×. The 2024 excess (2.1) came from real abstracts, where polishing is mixed in, so the two results do not settle the polishing case. Judge "crucial" against the author's baseline and flag it only inside a cluster.
- **Unchanged:** sentence-initial However and Moreover (humans 3–4× more), semicolons (humans 3× more in introductions and discussions), hedges (no difference), "in this study" (humans 2× more).
- **Word lists age:** delve, showcase, meticulous and pivotal are near zero in these 2026 models. Wikipedia's list for the GPT-5 era (mid-2025 on) is only emphasizing, enhance, highlighting and showcasing; on 207,111 astro-ph papers, delve has fallen since mid-2024 while underscore and notably kept rising (Saad & Ting 2026, read via sepia's ledger).
- **Sentence length (evidence for the "Missing short sentences" candidate in SKILL.md):** 2025 aligned models write almost no short sentences in English news leads (1–4% of sentences of 1–15 tokens against 32–33% for humans; Gude et al. 2026, prompt asked for two or three sentences, models incl. GPT-4o); within-text length spread is lower in model text in four studies across two model generations (sepia's ledger); uniformity is the strongest category in avoid-ai-writing's 2022–2024 human-control corpus (lift 11.7×); human ICLR reviewers score papers with more varied sentence length higher, a frozen LLM rater does not (Zheng 2026, reader preference, not a detector feature). No study covers academic prose written or polished by frontier models, and lieflat finds no difference in Chinese on 2026 models.

## Practitioner-only: too rare in abstracts to measure

tapestry, testament, boasts, garner, quietly, "stands as a testament", "in the heart of", "rich tapestry". These appear in practitioner lists from 2023–mid-2024, the GPT-4 era (Wikipedia "Signs of AI writing"). Replace them when they appear, but do not expect them in current model output.

Figurative gating ("gates access to", "gated behind") is a practitioner flag too. Gating mechanisms, gated units, MoE gates, and quantum gate operations are technical terms; keep them.

## Sources

- Kobak, González-Márquez, Horvát, Lause, "Delving into LLM-assisted writing in biomedical publications through excess vocabulary," Science Advances, 2025.
- Geng, Trotta, "Is ChatGPT transforming academics' writing style?" arXiv:2404.08627, 2024; "Human-LLM coevolution: evidence from academic writing," Findings of ACL, 2025.
- Liang et al., "Quantifying large language model usage in scientific papers," Nature Human Behaviour, 2025.
- Thelwall, Kousha, "Have LLM-associated terms increased in article full texts in all fields?" arXiv:2604.07565, 2026.
- Lee, "An LLM-associated register shift in Korean journal abstracts," arXiv:2609.07447, 2026 (working paper).
- Wikipedia, "Wikipedia:Signs of AI writing," revision of September 2026 (practitioner source; era lists and Historical indicators).
- elK-liang/deai-mark v2.2 (2026-09): SKILL.md, PROTOCOL.md, results/VALIDATION.md; paired biomedical corpus, generation by MiniMax M2.7/M3 and GLM-5.3.
- OpenAI, "Prompting guidance for GPT-6 Astra" (vendor guidance), quoted verbatim in Nanako0129/sepia `skills/sepia/references/model-fingerprints.md`.
- Shan, Lee, Hao, "AI Writers Have a Consistent Stylometric Footprint, but AI Editors Do Not," arXiv:2608.27855, 2026; Saad & Ting 2026 (astro-ph); both read through sepia's `research/sources.md`, not in the original.
- Evidence for the grammar and punctuation entries in SKILL.md:
  - Reinhart et al., "Do LLMs write like humans? Variation in grammatical and rhetorical styles," arXiv:2410.16107 (PNAS 2025). Participial clauses 2–5×, nominalizations 1.5–2×; agentless passive in GPT-4o about half the human rate. Its human corpus spans several genres, academic among them.
  - Czuma, "Em-ergence of the em-dash," arXiv:2606.29540, 2026. Freeburg, "The Last Fingerprint," arXiv:2603.27006, 2026.
  - Miletić, Falk, "What are LLMs doing to scientific communication?" arXiv:2605.19936, 2026. Humans use more brackets and conjunctions.
  - Peters, Chin-Yee, "Generalization bias in large language model summarization of scientific research," Royal Society Open Science, 2025.
  - Russell, Karpinska, Iyyer, "People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text," ACL, 2025.
  - Liang et al., "GPT detectors are biased against non-native English writers," Patterns, 2023. Saha, Feizi, "Almost AI, almost human: the challenge of detecting AI-polished writing," Findings of ACL, 2025.
- Evidence for the scope lines in SKILL.md (added 2026-09-29):
  - Russell et al., StoryScope, arXiv:2604.03136, 2026: discourse features separate AI from human fiction (61,608 stories); the theme-explicitness excess behind "paragraph-closing interpretations" is measured on fiction only.
  - Daguilar0123/ai-writing-skill-field-guide, `docs/BLIND-TEST.md` (2026-07): blader/humanizer v2.9.1 on 16 genuine paragraphs changed a median 8–9% of tokens; Claude judges (sonnet and opus seats) picked the humanized version 83.3% cold and 76.7% with a writing sample (n=30 each; pooled with the haiku seat, 62.2% and 51.1%), keying on removed author habits.
  - MohamedAbdallah-14/unslop README (2026-09): deterministic surface rewriting moved the TMR detector score by 0.0–0.2 percentage points.
- The full evidence table and the revision rationale are in `~/huicheng/deai-research-2026-09/`: `proposal.md`, `corpus.md`, and the 2026-09-29 GitHub survey `github-survey.md`.
