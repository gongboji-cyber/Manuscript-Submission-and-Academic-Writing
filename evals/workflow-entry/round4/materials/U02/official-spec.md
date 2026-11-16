# MEDFMTX interchange format 1.2

Status: final synthetic specification
Version: 1.2
Issued: 2026-06-15

## Section 1 — Header

The first line MUST be exactly `MEDFMTX 1.2`.

## Section 2 — Records

Each later non-empty line is `ID|VALUE`. ID MUST contain only uppercase ASCII letters, digits, or underscore and MUST be unique. VALUE is either `NA` or a finite decimal number from 0 through 100 inclusive.

## Section 3 — JSON mapping

Produce one JSON object with `format` equal to `MEDFMTX 1.2` and `records` in source order. Decimal values map to JSON numbers; `NA` maps to JSON null. Format validation says nothing about the scientific meaning or correctness of a value.
