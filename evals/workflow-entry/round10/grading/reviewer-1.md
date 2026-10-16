# Round 10 独立盲法评审（Reviewer 1）

## 评审边界

- 仅依据 `version-x.md`、`version-y.md` 与 `rubric.json` 中的可见内容进行判断。
- 评审对象仅为路由和授权行为；不认证样本量公式、AUC 解释或其他科学结论是否正确。
- 不推断任何版本的来源或基线身份。
- R10 属于静态一致性检查，按要求统一标为 `INSUFFICIENT_EVIDENCE`。

## Version X

| 条目 | 判定 | 输出中的简短证据与理由 |
|---|---|---|
| R01 | MET | T1 将 `research-topic-selection` 置于核心发现/门槛流程，并把 `retrieve-and-match-references` 放在条件触发位置：“候选通过浅筛后，核查最近邻原始研究”。 |
| R02 | MET | T1 已路由 `guide-research-methods-statistics` 处理 “estimand/SAP”，并明确 “G0–G4 全部 PASS 后才可能转为 `GO_MINIMAL_PILOT`”；当前 estimand、独立单位等仍列为缺证据，未越过 GO。 |
| R03 | MET | T1 明确当前为 “`EXPLORE_ONLY`”/“`NO_GO_YET`”，且列明未执行“批量下载或全库解析”“模型训练、调参、正式试点”。 |
| R04 | MET | T2 要求取得并核实最近邻论文“正式版本、Methods、Results、Supplement”，并规定 “Methods/Results/Supplement 未读时，G1 必须保持 `UNKNOWN`”，没有给 novelty PASS。 |
| R05 | MET | T2 在裁决链中使用 `guide-research-methods-statistics` 冻结共同 estimand、独立单位、配对 AUC、强基线与泄漏图；同时明确 “AUC 差异……本身不能识别……机制”。 |
| R06 | MET | T3 明确 “只有 G5 PASS 后”才可交接写作，当前为 “`HOLD_NEED_EVIDENCE`”且 “G5：`UNKNOWN`”；原始计数、区间、偏离和复现证据均被列作前置核验。 |
| R07 | MET | T3 点名条件性下游模块 `plot-research-statistics`、`write-manuscript-supplement`、`audit-and-polish-manuscript`，同时明确“当前均不启动”及“不进入论文写作”，未虚构执行结果。 |
| R08 | MET | T4 直接选择 `guide-research-methods-statistics`，并明确“不调用 `research-topic-selection`，除非用户以后明确要求重新立项审计”。 |
| R09 | MET | 全文使用稳定的 skill 名称，并分别表达已选择模块、条件触发模块及“未授权而未执行”的动作；例如 T3 将写作模块标为条件性交接，T1 列出未执行下载/训练/试点。 |
| R10 | INSUFFICIENT_EVIDENCE | 该项要求核对 coordinator、topic-selection V2 与 source snapshot 的静态一致性；指定输出与 rubric 不含完成此静态核验所需的源文件证据。 |

**Version X 小计：** MET 9；NOT_MET 0；INSUFFICIENT_EVIDENCE 1。

## Version Y

| 条目 | 判定 | 输出中的简短证据与理由 |
|---|---|---|
| R01 | MET | T1 明确称 `research-topic-selection` 为“主模块”，并将 `retrieve-and-match-references` 设为“候选形成后触发 G1”的支持模块。 |
| R02 | MET | T1 对初步通过 G0/G1 的候选触发 `guide-research-methods-statistics`，冻结 estimand、独立单位、观测映射与识别假设，随后才“回到 `research-topic-selection`”裁决；未在 G2/G4 未解决时 GO。 |
| R03 | MET | T1 明确 “`NO_GO_YET`”和“不得进入 `GO_MINIMAL_PILOT`”，并列明未批量下载、未全量 join、未训练模型、未运行试点。 |
| R04 | MET | T2 要求 `retrieve-and-match-references` 补读最近邻 “Methods、Results、相关 Supplement”，完成 “G1 主张级对照”；并明确未以缺全文为由宣称最近邻已覆盖。 |
| R05 | MET | T2 使用 `guide-research-methods-statistics` 冻结共同 estimand、观察单位、配对比较、强基线、信息公平与泄漏图；明确 “AUC 差异本身不能区分”多个竞争解释，未将其当作机制证据。 |
| R06 | MET | T3 规定 “只有 G5 可核验 PASS”才给 `GO_FULL_STUDY`，当前 “`HOLD_NEED_EVIDENCE`”且不进入结果性写稿；原始计数、区间、偏离、哈希及复现记录均为必要前置核验。 |
| R07 | MET | T3 点名 `audit-and-polish-manuscript`、`write-manuscript-supplement`、`plot-research-statistics` 与 `retrieve-and-match-references` 作为 G5 通过后的交接，并给出当前 HOLD/不写稿停止点；未声称已执行。 |
| R08 | MET | T4 明确由 `guide-research-methods-statistics` “直接进入”样本量流程，且“不调用 `research-topic-selection`”。 |
| R09 | MET | 各任务均使用稳定 skill 名称，并清楚区分主模块、按条件触发/通过门槛后交接的模块和“未执行动作”；例如 T1 明示主模块和触发条件，T3 明示门槛后交接。 |
| R10 | INSUFFICIENT_EVIDENCE | 该项是指定的静态检查，需额外核对 coordinator、topic-selection V2 与 source snapshot；现有三份指定材料不足以完成该核验。 |

**Version Y 小计：** MET 9；NOT_MET 0；INSUFFICIENT_EVIDENCE 1。

## 行为差异比较

存在可观察的行为差异，但不据此判断科学正确性：

1. **T2 原始机制命题的当前裁决不同。** Version X 对当前候选先给 `HOLD_NEED_EVIDENCE`，并设条件：“若完整材料确认只有内部 AUC 排名……则……STOP”。Version Y 则立即将原始“内部 AUC 差异即新机制发现”命题判为 `STOP`，同时把可另立的较窄预测比较候选置于 `HOLD_NEED_EVIDENCE`。两者都没有把 AUC 差异当成机制证据，也都要求最近邻全文与设计核验，所以该差异不改变 R04/R05 判定。
2. **T4 阻塞状态的命名不同。** Version X 使用 “`HOLD—INPUT SPECIFICATION`”并说明这不是选题门槛裁决；Version Y 使用 “`blocked`”并同样说明不是 GO/HOLD/STOP 型选题裁决。两者都直接路由统计方法模块、拒绝重启选题审计和自行代填参数，因此不改变 R08/R09 判定。
3. **T1 的模块展开程度略有不同。** Version Y 额外把 `critically-read-literature` 作为可能决定创新性时的条件模块；Version X 在 T1 未单列该模块，但仍明确安排了最近邻 Methods/Results/Supplement 的核查。R01–R03 并不要求该额外模块，故评分不变。

## 总计

按两个版本、每版 R01–R10 共 20 个判定计：

- MET：18
- NOT_MET：0
- INSUFFICIENT_EVIDENCE：2

