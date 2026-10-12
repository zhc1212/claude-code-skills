#!/usr/bin/env python3
"""Inventory of math symbols, operators, acronyms, coined names and displays in a LaTeX paper.

usage: symbol_inventory.py main.tex [--body-end LABEL] [--show SYMBOL ...]

\\input and \\include are followed; locations print as file:line once more than one
file is read. Regions: abs (abstract), body (to --body-end label, else the first of
\\section*{Limitations} / \\appendix), post (Limitations and other unnumbered back
matter), app (after \\appendix). Only text after \\begin{document} is inventoried;
verbatim, comment environments and \\iffalse blocks are skipped. The inventory lists
candidates; whether a line defines or uses a symbol is read from the source.
"""
import argparse, bisect, collections, os, re

ap = argparse.ArgumentParser()
ap.add_argument("tex")
ap.add_argument("--body-end", help="label on the last body line, e.g. body:end")
ap.add_argument("--show", nargs="*", default=[], help="print every line using these symbols")
args = ap.parse_args()


def strip_comment(line):
    # a % after an even number of backslashes starts a comment; % inside \url{...} is text
    prot = re.sub(r"\\(?:url|href)\{[^}]*\}", lambda m: m.group(0).replace("%", "\0"), line)
    prot = re.sub(r"(^|[^\\])((?:\\\\)*)%.*", r"\1\2", prot)
    return prot.replace("\0", "%")


# ---- load, following \input / \include; src[i] = (file, line, raw text) ----
src, unresolved, seen = [], [], set()


def load(path):
    seen.add(os.path.abspath(path))
    base = os.path.dirname(path)
    for n, raw in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
        m = re.search(r"\\(?:input|include)\{([^}]+)\}", strip_comment(raw))
        if m:
            p = os.path.join(base, m.group(1))
            p = p if os.path.isfile(p) else p + ".tex"
            if os.path.isfile(p) and os.path.abspath(p) not in seen:
                src.append((path, n, ""))
                load(p)
                continue
            if not os.path.isfile(p):
                unresolved.append(f"{os.path.basename(path)}:{n} {m.group(1)}")
        src.append((path, n, raw))


load(args.tex)
files = sorted({f for f, _, _ in src})


def loc(l):
    if not 1 <= l <= len(src):
        return "end"
    return str(src[l - 1][1]) if len(files) == 1 else f"{os.path.basename(src[l - 1][0])}:{src[l - 1][1]}"


text = "\n".join(strip_comment(r) for _, _, r in src)
blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))  # keeps offsets, so lineof() stays right


def group_at(s, i):
    """Return (content, end) of the balanced {...} group starting at s[i] == '{'."""
    depth = 0
    for j in range(i, len(s)):
        depth += {"{": 1, "}": -1}.get(s[j], 0)
        if depth == 0:
            return s[i + 1:j], j + 1
    return None, i


# ---- macros: expand short argument-free math macros; list macros with arguments ----
macros, param_macros = {}, {}
for m in re.finditer(r"\\(?:re|provide)?newcommand\*?\s*\{?\\([A-Za-z]+)\}?\s*(\[\d\])?\s*(?=\{)|\\def\\([A-Za-z]+)((?:#\d)*)\s*(?=\{)", text):
    name = m.group(1) or m.group(3)
    body, _ = group_at(text, m.end())
    if body is None:
        continue
    if m.group(2) or m.group(4):
        param_macros[name] = body.replace("\n", " ")
        continue
    body = body.replace("\n", " ")
    if len(body) < 60 and not re.search(r"[a-z]{4,}", re.sub(r"\\[A-Za-z]+", "", body)):
        macros[name] = body
for name, body in macros.items():
    text = re.sub(r"\\" + name + r"(?![A-Za-z])", lambda _: body, text)

# skip the preamble and non-rendered regions (offsets preserved)
doc = re.search(r"\\begin\{document\}", text)
if doc:
    text = blank(re.match(r"(?s).*", text[:doc.end()])) + text[doc.end():]
text = re.sub(r"(?s)\\begin\{(verbatim|lstlisting|comment|minted)\}.*?\\end\{\1\}|\\iffalse\b.*?\\fi\b", blank, text)

off = [0]
for l in text.split("\n"):
    off.append(off[-1] + len(l) + 1)
lineof = lambda i: bisect.bisect_right(off, i)


def first_line(pat):
    m = re.search(pat, text)
    return lineof(m.start()) if m else None


