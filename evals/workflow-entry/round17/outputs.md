# Round 17 匿名原始输出

## 运行条件

- X：同一原始任务；fresh 执行者；不得读取仓库、网络或评测材料。
- Y：同一原始任务；fresh 执行者；只读取候选 commit `5e6e1eb9b2081635c847580f6460b1547ba10dda` 的根 `SKILL.md` 与完成任务所需的最少专业模块；不得读取 `evals/`、PR 描述或网络。
- 两组使用同一代理模型条件；精确部署 ID、token、费用和可比端到端耗时未提供。

## 输出 X

### A

- ROUTE：技术路线图/矢量流程图模块
- DECISION：画“拟议研究流程”，不走统计作图。
- DELIVERABLE：可编辑母版＋SVG/PDF预览。
- REQUIRED_CHECKS：五阶段完整；分支与数据流一致；明确标注“拟议/尚未实施”；文字可编辑。
- LIMITS：不得虚构病例分母、性能指标或验证结果。

### B

- ROUTE：科研统计作图模块（forest plot）。
- DECISION：按队列及亚组绘制单panel投稿图。
- DELIVERABLE：可编辑绘图源文件、800 dpi TIFF、矢量PDF。
- REQUIRED_CHECKS：点估计和95% CI与原表逐项一致；参考线、效应方向及尺度正确；亚组层级清楚；无裁切、重叠或字体嵌入问题。
- LIMITS：不补造缺失效应量，不擅自合并队列或计算汇总效应。

### C

- ROUTE：专利附图/精确矢量流程图模块。
- DECISION：不用生成式图片；依据确认步骤制作纯黑白A4竖版图。
- DELIVERABLE：先交结构草图核对逻辑，再交可编辑母版，随后导出SVG及渲染预览。
- REQUIRED_CHECKS：步骤、分支、箭头方向逐项核对；线宽和字体统一；黑白打印可辨；A4缩放后文字清晰；SVG元素可编辑。
- LIMITS：不添加未确认算法、患者数据、效果结论或装饰性颜色。

### D

- ROUTE：Methods文字表述。
- DECISION：无需额外流程图；三步线性动作以一句或短段落说明更合适。
- DELIVERABLE：可复现的Methods描述，注明CSV输入、列名核验规则和汇总表输出。
- REQUIRED_CHECKS：输入、核验条件、输出及软件版本交代清楚。
- LIMITS：仅在编辑或期刊明确要求图示时再绘制。

## 输出 Y

### A

**ROUTE**：`research-flow-diagrams`
**DECISION**：按“方案阶段”制作；首选可编辑 Mermaid 母版，不画成结果图。
**DELIVERABLE**：`.mmd` 源码、图题/图注、元素—来源/状态表；需要预览时再渲染 SVG。
**REQUIRED_CHECKS**：核对节点、箭头及训练—内部验证—外部验证边界；所有步骤标为“拟议/待核”；检查纵向布局、分支归宿及可编辑性。
**LIMITS**：不填病例分母、性能或验证结果，不暗示研究已经执行或不存在的数据隔离措施。

### B

**ROUTE**：`plot-research-statistics`
**DECISION**：制作单 panel forest plot；仅用现有效应量和95% CI，不反推原始数据。
**DELIVERABLE**：白底 RGB/LZW 800-dpi TIFF、单页矢量 PDF、独立可运行代码、输入来源/哈希与复现命令。
**REQUIRED_CHECKS**：核对效应指标、CI定义、方向、无效线、尺度及三个队列/亚组排序；重开 TIFF 检查像素、双向 DPI、物理尺寸；渲染 PDF 检查字体、矢量性、裁剪、重叠和区间完整性，并记录 P01–P24 状态。
**LIMITS**：不新增检验、不拼多 panel；未实际查看两种导出文件不能判定通过。

### C

**ROUTE**：主模块 `write-chinese-medical-patent`；附图制作交接 `research-flow-diagrams`。
**DECISION**：先冻结结构与专利用语，再出成品。
**DELIVERABLE**：顺序为 Mermaid 可编辑母版 → 术语/编号映射 → 同源渲染 SVG；采用 A4 竖版、TB布局、纯黑白。
**REQUIRED_CHECKS**：逐项核对已确认步骤、箭头、条件和分支归宿；与说明书/权利要求术语及附图编号一致；检查每行不超过4节点、无蓝灰填充/渐变/阴影，并实际打开 SVG 做裁剪、重叠、字号和黑白视觉检查。
**LIMITS**：不补患者数据、参数、效果或未确认路径；附图完成不等于申请文件可提交或具备授权前景。

### D

**ROUTE**：`research-flow-diagrams` 的“先判断文字是否更清楚”门槛。
**DECISION**：无需额外画图；三步线性动作写入 Methods 更合适。
**DELIVERABLE**：一句或一段方法描述，明确 CSV 输入、列名核对规则和汇总表输出。
**REQUIRED_CHECKS**：确认顺序、列名判定标准、输出表内容与实际实现一致。
**LIMITS**：若后续出现分支、异常处理、多人职责或编辑明确索图，再升级为流程图。
