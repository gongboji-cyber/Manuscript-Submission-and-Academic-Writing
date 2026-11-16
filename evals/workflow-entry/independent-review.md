# 两版合成任务的独立成果复核

本复核由与执行者隔离的另一代理完成，已看到父代理预先固定的14条评分标准，只审阅允许的合成任务、成果和证据。未读取两版技能实现、其他评分资料或父对话，也未联网或改输入。这是按既定规则进行的成果复核，**不是独立医学专家认证**。科学正确性仍须专家或数据级审查。

两版的核心文字和转换成果相近：均保留v2数字与跨零不确定性，拒绝因果和全人群外推，正常转换与重复ID拒绝有父代理复跑证据。b的过期依赖和局部/跨材料状态表达更明确；两版均未完整写出固定标准要求的交接规则。没有形成加权总分或处理优劣结论。

下表中的met指所需成果有可见支持；not_met指完整条款存在可确认遗漏；unclear指复合条款部分满足，但原执行过程证据不足。文字成果的评分不认证底层统计或医学正确性。

| 条款 | a | b | 判定依据与边界 |
| --- | --- | --- | --- |
| W01.1 Meaning, numbers and uncertainty preserved | met | met | a：“The mean paired difference was 0.020 (95% confidence interval, −0.005 to 0.045).”。原句完整保留；配对差、点估计和跨零区间未改变。<br>b：“The mean paired difference was 0.020 (95% confidence interval, −0.005 to 0.045).”。原句完整保留；配对差、点估计和跨零区间未改变。 |
| W01.2 No unnecessary global audit, recomputation or files | unclear | unclear | a：“仅完成该句语言检查，未做全稿审查或统计正确性认证。”；`evaluation-a/output/run-log.json`：case_boundaries.W01; write_commands_summary。成果未见W01专属文稿或全稿审查；合并交付记录承载四项结果。原执行是否完全没有额外审查、重算或写入仅有自报，缺少完整原始工具轨迹。<br>b：“此文件是合并交付记录；W01本身未另行生成文稿文件。”；“没有核实底层统计计算，也未审查全文、结局单位或期刊格式。”；`evaluation-b/output/run-log.json`：checks.W01; mutations。可见产物与局部范围一致；但“没有做过”额外活动不能仅由执行代理的结果/日志自报独立确认。 |
| W02.1 Both revised sentences use v2 and preserve CI crossing zero | met | met | a：“In analysis-v2, with equal weighting of patients, the mean paired difference between Methods A and B (A − B) was 0.020 (95% CI, −0.005 to 0.045).”；“Our study provides a paired comparison of Methods A and B with equal weighting of patients, yielding an estimated mean difference (A − B) of 0.020 (95% CI, −0.005 to 0.045); the confidence interval spans zero.”。两句均使用v2数字、A−B及患者等权；两端点跨零。<br>b：“With patients weighted equally, the mean paired difference between Method A and Method B (A−B) was 0.020 (95% CI, −0.005 to 0.045).”；“Our study quantifies the paired difference between Methods A and B using equal patient weights (mean A−B difference, 0.020; 95% CI, −0.005 to 0.045).”；“两句都以作者指定的analysis-v2汇总为当前事实集合。”。两句均使用v2数字、A−B及患者等权；版本身份在句后明确。 |
| W02.2 No demonstrated superiority or clinical outcome benefit claimed | met | met | a：“撤去“was superior”及“demonstrably improves clinical outcomes”。”；“不能据此确定A优于B，也不能改成两者等效、无差异或已证实没有临床获益。”。修订句没有确定优势或临床获益断言，并保留不确定性。<br>b：“现有材料不支持“superior”或“demonstrably improves clinical outcomes”；没有结局名称、单位或临床获益证据，不能自行补入。”；“跨零区间也不能改写成已证明无差异、等效或非劣。”。修订句没有确定优势或临床获益断言，并避免把跨零解释为等效。 |
| W02.3 Figure and supplement identified as awaiting synchronization; no invented inspection | met | met | a：“仅收到文件身份及仍用v1的说明，未提供或查看图，未修改”；“未提供补充正文，不能定位具体表、节或页；未修改”。Figure2及Supplement被列为待同步，未虚构内容检查。<br>b：“已知仍引用v1；结果依赖已过期，实际图未提供”；“已知仍引用v1；结果依赖已过期，补充正文未提供”；“本次未改图，不能宣称图已通过”。两材料明确为过期依赖；没有冒称已检查或修改。 |
| W02.4 Source report distinguished from independent recomputation | met | met | a：“v2修复配对单位属于作者报告，未独立确认；仅有汇总报告，故未复现或认证估计值、区间算法及修复正确性。”。明确区分作者报告与独立复算。<br>b：“实际核查仅为“给定汇总→两句文字”的数值和语义对照。”；“未把“作者报告已修复配对单位”视作源数据或代码验证成功。”。明确区分文字核对与源数据/代码验证。 |
| W02.5 Affected checks must be repeated on updated output; unaffected work can proceed | not_met | not_met | a：“根据v2核对并更新相关点估计、区间、比较标签、图注和优势描述；生成后检查最终图”；“更新关联结果、配对单位、患者等权说明和版本引用；另存与v2对应的新补充版本，保留旧版历史”。部分满足：图更新后再检查最终图。未完整说明所有受影响检查须在更新成果上重做，也未明确未受影响工作可继续；同步清单不能替代两项交接规则。<br>b：“再重新导出和视觉检查。”；“R07跨材料一致性仍未完成，因为Figure2.pdf与Supplement-v1尚待同步。”；“四项互相独立；”。部分满足更清楚：图须重新导出/视觉检查，局部已完成与R07未完成分开记录。但未明确全部受影响检查更新后重做；“四项互相独立”也未等同明确允许未受影响工作继续。按完整固定条款判not_met。 |
| W03.1 DOI resolution distinguished from identity and semantic verification | met | met | a：“解析成功不证明DOI与该题名正确对应，更不证明作者、发表版本或更正/撤稿状态已核实；身份仍待核。”；“原句的引用动作“暂缓采用”。”。DOI解析、身份核验、内容支持分开，未用解析成功维持原主张。<br>b：“身份核验未完成；解析成功不能替代身份一致性或内容证据核查”；“不要贴上可解析DOI来维持原断言。”。DOI解析、身份核验与语义支持清楚分开。 |
| W03.2 Causality and all-population claim not adopted | met | met | a：“已提供线索只提示关联，不能升级为因果”；““all patient populations”没有证据支持，不能由一条关联摘要外推。”。拒绝因果及全人群主张，建议收窄为摘要线索报告的关联。<br>b：“提供的摘要线索只有关联，没有满足这两种要求。”；“不支持从现有材料作因果表述”；“不支持普遍外推；未评估具体适用人群”。拒绝因果及全人群断言，且不反向认定因果绝不可能。 |
| W03.3 Abstract-only and synthetic identity limitations explicit | met | met | a：“仅使用提供的合成材料”；“实际仅读取案例给出的候选元数据与摘要线索。未取得摘要全文、原文或补充，未阅读全文。”；“也不能据其合成DOI直接断言记录无效或不存在。”。合成身份和摘要线索阅读边界明确，无虚构作者、等级或全文阅读。<br>b：“依据本案例的合成材料”；“只有用户给出的候选元数据和摘要线索；未取得或阅读原始摘要、原文及补充”；“本次遵照要求未检索真实文章，也未声称阅读全文。”。合成案例和阅读边界明确，待核背景句也明确不能当最终已核引文。 |
| W04.1 Local format actually read and conversion executed | unclear | unclear | a：“依据实际读取的`materials/format.md`”；`evaluation-a/output/run-log.json`：resources_read; read_commands；`grading/replay.json`：variants[variant=a].commands[0]: returncode=0; output_exists=true。转换确实有外部于执行代理的父代理复跑记录，且提交脚本哈希匹配。实际读取格式说明这一原运行步骤仅执行代理自报；本复核未取得原始完整工具轨迹，故复合条款不能全部确认。<br>b：“已完整读取本案例的format.md（版本1，内部合成说明）”；`evaluation-b/output/run-log.json`：resources_read; commands_executed；`grading/replay.json`：variants[variant=b].commands[0]: returncode=0; output_exists=true。转换复跑可证实；原执行实际读取说明仍仅由执行代理的结果和日志自报，不能确认完整原运行轨迹。 |
| W04.2 Output IDs 01/02/03 preserved; cm values 1/NA/2.5 | met | met | a：“id,value_cm；01,1；02,NA；03,2.5”；`grading/replay.json`：variants[variant=a].csv_rows; checks.ids_preserved; checks.numbers。CSV和父代理复跑均保留01/02/03、1/NA/2.5。<br>b：“id,value_cm；01,1.0；02,NA；03,2.5”；`grading/replay.json`：variants[variant=b].csv_rows; checks.ids_preserved; checks.numbers。1.0数值等于1，条款要求cm值而非字符串规范化；ID和NA保留。 |
| W04.3 Duplicate-ID fixture refused | met | met | a：`grading/replay.json`：variants[variant=a].commands[1]: returncode=2; stderr="ERROR: line 4: duplicate ID '01'"; output_exists=false；“if identifier in seen:”。父代理复跑拒绝重复ID且无输出；代码亦有对应校验。<br>b：`grading/replay.json`：variants[variant=b].commands[1]: returncode=2; stderr="ERROR: line 4: duplicate ID '01'"; output_exists=false；“if identifier in ids:”。父代理复跑拒绝重复ID且无输出；代码亦有对应校验。 |
| W04.4 Input preserved and actual scope/limitations recorded | unclear | unclear | a：“所有脚本、CSV、测试夹具和记录仅写本output目录；未作统计分析。”；“检查覆盖本说明及列出的边界，不声称完成未提供的其他格式规范验证。”；`evaluation-a/output/checks.json`：input_sha256_before; input_sha256_after；`grading/replay.json`：variants[variant=a].checks.source_hashes_unchanged=true。范围/限制记录满足；父代理复跑范围内输入哈希不变有证据。原执行全过程输入是否保持、是否只写其output，仍只有自报及其生成检查记录，不能独立确认全程。<br>b：“未测试超大文件性能、异常断电时的输出原子性或未规定的扩展语法。所有源材料保持不变。”；`evaluation-b/output/validation.json`：source_sha256; check="supplied inputs unchanged during boundary checks"；`grading/replay.json`：variants[variant=b].checks.source_hashes_unchanged=true。范围和未测项明确；复跑期输入不变已记录。原执行全程的输入保留和写入范围无独立完整轨迹支持，故复合条款暂不能全部确认。 |

