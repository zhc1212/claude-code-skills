#!/usr/bin/env python3
"""Measure the text of every figure as it renders in a compiled paper PDF.

Reports, per figure (panels sharing one caption are grouped): page, caption, source files,
LaTeX scale, visible placed size, rendered text sizes and font families, and effective raster
DPI; then figure-set consistency against the body and caption sizes.

Sizes come from PyMuPDF on the final PDF, so every transform is applied: the
\\includegraphics scale, nested Form XObject matrices, and mathtext sub/superscripts.
Figures are located by Form XObject placement, clipped to ancestor Form BBoxes and rectangular
clip paths (this is how pdfTeX realises trim/clip). pdfTeX and LuaTeX record each source path
in /PTEX.FileName; a top-level Form without one (XeTeX, PyMuPDF) is reported unnamed. Inline
TikZ/pgfplots draws straight into the page, so its text cannot be attributed: such figures
appear under "captions without an included graphic" and in the "outside figures" line.

Usage: figure_text_audit.py main.pdf [--floor 7] [--json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    sys.exit("PyMuPDF is required: python3 -m pip install pymupdf")

IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
WHITESPACE = set(b" \t\r\n\f\x00")
DELIMITERS = set(b"()<>[]{}/%")
NUMBER = re.compile(rb"[-+]?(?:\d+\.?\d*|\.\d+)$")
CAPTION = re.compile(r"^\s*(Figure|Fig\.|Table)\s*(\d+)\s*[:.|]")
REFERENCE = re.compile(r"/([^\s/<>\[\]()]+)\s+(\d+)\s+0\s+R")
STYLE_SUFFIX = re.compile(r"[-,](Bold|Italic|Oblique|Regular|Roman|Medium|Light|Semibold|Book|Black|"
                          r"Regu|Medi|Ital|Demi)\w*$", re.I)
MATH_FONT = re.compile(r"^(STIX|CM(MI|SY|EX|R)\d|MSBM|MSAM|Symbol|DejaVuSans-Math|cmmi|cmsy|cmr)", re.I)
PAINT = {b"n", b"f", b"F", b"f*", b"S", b"s", b"B", b"B*", b"b", b"b*"}
PATH = {b"m", b"l", b"c", b"v", b"y", b"h"}
CAPTION_REACH = 100.0  # pt; a caption farther than this from a graphic is not its caption


def multiply(m, n):
    """PDF row-vector product m x n of [a b c d e f] matrices."""
    a, b, c, d, e, f = m
    A, B, C, D, E, F = n
    return (a * A + b * C, a * B + b * D, c * A + d * C, c * B + d * D,
            e * A + f * C + E, e * B + f * D + F)


def invert(m):
    a, b, c, d, e, f = m
    det = a * d - b * c
    return (d / det, -b / det, -c / det, a / det, (c * f - d * e) / det, (b * e - a * f) / det)


def transform(rect, m):
    """Bounding box of rect (x0, y0, x1, y1) under matrix m."""
    a, b, c, d, e, f = m
    xs, ys = [], []
    for x in (rect[0], rect[2]):
        for y in (rect[1], rect[3]):
            xs.append(x * a + y * c + e)
            ys.append(x * b + y * d + f)
    return (min(xs), min(ys), max(xs), max(ys))


def intersect(r, s):
    if r is None or s is None:
        return r or s
    out = (max(r[0], s[0]), max(r[1], s[1]), min(r[2], s[2]), min(r[3], s[3]))
    return out if out[0] < out[2] and out[1] < out[3] else (out[0], out[1], out[0], out[1])


def lex(data: bytes):
    """Yield ('num', float) | ('name', str) | ('op', bytes); skip strings, comments, inline images."""
    i, n = 0, len(data)
    while i < n:
        ch = data[i]
        if ch in WHITESPACE:
            i += 1
        elif ch == 0x25:  # % comment
            while i < n and data[i] not in (0x0A, 0x0D):
                i += 1
        elif ch == 0x28:  # ( literal string, balanced with escapes
            depth, i = 1, i + 1
            while i < n and depth:
                if data[i] == 0x5C:
                    i += 2
                    continue
                depth += {0x28: 1, 0x29: -1}.get(data[i], 0)
                i += 1
        elif ch == 0x3C:  # << or <hex>
            if data[i + 1:i + 2] == b"<":
                i += 2
            else:
                j = data.find(b">", i)
                i = n if j < 0 else j + 1
        elif ch == 0x3E:  # >>
            i += 2
        elif ch in b"[]{}":
            i += 1
        elif ch == 0x2F:  # /Name
            j = i + 1
            while j < n and data[j] not in WHITESPACE and data[j] not in DELIMITERS:
                j += 1
            yield "name", data[i + 1:j].decode("latin-1")
            i = j
        else:
            j = i
            while j < n and data[j] not in WHITESPACE and data[j] not in DELIMITERS:
                j += 1
            token, i = data[i:j], max(j, i + 1)
            if NUMBER.match(token):
                yield "num", float(token)
            elif token == b"ID":  # inline image data runs to a whitespace-delimited EI
                match = re.compile(rb"\sEI(?=\s|$)").search(data, i)
                i = n if match is None else match.end()
            else:
                yield "op", token


def numbers(text):
    return tuple(float(v) for v in re.findall(r"[-+]?(?:\d+\.?\d*|\.\d+)", text))


def xobject_names(doc, xref):
    """Map resource name -> xref for a Form XObject's /Resources /XObject dict."""
    kind, value = doc.xref_get_key(xref, "Resources/XObject")
    if kind == "xref":
        value = doc.xref_object(int(value.split()[0]))
    elif kind != "dict":
        return {}
    return {name: int(ref) for name, ref in REFERENCE.findall(value)}


