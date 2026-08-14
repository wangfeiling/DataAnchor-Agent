---
name: data-agent-step3-plan-hive-layering
description: 执行 Hive Data Agent Spec Step 3，读取 Step 2 已验证的 Hive 表字段来源，查询这些来源表的真实 ODS、DWD、DIM、DWS 或 ADS 层级及上游血缘，并依据当前建表、改表和分层规范决定目标字段与模型落层、迭代现有表还是新建表、哪些上游需要同步扩字段。输出层级核验、目标表决策、逐跳扩字段和影响范围；不修改 Step 2 字段来源或指标口径。
---

# Step 3: 数仓分层与表变更设计

## 启动前

1. 完整读取 [../../references/evidence-policy.md](../../references/evidence-policy.md)。
2. 完整读取 [../../references/hive-warehouse-rules.md](../../references/hive-warehouse-rules.md)。
3. 完整读取 [../../references/workflow-contracts.md](../../references/workflow-contracts.md) 的 `SPEC_STEP_3` 契约。
4. 读取 [references/method.md](references/method.md)，并使用 [../../template/step3-layering-and-change-template.md](../../template/step3-layering-and-change-template.md)。

## 输入门槛

读取实际采用的 Step 1 与 Step 2 handoff。Step 2 为 `BLOCKED` 或核心来源未决时停止。继承 Step 2 字段来源、指标口径和冲突，不在本阶段替换。

## 执行流程

1. 对 Step 2 的每张 Hive 来源表查询环境、全限定名、真实层级、粒度、分区、TTL、owner 和最近可用分区。
2. 读取当前版本的 ODS/DWD/DIM/DWS/ADS 建表、改表与命名规范，记录版本和适用范围。
3. 查询来源字段的表级与字段级上游血缘，识别语义最初产生位置和当前丢失环节。
4. 根据业务粒度、语义责任、复用范围、生命周期、SLA 和消费者选择目标层。
5. 召回可能承载需求的现有 Hive 表，对“迭代现有表”和“新建表”执行同一决策矩阵。
6. 逐字段判断是否需要上游同步扩展；沿真实血缘列出每一跳、owner、变更、回填、发布顺序和验证项。
7. 评估直接/关键间接消费者、任务、权限、质量规则、历史分区、成本和兼容性。
8. 输出 `step3-layering-and-table-change.md` 与 `step3-handoff.json`。

## 决策纪律

- 不凭表名前缀确认层级；层级必须有元数据或规范登记 evidence。
- ODS 保留源语义，DWD 承载规范原子事实，DIM 承载一致性维度，DWS 承载公共汇总，ADS 承载场景服务。
- 可复用原子事实不应只新增在 ADS；场景专属规则不应无理由上移到 DWS。
- 改表必须证明主题、粒度、时间、生命周期、owner 和兼容性一致。
- 上游扩字段由实际缺口与血缘决定，不因“以后可能有用”扩散。
- 来源不可实现时退回 Step 2，不在 Step 3 换字段或重定义指标。

## 门禁

`PASS` 要求所有来源表层级已核验、目标层明确、改表/建表结论有依据、上游扩字段逐跳可执行。关键分层规范、层级、血缘、owner 或兼容性未知且会改变决策时 `BLOCKED`；只剩上线前配置项时可 `CONDITIONAL`。
