#!/usr/bin/env python3
"""Validate gate-ledger structure and the logical burden of GO/STOP decisions.

This catches missing gates, unsubstantiated PASS, premature GO, and unsupported
G1-based STOP. It CANNOT verify cited papers, data access, or scientific truth.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

GATES = ("G0", "G1", "G2", "G3", "G4", "G5")
STATUSES = {"PASS", "FAIL", "UNKNOWN", "NOT_TESTED"}
DECISIONS = {
    "EXPLORE_ONLY",
    "HOLD_NEED_EVIDENCE",
    "HOLD_DATA_ACCESS",
    "GO_MINIMAL_PILOT",
    "GO_FULL_STUDY",
    "STOP",
}
PILOT_STATUSES = {"NOT_RUN", "RUN", "INVALID"}
READING_LEVELS = {
    "not_applicable",
    "metadata-only",
    "abstract-read",
    "methods-results-read",
    "fulltext-supp-reviewed",
}
FIELDS = (
    "topic_id",
    "gate",
    "status",
    "evidence_refs",
    "reading_level",
    "blocker",
    "unlock",
    "decision",
    "pilot_status",
)


def validate_rows(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    grouped: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)

    if not rows:
        return ["Ledger has no rows"]

    for line, row in enumerate(rows, start=2):
        topic = (row.get("topic_id") or "").strip()
        gate = (row.get("gate") or "").strip()
        status = (row.get("status") or "").strip()
        refs = (row.get("evidence_refs") or "").strip()
        reading = (row.get("reading_level") or "").strip()
        decision = (row.get("decision") or "").strip()
        pilot = (row.get("pilot_status") or "").strip()
        label = f"row {line} ({topic or 'MISSING_ID'}/{gate or 'MISSING_GATE'})"

        if not topic:
            errors.append(f"{label}: topic_id required")
            continue
        if gate not in GATES:
            errors.append(f"{label}: unknown gate")
            continue
        if gate in grouped[topic]:
            errors.append(f"{label}: duplicate gate")
            continue
        grouped[topic][gate] = row
        if status not in STATUSES:
            errors.append(f"{label}: invalid status {status!r}")
        if decision not in DECISIONS:
            errors.append(f"{label}: invalid decision {decision!r}")
        if pilot not in PILOT_STATUSES:
            errors.append(f"{label}: invalid pilot_status {pilot!r}")
        if reading not in READING_LEVELS:
            errors.append(f"{label}: invalid reading_level {reading!r}")
        if status in {"PASS", "FAIL"} and not refs:
            errors.append(f"{label}: PASS/FAIL requires traceable evidence_refs")
        if gate == "G1" and status in {"PASS", "FAIL"}:
            if reading != "fulltext-supp-reviewed":
                errors.append(f"{label}: G1 PASS/FAIL requires fulltext-supp-reviewed")
        if status in {"UNKNOWN", "NOT_TESTED"} and not (row.get("blocker") or "").strip():
            errors.append(f"{label}: unknown/untested gate needs blocker")
        if status in {"UNKNOWN", "NOT_TESTED"} and not (row.get("unlock") or "").strip():
            errors.append(f"{label}: unknown/untested gate needs unlock")

    for topic, gates in grouped.items():
        missing = sorted(set(GATES) - set(gates))
        if missing:
            errors.append(f"{topic}: missing gates: {', '.join(missing)}")
            continue
        decisions = {g["decision"].strip() for g in gates.values()}
        pilots = {g["pilot_status"].strip() for g in gates.values()}
        if len(decisions) != 1:
            errors.append(f"{topic}: contradictory decisions {sorted(decisions)}")
            continue
        if len(pilots) != 1:
            errors.append(f"{topic}: contradictory pilot statuses {sorted(pilots)}")
            continue
        decision = next(iter(decisions))
        pilot = next(iter(pilots))
        all_early_pass = all(gates[g]["status"].strip() == "PASS" for g in GATES[:5])
        if decision in {"GO_MINIMAL_PILOT", "GO_FULL_STUDY"} and not all_early_pass:
            errors.append(f"{topic}: GO requires G0-G4 all PASS")
        if decision == "GO_FULL_STUDY":
            if gates["G5"]["status"].strip() != "PASS":
                errors.append(f"{topic}: GO_FULL_STUDY requires G5 PASS")
            if pilot != "RUN":
                errors.append(f"{topic}: GO_FULL_STUDY requires pilot_status RUN")
        if decision == "GO_MINIMAL_PILOT" and pilot == "INVALID":
            errors.append(f"{topic}: invalid pilot cannot justify GO_MINIMAL_PILOT")
        if decision == "STOP":
            failed = [g for g in GATES[:5] if gates[g]["status"].strip() == "FAIL"]
            if not failed:
                errors.append(f"{topic}: STOP requires evidenced FAIL in G0-G4")
        if decision == "HOLD_DATA_ACCESS":
            gate3 = gates["G3"]
            if gate3["status"].strip() == "PASS":
                errors.append(f"{topic}: access HOLD contradicts G3 PASS")
            if "ACCESS_BLOCKED" not in (gate3.get("blocker") or ""):
                errors.append(f"{topic}: HOLD_DATA_ACCESS needs G3 blocker ACCESS_BLOCKED")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="CSV gate ledger with one row per topic/gate")
    args = parser.parse_args()
    try:
        with args.csv_file.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            missing = set(FIELDS) - set(reader.fieldnames or ())
            if missing:
                print(f"ERROR missing columns: {', '.join(sorted(missing))}", file=sys.stderr)
                return 2
            rows = list(reader)
    except (OSError, csv.Error) as exc:
        print(f"ERROR reading {args.csv_file}: {exc}", file=sys.stderr)
        return 2

    errors = validate_rows(rows)
    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        print(f"{len(errors)} validation problem(s)", file=sys.stderr)
        return 1
    print(f"PASS {len(rows)} gate rows / {len({r['topic_id'] for r in rows})} topics")
    print("Note: this validates ledger logic, not actual sources or scientific merit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
