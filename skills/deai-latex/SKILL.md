---
name: deai-latex
description: Use when English prose from an academic paper, in LaTeX or plain text, should lose its AI writing style: "去AI味", "de-AI", "deai", "remove AI style", "AI tells", "reads like ChatGPT", or after pasting paper text that ChatGPT or Claude wrote or polished. Also reached from /oral-paragraph-audit Check 6. General polishing with no AI-style complaint (grammar, flow) goes to paper-polish or polish-english-paper; prose that is not from a paper goes to /humanizer.
---

# De-AI Paper Prose

If the user hasn't provided the text yet, ask: **"Please paste the passage and, if you have them, your own draft of it or another passage you wrote without AI help."**

The yardstick is the author's own writing, read at its median rather than its best. A mark the author uses at their usual rate is their style; only a rate above theirs is a tell, and their rate is a ceiling, never a target to converge on. Model style lives more in rhetorical moves (how a sentence stages, inflates, or shapes its content) than in single words, and word habits change with each model release while the moves persist. Finding a pattern does not license an edit: every candidate is judged in context first, and text the author wrote comes back unchanged. The rewriter is a model with habits of its own, so the procedure ends by checking what the rewrite itself added.

## Modes

- **Pasted (default).** Deliver the two-part output at the end.
- **File.** Edit the prose in place; math, commands, citations, and comments pass through unchanged. Report a summary rather than the file, and in a page-capped paper include the net word change, since a longer passage can push content past the limit.
- **Embedded** (`/oral-paragraph-audit` Check 6). You are the same agent doing both, so there is no hand-off. Run the procedure on the paragraph and carry forward the rewrite, the baseline table (or "no baseline"), each finding with its family and triggering phrase, and each dismissed candidate with its reason. The caller judges whether findings cluster in one sentence or scatter, which a count cannot show. Skip the two-part output.

## Procedure

1. **Baseline.** Name the section (abstract, introduction, method, experiments, related work, limitations, conclusion); method prose legitimately uses passives and nominal style. Then find the author's own writing, strongest first:
   - the author's earlier version of this same passage (a draft the user supplies, or the commit before an AI edit), which shows exactly what the model changed;
   - other text the author wrote without AI help, from the same section type first (method against method), then from any section.

   Text is a baseline only if the user names it as their own, or the history ties it to them before any AI edit (the commit that imported their draft, a section only that commit touched). Text of unknown author or AI history is no baseline. The two ways a baseline goes wrong fail in opposite directions: an AI-polished one raises the allowances and passes AI wording off as the author's, so findings are missed; a coauthor's, or one from another section type, sets the allowances by habits that are not this passage's, so its ordinary features get flagged.

   Count per 1,000 prose words, in the baseline and in the passage, leaving out math, displayed environments, comments, and command names:
   - em dashes (`---` or `—`; the two around one aside count as two);
   - colons that elaborate a claim ("the two losses are coupled: lowering one raises the other"), apart from colons that introduce a list or follow a label ("Stage 1:");
   - semicolons that join clauses, apart from those separating list items that contain commas;
   - clause tails, exactly ", so", ", which", and ", rather than";
   - sentence-initial connectives: however, moreover, furthermore, additionally, therefore, thus, hence, consequently, instead, together, finally, in contrast, as a result ("Instead," and "Together," only as sentence adverbs; ordinals that number a sequence are not connectives);
   - mid-sentence therefore, thus, hence, consequently, however, moreover, furthermore, additionally (used only by step 6).

   Also record the share of sentences under 16 words; a sentence ends in `.`, `?`, or `!` outside math, and headings and fragments under three words are not sentences. The author's **allowance** for a feature is the baseline rate times the passage's length, rounded up: 2.0 colons per 1,000 words allow one colon in a 355-word passage. `python3 <skill dir>/scripts/audit_style.py count PASSAGE --baseline BASELINE` computes the table for LaTeX or plain text and prints every match in context; `<skill dir>` is the base directory shown when this skill loads, and pasted text goes into temp files first. Its colon and semicolon classes are heuristics, so read the matches before trusting a count; a pattern match is not yet a candidate. **Done when** the table (feature × baseline, passage, allowance) exists under a line naming the baseline, its provenance (named by the user, or from the history), and its scope (same passage, same section type, other section), or you have stated "no baseline available". Without a baseline, counted features and edit residue are off and catalogue phrases are the only candidates; in pasted mode, add that the author's draft or own writing would enable the rate checks.

2. **Audit, without editing.** Read the passage against the catalogue three times: for words, for sentences, and for paragraphs. With the author's earlier version, also compare the two sentence by sentence for edit residue. A counted feature is a candidate when the passage has at least two instances and more than the allowance. Record every candidate with its family, triggering phrase, and location. **Done when** every sentence has been read at all three levels and every candidate is listed.

