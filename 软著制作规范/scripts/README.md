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