def find_forms(doc, content, names, ctm, clip, depth, parent, found):
    """Record each Form XObject invocation with its matrix and visible region (PDF space)."""
    stack, operands, rects, curved, clipping = [], [], [], False, False
    for kind, value in lex(content):
        if kind != "op":
            operands.append(value)
            continue
        if value == b"q":
            stack.append((ctm, clip))
        elif value == b"Q":
            ctm, clip = stack.pop() if stack else (ctm, clip)
        elif value == b"cm" and len(operands) >= 6 and all(isinstance(v, float) for v in operands[-6:]):
            ctm = multiply(tuple(operands[-6:]), ctm)
        elif value == b"re" and len(operands) >= 4:
            x, y, w, h = operands[-4:]
            rects.append(transform((x, y, x + w, y + h), ctm))
        elif value in PATH:
            curved = True
        elif value in (b"W", b"W*"):
            clipping = True
        elif value in PAINT:
            if clipping and rects and not curved:  # curved clip paths are not modelled
                box = (min(r[0] for r in rects), min(r[1] for r in rects),
                       max(r[2] for r in rects), max(r[3] for r in rects))
                clip = intersect(clip, box)
            rects, curved, clipping = [], False, False
        elif value == b"Do" and operands and isinstance(operands[-1], str) and operands[-1] in names:
            xref = names[operands[-1]]
            if doc.xref_get_key(xref, "Subtype")[1] == "/Form" and depth < 8:
                kind_m, matrix = doc.xref_get_key(xref, "Matrix")
                total = multiply(numbers(matrix) if kind_m == "array" else IDENTITY, ctm)
                bbox = numbers(doc.xref_get_key(xref, "BBox")[1])
                visible = intersect(clip, transform(bbox, total))
                kind_f, filename = doc.xref_get_key(xref, "PTEX.FileName")
                found.append({"matrix": total, "bbox": bbox, "visible": visible, "depth": depth,
                              "parent": parent, "file": filename if kind_f == "string" else None})
                find_forms(doc, doc.xref_stream(xref) or b"", xobject_names(doc, xref), total, visible,
                           depth + 1, len(found) - 1, found)
        operands = []


def crop_origin(doc, page):
    """(x0, y1) of the effective CropBox in PDF space, following /Parent inheritance."""
    for key in ("CropBox", "MediaBox"):
        xref = page.xref
        while xref:
            kind, value = doc.xref_get_key(xref, key)
            if kind == "array":
                box = numbers(value)
                return min(box[0], box[2]), max(box[1], box[3])
            kind, value = doc.xref_get_key(xref, "Parent")
            xref = int(value.split()[0]) if kind == "xref" else 0
    return 0.0, page.rect.height


