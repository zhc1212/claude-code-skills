---
name: weekly-report
description: Generate weekly progress report (周报) in QuAIR LaTeX template. Use when user says "写周报", "weekly report", "周报", "progress report", "本周总结", or at the end of each week. Aggregates git log, experiment results, paper progress, and project state across multiple projects into the standard QuAIR format (Summary → Key Points → Plan).
---

# Weekly Report Generator

Generate a LaTeX weekly progress report following the QuAIR lab template and 周报规范2025. The report is read by the advisor alongside reports from other lab members — keep it technical, concrete, and scannable.

## Configuration

**Weekly notes root:**
```
~/huicheng/weekly_note/
```

**Active project roots** (scan these for evidence; update as projects change):
```
~/huicheng/Lean-QIT-Agent
~/huicheng/SVD_LLM
~/huicheng/LLM_Compression
~/huicheng/Quantum-Matter
~/huicheng/Lean-QIT-Dev
```

If the user invokes the skill from within a project directory and says "只写这个项目" or "single project", gather evidence only from cwd instead of all active projects.

**Template files:**
The canonical `pretex.tex` lives in the weekly notes root or the most recent note directory. Copy it into each new note directory.

## Two-Part Structure (from 周报规范2025)

The report has two parts with different goals and page budgets:

**Part 1 — 项目进展与规划 (Summary + Plan): target ≤ 1 page**
- `\section{Summary of Progress}` (§2.1): enumerate completed tasks with concrete outcomes — one line per item
- `\section{Plan}` (§2.4): concrete TODO checklist + project status table
- Note: in the LaTeX template, Plan appears as §2.4 after Key Points, but its content should be concise enough that Summary + Plan together stay within ~1 page of reading

**Part 2 — 核心技术进展与积累 (Key Points): 1–10 pages**
- Each Key Point = one self-contained technical narrative
- Must be readable by a domain reader without prior weekly reports
- Academic rigor: precise terminology, cite prior work where relevant
- Accumulation-oriented: write as material that can evolve into papers, thesis chapters, or knowledge base entries (per 周报规范 §2.1)
- **Required rhetorical roles** (must appear in every Key Point, but subsection titles are flexible):
  1. **Background and motivation** (含文献调研 per 周报规范 §2.2): why this work matters, what prior work exists, literature context
  2. **Problem definition**: rigorous, self-contained problem or task statement
  3. **Method/Results**: technical approach, analysis, experiments, concrete numbers
  4. **Discussion**: interpretation, takeaways, open questions, implications

### Key Point structure selection

Choose the structure that best fits the content:

**Default (theory/paper/conceptual work)** — use the canonical 4-subsection format:
```
\subsection{Problem and Setup}
\subsection{Preliminaries}
\subsection{Results}
\subsection{Conjectures and Discussions}
```

**Alternative (issue/PR/experiment-driven work)** — use issue-based or experiment-based sections:
```
\section{Issue \#XX: <Descriptive Title>}
\subsection{Motivation}        % ← covers background + problem definition
\subsection{Implementation}    % ← covers method
\subsection{Experiments / A/B Results}  % ← covers results
\subsection{Discussion}        % or \paragraph{Conclusion.} if brief
```

Either structure is acceptable as long as all four rhetorical roles are present. Do NOT generate empty subsections — if a week's work is purely engineering with no new theory, skip Preliminaries and fold background into Motivation.

## Step 1: Determine Scope

Find the most recent note number:
```bash
grep -roh '\\lecture{[0-9]*}' ~/huicheng/weekly_note/张惠程_*/main.tex 2>/dev/null \
  | grep -o '[0-9]*' | sort -n | tail -1
```
Increment by 1 for the new note number.

Determine the date range (Monday–Sunday of the reporting week):
- If invoked **Friday–Sunday**: use the current week (Monday of this week to Sunday)
- If invoked **Monday–Thursday**: use the previous completed week (last Monday to last Sunday)
- If the user specifies a date range, use that

Convert to `YYYY-MM-DD` for git queries.

## Step 2: Gather Evidence (parallel)

These data sources are independent — gather them in parallel.

