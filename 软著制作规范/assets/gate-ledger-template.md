# 阶段确认台账模板

| Gate | 状态 | 确认时间 | 依据 | 用户确认/授权 | 后续变更是否使其失效 |
| --- | --- | --- | --- | --- | --- |
| BUSINESS_UNDERSTANDING_CONFIRMED |  |  |  |  |  |
| APPLICATION_FACTS_CONFIRMED |  |  |  |  |  |
| CODE_SELECTION_CONFIRMED |  |  |  |  |  |
| SCREENSHOT_PLAN_CONFIRMED |  |  |  |  |  |
| FINAL_DRAFT_CONFIRMED |  |  |  |  |  |
| MANUAL_RENDER_QA |  |  |  |  |  |

规则：

- 状态仅用：PENDING / CONFIRMED / INVALIDATED / NOT_APPLICABLE。
- 任一已确认字段发生实质变化，必须将受影响 Gate 标为 INVALIDATED 并重新确认。
- 用户明确要求“一竿到底”只代表流程可不停顿，不代表著作权人、日期、权属等法律事实可以由 agent 猜测。
- 人工 Word/WPS/PDF 渲染未完成时，MANUAL_RENDER_QA 不得标 CONFIRMED。
