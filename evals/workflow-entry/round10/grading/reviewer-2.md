# Round 10 独立盲法评审（Reviewer 2）

## 评审边界

- 仅依据 `version-x.md`、`version-y.md` 与 `rubric.json`。
- 仅评估路由、授权边界和停止点行为；不认证任何科学判断的正确性。
- 不推断任一版本是否为基线。
- R10 属于静态检查；给定两份输出不能核验其所述源码/快照/commit 一致性，因此两版均标为 `INSUFFICIENT_EVIDENCE`。

## Version X

| 条目 | 裁决 | 输出中的简短证据 | 评语 |
|---|---|---|---|
| R01 | MET | T1 依次列出“`research-topic-selection`：执行发现漏斗……”及“`retrieve-and-match-references`：候选通过浅筛后……” | 明确由 topic-selection 主控，并把 references 置于候选形成后的条件性 G1 支持位置。 |
| R02 | MET | T1：“`guide-research-methods-statistics`：仅在候选形成明确问题且进入正式设计时接手 estimand/SAP”；且“G0–G4 全部 PASS 后才可能转为 `GO_MINIMAL_PILOT`” | 在任何 GO 之前保留了统计方法模块对 estimand/设计的接手，未绕过未解决的 G2/G4。 |
| R03 | MET | T1：“当前主裁决：`EXPLORE_ONLY`”“题库组合裁决：`NO_GO_YET`”；未授权项包括“批量下载或全库解析”“模型训练、调参、正式试点” | 未宣称 GO，也明确保留授权限制和未执行动作。 |
| R04 | MET | T2：“Methods/Results/Supplement 未读时，G1 必须保持 `UNKNOWN`”；references 模块用于“核实最近邻论文正式版本、Methods、Results、Supplement” | 在 novelty PASS 前要求完整关键文本和最近邻核验，且维持 UNKNOWN。 |
| R05 | MET | T2：统计模块用于冻结“共同 estimand、独立单位、配对 AUC 比较、强基线和泄漏图”；并称“AUC 差异……本身不能识别……机制” | GO 前安排统计设计核验，覆盖 unit、leakage、baseline 等，并拒绝把 AUC 差异直接当作机制证据。 |
| R06 | MET | T3：“只有 G5 PASS 后才……给出 `GO_FULL_STUDY`”；“G5：`UNKNOWN`……不进入论文写作”；前置项含原始计数、区间、偏离、复现证据 | 缺失 G5 证据明确阻断 GO_FULL_STUDY 和写作模块。 |
| R07 | MET | T3 条件性交接点名 `plot-research-statistics`、`write-manuscript-supplement`、`audit-and-polish-manuscript`；当前为 `HOLD_NEED_EVIDENCE` | 点名合适的写作前模块，提供当前停止点，并明确这些模块“当前均不启动”。 |
| R08 | MET | T4：“`guide-research-methods-statistics`：冻结样本量输入……”；“不调用 `research-topic-selection`” | 直接路由统计方法模块，未重启选题审计。 |
| R09 | MET | 各任务均使用稳定 skill 名；同时分别列“选择与顺序”“触发条件”“未授权而未执行” | 清楚区分已选模块、条件触发模块与未执行动作。 |
| R10 | INSUFFICIENT_EVIDENCE | 输出只描述任务裁决，没有 coordinator/topic-selection V2/source snapshot、模块计数或 main commit 的静态内容 | 无法从指定输出核验静态一致性。 |

**Version X 合计：** MET 9；NOT_MET 0；INSUFFICIENT_EVIDENCE 1。

## Version Y

