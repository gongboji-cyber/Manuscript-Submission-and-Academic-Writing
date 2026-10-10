#!/usr/bin/env python3
"""Small, dependency-free renderer for editable scientific block diagrams.

Input: explicit-position JSON. Output: native draw.io XML, SVG, audit JSON.
This is intentionally NOT an automatic layout engine or scientific fact checker.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


ROLES = {
    "input": ("#e7f1f9", "#407897"),
    "process": ("#edf0f4", "#697889"),
    "novel": ("#ffeddc", "#b36a36"),
    "output": ("#e6f3e9", "#42835b"),
    "validation": ("#eae8f6", "#736b9c"),
    "decision": ("#fdf3d9", "#9e823d"),
    "excluded": ("#f8e9e7", "#aa655e"),
}
EDGE_STYLES = {"main": ("#425466", False), "conditional": ("#425466", True),
               "feedback": ("#7b668e", True), "hypothesis": ("#aa655e", True)}
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def number(v, name, lo=0, hi=99999):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not lo <= v <= hi:
        raise ValueError(f"{name} must be a finite number in [{lo}, {hi}]")
    return float(v)


def text_lines(label):
    return str(label).split("\n")


def text_estimate(line, font_size):
    # Conservative approximation only; final visual inspection is mandatory.
    return sum(font_size * (0.98 if ord(c) >= 0x2E80 else 0.59) for c in line)


def overlap(a, b, margin=0):
    return (a["x"] < b["x"] + b["w"] + margin and
            a["x"] + a["w"] + margin > b["x"] and
            a["y"] < b["y"] + b["h"] + margin and
            a["y"] + a["h"] + margin > b["y"])


def segment_through_rect(p, q, rect):
    """Report only simple axis-aligned segments through a foreign box interior."""
    x1, y1 = p
    x2, y2 = q
    left, right = rect["x"] + 3, rect["x"] + rect["w"] - 3
    top, bottom = rect["y"] + 3, rect["y"] + rect["h"] - 3
    if abs(y1 - y2) < 0.001 and top < y1 < bottom:
        return max(min(x1, x2), left) < min(max(x1, x2), right)
    if abs(x1 - x2) < 0.001 and left < x1 < right:
        return max(min(y1, y2), top) < min(max(y1, y2), bottom)
    return False


def evaluate(spec, strict=False):
    errors, warnings = [], []
    canvas = spec.get("canvas", {})
    try:
        width = number(canvas.get("width"), "canvas.width", 320, 5000)
        height = number(canvas.get("height"), "canvas.height", 240, 5000)
    except (TypeError, ValueError) as exc:
        return {"errors": [str(exc)], "warnings": [], "passed": False}
    synthetic = spec.get("synthetic")
    if not isinstance(synthetic, bool):
        errors.append("Set top-level synthetic to true or false explicitly.")
    if not isinstance(spec.get("title"), str) or not spec["title"].strip():
        errors.append("Non-empty title is required.")
    elif text_estimate(spec["title"], 21) > width - 48:
        warnings.append("Title may exceed canvas width.")
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    groups = spec.get("groups", [])
    if not isinstance(nodes, list) or len(nodes) < 2:
        errors.append("At least two nodes are required.")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges must be an array")
        edges = []
    if not isinstance(groups, list):
        errors.append("groups must be an array")
        groups = []
    ids = set()
    checked = []
    for i, n in enumerate(nodes):
        if not isinstance(n, dict):
            errors.append(f"nodes[{i}] is not an object")
            continue
        ident = n.get("id")
        if not isinstance(ident, str) or not ID_RE.fullmatch(ident):
            errors.append(f"nodes[{i}].id must match {ID_RE.pattern}")
            continue
        if ident in ids:
            errors.append(f"Duplicate node id {ident}")
        ids.add(ident)
        if n.get("role", "process") not in ROLES:
            errors.append(f"{ident}: unknown role {n.get('role')!r}")
        if n.get("shape", "round") not in ("round", "rect", "diamond"):
            errors.append(f"{ident}: unknown shape")
        if not isinstance(n.get("label"), str) or not n["label"].strip():
            errors.append(f"{ident}: non-empty label required")
        try:
            for attr, lo in (("x", 0), ("y", 0), ("w", 48), ("h", 32)):
                number(n.get(attr), f"{ident}.{attr}", lo)
            if n["x"] + n["w"] > width or n["y"] + n["h"] > height:
                errors.append(f"{ident}: node lies beyond canvas")
            checked.append(n)
            for line in text_lines(n.get("label", "")):
                if text_estimate(line, 15) > n["w"] - 18:
                    warnings.append(f"{ident}: possible text overflow; inspect SVG")
                    break
            if len(text_lines(n.get("label", ""))) * 20 > n["h"] - 8:
                warnings.append(f"{ident}: possible vertical text overflow")
        except (TypeError, ValueError, KeyError) as exc:
            errors.append(str(exc))
        if not synthetic and not n.get("evidence"):
            msg = f"{ident}: missing source/plan evidence"
            (errors if strict else warnings).append(msg)
        if "count" in n:
            value = n["count"]
            if type(value) is not int or value < 0:
                errors.append(f"{ident}: count must be a non-negative integer")
            elif not re.search(r"\bn\s*=\s*" + str(value) + r"(?!\d)", n.get("label", ""), flags=re.I):
                warnings.append(f"{ident}: count disagrees with / missing from label")
            if not n.get("unit"):
                errors.append(f"{ident}: count requires unit (patients, records, samples...)")
    for i, a in enumerate(checked):
        for b in checked[i + 1:]:
            if overlap(a, b):
                errors.append(f"Node boxes overlap: {a['id']} and {b['id']}")
    edge_ids = set()
    index = {n["id"]: n for n in checked}
    for i, e in enumerate(edges):
        if not isinstance(e, dict):
            errors.append(f"edges[{i}] is not an object")
            continue
        ident = e.get("id")
        if not isinstance(ident, str) or not ID_RE.fullmatch(ident) or ident in edge_ids or ident in ids:
            errors.append(f"Invalid/duplicate edge id {ident!r}")
        edge_ids.add(ident)
        if e.get("source") not in ids or e.get("target") not in ids:
            errors.append(f"{ident}: unknown source/target")
        if e.get("source") == e.get("target"):
            warnings.append(f"{ident}: self loop requires manual routing review")
        if e.get("kind", "main") not in EDGE_STYLES:
            errors.append(f"{ident}: unknown edge kind")
        for port in ("from_port", "to_port"):
            if e.get(port, "auto") not in ("auto", "top", "bottom", "left", "right"):
                errors.append(f"{ident}: invalid {port}")
        via = e.get("via", [])
        if not isinstance(via, list):
            errors.append(f"{ident}: via must be a list of waypoints")
            via = []
        for xy in via:
            if not isinstance(xy, list) or len(xy) != 2:
                errors.append(f"{ident}: via must contain [x,y]")
                continue
            try:
                x, y = number(xy[0], "via.x"), number(xy[1], "via.y")
                if x > width or y > height:
                    errors.append(f"{ident}: waypoint exceeds canvas")
            except (TypeError, ValueError) as exc:
                errors.append(str(exc))
        if not synthetic and e.get("label") and not e.get("evidence"):
            msg = f"{ident}: labelled edge has no evidence"
            (errors if strict else warnings).append(msg)
        if e.get("source") in index and e.get("target") in index:
            pts, _, _ = edge_points(index[e["source"]], index[e["target"]], e)
            for foreign in checked:
                if foreign["id"] in (e["source"], e["target"]):
                    continue
                if any(segment_through_rect(p, q, foreign) for p, q in zip(pts, pts[1:])):
                    warnings.append(f"{ident}: path crosses {foreign['id']} (check actual render)")
    for bal in spec.get("balances", []):
        if not isinstance(bal, dict) or bal.get("parent") not in index:
            errors.append("Invalid balance parent")
            continue
        parts = bal.get("parts", [])
        if not isinstance(parts, list) or not parts or len(parts) != len(set(parts)) or any(p not in index for p in parts):
            errors.append(f"{bal['parent']}: invalid balance parts")
            continue
        involved = [index[bal["parent"]], *[index[p] for p in parts]]
        if any(type(n.get("count")) is not int or n["count"] < 0 or not n.get("unit") for n in involved):
            errors.append(f"{bal['parent']}: all balanced nodes need valid integer count and unit")
            continue
        if len({n["unit"] for n in involved}) != 1:
            errors.append(f"{bal['parent']}: cannot balance different units")
        elif involved[0]["count"] != sum(n["count"] for n in involved[1:]):
            errors.append(f"{bal['parent']}: conservation check fails")
    for g in groups:
        if not isinstance(g, dict) or not all(x in g for x in ("label", "x", "y", "w", "h")):
            errors.append("Every group needs label, x, y, w, h")
            continue
        try:
            for a in ("x", "y", "w", "h"):
                number(g[a], f"group.{a}", 0 if a in ("x", "y") else 1)
            if g["x"] + g["w"] > width or g["y"] + g["h"] > height:
                errors.append(f"group {g['label']}: beyond canvas")
        except (TypeError, ValueError) as exc:
            errors.append(str(exc))
    if len(nodes) > 14:
        warnings.append("Dense diagram: consider grouped overview + detailed subfigure.")
    return {"errors": sorted(set(errors)), "warnings": sorted(set(warnings)),
            "passed": not errors, "node_count": len(nodes), "edge_count": len(edges),
            "synthetic": synthetic, "note": "Automated checks are not visual or scientific validation."}


def port(n, side):
    x, y, w, h = [n[k] for k in ("x", "y", "w", "h")]
    return {"right": (x + w, y + h / 2), "left": (x, y + h / 2),
            "top": (x + w / 2, y), "bottom": (x + w / 2, y + h)}[side]


def choose_ports(a, b, e):
    ax, ay = a["x"] + a["w"] / 2, a["y"] + a["h"] / 2
    bx, by = b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
    if abs(bx - ax) > abs(by - ay):
        ap, bp = (("right", "left") if bx >= ax else ("left", "right"))
    else:
        ap, bp = (("bottom", "top") if by >= ay else ("top", "bottom"))
    return e.get("from_port", "auto").replace("auto", ap), e.get("to_port", "auto").replace("auto", bp)


def edge_points(a, b, e):
    ap, bp = choose_ports(a, b, e)
    start, end = port(a, ap), port(b, bp)
    via = [tuple(x) for x in e.get("via", [])]
    if not via and abs(start[0] - end[0]) > 2 and abs(start[1] - end[1]) > 2:
        # Basic elbow, not an obstacle-aware route; manually add via if necessary.
        mid = (start[0] + end[0]) / 2
        via = [(mid, start[1]), (mid, end[1])]
    return [start, *via, end], ap, bp


def svg_element(parent, tag, **props):
    return ET.SubElement(parent, tag, {k.replace("_", "-"): str(v) for k, v in props.items()})


def render_svg(spec):
    width, height = spec["canvas"]["width"], spec["canvas"]["height"]
    svg = ET.Element("svg", {"xmlns": "http://www.w3.org/2000/svg",
                             "viewBox": f"0 0 {width} {height}", "width": str(width),
                             "height": str(height), "role": "img",
                             "aria-label": spec["title"]})
    ET.SubElement(svg, "title").text = spec["title"]
    ET.SubElement(svg, "desc").text = "Editable figure source is the matching draw.io file."
    defs = ET.SubElement(svg, "defs")
    marker = ET.SubElement(defs, "marker", {"id": "arrow", "viewBox": "0 0 10 10",
                                           "refX": "9", "refY": "5",
                                           "markerWidth": "7", "markerHeight": "7",
                                           "orient": "auto-start-reverse"})
    svg_element(marker, "path", d="M 0 0 L 10 5 L 0 10 z", fill="#425466")
    svg_element(svg, "rect", x=0, y=0, width=width, height=height, fill="#ffffff")
    title = svg_element(svg, "text", x=24, y=35, fill="#213344", font_size=21,
                        font_weight=600, font_family="Arial, Helvetica, sans-serif")
    title.text = spec["title"]
    for g in spec.get("groups", []):
        svg_element(svg, "rect", x=g["x"], y=g["y"], width=g["w"], height=g["h"],
                    rx=12, fill="#f7f9fb", stroke="#bdc9d2", stroke_width=1,
                    stroke_dasharray="5 5")
        t = svg_element(svg, "text", x=g["x"] + 12, y=g["y"] + 23,
                        fill="#536578", font_family="Arial, Helvetica, sans-serif",
                        font_size=14, font_weight=600)
        t.text = g["label"]
    nodes = {n["id"]: n for n in spec["nodes"]}
    for e in spec.get("edges", []):
        pts, _, _ = edge_points(nodes[e["source"]], nodes[e["target"]], e)
        color, dashed = EDGE_STYLES[e.get("kind", "main")]
        line = svg_element(svg, "polyline", points=" ".join(f"{x:g},{y:g}" for x, y in pts),
                           fill="none", stroke=color, stroke_width=2,
                           marker_end="url(#arrow)", stroke_linejoin="round")
        if dashed:
            line.set("stroke-dasharray", "6 4")
        if e.get("label"):
            seg = max(zip(pts[:-1], pts[1:]), key=lambda t: math.dist(t[0], t[1]))
            lx = (seg[0][0] + seg[1][0]) / 2 + e.get("label_dx", 0)
            ly = (seg[0][1] + seg[1][1]) / 2 - 9 + e.get("label_dy", 0)
            t = svg_element(svg, "text", x=lx, y=ly, fill=color, font_size=13,
                            text_anchor="middle", font_family="Arial, Helvetica, sans-serif")
            t.text = e["label"]
    for n in spec["nodes"]:
        fill, border = ROLES[n.get("role", "process")]
        x, y, w, h = [n[k] for k in ("x", "y", "w", "h")]
        shape = n.get("shape", "round")
        if shape == "diamond":
            points = f"{x+w/2:g},{y:g} {x+w:g},{y+h/2:g} {x+w/2:g},{y+h:g} {x:g},{y+h/2:g}"
            svg_element(svg, "polygon", points=points, fill=fill, stroke=border, stroke_width=1.6)
        else:
            svg_element(svg, "rect", x=x, y=y, width=w, height=h, rx=12 if shape == "round" else 2,
                        fill=fill, stroke=border, stroke_width=1.6)
        lines = text_lines(n["label"])
        baseline = y + h / 2 - (len(lines) - 1) * 10 + 5
        t = svg_element(svg, "text", x=x + w / 2, y=baseline, fill="#23313e",
                        font_size=15, font_family="Arial, Helvetica, sans-serif",
                        text_anchor="middle")
        for i, line in enumerate(lines):
            sub = svg_element(t, "tspan", x=x + w / 2, dy=0 if i == 0 else 20)
            sub.text = line
    return ET.tostring(svg, encoding="unicode", xml_declaration=True)


def render_drawio(spec):
    f = ET.Element("mxfile", {"host": "app.diagrams.net", "agent": "research-flow-diagrams"})
    diagram = ET.SubElement(f, "diagram", {"name": "Figure"})
    model = ET.SubElement(diagram, "mxGraphModel", {
        "dx": "1200", "dy": "800", "grid": "1", "gridSize": "10", "guides": "1",
        "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1",
        "pageScale": "1", "pageWidth": str(spec["canvas"]["width"]),
        "pageHeight": str(spec["canvas"]["height"]), "math": "0", "shadow": "0"})
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    for i, g in enumerate(spec.get("groups", [])):
        c = ET.SubElement(root, "mxCell", {
            "id": f"group-{i}", "value": g["label"],
            "style": "rounded=1;whiteSpace=wrap;html=0;align=left;verticalAlign=top;"
                     "spacingLeft=12;spacingTop=10;fillColor=#f7f9fb;strokeColor=#bdc9d2;"
                     "dashed=1;fontColor=#536578;fontSize=14;",
            "vertex": "1", "parent": "1"})
        ET.SubElement(c, "mxGeometry", {"x": str(g["x"]), "y": str(g["y"]),
                                         "width": str(g["w"]), "height": str(g["h"]),
                                         "as": "geometry"})
    for n in spec["nodes"]:
        fill, border = ROLES[n.get("role", "process")]
        shape = n.get("shape", "round")
        design = "rhombus;" if shape == "diamond" else ("rounded=1;arcSize=12;" if shape == "round" else "rounded=0;")
        style = (f"{design}whiteSpace=wrap;html=0;align=center;verticalAlign=middle;"
                 f"fillColor={fill};strokeColor={border};strokeWidth=1.5;"
                 "fontColor=#23313e;fontFamily=Arial;fontSize=15;")
        c = ET.SubElement(root, "mxCell", {"id": n["id"], "value": n["label"],
                                            "style": style, "vertex": "1", "parent": "1"})
        ET.SubElement(c, "mxGeometry", {"x": str(n["x"]), "y": str(n["y"]), "width": str(n["w"]),
                                         "height": str(n["h"]), "as": "geometry"})
    nodes = {n["id"]: n for n in spec["nodes"]}
    side = {"left": (0, 0.5), "right": (1, 0.5), "top": (0.5, 0), "bottom": (0.5, 1)}
    for e in spec.get("edges", []):
        color, dash = EDGE_STYLES[e.get("kind", "main")]
        points, ap, bp = edge_points(nodes[e["source"]], nodes[e["target"]], e)
        ex, ey = side[ap]
        ix, iy = side[bp]
        style = (f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=0;"
                 f"strokeColor={color};strokeWidth=2;endArrow=block;endFill=1;"
                 f"dashed={1 if dash else 0};exitX={ex};exitY={ey};exitDx=0;exitDy=0;"
                 f"entryX={ix};entryY={iy};entryDx=0;entryDy=0;"
                 "fontColor=#425466;fontSize=13;")
        c = ET.SubElement(root, "mxCell", {
            "id": e["id"], "value": e.get("label", ""), "style": style,
            "edge": "1", "parent": "1", "source": e["source"], "target": e["target"]})
        geo = ET.SubElement(c, "mxGeometry", {"relative": "1", "as": "geometry"})
        if len(points) > 2:
            array = ET.SubElement(geo, "Array", {"as": "points"})
            for x, y in points[1:-1]:
                ET.SubElement(array, "mxPoint", {"x": str(x), "y": str(y)})
    return ET.tostring(f, encoding="unicode", xml_declaration=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path, help="Explicit-position UTF-8 JSON")
    parser.add_argument("--out", required=True, type=Path, help="Output folder")
    parser.add_argument("--strict", action="store_true", help="Require evidence on every real node / labelled edge")
    args = parser.parse_args(argv)
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        audit = evaluate(spec, strict=args.strict)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not audit["passed"]:
        print("FAIL: " + "; ".join(audit["errors"]), file=sys.stderr)
        return 2
    svg = render_svg(spec)
    drawio = render_drawio(spec)
    # Both are reparsed before writing, catching malformed XML early.
    ET.fromstring(svg)
    ET.fromstring(drawio)
    (args.out / "diagram.svg").write_text(svg + "\n", encoding="utf-8")
    (args.out / "diagram.drawio").write_text(drawio + "\n", encoding="utf-8")
    print(f"Generated diagram.svg and diagram.drawio; {len(audit['warnings'])} warning(s).")
    print("Mandatory next step: open the actual render and native draw.io file; inspect every label and edge.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