abs_start = first_line(r"\\begin\{abstract\}") or 1
abs_end = first_line(r"\\end\{abstract\}") or 0
app_start = first_line(r"\\appendix\b") or 10**9
post_start = first_line(r"\\section\*\{(Limitations|Ethics|Acknowledg)") or app_start
body_end = (first_line(r"\\label\{" + re.escape(args.body_end) + r"\}") if args.body_end else None) or post_start - 1


def region(l):
    if l < abs_start: return "pre"
    if l <= abs_end: return "abs"
    if l <= body_end: return "body"
    if l < app_start: return "post"
    return "app"


# $$...$$ only between whitespace, so two abutting inline formulas ($a$$b$) are not a display
DISPLAY = r"\\begin\{(equation|align|gather|multline|eqnarray|flalign)(\*?)\}(.+?)\\end\{\1\2\}|(?<!\S)\$\$(.+?)\$\$(?![^\s.,;:])|\\\[(.+?)\\\]"
spans = []
for m in re.finditer(DISPLAY + r"|(?<!\\)\$(.+?)(?<!\\)\$|\\\((.+?)\\\)", text, re.S):
    g = next(i for i in (3, 4, 5, 6, 7) if m.group(i) is not None)
    spans.append((m.start(g), m.group(g)))

GREEK = ("alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|iota|kappa|lambda|mu|nu|xi|pi|rho|"
         "sigma|tau|upsilon|phi|varphi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Phi|Psi|Omega|ell")
DECS = "tilde|check|hat|widehat|widetilde|bar|overline|underline|breve|vec|dot|ddot|mathbf|boldsymbol|bm|mathcal|mathbb|mathrm|mathsf|mathfrak|mathit|mathscr"
DEC = r"\\(?:" + DECS + r")\s*"
SUB = r"(?:_\{(?:[^{}]|\{[^{}]*\})*\}|_\\[A-Za-z]+|_[A-Za-z0-9])"
SUP = r"(?:\^\{\\text\{[^{}]*\}\}|\^\{\([^{}]*\)\}|\^\{?\*\}?|\^\{?\\star\}?)"
sym_re = re.compile(r"((?:" + DEC + r"\{?\s*)*)(\\(?:" + GREEK + r")(?![A-Za-z])|(?<![\\A-Za-z])[A-Za-z](?![A-Za-z]))\}?\s*(" + SUB + r")?(" + SUP + r")?")
op_re = re.compile(r"\\(?:text|operatorname|mathrm)\{([A-Za-z][A-Za-z-]{1,})\}")


def norm(d, base, sub, sup):
    d = re.sub(r"[\s{}]", "", d)
    clean = lambda s: re.sub(r"\\(?:text|mathrm)\{([^{}]*)\}", r"\1", s or "").replace(" ", "")
    return d + base + clean(sub) + clean(sup)


syms = collections.defaultdict(list)
ops = collections.defaultdict(list)
for at, b in spans:
    for m in op_re.finditer(b):
        start = m.start()
        if not re.search(r"[_^]\{?$", b[max(0, start - 2):start]):
            ops[m.group(1)].append(lineof(at + start))
    # drop word-like \text{...} outside sub/superscripts; keep them inside (B_{\text{target}})
    # and keep a single-letter \mathrm{I} as a symbol
    b2 = re.sub(r"\\(text|operatorname|mathrm|label|ref|eqref|textit|textbf|texttt|mbox)\{(?:[^{}]|\{[^{}]*\})*\}",
                lambda x: x.group(0) if b[max(0, x.start() - 2):x.start()] in ("_{", "^{")
                or (x.group(1) == "mathrm" and re.fullmatch(r"\\mathrm\{[A-Za-z]\}", x.group(0))) else blank(x), b)
    for m in sym_re.finditer(b2):
        syms[norm(m.group(1), m.group(2), m.group(3), m.group(4))].append(lineof(at + m.start(2)))


def row(name, ls):
    c = collections.Counter(region(l) for l in ls)
    flags = []
    if len(ls) <= 1: flags.append("once")
    if c["app"] and not (c["body"] or c["abs"]): flags.append("app-only")
    if c["abs"]: flags.append("in-abstract")
    return f"{loc(min(ls)):>6s}  {name:26s} abs{c['abs']:<3d} body{c['body']:<4d} post{c['post']:<3d} app{c['app']:<4d} {' '.join(flags)}"


print(f"# files read: {', '.join(os.path.basename(f) for f in files)}"
      + (f"; UNRESOLVED inputs (not inventoried): {', '.join(unresolved)}" if unresolved else ""))
