#!/usr/bin/env python3
"""Stage a minimal, auditable Word-skill bundle for one execution scope.

This script uses only the Python standard library. It never deletes or
overwrites an output directory. The manifest sits beside ``bundle/`` so it can
hash every file exposed to the executor without a recursive self-hash.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path


LOCAL_SKILL = """---
name: format-academic-word-local-three-line
description: Safely convert one already identified Word data table to a three-line table, preserve content and structure, and render the result for visual verification. Use only for this local table-formatting scope; stop and request a different bundle for full-document formatting or audit.
---

# Word单表三线表局部执行包

## 范围

只处理用户已经定位的一个数据表。先读取 `references/formatting.md` 中三线表相关内容和 `references/three-line-tables.md`；按需导入 `scripts/word_format_helpers.py`。不要润色、重算、补引文、修改表外段落或扩展为全文格式审计。

如果请求变为完整格式化、完整审计、完整清单或其他模块任务，立即停止，不修改DOCX，并要求协调者用相应scope重新分包。不要从记忆重建未提供的资源。

## 执行

1. 保留原件，记录目标表位置、行列、实际表头行数、合并、文字和数字；确认它是数据表而非布局表、嵌套表或公式容器。
2. 修改前检查缺省网格单元格、嵌套表和纵向合并边界。纵向合并跨越表头与正文、或结构不能安全判定时，停止并报告具体位置；不得拆分合并、复制数据或绕过辅助函数的异常。
3. 仅对已确认目标表调用 `three_line_table`。导入包内辅助函数时使用 `python -B` 或等效设置禁用字节码缓存，技能资源目录只读，不在其中生成 `__pycache__`、日志或中间产物。保存为新文件，不覆盖输入；不改变文字、数字、引用、合并关系或表外格式。
4. 对照原件核验内容和结构；使用环境提供的documents渲染流程渲染最新输出，逐页检查表线、残余竖线/网格/底色、裁切、重叠、缺字和说明位置。有缺陷则修复并重新渲染。
5. 只交付格式副本及本次表格直接相关的结构/视觉结果。未实际渲染、仍有未看页面或遇到安全停止条件时，不声称完成或视觉通过。

## 记录

执行日志列出实际读取文件、命令、输入/输出SHA-256、结构检查、渲染器与逐页结论。日志中的通过仅限授权表格和已观察页面，不认证全文、科学正确性或期刊合规。
"""


SCOPES = {
    "local-three-line": {
        "generated_skill": LOCAL_SKILL,
        "files": (
            "references/formatting.md",
            "references/three-line-tables.md",
            "scripts/word_format_helpers.py",
        ),
    },
    "full-audit": {
        "generated_skill": None,
        "files": (
            "SKILL.md",
            "assets/default-profile.json",
            "references/checklist.md",
            "references/formatting.md",
            "references/three-line-tables.md",
            "scripts/word_format_helpers.py",
        ),
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_source(source_root: Path, relative: str) -> Path:
    source = source_root / relative
    if source.is_symlink() or not source.is_file():
        raise ValueError(f"Required regular file is missing or unsafe: {relative}")
    resolved_root = source_root.resolve()
    resolved = source.resolve()
    if resolved_root not in resolved.parents:
        raise ValueError(f"Source escapes skill root: {relative}")
    return source


def preflight(source_root: Path, output: Path, scope: str) -> list[tuple[str, Path]]:
    if not source_root.is_dir():
        raise ValueError(f"Source root is not a directory: {source_root}")
    if output.exists():
        state = "non-empty" if output.is_dir() and any(output.iterdir()) else "existing"
        raise ValueError(f"Refusing {state} output path: {output}")
    source_resolved = source_root.resolve()
    output_resolved = output.resolve(strict=False)
    if source_resolved == output_resolved or source_resolved in output_resolved.parents:
        raise ValueError("Output must not be inside the source skill directory")
    selected = []
    for relative in SCOPES[scope]["files"]:
        selected.append((relative, safe_source(source_root, relative)))
    return selected


def stage(source_root: Path, output: Path, scope: str) -> Path:
    selected = preflight(source_root, output, scope)
    output.parent.mkdir(parents=True, exist_ok=True)
    temp_root = Path(tempfile.mkdtemp(prefix=f".{output.name}.tmp-", dir=output.parent))
    try:
        bundle = temp_root / "bundle"
        bundle.mkdir()
        generated = SCOPES[scope]["generated_skill"]
        if generated is not None:
            (bundle / "SKILL.md").write_text(generated, encoding="utf-8", newline="\n")
        for relative, source in selected:
            target = bundle / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target, follow_symlinks=False)

        records = []
        for path in sorted(p for p in bundle.rglob("*") if p.is_file()):
            relative = path.relative_to(bundle).as_posix()
            origin = "<generated:local-three-line>" if relative == "SKILL.md" and generated is not None else relative
            records.append({
                "bundle_path": relative,
                "source_path": origin,
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            })
        manifest = {
            "schema_version": 1,
            "scope": scope,
            "executor_root": "bundle",
            "manifest_exposure": "coordinator-only",
            "files": records,
        }
        (temp_root / "bundle-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        os.rename(temp_root, output)
    except Exception:
        shutil.rmtree(temp_root, ignore_errors=True)
        raise
    return output / "bundle-manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True,
                        help="Word skill directory containing SKILL.md")
    parser.add_argument("--scope", choices=sorted(SCOPES), required=True)
    parser.add_argument("--output", type=Path, required=True,
                        help="New output directory; must not already exist")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = stage(args.source_root, args.output, args.scope)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"stage_task_bundle: {exc}") from exc
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
