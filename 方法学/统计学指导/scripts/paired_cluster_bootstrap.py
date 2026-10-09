#!/usr/bin/env python3
"""Paired supplied numeric A-B mean, resampling independent clusters; percentile CI only."""
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


def compute(data, cluster_col, row_key, a, b, weighting, reps=10000, seed=2026, confidence=.95, allow_complete_case=False, missing_tokens=('', 'NA', 'N/A', 'NaN', 'nan')):
    if weighting not in ('equal_cluster', 'equal_observation'):
        raise ValueError('Explicit weighting required')
    if not isinstance(reps, int) or reps < 2 or not 0 < confidence < 1:
        raise ValueError('Require reps >= 2 and 0 < confidence < 1')
    if not row_key or len(set(row_key)) != len(row_key) or cluster_col not in row_key:
        raise ValueError('row_key must contain the cluster column and unique column names')
    if a == b or a == cluster_col or b == cluster_col or set(row_key) & {a, b}:
        raise ValueError('Pair measures must be distinct from each other and key columns')
    with Path(data).open(encoding="utf-8-sig", newline="") as f:
        header = next(csv.reader(f), [])
    if not header or len(header) != len(set(header)) or any(not c for c in header):
        raise ValueError("CSV requires nonempty unique column headers")
    df = pd.read_csv(data, dtype=str, keep_default_na=False)
    if set(row_key + [cluster_col, a, b]) - set(df.columns):
        raise ValueError('Required columns absent')
    tokens = set(missing_tokens) | {''}
    if df[row_key].isin(tokens).any().any():
        raise ValueError('Missing key/cluster values; fix identity before inference')
    if any(df[c].ne(df[c].str.strip()).any() for c in row_key):
        raise ValueError('Whitespace at key edges; verify canonical identity before inference')
    if df.duplicated(row_key).any():
        raise ValueError('Duplicate row keys; do not silently deduplicate')
    pair = []
    for c in (a, b):
        miss = df[c].isin(tokens)
        vals = pd.to_numeric(df[c].mask(miss), errors='coerce')
        if ((~miss) & vals.isna()).any() or np.isinf(vals.to_numpy(dtype=float)).any():
            raise ValueError('Non-numeric or infinite measures; fix inputs, not complete-case drop')
        pair.append(vals)
    complete = pair[0].notna() & pair[1].notna()
    dropped = int((~complete).sum())
    if dropped and not allow_complete_case:
        raise ValueError('Missing pairs: explicitly justify and pass --allow-complete-case, or use another missing-data method')
    all_clusters = int(df[cluster_col].nunique())
    retained = df.loc[complete].copy()
    differences = pair[0][complete] - pair[1][complete]
    if not np.isfinite(differences).all():
        raise ValueError('Difference overflow; rescale before inference')
    group = differences.groupby(retained[cluster_col], sort=True).agg(['sum', 'count'])
    g = len(group)
    if g < 2:
        raise ValueError('At least two retained independent clusters required; inference may still be unreliable with few clusters')
    sums = group['sum'].to_numpy(dtype=float)
    counts = group['count'].to_numpy(dtype=float)
    if not np.isfinite(sums).all():
        raise ValueError('Cluster sum overflow; rescale')
    means = sums / counts
    estimate = float(means.mean() if weighting == 'equal_cluster' else sums.sum() / counts.sum())
    rng = np.random.default_rng(seed)
    boots = np.empty(reps)
    # Preserve repeated cluster draws; bound the index matrix memory.
    block = max(1, min(256, 1000000 // g))
    for start in range(0, reps, block):
        idx = rng.integers(0, g, size=(min(block, reps-start), g))
        if weighting == 'equal_cluster':
            vals = means[idx].mean(axis=1)
        else:
            vals = sums[idx].sum(axis=1) / counts[idx].sum(axis=1)
        boots[start:start+len(vals)] = vals
    if not np.isfinite(boots).all() or not np.isfinite(estimate):
        raise ValueError('Estimator overflow; rescale')
    tail = (1-confidence)/2
    low, high = np.quantile(boots, [tail, 1-tail], method='linear')
    warnings = ['Interval covers sampling uncertainty for supplied numeric paired differences only; no causal identification or training-process uncertainty.']
    if g < 30:
        warnings.append('Few clusters (<30, heuristic review flag, not a validity threshold): percentile coverage may be poor; review design and small-sample inference.')
    if dropped:
        warnings.append('Complete-case restriction changes available rows/clusters; missingness assumptions not verified.')
    if np.ptp(boots) == 0:
        warnings.append('Degenerate bootstrap distribution; this does not rule out measurement, selection or other uncertainty.')
    return {
        'schema_version': 1, 'contrast': f'{a} minus {b}', 'weighting': weighting,
        'estimand_description': 'mean of cluster mean paired differences' if weighting == 'equal_cluster' else 'mean of all retained observation paired differences',
        'input_rows': len(df), 'retained_pair_rows': len(retained), 'dropped_pair_rows': dropped,
        'input_clusters': all_clusters, 'retained_clusters': g, 'entire_clusters_lost': all_clusters-g,
        'estimate': estimate, 'interval': [float(low), float(high)], 'confidence': confidence,
        'interval_method': 'cluster percentile bootstrap, NumPy linear quantiles (not BCa)',
        'reps': reps, 'seed': seed, 'bootstrap_sd': float(boots.std(ddof=1)),
        'bootstrap_degenerate': bool(np.ptp(boots) == 0), 'warnings': warnings,
        'provenance': {'utc': datetime.now(timezone.utc).isoformat(), 'input_sha256': sha(data),
            'script_sha256': sha(__file__), 'argv': sys.argv, 'cluster_col': cluster_col,
            'row_key': row_key, 'missing_tokens': list(missing_tokens), 'allow_complete_case': allow_complete_case,
            'python': platform.python_version(), 'pandas': pd.__version__, 'numpy': np.__version__},
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', required=True)
    p.add_argument('--cluster-col', required=True)
    p.add_argument('--row-key', nargs='+', required=True)
    p.add_argument('--a', required=True)
    p.add_argument('--b', required=True)
    p.add_argument('--weighting', choices=['equal_cluster', 'equal_observation'], required=True)
    p.add_argument('--reps', type=int, default=10000)
    p.add_argument('--seed', type=int, default=2026)
    p.add_argument('--confidence', type=float, default=.95)
    p.add_argument('--allow-complete-case', action='store_true')
    p.add_argument('--missing-token', action='append', help='Additional exact token treated as missing')
    p.add_argument('--out', required=True)
    args = p.parse_args()
    try:
        out = Path(args.out)
        if out.exists() or out.resolve() in {Path(args.data).resolve(), Path(__file__).resolve()}:
            raise ValueError('Output must be new and must not overwrite inputs or script')
        result = compute(args.data, args.cluster_col, args.row_key, args.a, args.b,
            args.weighting, args.reps, args.seed, args.confidence, args.allow_complete_case,
            tuple(['', 'NA', 'N/A', 'NaN', 'nan'] + (args.missing_token or [])))
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open('x', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.write('\n')
        print(f'Result written: {out}; inspect warnings and estimand before use')
    except (ValueError, OSError, pd.errors.ParserError) as e:
        p.exit(2, f'Paired bootstrap refused: {e}\n')


if __name__ == '__main__':
    main()
