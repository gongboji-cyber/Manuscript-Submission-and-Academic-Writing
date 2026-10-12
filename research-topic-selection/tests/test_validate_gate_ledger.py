"""Regression tests for decision consistency, including positive controls."""

from __future__ import annotations

import csv
import sys
import unittest
from copy import deepcopy
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from validate_gate_ledger import validate_rows  # noqa: E402


class GateLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with (SKILL_DIR / "assets" / "gate-ledger-example.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            cls.base = list(csv.DictReader(handle))

    def get_topic(self, topic: str) -> list[dict[str, str]]:
        return deepcopy([row for row in self.base if row["topic_id"] == topic])

    def test_positive_pilot_and_hold_and_evidenced_stop(self) -> None:
        self.assertEqual(validate_rows(deepcopy(self.base)), [])

    def test_false_go_when_missing_independent_data(self) -> None:
        rows = self.get_topic("SYNTH_GO_PILOT")
        for row in rows:
            if row["gate"] == "G3":
                row["status"] = "UNKNOWN"
                row["evidence_refs"] = ""
                row["blocker"] = "JOIN_UNKNOWN"
                row["unlock"] = "Obtain joined independent reference"
        self.assertTrue(any("G0-G4" in err for err in validate_rows(rows)))

    def test_false_go_on_unread_competitor(self) -> None:
        rows = self.get_topic("SYNTH_GO_PILOT")
        for row in rows:
            if row["gate"] == "G1":
                row["reading_level"] = "abstract-read"
        self.assertTrue(any("fulltext-supp-reviewed" in err for err in validate_rows(rows)))

    def test_false_stop_based_on_title_similarity(self) -> None:
        rows = self.get_topic("SYNTH_STOP")
        for row in rows:
            if row["gate"] == "G1":
                row["reading_level"] = "metadata-only"
        self.assertTrue(any("fulltext-supp-reviewed" in err for err in validate_rows(rows)))

    def test_stop_without_failed_gate(self) -> None:
        rows = self.get_topic("SYNTH_HOLD")
        for row in rows:
            row["decision"] = "STOP"
        self.assertTrue(any("STOP requires" in err for err in validate_rows(rows)))

    def test_full_study_requires_actual_pilot(self) -> None:
        rows = self.get_topic("SYNTH_GO_PILOT")
        for row in rows:
            row["decision"] = "GO_FULL_STUDY"
        errors = validate_rows(rows)
        self.assertTrue(any("G5 PASS" in err for err in errors))
        self.assertTrue(any("pilot_status RUN" in err for err in errors))

    def test_valid_full_study_positive_control(self) -> None:
        rows = self.get_topic("SYNTH_GO_PILOT")
        for row in rows:
            row["decision"] = "GO_FULL_STUDY"
            row["pilot_status"] = "RUN"
            if row["gate"] == "G5":
                row["status"] = "PASS"
                row["evidence_refs"] = "SYNTH-E5-RESULTS"
                row["blocker"] = ""
                row["unlock"] = ""
        self.assertEqual(validate_rows(rows), [])

    def test_access_hold_is_not_scientific_stop(self) -> None:
        rows = self.get_topic("SYNTH_HOLD")
        for row in rows:
            row["decision"] = "HOLD_DATA_ACCESS"
            if row["gate"] == "G3":
                row["blocker"] = "ACCESS_BLOCKED: HTTP 403"
        self.assertEqual(validate_rows(rows), [])

    def test_missing_gate_or_conflicting_decisions(self) -> None:
        rows = self.get_topic("SYNTH_GO_PILOT")
        self.assertTrue(any("missing gates" in err for err in validate_rows(rows[:-1])))
        rows[0]["decision"] = "STOP"
        self.assertTrue(any("contradictory" in err for err in validate_rows(rows)))

    def test_unsubstantiated_pass(self) -> None:
        rows = self.get_topic("SYNTH_GO_PILOT")
        rows[0]["evidence_refs"] = ""
        self.assertTrue(any("evidence_refs" in err for err in validate_rows(rows)))


if __name__ == "__main__":
    unittest.main()
