# scripts

这些脚本用于把可复算的软著工程步骤标准化。它们不负责替申请人决定著作权人、开发方式、取得方式、完成日期或发表状态。

## 快速开始

```bash
python run_pipeline.py bootstrap "<项目目录>" --profile auto
```

确认业务边界、第一方源码和权属后：

```bash
python run_pipeline.py post-confirm "<项目目录>" "<代码文件选择.json>"
```

最终一致性检查：

```bash
python run_pipeline.py audit \
  --application "<application-facts.json>" \
  --manual "<软件说明书.docx>" \
  --source-map "<SOURCE_PAGE_MAP.csv>"
```

## 设计约束

- Python 标准库优先；
- 不生成业务源码；
- 不补造 Git 历史；
- 不把候选代码自动等同为第一方代码；
- 不用名义页数替代最终 Word/WPS/PDF 页数；
- 自动审计通过也不等同于登记成功。

详细说明见 `../references/automation-and-scripts.md`。


## DOCX 自动生成

```bash
python run_pipeline.py build-docx \
  --project "<项目目录>" \
  --facts "<application-facts.json>" \
  --manual-md "<软件说明书.md>" \
  --selection "<代码文件选择.json>" \
  --screenshots "<截图证据.csv>" \
  --out-dir "<04_正式资料>"
```

需要 `python-docx`。截图 manifest 中的 `figure_id` 可在 Markdown 用 `[[FIGURE:figure_id]]` 插入真实截图。

## 真实分页与视觉 QA

```bash
python run_pipeline.py render-qa --docx "<说明书.docx>" --out-dir qa_manual --kind manual
python run_pipeline.py render-qa --docx "<源程序.docx>" --out-dir qa_source --kind source --source-map "<..._SOURCE_PAGE_MAP.csv>"
```

优先调用 Microsoft Word COM；没有 Word 时调用 LibreOffice。输出真实 PDF、分页 QA CSV/JSON/MD，并在可用时导出逐页 PNG。自动 PASS 后仍必须人工逐页查看。

## 最终提交包

```bash
python run_pipeline.py package \
  --facts "<application-facts.json>" \
  --manual-docx "<说明书.docx>" --manual-pdf "<说明书.pdf>" \
  --source-docx "<源程序.docx>" --source-pdf "<源程序.pdf>" \
  --screenshots-dir "<正式截图目录>" \
  --internal-dir "<内部审计目录>" \
  --out-dir "<最终提交包>" --require-pdf
```

只有 `manual_render_qa=true/CONFIRMED` 才允许生成 READY 提交包。正式上传目录和内部归档目录自动分离，并生成 `PACKAGE_MANIFEST.json` 与 `FINAL_HASHES.sha256`。
