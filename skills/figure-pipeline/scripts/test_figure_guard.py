#!/usr/bin/env python3
"""Regression test for figure_guard.py: known edits must land in the right category.

Needs matplotlib. Run: python3 test_figure_guard.py
A data edit (divisor, swapped series, interval bound) is DATA; a rounded value label is NUMERIC;
a legend move, a font change, open markers, a moved or resized diagram is STYLE only; a changed axis range is AXES; an inserted label is one TEXT change, not a re-keying of every later label; a filled
marker appended over a point its series already draws, or removed again, is STYLE, but one at a new point, or two unlabelled series
trading data, is DATA; a figure the edit does not touch stays byte-identical; an output the generator stops saving fails; the
generator's data file and source appear in reads.json, also when they sit above the working
directory and --root names the top, and across several generators captured into one directory.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).with_name("figure_guard.py")

GENERATOR = '''
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import json
import helper  # a local module: its source must appear in reads.json even when loaded from .pyc

DIVISOR, SWAP, CI, LOC, LABEL, BOX_X, YLIM, SIZE, CONTROL, FONT, NOTE, MFC, USWAP, OVERLAY = {params}
plt.rcParams["font.family"] = FONT
raw = json.load(open("data.json"))
names = ["Base", "Ours"] if SWAP else ["Ours", "Base"]
fig, (ax, bx) = plt.subplots(1, 2, figsize=(4, 2))
for name, key in zip(names, raw):
    ys = [v / DIVISOR for v in raw[key]]
    ax.plot(range(4), ys, label=name, marker="o", mfc=MFC)
pair = [[0.1, 0.2], [0.4, 0.3]]
for colour, ys in zip(["C2", "C3"], pair[::-1] if USWAP else pair):  # unlabelled series, keyed by index
    ax.plot([0, 3], ys, color=colour)
if OVERLAY:  # appended after the series, as a per-point fill is
    ax.plot([0], [OVERLAY], ls="", marker="o", color="C2")
ax.fill_between(range(4), [0.1, 0.2, 0.3, 0.4], [0.3, 0.4, 0.5, CI], alpha=0.2)
ax.legend(loc=LOC)
if YLIM:
    ax.set_ylim(*YLIM)
if NOTE:
    bx.text(0, 0.5, NOTE)  # inserted before the value labels, shifting their order
bars = bx.bar(["A", "B"], [0.873, 0.912])
for bar, v in zip(bars, [0.873, 0.912]):
    bx.text(bar.get_x() + bar.get_width() / 2, v, LABEL.format(v), ha="center")
fig.savefig("plot.pdf", metadata={{"CreationDate": None}})
fig2, dx = plt.subplots(figsize=SIZE)
dx.axis("off")
dx.text(BOX_X, 0.5, "Model", bbox=dict(boxstyle="round"))
dx.annotate("", xy=(0.9, 0.5), xytext=(BOX_X + 0.2, 0.5), arrowprops=dict(arrowstyle="->"))
fig2.savefig("diagram.pdf", metadata={{"CreationDate": None}})
if CONTROL:
    fig3, ex = plt.subplots(figsize=(2, 1))
    ex.plot([0, 1], [0, 1])
    fig3.savefig("control.pdf", metadata={{"CreationDate": None}})
'''

BASE = dict(divisor=100, swap=False, ci=0.6, loc="upper left", label="{:.3f}", box_x=0.2, ylim=None, size=(2, 1),
            control=True, font="sans-serif", note=None, mfc=None, uswap=False, overlay=None)


def capture(root, name, **changes):
    params = {**BASE, **changes}
    (root / "data.json").write_text(json.dumps({"Ours": [20, 35, 47, 56], "Base": [20, 30, 38, 44]}))
    if not (root / "helper.py").exists():  # written once, so later runs load it from __pycache__
        (root / "helper.py").write_text("SCALE = 1\n")
    order = ["divisor", "swap", "ci", "loc", "label", "box_x", "ylim", "size", "control", "font", "note", "mfc",
             "uswap", "overlay"]
    (root / "make.py").write_text(GENERATOR.format(params=", ".join(repr(params[k]) for k in order)))
    out = root / name
    subprocess.run([sys.executable, str(GUARD), "capture", str(out), "--", "make.py"], cwd=root, check=True,
                   stdout=subprocess.DEVNULL)
    return out


def compare(before, after):
    run = subprocess.run([sys.executable, str(GUARD), "compare", str(before), str(after), "--json"],
                         capture_output=True, text=True)
    return run.returncode, {f["file"]: f for f in json.loads(run.stdout)}


def categories(report, file):
    return {c for c in ("DATA", "NUMERIC", "TEXT", "AXES", "STYLE") if report[file][c]}


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        base = capture(root, "base")
        again = capture(root, "again")
        code, rep = compare(base, again)
        assert code == 0 and all(f["bytes_identical"] for f in rep.values()), rep
        assert all(f["reproduced"] for f in rep.values()), "unmodified generator did not reproduce bytes"

        for capture_dir in (base, again):  # the second run imports helper from __pycache__
            assert set(json.loads((capture_dir / "reads.json").read_text())) == {"make.py", "data.json", "helper.py"}

        # name: (change, categories that must appear, categories that must not, exit status)
        cases = {
            "divisor": (dict(divisor=10), {"DATA"}, set(), 1),
            "swap": (dict(swap=True), {"DATA"}, set(), 1),
            "unlabelled swap": (dict(uswap=True), {"DATA"}, set(), 1),
            "new point": (dict(overlay=0.15), {"DATA"}, set(), 1),
            "ci": (dict(ci=0.9), {"DATA"}, set(), 1),
            "rounded": (dict(label="{:.2f}"), {"NUMERIC", "TEXT"}, {"DATA"}, 1),
            "legend": (dict(loc="lower right"), {"STYLE"}, {"DATA", "NUMERIC", "TEXT", "AXES"}, 0),
            "ylim": (dict(ylim=(0, 1)), {"AXES"}, {"DATA", "NUMERIC", "TEXT"}, 0),
        }
        code, rep = compare(base, capture(root, "note", note="independent measures"))
        assert rep["plot.pdf"]["TEXT"] == ["ax1.text[independent measures]"] and code == 0, rep["plot.pdf"]["TEXT"]
        code, rep = compare(base, capture(root, "open-markers", mfc="white"))
        assert categories(rep, "plot.pdf") == {"STYLE"} and code == 0, rep["plot.pdf"]
        code, rep = compare(base, over := capture(root, "overplot", overlay=0.1))
        assert categories(rep, "plot.pdf") == {"STYLE"} and code == 0, rep["plot.pdf"]
        code, rep = compare(over, base)  # the same overlay removed
        assert categories(rep, "plot.pdf") == {"STYLE"} and code == 0, rep["plot.pdf"]
        code, rep = compare(base, capture(root, "font", font="serif"))
        assert categories(rep, "plot.pdf") == {"STYLE"} and code == 0, rep["plot.pdf"]
        for name, (change, present, absent, exit_code) in cases.items():
            code, rep = compare(base, capture(root, name, **change))
            found = categories(rep, "plot.pdf")
            assert present <= found and not absent & found, (name, found)
            assert code == exit_code, (name, code)
            assert rep["control.pdf"]["bytes_identical"] and rep["diagram.pdf"]["bytes_identical"], name
        for name, change in {"box": dict(box_x=0.3), "resize": dict(size=(2.5, 1))}.items():
            code, rep = compare(base, capture(root, name, **change))
            assert categories(rep, "diagram.pdf") == {"STYLE"} and code == 0, (name, rep["diagram.pdf"])
            assert rep["plot.pdf"]["bytes_identical"], name
        code, rep = compare(base, capture(root, "omitted", control=False))
        assert rep["control.pdf"]["only_in"] == "before" and code == 1, rep["control.pdf"]

        sub = root / "paper"  # a generator run from a subdirectory that reads ../data.json
        sub.mkdir()
        (sub / "make.py").write_text('import json\nimport matplotlib.pyplot as plt\njson.load(open("../data.json"))\n'
                                     'plt.figure().savefig("sub.pdf")\n')
        subprocess.run([sys.executable, str(GUARD), "capture", str(root / "sub"), "--root", "..", "--", "make.py"],
                       cwd=sub, check=True, stdout=subprocess.DEVNULL)
        assert set(json.loads((root / "sub" / "reads.json").read_text())) == {"paper/make.py", "data.json"}
        assert (root / "sub" / "paper__sub.pdf.json").exists()
        (root / "other.py").write_text('import matplotlib.pyplot as plt\nplt.figure().savefig("other.pdf")\n')
        subprocess.run([sys.executable, str(GUARD), "capture", str(root / "sub"), "--", "other.py"], cwd=root,
                       check=True, stdout=subprocess.DEVNULL)  # a second generator into the same capture
        assert set(json.loads((root / "sub" / "reads.json").read_text())) == {"paper/make.py", "data.json", "other.py"}
    print("PASS")


if __name__ == "__main__":
    main()
