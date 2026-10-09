#!/usr/bin/env python3
"""Check that a figure repair changed only what it was meant to change.

Run the project's matplotlib generator under `capture` before and after the repair, then
`compare` the two captures. Each saved figure gets an inventory of its plotted content, sorted
into categories:

  DATA     plotted values: line, scatter, band, error-bar and image data, bar values (base and
           length; bar position and width are STYLE)
  NUMERIC  numbers inside figure text (value labels, annotations), compared as a multiset
  TEXT     titles, axis labels, legend entries, annotations
  AXES     limits, scales, tick labels
  STYLE    colours, markers, widths, fonts, positions, sizes; all geometry of axes drawn
           with the axis off (diagrams), so moving a box or connector is not a data change;
           a line added or removed whose every point a same-colour line already draws (an
           overplot, such as a filled marker over an open one)

Usage (with the project's interpreter, from the directory the generator expects):
  figure_guard.py capture OUT_DIR [--root DIR] -- script.py [args]   (or: -- -m package.module [args])
  figure_guard.py compare BEFORE_DIR AFTER_DIR [--json]

capture also writes reads.json: every file under --root (default: the current directory) that
the generator and its local imports opened for reading, with its sha256: the inputs to freeze and
to re-check before writing back. Several generators captured into one directory share one
reads.json. Exit status of compare: 1 when any DATA or NUMERIC difference exists, an output was
saved on one side only, or bytes changed with no inventoried difference; else 0.
"""

import argparse
import hashlib
import json
import re
import runpy
import sys
from collections import Counter
from pathlib import Path

CATEGORIES = ("DATA", "NUMERIC", "TEXT", "AXES", "STYLE")
NUMBER = re.compile(r"[-−]?\d+(?:[.,]\d+)*%?")


def sha256(path):
    path = Path(path)
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def rounded(values):
    try:
        import numpy as np

        array = np.asarray(values, dtype=float)
        return np.round(array, 9).tolist()
    except (TypeError, ValueError):
        return str(values)


def colour(value):
    from matplotlib.colors import to_hex

    try:
        return to_hex(value, keep_alpha=True)
    except (TypeError, ValueError):
        return [colour(v) for v in value] if len(value) else []


def keyed(items, prefix):
    """Key artists by their label when unique, so reordering plot calls is not a change."""
    labels = Counter(item.get_label() for item in items)
    for i, item in enumerate(items):
        label = item.get_label()
        yield (f"{prefix}[{label}]" if label and not label.startswith("_") and labels[label] == 1
               else f"{prefix}{i}"), item


