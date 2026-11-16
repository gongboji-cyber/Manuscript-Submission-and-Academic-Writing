"""Replay synthetic converter artifacts in disposable directories, without deps.

Run: python -B evals/workflow-entry/replay_converters.py
This does not rerun a model or validate medical/statistical conclusions.
"""
import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def replay(variant, directory):
    materials, output = directory / "materials", directory / "output"
    shutil.copytree(ROOT / "materials", materials)
    output.mkdir()
    check = "check_conversion.py" if variant == "a" else "check_unitrows.py"
    for name in ("convert_unitrows.py", check):
        shutil.copyfile(ROOT / "results" / variant / name, output / name)
    commands = []

    def run(args):
        command = [sys.executable, "-B", *map(str, args)]
        process = subprocess.run(command, text=True, capture_output=True, timeout=30)
        commands.append(dict(argv=command, exit_code=process.returncode,
                             stdout=process.stdout, stderr=process.stderr))
        return process

    normal = run([output / "convert_unitrows.py", materials / "input.unitrows",
                  output / "input.csv"])
    duplicate = run([output / "convert_unitrows.py", materials / "duplicate.unitrows",
                     output / "duplicate.csv"])
    if normal.returncode != 0 or duplicate.returncode == 0 or (output / "duplicate.csv").exists():
        raise AssertionError("normal conversion or duplicate refusal failed")
    with (output / "input.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if ([r["id"] for r in rows] != ["01", "02", "03"] or
            [float(rows[0]["value_cm"]), rows[1]["value_cm"],
             float(rows[2]["value_cm"])] != [1, "NA", 2.5]):
        raise AssertionError("IDs, missing value or conversion changed")
    boundary = run([output / check])
    if boundary.returncode != 0:
        raise AssertionError(boundary.stderr)
    return dict(variant=variant, csv_rows=rows, commands=commands)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="workflow-entry-replay-") as temporary:
        results = [replay(v, Path(temporary) / v) for v in "ab"]
    print(json.dumps(dict(python=sys.version, scope="converter replay only",
                          results=results), ensure_ascii=False, indent=2))
