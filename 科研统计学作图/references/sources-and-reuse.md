# 来源与复用台账

核查日期：2026-10-09。本文为独立编写的工作流，脚本独立实现并调用现成绘图库；不整包复制第三方skill。分清官方规范、开源实现和内部偏好。运行时记录实际安装版本，引用软件按项目要求处理；若以后复制实质代码/文档须保留对应版权与许可全文。

| 来源 | 已读取的内容/经验 | 本skill采用与调整 |
| --- | --- | --- |
| [Nature final submission](https://www.nature.com/nature/for-authors/final-submission)及[研究图指南](https://research-figure-guide.nature.com/) | sans-serif、最终尺寸字号、细线、可编辑矢量及避免栅格化文字 | 按期刊/阶段核验，不把风格等同合规；800dpi为用户母版要求 |
| [Nature initial submission](https://www.nature.com/nature/for-authors/initial-submission) | 初投与最终制作要求不同，统计误差与n需定义 | 区分阶段及图类型，未指定期刊则标内部默认 |
| [Matplotlib布局](https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html)、[savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html)、[Gallery](https://matplotlib.org/stable/gallery/index.html) | renderer/布局、外置图例、图型原语、输出参数 | 不重造基础绘图原语；不混tight_layout；固定画布且实际重新打开输出 |
| [K-Dense scientific-visualization](https://github.com/K-Dense-AI/scientific-agent-skills/tree/92ace75ac21efe19a620434e0ca4e356081fe807/skills/scientific-visualization)；MIT | 证据先行、复制单位、缺失、可访问性、来源与元数据、实际文件验收 | 只采纳与本任务有关原则，自写中文规则；明确单panel和800dpi，移除多panel默认，不采用未经核对的期刊表 |
| [SciencePlots](https://github.com/garrettj403/SciencePlots/tree/b9b16959570bd2fbc9ff5118bacc423c3bddd592)；MIT | 已读nature.mplstyle，sans-serif和小字号、线宽配置 | 作为可选现成样式；本工具独立rc_context，无LaTeX依赖。若使用science/no-latex/nature组合，最后覆盖确认字体；不能继承tight导出而静默改变尺寸 |
| [adjustText](https://github.com/Phlya/adjustText/tree/92b0397b5de118151b788d5fb35aa7272f32c0ce)；MIT | 标签避让算法及在所有绘图完成后调整 | 不重新实现标签优化；可选调用并检查最终位置，不声称它修复图例/所有轴文字 |
| [RainCloudPlots](https://github.com/RainCloudPlots/RainCloudPlots) | 密度、摘要和原始点共同表达的实现/教程 | 作为高级图型实现候选，具体许可/版本在使用或复制前再核查 |
| [DABEST-python](https://github.com/ACCLAB/DABEST-python) | 效应与不确定性的估计图 | 专用实现候选，保持配对/独立单位，不能擅自替代已冻结统计 |
| [forestplot](https://github.com/LSYS/forestplot) | 带区间的系数图实现 | 长标签/模型系数图候选；先核实际版本/API/许可，仍逐panel导出 |

## 使用边界

不将第三方项目自己的“Nature标准”直接视为官方规则。Nature当前初投页有90/180mm等表述，最终制作页有89/183mm；本工具89mm是内部起点，不认证所有情况。Nature Extended Data等还可能有不同分辨率/体积要求：保留800dpi母版并另出被要求的版本，不让800dpi要求误导投稿。

已经成熟的统计算法和绘图原语直接调用；本skill新增的是任务选图、单panel代码保存、固定尺寸输出、保真与视觉核查的组合。未核许可的第三方代码不复制入仓库，绝不把真实稿件或患者数据当公开演示输入。
