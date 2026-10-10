---
name: defensive-writing-sweep
description: "Sweeps a whole paper draft, a section, or an appendix for defensive (boundary) writing: qualifications written for an anticipated reviewer instead of the reader, and tables, rows, or appendix sections placed only to pre-empt objections. Use when the user asks about 防御性写作, 边界性写作, 防御性表述, defensive writing, or over-hedging across a paper or section. Returns a candidate list for the author and edits nothing; a single paragraph goes to oral-paragraph-audit."
---

# Defensive-Writing Sweep

The rule is the **Boundaries** rule of Check 8 in
`~/.claude/skills/oral-paragraph-audit/SKILL.md`; read it before the sweep. Its
test, restated here because every candidate needs it: delete the boundary. If
the claim it qualifies stays true on the paper's evidence, the boundary is
defensive. If that claim becomes false, the boundary belongs inside the claim
as scope words, stated once. The reason the rule exists is principle 11 in
`~/.claude/skills/oral-paragraph-audit/references/writing-philosophy.md`.

Exempt: the Limitations section, the scope words that make a claim true, and a
grounded limitation stated once.

## Procedure

1. Read the Boundaries rule. If the project keeps review notes (a fix tracker,
   a decisions log), grep them for 防御 and "defensive": the author's earlier
   calls are the precedent for borderline cases.
2. **Sentences.** Grep the source for the markers below, then read in full
   every paragraph with a hit and every abstract, contribution, results,
   discussion, and conclusion paragraph, because a repeated qualifier carries
   no marker. Apply the test to each candidate.
   - not-shown: `does not (establish|show|imply|isolate|guarantee)`, `we do not claim`, `does and does not`
   - generic scope and doubt: `in the evaluated settings`, `may not (transfer|generalize|hold)`, `within (our|the) tested`
   - reading instructions: `rather than`, `should be (read|treated|interpreted) as`
   - explanations and meta-comment: `consistent with`, `caveat`, `note that`, `for completeness`, `we report this`
3. **Structure.** Give every table, figure, and appendix section a one-line
   verdict: the claim it supports and the section that cites it. A row,
   panel, or section whose only job is to answer an objection the paper does
   not raise (an ablation row in the main comparison table, an appendix that
   reconciles runs or rebuts an imagined reviewer) is a candidate.
4. **Side results.** List each unfavourable result stated next to a claim
   whose scope already excludes it, and each untested explanation attached to
   one. Dropping a reported result is the author's call; list it, never delete
   it.

Done when every marker hit and every paragraph named in step 2 has been read
and either listed or passed, and every table, figure, and appendix section has
its verdict line.

## Output

```
| # | Location | Text | Kind | Test | Proposed action |
|---|---|---|---|---|---|
| 1 | main.tex:175 | "consistent with …" | explanation | claim "worse on WT2" stays true without it | delete |
```

- **Kind**: not-shown, ungrounded doubt, generic scope, reading instruction,
  repeated qualifier, side result, explanation, structural.
- **Test**: the claim the boundary qualifies and whether it stays true without
  it, naming the evidence.
- **Proposed action**: delete; fold into the claim as "[scope words]"; move to
  [place]; or author's call (side results and structural items).

Then the verdict lines for tables, figures, and appendix sections, and a last
line `Candidates: N (by kind: …)`. Edit nothing until the author picks
candidates; apply the picked ones through oral-paragraph-audit Procedure
steps 4–5 and end the report with step 5's `Recheck:` line.