def to_page(rect, origin):
    """PDF-space rect -> PyMuPDF text space (unrotated, CropBox-relative, y down)."""
    x0, y1 = origin
    return fitz.Rect(rect[0] - x0, y1 - rect[3], rect[2] - x0, y1 - rect[1])


def family(font):
    return STYLE_SUFFIX.sub("", font.split("+")[-1])


def weighted_mode(counter):
    return max(counter.items(), key=lambda kv: kv[1])[0] if counter else None


def weighted_median(counter):
    total, running = sum(counter.values()), 0
    for size, count in sorted(counter.items()):
        running += count
        if running * 2 >= total:
            return size
    return None


def placements(doc, page):
    """Graphics placed on one page: named Forms, unnamed top-level Forms, rasters."""
    names = {name: xref for xref, name, invoker, _ in page.get_xobjects() if invoker == 0}
    forms = []
    find_forms(doc, page.read_contents(), names, IDENTITY, None, 0, None, forms)
    wraps_named = set()
    for form in forms:
        if form["file"]:
            parent = form["parent"]
            while parent is not None:
                wraps_named.add(parent)
                parent = forms[parent]["parent"]
    origin = crop_origin(doc, page)
    out = []
    for index, form in enumerate(forms):
        if not form["file"] and (form["depth"] or index in wraps_named):
            continue
        a, b, c, d = form["matrix"][:4]
        sx, sy = (a * a + b * b) ** 0.5, (c * c + d * d) ** 0.5
        own = intersect(form["bbox"], transform(form["visible"], invert(form["matrix"])))
        placed = transform(form["bbox"], form["matrix"])
        visible = form["visible"]
        out.append({"kind": "vector", "file": re.sub(r"^\./|(?<=/)/+", "", form["file"]) if form["file"] else None,
                    "rect": to_page(visible, origin), "scale": round((sx * sy) ** 0.5, 4),
                    "stretch": round(sx / sy, 3) if sy else None,
                    "placed_in": [round(sx * (own[2] - own[0]) / 72, 2), round(sy * (own[3] - own[1]) / 72, 2)],
                    "clipped": (placed[2] - placed[0]) * (placed[3] - placed[1])
                    > 1.01 * (visible[2] - visible[0]) * (visible[3] - visible[1]),
                    "rasters": [], "spans": []})
    for image in page.get_image_info(xrefs=True):
        a, b, c, d = image["transform"][:4]
        side_w, side_h = (a * a + b * b) ** 0.5 / 72, (c * c + d * d) ** 0.5 / 72
        dpi = min(image["width"] / side_w, image["height"] / side_h) if side_w and side_h else None
        raster = {"effective_dpi": round(dpi, 1) if dpi else None, "px": [image["width"], image["height"]],
                  "placed_in": [round(side_w, 2), round(side_h, 2)]}
        rect = fitz.Rect(image["bbox"])
        centre = (rect.tl + rect.br) * 0.5
        hosts = [p for p in out if p["kind"] == "vector" and centre in p["rect"] + (-1, -1, 1, 1)]
        if hosts:
            min(hosts, key=lambda p: p["rect"].get_area())["rasters"].append(raster)
        else:
            out.append({"kind": "raster", "file": None, "rect": rect, "scale": None, "stretch": None,
                        "placed_in": raster["placed_in"], "clipped": False, "rasters": [raster], "spans": []})
    return out


def reading_frame(rect, direction):
    """Rect in a caption's reading frame: u runs along its text, v down the lines."""
    dx, dy = direction
    us = [x * dx + y * dy for x in (rect.x0, rect.x1) for y in (rect.y0, rect.y1)]
    vs = [y * dx - x * dy for x in (rect.x0, rect.x1) for y in (rect.y0, rect.y1)]
    return min(us), max(us), min(vs), max(vs)


def associate(graphic, captions):
    """Nearest caption before or after the graphic in the caption's reading frame, overlapping it
    along the text direction (so landscape pages work); None beyond CAPTION_REACH."""
    best, best_gap = None, CAPTION_REACH
    for cap in captions:
        cu0, cu1, cv0, cv1 = reading_frame(cap["rect"], cap["dir"])
        gu0, gu1, gv0, gv1 = reading_frame(graphic["rect"], cap["dir"])
        if cu1 <= gu0 or cu0 >= gu1:
            continue
        if cv0 >= gv1 - 3:
            gap = cv0 - gv1
        elif cv1 <= gv0 + 3:
            gap = gv0 - cv1
        else:
            continue
        if gap < best_gap:
            best, best_gap = cap["label"], gap
    return best