### Multi-project evidence

For EACH active project root, gather:

**Git commits (all branches):**
```bash
git -C <project_root> log --oneline --since="YYYY-MM-DD" --until="YYYY-MM-DD" --all --no-merges
```

**Paper directory changes:**
```bash
git -C <project_root> log --oneline --since="YYYY-MM-DD" --until="YYYY-MM-DD" -- paper/ 2>/dev/null
```

**Project state:**
Read `<project_root>/.planning/STATE.md` if it exists.

**Issues and PRs:**
```bash
# Extract owner/repo from git remote (handles both HTTPS and SSH)
REMOTE=$(git -C <project_root> remote get-url origin 2>/dev/null)
REPO=$(echo "$REMOTE" | sed -E 's#(https://github.com/|git@github.com:)##; s/\.git$//')
# Skip gh commands if REPO is empty or gh is not authenticated
if [ -n "$REPO" ] && gh auth status &>/dev/null; then
  gh issue list --repo "$REPO" --state all --search "updated:>YYYY-MM-DD" --limit 20 2>/dev/null
  gh pr list --repo "$REPO" --state all --search "updated:>YYYY-MM-DD" --limit 20 2>/dev/null
fi
```

**Experiment artifacts:**
```bash
find <project_root>/models/ <project_root>/outputs/ -newermt "YYYY-MM-DD" -type f 2>/dev/null | head -20
find <project_root> -name "*.log" -newermt "YYYY-MM-DD" -path "*/experiments/*" 2>/dev/null | head -10
```

### Cross-project evidence

**Previous week's Plan (for follow-up):**
Read the most recent `~/huicheng/weekly_note/张惠程_*/main.tex` Plan section. Check whether each planned item was addressed — this informs the Summary.

**Paper reading / literature:**
Check for any new papers read, annotated, or cited this week across all projects. Include in Preliminaries/Background of relevant Key Points.

## Step 3: Identify Key Points

From the evidence, identify 1–3 key points. Each should be a coherent work thread, not a grab-bag. Good key points have a clear goal, concrete results, and a takeaway.

Common patterns from accepted reports:
- **Paper revision cycle**: narrative reframe + writing polish + verification
- **Experiment campaign**: hypothesis → setup → results → interpretation
- **New method/direction**: motivation → implementation → A/B results
- **Theory + empirical validation**: theorem statements → numerical verification
- **Issue-driven development**: problem → implementation → PR → validation

If the week was dominated by one large effort (paper submission, major experiment), 1–2 key points is fine. Do not pad.

**Framework reproduction weeks**: when the week's work is reproducing/implementing an existing paper's framework, structure Key Point 1 as: (1) include the paper's architecture figure, (2) a coverage mapping table showing each component → our implementation + status, (3) E2E validation results. This makes the advisor's reading efficient — they see the target, the mapping, and the evidence.

## Step 4: Create Directory and Files

```bash
NOTES_ROOT=~/huicheng/weekly_note
MOST_RECENT=$(ls -d "$NOTES_ROOT"/张惠程_* 2>/dev/null | sort | tail -1)
NEW_DIR="$NOTES_ROOT/张惠程_<MMDD>_<MMDD>"
mkdir -p "$NEW_DIR"
```

Copy template files from the most recent note or the template directory:
```bash
if [ -f "$MOST_RECENT/pretex.tex" ]; then
  cp "$MOST_RECENT/pretex.tex" "$NEW_DIR/"
elif [ -f "$NOTES_ROOT/张惠程_0307_0313/weekly note template/pretex.tex" ]; then
  cp "$NOTES_ROOT/张惠程_0307_0313/weekly note template/pretex.tex" "$NEW_DIR/"
else
  echo "ERROR: pretex.tex not found. Ask the user for the template location."
  # HARD STOP — do not generate main.tex without pretex.tex
fi
```

**IMPORTANT**: If `pretex.tex` cannot be found, ask the user for its location before proceeding. Do NOT write main.tex without it — compilation will fail.

