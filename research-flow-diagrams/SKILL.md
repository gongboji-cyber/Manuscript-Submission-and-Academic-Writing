---
name: research-flow-diagrams
description: Design, generate, revise and audit evidence-grounded scientific flowcharts and technical roadmaps (科研流程图、技术路线图、研究设计流程、患者纳排图、PRISMA/CONSORT流程、实验步骤、方法框架、数据处理管线、模型架构、决策树、泳道图、机制示意图、graphical abstract). Select a suitable diagram grammar, verify nodes/edges/counts against source materials, preserve editable Mermaid/draw.io/vector sources, render and visually inspect actual exports. Use for conceptual or procedural diagrams, not statistical result plots.
---

# 科研流程图与技术路线图

把图当作**可核验的研究主张**，而不是文本自动排成彩色方框。先核语义，再定布局，最后导出并看实际图。任何箭头都在表达依赖、时间、数据移动、因果或条件；不能用同一种箭头偷换含义。

## 资源与分流

- 每次先读 [图型与后端选择](references/diagram-types.md) 和 [证据与语义校验](references/semantic-integrity.md)。
- 开始排版前读 [布局、导出和视觉复核](references/layout-export.md)；交付时逐项填写 [32项检查表](references/checklist.md)。
- 参考第三方方案、投稿标准或图标时读 [来源与复用说明](references/sources-and-adaptations.md)。
- 简单、已明确坐标的流程和路线图可复制 [示例规格](assets/method-route.example.json) 或 [模拟纳排示例](assets/cohort-flow.example.json)，调用 `scripts/render_diagram.py` 输出**原生可编辑draw.io + SVG + 审计JSON**。脚本为小型受限版式后端，不是复杂图的自动排版引擎。
- 复杂多分支自动布局优先 Mermaid/Graphviz 起稿、draw.io 或专用框架细化；医学决策图、因果DAG、网络拓扑及模型计算图分别遵守自身语义，不强行套四栏。

## 六步工作流

1. **定义通信目标。** 写一句“读者读完图必须理解什么”；声明受众、图类、研究阶段（方案/结果）、目标期刊/版面、输出语言、是否需要原生可编辑PPTX或draw.io。先判断段落/表格是否更清楚。若是统计图，交给 `plot-research-statistics`。
2. **抽取并冻结证据。** 从方案、手稿、纳排台账、可执行代码、数据字典、文献或用户明确假设提取节点、边、分组、时间、单位、数值、缩写；记录`元素ID → 精确来源/代码位置 → 状态(已证实/待核/假设)`。没有证据不填数值、不补路径、不猜模型结构；模拟图注明 `SYNTHETIC`。患者路径核对每个分母、重复计数、排除理由的互斥性与加和关系。
3. **制作语义草图。** 用稳定ID写节点表、边表、条件分支与分组；声明边类型（顺序、数据流、依赖、条件、反馈、因果假设）。将训练、调参、测试、人工GT、最终报告分清。模型图以实际 `forward`/配置/推理调用链为依据；设计方案图不得伪装为已执行结果。分支应有归宿，连接禁止暗示未执行的分析或不存在的数据泄漏防护。
4. **选语法与布局。** 小流程/讨论稿用Mermaid；需形状级编辑、队列泳道、精确排版选draw.io；极复杂有向图可用Graphviz自动布局再人工修订；符号与机制说明可用SVG/TikZ/原生PPTX；其他支持工具按环境选择。选横向（管线）、纵向（阶段）、泳道（责任主体）或分层（架构）；分组而不是强迫小字号容纳过多节点。需要时先给读者一个总览，再另画局部细节。
5. **生成并迭代。** 保留结构源文件（`.mmd`、`.dot`、`.json` 或`.drawio`）和最终布局源。用脚本或真实应用渲染，不根据源码“脑补已完成”。逐轮核对：一轮科学/语义，一轮空间布局，一轮实际导出视觉；严重问题修订并重新生成。无法渲染时明确标为未做视觉QA；没有独立复核条件也不能宣称“双审通过”。
6. **冻结交付。** 提交可编辑源、矢量SVG或PDF、所需位图预览/TIFF、短图注、元素-来源映射、运行命令、版本和已完成/待核的QA记录。期刊正式规范优先，不能把内部字体、色板或800 dpi偏好说成所有期刊统一规定。

## 默认科学与设计约束

- 用颜色编码**语义角色**（输入/方法/贡献/输出/核验/风险）；不用颜色独自表示通过/失败，搭配文字、边型或形状。白底、低装饰、跨图一致。读者首先看到问题与核心贡献，不是装饰。
- 框中文字用简短的具体名词/动作，完整方法放图注；缩写首次展开。可读性优先于节点密度。数字带分母、单位、时间点和来源；图内的`n`绝不从排版推断。
- 实线表示主流程；虚线仅在明确图例中表示可选/反馈/假设。因果关系须有设计支持，相关性不能画成确定因果。区分“同一患者多次就诊”和“患者级独立样本”；训练/测试箭头应忠于真实数据访问。
- 不用AI位图当准确流程图的唯一母版。生成插画仅可用于背景或非精确装饰，不能代替节点、箭头、计数与原生可编辑文件。
- 外部图表、论文示意图和商标不得逐像素描摹；学习信息组织原则，独立画图。禁止公开患者级数据、未授权图片、隐私标识和本地敏感路径。

## 小型可编辑图后端

先检查 `python -B scripts/render_diagram.py --help`。此工具仅支持显式坐标的直角框/菱形、分组、直线与折线路径；为 `.drawio` 生成真正的原生形状和连线，同时从同一JSON生成SVG。它会拒绝重复ID、未知边端点、越界/框重叠；对 `count/unit/balances` 声明的同单位分流执行加和核对，对未标证据给出警示，真实研究可加 `--strict` 要求证据字段。**不能**自动解决全部标签/线段碰撞、医学科学错误或替代人眼查图。

```bash
python -B scripts/render_diagram.py \
  --spec assets/method-route.example.json --out /tmp/route_demo
```

在真实项目中先复制示例至项目目录并替换所有 `SYNTHETIC` 内容；脚本没有权限从临床数据推算真实纳排。若项目要求原生PowerPoint形状/专业BPMN，转换后要逐节点核查可编辑性，不能以一张嵌入的SVG冒充原生编辑。

## 与其他模块协同

- `guide-research-methods-statistics` 提供问题、设计、estimand、独立单位、数据流和风险；本模块只负责图示与图上语义审计，不擅自改变SAP。
- `plot-research-statistics` 负责带数据/估计量/不确定性的统计panel；本模块负责流程、技术路线、框架与模型结构。若一张图混合两者，分别生成并在用户授权的排版流程中组合，保留各自母版。
- `audit-and-polish-manuscript` / `write-manuscript-supplement` 核查图—正文—补充材料—图注的一致性；`format-academic-word` 负责最终文稿嵌图与排版。

## 最终答复格式

简报：图的核心信息及图型理由；列出已核验和待确认的关键元素；给出所有实际生成、验证过的文件与来源及重现命令；报告语义QA、自动QA、视觉QA、期刊要求核查的真实状态。缺少关键证据时交付标注清楚的结构草案，**不宣称可投稿**。
