---
name: abstract-intro-audit
description: "Audit academic paper abstracts and introductions against empirical structural patterns from 956 CVPR 2025/2026 Highlight papers. Checks structural completeness, component word count balance, pattern matching, and composition quality. Use when the user wants to check, review, or get structural feedback on their abstract or introduction. Trigger on: '检查abstract', '审查intro', 'audit my abstract', 'check my introduction', '摘要结构检查', '看看abstract写得怎么样', '帮我看看摘要', 'intro结构', 'abstract结构', 'review my abstract', 'introduction structure check', '摘要审查', '前言检查', or when the user pastes abstract/intro text asking for structural advice. Also trigger when the user is drafting an abstract/intro and wants guidance on what components to include or how to balance them. Most applicable to CV/ML conference papers (empirical data from CVPR); use cautiously for adjacent venues (NeurIPS, ICLR, ECCV). NOT for paragraph-level writing quality (use /oral-paragraph-audit), grammar checks, or full-paper review."
---

# Abstract & Introduction Structural Audit

Audit a paper's abstract and/or introduction against empirical patterns
extracted from 956 CVPR 2025/2026 Highlight papers (385 from 2025, 571
from 2026). This is a structural auditor — it checks what components are
present, whether they are proportionally balanced, and which composition
pattern the text follows. It does not rewrite the text or judge writing
quality at the sentence level.

## Philosophy

Abstract and introduction determine how reviewers first frame the paper's
story and contributions. These sections cannot be fully outsourced to AI —
narrative arc, problem framing, contribution ordering, and pacing require
the author's judgment. But authors (especially newer ones) often lack a
mental model of what structural components to include, how much to write
for each, or what sentence patterns are effective. This skill bridges that
gap with empirical data, not opinions.

## Input

Accept any of:
- A LaTeX file path — extract `\begin{abstract}...\end{abstract}` and/or
  the Introduction section (from `\section{Introduction}` to the next
  `\section{}`)
- Pasted text — identify whether it is abstract, intro, or both
- A specific target: "check my abstract" vs "review the intro"

When given a full LaTeX file, strip LaTeX commands, citations, and math
environments for word counting, but preserve them in any quoted text.

## Audit Workflow

### Step 0: Paper-Type Classification

Before auditing, classify the paper type. Different types have legitimately
different structural norms — a dataset paper should not be penalized for
having a short method section.

| Paper Type | Expected Abstract Emphasis | Expected Intro Emphasis |
|------------|---------------------------|------------------------|
| **Method** (default) | Gap → Method → Results | Gap depth + method proportion |
| **Dataset / Benchmark** | Data scope, collection, tasks, access; **Expected results**: model evaluation findings, human alignment scores, coverage statistics | Dataset motivation, comparison to existing, usage protocol |
| **Application** | Domain problem → adaptation → domain results | Domain-specific gap, practical impact |
| **Theory** | Assumptions → theorem statement → implications | Formal problem setup, proof sketch, theoretical contribution |
| **Survey / Analysis** | Scope → methodology → key findings | Taxonomy, coverage criteria, synthesis contribution |
| **Resource / Tool** | Capability → design → adoption evidence | Ecosystem gap, design decisions, community value |

If the paper type is unclear, default to **Method** (the most common type
in the CVPR corpus). State the inferred type in the report so the user can
correct it. When the type is non-Method, relax checks that assume Method
norms (e.g., method proportion, results specificity) and apply type-specific
expectations instead.

### Step 1: Extract and Segment

1. Extract the target text (abstract, intro, or both)
2. Count total words (exclude LaTeX commands, `\cite{}`, math environments)
3. Segment into structural components using semantic understanding:
   - **Abstract components**: Background, Task Definition, Research Gap,
     Method Overview, Contribution Claims, Result Highlights, Significance
   - **Intro components**: Background, Task Definition, Research Gap,
     Related Work Overview, Method Overview, Contribution Statement,
     Itemized Contributions, Result Highlights, Significance, Paper
     Organization

Mark each component's start/end sentences and word count.