3. **Adjudicate.** A candidate becomes a finding only if it survives three questions.
   - **Is it the author's?** A catalogue word or construction that the baseline also contains is held to the allowance, like a counted feature. Wording that the author's earlier version already has is the author's.
   - **Is it doing work here?** A precise technical use ("gating mechanism", "robust regression"), the section's convention, a list with a paper function, a phrase quoted or discussed rather than used, or a mark that reads clearly in context is dismissed.
   - **Does it cluster?** A catalogue phrase can be a finding on one sighting, but several candidates in one sentence make each more likely to be real, and one isolated em dash or "however" rarely is.

   Record the reason for every dismissal. If nothing survives, return the passage unchanged and say it reads as the author's; that is the expected result for text the author wrote, not a fallback. **Done when** every candidate is a finding or dismissed with a reason.

4. **Edit minimally.** Before the first edit, read `references/examples.md` for how small an edit should be.
   - One edit per finding, and the log names the finding. An edit that answers to no finding is reverted.
   - The first choice of fix is the author's own wording from the earlier version, where it says what the passage says; where the edit changed the claim, fix within the passage's wording and log the change. Otherwise change the sentence's words, subject, or opening.
   - Keep one proposition per sentence and the author's order of definition, equation, and reason. Restoring the author's earlier order inside a paragraph keeps that order. Any other fix that would merge author sentences or move a reason ahead of what it explains is left undone and named in the log.
   - Bring a counted feature down to the allowance, not to zero. Fix first the instances the earlier version shows the model created.
   - To split off a ", so" tail, start the consequence as a new sentence with no connective; placed right after its cause, it keeps the causal link. Add "therefore" or "thus" only where a reader could not otherwise see the link.

   **Done when** every finding is fixed or listed as left in place with its reason.

