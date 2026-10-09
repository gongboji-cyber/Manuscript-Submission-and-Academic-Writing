#!/usr/bin/env python3
"""Original narrow CSV audit. Counts only; no clinical validity certification."""
import argparse
import csv
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def audit(data, config):
    cfg = json.loads(Path(config).read_text(encoding='utf-8'))
    allowed = {'unit_col', 'row_key', 'split_col', 'numeric_cols', 'paired_cols', 'bounds', 'missing_tokens'}
    if not isinstance(cfg, dict) or set(cfg) - allowed:
        raise ValueError('Unsupported config fields')
    if not isinstance(cfg.get('unit_col'), str) or not cfg['unit_col']:
        raise ValueError('unit_col must explicitly name the independent unit')
    keys = cfg.get('row_key')
    if not isinstance(keys, list) or not keys or len(set(keys)) != len(keys) or not all(isinstance(x, str) and x for x in keys):
        raise ValueError('row_key must be a nonempty unique list of column names')
    for role in ('numeric_cols', 'paired_cols', 'missing_tokens'):
        vals = cfg.get(role, [])
        if not isinstance(vals, list) or not all(isinstance(v, str) for v in vals):
            raise ValueError(f'{role} must be a list of strings')
    pair = cfg.get('paired_cols', [])
    if pair and (len(pair) != 2 or pair[0] == pair[1]):
        raise ValueError('paired_cols must name two distinct columns')
    split = cfg.get('split_col')
    if split is not None and (not isinstance(split, str) or not split):
        raise ValueError('split_col must be a column name or null')
    bounds = cfg.get('bounds', {})
    if not isinstance(bounds, dict):
        raise ValueError('bounds must be an object')
    for col, limits in bounds.items():
        if col not in cfg.get('numeric_cols', []) or not isinstance(limits, list) or len(limits) != 2:
            raise ValueError('bounds require a configured numeric column and [lower, upper]')
        if not all(isinstance(v, (float, int)) and not isinstance(v, bool) and np.isfinite(v) for v in limits) or limits[0] > limits[1]:
            raise ValueError('bounds must be finite and ordered')
    with Path(data).open(encoding="utf-8-sig", newline="") as f:
        header = next(csv.reader(f), [])
    if not header or len(header) != len(set(header)) or any(not c for c in header):
        raise ValueError("CSV requires nonempty unique column headers")
    df = pd.read_csv(data, dtype=str, keep_default_na=False)
    needed = set(keys + [cfg['unit_col']] + cfg.get('numeric_cols', []) + pair + ([split] if split else []))
    if needed - set(df.columns):
        raise ValueError('Missing configured columns: ' + ', '.join(sorted(needed - set(df.columns))))
    # Preserve identifiers, including leading zeroes; don't silently strip/canonicalize.
    tokens = set(cfg.get('missing_tokens', [''])) | {''}
    missing = df.isin(tokens)
    numeric = {}
    values = {}
    for col in set(cfg.get('numeric_cols', []) + pair):
        v = pd.to_numeric(df[col].mask(missing[col]), errors='coerce')
        arr = v.to_numpy(dtype=float)
        nonfinite = np.isinf(arr)
        invalid = (~missing[col]) & v.isna()
        info = {'missing': int(missing[col].sum()), 'invalid_numeric': int(invalid.sum()), 'infinite': int(nonfinite.sum())}
        if col in bounds:
            lo, hi = bounds[col]
            info['outside_bounds'] = int(((v < lo) | (v > hi)).sum())
        numeric[col] = info
        values[col] = v
    valid_unit = ~missing[cfg['unit_col']]
    unit = df.loc[valid_unit, cfg['unit_col']]
    result = {
        'schema_version': 1, 'scope': 'technical_data_checks_only',
        'rows': len(df), 'columns': len(df.columns),
        'independent_unit_column_declared_by_user': cfg['unit_col'],
        'distinct_nonmissing_units': int(unit.nunique()),
        'rows_missing_unit': int((~valid_unit).sum()),
        'units_with_multiple_rows': int((unit.value_counts() > 1).sum()),
        'row_key': keys,
        'rows_with_missing_key': int(missing[keys].any(axis=1).sum()),
        'rows_with_edge_whitespace_in_keys': int(pd.concat([df[c].ne(df[c].str.strip()) for c in keys], axis=1).any(axis=1).sum()),
        'rows_in_duplicate_keys': int(df.duplicated(keys, keep=False).sum()),
        'duplicate_full_rows_after_first': int(df.duplicated().sum()),
        'missing_by_configured_column': {c: int(missing[c].sum()) for c in sorted(needed)},
        'numeric_checks': {c: numeric[c] for c in sorted(numeric)},
        'limitations': ['No automatic row deletion, inferential validity, canonical identity verification, missingness mechanism or causal identification assessment.'],
    }
    if split:
        ok = valid_unit & ~missing[split]
        grouped = df.loc[ok].groupby(cfg['unit_col'])[split].nunique()
        result['split_checks'] = {'rows_missing_split': int(missing[split].sum()), 'units_in_multiple_splits': int((grouped > 1).sum())}
    if pair:
        complete = np.isfinite(values[pair[0]].to_numpy(dtype=float)) & np.isfinite(values[pair[1]].to_numpy(dtype=float))
        result['pair_checks'] = {'columns': pair, 'finite_complete_pair_rows': int(complete.sum()), 'incomplete_or_invalid_pair_rows': int((~complete).sum())}
    result['provenance'] = {
        'utc': datetime.now(timezone.utc).isoformat(), 'input_sha256': sha(data),
        'config_sha256': sha(config), 'script_sha256': sha(__file__),
        'argv': sys.argv, 'python': platform.python_version(), 'pandas': pd.__version__, 'numpy': np.__version__,
    }
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', required=True)
    p.add_argument('--config', required=True, help='JSON with explicit unit_col, row_key and optional numeric_cols/paired_cols/bounds/split_col/missing_tokens')
    p.add_argument('--out', required=True)
    args = p.parse_args()
    try:
        out = Path(args.out)
        if out.resolve() in {Path(args.data).resolve(), Path(args.config).resolve(), Path(__file__).resolve()} or out.exists():
            raise ValueError('Output must be new and must not overwrite an input or script')
        report = audit(args.data, args.config)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open('x', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.write('\n')
        print(f'Audit written: {out}; scientific validity was not assessed')
    except (ValueError, OSError, pd.errors.ParserError) as e:
        p.exit(2, f'Input audit refused: {e}\n')


if __name__ == '__main__':
    main()
