import csv
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from discovery import build_registry_rows, deduplicate, record_key
from extraction import build_evidence_rows, extract_contexts, provisional_dimensions
from gates import denominator_summary, gate_decision


def _fixture_path(name):
    return Path(__file__).resolve().parent.parent / "fixtures" / name


def test_deduplicate_uses_first_id():
    records = [
        {"openalex_id": "W1", "title": "A", "_frame": "A"},
        {"doi": "https://doi.org/10.0000/x", "title": "A", "_frame": "B"},
    ]
    unique, frames = deduplicate(records)
    assert len(unique) == 2


def test_build_registry_flags_prior_known_and_status():
    records = json.loads(_fixture_path("sample_records.json").read_text(encoding="utf-8"))
    rows = build_registry_rows(records, prior_known_dois={"10.0000/syn1"})
    by_title = {r["title"]: r for r in rows}
    assert by_title["Synthetic preserved childhood pneumonia citation"]["status"] == "PRIOR_KNOWN_CASE"
    assert by_title["Synthetic irrelevant record"]["status"] == "EXCLUDED_NOT_RELEVANT"


def test_extract_and_classify_preserved_context():
    text = _fixture_path("passages/SYN1.txt").read_text(encoding="utf-8")
    contexts = extract_contexts(text)
    assert contexts
    assert provisional_dimensions(contexts) == ["P0"]


def test_extract_builds_evidence_rows():
    registry = _fixture_path("..") / "templates" / "record_registry.csv"
    # Write a tiny registry for the synthetic passage.
    registry_tmp = Path(__file__).resolve().parent / "synthetic_registry.csv"
    with open(registry_tmp, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["record_id", "doi", "title"])
        writer.writerow(["SYN1", "10.0000/syn1", "Synthetic preserved childhood pneumonia citation"])
    rows = build_evidence_rows(_fixture_path("passages"), registry_tmp)
    assert any(r["record_id"] == "SYN1" and r["provisional_dimensions"] == "P0" for r in rows)
    registry_tmp.unlink()


def test_gate_pivots_without_independent_drift():
    summary = {
        "total_records": 10,
        "prior_known_cases": 1,
        "independent_records": 9,
        "independent_verified_reuse": 3,
        "independent_verified_drift": 0,
        "independent_verified_preserved": 3,
        "human_reliability_assessed": 0,
    }
    decision = gate_decision(summary)
    assert decision["verdict"] == "PIVOT"
    assert decision["reliability"] == "HUMAN_RELIABILITY_PENDING"


def test_denominator_excludes_machine_prior_known_and_duplicate_rows():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        registry = root / "registry.csv"
        evidence = root / "evidence.csv"
        registry.write_text(
            "record_id,prior_known_case\nR1,False\nR2,False\nK1,True\n",
            encoding="utf-8",
        )
        evidence.write_text(
            "record_id,source_cited,provisional_dimensions,reviewer_status\n"
            "R1,True,D1,machine_provisional\n"
            "K1,True,D1,human_verified\n"
            "R2,False,D1,human_verified\n"
            "R1,True,D1,human_verified\n"
            "R1,True,D2,human_verified\n",
            encoding="utf-8",
        )

        summary = denominator_summary(registry, evidence)
        assert summary["independent_records"] == 2
        assert summary["independent_verified_reuse"] == 1
        assert summary["independent_verified_drift"] == 1
        assert gate_decision(summary)["verdict"] == "STOP"


def test_denominator_requires_human_verified_source_match():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        registry = root / "registry.csv"
        evidence = root / "evidence.csv"
        registry.write_text("record_id,prior_known_case\nR1,False\n", encoding="utf-8")
        evidence.write_text(
            "record_id,source_cited,provisional_dimensions,reviewer_status\n"
            "R1,True,P0,machine_provisional\n"
            "R1,False,P0,human_verified\n",
            encoding="utf-8",
        )

        summary = denominator_summary(registry, evidence)
        assert summary["independent_verified_reuse"] == 0
        assert summary["independent_verified_preserved"] == 0
