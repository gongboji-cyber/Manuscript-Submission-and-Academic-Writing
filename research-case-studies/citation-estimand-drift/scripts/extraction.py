#!/usr/bin/env python3
"""Citation-context extraction and provisional meaning-drift classification."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, List


VALUE_RE = re.compile(
    r"(?:1[,.\s]?400|1400|2[,.\s]?500|2500|1[,.\s]?620|1620)\s*(?:cases?)?(?:\s+of\s+pneumonia)?\s*(?:per\s*100[,\s]?000|/100[,\s]?000)",
    re.IGNORECASE,
)
SOURCE_RE = re.compile(r"UNICEF|Wahl|data\.unicef\.org|S2214-109X", re.IGNORECASE)


def extract_contexts(text: str, width: int = 500) -> List[str]:
    contexts: List[str] = []
    seen: set[str] = set()
    for match in VALUE_RE.finditer(text):
        start = max(0, match.start() - width)
        end = min(len(text), match.end() + width)
        fragment = re.sub(r"\s+", " ", text[start:end]).strip()
        key = fragment[:80]
        if key not in seen:
            seen.add(key)
            contexts.append(fragment)
    return contexts


def provisional_dimensions(passages: List[str]) -> List[str]:
    text = " ".join(passages).lower()
    codes: set[str] = set()
    has_incidence = re.search(r"\bincidence\b", text) is not None
    has_prevalence = re.search(r"\bprevalence\b|\bprevalent\b", text) is not None
    has_pretest = re.search(r"pre[- ]?test\s+probability|prior\s+probability|pretest", text) is not None
    has_infant = re.search(r"\binfant\b|\bneonatal\b|\bneonate\b", text) is not None

    if has_pretest:
        codes.add("D5")
    if has_prevalence and not has_incidence:
        codes.add("D1")
    if has_infant and re.search(r"(?:1[,.\s]?400|1400)", text):
        codes.add("D2")
    if not codes and has_incidence:
        codes.add("P0")
    if not codes:
        codes.add("U")
    return sorted(codes)


def build_evidence_rows(passage_dir: Path, registry_path: Path) -> List[Dict[str, str]]:
    with open(registry_path, encoding="utf-8-sig") as handle:
        registry = {r["record_id"]: r for r in csv.DictReader(handle)}
    rows: List[Dict[str, str]] = []
    for path in sorted(passage_dir.glob("*.txt")):
        record_id = path.stem
        text = path.read_text(encoding="utf-8", errors="ignore")
        contexts = extract_contexts(text)
        if not contexts:
            continue
        record = registry.get(record_id, {})
        rows.append(
            {
                "record_id": record_id,
                "doi": record.get("doi", ""),
                "source_cited": str(bool(SOURCE_RE.search(text))),
                "provisional_dimensions": ";".join(provisional_dimensions(contexts)),
                "passages": " || ".join(contexts[:3]),
                "reviewer_status": "machine_provisional",
            }
        )
    return rows


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract citation contexts and provisional codes.")
    parser.add_argument("--passages-dir", required=True)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    rows = build_evidence_rows(Path(args.passages_dir), Path(args.registry))
    if rows:
        with open(args.out, "w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    else:
        Path(args.out).write_text("", encoding="utf-8")
    print(f"wrote {len(rows)} evidence rows to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
