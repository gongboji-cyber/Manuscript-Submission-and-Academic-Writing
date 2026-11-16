import hashlib
import json
import sys
import zipfile
from pathlib import Path

from lxml import etree


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def norm_xml(element):
    return etree.tostring(element, method="c14n", exclusive=True, with_comments=True)


def text_of(element):
    return "".join(element.itertext())


def report(path):
    path = Path(path)
    with zipfile.ZipFile(path) as zf:
        document_bytes = zf.read("word/document.xml")
        root = etree.fromstring(document_bytes)
    body = root.find(W + "body")
    paragraphs = body.findall(W + "p")
    tables = body.findall(W + "tbl")
    para_records = []
    for p in paragraphs:
        ppr = p.find(W + "pPr")
        para_records.append({
            "text": "".join(p.itertext()),
            "pPr_sha256": digest(norm_xml(ppr)) if ppr is not None else None,
            "xml_sha256": digest(norm_xml(p)),
        })
    table_records = []
    for tbl in tables:
        rows = tbl.findall(W + "tr")
        cells = [[text_of(tc) for tc in tr.findall(W + "tc")] for tr in rows]
        borders = []
        fills = []
        for r_idx, tr in enumerate(rows):
            for c_idx, tc in enumerate(tr.findall(W + "tc")):
                tcpr = tc.find(W + "tcPr")
                cell_edges = {}
                if tcpr is not None:
                    tc_borders = tcpr.find(W + "tcBorders")
                    if tc_borders is not None:
                        for edge in tc_borders:
                            cell_edges[etree.QName(edge).localname] = {
                                etree.QName(k).localname: v for k, v in edge.attrib.items()
                            }
                    shd = tcpr.find(W + "shd")
                    if shd is not None:
                        fills.append({"row": r_idx, "col": c_idx, "fill": shd.get(W + "fill")})
                borders.append({"row": r_idx, "col": c_idx, "edges": cell_edges})
        table_records.append({
            "rows": len(rows),
            "cells": cells,
            "borders": borders,
            "fills": fills,
            "gridCols": len(tbl.findall("./" + W + "tblGrid/" + W + "gridCol")),
        })
    sects = body.findall(W + "sectPr")
    return {
        "path": str(path),
        "sha256": digest(path.read_bytes()),
        "paragraphs": para_records,
        "tables": table_records,
        "section_sha256": [digest(norm_xml(x)) for x in sects],
    }


if __name__ == "__main__":
    print(json.dumps(report(sys.argv[1]), ensure_ascii=False, indent=2))
