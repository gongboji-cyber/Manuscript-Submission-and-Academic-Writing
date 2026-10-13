#!/usr/bin/env python3
"""Traceable ordinary software-copyright code excerpt preparation.

Produces text and provenance, NOT registered documents or a legal compliance
certificate. Only explicitly named local source files are accepted. No third
party dependencies. Use a private output directory OUTSIDE the source project.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

LINES_PER_PAGE = 50
SIDE_PAGES = 30
DISALLOWED_DIRS = {
    ".git", "node_modules", "vendor", "third_party", "third-party",
    "__pycache__", ".venv", "venv", "dist", "build",
}
DISALLOWED_SUFFIXES = {
    ".ipynb", ".lock", ".map", ".pyc", ".class", ".jar", ".dll",
    ".exe", ".pdf", ".docx", ".zip", ".png", ".jpg", ".jpeg",
}
SENSITIVE = [
    re.compile(r"-----BEGIN [^-]*(?:PRIVATE KEY|OPENSSH PRIVATE KEY)-----"),
    re.compile(r"""(?i)(?:api[_-]?key|secret|password|access[_-]?token)\s*[:=]\s*["'][^"'\n]{6,}["']"""),
    re.compile(r"(?<!\d)[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?!\d)"),
]


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_file(root: Path, relative: str) -> tuple[Path, str]:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError("Absolute or traversing source path is prohibited")
    if not relative or any(p.lower() in DISALLOWED_DIRS for p in candidate.parts):
        raise ValueError("Vendor/generated directory is prohibited")
    if candidate.suffix.lower() in DISALLOWED_SUFFIXES or candidate.name.endswith(".min.js"):
        raise ValueError("Non-source or generated file is prohibited")
    final = (root / candidate).resolve(strict=True)
    if final == root or root not in final.parents or not final.is_file():
        raise ValueError("Source must be a regular file inside project")
    return final, final.relative_to(root).as_posix()


def prepare(project: Path, output: Path, relative_paths: list[str]) -> dict:
    root = project.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Project must be a directory")
    dest = output.resolve()
    if dest == root or root in dest.parents:
        raise ValueError("Output must be outside project to avoid accidental commit")
    if dest.exists() and any(dest.iterdir()):
        raise ValueError("Output directory is not empty (avoid stale evidence)")
    if not relative_paths or len(relative_paths) != len(set(relative_paths)):
        raise ValueError("Supply a non-empty, non-duplicate explicit source list")

    all_rows = []
    inventory = []
    for name in relative_paths:
        source, rel = safe_file(root, name)
        raw = source.read_bytes()
        if not raw or b"\0" in raw or len(raw) > 2_000_000:
            raise ValueError("Empty, binary or overlarge source file: " + rel)
        try:
            data = raw.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ValueError("Non-UTF8 source requires manual controlled conversion: " + rel) from exc
        if any(pattern.search(data) for pattern in SENSITIVE):
            raise ValueError("Possible credential or identity number: " + rel)
        lines = data.splitlines()
        if not lines:
            raise ValueError("No lines in source: " + rel)
        inventory.append({"file": rel, "sha256": sha256(raw), "source_lines": len(lines)})
        all_rows.extend({"file": rel, "original_line": i, "text": line}
                        for i, line in enumerate(lines, 1))

    cap = LINES_PER_PAGE * SIDE_PAGES
    total = len(all_rows)
    if total <= 2 * cap:
        mode = "full"
        parts = [("all", all_rows)]
    else:
        mode = "head_and_tail"
        parts = [("first_30", all_rows[:cap]), ("last_30", all_rows[-cap:])]

    dest.mkdir(parents=True, exist_ok=True)
    pages_dir = dest / "pages"
    pages_dir.mkdir()
    report = {
        "method": "ordinary_deposit_preflight",
        "status": "NOT_PDF_VALIDATED_NOT_OFFICIALLY_APPROVED",
        "rule": {"source_lines_per_logical_page": LINES_PER_PAGE,
                 "pages_per_side": SIDE_PAGES},
        "scope_confirmation_required": True,
        "rightsholder_confirmation_required": True,
        "rendered_pdf_page_check_required": True,
        "sources": inventory,
        "selected_total_source_lines": total,
        "deposit_mode": mode,
        "extracted_lines": sum(len(rows) for _, rows in parts),
        "parts": [],
        "pages": [],
        "warnings": [],
    }
    counter = 0
    for label, rows in parts:
        body = "\n".join(r["text"] for r in rows) + "\n"
        text_name = "code_" + label + ".txt"
        (dest / text_name).write_text(body, encoding="utf-8", newline="\n")
        segment = {"part": label, "text_file": text_name,
                   "line_count": len(rows), "sha256": sha256(body.encode("utf-8")),
                   "pages": []}
        for start in range(0, len(rows), LINES_PER_PAGE):
            counter += 1
            chunk = rows[start:start + LINES_PER_PAGE]
            page_name = f"page_{counter:03d}.txt"
            content = "\n".join(r["text"] for r in chunk) + "\n"
            (pages_dir / page_name).write_text(content, encoding="utf-8", newline="\n")
            spans = []
            for entry in chunk:
                if spans and spans[-1]["file"] == entry["file"] and spans[-1]["end_line"] + 1 == entry["original_line"]:
                    spans[-1]["end_line"] = entry["original_line"]
                else:
                    spans.append({"file": entry["file"], "start_line": entry["original_line"],
                                  "end_line": entry["original_line"]})
            item = {"logical_page": counter, "part": label, "page_file": "pages/" + page_name,
                    "line_count": len(chunk), "blank_line_count": sum(not x["text"].strip() for x in chunk),
                    "sha256": sha256(content.encode("utf-8")), "source_spans": spans}
            report["pages"].append(item)
            segment["pages"].append(counter)
            if item["blank_line_count"] > 10:
                report["warnings"].append(f"Logical page {counter}: many blank lines; manually review")
        report["parts"].append(segment)
    report["logical_page_count"] = counter
    report["warnings"].extend([
        "UTF-8 and line endings are normalized for page text; original files are hashed and untouched.",
        "A logical page is NOT a rendered Word/PDF page; check all actual physical pages.",
        "Confirm the selected files truly represent the applicant's software and are eligible original/authorized code.",
        "No intellectual-property ownership, secrets completeness, or clinical validation is certified.",
    ])
    (dest / "manifest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--files", nargs="+", required=True, help="ordered source paths relative to project")
    args = ap.parse_args()
    report = prepare(args.project, args.out, args.files)
    print(json.dumps({"mode": report["deposit_mode"],
                      "selected_source_lines": report["selected_total_source_lines"],
                      "extracted_lines": report["extracted_lines"],
                      "logical_pages": report["logical_page_count"],
                      "manifest": str(args.out / "manifest.json"),
                      "PDF_validated": False}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