The `pretex.tex` contains the `\lecture` command (framebox header style), theorem/lemma/proof environments, math macros (`\bra{}`, `\ket{}`, `\norm{}`, `\tr`, `\RR`, calligraphic `\cA`–`\cZ`, etc.), colored boxes (`tBox`, `dBox`, `rBox`), and page numbering. Do NOT redefine `\lecture` in main.tex — it is inherited from pretex.

If the report cites papers, also create `ref.bib` with the relevant BibTeX entries.

## Step 5: Write main.tex

Use this preamble. The `\lecture` command comes from `pretex.tex` — do NOT define it here:

```latex
% -*- TeX -*-
\documentclass[twoside,11pt]{article}

\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
\raggedbottom

\usepackage{array}
\setlength{\tabcolsep}{4mm}
\renewcommand\arraystretch{1.2}

\input{pretex}

\usepackage{geometry}
\geometry{left=25mm,right=25mm,top=25mm,bottom=25mm}

\usepackage[numbers,comma,sort&compress]{natbib}
\usepackage{times}
\usepackage{amsmath,amsfonts,amssymb,graphicx,mathtools,bm,relsize}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{multirow}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{float}

\setlist[enumerate]{leftmargin=2em,itemsep=3pt,topsep=3pt,parsep=0pt}
\setlist[itemize]{leftmargin=2em,itemsep=2pt,topsep=2pt,parsep=0pt}

\begin{document}

\lecture{<N>}{Weekly Note}{Huicheng Zhang}{<Month DDth, YYYY>}
```

Then the body follows this structure (section order per 模板.pdf §2.1–2.4):

```latex
%% ================================================================
%% Summary of Progress  (target: 0.5--1 page, per 周报规范 §4.3)
%% ================================================================

\section{Summary of Progress}

\begin{enumerate}
  \item \textbf{<Project/Topic>}: <1-line summary with concrete numbers>.
  \item \textbf{<Project/Topic>}: <1-line summary>.
\end{enumerate}


%% ================================================================
%% Key Points  (target: 1--10 pages, per 周报规范 §4.3)
%% ================================================================

%% --- Option A: canonical 4-subsection (theory/paper/conceptual work) ---

\section{Key Point 1: <Descriptive Title>}
\label{sec:<label>}

\subsection{Problem and Setup}
% Goal, starting state, why this matters. 1-2 paragraphs.

\subsection{Preliminaries}
% Background, literature context, notation, prior work.
% Per 周报规范 §2.2: include 研究背景与动机(含文献调研).
% Cite relevant papers: \cite{...}

\subsection{Results}
% What happened. Use \paragraph{Name.} for sub-topics.
% Include concrete numbers. Reference tables/figures if any.

\subsection{Conjectures and Discussions}
% Interpretation, takeaways, open questions. 1-2 paragraphs.


%% --- Option B: issue/experiment-driven (alternative structure) ---

\section{Issue \#XX: <Descriptive Title>}
\label{sec:<label2>}

\subsection{Motivation}
% Background + literature context + why this matters.

\subsection{Implementation}
% Technical approach, method description.

\subsection{Experiments}
% A/B results, metrics, concrete numbers.

\paragraph{Discussion.}
% Interpretation, next implications. Can be brief.


%% ================================================================
%% Plan  (after Key Points, per 模板.pdf §2.4)
%% ================================================================

\section{Plan}

\paragraph{Next week TODO.}
\begin{enumerate}
  \item <specific, checkable action item>.
  \item <specific, checkable action item>.
\end{enumerate}

% Project status table (per 模板.pdf Table 2.1)
% Two-tier layout: high-priority above first \midrule, lower-priority below second \midrule
% Use [H] (not [htbp]) to prevent floating to a separate page with large whitespace
\begin{table}[H]
\centering
\caption{Current status of projects and tasks, organized by priority.
  The upper section denotes high-priority tasks; the lower section lists
  tasks scheduled for future attention. Tasks with blockers are labelled On-hold.}
\small
\begin{tabular}{@{}clp{6.5cm}l@{}}
\toprule
Priority & Project/Task & Description & Status \\
\midrule
0 & <project> & <description> & On-going \\
1 & <project> & <description> & On-going \\
\midrule
2 & <project> & <description> & Pending \\
3 & <project> & <description> & On-hold \\
\bottomrule
\end{tabular}
\end{table}


%% ================================================================
%% Appendix  (optional — per 模板.pdf §2.5)
%% ================================================================

% Include Appendix ONLY when the week has:
%   - Formal theorem proofs or lemma statements
%   - Detailed derivations too long for Key Points
%   - Extended tables, symbol conventions, or circuit diagrams
% If none of the above apply, omit the Appendix section entirely.

\section{Appendix}

\subsection{Theorem Proofs}
% Use pretex theorem environments: \begin{theorem}...\end{theorem}
% \begin{proof}...\end{proof}, \begin{lemma}...\end{lemma}

\subsection{Supplementary Tables}
% Extended data tables, symbol conventions, etc.


%% ================================================================
%% References (include ONLY if \cite{} commands are used above)
%% ================================================================
% If no citations exist, omit these two lines entirely.

\bibliographystyle{unsrt}
\bibliography{ref}

\end{document}
```

