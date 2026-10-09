# 单panel布局、导出与验收

## 尺寸、样式和字体

内部起点89×70 mm；根据内容调整。Nature官方初投/制作阶段的尺寸表述有差别，不能把一套参数叫所有Nature子刊标准。最终物理尺寸下核查字体，统一sans-serif；Arial/Helvetica缺失时记录实际已安装替代名称，中文/希腊/数学符号检查字形覆盖。

白底、适量留白、细轴线；连续非负用顺序色图，有明确中心才用发散色图，缺失专色；避免jet/rainbow。颜色辅以标记/线型，灰度检查不等于完整色觉可访问性认证。

## 防裁剪和碰撞

先画完整数据/区间/标签，再draw检查renderer文字bbox。标题、轴标签、刻度、offset、色标、图例、注释均检查。优先扩大/重分配画布、换行、减少刻度、合并重复图例，不删数据或缩短CI。旋转刻度后仍检查边界。

优先constrained layout，不随后调用tight_layout。固定尺寸默认bbox_inches=None；tight裁剪可能改变物理宽度，不是默认修复。图例绘图区外且画布内，外置后主图不能过窄；长图例换行/上移/直接标签，不以loc='best'验收。

adjustText只在最终尺寸和所有绘图完成后调用，并核查引导线归属；不会认证所有轴文字和导出后端无碰撞。注释与数据的碰撞仍人工看。

## 工具与复现

依赖Python、Matplotlib、NumPy、pandas、Pillow、PyMuPDF；自定义helper无需pandas。可选库不安装也可用基础工具；记录实际版本。

```bash
python scripts/plot_panel.py --data /path/verified.csv --spec /path/panel.json --out /path/panels/Fig2A
```

输出包含同名TIFF/PDF、自动QA、代码副本、配置和授权输入副本。默认不覆盖，使用新版本目录；确认覆盖范围后才用--overwrite。在panel目录执行QA中的reproduce_command，代码无需个人skill绝对路径。copy_input=false时保存原输入绝对路径/哈希，数据受限时按此处理。

JSON至少设置panel_id、kind、columns、question、analysis_unit、xlabel/ylabel（含单位）；按任务设置width_mm、height_mm、font、seed、uncertainty、transformations、copy_input。columns为角色到CSV列名的映射：

| kind | columns与附加配置 |
| --- | --- |
| strip、box | y；多组加group，可用order指定完整组序；box保留全部原始点 |
| violin | 同上，加density_support=[下界,上界]，无界用null；bandwidth默认scott。至少5个非同值观测只是运行保护，不认证KDE科学充分性 |
| paired | y、group、id；恰好两个条件；order决定方向；重复ID×条件报错，缺失只显示真实观测、不补线 |
| scatter | x、y，可加group；数值轴，不自动回归/检验 |
| line | x、y，可加group；每序列x唯一；可加low/high及uncertainty；expected_x明确全部有序时点，未观测时点断线 |
| forest | label、y（估计）、low、high及uncertainty；reference按效应定义；比值可用xscale=log并确保正值 |
| histogram | y，可加group；bins默认auto且各组共用边界，具体边界记入QA |
| ecdf | y，可加group；按真实非缺失分母阶梯累计 |
| heatmap | x（列类别）、label（行类别）、y（数值）；必填vmin/vmax，可加center、cmap、colorbar_label；不重复单元格平均 |
| bar | label、y；bar_semantics=count或proportion；比例还需denominator说明，连续均值柱报错 |

入口不添加新P值/CI，不自动构建高级诊断/生存统计，也不自动对数据注释避让；有这些需求时使用专用实现并人工核查。自动通过只说明所覆盖的技术检查通过，图注/样本数和统计语义还须单独核验。

自定义绘图使用panel_tools的panel_style、new_panel和export_panel。一个主要axis；色标以_colorbar识别；风险表等额外axis设label='_panel_auxiliary'，并在provenance说明，不能借此拼组图。

## 格式核查

- TIFF直接从绘图对象800dpi渲染，RGB白底/LZW；重新打开核查双向DPI≈800、像素≈毫米/25.4×800（取整允许1像素）；不从旧300dpiPNG放大。
- PDF单页、相同尺寸，点/线/字保持矢量，TrueType嵌入；不整图截图、不转文字轮廓。矢量PDF没有800dpi概念，DPI只用于其位图层。
- 统计热图可用未栅格化pcolormesh；原生影像保留位图并如实称混合PDF，不造矢量细节。大点云栅格化须授权。
- 核查PDF页面、字体/Type3、路径与位图，扩展名不是证明。自动报告覆盖启发式文字bbox、图例与轴区、主轴数量、TIFF元数据和PDF对象；不保证所有语义/数据碰撞/字形/后端差异。例外须逐项有理由，不批量忽略。
- 默认拒绝clip_on文本注释，避免把被轴边框截字误判画布安全；从源代码定位修复。

## 最终视觉闭环

从实际TIFF生成预览，从实际PDF渲染页面；分别逐panel查看完整图和局部文字/图例/误差线，在最终尺寸和放大比例核查。对照数据看须/端帽、点数/缺失、色标、参考线。发现问题改源代码重导出，再检查最新两种格式，不混旧预览。自动通过但未看图记录visual_review=pending；实际逐图查看后另填通过/例外/不通过，不能用OCR或元数据认证视觉PASS。
