---
name: prepare-chinese-software-copyright
description: Evidence-grounded preparation and pre-submission audit for Chinese computer software copyright registration (计算机软件著作权登记/软著). Use for 软著制作、软件著作权申请材料、申请表信息、软件说明书/用户手册、源程序鉴别材料、代码抽取、前后30页、软著材料一致性检查、补正前自检. Read the real project first, separate verified facts from drafting choices, preserve source-code authenticity, and apply current official rules. Do not invent code, development dates, authorship, ownership, functionality, screenshots, source-line counts or registration conclusions.
---

# 软著制作规范

## 核心定位

本 skill 用于把**真实存在的软件项目**整理成中国计算机软件著作权登记所需的可核对材料，并在提交前完成真实性、一致性、权属和形式审计。

它不是“自动编一个软件去拿证”，更不是“把几千行 AI 生成代码塞进 Word”。软著保护的是已经形成的软件表达，登记材料应当能回到真实项目、真实权属和真实文档。

本 skill 默认覆盖：

1. 项目扫描与软件事实台账；
2. 软件名称、版本、开发完成日期、发表状态等申请字段整理；
3. 源程序鉴别材料规划与抽取；
4. 文档鉴别材料（用户手册、操作说明、设计说明等）制作；
5. 申请字段—源码—文档—截图之间的一致性审计；
6. 权属、合作开发、委托开发、职务开发和第三方代码风险提示；
7. 提交前 GO / HOLD / STOP 裁决。

本 skill 不替代中国版权保护中心、版权行政机关、律师或代理机构，不承诺登记成功，也不把登记证书等同于对全部权属事实的终局认定。

## 资源导航

开始工作前按任务读取：

- 当前法律与登记规则：`references/current-rules.md`
- 项目扫描、源码选择与鉴别材料：`references/source-code-materials.md`
- 申请字段、说明文档和截图一致性：`references/application-and-documentation.md`
- 官网字段 schema 与长度/来源口径：`references/application-field-schema.md`
- 工作区、文档结构与阶段门禁：`references/workspace-and-document-structure.md`
- 自动化脚本与执行边界：`references/automation-and-scripts.md`
- DOCX 自动生成、真实分页 QA、提交包构建脚本：`scripts/`
- 权属、第三方代码与开源合规：`references/ownership-and-third-party-code.md`
- 完整提交前自检：`references/checklist.md`
- 公开来源与借鉴边界：`references/sources-and-adaptations.md`
- 软件事实台账模板：`assets/software-fact-ledger-template.md`
- 申请信息模板：`assets/application-info-template.md`
- 审计报告模板：`assets/audit-report-template.md`
- 阶段确认台账模板：`assets/gate-ledger-template.md`
- canonical 申请事实 JSON：`assets/application-facts-template.json`

官方法规、登记机构当前页面、用户真实项目和权属文件优先级最高。GitHub 项目只能提供工作流与工程实现参考，不能替代官方规则。

## 0. 不可突破的约束

- 不编造源代码、功能模块、页面、接口、算法、数据库、截图、开发完成日期、首次发表日期、开发者、著作权人或源程序量。
- 不为“凑够 60 页”生成不存在的业务代码；源码不足时按真实规模处理。
- 不把第三方库、框架源码、自动生成代码、依赖目录、构建产物、模板样板当作本软件原创主体代码。
- 不把“项目能运行”自动等同于“申请人拥有全部著作权”。权属必须单独核对。
- 不把软件名称、版本号、著作权人、开发完成日期、主要功能在申请表、手册、源码页眉和截图中写成多个版本。
- 不硬编码“每页必须 60 行”。现行《计算机软件著作权登记办法》要求通常情况下程序每页不少于 50 行；文档每页不少于 30 行。若官方系统或最新办事指南另有当前格式要求，以官方当前要求为准。
- 不把“前 30 页 + 后 30 页”误解为必须来自任意拼接的两堆代码。正常交存强调源程序前、后各连续 30 页；总程序不足 60 页时应提交全部。
- 不在公开仓库上传用户未授权公开的源码、密钥、患者数据、商业秘密、内部接口、私人合同或身份证明。

## 1. 先判任务类型