### Key structural rules (from 模板.pdf and 周报规范2025)

- **Section order**: Summary → Key Points → Plan → Appendix → References (per 模板.pdf §2.1–2.5)
- **Plan has two parts** (per 周报规范 §1.2): (1) a concrete **TODO checklist** with specific, checkable items for next week; (2) a **project status table** (模板.pdf Table 2.1) listing all active projects with Priority, Description, and Status (On-going / Pending / On-hold / Done). The table uses a two-tier layout: high-priority above the first `\midrule`, lower-priority below the second `\midrule`.
- **Rhetorical roles required** in every Key Point: background/motivation (含文献调研), problem definition, method/results, discussion — but subsection titles adapt to content type
- **Page budgets** (per 周报规范 §4.3): Summary = **0.5–1 page**; Key Points = **1–10 pages** (adjust to content depth); Plan = concise
- **No intro paragraph before Summary**: go straight to `\begin{enumerate}`
- **Date format**: "Month DDth, YYYY" (e.g., "June 7th, 2026") — use ordinal suffix
- **Appendix is optional**: include only when formal proofs, derivations, or extended tables exist

### Tables

Use `booktabs` style (`\toprule`, `\midrule`, `\bottomrule`). Common patterns:

**Experiment comparison table:**
```latex
\begin{table}[ht]
\centering
\caption{Description of what's being compared.}
\small
\begin{tabular}{@{}lcc@{}}
\toprule
\textbf{Method} & \textbf{Metric 1} & \textbf{Metric 2} \\
\midrule
Baseline   & value & value \\
\textbf{Ours} & \textbf{value} & \textbf{value} \\
\bottomrule
\end{tabular}
\end{table}
```

**TODO follow-up table** (optional — use when last week had specific planned items to track):
```latex
\begin{table}[htbp]
\centering
\caption{Status of last week's planned items.}
\small
\begin{tabular}{@{}clp{7.5cm}l@{}}
\toprule
\# & Status & Item & Notes \\
\midrule
1 & \textcolor{green!60!black}{Done} & <item> & <ref to section> \\
2 & \textcolor{orange}{Partial} & <item> & <what remains> \\
3 & Not started & <item> & Deferred \\
\bottomrule
\end{tabular}
\end{table}
```

## Step 6: Compile and Verify

**Always run the full compile cycle**, even if you think citations haven't changed — partial compiles cause stale cross-references and missing bibliography:

