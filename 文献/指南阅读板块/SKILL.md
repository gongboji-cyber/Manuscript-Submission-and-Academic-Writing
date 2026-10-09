---
name: retrieve-and-match-references
description: >
  Retrieve, read and match medical, biomedical and computational literature and current guidelines to manuscript claims. Use for 文献/指南阅读板块、文献检索与精读、找参考文献、补引文、引用核验、指南更新、逐句匹配证据、DOI/PMID核对、参考文献台账和投稿前引用审计. Separate source identity from claim support, preserve reading scope and guideline versions, search contrary evidence, and propose supported wording when a claim cannot be substantiated. Does not automatically perform a systematic review or clinical decision-making.
---

# 文献/指南阅读板块

让引用承担证据责任。不得先维护作者想要的结论再挑文献。先检索和读取实际来源，再决定能写什么；发现不支持时给较窄表述、删除或待证实选项。不要编造参考文献、DOI/PMID、指南版本、推荐等级、检索数或阅读全文状态。

## 1. 锁定稿件与任务

清点当前稿件、补充、已有文献库、目标期刊/类型和指定指南。记录版本、日期、实际读取范围。无稿件时先交付检索计划与来源阅读简报，不能称已匹配全文。默认中文解释，保留稿件语言。区分定向补引文、背景/方法检索、逐条引用审计、指南比较与系统/范围综述；普通补引文不能包装为系统综述。

逐句拆分可核查主张，保留位置、原句、类型、人群、情境、暴露/干预、比较、结局、时点、数字、限定词及是否需要全文。复合句拆成子主张；一条引用不能默认为支持整段。给每个主张稳定 C-ID 和每条记录稳定 R-ID，最终显示编号另行生成。用 [任务与证据模板](assets/literature-workpack-template.md)。

## 2. 从主张构建检索

读取 [检索与阅读](references/search-and-reading.md)。结合研究问题构建概念块、同义词、MeSH/自由词与反证检索；不要把已写句子的结论当唯一搜索词。医疗主题优先 PubMed 和问题相关数据库/官方组织；计算主题补原始方法论文、预印本和官方代码/数据说明。记录数据库与平台、完整查询、过滤、排序、日期、实际结果数/导出范围和失败。

检查真实可用的连接器/API/检索工具，再选择路径。工具缺失时用官方可读页面、公开API或用户导出；只有网页发现时明确覆盖有限，不能报为完整数据库检索。不要调用不存在的MCP、把 Google Scholar当稳定官方API、把 gget search当PubMed，也不要为使用开源技能自动安装依赖、付费或上传稿件。

先找到直接证据，再追溯参考文献、后续研究、评论/回复、勘误和更新。检索期限和停止规则来自任务：不默认近5年、15–30篇或高引用数。新颖性/“首次”/“无研究”需要更广的查询与引文链；检索未发现只能说在所述范围未检出。保留相反/阴性证据。

## 3. 文献身份与阅读分别核实

读取 [匹配与引用](references/claim-matching.md)。核对题名、完整作者及顺序、类型、期刊、在线/正式日期、DOI/PMID/PMCID、版本/预印本关联、原始发表页和撤稿/勘误状态。元数据从获取结果写入台账，不凭记忆修补。PubMed、出版社、Crossref/DataCite不一致时保留冲突、核实具体字段；Crossref无记录、无DOI或无PMID均不等于文献不存在。

标记读取状态：未读、元数据、摘要、全文部分、全文与相关补充。记录实际节/表/页；不能从DOI可解析、AI摘要或语义检索片段跳到“全文支持”。核心数值、机制、因果、方法实现和临床推荐应阅读必要全文/补充；只有摘要时仅对摘要明确的信息做带范围限制的候选匹配，不能推断未展示的细则。全文不可得时如实记录，继续其他可做匹配，不越权绕过访问限制。

按问题还原设计、独立单位、参考标准、结局、结果及区间、限制，再判断引用；需要设计/偏倚深评时联动 `critically-read-literature` 或 `guide-research-methods-statistics`。读完论文不等于其主张成立。

