from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundle_check(case: str, manifest_case: str) -> dict[str, object]:
    bundle = ROOT / "runs" / case / "bundle"
    manifest = json.loads(
        (ROOT / "bundles" / manifest_case / "bundle-manifest.json").read_text(encoding="utf-8")
    )
    actual = sorted(p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file())
    listed = sorted(item["bundle_path"] for item in manifest["files"])
    hashes = {rel: sha256(bundle / rel) for rel in actual}
    expected = {item["bundle_path"]: item["sha256"] for item in manifest["files"]}
    payload = "\n".join(
        (bundle / rel).read_text(encoding="utf-8")
        for rel in actual
        if rel.endswith((".md", ".py"))
    )
    return {
        "actual_files": actual,
        "manifest_files": listed,
        "file_set_equal": actual == listed,
        "hashes_equal": hashes == expected,
        "contains_checklist_md": any(Path(rel).name == "checklist.md" for rel in actual),
        "contains_F01_or_F20": "F01" in payload or "F20" in payload,
    }


def main() -> None:
    result = json.loads((ROOT / "parent-verification-revised.json").read_text(encoding="utf-8"))
    run = ROOT / "runs" / "p03-final"
    log = (run / "execution-log.md").read_text(encoding="utf-8")
    result["p03"] = {
        "input_sha256": sha256(run / "input.docx"),
        "expected_input_sha256": "e7b80c318e311100a20a3314dc3fd92141ba41a44ba03aad575d15efb96269cb",
        "formatted_exists": (run / "formatted.docx").exists(),
        "log_exists": (run / "execution-log.md").exists(),
        "log_sha256": sha256(run / "execution-log.md"),
        "contains_ellipsis_placeholder": bool(re.search(r"\.\.\.|…|\b略\b", log)),
        "records_exact_commands_section": "## Commands actually run" in log,
        "records_runtime_section": "## Runtime and tool versions" in log,
        "records_noncertification_boundary": "does not certify scientific correctness" in log,
    }
    result["bundles"]["p03-final"] = bundle_check("p03-final", "p03-final")
    result["bundles"].pop("p03-revised", None)
    result["verification_composition"] = {
        "p01": "revised regression run; document algorithm and full commands unchanged by final logging clarification",
        "p02": "revised regression run; document algorithm and full commands unchanged by final logging clarification",
        "p03": "fresh final run using the final clarified local bundle",
    }
    (ROOT / "parent-verification-final.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
