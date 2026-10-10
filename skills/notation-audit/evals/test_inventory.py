#!/usr/bin/env python3
"""Deterministic regressions for scripts/symbol_inventory.py (no model calls).

Each case writes a tiny LaTeX file into a temp dir, runs the inventory, and checks
that every expected substring appears and every forbidden one does not.
"""
import os, re, subprocess, sys, tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "symbol_inventory.py")
DOC = "\\documentclass{article}\n\\begin{document}\n%s\n\\end{document}\n"

CASES = [
    ("include is followed, location is file:line",
     {"main.tex": DOC % "Intro.\n\\input{sec}", "sec.tex": "We set $\\alpha = 1$.\n"},
     [r"sec\.tex:1\s+\\alpha"], []),
    ("unresolved include is reported",
     {"main.tex": DOC % "\\input{missing}"}, ["UNRESOLVED inputs"], []),
    ("multiline macro keeps line numbers; --show does not crash",
     {"main.tex": "\\newcommand{\\foo}{\nx\n}\n\\begin{document}\n$\\foo$.\n$\\foo$.\n\\end{document}\n"},
     [r"^\s+5\s+x\s", r"Lines using x\n\s+5 \["], [], ["--show", "x"]),
    ("Greek macro expands; macro with arguments is listed",
     {"main.tex": "\\newcommand{\\sig}{\\sigma}\n\\newcommand{\\loss}[1]{\\mathcal{L}(#1)}\n" + DOC % "$\\sig$ and $\\loss{\\theta}$."},
     [r"\\sigma\s", r"\\loss -> "], []),
    ("align: every numbered row, \\cref counts, \\notag skipped",
     {"main.tex": DOC % "\\begin{align}\na &= b \\label{eq:a}\\\\\nc &= d \\label{eq:b}\\\\\ne &= f \\notag\n\\end{align}\nSee \\cref{eq:a}."},
     [r"eq:a\s+refs 1", r"\+ eq:b\s+refs 0.*never referenced"], [r"\(no label\)"]),
    ("$$ display listed; \\text{.} counts as punctuation; comma inside aligned",
     {"main.tex": DOC % "We have\n$$p=q$$\nthen\n\\[ x=y\\text{.} \\]\nand\n\\begin{equation}\n\\begin{aligned}\nu &= v,\n\\end{aligned}\n\\label{eq:u}\n\\end{equation}\nwhere $u$ is. Eq.~\\ref{eq:u}."},
     [r"\(unnumbered\)\s+refs 0\s+ends 'none' next then", r"ends '\.'\s+next and", r"eq:u\s+refs 1\s+ends ','"], []),
    ("% inside \\url is text; \\\\% starts a comment",
     {"main.tex": DOC % "\\url{https://example.org/a%20b} then $z$ and TPU.\n$u$ \\\\% comment $v$"},
     [r"\bz\s", r"TPU\("], [r"^\s+\d+\s+v\s"]),
    ("acronym: offset order, false parenthetical, reversed form",
     {"main.tex": DOC % "NLP appears first; natural language processing (NLP) is now defined.\nWe compare methods (NLP) and use NLP again.\nWe use GPT2 rarely. RL (reinforcement learning) helps; RL again."},
     [r"NLP\s+uses\d+\s+used before definition", r"RL\s+uses"], [r"NLP.*defined 2x"]),
    ("coined names: \\textit and multiword",
     {"main.tex": DOC % "We compare \\textit{Static} and \\emph{Type Mean}. Static wins over Type Mean."},
     [r"Static\s+uses2", r"Type Mean\s+uses2"], []),
    ("abutting inline formulas are not a $$ display",
     {"main.tex": DOC % "Rates $30\\times$, $1000$\\times$${}^*$ and $q$."},
     [r"\bq\s"], [r"\(unnumbered\)"]),
    ("preamble and verbatim are not inventoried; star superscript kept",
     {"main.tex": "\\newcommand{\\zz}{\\omega}\n\\begin{document}\n\\begin{verbatim}\n$q$\n\\end{verbatim}\n$x^{*}$ and $\\widetilde{y}$ and $\\mathrm{I}$.\n\\end{document}\n"},
     [r"x\^\{\*\}|x\^\*", r"\\widetildey", r"\\mathrmI"], [r"^\s+\d+\s+q\s", r"\\omega"]),
]


def run(files, extra):
    d = tempfile.mkdtemp()
    for name, body in files.items():
        with open(os.path.join(d, name), "w") as f:
            f.write(body)
    r = subprocess.run([sys.executable, SCRIPT, os.path.join(d, "main.tex")] + extra,
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


fails = 0
for case in CASES:
    name, files, must, mustnot = case[:4]
    extra = case[4] if len(case) > 4 else []
    code, out = run(files, extra)
    bad = [p for p in must if not re.search(p, out, re.M)] + [f"NOT {p}" for p in mustnot if re.search(p, out, re.M)]
    if code or bad:
        fails += 1
        print(f"FAIL {name}: exit={code} {bad}\n{out}")
    else:
        print(f"PASS {name}")
print(f"{len(CASES) - fails}/{len(CASES)} inventory regressions pass")
sys.exit(1 if fails else 0)
