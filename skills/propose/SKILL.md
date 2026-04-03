---
name: propose
description: Propose a new compression method, research direction, or feature — brainstorm, clarify, and file a GitHub issue. Use when user says "提议", "propose", "new idea", "我有个想法", or wants to propose something new.
user_invocable: true
---

# Propose

Guide the user through proposing a new compression method, research direction, or feature for SVD_LLM.

## Step 1: Identify the Proposal Type

Ask the user what they want to propose:
- **Compression method** — new SVD/low-rank compression strategy
- **Rank allocation** — new way to allocate ranks across layers
- **Fine-tuning strategy** — new post-compression recovery approach
- **Evaluation** — new benchmarks, metrics, or models to evaluate
- **Feature** — tooling, CI, documentation, etc.

## Step 2: Brainstorm

For **compression/rank/fine-tuning** proposals:
1. What is the core idea? (1-2 sentences)
2. What is the mathematical formulation?
3. How does it differ from the existing `svd_llm_w` method?
4. What improvement is expected? (perplexity, speed, memory)
5. Are there relevant papers? (search arXiv/Google Scholar for related work)

For **feature** proposals:
1. What problem does this solve?
2. What is the expected user workflow?
3. What files/modules are affected?

## Step 3: Novelty Check

For research proposals, verify novelty:
- Search recent literature for similar approaches
- Check existing issues/PRs for overlap
- Compare with methods in `docs/technical_report.md`

## Step 4: Draft Issue

Create a structured GitHub issue:

```bash
gh issue create --title "[<type>] <title>" --body "$(cat <<'EOF'
## Summary
<1-2 sentence description>

## Motivation
<Why this is useful>

## Technical Approach
<Mathematical formulation or implementation plan>

## Related Work
<References to relevant papers>

## Expected Impact
<What improvement is expected>

## Implementation Plan
- [ ] Step 1: ...
- [ ] Step 2: ...
- [ ] Step 3: ...
EOF
)"
```

## Step 5: Confirm

Present the draft to the user before creating. Allow edits.

After creation, suggest next steps:
- `/issue-to-pr $ISSUE` to start implementation
- `/check-issue $ISSUE` to validate quality
