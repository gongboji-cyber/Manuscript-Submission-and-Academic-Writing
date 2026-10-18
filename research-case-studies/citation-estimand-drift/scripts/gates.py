#!/usr/bin/env python3
"""Denominator and GO/PIVOT/STOP decision gates."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List


def denominator_summary(registry_path: Path, evidence_path: Path) -> Dict[str, int]:
    with open(registry_path, encoding="utf-8-sig") as handle:
        registry = list(csv.DictReader(handle))
    evidence_rows: List[Dict[str, str]] = []
    if evidence_path.exists() and evidence_path.stat().st_size:
        with open(evidence_path, encoding="utf-8-sig") as handle:
            evidence_rows = list(csv.DictReader(handle))

    independent = [r for r in registry if r.get("prior_known_case") != "True"]
    verified = [r for r in evidence_rows if r.get("provisional_dimensions") != "U"]
    drift = [r for r in verified if "D" in r.get("provisional_dimensions", "")]
    preserved = [r for r in verified if r.get("provisional_dimensions") == "P0"]
    return {
        "total_records": len(registry),
        "prior_known_cases": len(registry) - len(independent),
        "independent_records": len(independent),
        "independent_verified_reuse": len(verified),
        "independent_verified_drift": len(drift),
        "independent_verified_preserved": len(preserved),
        "human_reliability_assessed": 0,
    }


def gate_decision(summary: Dict[str, int]) -> Dict[str, str]:
    if summary["human_reliability_assessed"] == 0:
        reliability = "HUMAN_RELIABILITY_PENDING"
    else:
        reliability = "RELIABILITY_ASSESSED"
    if summary["independent_verified_reuse"] < 3:
        verdict = "STOP"
        reason = "insufficient_verified_independent_evidence"
    elif summary["independent_verified_drift"] == 0:
        verdict = "PIVOT"
        reason = "no_independently_verified_drift"
    else:
        verdict = "GO"
        reason = "independent_drift_verified"
    return {"verdict": verdict, "reason": reason, "reliability": reliability}


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute denominator and gate decision.")
    parser.add_argument("--registry", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    summary = denominator_summary(Path(args.registry), Path(args.evidence))
    summary.update(gate_decision(summary))
    Path(args.out).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
