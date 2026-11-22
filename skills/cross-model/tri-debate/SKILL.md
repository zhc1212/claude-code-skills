---
name: tri-debate
description: Structured three-party debate among Claude, Codex (GPT via Codex CLI) and Gemini 4 Carbon (via the Antigravity CLI `agy`) on a technical or research decision, with parallel blind openings, claims verified before anyone sees another position, unattributed relay and a final endorsement round. Use when the user wants Codex and Carbon (or Gemini, agy) in one discussion — "三方讨论", "三个模型讨论", "让codex和carbon一起讨论", "codex和gemini一起辩", "three-way debate", "tri-debate". A debate that names one model goes to codex-debate or agy-debate.
---

# Tri-Debate

Run [`../shared-references/debate-protocol.md`](../shared-references/debate-protocol.md) with Codex and Carbon as
opponents (both columns under Participants). Its Two-Party Round Messages do not apply: the round flow below replaces
them. Everything else in the protocol applies as written. Where the two differ, this file wins.

## Both opponents

- Verification (Opponent rules) also comes before a claim reaches the other opponent. Relay an uncheckable claim as
  conditional.
- The blind opening says the debate is with Claude and one other AI model.
- Each wave sends both calls at once with `run_in_background` and waits for both replies. Claude saves its own opening
  or round reply to `r{N}-claude.md` before reading either.
- Prompts are `r{N}-prompt-codex.md` and `r{N}-prompt-agy.md`. They differ only in the read-only line and, after
  round 0, the tilt.
- If one CLI still fails after one narrowed retry, tell the user and continue with the other, instead of the
  question in Failures. Mark the result partial, and its ledger column missing.

## Round flow

The budget is the blind opening plus at most two rounds, a focused round and a final round. A Phase 5 stopping
condition can end it earlier.

1. **Blind opening** (Phase 2), both calls in parallel on the same packet.
2. **Verify, then build the ledger.** Verify all three openings before either opponent sees another position. Then
   build the ledger (Phase 3), one column per participant. The blind-opening positions stay in the record as the pre-exposure
   view.
3. **Relay packet.** Send one identical packet to both:
   - The arguments of all three, Claude's included. Group them by claim, warrant and caveat. Quote them verbatim
     with grounds, verification tag, scope condition and falsifier. Keep distinct evidence and measured uncertainty.
   - No author names, counts, peer confidence ratings or statements that anyone agrees. Settled points appear only as
     premises the open question rests on.
   - A file one participant cited reaches the other as an absolute path plus an excerpt.
4. **Focused round.**
   - When the candidates have explicit, testable requirements, ask each opponent to break every candidate (its own
     included), then repair or concede, then give a conditional update.
   - Otherwise, ask it to steel-man the strongest opposing argument, challenge the crux that could change the action,
     and update.
   - Tilts: Codex gives the smallest counterexample to its own preferred option. Carbon proposes the strongest hybrid
     or alternative the arguments miss.
   - When Phase 3's Immediate Agreement Protocol calls for red-team mode, this round is that red-team, asked without
     saying who agrees.
5. **Final round.** Send the merged decisions as numbered items.
   - Each opponent endorses each item, or objects with the smallest change that would make it endorse.
   - Each quotes any of its own words that the merge misrepresents.
   - When convergence since the blind openings has no stated cause (a verified artifact, a demonstrated
     counterexample, a clarified user constraint or a repair), the same prompt asks each to attack that convergence's
     weakest premise.
6. **Close**, then run Phases 6–7:
   - An item is consensus when every participant endorsed it as sent.
   - Claude may adopt a smallest change. It then counts as endorsed only by its proposer; record the other side's
     endorsement of the earlier wording. Such items, and items with conflicting changes, are splits.
   - A split is never consensus. Lead with the action a stated user priority selects. Otherwise give the deciding test
     or the conditional options. Report a blind-opening majority, if there was one, as history.
   - The outcome is consensus only when every decision-bearing item is. Otherwise it is the Phase 5 outcome that fits
     the open items, and they go under Unresolved.