### A. 从真实项目生成整套软著材料
必须先扫描项目，再生成建议稿和材料。默认输出：事实台账、申请信息、源码材料计划、说明文档草稿和审计报告。

### B. 只生成源程序鉴别材料
重点做源码识别、排除第三方/生成代码、连续区间规划、页数/行数核验和页眉一致性。

### C. 只写软件说明书/用户手册
必须以真实界面、真实功能和真实项目结构为依据。没有截图时可以保留明确的截图占位符，但不能伪造界面。

### D. 填申请表/字段
只整理已有事实并指出缺失项。对开发方式、权利取得方式、发表状态等不确定项必须询问或标为待确认。

### E. 既有材料审计/补正
先做交叉一致性矩阵，不默认整篇重写。定位真实风险后定点修订。

## 2. 建立软件事实台账

任何正式材料前先填写 `assets/software-fact-ledger-template.md`。

每个关键事实至少记录：

| ID | 事实 | 来源 | 核验层级 | 是否写入申请表 | 是否写入文档 | 是否进入源码材料 | 待确认 |
| --- | --- | --- | --- | --- | --- | --- | --- |

建议核验层级：

- S0：仅用户口头陈述；
- S1：项目文件/配置可见；
- S2：源码或提交历史直接支持；
- S3：可运行/构建/截图或独立检查支持；
- S4：合同、任务书、登记文件等正式材料支持。

权属和开发时间类事实，优先寻找 S4 或至少多源交叉支持。

## 3. 项目扫描必须先于写作

优先使用 `scripts/scan_project.py` 建立可复算 inventory；若环境不允许执行脚本，再由 agent 手工扫描，但输出字段应尽量与 inventory schema 对齐。脚本结果只是工程事实，不是权属结论。


扫描目标不是“统计文件数”，而是确定什么软件真实存在。

至少识别：

- 项目类型：Web、桌面、移动端、小程序、后端服务、数据分析工具、插件、SDK、算法平台等；
- 技术栈与主要语言；
- 入口文件与运行方式；
- 核心业务模块；
- 数据层、接口层、前端页面/交互层；
- 版本信息来源；
- 可用源码总量与可交存源码范围；
- 第三方依赖、自动生成代码和外部资源；
- 能否获取真实截图或运行界面；
- 软件名称在代码、包名、标题、README 中是否一致。

默认排除：依赖目录、构建产物、缓存、日志、二进制、压缩包、字体、媒体资源、锁文件的大段机械内容、自动生成代码和第三方 vendored 源码。

## 4. 源程序鉴别材料先做“真实性选择”，再做分页

现行规则基线：程序和文档鉴别材料通常由前、后各连续 30 页组成；不足 60 页提交全部；除特定情况外，程序每页不少于 50 行，文档每页不少于 30 行。

工作流：

1. 使用 `scripts/propose_code_selection.py` 或等价人工流程生成候选源码清单；
2. 标记原创核心代码、第三方/生成代码、配置/样板代码；
3. 确定可代表“申请软件本身”的连续代码序列；
4. 规划前段与后段；
5. 对确认后的第一方源码用 `scripts/count_first_party_loc.py` 复算 LOC/hash，并用 `scripts/build_source_page_map.py` 建立名义页映射；排版后仍需核验实际每页行数、页数、连续性和文件边界；
6. 若使用例外交存，必须明确采用的官方允许方式及原因。

不要只按文件扩展名筛选。应优先保留能体现软件主体逻辑的源码，同时维持真实文件顺序和连续性。

详见 `references/source-code-materials.md`。

## 5. 文档鉴别材料不是宣传册

文档结构不应只有一种固定模板。先判软件形态，再选择 GUI/Web 操作手册、CLI/科研工具使用说明书或 SDK/API 接口说明。详细结构见 `references/workspace-and-document-structure.md`。

借鉴 SoftwareCopyright-Skill 的优点：操作手册要像真实软件随附文档，先理解业务再写；核心页面/流程要从普通用户视角描述用途、入口、动作、限制和反馈；“相关文档”只有真实存在时才列出，禁止为模板完整虚构总体设计、测试案例等历史资料。


“文档”可以是用于描述程序内容、组成、设计、功能规格、开发情况、测试结果或使用方法的文字资料和图表。实际提交哪一种，以项目现状和当前登记要求为准。

