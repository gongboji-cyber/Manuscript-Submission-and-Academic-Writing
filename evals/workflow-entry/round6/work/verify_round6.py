import hashlib
import json
import sys
import zipfile
from copy import deepcopy
from pathlib import Path

from lxml import etree


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = "{" + NS["w"] + "}"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def package(path):
    with zipfile.ZipFile(path) as zf:
        names = sorted(zf.namelist())
        parts = {name: zf.read(name) for name in names}
    return names, parts


def canonical_without_authorized_nodes(xml_bytes):
    root = etree.fromstring(xml_bytes)
    for node in root.xpath(".//w:tblBorders | .//w:tcBorders | .//w:shd", namespaces=NS):
        node.getparent().remove(node)
    return etree.tostring(root, method="c14n", exclusive=True, with_comments=True)


def edge_state(tc, edge):
    nodes = tc.xpath("./w:tcPr/w:tcBorders/w:" + edge, namespaces=NS)
    if not nodes:
        return None
    node = nodes[-1]
    return {
        "val": node.get(W + "val"),
        "sz": node.get(W + "sz"),
        "color": node.get(W + "color"),
    }


def verify(input_path, output_path):
    input_names, input_parts = package(input_path)
    output_names, output_parts = package(output_path)
    changed = [n for n in input_names if input_parts.get(n) != output_parts.get(n)]
    root_in = etree.fromstring(input_parts["word/document.xml"])
    root_out = etree.fromstring(output_parts["word/document.xml"])
    tables_in = root_in.xpath(".//w:body/w:tbl", namespaces=NS)
    tables_out = root_out.xpath(".//w:body/w:tbl", namespaces=NS)
    table = tables_out[0] if len(tables_out) == 1 else None
    rows = table.xpath("./w:tr", namespaces=NS) if table is not None else []
    shape = [len(r.xpath("./w:tc", namespaces=NS)) for r in rows]
    cell_text = [
        ["".join(tc.itertext()) for tc in row.xpath("./w:tc", namespaces=NS)]
        for row in rows
    ]
    input_cell_text = [
        ["".join(tc.itertext()) for tc in row.xpath("./w:tc", namespaces=NS)]
        for row in tables_in[0].xpath("./w:tr", namespaces=NS)
    ] if len(tables_in) == 1 else []
    border_checks = []
    for r_idx, row in enumerate(rows):
        for c_idx, tc in enumerate(row.xpath("./w:tc", namespaces=NS)):
            states = {edge: edge_state(tc, edge) for edge in (
                "top", "bottom", "left", "right", "start", "end",
                "insideH", "insideV", "tl2br", "tr2bl"
            )}
            wanted_top = r_idx == 0
            wanted_header_bottom = r_idx == 0
            wanted_table_bottom = r_idx == len(rows) - 1
            border_checks.append({
                "row": r_idx,
                "col": c_idx,
                "states": states,
                "top_ok": (states["top"] or {}).get("val") == "single" and (states["top"] or {}).get("sz") == "8" if wanted_top else (states["top"] is None or states["top"].get("val") in ("nil", "none")),
                "bottom_ok": (
                    (states["bottom"] or {}).get("val") == "single"
                    and (states["bottom"] or {}).get("sz") == ("8" if wanted_table_bottom else "4")
                ) if (wanted_header_bottom or wanted_table_bottom) else (states["bottom"] is None or states["bottom"].get("val") in ("nil", "none")),
                "other_edges_off": all(states[e] is None or states[e].get("val") in ("nil", "none") for e in ("left", "right", "start", "end", "insideH", "insideV", "tl2br", "tr2bl")),
            })
    shadings = root_out.xpath(".//w:body/w:tbl//w:shd", namespaces=NS)
    paragraphs_in = [etree.tostring(p, method="c14n", exclusive=True) for p in root_in.xpath("./w:body/w:p", namespaces=NS)]
    paragraphs_out = [etree.tostring(p, method="c14n", exclusive=True) for p in root_out.xpath("./w:body/w:p", namespaces=NS)]
    sects_in = [etree.tostring(s, method="c14n", exclusive=True) for s in root_in.xpath(".//w:sectPr", namespaces=NS)]
    sects_out = [etree.tostring(s, method="c14n", exclusive=True) for s in root_out.xpath(".//w:sectPr", namespaces=NS)]
    return {
        "input": str(input_path),
        "output": str(output_path),
        "input_sha256": sha256(input_path),
        "output_sha256": sha256(output_path),
        "zip_test": "readable",
        "package_members_equal": input_names == output_names,
        "changed_package_parts": changed,
        "only_document_xml_changed": changed == ["word/document.xml"],
        "non_target_xml_equal": canonical_without_authorized_nodes(input_parts["word/document.xml"]) == canonical_without_authorized_nodes(output_parts["word/document.xml"]),
        "outside_table_paragraph_xml_equal": paragraphs_in == paragraphs_out,
        "section_xml_equal": sects_in == sects_out,
        "table_count": len(tables_out),
        "table_shape": shape,
        "table_text_equal": cell_text == input_cell_text,
        "merge_markers_equal": [etree.tostring(x) for x in root_in.xpath(".//w:gridSpan | .//w:vMerge", namespaces=NS)] == [etree.tostring(x) for x in root_out.xpath(".//w:gridSpan | .//w:vMerge", namespaces=NS)],
        "shading_element_count": len(shadings),
        "borders_all_expected": bool(border_checks) and all(x["top_ok"] and x["bottom_ok"] and x["other_edges_off"] for x in border_checks),
        "border_checks": border_checks,
    }


if __name__ == "__main__":
    input_path = sys.argv[1]
    outputs = sys.argv[2:]
    print(json.dumps([verify(input_path, output) for output in outputs], ensure_ascii=False, indent=2))
