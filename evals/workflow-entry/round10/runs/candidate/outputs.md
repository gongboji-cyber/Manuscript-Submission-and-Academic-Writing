以下裁决仅基于给定合成事实与候选 skill 规则；未联网、未下载数据、未运行分析或模型、未修改仓库。

## T1：公开多组学数据筛选开题课题

**Stable skill 与顺序**

1. `coordinate-research-workflow`：锁定本轮授权、材料版本和停止条件。
2. `research-topic-selection`：主模块；完成 L0 目录盘点、L1 语义聚类、L2 可证伪命题构建，并仅对少量存活者进入有界 L3 风险核验。
3. `retrieve-and-match-references`：候选形成后触发 G1；检索最近邻、反证和数据说明，记录 `metadata-only / abstract-read / methods-results-read / full-text-and-supplement-reviewed`。
4. `critically-read-literature`：仅当某篇最近邻可能决定创新性或包含关键设计细节时触发，核查其 Methods、Results、相关 Supplement 和主张边界。
5. `guide-research-methods-statistics`：仅对通过初步 G0/G1 的候选触发 G2；分别冻结可识别的 estimand、独立单位、观测映射和识别假设。不同方法没有共同 estimand 时不得强造“统一排名”。
6. 回到 `research-topic-selection`：在授权范围内核验数据字典、真实联结键和小样例，记录 G3 的初步状态；可以起草 G4 试点协议，但不得执行。

**本轮可达到的上限**

最多完成 L0–L2，并对少量候选做有界 L3：题录/摘要核验、数据目录与小样例字段核验、联结键候选确认、局部 join 演练和来源谱系草图。若完整联合交集需要全量文件，只能标 `UNKNOWN/NOT_TESTED`。

当前材料不能证明：

- G1：摘要不足以证明最近邻未覆盖；
- G2：尚无候选级 estimand、独立单位和识别假设；
- G3：未核实 `N0 → N_key → N_label → N_independent → N_eval`；
- G4：尚不能冻结公平、可否证的试点。

**当前裁决/停止点**

- 组合层面：`NO_GO_YET`。
- 尚未形成具体命题者：`EXPLORE_ONLY`。
- 已形成但被 G1–G3 缺口阻断者：`HOLD_NEED_EVIDENCE`。
- 不得进入 `GO_MINIMAL_PILOT`；目录很大不等于可分析交集大，也不能把未核实交集写成 0。

**仍缺证据**

最近邻全文与补充材料；候选级估计量；独立单位；真实 join key；去重规则；联合交集和逐步分母；标签有效性与缺失机制；训练/调参/测试/参考标准谱系；许可；泄漏检查；有效事件数与精度；强基线和冻结结果树。

**未执行动作**

未批量下载、未全量 join、未训练模型、未运行正式或最小试点、未生成经验结果、未宣称创新或数据适格。本次也未实际联网检索。

---

## T2：将同一队列三模型内部 AUC 差异解释为机制发现

**Stable skill 与顺序**

1. `coordinate-research-workflow`：限定为候选审计，不执行分析。
2. `research-topic-selection`：先审 G0/G2，区分“预测判别差异”和“机制识别”。
3. `retrieve-and-match-references`：若考虑保留更窄命题，先补读最近邻 Methods、Results、相关 Supplement，完成 G1 主张级对照。
4. `critically-read-literature`：建立“机制主张—AUC证据”图，检验最强作者解释和替代机制。
5. `guide-research-methods-statistics`：仅在重构为预测比较后触发；冻结共同 estimand、观察单位、配对比较、强基线、信息公平和泄漏图。
6. 回到 `research-topic-selection` 给唯一裁决。

**当前裁决/停止点**

对“内部 AUC 差异即新机制发现”这一原命题：`STOP`。

理由不是最近邻摘要相似，而是 G2 的结构性问题：AUC 衡量给定队列和标签下的排序判别，三个模型的 AUC 差异本身不能区分生物机制、代理特征、数据处理、模型容量、过拟合或泄漏等竞争解释。若没有正交测量、干预或能区分机制的设计，机制 estimand 不可识别。

可另立一个更窄的新候选——“同一目标量下三模型的公平内部预测性能比较”——但该候选当前只能是 `HOLD_NEED_EVIDENCE`，不能继承原命题的创新性。

**仍缺证据**

最近邻全文及补充材料；目标人群和独立单位；三模型是否共享同一 estimand；AUC 的配对结构和区间；训练、调参与评价隔离；强朴素及最近邻基线；预处理与标签泄漏路径；模型输入预算是否公平；外部或时间验证；真正能辨别机制的正交/干预证据。

