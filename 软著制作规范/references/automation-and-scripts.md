# 自动化脚本与执行边界

本 skill 的自动化目标不是“无人值守替申请人决定法律事实”，而是把可自动复算的工程步骤稳定化，把必须人工确认的事实留在门禁处。

## 1. 脚本总览

| 脚本 | 作用 | 是否可以自动完成 | 不能替代什么 |
| --- | --- | --- | --- |
| `init_workspace.py` | 建立分层工作区和门禁状态 | 是 | 不判断项目是否适合登记 |
| `scan_project.py` | 扫描文件、语言、LOC、hash | 是 | 不证明作者/权属 |
| `propose_code_selection.py` | 生成代码候选和选择理由 | 仅生成建议 | 不能自动确认第一方源码 |
| `count_first_party_loc.py` | 对确认后的第一方文件复算 LOC/hash | 是 | 不决定哪些文件属于申请人 |
| `build_source_page_map.py` | 生成名义源码页映射 | 是 | 不替代 Word/WPS/PDF 实际分页 |
| `final_consistency_audit.py` | 对申请事实、说明书、源码页映射做交叉一致性检查 | 是 | 不替代法律审查和视觉 QA |
| `run_pipeline.py` | 按门禁组织上述脚本 | 是，但遇门禁主动停止 | 不允许越过权属/日期/截图确认 |

全部脚本默认只使用 Python 标准库，尽量减少环境依赖。

## 2. 推荐执行流程

### 阶段 A：初始化与扫描

```bash
python scripts/run_pipeline.py bootstrap "<PROJECT_ROOT>" --profile cli
```

可选 profile：

- `gui`：桌面/Web/移动端；
- `cli`：命令行、科研分析工具、数据管线；
- `sdk`：SDK/API/库；
- `auto`：未知软件形态。

该阶段输出：

- 标准工作区；
- project-inventory.json/csv；
- 代码文件候选清单；
- 代码文件选择.json。

**随后必须停止。**

模型/申请人需要核对：第三方、生成代码、测试、样例、权属、软件范围，并把真正确认的文件标为：

- `FIRST_PARTY`
- `APPLICANT_CONFIRMED`
- 或 `VERIFIED_FIRST_PARTY`

### 阶段 B：确认后复算

```bash
python scripts/run_pipeline.py post-confirm "<PROJECT_ROOT>" "<代码文件选择.json>"
```

若任何被选文件仍是 `UNVERIFIED`，流水线应拒绝继续。

输出：

- FIRST_PARTY_LOC_AUDIT.json/csv；
- SOURCE_PAGE_MAP.csv/json。

## 3. canonical application facts

建议创建一个内部 JSON：

```json
{
  "canonical": {
    "software_full_name": "待申请人确认",
    "software_short_name": "",
    "version": "待申请人确认",
    "copyright_owner": "待申请人确认",
    "development_mode": "待申请人确认",
    "rights_acquisition": "待申请人确认",
    "completion_date": "待申请人确认",
    "publication_status": "待申请人确认",
    "manual_render_qa": false
  }
}
```

该 JSON 是自动一致性审计的唯一 canonical 口径之一，但内容仍需来自事实台账和申请人确认。

## 4. 最终一致性审计

```bash
python scripts/run_pipeline.py audit \
  --application "<application-facts.json>" \
  --manual "<软件说明书.docx>" \
  --source-map "<SOURCE_PAGE_MAP.csv>"
```

若 `manual_render_qa != true/CONFIRMED`，最终脚本必须保持 HOLD，避免把“自动文本检查通过”误写成“已经可提交”。

## 5. 源码页映射的定位

`build_source_page_map.py` 采用名义行数进行页映射，只用于：

- 复核文件顺序；
- 复核代码连续性；
- 标记最后自然不足页；
- 给 Word/PDF 实际分页 QA 提供基准。

它不能声称 Word 最终页数就是名义页数。超长行自动换行、页眉、文件标题、字体和段距都可能改变实际页数。

