# 开源与社区来源台账

核查时间：2026-10-10。以下仅吸收工具选择与质量控制思路；本Skill文案、JSON示例与Python脚本均独立编写，未复制第三方脚本、图形资产和模板。若后续引入外部素材/代码，须单独核对该提交版本的许可证及版权声明并按许可保留。

| 来源 | 已核查特点 | 在本模块中的原创整合与边界 |
| --- | --- | --- |
| [Kkkakania/scientific-diagram-skill](https://github.com/Kkkakania/scientific-diagram-skill)，MIT | Mermaid草拟，draw.io可编辑交付，XML与示例QC | 采用“语义草案→可编辑图→验证”顺序；自写完整的科研证据/计数审计，未复制模板 |
| [YikaiDong-git/PaperWorkflowFig-skill](https://github.com/YikaiDong-git/PaperWorkflowFig-skill)，README载明MIT | Figure 1预检、核心贡献突出、渲染后再审 | 吸收视觉复核与数字保真；不接受普遍“每图必须四栏、三轮双agent、禁止PNG”的硬规则 |
| [K-Dense-AI/scientific-agent-skills/markdown-mermaid-writing](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/markdown-mermaid-writing)，Apache-2.0 | 以Mermaid文本保留结构、按图类分流、检查不同渲染版本 | 采用可版本化的结构源，复杂统计图仍独立绘制；不复制具体手册 |
| [Ztsdut/ml-architecture-diagram-skill](https://github.com/Ztsdut/ml-architecture-diagram-skill)，MIT | 先恢复真实计算图，经过语义审阅，再生成可编辑架构图 | 对计算工作流增加代码路径/配置审计；不把通用框图误作神经网络拓扑 |
| [luffy666code/diagram-design-skill](https://github.com/luffy666code/diagram-design-skill)，MIT | 按图型和行为语义选择布局，强调视觉简化与可访问性 | 将图型选择从“只有flowchart”扩到决策、泳道、时序、层级等，不引入大量展示专用HTML模板 |
| [draw.io官方：Mermaid导入与编辑](https://www.drawio.com/docs/manual/mermaid/) | 默认Diagram可编辑；Image为静态SVG；重新从Mermaid生成会覆盖手工几何 | 两次冻结与最终原生.drawio母版；源文本和排版版同时留档 |
| [draw.io官方：AI生成图提示建议](https://www.drawio.com/docs/best-practice/write-query-generate-diagram/) | AI起稿适合简单流程/概念；复杂专业符号应人工校订；不传敏感信息 | 专业流程与证据检查不能外包给生成器；敏感研究内容仅本地 |
| [社区讨论：LLM布局问题](https://www.reddit.com/r/AI_Agents/comments/1qd0nq9/how_do_you_get_llms_to_generate_actually_good/) | 个人经验指出复杂图易重叠/错误连线；属轶事证据 | 用“语义与排版分离＋实际图复核”处理风险，不将论坛意见当严格研究证据 |
| [Mermaid文档](https://mermaid.js.org/intro/)、[Graphviz文档](https://graphviz.org/documentation/)、[diagrams.net](https://www.drawio.com/) | 现成DSL、自动布局、图形编辑/导出 | 可用成熟后端，不在Skill内重新发明复杂自动布局 |

## 与原有统计图模块的分工

本模块不计算统计推断、不更动纳排台账或实际研究结果，不取代统计作图单panel的800dpi TIFF/矢量PDF流程。若要制作真正的 Figure 1 概念管线，应先确认它是方法示意还是数值结果，必要时拆开提供源文件。

## 外部使用原则

第三方GitHub Star数、论坛帖、作者称“publication-ready”都不是可靠性验证。每张真实科研图应以论文材料/代码/台账为证据，再以实际导出图形完成空间与可读性验证。