def inventory(fig):
    from matplotlib.collections import PolyCollection
    from matplotlib.container import BarContainer

    inv = {c: {} for c in CATEGORIES}
    inv["STYLE"]["figure.size"] = rounded(fig.get_size_inches())
    for i, t in enumerate(fig.texts):
        inv["TEXT"][f"figure.text{i}"] = t.get_text()
    for a, ax in enumerate(fig.axes):
        p, data = f"ax{a}", ("DATA" if ax.axison else "STYLE")
        inv["STYLE"][f"{p}.position"] = rounded(ax.get_position().bounds)
        inv["STYLE"][f"{p}.fonts"] = sorted({t.get_fontname() for t in ax.texts + ax.get_xticklabels()
                                              + ax.get_yticklabels() + [ax.xaxis.label, ax.yaxis.label]})
        for name in ("title", "xlabel", "ylabel"):
            inv["TEXT"][f"{p}.{name}"] = getattr(ax, f"get_{name}")()
        if ax.axison:
            inv["AXES"][f"{p}.limits"] = rounded([ax.get_xlim(), ax.get_ylim()])
            inv["AXES"][f"{p}.scales"] = [ax.get_xscale(), ax.get_yscale()]
            inv["AXES"][f"{p}.xticks"] = [t.get_text() for t in ax.get_xticklabels()]
            inv["AXES"][f"{p}.yticks"] = [t.get_text() for t in ax.get_yticklabels()]
        for key, line in keyed(ax.lines, f"{p}.line"):
            inv[data][f"{key}.xy"] = rounded(line.get_xydata())
            inv["STYLE"][f"{key}.style"] = [colour(line.get_color()), line.get_linewidth(), line.get_linestyle(),
                                            str(line.get_marker()), line.get_markersize(),
                                            colour(line.get_markerfacecolor()), line.get_markeredgewidth()]
        for k, container in enumerate(c for c in ax.containers if isinstance(c, BarContainer)):
            value = ("get_x", "get_width") if container.orientation == "horizontal" else ("get_y", "get_height")
            inv[data][f"{p}.bars{k}"] = [rounded([getattr(r, g)() for g in value]) for r in container.patches]
        for key, patch in keyed(ax.patches, f"{p}.patch"):
            inv["STYLE"][key] = [type(patch).__name__, colour(patch.get_facecolor()),
                                 rounded(patch.get_extents().bounds)]
        for key, coll in keyed(ax.collections, f"{p}.coll"):
            inv[data][f"{key}.offsets"] = rounded(coll.get_offsets())
            if isinstance(coll, PolyCollection) or type(coll).__name__ in ("LineCollection", "FillBetweenPolyCollection"):
                inv[data][f"{key}.paths"] = [rounded(path.vertices) for path in coll.get_paths()]
            if coll.get_array() is not None:
                inv[data][f"{key}.array"] = rounded(coll.get_array())
            inv["STYLE"][f"{key}.style"] = [colour(coll.get_facecolor()), colour(coll.get_edgecolor()),
                                            rounded(coll.get_linewidths()), rounded(coll.get_sizes())]
        for i, image in enumerate(ax.images):
            inv[data][f"{p}.image{i}"] = hashlib.sha256(image.get_array().tobytes()).hexdigest()
        seen = Counter()
        for t in ax.texts:  # keyed by content, so inserting one label does not re-key the others
            seen[t.get_text()] += 1
            key = f"{p}.text[{t.get_text()}]" + (f"#{seen[t.get_text()]}" if seen[t.get_text()] > 1 else "")
            inv["TEXT"][key] = t.get_text()
            inv["STYLE"][f"{key}.place"] = rounded(t.get_position()) + [t.get_fontsize(), t.get_fontweight()]
        legend = ax.get_legend()
        if legend:
            inv["TEXT"][f"{p}.legend"] = [t.get_text() for t in legend.get_texts()]
            inv["STYLE"][f"{p}.legend.place"] = [str(legend._loc), rounded(legend.get_window_extent().bounds)]
    return inv


def capture(out, command, root="."):
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib.figure import Figure

    out, root = Path(out), Path(root).resolve()
    out.mkdir(parents=True, exist_ok=True)
    original, outputs = Figure.savefig, set()

    def savefig(self, fname, *args, **kwargs):
        previous = sha256(fname) if isinstance(fname, (str, Path)) else None
        result = original(self, fname, *args, **kwargs)
        if isinstance(fname, (str, Path)):
            path = Path(fname).resolve()
            outputs.add(path)
            name = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
            record = {"file": name, "sha256": sha256(path), "previous_sha256": previous, "inventory": inventory(self)}
            (out / (name.replace("/", "__") + ".json")).write_text(json.dumps(record))
        return result

    Figure.savefig = savefig
    reads = set()

    def audit(event, args):  # every file the generator and its local imports read under root
        if event == "open" and isinstance(args[0], (str, Path)) and (args[1] or "r").strip("rbt") == "":
            path = Path(args[0]).resolve()
            if path.is_relative_to(root) and "__pycache__" not in path.parts and not path.is_relative_to(out.resolve()):
                reads.add(path)

    sys.addaudithook(audit)
    try:
        run(command)
    finally:  # local modules loaded from __pycache__ never open their source, so add them by name
        reads.update(Path(m.__file__).resolve() for m in list(sys.modules.values())
                     if getattr(m, "__file__", None) and Path(m.__file__).resolve().is_relative_to(root)
                     and Path(m.__file__).resolve() != Path(__file__).resolve())
        listing = json.loads((out / "reads.json").read_text()) if (out / "reads.json").exists() else {}
        listing.update({str(p.relative_to(root)): sha256(p) for p in reads - outputs if p.is_file()})
        (out / "reads.json").write_text(json.dumps(dict(sorted(listing.items())), indent=1))


def run(command):
    if command[0] == "-m":
        sys.argv = command[1:]
        runpy.run_module(command[1], run_name="__main__", alter_sys=True)
    else:
        sys.argv = command
        sys.path.insert(0, str(Path(command[0]).resolve().parent))
        runpy.run_path(command[0], run_name="__main__")