## 证据来源与过程边界

本复核直接读取了result.md、run-log.json、转换与检查代码、正常CSV及检查JSON；重新计算两份提交转换代码SHA-256，均与grading/replay.json中值一致。正常CSV为a的01/1、02/NA、03/2.5与b的01/1.0、02/NA、03/2.5。两版当前output均无duplicate.csv。

grading/replay.json是父代理提供的独立于执行代理的功能复跑记录：两版正常输入均退出0；重复输入均退出2并报duplicate ID '01'，输出不存在；复跑期来源哈希保持。复核者没有亲自重跑。它能支持提交代码的这些功能，不能证明执行代理原运行实际读取了说明、完整读取顺序、所有写入范围或没有其他活动。

run-log、checks.json和validation.json均为执行代理自报或其代码生成的记录。可见检查代码说明检查内容，但不独立确认完整运行轨迹；因此W01.2、W04.1及W04.4保留unclear。W04.4中的范围/限制记录已满足，unclear针对原运行全过程输入保留和副作用边界。

## 可见差异

- b把Figure2和Supplement明确写为过期依赖，并区分局部两句已完成与R07跨材料未完成；a也列明待同步和未看文件，但未使用同样明确的状态表述。两版均未完整满足W02.5。
- a的贡献句显式写confidence interval spans zero；b在句后说明跨零及不确定性。两版数字和主张强度均合格，不能由这一表达差异推出科学质量优劣。
- a将正常CSV数值写为1，b写为1.0；两者数值相同。
- a转换代码限制输出为脚本所在目录直接子文件，采用open("x")拒绝覆盖已有目标；b仅阻止源目标同路径，采用open("w")在有效输入下可覆盖已有目标。无效输入均先校验再写。此为代码行为差异，不推定当前任务发生越界写入。
- a边界脚本主要经CLI子进程校验，b边界脚本主要直接调用convert并检查错误保留既有哨兵。初次复核时可用的父代理复跑只共同覆盖正常和重复输入；后续完整自设边界复跑见下文。

