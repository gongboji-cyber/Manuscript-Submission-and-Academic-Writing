#!/usr/bin/env python3
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MATERIALS = ROOT.parent / "materials"
SCRIPT = ROOT / "convert_unitrows.py"
commands, checks = [], []
inputs = [MATERIALS / name for name in ("input.unitrows", "duplicate.unitrows", "format.md", "cases.json")]
def hashes():
    return {str(path.relative_to(ROOT.parent)): hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs}
before = hashes()
def run(source, target):
    command = [sys.executable, "-B", str(SCRIPT), str(source), str(target)]
    result = subprocess.run(command, capture_output=True, text=True)
    commands.append({"argv": command, "exit_code": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()})
    return result

def check(name, condition):
    checks.append({"name": name, "passed": bool(condition)})
    if not condition:
        raise AssertionError(name)

result = run(MATERIALS / "input.unitrows", ROOT / "verified.csv")
check("provided input: successful execution", result.returncode == 0)
with (ROOT / "input.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.reader(handle))
check("exact headers, IDs, unit conversion and NA", rows == [["id", "value_cm"], ["01", "1"], ["02", "NA"], ["03", "2.5"]])
check("independent second conversion matches", (ROOT / "input.csv").read_bytes() == (ROOT / "verified.csv").read_bytes())
result = run(MATERIALS / "duplicate.unitrows", ROOT / "duplicate_checked.csv")
check("provided duplicate: exit 2 and no output", result.returncode == 2 and not (ROOT / "duplicate_checked.csv").exists() and not (ROOT / "duplicate.csv").exists())
invalid = {
    "bad_magic": "#UNITROWS/2\nid|value_mm\n01|10\n",
    "bad_columns_header": "#UNITROWS/1\nid|value_cm\n01|10\n",
    "wrong_columns": "#UNITROWS/1\nid|value_mm\n01|10|extra\n",
    "empty_id": "#UNITROWS/1\nid|value_mm\n|10\n",
    "blank_row": "#UNITROWS/1\nid|value_mm\n01|10\n\n",
    "nan": "#UNITROWS/1\nid|value_mm\n01|NaN\n",
    "inf": "#UNITROWS/1\nid|value_mm\n01|Infinity\n",
    "negative_inf": "#UNITROWS/1\nid|value_mm\n01|-inf\n",
    "lowercase_na": "#UNITROWS/1\nid|value_mm\n01|na\n",
    "na_space": "#UNITROWS/1\nid|value_mm\n01|NA \n",
    "empty_value": "#UNITROWS/1\nid|value_mm\n01|\n",
}
for name, content in invalid.items():
    source, target = ROOT / (name + ".unitrows"), ROOT / (name + ".csv")
    source.write_text(content, encoding="utf-8")
    result = run(source, target)
    check(name + ": rejected without CSV", result.returncode == 2 and not target.exists())
source = ROOT / "numeric_edges.unitrows"
source.write_text("#UNITROWS/1\nid|value_mm\n0001|-5\n0|0\nscientific|1e2\ncomma,id|25\n spaced id |NA\nprecise|123456789012345678901234567890.1\n", encoding="utf-8")
result = run(source, ROOT / "numeric_edges.csv")
check("numeric and quoted ID edges: successful execution", result.returncode == 0)
with (ROOT / "numeric_edges.csv").open(newline="", encoding="utf-8") as handle:
    edge_rows = list(csv.reader(handle))
check("negative, zero, exponent, comma and spaced IDs, exact decimal precision", edge_rows[1:] == [["0001", "-0.5"], ["0", "0"], ["scientific", "10"], ["comma,id", "2.5"], [" spaced id ", "NA"], ["precise", "12345678901234567890123456789.01"]])
original_output = (ROOT / "input.csv").read_bytes()
result = run(MATERIALS / "input.unitrows", ROOT / "input.csv")
check("existing output: rejected and unchanged", result.returncode == 2 and (ROOT / "input.csv").read_bytes() == original_output)
after = hashes()
check("all supplied material hashes unchanged during checks", before == after)
report = {"python_version": sys.version, "checks": checks, "commands": commands, "input_sha256_before": before, "input_sha256_after": after, "script_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(), "csv_sha256": hashlib.sha256((ROOT / "input.csv").read_bytes()).hexdigest()}
(ROOT / "checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"checks_passed": len(checks), "checks_failed": 0, "main_csv": rows}, ensure_ascii=False))
