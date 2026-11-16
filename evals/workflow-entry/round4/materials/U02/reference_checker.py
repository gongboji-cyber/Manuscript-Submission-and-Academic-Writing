#!/usr/bin/env python3
"""Reference checker for the synthetic MEDFMTX 1.2 evaluation fixture."""

import argparse
import json
import math
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

ID_RE = re.compile(r"^[A-Z0-9_]+$")


def convert(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "MEDFMTX 1.2":
        raise ValueError("invalid header")
    seen = set()
    records = []
    for line_number, line in enumerate(lines[1:], start=2):
        if not line:
            continue
        if line.count("|") != 1:
            raise ValueError(f"line {line_number}: expected one separator")
        record_id, raw_value = line.split("|", 1)
        if not ID_RE.fullmatch(record_id):
            raise ValueError(f"line {line_number}: invalid ID")
        if record_id in seen:
            raise ValueError(f"line {line_number}: duplicate ID {record_id}")
        seen.add(record_id)
        if raw_value == "NA":
            value = None
        else:
            try:
                decimal_value = Decimal(raw_value)
            except InvalidOperation as exc:
                raise ValueError(f"line {line_number}: invalid decimal") from exc
            value = float(decimal_value)
            if not math.isfinite(value) or not 0 <= value <= 100:
                raise ValueError(f"line {line_number}: value outside 0..100")
            if decimal_value == decimal_value.to_integral():
                value = int(decimal_value)
        records.append({"id": record_id, "value": value})
    return {"format": "MEDFMTX 1.2", "records": records}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(convert(args.input), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