print(f"# regions: abstract from line {loc(abs_start)}; body ends line {loc(body_end)}; post-body from "
      f"{loc(post_start) if post_start < 10**9 else 'none'}; appendix from {loc(app_start) if app_start < 10**9 else 'none'}")
print("\n## Symbols (first use, counts by region, flags)")
for k, v in sorted(syms.items(), key=lambda kv: min(kv[1])):
    print(row(k, v))
print("\n## Operators and text identifiers in math")
for k, v in sorted(ops.items(), key=lambda kv: min(kv[1])):
    print(row("op:" + k, v))
if param_macros:
    print("\n## Macros with arguments (not expanded; read their uses)")
    for name, body in param_macros.items():
        n = len(re.findall(r"\\" + name + r"(?![A-Za-z])", text))
        print(f"  \\{name} -> {body[:60]}  (uses {n})")

print("\n## Symbol families sharing a base letter (check meanings)")
fam = collections.defaultdict(set)
for k in syms:
    base = re.sub(r"^(?:\\(?:" + DECS + "))+", "", k)
    m = re.match(r"(\\[A-Za-z]+|[A-Za-z])", base)
    if m: fam[m.group(1)].add(k)
for b, ks in sorted(fam.items()):
    if len(ks) > 1:
        print(f"  {b}: {', '.join(sorted(ks))}")

# prose: math blanked, formatting wrappers opened up; keyless: math kept, keys blanked
prose = re.sub(DISPLAY + r"|(?<!\\)\$[^$]*(?<!\\)\$", blank, text, flags=re.S)
prose = re.sub(r"\\(?:textsc|textbf|emph|textit)\{([^{}]*)\}", lambda m: " " * (len(m.group(0)) - len(m.group(1)) - 1) + m.group(1) + " ", prose)
keyless = re.sub(r"\\(?:label|ref|eqref|cref|Cref|autoref|pageref|cite\w*|includegraphics|url|href)(?:\[[^]]*\])?\{[^}]*\}", blank, text)
keyless = re.sub(r"\\texttt\{[^}]*\}", blank, keyless)


def subseq(needle, hay):
    it = iter(hay)
    return all(ch in it for ch in needle)


def expands(acr, words):
    """acr's letters are a subsequence of 1-6 consecutive words that start with its first letter."""
    letters = re.sub(r"[^a-z]", "", acr.lower())
    for k in range(1, min(6, len(words)) + 1):
        cand = [w.lower() for w in words[-k:]]
        if cand[0][0] == letters[0] and subseq(letters, "".join(cand)):
            return True
    return False


print("\n## Acronyms defined in parentheses")
ACR = r"[A-Z][A-Za-z0-9-]*[A-Z0-9][A-Za-z0-9-]*"
defs = collections.defaultdict(list)  # acronym -> definition offsets
for m in re.finditer(r"\(\s*(" + ACR + r")\s*\)", prose):  # natural language processing (NLP)
    a = m.group(1)
    if 2 <= len(a) <= 8 and expands(a, re.findall(r"[A-Za-z]+", prose[max(0, m.start() - 90):m.start()])):
        defs[a].append(m.start(1))
for m in re.finditer(r"(?<![A-Za-z])(" + ACR + r")\s*\(([^()]{3,90})\)", prose):  # NLP (natural language processing)
    a, words = m.group(1), re.findall(r"[A-Za-z]+", m.group(2))
    if 2 <= len(a) <= 8 and words and expands(a, words) and m.start(1) not in defs[a]:
        defs[a].append(m.start(1))
for a, dl in sorted(defs.items(), key=lambda kv: min(kv[1])):
    dl.sort()
    uses = [x.start() for x in re.finditer(r"(?<![A-Za-z])" + re.escape(a) + r"(?![A-Za-z])", keyless)]
    before = sorted({lineof(u) for u in uses if u < dl[0]})
    flags = []
    if len(dl) > 1: flags.append(f"defined {len(dl)}x at {[loc(lineof(d)) for d in dl]}")
    if len(uses) - len(dl) <= 1: flags.append("used once")
    if before: flags.append(f"used before definition at {[loc(l) for l in before[:3]]}")
    print(f"{loc(lineof(dl[0])):>6s}  {a:10s} uses{len(uses):<4d} {'; '.join(flags)}")

