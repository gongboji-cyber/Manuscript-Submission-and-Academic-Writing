#!/usr/bin/env python3
"""Convert this case's UNITROWS/1 format; standard library only."""
import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import sys

OUTPUT_ROOT = Path(__file__).resolve().parent
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")

def convert(source, destination):
    destination = Path(destination).resolve()
    if destination.parent != OUTPUT_ROOT:
        raise ValueError("output must be directly inside the script's output directory")
    if Path(source).resolve() == destination:
        raise ValueError("input must not be overwritten")
    lines = Path(source).read_text(encoding="utf-8").splitlines()
    if len(lines) < 2 or lines[0] != "#UNITROWS/1" or lines[1] != "id|value_mm":
        raise ValueError("invalid UNITROWS/1 header")
    rows, seen = [], set()
    for line_number, line in enumerate(lines[2:], start=3):
        fields = line.split("|")
        if len(fields) != 2:
            raise ValueError(f"line {line_number}: expected exactly two columns")
        identifier, raw = fields
        if not identifier:
            raise ValueError(f"line {line_number}: empty ID")
        if identifier in seen:
            raise ValueError(f"line {line_number}: duplicate ID {identifier!r}")
        seen.add(identifier)
        if raw == "NA":
            value_cm = "NA"
        else:
            if not NUMBER.fullmatch(raw):
                raise ValueError(f"line {line_number}: invalid or non-finite number")
            try:
                value = Decimal(raw)
            except InvalidOperation as exc:
                raise ValueError(f"line {line_number}: invalid number") from exc
            if not value.is_finite():
                raise ValueError(f"line {line_number}: non-finite number")
            sign, digits, exponent = value.as_tuple()
            # Shift the decimal exponent; avoid floating-point or context rounding.
            value_cm = format(Decimal((sign, digits, exponent - 1)), "f")
            if "." in value_cm:
                value_cm = value_cm.rstrip("0").rstrip(".")
        rows.append((identifier, value_cm))
    # Validate all rows first; errors above cannot leave a partial CSV.
    with destination.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("id", "value_cm"))
        writer.writerows(rows)
    return len(rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    try:
        count = convert(args.input, args.output)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Converted {count} rows to {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
