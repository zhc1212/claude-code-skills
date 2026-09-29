#!/usr/bin/env python3
"""Mechanical counts for deai-latex steps 1, 5 and 6. Standard library only.

  audit_style.py count PASSAGE [--baseline FILE]
  audit_style.py compare SOURCE REWRITE [--earlier FILE] [--baseline FILE]

Input is LaTeX or plain text. A count is a candidate, not a finding: the colon and semicolon
classes are heuristics, so every match is printed in context for the reader to judge.
"""
import argparse, math, re, sys
from collections import Counter

BR = r"\{((?:[^{}]|\{[^{}]*\})*)\}"  # a brace group, one level of nesting
DISPLAY = (r"equation|align|alignat|gather|multline|eqnarray|displaymath|math|figure|table|tabular"
           r"|algorithm|algorithmic|lstlisting|verbatim|minted|tikzpicture")
DROP_ARG = r"cite[a-zA-Z]*|ref|eqref|autoref|cref|Cref|label|url|vspace|hspace|includegraphics|input|include|textcolor|color"
HEADING = r"part|chapter|section|subsection|subsubsection|paragraph|subparagraph"
BREAK, LIST, DOT = "\x00", "\x01", "\x02"
ABBREV = r"\b(e\.g|i\.e|et al|cf|vs|Fig|Figs|Eq|Eqs|Sec|Tab|resp|approx|No)\."
INIT_CONN = r"(however|moreover|furthermore|additionally|therefore|thus|hence|consequently|instead|together|finally|in contrast|as a result)\b"
MID_CONN = r"\b(therefore|thus|hence|consequently|however|moreover|furthermore|additionally)\b"
LABEL_BEFORE = r"(RQ\d+\s*(\([^)]*\))?|Stage \d+|following|consists of|contributions|as follows)\s*$"
FEATURES = ["em dash", "elab colon", "semicolon (clause)", "tail", "conn initial", "conn mid (step 6)"]
STOP = set("""a an the and or but nor if then than that this these those it its we our us they their them he she his her
i you your of in on at by for from to with without into onto over under between among within across about as per via
is are was were be been being has have had do does did can could may might must shall should will would not no so
such which who whom whose what when where while whereas because since although though also only both each every either
neither other another any all some more most less least very much many few one two three sym""".split())

def _is_latex(t):
    return re.search(r"\\[a-zA-Z]+", t) is not None  # in plain text, % is a percent sign

def _mask_math(t):
    if _is_latex(t):
        t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\begin\{(%s)\*?\}.*?\\end\{\1\*?\}" % DISPLAY, BREAK, t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]", BREAK, t, flags=re.S)
    return re.sub(r"(?<!\\)\$[^$]*\$|\\\(.*?\\\)", "SYM", t, flags=re.S)

