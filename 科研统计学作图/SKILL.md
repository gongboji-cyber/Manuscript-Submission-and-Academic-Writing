---
name: plot-research-statistics
description: Design, draw and audit evidence-grounded medical, biomedical and computational statistical figures (科研统计学作图、Nature风格、论文绘图、统计图选型、单panel、文字裁剪、标签重叠、图例遮挡、800dpi TIFF、矢量PDF). Select charts from the scientific question and data structure, preserve numerical evidence, save runnable per-panel code and source mappings, export individual panels rather than composites, and inspect actual TIFF/PDF outputs. Use for new plots or repairs to publication figures; do not fabricate data, recompute unapproved analyses, assemble multi-panel figures or treat stylistic presets as journal compliance.
---

# 科研统计学作图

## 资源

- 开始读取[选图目录](references/chart-selection.md)、[统计保真](references/statistical-integrity.md)和[布局与导出](references/layout-and-export.md)。
- 验收使用[24项检查](references/checklist.md)；核查期刊与第三方实现时读取[来源与复用](references/sources-and-reuse.md)。
- 使用[单panel工具](scripts/panel_tools.py)统一样式、检查文字边界并导出；使用[常用图入口](scripts/plot_panel.py)和[配置示例](assets/panel-spec.example.json)绘制核对后的CSV。工具不代替统计设计或逐图检查。

## 1. 根据研究问题选图

每个panel先写：**问题→读者应看到的比较/关系→变量与独立单位→图型→估计量/不确定性→来源**。核对配对/重复测量、单位、分母、缺失、删失、预处理、CI方法与展示范围。从证据选图，不先选漂亮模板再找结果。说明首选相对替代图的信息优势；阴性结果、异质性、失败与不确定性照常显示。

只有汇总值时使用点和区间，不伪造箱线图、小提琴或原始散点。缺少参考标准、原始值或区间定义时说明不能绘制/核实的部分，继续完成有依据的图。只绘图不擅自新增检验或重算已冻结结果；新分析先明确授权与方法。不以星号、挑选子组、截轴或隐藏异常值制造结论。

## 2. 固定单panel任务和版式

逐panel独立交付，稳定命名如Fig2A、Fig2B，每个panel保存独立可运行代码。**不生成组图、拼图或多panel PDF。** 同一panel必要色标或生存风险表可用辅助轴，不把独立研究问题藏入辅助轴。默认不烧录a/b标签，除非用户要求。

制定panel计划：图型、轴/单位、n、排序、配色/线型、误差定义、参考线、最终尺寸、图例位置和来源。跨panel相同组别的编码一致，比较尺度合理。“Nature风格”是克制、清晰、可编辑的版式，不是录用标准。内部起点89×70 mm、Arial/Helvetica优先、7 pt正文、6.5 pt刻度、0.6 pt轴线、白底。按内容调尺寸，不能无限缩字；核查指定期刊、图类型与投稿阶段的官方规则。保留用户要求的800dpi母版，需要期刊版本时另说明差异。

## 3. 使用现成绘图库，保留可运行代码

优先Matplotlib对象接口，按需使用Seaborn、SciencePlots、adjustText和专用统计库并记录版本/许可。复用验证过的绘图原语与算法，不搬运未核统计结论或期刊尺寸，不整套安装无关skill。

入口支持strip、box+原始点、violin+原始点、paired、scatter、line、forest、histogram、ECDF、heatmap和bar。配置明确列映射；配对必须有真实ID，区间使用核对后的结果，line不得自动平均重复测量或跨缺失连接。高级图型按目录使用专用实现，仍沿用导出/验收工具。抖动只沿分类轴并固定种子，不改变原始数值。

每个panel保存完整代码/辅助模块、配置、输入哈希/来源、转换说明、依赖版本和重运行命令。授权输入表默认复制至其私有输出目录；受限数据只记录本地路径/哈希或使用授权汇总绘图表。实际研究数据不进入公开skill仓库。

## 4. 防止裁剪、重叠和遮挡

完成科学内容后处理布局。使用constrained layout或明确边距，不混用tight_layout。默认固定画布，不靠bbox_inches='tight'静默改物理尺寸。标题、轴标签、刻度、offset、色标、图例和注释全部检查导出边界。draw后核查字形和文字bbox，调整尺寸/边距、换行、刻度或注释，再draw。

图例优先置于绘图区外且画布内，不遮挡点、线、CI、数字和关键内容，`loc='best'`不能代替验收。密集标注先减少重复，再用adjustText/引导线并核查归属。不能删点、缩短区间或移动数值避让。箱线须线与端帽完整；所有原始点已显示时可取消重复flier符号，不能隐藏离群值。

自动工具只覆盖指定的边界、文字碰撞、图例与轴区域及输出元数据，不覆盖所有注释与数据碰撞、语义或后端差异。**自动通过后仍分别打开实际TIFF与PDF渲染图，逐panel看完整图及局部。** 修正后重导出，检查最新版本。

## 5. 导出、核查、交付

每panel导出白底RGB/LZW无损**800dpi TIFF**和**单页矢量PDF**。重新打开TIFF验证像素、模式、双向DPI与物理尺寸；不放大旧低清图冒充新800dpi作图。PDF线、点、文字保持矢量/可编辑，嵌入字体，不转轮廓或整图截图；核查页面、字体和路径。原生影像等位图如实报告为混合PDF，不能称全矢量；大点云栅格化须授权/说明。

记录图型理由、内容核对、自动结果、TIFF/PDF视觉结果与待确认项，填写P01—P24，不总分。导出成功不等于统计或视觉通过，未看图时标待核。交付单panel TIFF/PDF、代码和简短检查结果，不交付组图，不把QA预览当投稿文件。按环境保存规则保存产物；本skill同步个人技能与指定GitHub仓库。
