# Round 16：流程图模块版本接续

## 缺陷与完成条件

PR #3 头 `f6b3eba` 相对 `main` 已分叉：总控本身已有唯一 `research-flow-diagrams` 路由，但分支中的流程图入口仍是旧 blob `5a663bc`，来源快照仍写 `main@304fea0`。与此同时 `main@b896589` 已把该模块改为 Mermaid-first，并新增专利、软著和技术说明书的黑白布局规则。若继续沿用旧快照，总控会错误声称已接续当前模块版本。

完成条件：以非强制、双父提交接入 `main@b896589`；现行流程图 blob 与 main 相同；来源快照记录新版本；根路由仍唯一；全部运行入口 frontmatter name 完整且唯一；运行 SKILL.md 的相对文件链接无缺失。

## 实际改动

提交 `b40fbaccabfdbd6085a765c93e03819f87d55699` 以 `f6b3eba` 和 `b896589` 为父提交。它原样接入 main 的 `research-flow-diagrams/SKILL.md`，仅更新 `references/workflow-sources.md` 的核查日期、main SHA 和职责快照。根 `SKILL.md` 路由无需修改，因为已正确把流程、技术路线、纳排和模型结构交给该稳定名称，并与统计结果作图区分。

没有新增或修改临床、统计、法律、专利或软著裁决规则；没有把 Mermaid 布局偏好当成科学依据。

## 静态验证

- 候选相对 main：领先 21 个提交、落后 0。
- 双父提交的第二父为 `main@b896589`。
- 根入口加 12 个专业入口，共 13 个运行 SKILL.md；13/13 有 name，13/13 唯一。
- 根总控中 `research-flow-diagrams` 稳定名称出现 1 次，对应相对链接存在。
- 全部运行 SKILL.md 的相对文件链接缺失数为 0。
- 候选流程图 blob 为 `ff4896e`，与 main 完全相同。
- 八个既有核心技能已按 main 当前 SHA 重新读取；本轮未改动它们。

机器可读结果见 `static-verification.json`。

## 测量边界与重查条件

本轮只验证版本接续、入口身份和静态链接，不包含模型行为运行、Mermaid 渲染、SVG/PNG/PDF 导出或视觉 QA，不能证明真实分流成功率、绘图质量、科学正确性或效率提升。模型、token、费用和端到端耗时不可得。

当 main 再次修改模块稳定名称、frontmatter、职责、默认交付格式或总控路由，或实际出现流程图/统计图误分流时重查。个人已安装技能未同步；PR 继续保持 draft，等待人工架构审阅。
