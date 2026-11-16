# 四项请求的交付结果

依据本案例的合成材料，先读取仓库根入口，再按任务选择必要模块。四项互相独立；没有联网、安装、重跑统计分析、操作账号、修改技能或覆盖输入。此文件是合并交付记录；W01本身未另行生成文稿文件。

## W01：局部英文检查

原句已经清楚、准确，无需润色，可直接保留：

> The mean paired difference was 0.020 (95% confidence interval, −0.005 to 0.045).

实际检查：语法、paired difference术语、点估计、区间端点与负号，以及不确定性的保留。原句没有把点估计写成确定优势，无需添加解释或改数字。这里仅完成这一句的语言与保真检查；没有核实底层统计计算，也未审查全文、结局单位或期刊格式。

## W02：按analysis-v2修订两句并标出同步项

Results可直接替换为：

> With patients weighted equally, the mean paired difference between Method A and Method B (A−B) was 0.020 (95% CI, −0.005 to 0.045).

Cover letter贡献句可直接替换为：

> Our study quantifies the paired difference between Methods A and B using equal patient weights (mean A−B difference, 0.020; 95% CI, −0.005 to 0.045).

两句都以作者指定的analysis-v2汇总为当前事实集合。修订把v1的0.035和0.010至0.060替换为v2数值，保留A−B方向、患者等权和区间跨零的不确定性。现有材料不支持“superior”或“demonstrably improves clinical outcomes”；没有结局名称、单位或临床获益证据，不能自行补入。跨零区间也不能改写成已证明无差异、等效或非劣。

| 材料/成果 | 依赖与当前状态 | 需要同步的动作及完成条件 |
| --- | --- | --- |
| analysis-v2汇总 | 作者指定当前版本；数值和配对修复仅为报告信息，未独立验证 | 后续若要确认分析正确性，需要对应源数据、代码/分析设定和运行日志；本次不重跑 |
| 修订Results句 | 依赖v2；局部文字更新已完成 | 已按给定汇总核对数值、方向、等权条件与主张强度；不等于数值复现 |
| 修订cover letter贡献句 | 依赖v2及Results；局部文字更新已完成 | 与修订Results一致；全文附信、作者声明和期刊要求未审查 |
| Figure2.pdf | 已知仍引用v1；结果依赖已过期，实际图未提供 | 取得可编辑源文件和图后，把相关估计与区间同步到v2，核对图注、A−B方向、单位及分析身份，再重新导出和视觉检查。本次未改图，不能宣称图已通过 |
| Supplement-v1 | 已知仍引用v1；结果依赖已过期，补充正文未提供 | 取得正文/表格后，核对并更新受影响的方法、等权与配对单位说明、结果、表图及交叉引用，保存对应新版本；不能猜具体页码或声称补充已改完 |
| 其他可能引用相关结果的位置 | 文件/内容未提供，是否受影响待核 | 定向查标题、摘要、其他Results/表格/图注、Discussion、Conclusion及投稿字段中同一比较和优势/临床获益主张；只同步确实依赖v1或越界主张的内容 |

实际核查仅为“给定汇总→两句文字”的数值和语义对照。投稿前自检模块的R03/R08及附信模块的L05/L08/L10所涉及的局部表达已修订；R07跨材料一致性仍未完成，因为Figure2.pdf与Supplement-v1尚待同步。未把“作者报告已修复配对单位”视作源数据或代码验证成功。没有生成Word，也未沿用未知的旧图或补充核验状态。

## W03：候选引用与主张支持判断

该候选记录不能支持原句：

> X causes Y in all patient populations.

原句同时要求因果证据和对所有患者人群的普遍适用证据；提供的摘要线索只有关联，没有满足这两种要求。这里判定的是“所给材料不足以支持原句”，不是认定X不可能导致Y，也不是认定未取得的全文一定没有更强证据。

| 记录/主张 | 实际依据和读取范围 | 处理 |
| --- | --- | --- |
| R-W03-01：Example Association Study；DOI原字段10.0000/synthetic | 只有用户给出的候选元数据和摘要线索；未取得或阅读原始摘要、原文及补充 | 保留为候选，不补作者、期刊、年份、页码或推荐等级 |
| 身份与状态 | 工具显示“DOI解析成功”是提供的工具结果；本次未自行解析，也未核对题名/DOI对应、发表版本、勘误或撤稿状态 | 身份核验未完成；解析成功不能替代身份一致性或内容证据核查 |
| C-W03-01a：X causes Y | 线索仅为X与Y有关联，设计及因果识别条件未知 | 不支持从现有材料作因果表述；全文层级内容未评估 |
| C-W03-01b：in all patient populations | 人群、场景及外部验证范围均未提供 | 不支持普遍外推；未评估具体适用人群 |

