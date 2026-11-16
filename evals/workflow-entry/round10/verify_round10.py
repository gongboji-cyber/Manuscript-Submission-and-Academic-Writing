#!/usr/bin/env python3
import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    root = args.root.resolve()

    coordinator = (root / "SKILL.md").read_text(encoding="utf-8")
    topic = (root / "research-topic-selection" / "SKILL.md").read_text(encoding="utf-8")
    sources = (root / "references" / "workflow-sources.md").read_text(encoding="utf-8")

    module_files = sorted(
        path
        for path in root.glob("*/SKILL.md")
        if "evals" not in path.parts
    ) + sorted(root.glob("*/*/SKILL.md"))
    module_files = [path for path in module_files if "evals" not in path.parts]

    links_missing = []
    for source in [root / "SKILL.md", *module_files]:
        text = source.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            resolved = source.parent / urllib.parse.unquote(target.split("#", 1)[0])
            if not resolved.resolve().exists():
                links_missing.append({"source": str(source.relative_to(root)), "target": target})

    checks = {
        "module_count_is_11": len(module_files) == 11,
        "coordinator_routes_g1_support_before_decision": "G1按需联动`retrieve-and-match-references`/`critically-read-literature`" in coordinator,
        "coordinator_routes_methods_before_decision": "G2/G4在裁决前按需联动`guide-research-methods-statistics`" in coordinator,
        "coordinator_blocks_writing_until_g5": "只有G5通过才考虑写稿/投稿模块" in coordinator,
        "stale_post_gate_methods_text_removed": "通过关口后再转`guide-research-methods-statistics`" not in coordinator,
        "topic_v2_defines_g0_g5": "## 硬门槛 G0–G5" in topic,
        "topic_v2_requires_methods_when_needed": "需要时联动 `retrieve-and-match-references`、`critically-read-literature`、`guide-research-methods-statistics`" in topic,
        "topic_v2_blocks_writing_until_g5": "仅在过 G5 后考虑写稿技能" in topic,
        "source_snapshot_matches_main": "main@5af337b3d8cdf530aa382ad9cf0f33de03cc046e" in sources,
        "source_snapshot_records_v2_handoffs": "G1、G2/G4分别按需联动" in sources,
        "relative_links_resolve": not links_missing,
    }
    result = {
        "checks": checks,
        "module_count": len(module_files),
        "missing_links": links_missing,
        "all_pass": all(checks.values()),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