## 6. 开发证据链

Git、测试日志、回归报告、release 和 hash 属于防御性证据。

原则：

- 有真实历史就归档；
- 没有就明确写没有；
- 不倒签、不伪造 commit；
- 当前时点可初始化新 Git，但第一条应写 archival import，而不是假装早期开发记录；
- 开发证据链默认不作为普通软著申请附件上传。

## 7. 失败即停

自动化脚本出现以下情形时应 HOLD：

- 项目路径不存在；
- 选中的源码文件缺失；
- 选中源码仍未确认第一方权属；
- 申请软件名或版本缺失；
- 正式文档中存在 TODO/待确认/截图占位；
- 中间源码页名义行数异常；
- Word/WPS/PDF 视觉 QA 未确认。

脚本的价值来自“把不确定性暴露出来”，而不是替申请人把所有状态改成绿色。


## 8. DOCX 自动生成

确认业务、申请事实、代码选择和截图后：

```bash
python scripts/run_pipeline.py build-docx \
  --project "<PROJECT_ROOT>" \
  --facts "<application-facts.json>" \
  --manual-md "<软件说明书.md>" \
  --selection "<代码文件选择.json>" \
  --screenshots "<截图证据.csv>" \
  --out-dir "<04_正式资料>"
```

说明书 Markdown 可使用标题、普通段落、无序列表、fenced code block、简单 Markdown 表格；`[[FIGURE:图4-1]]` 会把截图 manifest 中对应 figure_id 插入文档。

源程序 DOCX 只读取 `selected=true` 且 ownership_status 已确认的第一方文件，不会把依赖、测试或未确认代码自动塞进材料。

## 9. 真实分页 QA

源码名义页映射之后，还必须对 DOCX 做真实渲染：

```bash
python scripts/run_pipeline.py render-qa \
  --docx "<源程序鉴别材料.docx>" \
  --out-dir "<05_内部审计/render_qa>" \
  --kind source \
  --source-map "<..._SOURCE_PAGE_MAP.csv>" \
  --header-text "<软件全称> <版本号>"
```

说明书同样以 `--kind manual` 运行。渲染器优先 Windows Microsoft Word COM；若不可用则尝试 WPS Writer COM（KWPS/WPS/Kingsoft.WPS ProgID），最后回退 LibreOffice/soffice；PDF 文本提取优先 PyMuPDF、pypdf、pdftotext。

脚本会检查实际页数、名义页数漂移、空白页、中间源码页文本行数异常，以及说明书中的 TODO/待确认/截图占位。即使自动状态为 `AUTO_RENDER_QA_PASS`，也必须逐页看实际 PDF/PNG；只有人工视觉 QA 完成后才能把 `manual_render_qa` 改为 true。

## 10. 最终提交包构建

人工 QA 完成、canonical facts 冻结后：

```bash
python scripts/run_pipeline.py package \
  --facts "<application-facts.json>" \
  --manual-docx "<软件说明书.docx>" \
  --manual-pdf "<软件说明书.pdf>" \
  --source-docx "<源程序鉴别材料.docx>" \
  --source-pdf "<源程序鉴别材料.pdf>" \
  --screenshots-dir "<03_截图/正式>" \
  --internal-dir "<05_内部审计>" \
  --internal-dir "<06_开发证据链_可选>" \
  --out-dir "<最终提交包>" \
  --require-pdf
```

输出分成 `01_正式上传/` 和 `02_内部归档_不上传/`，并生成 `PACKAGE_MANIFEST.json`、`FINAL_HASHES.sha256` 和 `FINAL_SUBMISSION_PACKAGE_VERDICT.md`。

builder 会拒绝 canonical facts 仍有待确认、`manual_render_qa` 未确认、正式 DOCX 残留内部状态词、软件名/版本无法核对，或在 `--require-pdf` 模式下缺最终 PDF。因此自动成稿和正式提交之间仍保留真实人工 QA 门。