5. **Verify meaning.** Compare every changed sentence with its source. The rewrite must keep:
   - the same claims, scope, and hedge strength;
   - the same actors: when a passive becomes active, the agent must be one the source names;
   - every number, name, citation, and qualifier, with each number still attached to the noun it measures;
   - the direction of attribution: the author's own measurement stays the author's, and a reported claim stays reported ("reported", "claimed", "according to" are neither added nor removed);
   - the polarity of a judgment: a limitation or criticism does not come out as praise;
   - the grain of the results: several specific results are not merged into a general "better", and a vague benefit does not become a firm claim.

   It must add no new contrast, cause, consequence, or evaluative clause, and no broader generalization; LLM rewrites of scientific text broaden scope far more often than people do. Then run `python3 <skill dir>/scripts/audit_style.py compare SOURCE REWRITE` (add `--earlier FILE` for the author's earlier version). It lists every math span, citation key, reference, and number whose count changed, and each is restored unless it sat in a sentence a logged finding cut. It also flags every content word of the rewrite whose stem is absent from the source and the earlier version, so a form change (tuning, tune) is not flagged. A flagged word stays only if it is repair (an article, a subject, or the verb of a nominalization that a split sentence needs) or the plain word that fixes a logged finding ("uses" for "leverages") and brings in no entity, property, relation, quantity, or hedge the source lacks. Every other flagged word is an addition and is reverted. **Done when** every changed sentence has been checked, no protected span differs, and every flagged word is kept for one of the two reasons or reverted.

6. **Verify style.** Machine editing leaves its trace in the filler it adds around the content more than in the words it swaps, so run three checks.
   - **Deletion and reversion tests.** Strike every word or phrase the rewrite added: if the sentence still parses and says the same thing, the addition was filler and goes. Put back every wording the rewrite replaced: if the old wording carried no finding and said the same thing, restore it. Repair, as step 5 defines it, passes both tests.
   - **Recount.** Recount the step-1 features, mid-sentence connectives included, on the rewritten passage; the step-5 `compare` output has both sides. A feature whose count rose over the input is reverted, or kept with a one-line reason in the log. Run the catalogue again on every changed sentence, since a fix can itself create a tell.
   - **Displacement.** A removed mark often returns in another form with the same rhythm: an em dash becomes a colon or a comma-bounded appositive, a ", so" tail becomes "X therefore", split participial tails become a run of "This …" openers. When one fix repeats, vary it (a different subject, an embedded clause), and never leave two identical openers in a row. Also check the rewriter's standing habits: em dashes, claim-elaborating colons, ", so" tails, "rather than", "only", and prose that narrates a revision.

   Banning a mark in the instructions does not stop a model from producing it; only these checks show whether it did. **Done when** every addition and replacement has passed both tests, no counted feature rose (or each rise has its reason), and no displaced form remains.

## Catalogue

The families say what the model is doing, which helps recognize a listed pattern in a new form; a move with no entry is not a finding. Vocabulary lives in [references/vocabulary.md](references/vocabulary.md), tiered by measured excess and dated; read it when a passage contains words that sound inflated.

### Inflation: the stakes are raised above the content

- **AI vocabulary.** Use the tiers in `references/vocabulary.md`. Replace a listed word only when it is vague or inflated where it stands. Word forms count separately: "leveraging" is Tier 1, "leverage" only Tier 2.
- **Inflated significance and vague achievement.** "a wide range of", "remarkable success", "significant improvements", "comprehensive experiments", "sheds light on", "bridges the gap", "paves the way for", "opens new avenues", "suffers from limitations". Use the numbers the text already has; otherwise state the same claim plainly, at the same scope. "Plays a crucial role" is not on this list: human papers use it more often than 2026 models do, so flag it only inside a cluster.
- **Boosters and stakes-raisers.** "notably" (measured excess), "Interestingly", "Indeed", "Of course", "Naturally", "Unsurprisingly", and intensifiers such as "well beyond", "quite", "really", "very", "highly" when they add emphasis without precision.
- **Weasel attributions.** "Experts argue", "several studies" when few are cited. Name the source the text gives: the citation on the claim, or a work named beside it. With none, the sentence stays and the log flags it as needing a source; a source the text does not give is never attached.
- **Heavier forms of a plain verb.** Copula avoidance: LLM revision lowers "is" and "are" ("serves as a warm-start" → "is a warm-start"). Nominalization: instruction-tuned models nominalize at 1.5–2 times the human rate ("the examination of X" → "examining X"), unless the section's convention wants the noun.
- **Paired adjectives and verb doublets.** "robust and effective", "designed and developed": keep the more precise one.
- **Generic endings.** "This opens exciting avenues", "explore more robust and general methods", "Despite these promising results, several challenges remain". End on the last concrete finding, or name the limitation and its consequence.
- **Repeated contribution framing.** Several "we propose/show/demonstrate" variants in one paragraph.

### Staging: the reader is told how to take the content

- **Interpreting participial tails.** Instruction-tuned models use present participial clauses at 2–5 times the human rate. Trim a sentence-final "-ing" clause that restates the result ("…, demonstrating the effectiveness of …"); keep one that states a mechanism, condition, or consequence the source holds.
- **Negative parallelism.** "not only X but also Y", "it's not just X, it's Y": a contrast nobody raised. State Y, or "X and Y".
- **Formulaic openers and authority tropes.** "In recent years", "Recent advances in", "The real question is", "at its core", "fundamentally", "X is the Y of Z". State the ordinary point.
- **Fragmented headers.** A `\paragraph{}` followed by one sentence that restates it before the content starts. Cut the warm-up sentence.
- **Editorial scar tissue.** "A tempting approach would be X, but …" where X is never evaluated, cited, or mentioned again. Keep X when it is a baseline, an ablation, or a cited method.
- **Shadowboxing.** "To be clear, we do not claim …" answering an objection the paper never raises. Keep a scope statement that qualifies a claim the text makes.

### Rhythm by rule: one shape applied regardless of content

- **Forced groups of three.** Two items are fine; four are fine.
- **Tailing negations and false ranges.** "needs no separate pass, no extra tuning" → "needs neither a separate pass nor extra tuning"; "from architecture search to quantization" is a list, not a range.
- **Repeated sentence openings.** Three or more consecutive sentences with the same subject outside a contribution list. Begin with the action or change the subject where the referent allows; do not rotate synonyms and do not merge.
- **Manufactured punchlines.** A run of short declaratives stacked for drama. One short sentence is fine; three in a row is a tell.
- **Missing short sentences** (candidate; the evidence is non-academic, see `references/vocabulary.md`). In a passage of ten or more sentences with another finding, a share of sentences under 16 words below half the baseline share marks the longest sentences for splitting. Never merge, and do not alternate lengths on a schedule, which is its own tell.

### Punctuation and connectives: judged only against the baseline

- **Em dashes.** Their rise in papers is real at population level but says little about a single paper, and rates differ by model by an order of magnitude. Claude, a likely rewriter, uses them heavily, so step 6 recounts them.
- **Semicolons, claim-elaborating colons, and clause tails.** No published study measures them in academic English; the baseline decides.
- **Sentence-initial connectives.** "Additionally" shows measured excess, still rising, and "Importantly," is Tier 2; these two are catalogue phrases, candidates on sighting even without a baseline. "Moreover", "Furthermore", "Thus", and "Therefore" show no excess, and human papers open with "However" and "Moreover" more often than 2026 models do; keep them unless the baseline shows the author does not write them. Deleting transitions in bulk trades one template for another.

### Edit residue: traces of a model editing the author's draft

Visible only against the author's earlier version. Editing leaves a different trace from generation (see the generation-vs-editing caveat in `references/vocabulary.md`): in one local case (2026-09, Claude polishing an author's draft), ", so" tails went from 0 to 13 and claim-elaborating colons from 0 to 11.
- **Merged sentences.** Two author sentences joined into one by a colon, semicolon, clause tail, relative clause, or "and". They are not findings by themselves: the allowances and the short-sentence share decide how many joints to undo, merged joints go first, and the fix restores the author's split.
- **Reordered content.** A claim or condition the author placed after its reason or definition now comes first. Inside a paragraph, restoring the author's order is the default fix. A move across paragraphs is a structural edit: name it in the log and leave it.
- **Added filler.** Words the edit added around the content that the deletion test removes. A replaced word is left alone unless the new wording carries a finding.
- **Changed claim strength.** A hedge, qualifier, or scope the draft had and the edit dropped, or one the edit added. Name it in the log as a suspected claim change; restoring it is the author's call.

