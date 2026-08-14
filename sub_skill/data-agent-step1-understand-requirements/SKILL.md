---
name: data-agent-step1-understand-requirements
description: 执行 Hive Data Agent Spec Step 1，只基于原始业务需求文档和用户自然语言补充进行加深理解、保真拆分、歧义识别和验收整理，输出增强需求文档与结构化 handoff。用于提取业务目标、主体、事件、业务粒度、时间语义、范围、规则、优先级、非功能要求和验收条件；本阶段严禁检索知识库、Hive 表字段、指标字典、表索引、血缘或数据样本，也不提前拆物理字段。
---

# Step 1: 需求理解与拆分

## 启动前

1. 完整读取 [../../references/evidence-policy.md](../../references/evidence-policy.md)。
2. 完整读取 [../../references/knowledge-base-boundaries.md](../../references/knowledge-base-boundaries.md) 的 Step 1 禁止检索规则。
3. 完整读取 [../../references/workflow-contracts.md](../../references/workflow-contracts.md) 的 `SPEC_STEP_1` 契约。
4. 读取 [references/method.md](references/method.md)，并使用 [../../template/step1-enhanced-requirement-template.md](../../template/step1-enhanced-requirement-template.md)。

## 允许输入

- 用户提供的原始需求文档及版本/定位；
- 当前对话中用户的自然语言补充与明确确认；
- 用户提供的业务示例，仅作为需求语境。

不得读取已有 QA 的知识库事实、历史技术方案、指标库、Hive 元数据或任何检索结果。若总编排携带这些内容，本阶段忽略它们并在 handoff 中声明隔离。

## 执行流程

1. 保存输入快照，按章节、段落、页码或消息轮次建立 source requirement ID。
2. 保留业务方原始术语、别名、示例和上下文，不用技术术语替换原词。
3. 先形成对需求的加深理解：业务目标、使用者、业务过程、预期产物和成功标准。
4. 将复合需求拆成最小可独立验收的 requirement atoms，而不是字段清单。
5. 为每个 atom 提取主体、业务事件/状态、业务粒度、时间语义、范围、规则、输出、优先级、依赖和验收。
6. 识别冲突、隐含假设与多种解释；说明每种解释会影响哪个后续决策。
7. 提取 SLA、时效、历史范围、回填、权限、合规、成本和可观测性要求。
8. 输出 `step1-enhanced-requirement.md` 与 `step1-handoff.json`。

## 严禁事项

- 不检索或调用任何知识库、catalog、Hive、血缘、热度、选表或 SQL 能力。
- 不验证需求中疑似表名/字段名，只按原文保存。
- 不创建 `database.table.column` 映射、指标库命中、来源表候选或 ODS–ADS 层级判断。
- 不把业务展示项机械拆成猜测字段。
- 不因已有实现方便而改写业务目标。

## 门禁

`PASS` 必须满足需求项可追溯、业务粒度与时间语义足够清晰、关键验收可检查，并且 `knowledge_retrieval_performed = false`。会导致 Step 2 搜索不同业务对象的歧义必须 `BLOCKED`；只影响非核心展示的歧义可 `CONDITIONAL`。
