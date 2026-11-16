# 四个合成请求的执行结果

本仓库未发现根 `skills/SKILL.md`；本次按任务选择局部润色、附信和文献匹配模块。仅使用提供的合成材料；未联网、安装、操作账号、修改技能或重跑统计分析。W01—W03的文字结果汇总于此，不另生成图、Word或独立任务文件。

## W01：仅检查一句英文

无需润色，可直接使用原句：

> The mean paired difference was 0.020 (95% confidence interval, −0.005 to 0.045).

实际检查：句子语法、统计量名称和区间表达清楚；0.020、−0.005、0.045及配对差含义均保留。仅完成该句语言检查，未做全稿审查或统计正确性认证。

## W02：以作者指定的analysis-v2修订两句

**Results修订句：**

> In analysis-v2, with equal weighting of patients, the mean paired difference between Methods A and B (A − B) was 0.020 (95% CI, −0.005 to 0.045).

**Cover letter贡献句：**

> Our study provides a paired comparison of Methods A and B with equal weighting of patients, yielding an estimated mean difference (A − B) of 0.020 (95% CI, −0.005 to 0.045); the confidence interval spans zero.

实质变化：按作者指定的v2，将0.035和0.010–0.060替换为0.020和−0.005至0.045，明确A−B与患者等权；撤去“was superior”及“demonstrably improves clinical outcomes”。区间同时包含负值、零和正值，不能据此确定A优于B，也不能改成两者等效、无差异或已证实没有临床获益。提供材料未说明结局本身、方向解释或临床重要性阈值，故不添加相关结论。

| 需同步材料 | 具体动作 | 当前完成边界 |
| --- | --- | --- |
| Figure2.pdf | 根据v2核对并更新相关点估计、区间、比较标签、图注和优势描述；生成后检查最终图 | 仅收到文件身份及仍用v1的说明，未提供或查看图，未修改 |
| Supplement-v1 | 更新关联结果、配对单位、患者等权说明和版本引用；另存与v2对应的新补充版本，保留旧版历史 | 未提供补充正文，不能定位具体表、节或页；未修改 |
| 标题、摘要、讨论、结论及正文其他结果位置 | 若引用旧数值或确定优势/临床获益，统一至v2及其不确定性 | 未提供这些文本，列为待同步，不声称发现了具体旧值 |
| Methods、图表源数据或生成配置、结果台账 | 根据实际v2分析材料说明配对修复与权重；记录当前版本及旧版撤换范围 | 未提供源数据、代码或运行日志，不能核实实现或代写细节 |
| 完整cover letter与投稿系统相关摘要/贡献字段 | 若含同一主张，同步修订后的证据范围 | 本次只修订已给贡献句，未核全文或提交字段 |

实际复核：两句均与作者提供的v2汇总数字、符号、区间、A−B和等权条件一致（相关R03、R08、W02—W03；附信L05、L08、L10）。已给原文的数字与当前v2报告不一致，已在授权文字中修正。Figure2和Supplement的旧版状态仅来自用户说明。v2修复配对单位属于作者报告，未独立确认；仅有汇总报告，故未复现或认证估计值、区间算法及修复正确性。未改图、生成Word或重跑分析。

## W03：候选记录不能支持因果和全人群断言

目前不能用该候选记录支持：

> X causes Y in all patient populations.

| 检查轴 | 实际材料与判定 |
| --- | --- |
| 文献身份 | 仅有题名Example Association Study、原始DOI字段10.0000/synthetic及工具“解析成功”的报告。解析成功不证明DOI与该题名正确对应，更不证明作者、发表版本或更正/撤稿状态已核实；身份仍待核。也不能据其合成DOI直接断言记录无效或不存在。 |
| 阅读范围 | 实际仅读取案例给出的候选元数据与摘要线索。未取得摘要全文、原文或补充，未阅读全文。 |
| C01：X导致Y | 已提供线索只提示关联，不能升级为因果；必要研究设计、时间顺序、识别假设和分析未提供。对原因果主张不能采用该引用；全文层面的支持未评估。 |
| C02：所有患者人群 | 人群范围及外部适用性未提供，“all patient populations”没有证据支持，不能由一条关联摘要外推。 |
| 可保留的窄主张 | 仅限“摘要线索报告X与Y有关联”，不能给效应量、方向、推荐等级或特定人群标签。 |

当前可直接使用的透明表述：

> According to the available abstract summary, X was reported to be associated with Y.

这句只报告现有摘要线索，不能冒充已核验的全文研究结论。若用于最终稿，先取得并核对真实摘要和文献身份，再按其明确的人群及条件写关联句；若因果或普遍适用是核心论点，则需取得足够原文/补充及相应因果与外部适用性证据，否则删除或收窄该论点。

引用处理：保留为候选记录R01，原始题名和DOI字段原样保留；身份标“待核”、发表状态“未查”、阅读范围“候选元数据/摘要线索”，原句的引用动作“暂缓采用”。不纳入已核验最终参考文献表，不补作者、年份、期刊、卷页、推荐等级或全文定位。当前不联网寻找真实文章；无法完成身份、版本、更正/撤稿及全文证据核验。相关检查L11—L18、L27—L32、L36中，阅读边界已明确，身份与必要全文仍无法判断，原句需修改。

## W04：实际读取内部说明、编写和执行转换

依据实际读取的`materials/format.md`，UNITROWS/1只用于本合成案例；未引用或编造外部标准。

已交付标准库转换代码：[convert_unitrows.py](convert_unitrows.py)，实际运行：

```bash
python -B output/convert_unitrows.py materials/input.unitrows output/input.csv
python -B output/convert_unitrows.py materials/duplicate.unitrows output/duplicate.csv
python -B output/check_conversion.py
```

正常输入执行退出码0，生成：[input.csv](input.csv)。内容为：

```csv
id,value_cm
01,1
02,NA
03,2.5
```

转换代码先检查全部输入行，再以不覆盖已有文件的方式写CSV。ID作为字符串原样保留；`NA`严格匹配并保留；有限十进制数将指数减一，实现mm→cm而不经二进制浮点或小数上下文舍入。CSV通过标准库writer处理需引号的ID。标头错误、列数错误、空ID、重复ID和无效/非有限数值均拒绝，不静默丢行。

重复ID输入实际退出码2：

```text
ERROR: line 4: duplicate ID '01'
```

未生成`duplicate.csv`，没有部分成功输出。边界检查脚本：[check_conversion.py](check_conversion.py)；详单：[checks.json](checks.json)。实际19项检查全部通过：

| 检查内容 | 实际结果 |
| --- | --- |
| 正常输入、CSV表头、01/02/03前导零、10→1、25→2.5、NA | 全部符合预期；再次执行独立输出一致 |
| 附带重复ID样本 | 拒绝、退出2、无CSV |
| 非法版本标头、错误列名、三列、空ID、空行、空值 | 均拒绝、退出2、无CSV |
| NaN、Infinity、−inf、na、NA后附空格 | 均拒绝、退出2、无CSV |
| 负值、零、科学计数法、含逗号ID、带空格ID、长精度小数 | 转换正确；ID原样保留且CSV可正确回读；十进制精度保持 |
| 已存在目标文件 | 拒绝覆盖，原输出字节不变 |
| 提供的cases.json、format.md及两份UNITROWS输入 | 检查执行前后SHA256一致，输入保留 |

执行环境为Python标准库，实际Python版本及脚本/输入/CSV哈希记录在checks.json与run-log.json。所有脚本、CSV、测试夹具和记录仅写本output目录；未作统计分析。检查覆盖本说明及列出的边界，不声称完成未提供的其他格式规范验证。
