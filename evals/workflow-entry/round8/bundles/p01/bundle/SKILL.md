---
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

无论任务完成还是安全停止，结束前都要写执行日志。日志至少逐项列出：任务状态；实际读取文件；实际运行的命令及退出状态；实际使用的Python、python-docx及其他工具版本；输入SHA-256；输出文件和SHA-256（未生成则写不适用及原因）；结构检查；渲染器、页数和逐页结论（未渲染则写不适用及原因）。安全停止也必须记录用于作出判断的只读检查命令，不能只写操作概述。日志中的通过仅限授权表格和已观察页面，不认证全文、科学正确性或期刊合规。