基于目前线索，可直接用于工作记录的克制表述是：

> The available abstract summary suggests an association between X and Y; causal effects and applicability across patient populations remain unverified.

如果后续能核对原始摘要确实报告该关联，并明确研究对象，可把稿件背景句收窄为：

> An association between X and Y was reported in the population studied.

第二句是待核候选句，现阶段不要把它与R-W03-01一起列成“已核验最终引文”。对当前原句应删除因果/全人群断言，或在缺少证据时暂不采用；不要贴上可解析DOI来维持原断言。后续解除条件是取得足够的原始摘要/全文及必要补充，核实身份、研究设计、人群、结果与限制，再决定引用是否可用于限定背景表述或更强主张。本次遵照要求未检索真实文章，也未声称阅读全文。

## W04：UNITROWS/1实际转换与错误处理

已完整读取本案例的format.md（版本1，内部合成说明），并实际读取input.unitrows与duplicate.unitrows。格式来源仅为该说明，不引入外部行业规范。关键规则是精确两行标头、每行两列、非空且唯一的原样ID、有限实数或完全匹配NA，以及mm÷10转cm。

代码为[convert_unitrows.py](convert_unitrows.py)，只使用Python标准库。它先校验整份输入，再打开输出，拒绝非法记录时不静默丢行；ID保持字符串，通过csv.writer处理CSV转义。使用Decimal并直接调整十进制指数，避免二进制浮点或默认精度舍入改变数值。数值词法支持普通带符号十进制、小数和科学计数法；不把未定义的注释、空行或扩展语法当作合法输入。

实际执行：

```bash
python -B /workspace/scratch/46b39df32326/skill-optimization-20261011/evaluation-b/output/convert_unitrows.py /workspace/scratch/46b39df32326/skill-optimization-20261011/evaluation-b/materials/input.unitrows /workspace/scratch/46b39df32326/skill-optimization-20261011/evaluation-b/output/input.csv
python -B /workspace/scratch/46b39df32326/skill-optimization-20261011/evaluation-b/output/convert_unitrows.py /workspace/scratch/46b39df32326/skill-optimization-20261011/evaluation-b/materials/duplicate.unitrows /workspace/scratch/46b39df32326/skill-optimization-20261011/evaluation-b/output/duplicate.csv
python -B /workspace/scratch/46b39df32326/skill-optimization-20261011/evaluation-b/output/check_unitrows.py
```

正常转换命令退出0，生成[input.csv](input.csv)，内容已回读：

```csv
id,value_cm
01,1.0
02,NA
03,2.5
```

1.0与1表示相同数值；ID前导零和NA均保留。重复ID命令退出2，实际错误为`ERROR: line 4: duplicate ID '01'`，没有生成duplicate.csv。

[check_unitrows.py](check_unitrows.py)实际运行退出0，22项检查通过，0项失败；明细保存于[validation.json](validation.json)。

| 检查范围 | 实际结果 |
| --- | --- |
| 3行、CSV列名、01/02/03、10→1与25→2.5、NA不转0 | 通过 |
| 0、负数、小数、科学计数法、逗号ID的CSV转义、长十进制精确换算 | 通过 |
| 错误版本/列标头、过多/过少列、空行、空ID、重复ID | 全部拒绝；错误时保留已有输出哨兵内容 |
| NaN、inf、−Infinity、na、带空格NA、空值 | 全部拒绝；错误时保留已有输出哨兵内容 |
| 输入输出同路径 | 拒绝 |
| 提供的输入与说明在边界检查前后SHA-256一致 | 通过；所有派生测试材料仅写output |

已解决本案例的解析、单位和错误处理问题。验证是该版本说明下的技术转换检查，不构成统计分析、医学证据或其他格式版本的认证；未测试超大文件性能、异常断电时的输出原子性或未规定的扩展语法。所有源材料保持不变。

实际读取资源、命令和检查摘要见[run-log.json](run-log.json)。没有提供的token、费用或科学复现结果未估算。