```bash
cd ~/huicheng/weekly_note/张惠程_<MMDD>_<MMDD>/
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

**CRITICAL: The `cp` to final filename must be the ABSOLUTE LAST operation.**
If you edit and recompile main.tex after copying, the final PDF becomes stale.
Never do any edits between the last compile and the cp. The pattern is:
1. Make all edits
2. Run full compile cycle
3. `cp main.pdf 张惠程-<MMDD>-<MMDD>.pdf`
4. Verify with `md5sum main.pdf 张惠程-<MMDD>-<MMDD>.pdf` — they MUST match

Verify:
- PDF renders without errors
- `md5sum` of `main.pdf` and `张惠程-<MMDD>-<MMDD>.pdf` are identical
- Summary fits within 0.5–1 page
- Each Key Point contains all four rhetorical roles (background, problem, results, discussion)
- Note number is consecutive with the previous week
- Date and directory name match the reporting week
- Page numbering shows `N-1`, `N-2`, etc. (where N = note number)
- Project status table has two-tier layout (if included)
- Figures (if any) are visible in the final PDF — check with `pdfimages -list`

## Step 7: Submission Checklist

Per 周报规范2025 §2.2:

1. **Filename**: Rename compiled PDF to `张惠程-<MMDD>-<MMDD>.pdf` (e.g., `张惠程-0614-0620.pdf`)
   ```bash
   cp main.pdf ~/huicheng/weekly_note/张惠程_<MMDD>_<MMDD>/张惠程-<MMDD>-<MMDD>.pdf
   ```
   Note: directory uses underscores (`张惠程_0614_0620/`), PDF filename uses hyphens (`张惠程-0614-0620.pdf`) per 周报规范. MMDD format without year is standard (e.g., `0614-0620` not `20260614-20260620`).
2. **Deadline**: Submit before Friday end of work (every week)
3. **Channel**: Send the PDF via Zulip to the advisor
4. **Quick sanity check before sending**:
   - [ ] Summary is concise (≤1 page with Plan)
   - [ ] Key Points are self-contained (a domain reader can follow without prior reports)
   - [ ] Literature context included where relevant (per 规范 §2.2)
   - [ ] All numbers are accurate and reproducible
   - [ ] No target conference names unless explicitly intended

## Writing Guidelines

Distilled from 周报规范2025 and accepted reports:

- **Numbers over adjectives**: "PPL 42.1 → 11.4" not "significantly improved"
- **Reference project trackers**: "\#74 Block-Granularity" not just "the paper"
- **Bold the lead**: each list item starts with `\textbf{Topic}:` then detail
- **Summary items are one-liners**: compress a week's thread into one sentence with key numbers
- **Plan items are actionable**: "complete 13B downstream evaluation" not "continue working on paper"
- **Self-contained Key Points**: domain reader should understand without prior reports
- **Literature context**: include research background and prior work references in Key Points, especially for new directions or theoretical work (per 周报规范 §2.2: 研究背景与动机含文献调研)
- **Accumulation-oriented**: write Key Points as material that can evolve into paper sections, thesis chapters, or knowledge base entries (per 周报规范 §2.1)
- **Enumerate for Summary/Plan** (ordered), **itemize for Results** (unordered)
- **Figures optional**: include only when a result is best shown visually. Most weeks are text-only. When used, figures must have clear titles and descriptions (per 规范 §4.2)
- **Figures from papers**: when reproducing a paper's framework, include the original figure with proper attribution (`reproduced from~\cite{...}, Figure~N`). Crop with `pdftoppm` + `convert -crop` to remove page numbers, headers, and other artifacts. Verify the figure is visible in the final PDF with `pdfimages -list`.
- **Factual accuracy**: verify all numbers (commit counts, line counts, test counts, PR stats) against `git log`, `gh pr view`, and CI output before writing. When citing issue/PR numbers, double-check they exist. Never cite a published paper for internal activities (e.g., internal debates).
- **Branch/merge status**: always explicitly state if the main work is on an unmerged branch or draft PR. The advisor needs to know what has actually landed on `main`.
- **Issue counts**: count actual issues (e.g., #65, #66, #67, #68 = 4 issues), don't group into abstract "features" with a different count
- **English throughout**: lab template is in English
- **Academic tone**: precise terminology, objective language (per 规范 §4.1)
- **No target conference names** unless user explicitly includes them
- **Math notation**: use pretex macros (`\RR`, `\norm{}`, `\tr`, `\bra{}`, `\ket{}`, etc.)
- **Equation numbering**: inherits from pretex — equations auto-numbered as `N.1`, `N.2`, etc.
- **Theorem environments**: use pretex environments (`theorem`, `lemma`, `corollary`, `proposition`, `definition`, `example`, `remark`, `proof`) — do not redefine them