def numbers(texts):
    found = Counter()
    for t in texts:
        found.update(NUMBER.findall(t if isinstance(t, str) else " ".join(t)))
    return found


def overplot(key, inv, other):
    """A line drawn on one side only whose every point the other side draws in the same colour."""
    if ".line" not in key or not key.endswith(".xy") or key not in inv["DATA"] or key in other["DATA"]:
        return False
    axes, col = key.split(".")[0], inv["STYLE"][key[:-3] + ".style"][0]
    drawn = {tuple(p) for k, xy in other["DATA"].items() if k.startswith(f"{axes}.line") and k.endswith(".xy")
             and other["STYLE"][k[:-3] + ".style"][0] == col for p in xy}
    return all(tuple(p) in drawn for p in inv["DATA"][key])


def diff(before, after):
    result = {c: [] for c in CATEGORIES}
    for c in CATEGORIES[:1] + CATEGORIES[2:]:
        b, a = before[c], after[c]
        result[c] = [k for k in sorted(set(b) | set(a)) if b.get(k) != a.get(k)]
    over = [k for k in result["DATA"] if overplot(k, after, before) or overplot(k, before, after)]
    result["DATA"] = [k for k in result["DATA"] if k not in over]
    result["STYLE"] += [k[:-3] + ".overplot" for k in over]
    lost = numbers(before["TEXT"].values()) - numbers(after["TEXT"].values())
    gained = numbers(after["TEXT"].values()) - numbers(before["TEXT"].values())
    result["NUMERIC"] = [f"-{n}" for n in sorted(lost.elements())] + [f"+{n}" for n in sorted(gained.elements())]
    return result


def compare(before_dir, after_dir):
    load = lambda d: {r["file"]: r for r in (json.loads(p.read_text()) for p in Path(d).glob("*.json")  # noqa: E731
                                             if p.name != "reads.json")}
    before, after = load(before_dir), load(after_dir)
    report = []
    for name in sorted(set(before) | set(after)):
        b, a = before.get(name), after.get(name)
        entry = {"file": name, "only_in": None if b and a else ("before" if b else "after"),
                 "bytes_identical": bool(b and a and b["sha256"] == a["sha256"]),
                 "reproduced": bool(b and b["previous_sha256"] in (None, b["sha256"]))}
        entry.update(diff(b["inventory"], a["inventory"]) if b and a else {c: [] for c in CATEGORIES})
        entry["unexplained"] = bool(b and a) and not entry["bytes_identical"] and not any(entry[c] for c in CATEGORIES)
        report.append(entry)
    return report


def render(report):
    lines = []
    for f in report:
        if f["only_in"]:
            lines.append(f"{f['file']}: saved only {f['only_in']} the repair")
            continue
        state = "bytes identical" if f["bytes_identical"] else "bytes differ"
        lines.append(f"{f['file']}: {state}" + ("" if f["reproduced"] else " (baseline run did not reproduce the "
                                                                          "existing file)"))
        for c in CATEGORIES:
            if f[c]:
                lines.append(f"  {c}: " + ", ".join(f[c][:12]) + (" ..." if len(f[c]) > 12 else ""))
        if not f["bytes_identical"] and not any(f[c] for c in CATEGORIES):
            lines.append("  UNEXPLAINED: bytes differ but no inventoried property changed; inspect the render")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    cap = sub.add_parser("capture")
    cap.add_argument("out")
    cap.add_argument("--root", default=".", help="top directory of everything the generator reads (default: cwd)")
    cmp = sub.add_parser("compare")
    cmp.add_argument("before")
    cmp.add_argument("after")
    cmp.add_argument("--json", action="store_true")
    argv, command = sys.argv[1:], []
    if "--" in argv:
        argv, command = argv[:argv.index("--")], argv[argv.index("--") + 1:]
    args = parser.parse_args(argv)
    if args.cmd == "capture":
        if not command:
            parser.error("capture needs the generator after --")
        capture(args.out, command, args.root)
        return 0
    report = compare(args.before, args.after)
    print(json.dumps(report, indent=1) if args.json else render(report))
    return int(any(f["DATA"] or f["NUMERIC"] or f["only_in"] or f["unexplained"] for f in report))


if __name__ == "__main__":
    sys.exit(main())