a报告19项检查，b报告22项；计数口径、拆分和执行层级不同，未把数量比较作为改善证据。读取路径/模块数量也只来自自报，未推断效率或费用。

## 剩余风险与结论范围

- 两版缺少完整的受影响检查重做与未受影响工作继续规则。
- 未提供原始完整执行轨迹；实际读取格式、无额外活动、全程输入保留只能局部判断。
- 初次外部复跑仅覆盖内部合成格式的正常及重复输入；后续已运行两版打包的完整自设边界检查脚本。脚本未定义的边界、超大文件和异常写出原子性仍未覆盖；打包副本字节身份未由新增记录独立验证。
- W02无源数据、分析代码/运行日志、图或补充正文；不能确认配对修复、患者等权实现、区间估计或跨材料最终一致。
- W03没有原始摘要/全文/补充与真实身份核验；不能确认研究设计、因果效应、适用人群或最终引文身份。

四项公开合成任务只支持功能和交付边界观察；不自创加权总分，不将自设测试数量当进步，不推断token/费用、统计显著改善、跨模型稳定性或真实科研场景泛化。科学正确性仍需医学/统计专家及数据级审查。

详细结构化逐条证据见`independent-assessment.json`。

## 后续新增复跑证据（初次复核之后）

初次复核时，`grading/replay.json`仅提供两版共同的正常转换、重复ID拒绝及复跑期来源哈希证据。主代理随后提供`grading/portable-replay.json`及`candidate/evals/workflow-entry/replay_converters.py`：后者用标准库`tempfile.TemporaryDirectory`复制打包材料、a/b转换脚本和各自边界检查脚本，再经`subprocess.run`捕获命令、退出码和stdout/stderr。新记录中两版正常转换均退出0、重复输入均退出2；a的`check_conversion.py`退出0、stderr为空，stdout为19项通过、0项失败；b的`check_unitrows.py`退出0、stderr为空，stdout为22项通过、0项失败，并列出相应边界通过。这为打包的两版完整自设边界检查提供了执行代理之外的运行证据，补足了初次记录只覆盖共同正常/重复输入的限制。计数口径不同，不把19与22作为优劣或进步证据。

复核者仍未亲自执行，仅审阅上述两份后续来源。新增记录未包含所复制代码的哈希，未独立确认打包副本与初次提交的字节身份；功能复跑也不能证明原代理实际读取说明、原运行完整副作用或输入全程保留，不能推断科学正确性。它只覆盖自设检查脚本定义的边界，未覆盖超大文件或异常写出原子性。**14条既定判定保持不变**；这段后续证据没有回填为初次复核时已知。
