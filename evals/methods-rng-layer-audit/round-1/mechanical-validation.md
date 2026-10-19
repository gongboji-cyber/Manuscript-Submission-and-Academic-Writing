# Mechanical validation — 2026-10-20

This record validates the software behavior behind the proposed gate. It does not evaluate agent responses, prove scientific validity or certify the new workflow.

## Frozen defect and expected mechanical contrast

- Defect: an outer data seed can remain fixed while a nested estimator uses uncontrolled RNG.
- Expected contrast: repeated fits with `random_state=None` can differ; repeated fits with an integer `random_state` should match for this scikit-learn estimator and environment.
- Public synthetic input only; no manuscript, patient or private data.

## Environment and command

Python 3.12.14, NumPy 2.3.5, scikit-learn 1.8.0. Network was not used by the experiment.

```bash
python - <<'PY'
import hashlib, json, platform, time
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestRegressor

OUTER_SEED = 20261020
rng = np.random.default_rng(OUTER_SEED)
X = rng.normal(size=(360, 12))
y = 2*X[:,0] - 1.2*X[:,1] + 0.8*X[:,2]*X[:,3] + rng.normal(scale=1.2, size=360)
train = np.arange(0, 240)
test = np.arange(240, 360)

def run(model_seed):
    model = RandomForestRegressor(
        n_estimators=24, max_depth=5, min_samples_leaf=2,
        n_jobs=1, random_state=model_seed
    )
    model.fit(X[train], y[train])
    pred = model.predict(X[test])
    rmse = float(np.sqrt(np.mean((pred-y[test])**2)))
    digest = hashlib.sha256(pred.tobytes()).hexdigest()[:16]
    return rmse, digest, pred

start = time.perf_counter()
none_runs = [run(None) for _ in range(8)]
fixed_runs = [run(731) for _ in range(8)]
none_rmses = [x[0] for x in none_runs]
fixed_rmses = [x[0] for x in fixed_runs]
none_pred = np.stack([x[2] for x in none_runs])
fixed_pred = np.stack([x[2] for x in fixed_runs])
result = {
    "python": platform.python_version(),
    "sklearn": sklearn.__version__,
    "numpy": np.__version__,
    "outer_seed": OUTER_SEED,
    "n_estimators": 24,
    "repeats": 8,
    "random_state_none": {
        "unique_prediction_hashes": len({x[1] for x in none_runs}),
        "hashes": [x[1] for x in none_runs],
        "rmse_range": [min(none_rmses), max(none_rmses)],
        "max_abs_prediction_spread": float(np.max(np.ptp(none_pred, axis=0))),
    },
    "random_state_int": {
        "unique_prediction_hashes": len({x[1] for x in fixed_runs}),
        "hashes": [x[1] for x in fixed_runs],
        "rmse_range": [min(fixed_rmses), max(fixed_rmses)],
        "max_abs_prediction_spread": float(np.max(np.ptp(fixed_pred, axis=0))),
    },
    "elapsed_s": time.perf_counter() - start,
}
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

## Raw result

```json
{
  "elapsed_s": 0.43097534500000734,
  "n_estimators": 24,
  "numpy": "2.3.5",
  "outer_seed": 20261020,
  "python": "3.12.14",
  "random_state_int": {
    "hashes": [
      "6b99ea2249fc3479",
      "6b99ea2249fc3479",
      "6b99ea2249fc3479",
      "6b99ea2249fc3479",
      "6b99ea2249fc3479",
      "6b99ea2249fc3479",
      "6b99ea2249fc3479",
      "6b99ea2249fc3479"
    ],
    "max_abs_prediction_spread": 0.0,
    "rmse_range": [1.6720779402427381, 1.6720779402427381],
    "unique_prediction_hashes": 1
  },
  "random_state_none": {
    "hashes": [
      "bce0559d6bfb129e",
      "1bd0a0f58497b6c9",
      "83e434e900195799",
      "9f8380d4b37e5418",
      "86f821771f4a8ca9",
      "28efeb3d576d3c85",
      "c1803ba0770ac7d2",
      "09401a3172435fa3"
    ],
    "max_abs_prediction_spread": 1.6577171347906428,
    "rmse_range": [1.6132639653880312, 1.683118787319813],
    "unique_prediction_hashes": 8
  },
  "repeats": 8,
  "sklearn": "1.8.0"
}
```

The captured stdout artifact had SHA-256 `7ee94e7e6aaa2dfc4c47c97009ed7c6b502e45fdd746c97baf3b9375276ee48f`. The runtime exposed no monetary or call-token cost. The measured Python block time was 0.431 seconds; shell-level resource timing was unavailable.

## Primary evidence read

- scikit-learn 1.9.1 official *Common pitfalls*, lines 209–248: `random_state` behavior for repeated `fit`; lines 268–315: estimator/CV subtleties.
- scikit-learn 1.9.1 official `RandomForestRegressor`, lines 633–743: constructor, bootstrap and `random_state`.
- MolPAL official `publication` tag commit `fc0b913c87200e28bfc2e36028f559961f2f438b`, `molpal/models/sklmodels.py` lines 23–48: `RFModel` constructs `RandomForestRegressor` without `random_state`.

## Boundaries and pending review

The run demonstrates hidden estimator stochasticity in one synthetic setup and the specified local versions. It does not reproduce MolPAL study outcomes, measure a universal effect size, prove all parallel backends deterministic, or establish that integer seeding is always preferable for robustness studies. Re-run after library/backend/hardware changes. The four-case agent regression remains unexecuted because no independent same-context baseline/candidate runner and reviewer were available in this run.