### Leftovers: traces of the chat or of drafting

- **Narrated revision.** "We replaced the earlier penalty with a softmax", "Revised: …" belong in a response letter; say what the method is. Changelogs and rebuttals are exempt.
- **Chat formatting.** Prose split into bullets, bold-label-plus-colon bullets, decorative bold or italic. Keep lists with a paper function: contributions, assumptions, algorithm steps, settings, limitations.
- **Leaked tokens and placeholders.** `oaicite`, `contentReference`, `turn0search0`, "[insert source]", "TBD", "XX", and curly quotes pasted from a chat window. Remove them; supply a citation only if the user gives one.

## What is not a tell

- **Not in the catalogue, on evidence.** Passive voice: GPT-4o uses agentless passives at about half the human rate. Parentheses: human papers use more brackets than LLM-polished ones. Latinate words ("demonstrate", "utilize", "regarding") show no excess in the published counts. Paragraph-closing interpretations ("Overall, these results show …"): their measured excess is in fiction, and in a held-out paper test (2026-09) the author wrote them while the model's edit added none.
- **Not reliable on their own.** Polished grammar and consistent style; formal or low-frequency vocabulary; neutral or dry tone, the most common false positive of human judges; non-native phrasing, which detectors misread as AI; dashes, brackets, and quotations mixed into sentences, which expert annotators read as human; deliberate repeated openings that build a sequence ("We train. We prune. We retrain.").
- **Signs of the author.** Specific, hard-to-fabricate detail (an exact seed, an odd failure, a named cap that binds); unresolved tension; genuine asides and self-corrections; a scope qualifier the author can defend; plainness, repetition, and small slips. Blind judges pick out a humanized paragraph by which of the author's habits it changed, so smoothing these is itself the tell.

## Handled elsewhere

- Claim–evidence alignment, overclaim verbs, and hedge calibration belong to `/oral-paragraph-audit` Check 8. This skill keeps claim strength as the author set it (step 5) and names a suspected overclaim in the log without editing it.
- General paragraph and paper structure (recap openings, empty conclusions, signposts, echo, bridges, repeated arguments, one term per concept) belongs to `/oral-paragraph-audit` Checks 3–5.
- Grammar, flow, and formatting conventions (hyphenation, units, tense, heading case) belong to paper-polish.
- Detector scores are not a goal. Surface rewriting barely moves a modern detector (0.0–0.2 points in one 2026 test); the goal is prose that reads as the author's.

## Adding a pattern

A pattern enters the catalogue only with all three of the following; most practitioner lists fail the first.
- A measured excess in model text over human text: at least 2×, or 1.25–2× with a second, independent signal. Evidence from fiction or general prose makes a candidate, marked as such.
- A trigger that points at a specific word, construction, or countable shape. "Reads too uniformly" does not qualify.
- A date and a model era.

## Output Format

- **Part 1 [Text]**: the rewritten passage, or the original if nothing changed.
- **Part 2 [Log]**:
  - the baseline table with allowances and the baseline's provenance and scope, or "no baseline available";
  - each finding with its family, triggering phrase, and fix;
  - each dismissed candidate with its reason, one line each;
  - findings left in place because fixing them would merge or reorder the author's sentences, and any suspected overclaim;
  - the step-6 recount, and any edit reverted in step 5 or 6.
  - If nothing changed: "[PASS] Reads as the author's writing; no candidate survived adjudication. Returned unchanged."