def audit(path, floor):
    doc = fitz.open(path)
    groups, labels = [], set()
    body, caption_sizes, outside, outside_fonts = Counter(), Counter(), Counter(), Counter()
    for page in doc:
        graphics = placements(doc, page)
        captions = []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                spans = [s for s in line["spans"] if s["text"].strip()]
                if not spans:
                    continue
                label = CAPTION.match("".join(s["text"] for s in spans))
                if label:
                    word = "Table" if label.group(1) == "Table" else "Figure"
                    captions.append({"rect": fitz.Rect(line["bbox"]), "dir": tuple(line["dir"]),
                                     "label": f"{word} {label.group(2)}"})
                    labels.add(f"{word} {label.group(2)}")
                for span in spans:
                    box = fitz.Rect(span["bbox"])
                    centre = (box.tl + box.br) * 0.5
                    hosts = [g for g in graphics if centre in g["rect"] + (-1, -1, 1, 1)]
                    size, chars = round(span["size"], 2), len(span["text"].strip())
                    if hosts:
                        min(hosts, key=lambda g: g["rect"].get_area())["spans"].append(
                            (size, span["font"].split("+")[-1], span["text"].strip()))
                    elif label:
                        caption_sizes[round(size, 1)] += chars
                    else:
                        body[round(size, 1)] += chars
                        if size < floor:
                            outside[round(size, 1)] += chars
                            outside_fonts[span["font"].split("+")[-1]] += chars
        by_caption = {}
        for graphic in graphics:
            graphic["off_page"] = graphic["rect"] not in page.rect + (-1, -1, 1, 1)
            caption = associate(graphic, captions)
            key = caption or f"unmatched-{len(groups)}"
            if key not in by_caption:
                by_caption[key] = {"page": page.number + 1, "caption": caption, "panels": []}
                groups.append(by_caption[key])
            by_caption[key]["panels"].append(graphic)

    report = {"pdf": path, "pdf_sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(), "floor": floor,
              "figures": []}
    for number, group in enumerate(groups, 1):
        by_size = defaultdict(lambda: {"chars": 0, "fonts": Counter(), "samples": []})
        families, math, counts, notes = Counter(), Counter(), Counter(), []
        for panel in group["panels"]:
            for size, font, text in panel["spans"]:
                entry = by_size[size]
                entry["chars"] += len(text)
                entry["fonts"][font] += len(text)
                if len(entry["samples"]) < 3 and text not in entry["samples"]:
                    entry["samples"].append(text)
                (math if MATH_FONT.match(font) else families)[family(font)] += len(text)
                counts[size] += len(text)
            name = panel["file"] or panel["kind"]
            if panel["kind"] == "vector" and not panel["spans"] and not panel["rasters"]:
                notes.append(f"{name}: no extractable text (outlined glyphs, Type 3 bitmaps, or text-free)")
            if panel["stretch"] and abs(panel["stretch"] - 1) > 0.02:
                notes.append(f"{name}: non-uniform scaling x/y = {panel['stretch']} (stretched)")
            if panel["off_page"]:
                notes.append(f"{name}: extends beyond the page")
            if panel["clipped"]:
                notes.append(f"{name}: clipped to a window (trim/clip); measured inside the visible part only")
        kinds = {p["kind"] for p in group["panels"]}
        if any(p["rasters"] for p in group["panels"] if p["kind"] == "vector"):
            kinds.add("raster")
        report["figures"].append({
            "id": number, "page": group["page"], "caption": group["caption"],
            "kind": "mixed" if len(kinds) > 1 else kinds.pop(),
            "panels": [{"file": p["file"], "kind": p["kind"], "scale": p["scale"], "stretch": p["stretch"],
                        "placed_in": p["placed_in"], "rect_pt": [round(v, 1) for v in p["rect"]],
                        "rasters": p["rasters"]} for p in group["panels"]],
            "families": [f for f, _ in families.most_common()], "math_fonts": [f for f, _ in math.most_common()],
            "chars": sum(counts.values()), "min_size": min(counts) if counts else None,
            "median_size": weighted_median(counts), "max_size": max(counts) if counts else None,
            "below_floor_chars": sum(n for s, n in counts.items() if s < floor),
            "sizes": [{"size": s, "chars": e["chars"], "fonts": list(e["fonts"]), "samples": e["samples"]}
                      for s, e in sorted(by_size.items())],
            "notes": notes})
    used = {f["caption"] for f in report["figures"]}
    medians = {f["id"]: f["median_size"] for f in report["figures"] if f["median_size"] is not None}
    report["document"] = {
        "body_size": weighted_mode(body), "caption_size": weighted_mode(caption_sizes),
        "captions_without_graphics": sorted((x for x in labels - used if x.startswith("Figure")),
                                            key=lambda x: int(x.split()[1])),
        "outside_below_floor_chars": sum(outside.values()),
        "outside_below_floor_fonts": [f for f, _ in outside_fonts.most_common(3)]}
    report["set"] = {"main_families": dict(Counter(f["families"][0] for f in report["figures"] if f["families"])),
                     "median_sizes": medians,
                     "median_spread": round(max(medians.values()) - min(medians.values()), 2) if medians else None}
    return report


