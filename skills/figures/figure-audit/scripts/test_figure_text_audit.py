#!/usr/bin/env python3
"""Regression test for figure_text_audit.py: builds LaTeX fixtures with known answers.

Needs pdflatex, matplotlib and PyMuPDF. Run: python3 test_figure_text_audit.py
Covers LaTeX scaling and mathtext scripts, body math kept out of figures, raster DPI (plain and
rotated), panels sharing a caption, captions above figures, graphics inside tables, trim/clip,
pdflscape pages, rotated pages with an offset CropBox, and an unnamed Form XObject.
"""

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import fitz
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

SCRIPT = Path(__file__).with_name("figure_text_audit.py")

PAPER_A = r"""\documentclass[twocolumn]{article}\usepackage{graphicx}
\usepackage[textwidth=6.75in,columnsep=0.25in]{geometry}
\begin{document}
Body text with math $x_i^2$ here.
\begin{figure*}[t]\centering\includegraphics[width=0.5\textwidth]{figA.pdf}\caption{First.}\end{figure*}
\begin{figure}[h]\centering\includegraphics[width=\columnwidth]{figB.pdf}\caption{Second.}\end{figure}
\begin{figure}[h]\centering\includegraphics[width=\columnwidth]{figC.png}\caption{Third.}\end{figure}
\end{document}
"""

PAPER_B = r"""\documentclass{article}\usepackage{graphicx}\usepackage{pdflscape}
\usepackage[textwidth=6in]{geometry}
\begin{document}
Body text $y_j^2$.
\begin{figure}[h]\centering\includegraphics[width=0.48\textwidth]{figD.pdf}\hfill
\includegraphics[width=0.48\textwidth]{figE.pdf}\caption{Shared caption.}\end{figure}
\begin{figure}[h]\centering\caption{Caption above.}\includegraphics[width=3in]{figF.pdf}\end{figure}
\begin{table}[h]\centering\caption{A table.}\begin{tabular}{c}\includegraphics[width=1.5in]{figG.pdf}
\end{tabular}\end{table}
\clearpage
\begin{figure}[h]\centering\includegraphics[trim=108 0 0 0,clip,width=2in]{figH.pdf}\caption{Clipped.}
\end{figure}
\begin{figure}[h]\centering\includegraphics[angle=90,width=2in]{figC.png}\caption{Rotated raster.}
\end{figure}
\clearpage
\begin{landscape}
\begin{figure}[h]\centering\includegraphics[width=4in]{figB.pdf}\caption{Landscape page.}\end{figure}
\end{landscape}
\clearpage
\pdfpageattr{/CropBox [36 36 576 756]}
\begin{figure}[h]\centering\includegraphics[width=3.25in]{figA.pdf}\caption{Cropped page.}\end{figure}
\end{document}
"""


def make_figures(root):
    plt.rcParams["pdf.fonttype"] = 42
    fig, ax = plt.subplots(figsize=(8, 4))  # 8 pt ticks, 10 pt labels, mathtext superscript
    ax.plot([0, 1], [0, 1])
    ax.set_xlabel("AlphaLabel", fontsize=10)
    ax.set_ylabel(r"$R^2$ score", fontsize=10)
    ax.tick_params(labelsize=8)
    fig.savefig(root / "figA.pdf")
    plt.close(fig)
    with plt.rc_context({"font.family": "serif"}):  # 1:1 canvas, 9 pt serif
        fig, ax = plt.subplots(figsize=(3.25, 2))
        ax.bar([0, 1], [1, 2])
        ax.set_xlabel("BetaLabel", fontsize=9)
        ax.tick_params(labelsize=9)
        fig.savefig(root / "figB.pdf")
        plt.close(fig)
    fig, ax = plt.subplots(figsize=(3, 2))  # 300 x 200 px raster
    ax.imshow(np.random.default_rng(0).random((10, 10)))
    fig.savefig(root / "figC.png", dpi=100)
    plt.close(fig)
    for name in "DEFGH":
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.plot([0, 1], [1, 0])
        ax.set_xlabel(f"fig{name}Label", fontsize=8)
        ax.tick_params(labelsize=8)
        fig.savefig(root / f"fig{name}.pdf")
        plt.close(fig)


def compile_tex(root, name, source):
    (root / f"{name}.tex").write_text(source)
    for _ in range(2):
        subprocess.run(["pdflatex", "-interaction=batchmode", f"{name}.tex"], cwd=root,
                       stdout=subprocess.DEVNULL, check=False)
    return root / f"{name}.pdf"


