---
name: defensive-writing-sweep
description: "Sweeps a whole paper draft, a section, or an appendix for defensive and self-weakening writing: boundaries written for an anticipated reviewer, words that downgrade the paper's own results, contests staged where the paper loses, strengths its tables support but the text never states, and tables, rows, figures, or appendix sections with no claim to support. Use when the user asks about 防御性写作, 边界性写作, 扬长避短, 发布会原则, self-weakening, or over-hedging across a paper or section. Returns a candidate list for the author and edits nothing; a single paragraph goes to oral-paragraph-audit."
---

# Defensive-Writing Sweep

A paper is a **launch**, not a work report: it is built around its strongest
result, states each advantage outright, and gives each caveat once, in
Limitations. Two rules find what breaks that.

**Boundaries** is Check 8 in `~/.claude/skills/oral-paragraph-audit/SKILL.md`;
read it before the sweep. Its test, restated because every candidate needs it:
delete the boundary. If the claim it qualifies stays true on the paper's
evidence, the boundary is defensive. If that claim becomes false, the boundary
belongs inside the claim as scope words, stated once. Principle 11 in
`~/.claude/skills/oral-paragraph-audit/references/writing-philosophy.md` gives
the reason.

**Launch** kinds, each with the positive target for its rewrite:

- *self-weakening*: a word that grades the paper's own result downward:
  "only 3%", "merely", "unfortunately", "still trails", "falls behind", "grows
  slowly", "modest gain", "supplementary run", "we have not tried", 仅, 遗憾的是,
  仍明显落后, 效果有限. Target: the fact with its numbers, or the goal difference
  or trade-off behind it ("trained on QIT alone; on miniF2F it solves 111 of
  244"). A word that restricts a set ("tuned on LLaMA-2-7B only") is a scope
  word and falls under Boundaries.
- *staged loss*: a comparison the paper's own test does not win, set up as a
  contest in text, caption, bold, or a figure annotation (bracket, arrow, value
  label). Target: the axis, comparator, or budget the paper wins, with the full
  grid left in its table.
- *under-claim*: a stronger numeric result the paper already reports elsewhere
  (a table cell, an appendix, another section) that the body's claim leaves
  out:
  another baseline or budget whose interval excludes zero, a favourable ratio
  of two reported numbers, a result above another run's interval. Target: the
  sentence, built only from values and facts the paper states, each quoted
  with its location. A strength that needs a fact the paper does not state,
  or a cell you cannot read, goes in a note to the author below the tables.
- *process*: narration of what was tried and in what order ("we asked
  whether", "we then measure", "was stopped"). Target: the finding.
- *me-too*: likening the paper's finding to prior work when the paper's own
  evidence already carries it ("a contrast like the one X draws", "mirrors
  X"). Target: delete.
- *invited comparison*: a related-work sentence reporting another paper's
  finding that invites a comparison this paper does not run. Target: keep the
  citation, drop the finding.
- *one-sided caveat*: a caveat that a protocol choice (a cap, budget, or
  matching rule) favours the paper's method, when the paper's own numbers show
  the same choice also favours the baselines. Target: both sides in one
  sentence.
- *closing doubt*: a conclusion sentence that introduces a weakness or a
  missing experiment. Target: delete; Limitations owns it.

The abstract and introduction run problem → gap → idea → hardest result with
its number; a caveat there moves to Limitations.

**Keep on purpose.** Reframing changes the axis and the wording; the evidence
stays complete. These five classes stay:

- scope words that make a claim true;
- a grounded limitation stated once in Limitations. The section is exempt from
  the delete test; sweep it only for a caveat the body also states, a
  one-sided caveat, and self-weakening words;
- every analysis the paper or its records mark as prespecified, including a
  sensitivity check that weakens a claim, with the claim scoped to what that
  analysis supports;
- reuse of the evaluation set for selection or tuning, and the coverage of any
  audit a headline relies on;
- provenance that tells the reader which run a number comes from.

Keeping protects that a result is reported, not where it sits: a table, row,
panel, or appendix section gets its placement call in step 3, as a structural
item.

## Procedure

1. Read the Boundaries rule. Grep the project's review notes, decisions log,
   and evidence log for 防御, defensive, 扬长避短 and "moved out": earlier calls
   are precedent, and a removed item that has come back is a candidate.
2. **Sentences.** Grep the source for the markers below, then read in full
   every paragraph with a hit and every abstract, introduction, contribution,
   results, discussion, conclusion, and Limitations paragraph, because a
   repeated qualifier carries no marker. Apply both rules to each sentence.
   - not-shown: `does not (establish|show|imply|isolate|guarantee)`, `we do not claim`, `does and does not`
   - generic scope and doubt: `in the evaluated settings`, `may not (transfer|generalize|hold)`, `within (our|the) tested`
   - reading instructions: `rather than`, `should be (read|treated|interpreted) as`
   - explanations and meta-comment: `consistent with`, `caveat`, `note that`, `for completeness`, `we report this`, `like the one`, `mirrors`
   - self-weakening and process: `only`, `merely`, `unfortunately`, `trails?`, `lags?`, `falls? behind`, `slowly`, `modest`, `limited`, `supplementary`, `preliminary`, `we (asked|tested) whether`, `we have not`, `stopped`
3. **Structure.** Give every table, figure, and appendix section a one-line
   verdict: the claim it supports and the section that cites it. Read every
   figure annotation and bolded cell and name the comparison it stages. A row,
   panel, annotation, or section is a candidate when it only answers an
   objection the paper does not raise (an ablation row in the main comparison
   table, an appendix that reconciles runs), when no claim cites it, when it
   stages a loss, or when its own text disowns its conclusion (a stopped
   ablation that "rejects that update rather than X in general"). Each such
   candidate is also a table row of kind structural, in the group of the
   action you recommend.
4. **Strengths.** For every results table you can read, appendix tables
   included, write the strongest true statement its cells support and compare
   it with the body; each gap is an under-claim. A table you cannot read gets
   its verdict line only.
5. **Side results.** List each unfavourable result stated next to a claim
   whose scope already excludes it, and each untested explanation attached to
   one. Dropping a reported result is the author's call; list it, never delete
   it.

Done when every marker hit and every paragraph named in step 2 has been read
and either listed or passed, every table, figure, and appendix section has its
verdict line, and every results table has its strongest statement checked
against the body.

## Output

Four groups in this order, each a table with these columns:

```
| # | Location | Text | Kind | Test | Proposed action |
|---|---|---|---|---|---|
| 1 | main.tex:175 | "consistent with …" | explanation | claim "worse on WT2" stays true without it | delete |
```

1. **Delete.**
2. **Rewrite**: Proposed action is the replacement text, in the paper's language.
3. **Add strength**: the under-claims, each with the sentence to add and its source cell.
4. **Keep on purpose**: items a rule above would flag but a Keep class
   protects, with the class and the text that establishes it in Test. An item
   no rule flags, or whose class the paper's text does not establish, stays
   out of this group.

- **Kind**: not-shown, ungrounded doubt, generic scope, reading instruction,
  repeated qualifier, side result, explanation, structural, or a Launch kind.
- **Test**: the claim the item touches and whether it stays true without it,
  or the evidence a rewrite or addition rests on, naming the evidence.
- **Proposed action**: delete; fold into the claim as "[scope words]"; the
  replacement text; or move to [place]. Side results and structural items sit
  in the group of the action you recommend, and their Proposed action starts
  "author's call:".

Then the verdict lines for tables, figures, and appendix sections, and a last
line `Candidates: N (by kind: …)` counting groups 1–3. Edit nothing until the
author picks candidates; apply the picked ones through oral-paragraph-audit
Procedure steps 4–5, record each removed result in the project's evidence or
decisions log if it keeps one, and end the report with step 5's `Recheck:`
line.
