from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "snapshot-manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


records = []
for path in sorted(p for p in ROOT.rglob("*") if p.is_file() and p != OUTPUT):
    records.append({
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    })

OUTPUT.write_text(
    json.dumps({"schema_version": 1, "files": records}, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
