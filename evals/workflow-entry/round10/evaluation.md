# Round 10：选题 V2 与总控交接顺序

## 问题与完成条件

`main@5af337b3d8cdf530aa382ad9cf0f33de03cc046e` 将 `research-topic-selection` 重构为 V2：G1 可按需联动文献/批判性阅读，G2/G4 可在选题裁决前联动方法学，只有 G5 通过才考虑写稿。PR 在合入该版本后，总控仍写成“通过关口后再转方法学或投稿模块”，来源快照也仍指向旧 `main@b92b444`。这会把 G2/G4 所需的方法学核验放到裁决之后，并把写稿边界压缩成不区分 G5 的笼统后续。

本轮只做接口一致性修复，不增加医学规则、统计阈值或领域裁决。完成条件预先写入 `run-plan.json`：

1. 合入 V2 后，总控明确 G1、G2/G4 的裁决前联动与 G5 后写稿；
2. 已立项的局部统计任务不被重新拉回选题；
3. 来源快照记录实际 main commit；
4. 两版同条件前向测试无授权或范围回退；若两版行为都通过，不宣称行为成功率提高。

## 版本与最小改动

- 行为基线：`76ada51d9b2bee7841436e784d01ba8d16616722`，即 PR 分支合入 V2、尚未修总控的状态；其 tree 与实际运行的本地快照 `cae9aea` 一致。
- 候选运行版：`7e85396cae37218037250050b6b04399be7c2d50`；其 tree 与实际运行的本地快照 `ab078f8` 一致。
- 仅修改根 `SKILL.md` 的一行选题交接和 `references/workflow-sources.md` 的一段版本记录；V2 专业规则与其他模块未改。
- 个人已安装技能未同步；本修改继续留在 draft PR。

## 验证设计

四个公开合成任务只提供原始请求，分别覆盖：公开数据批量选题、AUC 差异冒充机制、试点后缺 G5 证据却要求写稿、已立项项目只做集群随机样本量。每版由一个 fresh 执行者运行一次；执行者未看到 `rubric.json`，未联网、未安装依赖、未写仓库、未接触真实研究材料。

两名 fresh 评审仅看到匿名 `version-x.md`、`version-y.md` 和冻结量表，不知道版本身份；R10 静态项对两份行为输出都必须判 `INSUFFICIENT_EVIDENCE`，另由父级脚本检查源码。

## 结果

### 行为前向测试

两名独立评审一致：

| 版本 | R01–R09 MET | NOT_MET | R10 |
| --- | ---: | ---: | --- |
| 基线 / Version X | 9/9 | 0 | `INSUFFICIENT_EVIDENCE` |
| 候选 / Version Y | 9/9 | 0 | `INSUFFICIENT_EVIDENCE` |

两版都把方法学核验放在实际 GO 前，并在 G5 缺证据时阻止写稿，说明执行者可从专业模块纠正旧总控文本。本批次没有观察到候选相对基线的通过率提升。两版在 T2 的裁决强度不同：基线对原机制命题先 HOLD、候选直接 STOP 并允许另立更窄预测候选；量表只验证没有把内部 AUC 差异当作机制证据，不能判定哪一科学裁决更正确。

### 静态一致性

同一脚本 `verify_round10.py` 在两个版本上运行：

- 基线：退出码 1；11 项中 6 项为 false，包括 G1/G2/G4 前置联动、G5 后写稿、移除旧顺序、main commit 与 V2 交接快照。
- 候选：退出码 0；11/11 true，模块数为 11，所有相对链接存在。

V2 自带回归另外实际运行：

```text
python3 -m unittest discover -s research-topic-selection/tests -v
Ran 10 tests ... OK

python3 research-topic-selection/scripts/validate_gate_ledger.py \
  research-topic-selection/assets/gate-ledger-example.csv
PASS 18 gate rows / 3 topics
```

根入口与十一份专业入口均通过当前 skill-creator `quick_validate.py`；相对链接检查为 12 个入口、0 缺失。

## 证据定位

- 原始请求：`cases.json`
- 冻结量表：`rubric.json`
- 运行条件：`run-plan.json`
- 原始输出：`runs/baseline/outputs.md`、`runs/candidate/outputs.md`
- 匿名副本与两名评审：`grading/`
- 静态脚本与结果：`verify_round10.py`、`static-baseline-verification.json`、`static-verification.json`

原始输出 SHA-256：

- baseline：`ba433135c79f87381eb6891f4315de1aaf544d2e5ea3f57cd654bca602abb74c`
- candidate：`604baca9cd6fcd84dc7b917e365f1eec5ef91ccf30406cfa2bfe9abe3d117857`

独立评审 SHA-256：

- reviewer 1：`ed87e89f84d6c22b534b0fc399ef14fda4014b90d722f1378291e6b197922243`
- reviewer 2：`357b12e31c2e4968d6c16283c3ef5b4b10bca90e469c61fa42b5f8be04a18dcb`

## 测量边界与停止决定

每个版本只有一个四任务批次；没有可用的精确模型部署、token、费用、完整工具事件流或可比耗时。执行者没有实际检索文献、访问数据、计算样本量或运行试点；独立评审只验证路由、授权和停止行为，不认证科学正确性。

因此本轮结论限于：静态跨模块合同从不一致变为一致，且在当前合成任务中未观察到行为回退。不能宣称一般可靠性、科学正确性、效率或成本改善。按预设停止规则，不再为同一问题增加提示词；下一轮应选择新的实际失败或可核查变更。
