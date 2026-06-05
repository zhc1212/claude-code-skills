---
name: codex-paper-adversary
description: "Sends paper sections to GPT via Codex MCP for independent adversarial review — Codex's job is to REJECT, not to help improve. Attacks are grounded in real venue reviewer standards (Quality/Clarity/Significance/Originality), calibrated to actual venue scoring scales, and constrained by explicit fatality gates. Use when user says \"codex review my paper\", \"hostile review\", \"adversarial paper review\", \"codex as reviewer\", \"try to reject my paper\", \"codex审我的论文\", \"codex当reviewer\", \"让codex挑刺\", \"论文对抗审查\", \"codex帮我找论文弱点\", \"模拟拒稿\". Not for code review (/codex-review), multi-persona simulated review (/academic-paper-reviewer), or paper writing/polishing. This is specifically adversarial — the goal is rejection, not improvement."
---

# Codex Paper Adversary

Get a hostile paper review from GPT via Codex MCP — a standards-bound
prosecutor, not a balanced reviewer. Codex finds reasons to REJECT,
grounded in the same evaluation dimensions real reviewers use.

This matters because a helpful reviewer anchors on "how can this be better"
and misses the failure modes that sink papers. A hostile reviewer asks "why
should this be rejected" and finds the attacks that real Reviewer 2 will find.

**Cross-model value**: academic-paper-reviewer simulates 5 personas, but
they are all Claude instances with correlated blind spots. This skill uses
GPT — a different model family with different failure modes. Claude
orchestrates and evaluates; Codex provides independent adversarial pressure.

## Review Modes

### Section Review (default)
User provides a specific section. Claude reads it, extracts claims, builds
the adversarial packet. Best for iterative hardening.

### Claim Review
User provides specific claims or contributions. Best for stress-testing
bold claims before submission.

### Full Draft Review
Claude splits into sections, runs multi-pass Codex review (one fresh call
per section for independence), then synthesizes with a cross-section
consistency check.

## Protocol

```
1. User provides paper section(s), claims, or PDF path
2. Claude extracts claims + figure/table assertions
3. Claude builds adversarial packet (raw text + venue standards)
4. Codex adversarial review: Fair Target Lock → find reasons to REJECT
5. Claude evaluates each attack (legitimate / partially valid / unfair)
6. Claude self-checks: actionable? expression≠method? score objective?
7. Present: all attacks + Claude's assessment + rejection narrative
8. Follow-up: challenge with rebuttal gate
```

## Step 1: Extract Claims

Read the provided material. For each substantive claim, record:
- The claim text (quote or close paraphrase)
- The evidence presented in the paper to support it
- The logical link between evidence and claim

Do NOT interpret, strengthen, or steelman the claims. Record what the paper
actually says, not what it should say.

For figures and tables, also record:
- What the figure/table claims to show
- Whether the axes, labels, and data ranges are appropriate
- Whether the visual presentation matches the textual claims

If the user specified a venue, note it. If not, ask: "Which venue? Reviewer
expectations differ." Default to ICLR/NeurIPS if unspecified.

## Step 2: Build Adversarial Packet

Include: raw paper text (unmodified), venue and review standards (below),
adversarial framing with Fair Target Lock.

**Do NOT include** Claude's interpretation, Claude's opinion, or hints
about what might be weak. Blind independence is the entire point.

## Step 3: Codex Adversarial Review

Call `mcp__codex__codex` with `config: {"reasoning_effort": "xhigh"}`:

```
## Adversarial Paper Review

You are Reviewer 2 at {venue}. Your job is to find reasons to REJECT.
You are not helping the authors — you are building a prosecution case.
Every attack must be grounded in what the paper says or fails to say.

### Fair Target Lock
Before attacking, state in 2-4 bullets what the paper claims, using only
what is written. Do not improve, steelman, praise, list agreements, or
describe what you learned. Then attack those claims.

### Paper Text
{raw paper text}

### Review Dimensions
All attacks must map to at least one evaluation dimension:
- **Quality/Rigor**: claims supported? baselines fair? ablations complete?
- **Clarity**: reproducible? notation consistent? self-contained?
- **Significance**: impactful? important problem? will others build on this?
- **Originality**: new insights? how different from prior work?

### Attack Categories
Classify each weakness:
- Unsupported claims | Missing baselines | Statistical weakness
- Novelty concerns | Reproducibility gaps | Logical leaps
- Scope overclaims | Presentation mismatch | Figure/table issues

### Fatality Gates
An attack is "fatal" ONLY if it satisfies at least one:
1. Core claim unsupported by the paper's own evidence
2. Main experimental comparison is invalid or missing an essential baseline
3. Claimed novelty collapses under obvious prior-work framing
4. Method cannot answer the stated research question
5. Results contradict the conclusion
6. Scope of claim greatly exceeds tested setting

Multiple major attacks can still justify rejection without a single fatal.

### Output Format
For each attack:
- **Category**: one of the attack categories above
- **Dimension violated**: Quality / Clarity / Significance / Originality
- **Venue criterion**: e.g., "ICLR Soundness", "NeurIPS Quality"
- **Severity**: fatal (passes a fatality gate) / major / minor
- **Confidence**: high / medium / low
- **Claim attacked**: the specific text being challenged
- **Attack**: why this is weak — be specific
- **Evidence from paper**: what the paper says (or doesn't say)
- **What would fix it**: specific revision needed
- **Falsifier**: what would make this attack invalid

After all attacks:

### Strongest Rejection Case
One paragraph: the single most compelling narrative for why this paper
should be rejected. Not a list — a coherent argument a real reviewer
would write in their overall assessment. Ground it in specific attacks.

### Hostile Review Score
- **Recommendation**: Reject / Weak Reject / Borderline / Weak Accept
- **{venue} score**: {use actual venue scale — NeurIPS 1-6 / ICLR 1-10}
- **Subscores** (if ICLR): Soundness X/4, Presentation X/4, Contribution X/4
- **Score driver**: the single factor most responsible for this score
- **What would flip**: minimum changes to move up one tier
- **Label**: "This is a hostile reviewer score, not an objective assessment."

### Attack Summary
- Total: N (F fatal, M major, m minor)
- Dimension distribution: Quality X, Significance Y, Originality Z, Clarity W
- Pattern: [if attacks cluster, note it]
```