def audit(pdf):
    out = subprocess.run([sys.executable, str(SCRIPT), str(pdf), "--json"], capture_output=True, text=True,
                         check=True)
    return json.loads(out.stdout)


def close(actual, expected, tol):
    assert actual is not None and abs(actual - expected) < tol, (actual, expected)


def test_basic(root):
    pdf = compile_tex(root, "paper_a", PAPER_A)
    report = audit(pdf)
    assert report["pdf_sha256"] == hashlib.sha256(pdf.read_bytes()).hexdigest()
    figs = {(f["panels"][0]["file"] or "raster@" + f["caption"]): f for f in report["figures"]}
    assert set(figs) == {"figA.pdf", "figB.pdf", "raster@Figure 3"}, figs.keys()
    a, b, c = figs["figA.pdf"], figs["figB.pdf"], figs["raster@Figure 3"]
    assert a["caption"] == "Figure 1"
    close(a["panels"][0]["scale"], 0.4219, 0.002)
    assert {3.38, 4.22} <= {round(s["size"], 2) for s in a["sizes"]}
    close(a["min_size"], 2.95, 0.1)  # mathtext superscript, about 0.7 x 4.22 pt
    assert b["caption"] == "Figure 2" and b["families"] == ["DejaVuSerif"]
    close(b["panels"][0]["scale"], 1.0, 0.002)
    close(b["min_size"], 9.0, 0.05)
    assert c["kind"] == "raster"
    close(c["panels"][0]["rasters"][0]["effective_dpi"], 92.3, 1.0)
    assert all(t != "x" for f in report["figures"] for s in f["sizes"] for t in s["samples"]), "body math leaked"
    close(report["document"]["body_size"], 10.0, 0.1)


def test_attribution(root):
    pdf = compile_tex(root, "paper_b", PAPER_B)
    doc = fitz.open(pdf)

    def page_with(caption):  # float placement varies across TeX installations
        return next(p for p in doc if caption in p.get_text())

    page_with("Clipped.").set_rotation(90)  # clipped figure on a rotated page
    raster = page_with("Rotated raster.")
    raster.set_cropbox(fitz.Rect(36, 36, 576, 756))
    raster.set_rotation(90)  # rotated raster on a rotated, cropped page
    cropped = page_with("Cropped page.")
    cropped.set_rotation(90)
    cropped.set_cropbox(fitz.Rect(20, 60, 560, 740))  # asymmetric CropBox
    page = doc.new_page(width=612, height=792)
    page.show_pdf_page(fitz.Rect(144, 100, 378, 244), fitz.open(root / "figB.pdf"), 0)  # unnamed Form
    page.insert_text((144, 270), "Figure 7: Unnamed form.", fontsize=10, fontname="helv")
    doc.save(root / "paper_b_mod.pdf")
    by = {f["caption"]: f for f in audit(root / "paper_b_mod.pdf")["figures"]}
    expected = {"Figure 1", "Figure 2", "Table 1", "Figure 3", "Figure 4", "Figure 5", "Figure 6", "Figure 7"}
    assert set(by) == expected, sorted(map(str, by))
    assert sorted(p["file"] for p in by["Figure 1"]["panels"]) == ["figD.pdf", "figE.pdf"]
    close(by["Figure 1"]["min_size"], 7.68, 0.02)
    assert [p["file"] for p in by["Figure 2"]["panels"]] == ["figF.pdf"]
    assert [p["file"] for p in by["Table 1"]["panels"]] == ["figG.pdf"]
    close(by["Table 1"]["min_size"], 4.0, 0.02)
    clipped = by["Figure 3"]["panels"][0]
    close(clipped["scale"], 1.3333, 0.002)
    close(clipped["placed_in"][0], 2.0, 0.02)
    close(by["Figure 4"]["panels"][0]["rasters"][0]["effective_dpi"], 100.0, 1.0)
    landscape = by["Figure 5"]["panels"][0]
    close(landscape["scale"], 1.2308, 0.002)
    close(landscape["placed_in"][0], 4.0, 0.02)
    close(by["Figure 6"]["panels"][0]["scale"], 0.4062, 0.002)
    close(by["Figure 6"]["min_size"], 2.84, 0.05)
    assert by["Figure 7"]["panels"][0]["file"] is None
    close(by["Figure 7"]["min_size"], 9.0, 0.05)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        make_figures(root)
        test_basic(root)
        test_attribution(root)
    print("PASS")