def prose(text):
    """Prose with comments, math, keys and commands masked; BREAK marks a hard sentence boundary."""
    t = _mask_math(text)
    t = re.sub(r"\\(%s)\*?(\[[^\]]*\])*%s" % (DROP_ARG, BR), "", t)
    t = re.sub(r"\\(%s)\*?(\[[^\]]*\])?%s" % (HEADING, BR), BREAK, t)
    t = re.sub(r"\\(textbf|textit|emph)%s" % BR, lambda m: BREAK if m.group(2).strip().endswith((".", ":")) else m.group(0), t)
    t = re.sub(r"\\begin\{(itemize|enumerate|description)\}", LIST, t)
    t = re.sub(r"\\item\b(\[[^\]]*\])?", BREAK, t)
    t = re.sub(r"\\(begin|end)\{[^}]*\}", BREAK, t)
    t = re.sub(r"\n[ \t]*\n", BREAK, t)
    t = re.sub(r"\\([%&#_$])", r"\1", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
    t = t.replace("~", " ").replace("{", "").replace("}", "")
    return re.sub(r"[ \t\r\n]+", " ", t)

def sentences(p):
    """Sentences of the masked prose; chunks under three words (headings, fragments) are dropped."""
    p = re.sub(ABBREV, lambda m: m.group(0)[:-1].replace(".", DOT) + DOT, p)
    out = []
    for chunk in p.split(BREAK):
        for s in re.split(r"(?<=[.!?])\s+", chunk):
            s = s.replace(DOT, ".").strip()
            if len(s.replace(LIST, " ").split()) >= 3:
                out.append(s)
    return out

def _comma_list(after):
    """True when the text after a colon is a list whose items contain commas and are separated by semicolons."""
    items = after.split(";")
    return len(items) > 1 and all("," in item for item in items[:-1])

def _colon_is_elaborating(s, i):
    before, after = s[:i], s[i + 1:]
    if re.search(r"\d$", before) and re.match(r"\d", after):
        return False                                     # a ratio or a time
    if len(before.split()) <= 3 or re.search(LABEL_BEFORE, before[-40:]):
        return False                                     # a label such as "Stage 1:"
    if not after.strip() or re.match(r"\s*(%s|\((1|i|a)\))" % LIST, after) or _comma_list(after):
        return False                                     # introduces a list or a display
    return True

def features(text):
    p = prose(text)
    sents = sentences(p)
    hits = []
    for s in sents:
        clean = s.replace(LIST, " ")
        hits += [("em dash", clean, m.start()) for m in re.finditer(r"---|\u2014", clean)]
        hits += [("elab colon", clean, m.start()) for m in re.finditer(":", clean) if _colon_is_elaborating(clean, m.start())]
        for m in re.finditer(";", clean):
            colon = clean.rfind(":", 0, m.start())
            listy = (colon >= 0 and _comma_list(clean[colon + 1:])) or re.match(r"\s*(and |or )?\((\d+|[ivx]+|[a-z])\)", clean[m.end():])
            if not listy:
                hits.append(("semicolon (clause)", clean, m.start()))
        hits += [("tail", clean, m.start()) for m in re.finditer(r", (so|which|rather than)\b", clean)]
        if re.match(INIT_CONN, clean.lstrip("`'\"( "), re.I) and not re.match(r"(instead of|together with)\b", clean.lstrip("`'\"( "), re.I):
            hits.append(("conn initial", clean, 0))
        first = re.match(r"\S+", clean)
        hits += [("conn mid (step 6)", clean, m.start()) for m in re.finditer(MID_CONN, clean) if m.start() >= first.end()]
    return {"words": len(re.findall(r"[A-Za-z][A-Za-z\-']*", p)), "sentences": len(sents),
            "short": sum(1 for s in sents if len(s.replace(LIST, " ").split()) < 16),
            "counts": {k: sum(1 for h in hits if h[0] == k) for k in FEATURES}, "hits": hits}

def allowance(base_count, base_words, words):
    return math.ceil(base_count / base_words * words - 1e-9) if base_words else 0

def protected(text):
    """Multiset of spans a rewrite must keep: math, citation and reference keys, prose numbers, comments."""
    spans = Counter()
    t = text
    if _is_latex(text):
        spans.update(("comment", c.strip()) for c in re.findall(r"(?<!\\)%(.*)", text) if c.strip())
        t = re.sub(r"(?<!\\)%.*", "", text)
    for m in re.finditer(r"\\begin\{(%s)\*?\}(.*?)\\end\{\1\*?\}|\$\$(.*?)\$\$|\\\[(.*?)\\\]|(?<!\\)\$([^$]*)\$|\\\((.*?)\\\)" % DISPLAY, t, re.S):
        body = next(g for g in m.groups()[1:] if g is not None)
        spans[("math", " ".join(body.split()))] += 1
    for kind, keys in re.findall(r"\\(cite[a-zA-Z]*|ref|eqref|autoref|cref|Cref|label)\*?(?:\[[^\]]*\])*\{([^}]*)\}", t):
        group = "cite" if kind.startswith("cite") else "label" if kind == "label" else "ref"
        spans.update((group, k.strip()) for k in keys.split(",") if k.strip())
    spans.update(("number", n) for n in re.findall(r"(?<![A-Za-z\d.])\d+(?:\.\d+)?", prose(text)))
    return spans

def protected_diff(src, rw):
    return sorted((k, v, src[(k, v)], rw[(k, v)]) for (k, v) in set(src) | set(rw) if src[(k, v)] != rw[(k, v)])

def stem(w):
    for suf in ("ations", "ation", "ings", "ing", "ency", "ence", "ies", "ied", "ness", "ments", "ment", "ent", "ly", "ed", "es", "d", "s", "e"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w

def _content(text):
    return [w for w in re.findall(r"[a-z][a-z\-']*", prose(text).lower()) if len(w) >= 3 and w not in STOP]

def new_words(source, rewrite, earlier=""):
    """Content words of the rewrite whose stem appears in neither the source nor the earlier version."""
    known = {stem(w) for w in _content(source) + _content(earlier)}
    out, seen = [], set()
    for s in sentences(prose(rewrite)):
        for w in _content(s):
            if stem(w) not in known and w not in seen:
                seen.add(w)
                out.append((w, s))
    return out

def _snip(s, i, width=70):
    return ("…" if i > width else "") + s[max(0, i - width): i] + "⟦" + s[i:i + 1] + "⟧" + s[i + 1: i + width] + ("…" if i + width < len(s) else "")

def _read(path):
    return sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()

def _summary(name, f):
    share = f["short"] / f["sentences"] if f["sentences"] else 0
    return f"{name}: {f['words']} prose words, {f['sentences']} sentences, under 16 words {f['short']}/{f['sentences']} = {share:.0%}"

def cmd_count(a):
    f = features(_read(a.passage))
    print(_summary(a.passage, f))
    if a.baseline:
        b = features(_read(a.baseline))
        print(_summary("baseline " + a.baseline, b))
        print(f"\n{'feature':20} {'baseline /1k':>12} {'passage':>8} {'/1k':>6} {'allowance':>10}")
        for k in FEATURES:
            n, allow = f["counts"][k], allowance(b["counts"][k], b["words"], f["words"])
            flag = "  candidate" if n >= 2 and n > allow and k != "conn mid (step 6)" else ""
            print(f"{k:20} {1000 * b['counts'][k] / max(b['words'], 1):12.1f} {n:8} {1000 * n / max(f['words'], 1):6.1f} {allow:10}{flag}")
        if f["sentences"] >= 10 and b["sentences"] and f["short"] / f["sentences"] < b["short"] / b["sentences"] / 2:
            print("short-sentence share is below half the baseline share (a candidate only beside another finding)")
    else:
        print("\nno baseline: counted features are off; catalogue phrases are the only candidates")
        for k in FEATURES:
            print(f"{k:20} {f['counts'][k]:8}")
    if f["hits"]:
        print("\nmatches (read each before trusting the count):")
        for k, s, i in f["hits"]:
            print(f"  [{k}] {_snip(s, i)}")

def cmd_compare(a):
    src, rw = _read(a.source), _read(a.rewrite)
    fs, fr = features(src), features(rw)
    b = features(_read(a.baseline)) if a.baseline else None
    print(_summary("source", fs)); print(_summary("rewrite", fr))
    print(f"\n{'feature':20} {'source':>7} {'rewrite':>8}" + (f" {'allowance':>10}" if b else ""))
    for k in FEATURES:
        rise = "  rose" if fr["counts"][k] > fs["counts"][k] else ""
        allow = f" {allowance(b['counts'][k], b['words'], fr['words']):10}" if b else ""
        print(f"{k:20} {fs['counts'][k]:7} {fr['counts'][k]:8}{allow}{rise}")
    diff = protected_diff(protected(src), protected(rw))
    print("\nprotected spans that differ (restore each):" if diff else "\nprotected spans: identical")
    for k, v, ns, nr in diff:
        print(f"  {k} {v!r}: source {ns}, rewrite {nr}")
    words = new_words(src, rw, _read(a.earlier) if a.earlier else "")
    print("\ncontent words absent from the source (repair, a finding's plain word, or an addition):" if words else "\nnew content words: none")
    for w, s in words:
        print(f"  {w}: {s[:150]}")

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("count"); c.add_argument("passage"); c.add_argument("--baseline")
    c.set_defaults(run=cmd_count)
    d = sub.add_parser("compare"); d.add_argument("source"); d.add_argument("rewrite")
    d.add_argument("--earlier"); d.add_argument("--baseline"); d.set_defaults(run=cmd_compare)
    a = ap.parse_args(argv)
    a.run(a)

if __name__ == "__main__":
    main()
