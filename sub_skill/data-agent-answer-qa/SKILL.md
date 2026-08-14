---
name: data-agent-answer-qa
description: 以可追溯证据回答 Hive 数据仓库单一或组合式 QA，包括指标定义和口径、查找 Hive 表、字段含义与枚举、ODS/DWD/DIM/DWS/ADS 层级、分区与 TTL、表级和字段级血缘。用于不需要建设或改造数据产物的事实查询；若问题要求新增字段、任务、表或技术方案，则输出事实 handoff 并升级到 Spec。
---

# QA: Hive 数据问答

## 启动前

1. 完整读取 [../../references/evidence-policy.md](../../references/evidence-policy.md)。
2. 完整读取 [../../references/knowledge-base-boundaries.md](../../references/knowledge-base-boundaries.md) 的 Step 2 检索规则作为 QA 检索规范。
3. 读取 [references/method.md](references/method.md)，并使用 [../../template/qa-answer-template.md](../../template/qa-answer-template.md)。

## 流程

1. 分类为指标、表、字段、层级、分区/TTL、血缘或混合问题。
2. 解析环境、database、table、column、指标版本、业务域和时间点。
3. 为待回答事实建立 claim，选择指标知识库、Hive catalog、血缘或只读查询等直接来源。
4. 登记 evidence 的版本、定位、观测时间和限制；对冲突检查环境、版本和适用域。
5. 直接给结论、适用范围、证据、限制与必要后续动作。
6. 输出 `qa-answer.md` 与 `qa-handoff.json`。

## 边界

- 热度高不等于口径正确；表名前缀不等于层级已核验。
- 不执行修改数据的 SQL；验证默认只读且必须限制分区和扫描。
- 无法可靠识别对象时保持候选，不猜测 database/table/column。
- 需要改表、建表、扩字段、加工或完整方案时设置 `escalate_to_spec.required = true`。