print("\n## Uppercase runs never defined in parentheses (filter: LaTeX words, cited names, field-standard)")
firsts, runs = {}, collections.Counter()
for m in re.finditer(r"(?<![A-Za-z\\])([A-Z][A-Z0-9]{1,5})(?![A-Za-z])", keyless):
    runs[m.group(1)] += 1
    firsts.setdefault(m.group(1), lineof(m.start()))
print("  " + ", ".join(f"{a}({n}, L{loc(firsts[a])})" for a, n in runs.most_common() if a not in defs))

print("\n## Coined-name candidates (bold/italic names, CamelCase words; drop cited, tool and dataset names;"
      " arm names in table cells are read from the tables)")
fmt = {}
for m in re.finditer(r"\\(?:textbf|emph|textit|textsc)\{([A-Z][A-Za-z0-9-]*(?: [A-Z][A-Za-z0-9-]*){0,2})\}", text):
    fmt.setdefault(m.group(1), lineof(m.start()))
names = set(fmt) | set(re.findall(r"(?<![\\A-Za-z])([A-Z][a-z]+(?:[A-Z0-9][a-z0-9]*)+)(?![A-Za-z])", prose))
rows = []
for nm in names:
    ls = [lineof(x.start()) for x in re.finditer(r"(?<![\\A-Za-z])" + re.escape(nm) + r"(?![A-Za-z])", keyless)]
    if not ls: continue
    c = collections.Counter(region(l) for l in ls)
    flags = []
    if nm in fmt and ls[0] < fmt[nm]:
        flags.append(f"used before its first bold/italic occurrence at {[loc(l) for l in ls if l < fmt[nm]][:3]}")
    if len(ls) <= 1: flags.append("once")
    rows.append((ls[0], f"{loc(ls[0]):>6s}  {nm:16s} uses{len(ls):<4d} body{c['body']:<4d} app{c['app']:<4d} "
                        f"{'formatted at L' + loc(fmt[nm]) if nm in fmt else ''}  {'; '.join(flags)}"))
for _, r in sorted(rows):
    print(r)

print("\n## Displays (label, references, closing punctuation, next word)")
refs = collections.Counter()
for m in re.finditer(r"\\(?:eqref|ref|cref|Cref|autoref|crefrange|Crefrange|pageref)\{([^}]*)\}", text):
    for k in m.group(1).split(","):
        refs[k.strip()] += 1


def closing(body):
    t = body
    while True:
        t0 = t
        t = re.sub(r"(\\(?:label|tag)\{[^}]*\}|\\(?:quad|qquad|nonumber|notag)\b|\\[,;!: ]|\s)+$", "", t)
        t = re.sub(r"\\end\{(?:aligned|split|gathered|array|cases|[pbvBV]?matrix)\}$", "", t)
        t = re.sub(r"\\right\s*[.)\]|]$", "", t)
        if t == t0:
            break
    m = re.search(r"\\(?:text|mbox|textrm)\{\s*([,.;])\s*\}$", t)
    return m.group(1) if m else (t[-1] if t and t[-1] in ",.;" else "none")


for m in re.finditer(DISPLAY, text, re.S):
    env, star = m.group(1), m.group(2)
    body = next(g for g in (m.group(3), m.group(4), m.group(5)) if g is not None)
    numbered_env = env is not None and not star
    nxt = re.match(r"\s*([^\s]+)", text[m.end():])
    tail = f"ends {closing(body)!r:6s} next {nxt.group(1)[:20] if nxt else '-'}"
    rows_ = re.split(r"\\\\", body) if env in ("align", "gather", "eqnarray", "flalign") else [body]
    numbered = [r for r in rows_ if (numbered_env and not re.search(r"\\(?:nonumber|notag)\b", r) and r.strip())
                or re.search(r"\\tag\{", r)]
    if not numbered:
        print(f"{loc(lineof(m.start())):>6s}  {'(unnumbered)':24s} refs 0  {tail}")
        continue
    for i, r in enumerate(numbered):
        lab = re.search(r"\\label\{([^}]+)\}", r)
        n = refs[lab.group(1)] if lab else 0
        flag = "  <- numbered, never referenced" if n == 0 else ""
        name = lab.group(1) if lab else "(no label)"
        print(f"{loc(lineof(m.start())):>6s}  {('+ ' if i else '') + name:24s} refs {n}  {tail if i == len(numbered) - 1 else ''}{flag}")

for s in args.show:
    print(f"\n## Lines using {s}")
    for l in sorted(set(syms.get(s, []))):
        print(f"{loc(l):>6s} [{region(l)}] {src[l - 1][2].strip()[:150]}")
