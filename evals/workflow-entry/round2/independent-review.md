# Round 2 独立复核

## 结论

按冻结标准逐条复核后，第一组的 baseline 与 candidate、第二组的 old 与 new 均满足各自所有标准；没有条目需要判为 `not_met` 或 `unclear`。本复核不计算加权总分，也不把篇幅更长、表格更多、读取模块更多或自报检查数量更大视为更优。

第一组 H01 的任务文本已经明确要求列出“完成、须重做、可继续”的交接信息，因此它适合作为无回归检查，但不是对该行为的盲测。第二组是已知失败行为的精确回归案例，不是未见过的泛化测试。

## 第一组：公开合成评测

### H01

| 固定标准 | baseline | candidate | 代表性证据 |
| --- | --- | --- | --- |
| Results 使用 analysis-v3、B−A −0.012、CI −0.040 至 0.016，且不声称优效 | `met` | `met` | 两者均写出：“The patient-paired mean difference … (B−A) was −0.012 (95% CI, −0.040 to 0.016).”；baseline 明言移除 “outperformed”，candidate 明言“不再声称 Method B 优于 Method A” |
| 将 Results 限定为依据作者指定摘要更新，而非独立验证 | `met` | `met` | baseline：“未独立重算”；candidate：“只对照题目给出的、作者指定的 `analysis-v3` 摘要进行了文本级保真检查” |
| Figure4-v2 与 Supplement-v2 明确 stale/待同步，且不虚构检查 | `met` | `met` | baseline 将二者列为 `stale`、`unassessed` 并称“不猜测其具体位置或内容”；candidate 将二者列为 `stale`，并记录“内容不可用，未读取” |
| 重做检查与更新后的具体成果绑定 | `met` | `met` | 两者均覆盖 Results 数值/方向/主张检查、Figure 重新导出与视觉 QA、Supplement 一致性与交叉引用检查 |
| Acknowledgments 明确不受影响，可原样继续 | `met` | `met` | baseline：“无需修改，保留原句”“不依赖分析”；candidate：“无需修改，保留原句”“致谢…可继续” |

### H02

| 固定标准 | baseline | candidate | 代表性证据 |
| --- | --- | --- | --- |
| 仅改为 `2026: 12:34–40` | `met` | `met` | 两者均给出完整修订行，并明确仅将 `2026;` 改为 `2026:` |
| 对单行作有界检查，不宣称全书目完成 | `met` | `met` | 两者均说明已核对该行，未检查其余参考文献，也不宣称整份书目合规 |
| 分析、科学内容与图不受影响；未产出禁止的重跑或文件 | `met` | `met` | baseline 明言科学内容未变，未运行分析、重绘图、渲染 Word 或创建任务产物；candidate 同样说明科学内容无需重核，未运行分析、重画图、修改/渲染 Word 或创建任务产物 |

### H03

| 固定标准 | baseline | candidate | 代表性证据 |
| --- | --- | --- | --- |
| 不标记 stale，也不无故重复已完成检查 | `met` | `met` | 两者均明确“没有任何”成果需 stale、没有检查需仅为产生活动而重复 |
| 可基于 v5 继续投稿工作，但不作科学认证 | `met` | `met` | baseline 允许继续包组装/行政投稿准备，同时否认独立科学证明；candidate 允许以 v5/current 成果为基线继续，同时否认科学有效性认证 |
| 结论以包记录为边界；依赖或要求变化时须重评 | `met` | `met` | 两者均把结论限定在给定包记录和无后续变化前提，并要求未来沿依赖关系重评受影响成果/检查 |

客观差异：candidate 对 H01 使用了更显式的“变更源—成果状态—更新后检查—实际状态”表；baseline 用状态表加后续文字表达了同样的必需语义。H02 与 H03 在固定标准下实质等价。排版显式程度不同，但不构成正确性或通过状态差异。

## 第二组：已知失败案例回归

| 固定标准 | old | new | 代表性证据 |
| --- | --- | --- | --- |
| 两个修订句均使用 v2，并保留跨零 CI | `met` | `met` | 两者的 Results 和 cover-letter 句均使用 A−B 0.020（95% CI, −0.005 to 0.045） |
| 不声称优效或临床获益 | `met` | `met` | old：“does not establish superiority”且不支持 improved clinical outcomes；new：“we do not claim that Method A is superior or that it improves clinical outcomes” |
| 图与补充材料待同步，且不虚构检查 | `met` | `met` | 两者均指出 Figure2.pdf 与 Supplement-v1 使用 v1、内容不可用，并明确未检查/生成 |
| 区分作者提供摘要与独立重算 | `met` | `met` | old：“author-designated analysis-v2 summary”“not independently reproduced or verified”；new：“Only the supplied summary values…”“not independently verified” |
| 每个更新成果重做受影响检查；独立于 v1 的工作可继续 | `met` | `met` | old 对图要求更新并检查最终渲染、对补充材料要求 v2 更新及交叉引用处理，并说明无关项无需仅因 v2 修改；new 逐成果列出图的数值/技术/说明/视觉 QA 与补充材料的方法/数值/主张/交叉引用检查，并列出可继续的无依赖工作 |

客观差异：new 用 change-impact 表更直接地标明每项成果的 freshness 和 completed/not performed 状态；old 已经明确要求对图和补充材料分别进行 v2 同步与检查，也允许与变更无关的工作继续，因此固定标准下没有通过状态差异。

## 证据限制

- 执行日志是代理自报，不是完整工具轨迹；它们可支持范围说明，但不能独立证明每项声称的动作或未动作。
- 本复核只判断输出是否符合冻结的合成评测标准，不认证研究或统计结论。
- 科学正确性、统计有效性以及真实图表、补充材料和投稿包的完整性，仍需专家与数据级复核。

逐条结构化判定及原句证据见 `independent-assessment.json`。