**Segmentation guidance** — components are semantic functions, not rigid
blocks. Apply these rules for consistent labeling:
- A sentence can serve multiple functions (e.g., "Despite X, existing
  methods fail to Y" = Background + Gap). Assign to the **primary** function.
- Boundary heuristic: a new component starts when the rhetorical purpose
  shifts (introducing a limitation, proposing a solution, reporting results).
- When a sentence is genuinely ambiguous, assign to the component that
  makes the structural pattern more complete, and note low confidence.
- Sentences opening with "We introduce/propose/present [METHOD]" are
  **Method Overview**, even when in S1 position — do not classify as
  Background just because they appear first.
- Short abstracts (< 150 words) often merge components. A single sentence
  like "We propose X for Y, achieving Z" covers Method + Task + Results.
  This is compression, not absence — do not flag merged components as
  missing (see Component Merging below).

### Step 2: Pattern Matching

Identify which structural pattern the text most closely follows (see
the pattern tables below). Report:
- The matched pattern and its prevalence percentage
- Which components are present vs expected
- Whether the component order matches or deviates

**Important**: Pattern matching is **descriptive metadata, not a scoring
criterion**. The abstract patterns cover ~60% and intro patterns cover ~28%
of the corpus — most good papers will NOT perfectly match a named pattern.
"No dominant pattern match" is a normal, acceptable outcome. Report the
closest pattern for reference but never penalize non-matching structure
alone. Only flag structure as a concern when it harms reader comprehension
or omits functionally important components.

### Step 3: Quantitative Checks

For each component, compare word count against the empirical IQR. These
are **advisory signals, not pass/fail gates** — flag as risk, not defect.
Explain why the paper may intentionally deviate.

- **✓** Within IQR — well-balanced
- **⚠** Outside IQR but within Q1−1.5×IQR or Q3+1.5×IQR — slightly out
  of proportion, note possible reason
- **✗** Beyond Tukey fences — significantly out of proportion, verify intent

Also check the total word count against the section-level IQR.

**Component merging tolerance**: Strong abstracts often compress multiple
functions into single sentences. Recognize these merging patterns:
- "We propose X for Y, achieving Z" = Method + Task + Results
- "Despite progress in X, Y remains challenging due to Z" = Background + Gap
- "To address X, we introduce Y which achieves Z on W" = Gap + Method + Results

When components appear merged rather than absent, report them as "merged
into [component]" rather than "missing." Only flag as missing when the
reader genuinely cannot infer the function from the text. Short abstracts
(< 150 words) should expect merging; flag absence only when the text has
room but omits a key function.

### Step 4: Structural Quality Checks

Run these targeted checks:

**Abstract checks:**
1. **Method dominance**: Method overview should be ~45-50% of total words.
   If Background + Gap exceeds 40%, the abstract is likely unfocused.
2. **Results specificity**: Look for benchmark names, metric values, or
   quantified improvements. "Extensive experiments demonstrate effectiveness"
   alone is weak — flag unless paired with specifics.
3. **Opening pattern**: Does the first sentence follow an effective opening
   pattern? (See template data.) Avoid "In this paper, we..." as the
   opening — it wastes the reader's highest-attention position.
   SPJ's "Molehills not mountains" principle: a concrete example or specific
   problem beats grand claims. "Computer programs often have bugs. It is
   very important..." → Yawn. "Consider this program, which has an
   interesting bug..." → Cool!
4. **Significance closure**: Pattern 2 (with significance) covers 27.8% of
   top papers — if missing, note that a closing sentence about availability,
   impact, or future direction is a strong finishing move.
5. **Self-containment**: No bare symbols, no section/table references, no
   undefined jargon (align with oral-paragraph-audit Check 7 rules).
6. **"One ping" test** (Simon Peyton Jones): Can the reader identify one
   clear, sharp idea after reading the abstract? If the abstract tries to
   convey multiple disconnected ideas, flag. The abstract should have
   exactly "one ping" — the reader should know what the paper's key insight
   is. Many papers contain good ideas but do not distil what they are.
7. **Kent Beck's 4-sentence check**: As a secondary lens, verify the abstract
   covers: (1) State the problem, (2) Say why it's interesting, (3) Say
   what your solution achieves, (4) Say what follows from your solution.
   CVPR papers expand this to ~10 sentences, but the 4 functions must
   all be present.
8. **Antipattern detection**: Flag these specific problems:
   - Citations in abstract (should be self-contained)
   - Undefined abbreviations (unless venue-universal: CNN, GAN, NLP, LLM,
     VLM, ViT, NeRF, SOTA, 3DGS, MLP, VAE, CLIP)
   - Results not explained ("achieves 95.2%" without saying what that means)
   - Information not in the paper body (abstract promises not delivered)
   - Abstract reads like a mini-introduction (too much background, no result)
   - Excessive repetition of key terms (note but do not treat as a
     structural finding — recommend `/oral-paragraph-audit` for prose quality)

**Introduction checks:**
1. **Itemized contributions**: Present in ~96% of top-3 patterns. If missing,
   flag as the single highest-impact structural addition.
2. **Contribution refutability** (SPJ): Each contribution bullet must be
   specific enough that a reader can tell whether it is true. Flag vague
   contributions:
   - BAD: "We describe the X system. It is really cool."
   - GOOD: "We give the syntax and semantics of a language that supports
     concurrent processes (Section 3). Its innovative features are..."
   - BAD: "We study its properties"
   - GOOD: "We prove that the type system is sound, and that type checking
     is decidable (Section 4)"
   Each bullet should include a forward reference to the section providing
   evidence.
3. **Gap depth**: Research gap should be substantial (150-180 words average
   in Patterns 1-3). A shallow gap — one sentence of "existing methods have
   limitations" — is a top rejection signal.
4. **Method proportion**: Method overview is the longest section (~230 words
   average). If it is shorter than the gap section, the intro may feel
   complaint-heavy rather than solution-oriented.
5. **Result preview**: Brief (~32 words) — should preview the key takeaway
   without repeating the abstract's numbers verbatim.
6. **Related work placement**: SPJ strongly advises against putting related
   work before the reader understands your idea — it blocks the reader from
   reaching your contribution. CVPR data shows related work *in* intro is
   common (Patterns 1-3 all include it), but it should serve positioning,
   not comprehensive survey. If the related work section is longer than
   the method overview, flag — the reader may feel "I feel stupid / I feel
   tired" before reaching the idea.
7. **Forward references** (SPJ): "Check each claim in the introduction,
   identify the evidence, and forward-reference it from the claim." Each
   contribution bullet should point to the section that delivers evidence.
   The introduction should survey the whole paper via forward references,
   not via a mechanical "The rest of this paper is structured as follows..."
   paragraph. Flag any such mechanical roadmap paragraph.
8. **Narrative arc**: The intro should follow a natural story flow (SPJ's
   whiteboard model): Here is a problem → It's interesting → It's unsolved
   → Here is my idea → My idea works → Comparison. Check whether the
   components form this progressive arc rather than a disconnected list.

**Cross-section checks** (when both abstract and intro are available):
1. **Story alignment**: Same problem framing, same contribution emphasis?
   If the abstract frames the problem as efficiency but the intro frames
   it as accuracy, flag the inconsistency.
2. **Contribution match**: Each abstract claim should map to an intro bullet.
   Each intro bullet should trace back to an abstract claim.
3. **Progressive disclosure**: The intro should expand on the abstract, not
   repeat it. Check for verbatim overlap (>15 consecutive words = flag).

### Step 5: Template Suggestions

For weak or missing components, read the relevant reference file and
suggest 2-3 effective sentence templates with frequency data. Frame
these as "patterns that work well in top papers" — not prescriptions.

- Abstract templates: `references/abstract-templates.md`
- Intro templates: `references/intro-templates.md`

### Step 6: Report

Choose the report mode based on user request:

**Quick mode** (default for "快速看一下", "top issues", "quick check"):
```
# Quick Audit: [Paper Title]
**Type**: [paper type] | **Words**: [N] ([✓/⚠/✗] vs IQR [range]) | **Pattern**: [closest]

**Top 3 Issues:**
1. [Severity] [Issue] — [one-line fix]
2. [Severity] [Issue] — [one-line fix]
3. [Severity] [Issue] — [one-line fix]

**Verdict**: [one sentence overall assessment]
```

**Full mode** (default for all other requests):
Produce the structured report (see Output Format below).

---

## Abstract Empirical Data

**Source**: 956 CVPR 2025/2026 Highlight papers

### Overall
| Statistic | Value |
|-----------|-------|
| Mean words | 191.6 |
| IQR | 168–215 |

### Structural Patterns

**Pattern 1** (31.9%): Background → Research Gap → Method Overview → Result Highlights

| Component | Mean words | IQR |
|-----------|-----------|-----|
| Background | 25.0 | 17–29 |
| Research Gap | 38.1 | 22–49 |
| Method Overview | 93.4 | 73–114 |
| Result Highlights | 30.5 | 21–35 |

**Pattern 2** (27.8%): Background → Research Gap → Method Overview → Result Highlights → Significance

| Component | Mean words | IQR |
|-----------|-----------|-----|
| Background | 27.1 | 18–31 |
| Research Gap | 32.4 | 21–40 |
| Method Overview | 83.4 | 62–106 |
| Result Highlights | 39.1 | 22–51 |
| Significance | 18.7 | 11–25 |

### Proportion Guideline
- Background: ~13% of total
- Research Gap: ~18%
- Method Overview: ~45-50% (the core)
- Result Highlights: ~16%
- Significance (if present): ~10%

---

## Introduction Empirical Data

### Overall
| Statistic | Value |
|-----------|-------|
| Mean words | 705.0 |
| IQR | 593.5–808.2 |

### Structural Patterns

**Pattern 1** (14.3%): Background → Research Gap → Related Work → Method Overview → Itemized Contributions → Result Highlights

| Component | Mean words | IQR |
|-----------|-----------|-----|
| Background | 83.5 | 43–109 |
| Research Gap | 182.4 | 92–231 |
| Related Work | 127.3 | 58–160 |
| Method Overview | 233.9 | 157–298 |
| Itemized Contributions | 106.3 | 82–127 |
| Result Highlights | 32.2 | 18–40 |

**Pattern 2** (7.7%): Background → Task Definition → Research Gap → Related Work → Method Overview → Itemized Contributions → Result Highlights

| Component | Mean words | IQR |
|-----------|-----------|-----|
| Background | 81.9 | 53–103 |
| Task Definition | 37.0 | 21–45 |
| Research Gap | 152.6 | 99–206 |
| Related Work | 109.8 | 60–153 |
| Method Overview | 227.0 | 156–280 |
| Itemized Contributions | 100.4 | 79–121 |
| Result Highlights | 31.3 | 12–43 |

**Pattern 3** (6.2%): Background → Research Gap → Related Work → Method Overview → Itemized Contributions

| Component | Mean words | IQR |
|-----------|-----------|-----|
| Background | 83.7 | 48–100 |
| Research Gap | 155.5 | 66–229 |
| Related Work | 122.1 | 66–163 |
| Method Overview | 197.9 | 142–274 |
| Itemized Contributions | 94.1 | 73–115 |

### Proportion Guideline (Pattern 1)
- Background: ~11%
- Research Gap: ~24% (build the case)
- Related Work: ~17%
- Method Overview: ~31% (the solution)
- Itemized Contributions: ~14%
- Result Highlights: ~4% (brief preview)

---

## Output Format

```
# [Abstract / Introduction] Structural Audit

## Summary
- **Detected pattern**: [Pattern X] ([component sequence], [Y%] of CVPR Highlights)
- **Total words**: [N] (IQR: [range]) [✓/⚠/✗]
- **Components present**: [X/Y expected]
- **Top issues**: [1-3 bullet points, severity-tagged]

## Component Analysis

### [Component Name] (Lines [M]–[N])
- **Words**: [count] (IQR: [range]) [✓/⚠/✗]
- **Proportion**: [X%] of total (expected: ~[Y%])
- **Assessment**: [1-2 sentences]
- **Suggestion**: [if needed — include a template example with frequency]

[repeat for each detected component]

## Missing Components
[List components not found, with:
 - Why it matters (empirical prevalence)
 - Example template from the corpus
 - Where to insert it]

## Cross-Section Consistency [if both abstract and intro audited]
- Story alignment: [OK / flag]
- Contribution match: [OK / flag — list mismatches]
- Verbatim overlap: [OK / flag]

## Recommendations
[2-5 highest-impact structural changes, ordered by priority]
```

## Severity Levels

- **Blocking**: Missing a component present in >80% of top papers (e.g.,
  no itemized contributions in intro, no results in abstract)
- **Major**: Component significantly out of proportion (beyond Tukey fences),
  or structural pattern deviates in a way that weakens the narrative
- **Minor**: Slight imbalance, missing optional components (significance,
  paper organization), or unconventional but not harmful choices

**Every finding in the report must state**: (1) the evidence from the text,
(2) the empirical basis (frequency/IQR), and (3) a plausible reason the
author may have deviated intentionally. This prevents the audit from reading
as a checklist of defects rather than a diagnostic with context. The report
header must also state the inferred paper type and corpus fit confidence.

## Reader Attention Budget (SPJ)

Understanding *who reads what* helps assess structural priority:

| Section | Readers | Implication |
|---------|---------|-------------|
| Title | 1000 | Every word counts |
| Abstract | 100 | Decides whether to read the paper |
| Introduction | 100 | Decides whether to engage deeply |
| Problem / Method | 10 | Only committed readers |
| Details | 3 | Specialists |

This means the abstract and introduction together determine whether 97% of
potential readers ever see your actual contribution. Structural issues in
these sections have outsized impact on a paper's reception.

## Caveats

1. **Venue scope**: Empirical data is from CVPR (computer vision). Most
   applicable to CV/ML conference method papers. Use cautiously for adjacent
   venues (NeurIPS, ICLR, ECCV) — norms vary. Not applicable to theory
   venues (STOC/FOCS), systems venues (OSDI/SOSP), NLP venues with different
   traditions (ACL), or non-CS fields. SPJ/Kent Beck principles are
   CS-universal but the quantitative thresholds are CVPR-specific.
2. **Descriptive, not prescriptive**: The templates show what the majority
   does, not what is "correct." Unconventional structures work when done
   deliberately — flag deviations but don't penalize intentional choices.
3. **Structure, not content**: This skill checks composition architecture.
   It cannot evaluate whether the gap argument is convincing or the method
   is novel — that requires domain expertise.
4. **Approximate word counts**: IQR ranges are guidance. A 220-word abstract
   with IQR upper 215 is fine. Flag only significant outliers.
5. **SPJ's "4 sentences" is a minimum**: Kent Beck's model is a floor, not
   a ceiling. CVPR papers average ~10 sentences in abstracts. The 4-sentence
   check ensures all *functions* are present, not that the abstract is
   literally 4 sentences.

## Sources

Empirical data:
- 956 CVPR 2025/2026 Highlight papers (385 from 2025, 571 from 2026)
- Text processing via DeepSeek API

Writing logic frameworks:
- Simon Peyton Jones, "How to Write a Great Research Paper" (7 suggestions)
- Kent Beck's 4-sentence abstract model (via SPJ)
- Evans & Bellemare structural analysis (intro hook, research question)
- "Twelve Common Mistakes When Writing an Abstract" (Writing Clear Science)

## Handoff to Other Skills

- **Paragraph-level quality**: after structural audit, use `/oral-paragraph-audit`
  to check writing quality within each paragraph (density, transitions,
  claims, de-AI)
- **De-AI pass**: if the text reads as AI-generated, use `/deai-latex`
- **Full-paper check**: for a holistic pre-submission audit, use
  `/paper-presubmit-audit`
- **Figure/table audit**: `/figure-audit` for visual elements

Do not auto-invoke other skills. Present findings, let the user decide.