Save the `threadId` for follow-up.

## Step 4: Claude's Evaluation

For each attack, Claude evaluates independently:

- **Legitimate**: real gap. Note what authors should do.
- **Partially valid**: overstated or missing context. Note what's valid.
- **Unfair**: misunderstands paper, applies wrong standards. Note why.

Do NOT filter out attacks. Present all — the user decides what to address.

### Execution Self-Check

Before presenting, verify:
- Is each attack specific enough to be actionable? (Not "experiments are weak"
  but "missing comparison with method X on dataset Y")
- Did any attack confuse an expression problem with a method defect?
- Does the hostile score reflect the actual attacks, not just adversarial
  momentum?

These checks come from reviewer-view-paper's execution protocol — they
prevent false fatal attacks from inflating the rejection case.

## Step 5: Present Results

```markdown
## Adversarial Review: {section/claim}

**Venue**: {venue} | **Hostile Score**: {score} | **Attacks**: {N}
**Dimension distribution**: Quality {X}, Significance {Y}, Originality {Z}, Clarity {W}

### Fair Target Lock
{Codex's 2-4 bullet understanding of the paper's claims}

### Fatal Attacks
#### [{category}] [{dimension}] {title}
- **Claim**: {quoted text}
- **Attack**: {why weak}
- **Venue criterion**: {which review criterion this violates}
- **Fix**: {what would address it}
- **Falsifier**: {what invalidates this attack}
- **Claude**: {legitimate / partial / unfair} — {reason}

### Major Attacks
{same format}

### Minor Attacks
{condensed — one paragraph each}

### Strongest Rejection Case
{Codex's one-paragraph rejection narrative}
**Claude's assessment**: {does this narrative hold up?}

### Pattern Analysis
{where attacks cluster — paper's primary vulnerability}

### Defense Priority
1. {highest priority}
2. ...

### What Would Flip the Score
{from Codex's "what would flip" + falsifiers}
```

## Follow-Up

### Rebuttal Gate

When the user challenges an attack, send their defense to Codex via
`mcp__codex__codex-reply`. Codex must choose one action per attack:

- **Withdraw**: rebuttal directly falsifies the attack
- **Downgrade**: rebuttal weakens severity but leaves a real concern
- **Maintain**: rebuttal is partial, unsupported, or doesn't address the core
- **Strengthen**: rebuttal reveals an additional gap

Concession requires new evidence, corrected reading, or direct logical
refutation. Author persistence alone is not evidence. If Codex refuses
valid rebuttals, Claude flags "unfair persistence" in the assessment.

### Other Follow-Up

- **Elaborate**: ask Codex to expand on a specific finding
- **Review revisions**: fresh `mcp__codex__codex` call (blind to prior round)
- **Escalate to full draft**: run multi-pass after section-level review

## Multi-Pass for Full Draft Review

1. Split into: abstract+intro, method, experiments, discussion
2. Independent Codex calls per section (fresh calls for independence)
3. Cross-section consistency call: do experiments test intro claims?
   Are numbers consistent? Does method support what experiments measure?
4. Merge attacks, dedup by claim (keep higher severity), present

## Behavioral Rules

- **Blind independence**: Codex gets raw text only. No Claude opinions.
- **Adversarial framing is non-negotiable**: "REJECT" stays. Standards make
  attacks sharper, not gentler.
- **Present all attacks**: Claude evaluates but never suppresses.
- **Every attack needs a falsifier**: unfalsifiable complaints are not attacks.
- **No auto-revision**: present findings, user decides.
- **Standards-bound prosecution**: attacks must map to a review dimension
  and venue criterion. Hostility without standards is noise.

## Codex MCP

- **First call**: `mcp__codex__codex` with `config: {"reasoning_effort": "xhigh"}`
- **Follow-ups on same section**: `mcp__codex__codex-reply` with saved `threadId`
- **New section or re-review**: fresh `mcp__codex__codex` call (independent)
- On MCP error: tell user, offer Claude-only adversarial review
