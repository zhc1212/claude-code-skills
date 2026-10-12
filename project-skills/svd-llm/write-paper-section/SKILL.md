---
name: write-paper-section
description: Write or improve a section in the LaTeX paper (method, experiments, results). Use when user says "写论文段落", "write paper section", "写实验部分", "update paper", or wants to draft/edit a specific paper section.
user_invocable: true
---

# Write Paper Section

Write or improve a specific section of the LaTeX/technical paper for SVD_LLM.

## Invocation

- `/write-paper-section method` — write/improve the method section
- `/write-paper-section experiments` — write/improve experiments section
- `/write-paper-section results` — write/improve results section
- `/write-paper-section related-work` — write/improve related work

## Step 1: Identify Target

Ask the user which section to write (if not specified):
- **Abstract** — paper summary
- **Introduction** — motivation, contributions
- **Related Work** — prior art on LLM compression, SVD methods, LoRA
- **Method** — whitening, SVD truncation, rank allocation, Sequential LoRA
- **Experiments** — setup, models, baselines, metrics
- **Results** — tables, figures, analysis
- **Conclusion** — summary, future work

## Step 2: Gather Context

Read relevant source files depending on the section:

| Section | Key Sources |
|---------|------------|
| Method | `src/compress/whitening.py`, `src/model/replace.py`, `docs/math_derivation.md` |
| Experiments | `scripts/compress.py`, `scripts/eval_model.py`, `docs/results.md` |
| Results | `docs/results.md`, `data/` directory |
| Related Work | `references.bib`, `docs/technical_report.md` (Markdown overview), `docs/idea.tex` (LaTeX source) |

Also check existing paper files:
```bash
ls docs/*.tex docs/*.md
```

## Step 3: Draft

Write the section following academic conventions:
- Use LaTeX formatting if writing for `.tex` files
- Use precise mathematical notation for method descriptions
- Include proper citations from `references.bib`
- Reference specific equations, figures, and tables
- Follow the paper's existing notation and style

For **results sections**:
- Present data in well-formatted tables
- Compare against baselines (original SVD-LLM paper results)
- Include both perplexity and downstream task metrics
- Note compression ratios and model sizes

## Step 4: Review

Check the drafted section for:
- Mathematical correctness (verify against `docs/math_derivation.md`)
- Consistency with experimental results in `docs/results.md`
- Proper citation format
- No placeholder text left

## Step 5: Integrate

If writing LaTeX:
```bash
# Compile to check for errors
pdflatex docs/idea.tex  # or the target paper file
```

Present the draft to the user for review and refinement.
