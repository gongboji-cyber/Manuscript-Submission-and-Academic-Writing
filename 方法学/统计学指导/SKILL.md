---
name: guide-research-methods-statistics
description: >
  Guide and audit medical, biomedical and computational research methodology and statistics. Use for 方法学/统计学指导、研究设计、统计分析方案/SAP、estimand、样本量、偏倚、混杂、缺失数据、配对或聚类分析、诊断准确性、预测模型、AI验证、敏感性分析、可重复性与统计审计. Build a traceable question-to-design-to-estimator-to-evidence workflow; distinguish reporting completeness from methodological validity and risk of bias. Preserve data and register assumptions, deviations and conclusion limits.
---

# 方法学/统计学指导

先界定想回答的问题、独立单位和可识别的目标量，再选择方法。让每项建议能追溯到依据，每项数值能追溯到输入、代码和分析决策。使用中文沟通；按投稿需要生成英文 Methods/Results。不得制造数据、执行结果、预注册记录或已阅读全文的声明。

## 执行工作流

1. **建立输入清单。** 阅读实际方案、数据字典、流程图、已有代码与结果；记录获取日期、版本、哈希、纳排、伦理/数据使用条件。区分设计中、结果已知和复核中；结果已知后撰写的 SAP 必须标为追溯性，不能伪装事前计划。只问影响目标量、独立单位或可识别性的关键缺口；其他工作继续推进。没有数据时交付方案，不填写虚构结果。
2. **冻结问题和目标量。** 明确描述/关联/因果/诊断/预测/决策问题、目标人群、比较、结局、时间零点、随访、分析单位和权重；核实评分的含义和方向，平均评分升高不能自动叫临床获益。临床试验按 ICH E9(R1) 的五项属性写 estimand，区分 estimand/estimator/estimate；说明中间事件策略，不能等同于删除失访。填写 [方案模板](assets/analysis-plan-template.md)，读 [设计分流](references/study-designs.md)。
3. **画清数据生成和信息路径。** 区分患者、就诊、切片、病例-靶点、医院、研究、任务等层级；说明配对、嵌套与交叉依赖。核验参考标准、盲法、时间对齐、混杂、选择机制和训练/验证信息隔离。身份去重依据必须能核查；数据集名称不同不能证明独立。读 [因果和缺失](references/causal-and-missing.md)、[诊断和预测](references/diagnostic-and-prediction.md)。
4. **制定主分析与诊断。** 用 [方法选择](references/statistical-methods.md) 写出目标量、估计方法、假设、样本量依据、失败信号、补救与解释边界。先定义主结局、多重检验族、最小有意义差异/精度目标和探索分析。不得按结果挑主模型、按单变量 P 筛混杂因素、按 Shapiro P 自动切检验或补做 observed power。设计不支持的目标应收窄或停止该项推断。
5. **执行与审计。** 在独立工作目录保留原始数据，只产生派生数据；记录完整命令、代码和输入哈希、环境、种子、收敛/失败/排除、模型版本和输出哈希。先查基础数值和简单基线，再做复杂模型。按 [计算研究规范](references/computational-audit.md) 处理基准比较、消融、仿真与反事实复核。没有执行权限/数据时标“未执行”。不得公开患者级数据、身份字段或访问凭据。
6. **解释与交付。** 报告有效独立样本数、分母、绝对/相对效应及区间；区分 CI/预测区间/可信区间、统计显著性/临床意义、缺乏证据/证据支持等效。给出主分析、同目标量敏感性分析、不同目标量补充分析及其一致性。逐项填写 [48项清单](references/audit-checklist.md) 和 [证据审计模板](assets/evidence-audit-template.md)，结论紧随设计与误差边界。

## 依据与严重性

查询 [来源台账](references/sources.md)，在实际使用时重新核实版本、适用范围和官方原文。已知来源不能替代具体章节；只有摘要时不得推演未读细则。把指南明确要求、教材原则、原始研究证据、本模块经验和当前工作假设分别标注。遇到矛盾说明不同目标量/情境；不得以开源 skill 或期刊档次作为方法有效性的证据。

- **P0：该项推断不可继续。** 例如因果识别不成立却坚持因果结论、无合格参考标准却声称准确性、不可修复测试泄漏。保留描述性结果，说明所需新数据/新设计。
- **P1：影响主结论，先处理或限制。** 例如分析单位错误、主结局缺失机制未处理、预先计划不清、验证精度不足。
- **P2：可追溯性或报告不足。** 例如版本/分母/方法细节缺失；补齐后复核。

这是内部工作优先级，不是官方偏倚评级。清单状态用“有证据支持/需修改/无法判断/不适用”，记录理由和定位；不求总分，不宣称认证。正式使用 QUADAS-3、PROBAST+AI 等工具时另外按对应原版流程作领域判断。CONSORT/SPIRIT/STROBE/TRIPOD/STARD/PRISMA 是报告框架，不能用填报完整性代替设计有效性。

## 可执行工具与边界

要求 Python 3、pandas、NumPy；先核实实际环境，不自动安装第三方项目或付费服务。完整用法在脚本 `--help` 中。

```bash
python -B scripts/audit_inputs.py --data data.csv --config assets/audit-config.example.json --out audit.json
python -B scripts/paired_cluster_bootstrap.py --data paired.csv --cluster-col patient_id --row-key patient_id target_id --a score_A --b score_B --weighting equal_cluster --reps 10000 --seed 2026 --out paired_result.json
```

`audit_inputs.py` 仅检查配置指定的唯一键、缺失、数值范围、同一独立单位跨 split；默认不输出真实 ID，不猜单位或 MAR/MNAR。先修改示例配置中的列名、缺失标记、范围和单位。输出提醒不是自动删除指令；输入列/配置错误应拒绝。

`paired_cluster_bootstrap.py` 仅用于**已经配对的数值 A−B 均值**，按独立 cluster 有放回重抽样。必须声明完整行键和 `equal_cluster`（先求各 cluster 均值再等权）或 `equal_observation`（全部有效行等权，cluster 抽样仍保留组内结构）。默认拒绝缺失；明确允许 complete-case 才运行并报告损失。不能直接求 AUC 差、比例比、模型再训练不确定性、跨医院/跨靶点泛化或因果效应；这些任务必须另写正确估计函数和重抽样方案。百分位区间不是 BCa；少量 cluster 和退化分布须复核，小样本提示不等于已验证校正。仅接受有限数值、至少两个 cluster 和唯一完整行键。

## 联动其他模块

方法学问题先解决再调用 `audit-and-polish-manuscript` 润色；用 `write-manuscript-supplement` 记录详尽方法与敏感性结果；用 `critically-read-literature` 核验方法文献和批判主张；用 `plot-research-statistics` 保留单 panel 代码并导出 800 dpi TIFF/矢量 PDF；用 `format-academic-word` 排版。不能让润色、图形美观或可执行代码替代证据有效性。

## 默认交付

交付研究问题与 estimand 卡、带版本的 SAP、问题优先级和证据定位、分析/诊断/敏感性结果、运行清单及可复核代码、填写后的 checklist、可直接使用的 Methods 和受约束的 Results/结论。没有数据时交付未执行的方案与待补资料，不能暗示审计已完成。
