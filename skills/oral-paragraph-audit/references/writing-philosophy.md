# Writing Philosophy — Extended Rationale

## The Reviewer's Situation

A reviewer handles 3–6 papers per cycle, each in 2–3 hours, alongside their own
research deadlines. They pattern-match for quality signals. When a paragraph feels
unclear, they do not re-read — they note "writing could be improved" and move on.
Every point of friction is a micro-deduction that compounds. Oral-quality writing
eliminates this friction entirely.

## Oral vs. Poster vs. Workshop

The difference is not vocabulary or polish. It is information architecture:

| Tier | Reader experience |
|------|------------------|
| Workshop | Ideas are present; reader works to extract them |
| Poster | Ideas are clear; reader occasionally re-reads or looks back |
| **Oral** | Ideas land on first read — zero re-reading, zero backtracking, zero guessing |

## The Ten Principles (with sources)

Numbering matches the compact list in SKILL.md exactly.

1. **Every sentence earns its place.** Page limits are hard. A sentence that restates
   what the reader already knows wastes attention budget. Three things a sentence can
   do: advance the argument, introduce evidence, or specify mechanism. A sentence that
   does none of these is deletable. *(Drives Checks 2, 6)*

2. **Claims and evidence travel together.** When a reviewer reads "X outperforms Y,"
   they immediately look for the number. If evidence is two paragraphs away, the claim
   feels unsupported. Oral papers never make the reviewer search. *(Drives Check 3)*

3. **The paragraph is the unit of argument.** S1 states what this paragraph will prove.
   The rest proves it. A reviewer skimming only S1s should reconstruct the full argument.
   *(Drives Checks 0, 1, 4, 5)*

4. **Content lives in the right place.** A correct sentence in the wrong section is noise.
   Method explains *what and why*; Experiments explains *how and with what*. *(Drives Check 8)*

5. **Do not multiply entities beyond necessity.** Every symbol, acronym, and terminology
   variant is a cognitive slot. If two names refer to the same object, pick one. Formulas
   must be locally readable — a reviewer should understand every symbol without flipping
   back. *(Drives Checks 2, 8, 9)*

6. **Key information lands at the stress position.** Readers assign extra weight to
   sentence endings ([Gopen & Swan, 1990](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf)).
   Bury key findings in subordinate clauses and the reader misses the payload.
   *(Drives Check 4, interacts with Check 1)*

7. **Each paragraph must create reader value.** A paragraph that only reports what the
   authors did — without explaining why that matters to the community — is dead weight.
   An Experiments paragraph listing datasets and metrics is not valuable until it tells
   the reader what question the experiment answers. *(Drives Checks 0, 1, 3; inspired
   by [McEnerney's reader-value framework](https://henryleach.com/2016/05/the-craft-of-writing-effectively/))*

8. **Cohesion comes from logic, not connectors.** Furthermore, Additionally, Moreover,
   and In addition assert a logical relation exists without naming it. If removing the
   connector exposes a gap, the sentences need restructuring — the connector was masking
   weak argument structure. Real transitions arise from substance: the end of one sentence
   sets up the beginning of the next. *(Drives Check 4, interacts with Check 5)*

9. **Restrained, evidence-first register.** Top-venue academic tone: let evidence carry
   the weight. Boosters (really, very, remarkably) inflate importance without adding
   information. Stakes-raisers (Interestingly, Indeed, Unsurprisingly) editorialize
   where the reader should judge for themselves. Overclaim verbs (prove, demonstrate
   conclusively) promise what evidence rarely delivers. Prefer Anglo-Saxon over Latinate
   when no precision is gained: use not utilise, show not demonstrate, about not
   regarding. Respect venue and author style — this is a heuristic, not a universal rule.
   *(Drives Check 6 categories B and C)*

10. **Paragraphs are vectors, not items in a list.** Each paragraph should relate to the
    previous one through contrast, specification, deepening, or mechanism — not mere
    juxtaposition. A sequence that reads "one paragraph on A, one on B, Together these…"
    is a list pretending to be an argument. The reader should feel the argument move forward
    with each paragraph, not sideways. *(Drives Check 10, interacts with Check 5)*

These principles interact: good structure with low density wastes a well-framed argument
on filler. Dense paragraphs with decoupled claims are informative but unconvincing.
Well-structured paragraphs with buried findings force re-scanning. Good structure,
density, and evidence that fail to address a reader-relevant question are strategically
useless. Oral quality requires all ten simultaneously.

## Key References

- [Gopen & Swan, 1990](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) — topic and stress positions
- [McEnerney](https://henryleach.com/2016/05/the-craft-of-writing-effectively/) — reader-value framework
- [SPJ](https://simon.peytonjones.org/great-research-paper/) — refutable claims
- [Lipton](https://www.approximatelycorrect.com/2018/01/29/heuristics-technical-scientific-writing-machine-learning-perspective/) — ML writing heuristics
- [Farquhar](https://sebastianfarquhar.com/on-research/2024/11/04/how_to_write_ml_papers/) — boilerplate formalisms
- [Perez](https://ethanperez.net/easy-paper-writing-tips/) — pronoun clarity, verb-early
