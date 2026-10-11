#!/usr/bin/env python3
"""Convert the case-specific UNITROWS/1 format; no external standard assumed."""
import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re

NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z")


def convert(source, destination):
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError("input must not be overwritten")
    lines = source.read_text(encoding="utf-8").splitlines()
    if len(lines) < 2 or lines[0] != "#UNITROWS/1" or lines[1] != "id|value_mm":
        raise ValueError("invalid UNITROWS/1 header")
    rows, ids = [], set()
    for line_number, line in enumerate(lines[2:], start=3):
        fields = line.split("|")
        if len(fields) != 2:
            raise ValueError(f"line {line_number}: expected exactly two columns")
        identifier, value = fields
        if identifier == "":
            raise ValueError(f"line {line_number}: empty ID")
        if identifier in ids:
            raise ValueError(f"line {line_number}: duplicate ID {identifier!r}")
        ids.add(identifier)
        if value == "NA":
            converted = "NA"
        else:
            if NUMBER.fullmatch(value) is None:
                raise ValueError(f"line {line_number}: expected finite real or exact NA")
            try:
                number = Decimal(value)
            except InvalidOperation as error:
                raise ValueError(f"line {line_number}: invalid number") from error
            if not number.is_finite():
                raise ValueError(f"line {line_number}: non-finite number")
            # Change the exponent exactly, without context rounding or float coercion.
            sign, digits, exponent = number.as_tuple()
            converted = str(Decimal((sign, digits, exponent - 1)))
        rows.append((identifier, converted))
    # Validate the whole source before opening the output; errors leave no partial CSV.
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(("id", "value_cm"))
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        count = convert(args.input, args.output)
    except (ValueError, OSError) as error:
        parser.exit(2, f"ERROR: {error}\n")
    print(f"Converted {count} rows to {args.output.name}")