def render(report):
    doc = report["document"]
    lines = [f"{report['pdf']} (sha256 {report['pdf_sha256'][:12]}): body {doc['body_size']} pt, "
             f"caption {doc['caption_size']} pt, floor {report['floor']} pt",
             f"{'#':>2} {'page':>4} {'caption':<10} {'files':<30} {'kind':<6} {'width':>6} {'scale':>6} "
             f"{'text pt min/med/max':<20} {'<floor':>6}  main font"]
    for f in report["figures"]:
        sizes = "/".join("-" if v is None else f"{v:.2f}" for v in (f["min_size"], f["median_size"], f["max_size"]))
        scales = {p["scale"] for p in f["panels"] if p["scale"] is not None}
        scale = "-" if not scales else f"{min(scales):.3f}" + ("+" if len(scales) > 1 else "")
        files = ",".join((p["file"] or p["kind"]).split("/")[-1] for p in f["panels"])
        width = max(p["placed_in"][0] for p in f["panels"])
        lines.append(f"{f['id']:>2} {f['page']:>4} {str(f['caption']):<10} {files[-30:]:<30} {f['kind']:<6} "
                     f"{width:>5.2f}\" {scale:>6} {sizes:<20} {f['below_floor_chars']:>6}  "
                     f"{(f['families'] or ['-'])[0]}")
    for f in report["figures"]:
        small = [s for s in f["sizes"] if s["size"] < report["floor"]]
        if small:
            lines.append(f"  #{f['id']} below floor: " + "; ".join(f"{s['size']} pt {s['samples']}" for s in small))
        for p in f["panels"]:
            lines += [f"  #{f['id']} raster: {r['effective_dpi']} dpi effective ({r['px'][0]}x{r['px'][1]} px "
                      f"at {r['placed_in'][0]}x{r['placed_in'][1]} in)" for r in p["rasters"]]
        lines += [f"  #{f['id']} note: {n}" for n in f["notes"]]
        if len(f["families"]) > 1 or f["math_fonts"]:
            lines.append(f"  #{f['id']} fonts: {', '.join(f['families'])}"
                         + (f"; math: {', '.join(f['math_fonts'])}" if f["math_fonts"] else ""))
    s = report["set"]
    lines.append(f"Figure set: main fonts {s['main_families']}; median text spread {s['median_spread']} pt")
    if doc["captions_without_graphics"]:
        lines.append(f"Captions without an included graphic: {', '.join(doc['captions_without_graphics'])} "
                     "(text floats such as listings, inline TikZ/pgfplots, or a caption-matching miss); "
                     "review visually.")
    if doc["outside_below_floor_chars"]:
        lines.append(f"Outside figures: {doc['outside_below_floor_chars']} chars below floor "
                     f"({', '.join(doc['outside_below_floor_fonts'])}); usually math scripts or footnotes. "
                     "Inline TikZ/pgfplots text lands here and needs visual review.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("pdf")
    parser.add_argument("--floor", type=float, default=7.0, help="venue minimum rendered size in pt (default 7)")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of the table")
    args = parser.parse_args()
    report = audit(args.pdf, args.floor)
    print(json.dumps(report, indent=1) if args.json else render(report))


if __name__ == "__main__":
    main()
