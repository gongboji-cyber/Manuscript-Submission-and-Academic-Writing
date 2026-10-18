#!/usr/bin/env python3
"""Multi-channel citation discovery and de-duplication helpers.

This module intentionally contains no network code in the importable functions so
the test suite can run offline. The command-line interface can fetch OpenAlex if
network access and polite-use settings are available.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def reconstruct_abstract(inverted_index: Dict[str, List[int]] | None) -> str:
    if not inverted_index:
        return ""
    positions: Dict[int, str] = {}
    for word, indexes in inverted_index.items():
        for index in indexes:
            positions[index] = word
    return " ".join(positions[i] for i in sorted(positions))


def normalize_doi(doi: str | None) -> str:
    if not doi:
        return ""
    value = doi.lower().strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix):]
    return value.rstrip("/")


def record_key(record: Dict[str, Any]) -> str | None:
    openalex = record.get("openalex_id")
    if openalex:
        return f"openalex:{openalex}"
    doi = normalize_doi(record.get("doi"))
    if doi:
        return f"doi:{doi}"
    title = (record.get("title") or "").strip().lower()
    if title:
        return f"title:{title}"
    return None


def deduplicate(records: Iterable[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, List[str]]]:
    """Deduplicate records and return (unique_records, key_to_frames)."""
    unique: Dict[str, Dict[str, Any]] = {}
    frames: Dict[str, List[str]] = {}
    for record in records:
        key = record_key(record)
        if not key:
            continue
        if key not in unique:
            unique[key] = record
            frames[key] = []
        frames[key].append(record.get("_frame", "unknown"))
    return list(unique.values()), frames


def target_value_regex() -> re.Pattern[str]:
    return re.compile(
        r"(?:1[,.\s]?400|1400|2[,.\s]?500|2500|1[,.\s]?620|1620)"
        r"\s*(?:cases?)?(?:\s+of\s+pneumonia)?\s*(?:per\s*100[,\s]?000|/100[,\s]?000)",
        re.IGNORECASE,
    )


def classify_metadata(record: Dict[str, Any], abstract: str) -> str:
    text = ((record.get("title") or "") + " " + abstract).lower()
    if target_value_regex().search(text):
        return "CANDIDATE_NUMERICAL_REUSE"
    if "pneumonia" in text or "unicef" in text:
        return "CANDIDATE_RELEVANT"
    return "EXCLUDED_NOT_RELEVANT"


def build_registry_rows(
    records: Iterable[Dict[str, Any]],
    prior_known_dois: set[str] | None = None,
) -> List[Dict[str, Any]]:
    prior_known_dois = prior_known_dois or set()
    unique, frames = deduplicate(records)
    rows: List[Dict[str, Any]] = []
    for index, record in enumerate(unique, 1):
        doi = normalize_doi(record.get("doi"))
        prior = doi in {normalize_doi(d) for d in prior_known_dois}
        abstract = reconstruct_abstract(record.get("abstract_inverted_index"))
        status = "PRIOR_KNOWN_CASE" if prior else classify_metadata(record, abstract)
        rows.append(
            {
                "record_id": f"R{index:04d}",
                "openalex_id": record.get("openalex_id"),
                "doi": record.get("doi"),
                "title": record.get("title"),
                "year": record.get("publication_year") or record.get("year"),
                "frames": "; ".join(sorted(set(frames[record_key(record)]))),
                "duplicate": len(set(frames[record_key(record)])) > 1,
                "prior_known_case": prior,
                "status": status,
            }
        )
    return rows


def _fetch_openalex_works(query: str, per_page: int, mailto: str) -> List[Dict[str, Any]]:
    params = {
        "search": query,
        "filter": "publication_year:2018-2026",
        "per-page": str(per_page),
        "mailto": mailto,
    }
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": f"codex-research/1.0 (mailto:{mailto})"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.load(response)
    out: List[Dict[str, Any]] = []
    for work in data.get("results", []):
        primary = work.get("primary_location") or {}
        out.append(
            {
                "openalex_id": work.get("id"),
                "doi": work.get("doi"),
                "title": work.get("title"),
                "publication_year": work.get("publication_year"),
                "type": work.get("type"),
                "abstract_inverted_index": work.get("abstract_inverted_index"),
                "is_oa": (work.get("open_access") or {}).get("is_oa"),
                "oa_url": (work.get("open_access") or {}).get("oa_url"),
                "landing_page_url": primary.get("landing_page_url"),
                "_frame": "B",
            }
        )
    return out


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch and de-duplicate OpenAlex discovery records.")
    parser.add_argument("--query", action="append", required=True, help="OpenAlex search query; repeat for multiple queries.")
    parser.add_argument("--per-page", type=int, default=25)
    parser.add_argument("--mailto", default="research@example.com")
    parser.add_argument("--out", required=True, help="Output JSON path.")
    args = parser.parse_args(argv)

    all_records: List[Dict[str, Any]] = []
    for query in args.query:
        all_records.extend(_fetch_openalex_works(query, args.per_page, args.mailto))
    unique, _ = deduplicate(all_records)
    Path(args.out).write_text(json.dumps(unique, indent=2), encoding="utf-8")
    print(f"wrote {len(unique)} unique records to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
