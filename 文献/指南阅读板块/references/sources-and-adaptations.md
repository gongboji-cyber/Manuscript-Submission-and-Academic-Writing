# 来源、融合取舍与实际读取范围

核查日期：2026-10-09。下面是构建本模块的依据，不是某一医学问题的完整文献检索。原创中文流程、模板和脚本分别吸收可复核结构与长期项目经验；未复制第三方完整技能、代码、文献全文或个案材料。参考格式按组织/作者、题名、版本、官方入口及读取范围记录；实际研究需要补充对应原文、版本与获取日期。

## 官方来源

| ID | 来源/官方入口 | 本次读取范围 | 采用与边界 |
|---|---|---|---|
| S01 | National Library of Medicine. “PubMed User Guide.” 页面最近更新2026-09-30，[官方帮助](https://pubmed.ncbi.nlm.nih.gov/help/) | 检索概念、字段/ATM、日期、导出和全文发现相关段落 | 原生查询与记录字段；网站发现不冒充完整数据库检索，索引/过滤不能保证全部召回 |
| S02 | International Committee of Medical Journal Editors. “Preparing a Manuscript for Submission to a Medical Journal.”，[References段](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html) | References与主张边界段落 | 原始来源、引用身份与支持、撤稿/预印本标记、期刊具体格式；不是“文献越多越好”或自动证明科学有效 |
| S03 | Crossref. “REST API.”，[官方文档](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)及[使用说明](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/) | 元数据接口、works及分页/范围用途 | 登记元数据为身份核查一层；404/未收录不证明不存在，无DOI仍可有真实来源，不把创建/更新日期当发表年 |
| S04 | Crossref. “Crossmark.”，[官方说明](https://www.crossref.org/documentation/crossmark/) | 更新/撤稿用途和不能保证内容正确的说明 | 状态渠道之一；有/无按钮不自动保证无更新，核对实际通知及受影响内容 |
| S05 | National Library of Medicine. *Citing Medicine*与[Sample References](https://www.nlm.nih.gov/bsd/uniform_requirements.html) | 官方Sample References读到作者/期刊/不同文献类型示例；未通读整本Citing Medicine | 期刊缩写和医学引用进一步核对入口；不把常见Vancouver规则强加给所有期刊 |
| S06 | Rethlefsen ML et al. “PRISMA-S: an Extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews.” *Systematic Reviews*, vol.10, 2021, article39；[EQUATOR](https://www.equator-network.org/reporting-guidelines/prisma-s/) | 官方用途/版本与文献信息，不代替逐条阅读全部原清单 | 系统综述检索报告；普通补引用可借日志结构但不得宣称系统综述 |
| S07 | AGREE Next Steps Consortium. *AGREE II: User’s Manual and 23-item Instrument*. 2009, updated2017；[官方工具页](https://www.agreetrust.org/resource-centre/agree-ii/)，[官方PDF](https://www.agreetrust.org/wp-content/uploads/2017/12/AGREE-II-Users-Manual-and-23-item-Instrument-2009-Update-2017.pdf) | 官方PDF可读；用途/操作范围相关部分，未对任何具体指南评分 | 指南制定过程/透明度评价；不自动证明推荐正确，不借本模块清单声称完成AGREE II |
| S08 | Chen Y et al. “A Reporting Tool for Practice Guidelines in Health Care: The RIGHT Statement.” *Annals of Internal Medicine*, vol.166, no.2, 2017, pp.128–132；[EQUATOR](https://www.equator-network.org/reporting-guidelines/right-statement/) | 官方用途与发表信息 | 指南报告工具，不能当临床建议有效性认证 |
| S09 | GRADE Working Group. [官方主页与资源](https://www.gradeworkinggroup.org/) | 官方概念介绍/资源入口，未对体证据评级 | 证据确定性与推荐强度分开；不自创等级换算或给单篇研究机械GRADE分 |
| S10 | NLM. [当前pubmed_250101 DTD文档](https://dtd.nlm.nih.gov/ncbi/pubmed/doc/out/250101/index.html) | NLM官方2026基线公告确认仍使用pubmed_250101.dtd；读取DTD文档入口，解析实现另对合成输入实测；旧[字段说明页](https://www.nlm.nih.gov/bsd/licensee/elements_descriptions.html)已停止维护，未把它当现行规范 | 原创解析器处理期刊记录与有限字段；不承诺支持全部PubMed/Books对象，复杂导出需核查实际结构 |

## GitHub调研与独立融合

### O01 K-Dense-AI/scientific-agent-skills

固定commit：`92ace75ac21efe19a620434e0ca4e356081fe807`。

阅读[文献综述skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/92ace75ac21efe19a620434e0ca4e356081fe807/skills/literature-review/SKILL.md)、[引用管理skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/92ace75ac21efe19a620434e0ca4e356081fe807/skills/citation-management/SKILL.md)及citation_validation/search_and_citation相关资源。技能元数据和仓库[LICENSE.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/92ace75ac21efe19a620434e0ca4e356081fe807/LICENSE.md)均标MIT（其他技能仍需逐项核查）。借鉴多阶段检索、记录/报告/研究区分、元数据与内容支持分离、保留实际覆盖范围。

没有移植付费parallel/OpenRouter依赖、AI图形、软件版本断言或每次必须多数据库/预印本的硬规则；按实际问题选择工具。开源技能中的自引指令不成为我们医学稿件默认引文，只有实际相关贡献、身份核实和用户授权范围才考虑软件引用。脚本重新用标准库独立实现，不把格式验证叫科学验证。

### O02 Laszlo75/literature-search

固定commit：`a73fc0ade07f58b97296b2b4a9c8a091f62b0272`。

阅读[SKILL.md](https://github.com/Laszlo75/literature-search/blob/a73fc0ade07f58b97296b2b4a9c8a091f62b0272/SKILL.md)的指南发现、即时元数据台账、引用核查及冲突处理流程；[LICENSE](https://github.com/Laszlo75/literature-search/blob/a73fc0ade07f58b97296b2b4a9c8a091f62b0272/LICENSE)为CC BY-NC4.0，不是MIT。这里只比较公开工作流程和独立记录取舍，未移植受许可约束的代码/模板/表达，不重新许可该项目。以后直接复用必须另核查许可、署名与非商业限制。

有用启发：指南版本、内容与书目信息边取边登记，减少依靠模型记忆造成DOI/作者漂移。舍弃固定UK/NHS背景、近5年/15–30篇/预印本12个月限制、“PubMed每个字段永远优先”、无PubMed MCP即停止、摘要+片段通常足够正式评估以及只查标题判断撤稿。上传PDF仍需更新核查；核验查过的完整来源，不机械强迫对未变元数据重复联网。

## E：本项目经验

- COPD曲霉病：yield/accuracy、诊断标准、参考标准独立性和证据人群不可混用；方法评价不等于个体治疗推荐。
- 公开模型评估：同一任务的评分增益不等于临床获益；prompt/GT可见性、划分、原始pipeline和adapter版本决定方法引用适用范围。
- 公共数据与代码审计：名字不同不证明研究独立，静态代码不能单独证明数值影响，软件旧/新版解释必须依确切版本和运行范围。
- Letter和原作者回复：录用不证明每条批评，回复/勘误可能改变最强可支持主张；同时找反证，已澄清问题撤销或收窄。
- 投稿润色：保护数字、限定词、主张与引用锚点；不给缺证据句找“像”的引用，也不用高档期刊代替内容阅读。

这些为工作经验，不是上述组织逐字要求。每次实际应用重新核对临床指南、元数据服务和投稿格式变化；开放source title/URL/版本与实际阅读范围，不能用长来源表假装已读完所有全文。