默认优先生成“软件说明书/用户操作手册”，结构可包括：

1. 软件概述；
2. 开发目的和适用场景；
3. 运行环境；
4. 软件架构/模块组成；
5. 安装或启动方式；
6. 功能模块及操作流程；
7. 关键页面与截图；
8. 数据输入、处理和输出；
9. 异常/权限/数据管理（如真实存在）；
10. 版本说明。

禁止写入项目没有的“AI 智能推荐、区块链存证、自动诊断、实时协同”等功能。

## 6. 申请字段必须来自事实，不来自“常见写法”

高风险字段包括：

- 软件全称、简称、版本号；
- 开发完成日期；
- 首次发表日期与发表状态；
- 开发方式；
- 著作权人及其顺序；
- 权利取得方式；
- 软件分类/用途；
- 编程语言；
- 源程序量；
- 开发硬件/软件环境；
- 运行硬件/软件环境；
- 主要功能与技术特点。

对任何不确定字段，使用“待确认”，不要自动填“原始取得”“独立开发”“未发表”。

## 7. 权属审计单独进行

特别检查：

- 是否为职务开发；
- 是否为合作开发；
- 是否为委托开发；
- 是否基于他人软件修改；
- 是否存在项目任务书、合同、许可或转让；
- 申请人与代码仓库提交者是否不一致；
- 是否混入他人受限许可代码；
- 是否包含 GPL/AGPL 等可能影响分发义务的组件；
- 是否存在来源不明的复制代码。

登记并不消除这些风险。材料制作阶段只能基于已知证据判断，不替用户创造权属。

详见 `references/ownership-and-third-party-code.md`。

## 8. 一致性矩阵是提交前核心

可使用 `scripts/final_consistency_audit.py` 对 canonical 申请事实、DOCX/TXT/MD 正式材料和 SOURCE_PAGE_MAP 做自动文本级检查。自动检查不替代 Word/WPS/PDF 视觉渲染，也不作法律权属判断。


至少建立：

| 项目 | 申请表 | 源码材料 | 文档 | 截图/界面 | 项目事实 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| 软件全称 |  |  |  |  |  |  |
| 版本号 |  |  |  |  |  |  |
| 著作权人 |  |  |  |  |  |  |
| 主要功能 |  |  |  |  |  |  |
| 运行环境 |  |  |  |  |  |  |
| 开发完成日期 |  | 不适用 | 可选 | 不适用 |  |  |

任何实质冲突必须在提交前消除。

## 9. 标准工作流

默认使用分层工作区：`项目证据 → 草稿 → 截图 → 正式资料 → 内部审计 → 可选开发证据链`。正式资料与内部审计必须分开，避免将 TODO、agent 状态词、私人路径或内部研发记录误上传登记系统。

关键门禁至少包括：业务理解、申请事实、代码选择、截图计划、最终草稿和人工渲染 QA。任一已确认事实后来改变，对应门禁必须失效并重新确认。门禁台账模板见 `assets/gate-ledger-template.md`。


```text
输入：项目目录 / 仓库 / 既有软著材料
  ↓
Step 1 读取官方当前规则与本 skill references
  ↓
Step 2 运行 `run_pipeline.py bootstrap`（或等价流程），扫描真实项目并建立软件事实台账
  ↓
Step 3 进行权属与第三方代码初筛
  ↓
Step 4 生成业务理解.md/json，并建立 BUSINESS_UNDERSTANDING 门禁
  ↓
Step 5 整理申请字段，建立 APPLICATION_FACTS 门禁
  ↓
Step 6 生成代码候选清单与选择 JSON，建立 CODE_SELECTION 门禁；确认后运行 `run_pipeline.py post-confirm` 复算 LOC 与页映射
  ↓
Step 7 按软件形态起草说明文档与截图计划
  ↓
Step 8 使用 `build_docx_materials.py` 生成说明书 DOCX + 源程序 DOCX
  ↓
Step 9 使用 `render_pagination_qa.py` 实际渲染 DOCX→PDF/PNG，核对真实页数和分页漂移
  ↓
Step 10 运行自动一致性审计 + Word/WPS/PDF 人工视觉 QA
  ↓
Step 11 使用 `build_submission_package.py` 构建正式上传包与内部归档
  ↓
Step 12 输出 READY_FOR_SUBMISSION / GO / HOLD / STOP
```

