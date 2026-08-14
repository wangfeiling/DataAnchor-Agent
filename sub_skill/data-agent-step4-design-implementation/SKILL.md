---
name: data-agent-step4-design-implementation
description: 执行 Hive Data Agent Spec Step 4，将 Step 1–3 已确认的业务需求、Hive 字段与指标来源、ODS/DWD/DIM/DWS/ADS 落层和改表/建表决策细化为可直接开发的实现设计，包括目标 Hive schema、字段转换、Join、分区与增量、调度依赖、回填、数据质量、测试、性能、安全、发布和回滚。不重新检索或替换来源，不修改指标口径和层级决策。
---

# Step 4: Hive 开发实现设计

## 启动前

1. 完整读取 [../../references/evidence-policy.md](../../references/evidence-policy.md)。
2. 完整读取 [../../references/hive-warehouse-rules.md](../../references/hive-warehouse-rules.md)。
3. 完整读取 [../../references/workflow-contracts.md](../../references/workflow-contracts.md) 的 `SPEC_STEP_4` 契约。
4. 读取 [references/method.md](references/method.md)，并使用 [../../template/step4-implementation-design-template.md](../../template/step4-implementation-design-template.md)。

## 输入门槛

读取实际采用的 Step 1、Step 2 和 Step 3 handoff，并引用全部 artifact ID。Step 3 为 `BLOCKED` 时停止；上游为 `CONDITIONAL` 时继承条件。目标层、改表/建表和上游扩字段若不明确，退回 Step 3。

## 执行流程

1. 固定 Step 2 字段来源与指标口径、Step 3 目标层与表变更决策。
2. 定义目标 Hive 表一行业务含义、唯一性、字段顺序、类型、注释、分区、TTL 和 owner。
3. 对每个目标字段建立来源与转换：直接映射、标准化、枚举、派生、聚合、空值和默认值。
4. 设计 Join：键、基数、时间点、SCD、过滤、去重和 fanout 防护。
5. 设计分区与增量：业务时间/处理时间、水位、迟到、撤销、幂等、重跑和失败恢复。
6. 定义任务依赖、运行频率、SLA、资源和分区 ready 条件。
7. 定义历史回填、批次、断点续跑、新旧逻辑对账和消费者迁移。
8. 定义 schema、唯一性、完整性、枚举、范围、引用完整性、指标对账和新鲜度检查。
9. 定义单元/集成/回归/业务验收、发布顺序、观察期和 schema/data 双回滚。
10. 输出 `step4-hive-implementation-design.md` 与 `step4-handoff.json`。

## 边界

- 不新增 Step 2 没有的核心来源字段、表或指标口径。
- 不改变 Step 3 的层级、目标表类型或上游扩展范围。
- 发现不可实现时退回最早相关阶段，不在实现设计中暗改需求。
- 不用 `DISTINCT`、默认 0 或当前维度值掩盖基数、空值或历史问题。
- 物理优化参数必须有 Hive 引擎、数据量或访问模式依据；未知时标记待压测。
- 伪 SQL 只说明逻辑，不能声称已执行或已验证。

## 门禁

`PASS` 要求目标 schema、转换、Join、分区增量、调度、回填、质量、测试、发布和回滚均可执行。任何目标字段无来源/规则、Join 基数未知且影响正确性、增量不幂等或上游依赖不可满足时 `BLOCKED`。
