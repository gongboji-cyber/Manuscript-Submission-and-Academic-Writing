# 来源与改编说明

查阅日期：2026-10-09（Asia/Shanghai）。本skill将补充写作与投稿文件一致性思路用中文重新组织，加入适用于公开数据重分析、冻结模型、预处理及代码审计的路线、正文证据分工、32项清单和独立模板。未移植上游代码、安装器、全套工作流或硬编码期刊阈值，也不承诺原项目的性能或原作者认可。

## 采用的公开规则

| 来源 | 本次版本/文件 | 采用并重写的部分 |
| --- | --- | --- |
| Aperivue. MedSci Skills. | [sync-submission/SKILL.md](https://github.com/Aperivue/medsci-skills/blob/3b14ae2a9424a3a2b14f38338bc527823df06e96/skills/sync-submission/SKILL.md)；[assemble_supplement.py](https://github.com/Aperivue/medsci-skills/blob/3b14ae2a9424a3a2b14f38338bc527823df06e96/skills/sync-submission/scripts/assemble_supplement.py) | 台账与文件对应、重排后的调用核对、来源与成品版本绑定、组装/哈希检查不能代替内容或视觉判断。脚本仅静态阅读头部及相关组装流程说明，未执行或移植。 |
| Chiou, Wenyu. Academic Writing Skills. | [figures-tables-and-supplements.md](https://github.com/WenyuChiou/academic-writing-skills/blob/061d73ea4014e0486c2c753dbe9602dd9c3bb8ef/skills/academic-writing-skills/references/figures-tables-and-supplements.md) | 补充与正文并行发展、主要证据与扩展细节分工、图注/表注的独立阅读、重编号按内容任务逐处核验、最终尺寸视觉检查。 |

按实际科学影响使用P0/P1/P2，而不继承所有上游自动阻断规则。类型+编号分别管理，补充方法S1、图S1与表S1不混为同一对象。将孤立项目与缺少正文/补充入口具体区分，不要求每个面板都在正文列出。将机器检查和静态参考局限写进工作流程。

## 其他阅读与选择边界

本次也查看JasonYan-Bio/science-skills的Science写作模块、K-Dense的scientific-writing以及aipoch的figure-table-supplement-linkage-rules。它们分别提供期刊家族格式、通用证据流程与结构/内容错配提醒；未复制其文本、模板、代码或固定期刊规则。本skill主要依据上表两项来源改编，其余通用规则由已有自查流程和本项目需求独立整理。

## 官方规则入口

[Nature. Supplementary information.](https://www.nature.com/nature/for-authors/supp-info)（本次实际读取）。只作为核查SI类别、与正文/Extended Data分开管理、独立文件描述及格式规则的示例，不推广其编号、格式、文件大小或参考文献要求。

实际任务必须读取目标期刊当前官方作者指南及文章类型规则。规则访问失败记无法核实；不能用本次示例页、搜索摘要、旧指南或第三方skill代替实际合规核查。期刊规定与用户指令按主流程处理，本文件不是期刊认证表。

## 上游MIT通知

以下通知适用于对应来源及其改编，不对其他原有skill作统一重新授权。

### Aperivue/medsci-skills

[原许可](https://github.com/Aperivue/medsci-skills/blob/3b14ae2a9424a3a2b14f38338bc527823df06e96/LICENSE)

MIT License

Copyright (c) 2026 Aperivue (https://aperivue.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### WenyuChiou/academic-writing-skills

[原许可](https://github.com/WenyuChiou/academic-writing-skills/blob/061d73ea4014e0486c2c753dbe9602dd9c3bb8ef/LICENSE)

MIT License

Copyright (c) 2026 Wenyu Chiou

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

