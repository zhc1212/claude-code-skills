# Debate: {topic}

Date: {YYYY-MM-DD}
Rounds: {N}
Outcome: {consensus | decision-ready tradeoff | evidence-needed | stalemate}
{one record line per opponent, from Participants in debate-protocol.md}
Exchange: {exchange directory}
Evidence revisions: {repo@commit, … for the code and data the cruxes rest on}

## Final Conclusion

{detailed conclusion with reasoning — what was decided and why}

## Debate Trajectory

### Opening Positions
- **Claude**: {Toulmin-structured summary — claim, warrant, confidence}
- **{Opponent}**: {Toulmin-structured summary — claim, warrant, confidence} (one bullet per opponent)
- **Initial cruxes identified**: {list}

### Round-by-Round
#### Round 1: Crux identification
{what each model challenged, steel-mans offered, evidence cited with tiers}

#### Round 2: {focus}
{concessions with confidence changes, counter-arguments, position updates}

#### Round N: Resolution
{how the debate concluded, which stopping condition triggered}

## Crux Ledger (Final)

| Crux | Claude view | {one column per opponent} | Confidence | Resolution | Deciding evidence |
|------|------------|------------|------------|-----------|------------------|
| {crux} | {view} | {view} | C:{lvl} X:{lvl} (labels from Participants) | {status} | {evidence} [{tier}] |

## Evidence Ledger

| Claim | Evidence | Tier | Source | Status |
|-------|----------|------|--------|--------|
| {claim} | {evidence} | {tier} | {participant} | {accepted/contested/unresolved} |

## Unresolved Items

{any remaining disagreements with every position documented}
{what evidence or experiment would resolve each}

## Action Items

- [ ] {concrete action from consensus}
- [ ] {experiment/benchmark to resolve open question}
