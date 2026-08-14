---
name: data-agent-step2-map-hive-sources
description: 执行 Hive Data Agent Spec Step 2，以 Step 1 增强需求为输入，在业务与数据知识库中查找所需维度、指标、标识、时间、状态和属性，核验可复用指标及其版本、适用域、聚合与过滤口径，并映射到可验证的 Hive 表和字段来源。输出字段来源、表来源、指标复用方式和口径说明；不决定目标 ODS/DWD/DIM/DWS/ADS 落层，也不决定改表或新建表。
---

# Step 2: 字段来源与指标口径

## 启动前

1. 完整读取 [../../references/evidence-policy.md](../../references/evidence-policy.md)。
2. 完整读取 [../../references/knowledge-base-boundaries.md](../../references/knowledge-base-boundaries.md) 的 Step 2 检索规则。
3. 完整读取 [../../references/workflow-contracts.md](../../references/workflow-contracts.md) 的 `SPEC_STEP_2` 契约。
4. 读取 [references/method.md](references/method.md)，并使用 [../../template/step2-source-and-definition-template.md](../../template/step2-source-and-definition-template.md)。

## 输入门槛

读取实际使用的 `step1-handoff.json` 并引用 artifact ID。Step 1 为 `BLOCKED` 时停止；`knowledge_retrieval_performed` 不为 false 时退回 Step 1 修订。不得绕过增强需求直接从原始文档猜字段。

## 执行流程

1. 把每个 requirement 的所需数据项分类为维度、指标、标识、时间、状态、属性或规则。
2. 为每个数据项生成带业务域、主体、粒度、时间和同义词的知识库检索请求。
3. 先查规范业务定义，再查 Hive 表/字段物理实现；保存查询、版本、命中和未命中。
4. 对指标判断直接复用、带过滤复用、派生复用或无可复用指标，并核验适用域、粒度、窗口、维度限制、去重、分子/分母和版本。
5. 对维度核验规范维度、属性来源、业务键/代理键、历史变化、枚举和未知值策略。
6. 对每个字段记录 `database.table.column`、类型、含义、单位、时间、空值、枚举、过滤/转换和 evidence。
7. 对来源表记录用途和业务粒度，必要时确定 driving source 与辅表，但不查询或裁决目标层级。
8. 保留用户候选、选表函数和热度信号；它们只能召回或排序，不能单独证明口径。
9. 输出 `step2-field-source-and-definition.md` 与 `step2-handoff.json`。

## 边界

- 不根据表名前缀断言 ODS/DWD/DIM/DWS/ADS 层级。
- 不决定目标字段落层、迭代哪张目标表或新建目标表。
- 不把字段名相似、非空率、热度或历史使用次数当成语义证据。
- 知识库定义和 Hive 实现冲突时同时保留并标记 `CONFLICTED`。
- 找不到来源时输出 `MISSING` 与最短补证据动作，不创造字段。

## 门禁

`PASS` 要求所有核心需求项都有已验证来源或明确、可接受的派生关系，指标复用口径完整，冲突已裁决。核心维度/指标找不到来源、同名口径无法裁决或关键字段只凭推断时 `BLOCKED`；非核心展示项缺失可 `CONDITIONAL`。
