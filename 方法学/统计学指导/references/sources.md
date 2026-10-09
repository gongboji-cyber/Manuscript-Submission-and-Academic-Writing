# 来源台账与使用边界

核查日期：2026-10-09。链接以官方组织、作者入口、原始论文或其 PubMed/作者存档为准。以下不代表逐页读完所有教材或通过正式工具认证。记录实际可读范围；正文受限时只采用可核实信息。指南的完整表格和评分规则请阅读原版，不从本模块反向重建。实际研究须再次核查更新及适用扩展。

## 教材、声明与指南

| ID | 来源/版本与入口 | 本次可读范围 | 纳入原则及边界 |
|---|---|---|---|
| S01 | Hernán MA, Robins JM. *Causal Inference: What If*. Chapman & Hall/CRC, 2020；[作者更新入口](https://miguelhernan.org/whatifbook) | 作者页面、书的三部分结构；当前PDF链接访问失败，未通读 | 因果目标、设计/识别先于估计的教材入口；具体DAG/g-methods实现再读取相应正文，不用书名代替证明 |
| S02 | Harrell FE. *Regression Modeling Strategies*，[作者在线课程笔记](https://hbiostat.org/rmsc/)，重点[Missing Data](https://hbiostat.org/rmsc/missing)、[Multivariable](https://hbiostat.org/rmsc/multivar)、[Survival](https://hbiostat.org/rmsc/surv)、[Cox](https://hbiostat.org/rmsc/cox)与[Validation](https://hbiostat.org/rmsc/validate) | 相关章节可读网页，缺失概念、建模复杂度与重抽样验证段落；生存/Cox读取章节结构；不是通读付费教材 | 缺失机制假设、建模和完整流程验证；不把课程举例的重复数/建议当通用硬阈值 |
| S03 | James G, Witten D, Hastie T, Tibshirani R, Taylor J. *An Introduction to Statistical Learning with Applications in Python*. 2023；[作者书站](https://www.statlearning.com/)；R版第二版2021 | 作者书站版本/章节目录，未通读PDF | 为重抽样、收缩、学习方法提供进一步阅读入口；不声称教材直接验证本工具 |
| S03b | OpenIntro. *OpenIntro Statistics*；[官方书页](https://www.openintro.org/book/os/) | 官方获取页面，未通读正文；不锁定页面未明确核实的版次 | 基础概率、抽样和推断学习入口；复杂医学设计不能只靠基础检验章节 |
| S04 | ICH E9(R1), 2019 Step4. *Addendum on Estimands and Sensitivity Analysis*；[官方PDF](https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf) | 可读官方PDF，A.3 estimand属性和中间事件及敏感性相关段落 | 区分目标量/估计方法/数值、中间事件策略、敏感性与补充分析；临床试验范围，非试验使用属明确标注的概念迁移 |
| S05 | Wasserstein RL, Lazar NA. *The ASA Statement on p-Values: Context, Process, and Purpose*. 2016；doi:10.1080/00031305.2016.1154108；[ASA官方声明](https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf) | 官方3页声明及六原则 | P值非假设为真概率/效应大小，解释结合设计、估计与透明报告；不是禁用P值 |
| S06 | CONSORT 2025；BMJ 388:e081123；[EQUATOR官方入口](https://www.equator-network.org/reporting-guidelines/consort/) | 官方版本/适用设计/文献信息 | RCT报告完整性；不替代随机化或偏倚评价，扩展另查 |
| S07 | SPIRIT 2025；[官方已发表声明](https://www.consort-spirit.org/published-statements)，[EQUATOR入口](https://www.equator-network.org/reporting-guidelines/spirit-2013-statement-defining-standard-protocol-items-for-clinical-trials/) | 官方版本与协议用途，旧URL不代表仍是2013最新版 | 前瞻方案报告；结果已知后补写不能叫事前注册 |
| S08 | von Elm E et al. STROBE. 2007；Ann Intern Med 147:573–577；[EQUATOR](https://www.equator-network.org/reporting-guidelines/strobe/) | 官方用途和文献信息 | 观察性报告；不保证控制混杂或因果识别 |
| S09 | Collins GS et al. TRIPOD+AI. BMJ 2024;385:e078378；[EQUATOR](https://www.equator-network.org/reporting-guidelines/tripod-statement/) | 官方用途/版本及原始论文检索文本 | 预测模型报告；不当作方法设计处方或偏倚评分 |
| S10 | Sounderajah V et al. STARD-AI. Nat Med 2025；doi:10.1038/s41591-025-03953-8；[EQUATOR](https://www.equator-network.org/reporting-guidelines/the-stard-ai-reporting-guideline-for-diagnostic-accuracy-studies-using-artificial-intelligence/) | 官方用途/发表信息 | AI诊断准确性报告；普通诊断研究仍查STARD 2015及适用扩展 |
| S11 | QUADAS-3, 2026；doi:10.7326/ANNALS-25-02104；[Bristol官方工具页](https://www.bristol.ac.uk/population-health-sciences/projects/quadas/quadas-3/quadas-3-tool/) | 官方页面六阶段、四领域、accuracy-estimate层面和v1.2下载信息；未逐条执行完整工具 | 按研究问题/准确性估计评审偏倚与适用性；不能机械延用QUADAS-2或把本清单当官方工具 |
| S12 | Moons KGM et al. PROBAST+AI. BMJ 2025;388:e082505；doi:10.1136/bmj-2024-082505；[PubMed](https://pubmed.ncbi.nlm.nih.gov/40127903/) | PubMed摘要；BMJ正文403 | 区分开发质量与评价偏倚/适用性；正式判断需完整工具，不从摘要制造细则 |
| S13 | Page MJ et al. PRISMA 2020. BMJ 2021;372:n71；[EQUATOR](https://www.equator-network.org/reporting-guidelines/prisma/) | 官方用途/版本及文献信息 | 系统综述报告；不是原始研究方法评价，不代替设计对应偏倚工具 |

## 综合方法手册与医学统计报告补充

| ID | 来源/版本 | 读取范围与采用原则 | 边界 |
|---|---|---|---|
| S18 | Higgins JPT et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*；[官方入口](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current)，[变更页](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/versions-and-changes-handbook) | 官方主页面标6.5(2024)，变更页记录6.5.1(2025/2026)；第10章入口与综述分析路径 | 正式合并前读取适用章，按章节实际版本/日期引用；不能把主页面版本标签当全部修订已核对，不能推广为所有研究通用分析公式 |
| S19 | Lang TA, Altman DG. SAMPL；Int J Nurs Stud 2015;52:5–9；[EQUATOR入口](https://www.equator-network.org/reporting-guidelines/sampl/)，[官方PDF](https://www.equator-network.org/wp-content/uploads/2013/07/SAMPL-Guidelines-6-27-13.pdf) | 基础统计方法/结果报告PDF相关部分；明确方法、分母、效应、不确定性 | 补充医学统计报告完整性，不作为模型选择或偏倚认证 |

## 原始方法研究

| ID | 论文与稳定入口 | 实际读取与实施 | 适用边界 |
|---|---|---|---|
| S14 | Riley RD et al. *Calculating the sample size required for developing a clinical prediction model*. BMJ 2020;368:m441；doi:10.1136/bmj.m441；[原始论文](https://www.bmj.com/content/368/bmj.m441) | 原始论文检索摘要/正文片段；采纳参数数、结局频率、预期解释度与收缩等共同决定样本需求 | 不是固定10 EPV；不是外部验证或所有算法的统一公式，具体计算须核实全文与目标模型 |
| S15 | Sterne JAC et al. *Multiple imputation for missing data in epidemiological and clinical research: potential and pitfalls*. BMJ 2009;338:b2393；doi:10.1136/bmj.b2393；[PubMed](https://pubmed.ncbi.nlm.nih.gov/19564179/) | 元数据/摘要；PMC正文访问被拦截 | 作为MI专门进一步阅读；本模块缺失实施原则同时由S02支撑，不把摘要当MI全教程 |
| S16 | Van Calster B et al. *Calibration: the Achilles heel of predictive analytics*. BMC Med 2019;17:230；doi:10.1186/s12916-019-1466-7；[PubMed](https://pubmed.ncbi.nlm.nih.gov/31842878/) | 原始作者/期刊摘要检索文本，强调校准评价 | 不能凭该综述证明某算法或本数据已校准；具体方法读全文 |
| S17 | Morris TP, White IR, Crowther MJ. *Using simulation studies to evaluate statistical methods*. Stat Med 2019;38:2074–2102；doi:10.1002/sim.8086；[作者预印本全文](https://arxiv.org/html/1712.03198v3) | 作者公开全文ADEMP/表现指标/Monte Carlo不确定性相关部分；PMC访问受限 | 仿真情景内的方法评估，不是方法普遍优越证明；参数与失败机制必须具体化 |

## 开源 skill：借鉴结构，独立实现

代码和中文流程为本模块原创；未整段复制外部 SKILL.md/脚本。开源技能不是医学方法权威，不因star数背书。若以后直接复用代码，逐文件核查许可证并保留所需版权与许可；不要假定仓库许可证覆盖所有技能。

- **O01 K-Dense-AI/scientific-agent-skills**：核查commit `92ace75ac21efe19a620434e0ca4e356081fe807`；读取 [statistical-analysis](https://github.com/K-Dense-AI/scientific-agent-skills/blob/92ace75ac21efe19a620434e0ca4e356081fe807/skills/statistical-analysis/SKILL.md)、[scientific-critical-thinking](https://github.com/K-Dense-AI/scientific-agent-skills/blob/92ace75ac21efe19a620434e0ca4e356081fe807/skills/scientific-critical-thinking/SKILL.md)、[statsmodels](https://github.com/K-Dense-AI/scientific-agent-skills/blob/92ace75ac21efe19a620434e0ca4e356081fe807/skills/statsmodels/SKILL.md)相关流程。借鉴设计/单位优先、因果与预测分流、模型诊断和证据边界；statsmodels技能标BSD-3-Clause，仓库MIT，其他技能按各自元数据核查。未移植版本号断言、外部付费/AI绘图服务或APA固定输出。
- **O02 TerryFYL/claude-statistical-analysis-skill**：核查commit `82d104228d4f30988476d3a5f0c392565c916410`；读取 [SKILL.md](https://github.com/TerryFYL/claude-statistical-analysis-skill/blob/82d104228d4f30988476d3a5f0c392565c916410/SKILL.md) 数据画像、分流、样本量与结果输出部分及 [MIT LICENSE](https://github.com/TerryFYL/claude-statistical-analysis-skill/blob/82d104228d4f30988476d3a5f0c392565c916410/LICENSE)。借鉴输入画像/分层工作流；明确不采用Shapiro/Levene P自动切换、任意默认中效应、凭总N宣告充分、显著性驱动中介结论与固定图形风格。

## 项目经验与知识更新

来源类别 **E：本项目经验** 包括：患者/病例-靶点依赖、配对与权重先定义、canonical身份与跨划分审计、reference standard和yield/accuracy分离、GT-free与oracle路径、静态代码与运行证据分离、最小反事实修复、阴性/条件性结果分支、失败登记、可复核数值/图表一致性。这些是可审计工作规则，不能装成权威教材的逐字要求。

每次正式分析补充具体章节、版本、访问时间、采纳规则和边界。新指南改变适用规则时更新本台账、受影响工作流和对应清单，旧SAP保留版本，不回写既往承诺。
