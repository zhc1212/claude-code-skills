---
name: codex-paper-adversary
description: "Adversarial paper review via Codex MCP — Codex's job is to REJECT, grounded in venue reviewer standards with fatality gates and venue-calibrated scoring. Use whenever the user wants Codex to review their paper adversarially, even if they just say '让codex看看论文' without explicitly saying 'adversarial'. Triggers: \"codex review my paper\", \"hostile review\", \"adversarial paper review\", \"try to reject my paper\", \"codex审我的论文\", \"codex当reviewer\", \"codex挑刺\", \"论文对抗审查\", \"模拟拒稿\", \"让codex看看论文\", \"codex帮我审论文\". Not for code review (/codex-review), multi-persona review (/academic-paper-reviewer), or single-reviewer harsh review (/reviewer-view-paper)."
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

### Auto Full-Text Review (default)
Claude resolves the complete .tex source (including \input{}), merges into
a single text, and routes by token count:
- **< 25K tokens**: single Codex call for holistic review
- **≥ 25K tokens**: auto-splits into Multi-Pass Review

This is the default because adversarial review works best on the full paper
— section-local attacks miss cross-section inconsistencies.

### Section Review
User provides a specific section or excerpt. Claude reads it, extracts
claims (for Claude's own evaluation in Step 3 — NOT sent to Codex), and
builds the adversarial packet. Best for iterative hardening of a specific
section after the full review has identified problem areas.

### Claim Review
User provides specific claims or contributions. Best for stress-testing
bold claims before submission.

### Multi-Pass Review (manual)
Explicitly requested by user, or auto-triggered when merged text ≥ 25K
tokens. Claude splits by section headings, runs independent Codex calls
per section with a paper capsule for context (see below), then runs a
cross-section consistency pass.

## Input Resolution

### .tex (single file)
Read the file directly. Strip LaTeX comments (`%...`). Send text as-is.

### .tex (multi-file with \input{})
1. Read the root .tex file
2. Resolve all `\input{...}` and `\include{...}` recursively
3. Strip comments
4. Merge into a single text block with `% === section: filename ===` markers
5. Build a figure/table inventory (see below)

### PDF
1. Read the PDF with the Read tool (multimodal)
2. Extract visible text per page
3. For figures/tables, record captions and what they visually show
4. Assemble into text for the adversarial packet

### Other formats (.docx, Overleaf link, pasted text)
- **.docx**: ask user to export as PDF first — Word formatting doesn't preserve LaTeX structure
- **Overleaf**: ask user to download the .tex source or compiled PDF
- **Pasted text**: treat as Section Review mode
- **No figures at all**: skip the figure inventory, note "no figures" in the packet

### Figure/Table Protocol (tiered)

Codex cannot see images. Use a tiered description protocol:

**All figures/tables** (always include):
- Caption text verbatim
- `\label{}` for cross-reference tracking
- Role in the paper's argument (what claim does this support?)

**Review-critical figures** (supports a main claim, contains quantitative
comparisons, or has multiple panels with distinct results):
- Axes, variables, units
- Baselines and data series shown
- Visible trends and key numbers
- Error bars / uncertainty if present
- For multi-panel: panel-by-panel description

**Non-critical decorative/overview figures**: brief factual inventory only.

Mark any attack that depends on visual inspection as `[visual-only]` —
Claude verifies these since Codex reviewed blind to the image.

## Protocol

```
1. User provides section text, .tex path, PDF path, or claims
2. Resolve input (merge .tex, extract PDF, build figure inventory)
3. Claude builds adversarial packet (raw text + venue standards)
   — Section mode: Claude also extracts claims for own Step 5 eval
   — Full/Multi-Pass: NO claim pre-extraction (blind independence)
4. Codex adversarial review: Fair Target Lock → find reasons to REJECT
5. Claude evaluates each attack (legitimate / partially valid / unfair)
6. Claude self-checks: actionable? expression≠method? score objective?
7. Present: all attacks (numbered A01...) + Claude's assessment
8. Follow-up: challenge specific attacks via Rebuttal Gate
```

## Step 1: Build Adversarial Packet

Include: raw paper text (unmodified), figure/table inventory with captions,
venue and review standards, adversarial framing with Fair Target Lock.

If the user specified a venue, note it. If not, ask: "Which venue? Reviewer
expectations differ." Default to ICLR/NeurIPS if unspecified.

If the paper is in Chinese (or another non-English language), note this in
the packet so Codex reviews in the paper's language.

**Do NOT include** Claude's interpretation, Claude's claims analysis, or
hints about what might be weak. Blind independence is the entire point.

## Step 2: Codex Adversarial Review

Call `mcp__codex__codex` with `config: {"model": "gpt-5.6-sol", "reasoning_effort": "max"}`.
See `references/codex-prompt-template.md` for the full prompt.

Key elements of the prompt:
- "You are Reviewer 2 at {venue}. Your job is to find reasons to REJECT."
- Fair Target Lock: 2-4 bullets of paper's claims before attacking
- Review Dimensions: Quality/Rigor, Clarity, Significance, Originality
- 12 attack categories with dimension mapping
- 6 fatality gates (each must cite source span + venue consequence)
- Numbered output: A01, A02, ... with category, dimension, severity,
  confidence, claim attacked, attack, evidence, fix, falsifier
- Strongest Rejection Case (1 paragraph narrative)
- Hostile Review Score (venue-calibrated)
- `[visual-only]` marker for figure-dependent attacks

Save the `threadId` for follow-up.

## Step 3: Claude's Evaluation

For each attack, Claude evaluates independently:

- **Legitimate**: real gap. Note what authors should do.
- **Partially valid**: overstated or missing context. Note what's valid.
- **Unfair**: misunderstands paper, applies wrong standards. Note why.

For `[visual-only]` attacks, Claude verifies against the actual figure —
Codex attacked based on text description only; Claude has seen the image.

Do NOT filter out attacks. Present all — the user decides what to address.

### Execution Self-Check

Before presenting, verify:
- Is each attack specific enough to be actionable? (Not "experiments are weak"
  but "missing comparison with method X on dataset Y")
- Did any attack confuse an expression problem with a method defect?
- Does the hostile score reflect the actual attacks, not just adversarial
  momentum?

## Step 4: Present Results

```markdown
## Adversarial Review: {paper/section}

**Venue**: {venue} | **Hostile Score**: {score} | **Attacks**: {N}
**Dimension distribution**: Quality {X}, Significance {Y}, Originality {Z}, Clarity {W}
**Input mode**: {section / full-tex / multi-pass} | **Tokens sent**: ~{N}K

### Fair Target Lock
{Codex's 2-4 bullet understanding of the paper's claims}

### Fatal Attacks
#### A01 [{category}] [{dimension}] {title}
- **Claim**: {quoted text with source location}
- **Attack**: {why weak}
- **Venue criterion**: {which review criterion this violates}
- **Fix**: {what would address it}
- **Falsifier**: {what invalidates this attack}
- **Claude**: {legitimate / partial / unfair} — {reason}

### Major Attacks
{same format, A02, A03, ...}

### Minor Attacks
{condensed — one paragraph each, A0N, ...}

### Strongest Rejection Case
{Codex's one-paragraph rejection narrative}
**Claude's assessment**: {does this narrative hold up?}

### Pattern Analysis
{where attacks cluster — paper's primary vulnerability}

### Defense Priority
1. A{NN}: {highest priority}
2. A{NN}: ...

### What Would Flip the Score
{from Codex's "what would flip" + falsifiers}
```

## Follow-Up

### Rebuttal Gate

When the user challenges an attack, send to Codex via `mcp__codex__codex-reply`
with this structure:

```
The authors rebut attack A{NN} ({category}: {one-line summary}).

Rebuttal: {user's defense text}

Choose one action:
- Withdraw: rebuttal directly falsifies the attack
- Downgrade: rebuttal weakens severity but leaves a real concern
- Maintain: rebuttal is partial, unsupported, or doesn't address the core
- Strengthen: rebuttal reveals an additional gap

State what specific evidence changed your assessment.
Concession requires new evidence, corrected reading, or direct logical
refutation — author persistence alone is not evidence.
```

If Codex refuses valid rebuttals across multiple attacks, Claude flags
"unfair persistence" in the assessment.

### Other Follow-Up

- **Elaborate**: "expand on A03" → `mcp__codex__codex-reply`
- **Review revisions**: fresh `mcp__codex__codex` call (blind to prior round)
- **Escalate**: section review → full-tex or multi-pass review

### Calibration Mode (optional, post-submission)

After receiving real reviewer feedback, compare Codex attacks vs actual
reviews. See `references/calibration.md` for the full protocol.

## Multi-Pass for Full Draft Review

### Paper Capsule (prevents false "missing material" attacks)

Each section pass receives a ~300-500 word capsule alongside the section text:
- Title + target venue
- Abstract (compressed if needed)
- Claimed contributions (2-4 bullets)
- Method identity (3-5 bullets)
- Experiment map: datasets, baselines, metrics, main tables/figures
- **Location map**: where related work, limitations, method details, experiments,
  ablations, and appendix content appear — e.g., "Ablations in §4.4/Table 3;
  complexity analysis in Appendix C"

The location map is the key: it prevents attacks like "paper never discusses X"
when X is in a section Codex hasn't seen yet.

### Multi-Pass Steps

1. Read the merged .tex, identify section headings (`\section{}`, `\subsection{}`)
2. Group into logical review units (combine short sections, keep long ones separate)
3. Build the paper capsule from the full merged text
4. Independent Codex calls per unit (fresh calls, each gets capsule + section text)
5. Cross-section consistency call: do experiments test intro claims?
   Are numbers consistent? Does method support what experiments measure?
6. Merge attacks, dedup by claim (keep higher severity), renumber A01...

## Behavioral Rules

- **Blind independence**: Codex gets raw text only. No Claude opinions.
- **Adversarial framing is non-negotiable**: "REJECT" stays. Standards make
  attacks sharper, not gentler.
- **Present all attacks**: Claude evaluates but never suppresses.
- **Every attack needs a falsifier**: unfalsifiable complaints are not attacks.
- **No auto-revision**: present findings, user decides.
- **Standards-bound prosecution**: attacks must map to a review dimension
  and venue criterion. Hostility without standards is noise.
- **Number every attack**: A01, A02, ... for unambiguous rebuttal reference.

## Codex MCP

- **First call**: `mcp__codex__codex` with `config: {"model": "gpt-5.6-sol", "reasoning_effort": "max"}`
- **Follow-ups on same section**: `mcp__codex__codex-reply` with saved `threadId`
- **New section or re-review**: fresh `mcp__codex__codex` call (independent)
- On MCP error: tell user, offer Claude-only adversarial review (single-model,
  loses cross-model blind-spot coverage — note this limitation to the user)