除非用户明确要求“一竿到底且无需中间确认”，否则对**权属、名称、版本、日期、发表状态、开发方式**至少做一次确认门。即使用户授权一竿到底，agent 也只能在无冲突证据时继续，不得把未知法律事实自动填成常见答案。

## 10. 提交前裁决

### GO
关键事实可核；源码真实；权属没有已知矛盾；申请表、源码、文档、截图一致；形式要求已按当前官方规则复核。

### HOLD
软件本身真实，但仍缺关键确认，例如著作权人、开发完成日期、合作/委托合同、最终截图、当前官网字段或 PDF 分页。

### STOP
发现明显伪造源码、申请人无合理权属依据、核心材料来自他人项目、软件实际不存在，或要求通过虚构材料骗取登记。

## 11. 陌生情景检索路径

遇到本 skill 未覆盖的问题：

1. 先判断属于登记主体、权属、鉴别材料、例外交存、申请字段、补正、变更/补充登记还是第三方许可；
2. 查《计算机软件保护条例》；
3. 查《计算机软件著作权登记办法》；
4. 查国家版权局、中国版权保护中心当前办事页面与系统提示；
5. 再查可信代理实务、公开案例和 GitHub 工具；
6. 明确区分“法规明确”“官网当前要求”“工程经验”“仍需人工确认”。

不得用第三方博客覆盖官方规则。

## 12. 交付

根据任务交付一种或多种：

- 软件事实台账；
- 软著建议稿；
- 申请表字段信息；
- 源码候选清单与选择计划；
- 源程序鉴别材料；
- 软件说明书/用户手册；
- 截图清单；
- 权属与第三方代码风险表；
- 一致性矩阵；
- 提交前审计报告；
- 补正材料修改稿；
- `业务理解.md/json`；
- `代码文件候选清单.md` 与 `代码文件选择.json`；
- `截图计划.md` 与截图证据台账；
- 分层工作区与 generation report。

最终边界必须明确，例如：

“该版本已完成软著材料整理与内部一致性审计；最终登记字段、权属证明、上传格式与受理要求仍应以中国版权保护中心/登记系统当前要求和申请人的真实权属文件为准。”

## 13. 自动化执行快捷路径

当本地可运行 Python 3 时，推荐：

```bash
python scripts/run_pipeline.py bootstrap "<项目目录>" --profile auto
# 人工/模型确认业务、权属和代码候选后
python scripts/run_pipeline.py post-confirm "<项目目录>" "<代码文件选择.json>"
# 由确认后的 Markdown + facts + screenshot manifest 生成 DOCX
python scripts/run_pipeline.py build-docx --project "<项目目录>" --facts "<application-facts.json>" --manual-md "<软件说明书.md>" --selection "<代码文件选择.json>" --out-dir "<04_正式资料>"
# 分别对说明书和源程序 DOCX 做真实渲染 QA
python scripts/run_pipeline.py render-qa --docx "<软件说明书.docx>" --out-dir "<05_内部审计/manual_qa>" --kind manual
python scripts/run_pipeline.py render-qa --docx "<源程序鉴别材料.docx>" --out-dir "<05_内部审计/source_qa>" --kind source --source-map "<..._SOURCE_PAGE_MAP.csv>"
# 自动一致性审计
python scripts/run_pipeline.py audit --application "<application-facts.json>" --manual "<软件说明书.docx>" --source-map "<..._SOURCE_PAGE_MAP.csv>"
# 人工 Word/WPS/PDF 逐页确认后，将 manual_render_qa 设为 true，再构建最终提交包
python scripts/run_pipeline.py package --facts "<application-facts.json>" --manual-docx "<软件说明书.docx>" --manual-pdf "<软件说明书.pdf>" --source-docx "<源程序鉴别材料.docx>" --source-pdf "<源程序鉴别材料.pdf>" --out-dir "<最终提交包>" --require-pdf
```

任何阶段遇到未知权属、日期、发表状态或第一方代码边界时，流水线必须停在门禁，而不是填入“常见答案”。