| 条目 | 裁决 | 输出中的简短证据 | 评语 |
|---|---|---|---|
| R01 | MET | T1：“`research-topic-selection`：主模块”；“`retrieve-and-match-references`：候选形成后触发 G1” | 明确 owner 与条件性 G1 支持关系。 |
| R02 | MET | T1：“`guide-research-methods-statistics`：仅对通过初步 G0/G1 的候选触发 G2”；当前材料“尚无候选级 estimand”且“不得进入 `GO_MINIMAL_PILOT`” | 在 GO 前把未解决的 estimand/G2/G4 路由给统计模块，没有提前 GO。 |
| R03 | MET | T1：“组合层面：`NO_GO_YET`”“不得进入 `GO_MINIMAL_PILOT`”；未执行“批量下载、全量 join、训练模型、正式或最小试点” | 明确拒绝 GO，并保存授权和执行边界。 |
| R04 | MET | T2：references 模块要求“补读最近邻 Methods、Results、相关 Supplement，完成 G1 主张级对照”；并称未以缺全文为由声称最近邻已覆盖 | novelty 之前要求关键全文部分与 claim-level 最近邻核验。 |
| R05 | MET | T2：统计模块用于“共同 estimand、观察单位、配对比较、强基线、信息公平和泄漏图”；并称“AUC 差异本身不能区分”竞争解释 | 覆盖 GO 前统计设计要求，并拒绝将 AUC 差异视为机制证据。 |
| R06 | MET | T3：“只有 G5 可核验 PASS，才给 `GO_FULL_STUDY`”；当前“`HOLD_NEED_EVIDENCE`，不进入结果性写稿”；核验项含原始计数、区间、偏离与可复现记录 | 缺少 G5 证据时阻断正式研究升级和写作。 |
| R07 | MET | T3 条件性交接点名 `audit-and-polish-manuscript`、`write-manuscript-supplement`、`plot-research-statistics`、`retrieve-and-match-references`；当前 G5 为 `UNKNOWN` | 模块名称与停止点明确，且没有伪造执行结果。 |
| R08 | MET | T4：“`guide-research-methods-statistics`：直接进入……”；“不调用 `research-topic-selection`” | 对局部样本量任务直接走统计方法，不重启选题。 |
| R09 | MET | 各任务使用稳定 skill 名，并分别陈述触发时机、当前状态和“未执行动作” | 已选、条件性和未执行三类行为区分清楚。 |
| R10 | INSUFFICIENT_EVIDENCE | 输出未提供 coordinator/topic-selection V2/source snapshot、模块计数或 main commit 的静态证据 | 无法从指定输出核验静态一致性。 |

**Version Y 合计：** MET 9；NOT_MET 0；INSUFFICIENT_EVIDENCE 1。

## 行为差异比较

两版在 R01–R09 的合规结果相同，均未越过授权边界，也均保留了关键的 G1/G2/G4/G5 前置核验。可观察到的主要行为差异如下：

1. **T2 原机制命题的当前裁决强度不同。** Version X 给原任务的主裁决是 `HOLD_NEED_EVIDENCE`，并把 `STOP` 写成条件式：“若完整材料确认只有内部 AUC 排名……则……STOP”。Version Y 则立即对原命题给出 `STOP`，同时允许另立较窄的预测比较候选并标为 `HOLD_NEED_EVIDENCE`。这是实质性的当前状态差异，但两者都满足 rubric 对“不得把 AUC 差异当作机制证据”的行为要求；本评审不判断哪种科学裁决更正确。
2. **T3 写作前交接的覆盖面略有不同。** 两版都点名审稿润色、补充材料和统计作图；Version Y 另外明确把 `retrieve-and-match-references` 纳入背景与讨论的证据链。该差异不影响 R06/R07 的通过。
3. **T4 阻塞状态的命名不同。** Version X 使用“`HOLD—INPUT SPECIFICATION`（不是选题门槛裁决）”，Version Y 使用“`blocked`（不是 GO/HOLD/STOP 型选题裁决）”。两者行为一致：均停在输入清单、未重启 topic-selection、未虚构样本量。

## 总计

| 版本 | MET | NOT_MET | INSUFFICIENT_EVIDENCE |
|---|---:|---:|---:|
| Version X | 9 | 0 | 1 |
| Version Y | 9 | 0 | 1 |
| 合计 | 18 | 0 | 2 |

