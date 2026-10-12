---
name: notation-audit
description: "Audits the notation of a whole LaTeX paper (symbols, acronyms, coined names, equation numbers) against four rules: defined before use, defined once, one meaning per symbol, and none the paper does not need. Use when the user asks to check or unify a paper's symbols or notation (符号检查, 统一处理符号, notation check), and from paper-presubmit-audit Check 5. Returns a candidate list and edits nothing; one paragraph's formulas go to oral-paragraph-audit Check 9, word terminology to paper-presubmit-audit Check 16."
---

# Notation Audit

A reader meets each symbol, acronym, and coined name (a name the paper gives
its own arm, baseline, or control: Static, Oracle) once, at or before its
first use, with one meaning, and only where words would not do. The audit lists
every place the paper breaks that, plus the consistency checks below; the
author decides each candidate.

## Rules

1. **Defined before use.** Count use in the reading order of the compiled PDF:
   a float or caption that lands above its defining prose uses the symbol
   first; a float and its caption read as one unit, so a caption legend defines
   the symbols of its own float. Each separately uploaded PDF is its own
   document; an appendix in the same PDF shares the body's definitions. The
   definition gives type, domain, shape, or unit as applies ($\mathbf a \in
   \mathbb R^N$, $\tau > 0$, a budget counted in parameters), and every index
   range, summation set, and optimization domain is explicit, in words or
   symbols ("each sublayer $j$" states a range), and an index runs over the
   same range wherever it recurs. A `where` clause directly after a display
   defines at first use.
2. **Defined once.** After its definition a symbol, acronym, or coined name is
   only used. A recap paragraph, an appendix notation list, a caption gloss of
   a symbol or name the text defines, or a later sentence that writes the
   defining formula again is a candidate; a pointer ("§3") replaces it and
   keeps a float readable alone. A caption that defines a symbol only its float
   uses is a legend, not a repeat. The expression inside a later equation is a
   use. A second definition with different content (another dimension, another
   formula) is also a collision.
3. **One meaning per symbol (collision).** A symbol or name that reads two ways
   in overlapping scope: a loop index and a module name both written $k$; one
   coined name for two different arms; a step count $T$ in the same algorithm
   as a transpose $^T$. Two symbols that share a base letter but differ in
   subscript type (an indexed matrix $B_j$, a scalar $B_{\text{target}}$) are a
   candidate for the author's call.
4. **Occam.** Every symbol, acronym, coined name, and equation number earns its
   place. One used once or twice where words carry it, a second name for a
   defined quantity (a code identifier beside the paper's name: `q_proj` beside
   Q), an acronym used once, and a numbered display never referenced are
   candidates.

Consistency checks:

5. **Variants.** Where the paper distinguishes forms of one quantity (pre-clip,
   clipped, integer, final), each use carries the right form, and the
   distinction is stated where the reader first meets it. Edits drift these
   silently, so read every use.
6. **Typography.** One convention per kind: vectors bold and their components
   not; operators and word subscripts upright, one command per operator (under
   `times`, `\text` and `\mathrm` render in different fonts); one transpose
   symbol; one rendered spacing style for inline relations ($\rho{=}0.6$ or
   $\rho = 0.6$, count both; spaces in math source do not render); numbers
   formatted alike everywhere, in math and prose, with one thousands separator.
   A footnote marker sits after a word, since on a symbol it renders as an
   exponent.
7. **Figures and captions.** Symbols drawn in figure images and used in
   captions match the text's and are reachable in the same document.
8. **Displays and relations.** Each display is punctuated as part of its
   sentence. Each relation symbol matches the claim: identity, definition,
   approximation, or measured value. An approximate or fitted relation written
   with $=$ is a candidate; an equality exact over the stated cases, and a
   measured value ("accuracy $= 82\%$"), are not.
9. **Prose.** Sentences open on a word; two formulas are separated by words;
   the abstract and headings carry no undefined symbol.

Exempt: an overview figure whose labels name its symbols (a preview); a dummy
index bound inside a sum, and a local block index; notation and acronyms
standard for the venue ($\mathbb R$, $O(\cdot)$, softmax, log, SVD, LLM, GPU,
MLP).

## Procedure

1. Start every audit, a pasted excerpt included, by running `python3 <this
   skill's directory>/scripts/symbol_inventory.py MAIN.tex [--body-end LABEL]`
   (pasted text goes first into a file in a new `mktemp -d` directory). It
   follows `\input` and `\include` and names the files it read and any input it
   could not resolve; lists every math symbol, operator, and acronym with its
   first location and counts by region (abstract, body, post-body, appendix);
   flags symbols used once or only in the appendix; groups symbols that share a
   base letter; lists macros with arguments, which it does not expand; flags
   acronyms defined twice, used once, or used before their definition; and
   lists coined-name candidates (bold or italic names, CamelCase words) and
   every numbered row and display with its reference count, closing
   punctuation, and next word. `--show SYMBOL` prints every line that uses a
   symbol. A definition versus a use, one meaning versus two, and a float's
   position on the page are read from the source and the PDF.
2. For each symbol, acronym, and coined name in order of first use, find its
   definition site and apply rules 1–5. Arm names that appear only in table
   cells (Oracle) and symbols inside macros with arguments are added by
   reading the tables and the macro uses. Systems and tooling acronyms enter
   through hyperparameter tables and are the ones most often left undefined.
   For each base-letter family, read the `--show` lines and decide whether each
   letter keeps one meaning.
3. Grep the typography variants of rule 6; extract the text of every
   `\includegraphics` PDF with `pdftotext` for rule 7, and view as an image any
   figure whose extraction is empty (a raster, outlined text); read each
   display's closing punctuation and next word from the inventory for rule 8.

Done when every inventory row, acronym, and coined name has a verdict, pass or
candidate, and every figure has been extracted or viewed.

Edit nothing until the author picks candidates. Apply the picked ones through
oral-paragraph-audit Procedure steps 4–5 (step 5 rechecks each changed
sentence and its neighbours for cohesion), rebuild, rerun the inventory, and
end the report with step 5's `Recheck:` line.

## Output

```
| # | Location | Symbol | Rule | Problem | Proposed fix | Severity |
|---|---|---|---|---|---|---|
| 1 | main.tex:159 | ρ | defined before use | used in the Introduction, defined in §3.1 (L294) | define at first use; drop the §3.1 gloss | Major |
```

The table holds candidates only: places where a reader of the paper as written
misreads a symbol, looks elsewhere for its meaning, meets its definition a
second time, or carries one the paper does not need. Notation that reads
correctly where it stands passes, and so does any candidate you would call
optional. The Rule column gives the rule's bold name; a clean paper gives
`Candidates: 0`. Exempt symbols and passes go in one line under the table.

Severity on paper-presubmit-audit's scale: **Major** for an undefined symbol, a
collision in the body, a wrong variant, a redefinition with changed content, or
a relation symbol that misstates the claim; **Minor** for a restatement, an
unneeded entity, a typography inconsistency, or an unreferenced equation
number; **Blocking** only when notation leaves a headline result unreadable.
Then `Inventory: N symbols, M acronyms, C coined names`, `Coverage:` the files
read, any unresolved input, and whether the compiled PDF and every figure were
checked (a check that could not run is named here, and the candidate count
covers only what ran), and `Candidates: K (by rule: …)`.