**未执行动作**

未计算或比较 AUC、未重抽样、未审代码、未训练模型、未访问数据、未把预测差异升级为机制结论、未以缺全文为由声称最近邻已覆盖。

---

## T3：最小试点后仅有汇总图，要求立刻写论文

**Stable skill 与顺序**

1. `coordinate-research-workflow`：只接续既有流程，不因用户口头“达阈值”跳过验证。
2. `research-topic-selection`：定向复核 G5；不无故重做 G0–G4，但须确认原门槛记录仍对应当前数据、代码和预注册版本。
3. `guide-research-methods-statistics`：核对原始计数、分母、独立单位、估计值、区间、阈值、偏离、泄漏和复现证据；必要时在取得材料和授权后按冻结方案复现。
4. 回到 `research-topic-selection`：只有 G5 可核验 PASS，才给 `GO_FULL_STUDY`。
5. 仅在上述条件满足后，才交接：
   - `audit-and-polish-manuscript`：正文与主张审查；
   - `write-manuscript-supplement`：冻结方法、偏离和复现细节；
   - `plot-research-statistics`：基于已核结果重绘并做视觉 QA；
   - `retrieve-and-match-references`：给背景和讨论建立证据链。

**当前裁决/停止点**

`HOLD_NEED_EVIDENCE`，不进入结果性写稿。

“试点已运行”和“用户称达阈值”不能替代 G5 PASS；汇总图不能证明原始分母、区间、事前阈值、偏离、独立性或复现性。当前 G5 是 `UNKNOWN`，不是 `PASS`，也不能裁成 `STOP`。

**必要前置核验**

- 预注册/冻结方案的版本、时间戳及主要 estimand；
- 原始计数、每步分母、有效独立单位和纳排；
- 点估计、区间及是否以预先规定的方法跨过阈值；
- 强基线、正对照、信息公平和泄漏检查；
- 所有偏离、失败运行、排除与缺失处理；
- 数据/代码/环境/种子/输入输出哈希及可复现运行记录；
- 实际资源成本；
- 既有 G0–G4 证据是否仍 current。

**未执行动作**

未依据汇总图写 Results 或 Discussion，未反推计数或区间，未把偏离静默写成预注册内容，未重分析或复现，未重画结果图，未投稿、发送或公开材料。写稿虽被用户请求，但当前被 G5 门槛阻断。

---

## T4：集群随机设计样本量与 ICC 敏感性

**Stable skill 与顺序**

1. `coordinate-research-workflow`：确认任务仅限样本量，不扩大为选题审计。
2. `guide-research-methods-statistics`：直接进入冻结 estimand 下的样本量输入核验、设计效应、整群数量取整、流失调整及 ICC 敏感性分析。
3. 不调用 `research-topic-selection`；只有主要结局或 estimand 实际改变时才返回上游，而本例明确未要求改变。

**当前裁决/停止点**

不是 GO/HOLD/STOP 型选题裁决。当前执行状态为 `blocked`，停止在样本量输入清单；主要结局已冻结，但没有足够数值计算唯一所需样本量。不得自行假定“中等效应”、ICC 或簇大小。

**仍缺输入/证据**

- 设计类型、组数、分配比和随机化单位；
- 结局类型、效应尺度及最小有意义差异；
- 连续结局的 SD，或二分类结局的对照率与目标率；
- 双/单侧 α、目标 power、多重性；
- 平均簇大小、簇大小分布或 CV、最小/最大簇大小；
- ICC 点值、可信来源及拟纳入的敏感性范围；
- 预计个体失访和整簇失访；
- 可用簇数约束、分层/配对随机化；
- 主分析模型、协变量调整及小簇数自由度修正假设。

等簇大小时可从个体随机设计所需量 \(N_0\) 出发，使用  
\[
DE=1+(\bar m-1)\rho .
\]
簇大小不等时可将  
\[
DE\approx1+\{(1+CV^2)\bar m-1\}\rho
\]
作为初步近似，但最终应使用与设计、结局和主分析相符的方法，并按整簇向上取整。ICC 记录表应至少包含：`ICC｜平均簇大小｜CV｜设计效应｜膨胀后个体数｜每组/总簇数｜失访调整后簇数｜假设来源`。

**未执行动作**

未重做选题、未更改主要结局、未代填效应量/ICC、未给出虚构样本数、未运行软件或模拟、未把简单设计效应近似冒充复杂设计的正式计算。
