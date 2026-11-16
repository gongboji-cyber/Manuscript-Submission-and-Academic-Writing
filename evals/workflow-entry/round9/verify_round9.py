#!/usr/bin/env python3
"""Static regression checks for the Round 9 routing repair."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TOPIC_ROW_MARKER = "| 科研选题、立项、研究idea筛选或拒稿后是否值得重做 |"


def inspect(root: Path) -> dict[str, object]:
    entry = (root / "SKILL.md").read_text(encoding="utf-8")
    sources = (root / "references" / "workflow-sources.md").read_text(encoding="utf-8")
    module_entries = sorted(
        rel.as_posix()
        for p in root.rglob("SKILL.md")
        if (rel := p.relative_to(root)).parts[0] != "evals" and len(rel.parts) > 1
    )
    topic_target = root / "research-topic-selection" / "SKILL.md"
    return {
        "root": str(root),
        "module_count": len(module_entries),
        "module_entries": module_entries,
        "topic_route_count": entry.count(TOPIC_ROW_MARKER),
        "topic_target_exists": topic_target.is_file(),
        "source_snapshot_current": (
            "main@b92b44487caac54aaa491aa533ab18aa0ec52e45" in sources
            and "十一份专业模块SKILL.md" in sources
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    baseline = inspect(args.baseline)
    candidate = inspect(args.candidate)
    checks = {
        "baseline_reproduces_missing_route": baseline["topic_route_count"] == 0,
        "candidate_has_one_topic_route": candidate["topic_route_count"] == 1,
        "candidate_target_resolves": candidate["topic_target_exists"] is True,
        "candidate_has_eleven_modules": candidate["module_count"] == 11,
        "candidate_source_snapshot_current": candidate["source_snapshot_current"] is True,
    }
    payload = {"baseline": baseline, "candidate": candidate, "checks": checks}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