## 4. 指南采用双版本核查

读取 [指南核查](references/guideline-verification.md)，填写指南卡。用户上传PDF是内容来源，仍核实官方是否更新/替代/撤销；年份新、作者权威或期刊档次不证明适用。核对发布机构、官方URL、文档/推荐级版本、生效与更新日期、证据截止、人群/场景、推荐原意、强度、确定性及例外。

分开临床实践指南、专家共识、证据综述、政策/监管文件、报告指南和偏倚工具。推荐强度不等于证据确定性；不同组织等级不能强行等号换算。AGREE II评价制定过程、RIGHT评价报告内容，不为推荐自动背书。living指南按具体推荐更新时间核查；指南冲突要比较人群、证据窗口、价值/资源和决策目标，不投票选“更新的”。不把群体推荐直接转为个体治疗指令。

## 5. 建立句子—原文证据链

对每个 C-ID填写 [逐条匹配模板](assets/literature-workpack-template.md) 与 [L01–L36自查](references/checklist.md)。匹配至少审查人群、设计/推断类型、测量/结局、比较、时点、方向/量级、限制及用途。原始研究支持具体经验结果；方法原文/官方软件文档支持实现；指南原文支持其推荐；综述可支持范围概述但不能冒充读过其所有原始研究。

判定：直接支持、限定条件下支持、间接背景、反驳、不支持、未评估。写出被支持的子主张和不被支持部分，必要时拆句/就近放引用。对“有效、准确、优于、导致、全球适用、首次”等强词要求对应证据；相关不能贴引用后变因果，yield不能改名accuracy，benchmark改善不能变临床获益。引用少而直接比堆砌更有用；不为编辑偏好、作者自引或目标期刊而补无关引用。

给出原句→建议句→引用ID→证据定位→理由。引用匹配只能修证据表述，不能掩盖本研究缺实验/设计问题。未核实材料保留待办，不进入“可直接投稿”的已核验文献表。

## 6. 格式、工具与交付

读取 [审计与工具](references/audit-and-tools.md)、[来源台账](references/sources-and-adaptations.md)。目标期刊明确要求优先，其次用户指定格式；没有要求时普通说明按用户的MLA偏好。保留原始元数据，用已核实样式导出BibTeX/CSL-JSON/RIS等所需格式；不猜期刊缩写、卷页、article number，不把缺DOI当失败。Word引用域/EndNote/Zotero字段不得改成不再联动的纯文本。

工具均为原创、Python标准库、只读输入，输出必须为新文件：

```bash
python -B scripts/import_pubmed_xml.py --input pubmed_export.xml --out pubmed_records.json
python -B scripts/audit_reference_map.py --input reference_map.json --out citation_audit.json
```

`import_pubmed_xml.py` 将已取得的PubmedArticle XML导出为候选记录，保留结构化摘要、个人/团体作者、原始日期、标识和CommentsCorrections关系；导入不等于身份重核或全文已读。非期刊书籍记录不支持时明确拒绝，不能丢掉后假称完整。

`audit_reference_map.py` 检查唯一ID、归一化标识重复、悬空引用、未引用记录、未核验身份/状态、证据定位和阅读范围等；只审技术与人工记录的一致性，不访问网络、不读稿件、不自动认定语义支持。用 [JSON骨架](assets/reference-map.example.json) 建立输入，修改示例后运行。schema与边界见工具说明；检查通过仅指没发现所定义的结构问题。

默认交付：检索日志、阅读卡和指南卡、文献/研究关联台账、逐句匹配表、已授权的修订句及理由、核验过的参考文献/导出库、未读/冲突/证据缺口清单。报告实际完成的搜索与阅读，区分候选和最终采用。只有用户要求并且检索方法达标时才按PRISMA-S等生成系统综述报告；不会凭网页前几页宣称穷尽证据。整个skill只保存规则和合成模板，不公开未发表稿件、患者记录或私信。
