#!/usr/bin/env python3
"""Executable boundary checks; all derived data stays beside this script."""
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path
from convert_unitrows import convert

ROOT = Path(__file__).resolve().parent
MATERIALS = ROOT.parent / "materials"
results = []
source_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (MATERIALS / "input.unitrows", MATERIALS / "duplicate.unitrows", MATERIALS / "format.md")}


def check(label, assertion):
    assert assertion, label
    results.append({"check": label, "status": "passed"})


with (ROOT / "input.csv").open(encoding="utf-8", newline="") as handle:
    actual = list(csv.reader(handle))
check("CSV header and exactly 3 rows", actual[0] == ["id", "value_cm"] and len(actual) == 4)
check("leading zero IDs preserved", [r[0] for r in actual[1:]] == ["01", "02", "03"])
check("10 mm equals 1 cm and 25 mm equals 2.5 cm", Decimal(actual[1][1]) == Decimal("1") and Decimal(actual[3][1]) == Decimal("2.5"))
check("NA remains NA, distinct from zero", actual[2][1] == "NA")
check("duplicate CLI did not create output", not (ROOT / "duplicate.csv").exists())

edge = ROOT / "boundary.unitrows"
edge.write_text("#UNITROWS/1\nid|value_mm\n000|0\nneg|-5\nfraction|.5\nexponent|1e2\ncomma,id|0.123456789012345678901234567890123456789\n", encoding="utf-8")
convert(edge, ROOT / "boundary.csv")
with (ROOT / "boundary.csv").open(encoding="utf-8", newline="") as handle:
    boundary = list(csv.reader(handle))[1:]
check("zero, negative, fractional, exponent and CSV quoting", [r[0] for r in boundary] == ["000", "neg", "fraction", "exponent", "comma,id"] and [Decimal(r[1]) for r in boundary[:4]] == list(map(Decimal, ["0", "-0.5", "0.05", "10"])))
check("long decimal is converted without float rounding", boundary[-1][1] == "0.0123456789012345678901234567890123456789")

reject_cases = {
    "wrong version": "#UNITROWS/2\nid|value_mm\na|1\n",
    "wrong column header": "#UNITROWS/1\nid|value_cm\na|1\n",
    "too many columns": "#UNITROWS/1\nid|value_mm\na|1|2\n",
    "too few columns": "#UNITROWS/1\nid|value_mm\na\n",
    "blank row": "#UNITROWS/1\nid|value_mm\n\n",
    "empty ID": "#UNITROWS/1\nid|value_mm\n|1\n",
    "duplicate ID": (MATERIALS / "duplicate.unitrows").read_text(encoding="utf-8"),
    "NaN": "#UNITROWS/1\nid|value_mm\na|NaN\n",
    "infinity": "#UNITROWS/1\nid|value_mm\na|inf\n",
    "negative infinity": "#UNITROWS/1\nid|value_mm\na|-Infinity\n",
    "lowercase missing": "#UNITROWS/1\nid|value_mm\na|na\n",
    "padded missing": "#UNITROWS/1\nid|value_mm\na| NA\n",
    "empty value": "#UNITROWS/1\nid|value_mm\na|\n",
}
for index, (label, content) in enumerate(reject_cases.items()):
    source = ROOT / f"reject_{index}.unitrows"
    target = ROOT / f"reject_{index}.csv"
    source.write_text(content, encoding="utf-8")
    target.write_text("unchanged sentinel\n", encoding="utf-8")
    try:
        convert(source, target)
    except ValueError as error:
        check("reject " + label + " and preserve existing output", target.read_text(encoding="utf-8") == "unchanged sentinel\n")
        results[-1]["error"] = str(error)
    else:
        raise AssertionError("accepted " + label)

try:
    convert(edge, edge)
except ValueError:
    check("input overwrite forbidden", edge.read_text(encoding="utf-8").startswith("#UNITROWS/1\n"))
else:
    raise AssertionError("input overwrite accepted")

check("supplied inputs unchanged during boundary checks", all(hashlib.sha256((MATERIALS / name).read_bytes()).hexdigest() == digest for name, digest in source_hashes.items()))
(ROOT / "validation.json").write_text(json.dumps({"checks": results, "passed": len(results), "source_sha256": source_hashes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"passed": len(results), "failed": 0, "checks": results}, ensure_ascii=False))
