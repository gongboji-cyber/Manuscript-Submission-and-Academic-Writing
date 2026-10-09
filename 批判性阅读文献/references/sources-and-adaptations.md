# 来源、方法入口与改编

## 目录

- GitHub规则与采用边界
- 评论案例（MLA）
- 官方方法入口
- 用户样稿与隐私
- 上游MIT通知

查阅日期：9 Oct. 2026。采用下列公开规则，以中文重新组织工作流程、36项清单、反证卡与评论简报；未移植上游脚本、配置、模型委派、安装器或图像API。没有执行或验证上游代码，也不承诺原项目认可或性能。

## GitHub规则与采用边界

| 来源与锁定版本 | 实际读取 | 提炼并重写 | 不继承 |
| --- | --- | --- | --- |
| K-Dense Inc. [Scientific Critical Thinking](https://github.com/K-Dense-AI/claude-scientific-writer/blob/529b9f73ab4b48925027145800d7b49e96ccfd3c/.claude/skills/scientific-critical-thinking/SKILL.md). *GitHub*, 2026. Accessed 9 Oct. 2026. | SKILL.md和references/core_capabilities.md；MIT | 主张/证据分开、设计适配、具体比例适当的批评、条件判断 | 固定证据阶梯、通用GRADE简化、外部制图API |
| Chen, Po-Wei. [Paper Review](https://github.com/drpwchen/paper-review-and-digest/blob/79a3fca7e689e01119c740af1d1f0e64bd0f6fee/paper-review/SKILL.md). *GitHub*, 2026. Accessed 9 Oct. 2026. | paper-review/SKILL.md；MIT | DOI身份与语义两层、按设计核查、公开回复/修订检查、有限材料披露 | 声望/h-index评真伪、固定阶段/引用数、404=虚构、脚本决定语义真值、机械GRADE、特定Obsidian/Zotero配置 |

也查阅ByteDance deer-flow的academic-paper-review/SKILL.md（版本845af593017f88600f92108f2ae52f812d0a30a7），作为结构对照；未复制其文本/模板/代码，不继承固定至少三个优缺点、1—5打分或Accept/Reject式裁决。其内容是同行评议用途，与寻找成立的公开评论切口有区别。

Kassis, Timothy, et al. “Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents.” *arXiv*, 2026, https://doi.org/10.48550/arXiv.2609.00065. Accessed 9 Oct. 2026. 核实当前记录为2026-09-02修订，未列期刊版本；只用于所借鉴skill的来源，不作为医学方法有效性的证明。

## 评论案例（MLA）

以下只提炼已读评论/回复的论证方法；未复核完整原研究和全部补充，也未重跑其计算。短篇评论发表不等于每个观点已获科学证实。

- Christensen, Daniel Mølager, et al. “Matters Arising: Immortal Time Bias in the Analysis of Drug Prescription Trajectories.” *npj Digital Medicine*, vol. 5, 2022, article 190, https://doi.org/10.1038/s41746-022-00722-6. Accessed 9 Oct. 2026. 实际读取PMC全文：https://pmc.ncbi.nlm.nih.gov/articles/PMC9789065/ 。
- Mortensen, Laust Hvas, and Søren Brunak. “Reply to: Immortal Time Bias in the Analysis of Drug Prescription Trajectories.” *npj Digital Medicine*, vol. 5, 2022, article 191, https://doi.org/10.1038/s41746-022-00724-4. Accessed 9 Oct. 2026. 读取正文，承认具体生存比较问题并保留描述贡献；不能引申为全文无效。
- Pasquier, Diego. “On Meta-Analytic Models and the Effect of Hydroxychloroquine Use in COVID-19.” *Nature Communications*, vol. 16, 2025, article 6353, https://doi.org/10.1038/s41467-025-60478-x. Accessed 9 Oct. 2026.
- Schmitt, Andreas M., et al. “Reply to: On Meta-Analytic Models and the Effect of Hydroxychloroquine Use in COVID-19.” *Nature Communications*, vol. 16, 2025, article 6354, https://doi.org/10.1038/s41467-025-60479-w. Accessed 9 Oct. 2026. 两文正文用于学习模型精度、点估计和显著性边界；不从这场争论作治疗建议。
- van Tellingen, Olaf, and Renee X. de Menezes. “Reanalysis of In Vivo Drug Synergy Validation Study Rules Out Synergy in Most Cases.” *Nature Communications*, vol. 16, 2025, article 8534, https://doi.org/10.1038/s41467-025-62617-w. Accessed 9 Oct. 2026. 本次读取正文中的公式/加性反例和数据处理/重分析段落，未核图像、补充或作者回复；用作最小反例方法示例，不复制全部指控。

另检索到Haibe-Kains等的“Transparency and Reproducibility in Artificial Intelligence”（Nature，2020，DOI 10.1038/s41586-020-2766-y）及其回复，但本次出版社/PMC全文访问失败；不将其列为完成精读的案例，不以摘要代替细节证据。

## 官方方法入口

- University of Bristol. “QUADAS.” https://www.bristol.ac.uk/population-health-sciences/projects/quadas/ . Accessed 9 Oct. 2026. 官网当前推荐QUADAS-3，精确到诊断准确性估计的偏倚/适用性；实际任务读取最新工具，不复制完整量表。
- Moons, Karel G. M., et al. “PROBAST+AI: An Updated Quality, Risk of Bias, and Applicability Assessment Tool for Prediction Models Using Regression or Artificial Intelligence Methods.” *BMJ*, vol. 388, 2025, e082505, https://doi.org/10.1136/bmj-2024-082505. Accessed 9 Oct. 2026. 本次经PubMed记录/摘要核身份与开发/评价用途，未声称已完成全部信号问题阅读：https://pubmed.ncbi.nlm.nih.gov/40127903/ 。
- GRADE Working Group. “GRADE Handbook.” https://gradepro.org/handbook/ . Accessed 9 Oct. 2026. 阅读结局/证据体与非机械评级说明；官网指向新GRADE Book，使用时重核，不把论文整体分数称正式GRADE。
- Riskofbias.info. “Risk of Bias Tools.” https://www.riskofbias.info/ . Accessed 9 Oct. 2026. RCT、非随机干预与暴露分别选匹配工具；ROBINS-I V2官网本次仍标2025-11-20草案。这里只核官方范围/状态，实际评级另读对应官方材料。

这些是方法入口，不是本skill通过官方认证的声明。报告规范、偏倚工具、证据确定性和评论问题优先级是不同概念；禁止相互替代或把工具名称当完成证据。

## 用户样稿与隐私

本次读了四份上传DOCX的正文/参考文献及附加文本部件，抽象为诊断分类、风险与决策、筛查核验、人时与零点四条路径。录用状态来自用户说明；尚未独立核实出版版本。该提炼不公开标题、联系方式、作者声明、未发表全文、私人回复、原数据或接受函。AJRCCM目标原论文页面本次访问失败，因此规则歧义在这里是样稿的论证模式，不被标为重新证实的原文缺陷。

## 上游MIT通知

以下适用于相应来源与改编，不统一改变其他既有skill的授权。

### K-Dense Inc.

MIT License

Copyright (c) 2025-2026 K-Dense Inc.

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

### Po-Wei Chen

MIT License

Copyright (c) 2026 Po-Wei Chen (drpwchen.com)

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

