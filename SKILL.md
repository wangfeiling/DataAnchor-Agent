---
name: data-agent-orchestrate
description: 编排基于 Hive 数据仓库的语义数据开发 Data Agent，将用户请求分流为 QA 或 Spec。QA 回答指标、Hive 表、字段和血缘事实；Spec 严格执行 Step 1 需求理解与拆分、Step 2 知识库字段来源和指标复用、Step 3 ODS/DWD/DIM/DWS/ADS 落层及改表/建表与上游扩字段、Step 4 Hive 开发实现设计、Step 5 最终技术方案组装。用于把需求文档和自然语言补充转换为有证据、可追溯、可直接指导开发的技术方案。
---

# Hive Data Agent 总编排

## 启动前

1. 完整读取 [references/workflow-contracts.md](references/workflow-contracts.md) 与 [references/evidence-policy.md](references/evidence-policy.md)。
2. 需要路由或判断阶段是否可继续时，读取 [references/routing-and-gates.md](references/routing-and-gates.md)。
3. 执行 Spec Step 2 前读取 [references/knowledge-base-boundaries.md](references/knowledge-base-boundaries.md)。
4. 执行 Spec Step 3–4 前读取 [references/hive-warehouse-rules.md](references/hive-warehouse-rules.md)。
5. 为请求建立稳定 `request_id`，保留原始文档、补充消息和每次 artifact 版本。

## 核心边界

- 所有物理数据源均为 Hive 数据仓库表；对象使用 `database.table` 和字段名定位。
- 数仓分层固定为 ODS、DWD、DIM、DWS、ADS；具体决策必须依据组织规范和真实元数据。
- Step 1 严禁检索知识库、Hive catalog、表索引、字段索引、指标字典、热度、血缘或执行 SQL。
- Step 2 才能在知识库中查找维度、指标、字段和 Hive 表，并输出来源与口径；不得决定目标落层或改表/建表。
- Step 3 才能查询 Step 2 来源表的当前层级和血缘，并决定落层、迭代现有表或新建表、上游扩字段。
- Step 4 只把 Step 1–3 的已确认结果细化为可开发实现，不重选来源、不改落层。
- Step 5 只组装、追踪和一致性检查，不新增任何业务口径或架构决策。
- 任何阶段都不得把候选、热度、名称相似或推断伪装成事实。

## 模式路由

### QA

若用户只想查一个或一组现有事实，读取并执行 [sub_skill/data-agent-answer-qa/SKILL.md](sub_skill/data-agent-answer-qa/SKILL.md)。输出 `qa-answer.md` 和 `qa-handoff.json`。若问题实际要求建设或改造 Hive 产物，保留 QA 证据并切换 Spec。

### Spec

严格按顺序执行并使用 `template/` 对应模板：

1. 读取 [sub_skill/data-agent-step1-understand-requirements/SKILL.md](sub_skill/data-agent-step1-understand-requirements/SKILL.md)，输出增强需求与 `step1-handoff.json`。
2. Step 1 过门后读取 [sub_skill/data-agent-step2-map-hive-sources/SKILL.md](sub_skill/data-agent-step2-map-hive-sources/SKILL.md)，输出字段来源、表来源、指标复用与口径说明。
3. Step 2 过门后读取 [sub_skill/data-agent-step3-plan-hive-layering/SKILL.md](sub_skill/data-agent-step3-plan-hive-layering/SKILL.md)，输出来源表层级、目标落层、改表/建表和上游扩字段方案。
4. Step 3 过门后读取 [sub_skill/data-agent-step4-design-implementation/SKILL.md](sub_skill/data-agent-step4-design-implementation/SKILL.md)，输出 Hive 目标 schema、加工、调度、回填、质量、测试和发布设计。
5. Step 4 过门后读取 [sub_skill/data-agent-step5-compose-spec/SKILL.md](sub_skill/data-agent-step5-compose-spec/SKILL.md)，组装 `technical-spec.md`。
6. 仅在需要验证假设或排障时读取 [sub_skill/data-agent-debug-sql/SKILL.md](sub_skill/data-agent-debug-sql/SKILL.md)。该子技能不占用 Step 编号。

## 阶段控制

- `PASS`：核心输出完整且有适合事实类型的证据。
- `CONDITIONAL`：未决项不改变当前核心决策，但必须带到下游。
- `BLOCKED`：缺失或冲突会改变核心决策；停止依赖该结论的后续步骤。
- Step 2 发现业务语义不清时返回 Step 1；Step 3 发现来源不足时返回 Step 2；Step 4 发现模型不可实现时返回 Step 3；Step 5 发现冲突时返回产生冲突的最早阶段。
- 新证据推翻旧结论时创建新版本并设置 `supersedes_artifact_id`，不得覆盖历史。

## 自动校验

每阶段运行：

```text
python scripts/validate_handoff.py step1-handoff.json
```

最终组装后运行：

```text
python scripts/validate_handoff.py --chain step1-handoff.json step2-handoff.json step3-handoff.json step4-handoff.json step5-handoff.json
```

无法执行脚本时，按 [references/workflow-contracts.md](references/workflow-contracts.md) 人工核验并明确标记“未执行自动校验”。

## 最终交付

交付人类可读产物、JSON handoff、使用的 artifact 版本、总体状态、已验证事实、条件与阻塞项。最终技术方案必须采用 [template/final-technical-spec-template.md](template/final-technical-spec-template.md)，并建立 requirement → 字段/指标来源 → 层级/表变更 → 实现 → 测试的追踪关系。
