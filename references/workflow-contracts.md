# 工作流交付契约

## 目录

1. 通用 handoff
2. Step 1–5 payload
3. QA 与 Debug SQL
4. 版本与追踪

## 1. 通用 handoff

每步同时输出 Markdown 和 JSON：Markdown 供评审，JSON 供下游与自动校验。通用结构：

```json
{
  "contract_version": "2.0",
  "artifact_id": "REQ-001-step1-v1",
  "request_id": "REQ-001",
  "mode": "SPEC",
  "stage": "SPEC_STEP_1",
  "status": "PASS",
  "created_at": "2026-08-14T10:00:00+08:00",
  "input_artifact_ids": [],
  "supersedes_artifact_id": null,
  "claims": [],
  "evidence": [],
  "decisions": [],
  "open_items": [],
  "payload": {}
}
```

Claim 至少包含 `claim_id`、`statement`、`status`、`evidence_ids`、`origin_artifact_id`、`based_on_claim_ids`、`rationale`。Decision 包含 `decision_id`、`statement`、`basis_claim_ids`、`alternatives_considered`、`reason`。Open item 包含 `item_id`、`question_or_action`、`severity`、`owner`、`due_before`。

## 2. Step 1–5 payload

### SPEC_STEP_1

- `input_snapshot`；
- `enhanced_requirements`；
- `requirement_atoms`；
- `business_terms`；
- `ambiguities`；
- `acceptance_criteria`；
- `non_functional_requirements`；
- `knowledge_retrieval_performed`：必须为 false。

禁止物理映射、知识库命中和层级判断。

### SPEC_STEP_2

- `requirement_items`：维度/指标/标识/时间/状态/属性/规则分类；
- `knowledge_searches`；
- `metric_reuse`；
- `field_sources`；
- `table_sources`；
- `definition_notes`；
- `unresolved_mappings`。

### SPEC_STEP_3

- `source_layer_lookup`；
- `layering_rules_version`；
- `placement_decision`；
- `table_change_decision`；
- `upstream_extensions`；
- `impact_scope`；
- `dependency_order`。

### SPEC_STEP_4

- `target_schema`；
- `transformations`；
- `join_logic`；
- `partition_and_incremental`；
- `scheduling`；
- `backfill`；
- `data_quality`；
- `tests`；
- `release_and_rollback`。

### SPEC_STEP_5

- `input_versions`；
- `consistency_checks`；
- `requirements_traceability`；
- `final_spec_path`；
- `confirmed_vs_pending`。

## 3. QA 与 Debug SQL

QA payload：`question_type`、`answer_summary`、`answer_items`、`recommended_followups`、`escalate_to_spec`。

Debug SQL payload：`dialect`、`engine_version`、`parameters`、`checks`、`safety`、`execution_status`。默认 `execution_status = NOT_RUN`。

## 4. 版本与追踪

- 全流程使用同一 `request_id`；artifact ID 包含阶段和递增版本。
- 下游 `input_artifact_ids` 指向实际读取版本；修订设置 `supersedes_artifact_id`。
- Step 2 映射引用 Step 1 requirement ID；Step 3 决策引用 Step 2 source/mapping ID；Step 4 实现引用 Step 3 decision ID；Step 5 追踪全部 ID。
- 下游 claim 引用 `origin_artifact_id` 或拥有本阶段直接 evidence。
