"""List hidden or machine-directed text in PDFs (Check 2).

Usage: python3 hidden_text.py paper.pdf [supplement.pdf ...]   (needs PyMuPDF)
Prints one line per suspicious text run; no output means nothing was found.
"""
import re
import sys

import fitz  # PyMuPDF

INSTRUCTION = re.compile(
    r"ignore (all |any )?(previous|prior|above) instructions|positive review"
    r"|as an? (ai|llm|language model)|do not (highlight|mention) (any )?(negative|weakness)"
    r"|recommend accept",
    re.I,
)


def is_white(color):
    if len(color) == 4:  # CMYK
        return all(c == 0 for c in color)
    return all(c == 1 for c in color)  # gray or RGB


for path in sys.argv[1:]:
    doc = fitz.open(path)
    for pno, page in enumerate(doc, 1):
        area = page.rect
        for tr in page.get_texttrace():
            text = "".join(chr(c[0]) for c in tr["chars"]).strip()
            if not text:
                continue
            x0, y0, x1, y1 = tr["bbox"]
            why = []
            if tr["type"] == 3:
                why.append("invisible render mode")
            if tr["opacity"] == 0:
                why.append("opacity 0")
            if tr["size"] < 2:
                why.append(f"{tr['size']:.2f}pt")
            if is_white(tr["color"]):
                why.append("white fill")
            if x1 <= area.x0 or x0 >= area.x1 or y1 <= area.y0 or y0 >= area.y1:
                why.append("off-page")
            if why:
                print(f"{path} p{pno} [{', '.join(why)}] {text[:70]!r}")
        for m in INSTRUCTION.finditer(page.get_text()):
            print(f"{path} p{pno} [instruction-like] {m.group(0)!r}")
