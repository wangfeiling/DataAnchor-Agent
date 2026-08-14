---
name: data-agent-step5-compose-spec
description: 执行 Hive Data Agent Spec Step 5，将 Step 1 增强需求、Step 2 Hive 字段来源与指标口径、Step 3 ODS/DWD/DIM/DWS/ADS 分层及表变更决策、Step 4 开发实现设计组装成完整技术方案，执行版本链、需求追踪和跨阶段一致性检查。用于生成最终 technical-spec.md；只组装已确认内容，不新增或修改字段来源、指标口径、层级、目标表和实现决策。
---

# Step 5: 最终技术方案组装

## 启动前

1. 完整读取 [../../references/evidence-policy.md](../../references/evidence-policy.md)。
2. 完整读取 [../../references/workflow-contracts.md](../../references/workflow-contracts.md) 的 `SPEC_STEP_5` 契约。
3. 读取 [references/method.md](references/method.md)。
4. 使用 [../../template/step5-assembly-report-template.md](../../template/step5-assembly-report-template.md) 和 [../../template/final-technical-spec-template.md](../../template/final-technical-spec-template.md)。

## 输入门槛

读取实际采用的 Step 1–4 handoff，检查同一 `request_id`、版本链、`input_artifact_ids` 与上游状态。任一核心阶段 `BLOCKED` 时停止，并返回产生问题的最早阶段。上游 `CONDITIONAL` 必须保留到最终方案。

## 执行流程

1. 锁定 Step 1–4 artifact 版本，索引 requirement、mapping、metric、decision、field、transform 和 test ID。
2. 建立 requirement → Step 2 字段/指标来源 → Step 3 层级/表变更 → Step 4 实现/测试的追踪矩阵。
3. 检查业务粒度、时间语义、指标口径、字段来源、层级、目标表、schema、分区、调度、TTL 和 owner 是否跨阶段一致。
4. 按最终技术方案模板组装文档，区分已确认、条件性结论、未知和冲突。
5. 将所有 open item 汇总为 owner、解阻动作、截止点和阻塞阶段。
6. 输出 `technical-spec.md`、`step5-assembly-report.md` 与 `step5-handoff.json`。
7. 运行总编排的五阶段链路校验；发现冲突时修订来源阶段后重新组装。

## 组装纪律

- 不新增或替换 Hive 表、字段、指标、Join、目标层、目标表、分区或调度决策。
- 不把不同环境、版本或同名对象自动归并。
- 不把 `INFERRED`、`UNKNOWN`、`CONFLICTED` 改写成确定陈述。
- 不声称 SQL、回填、对账、性能或业务验收已经通过，除非有执行 evidence。
- 文档写得完整不等于事实完整；缺失必需信息时保留章节并标记状态。

## 门禁

`PASS` 要求 Step 1–4 核心状态均为 `PASS`、追踪完整、无语义漂移且方案可直接指导开发。只有不改变设计的上线配置待定时可 `CONDITIONAL`。任何 requirement 缺来源、实现或测试，或跨阶段决策冲突时 `BLOCKED`。
