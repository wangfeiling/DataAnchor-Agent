#!/usr/bin/env python3
"""Validate Hive Data Agent handoff artifacts with the Python standard library."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


COMMON_KEYS = {
    "contract_version", "artifact_id", "request_id", "mode", "stage", "status",
    "created_at", "input_artifact_ids", "supersedes_artifact_id", "claims",
    "evidence", "decisions", "open_items", "payload",
}

STAGE_KEYS = {
    "QA": {"question_type", "answer_summary", "answer_items", "recommended_followups", "escalate_to_spec"},
    "SPEC_STEP_1": {
        "input_snapshot", "enhanced_requirements", "requirement_atoms", "business_terms",
        "ambiguities", "acceptance_criteria", "non_functional_requirements",
        "knowledge_retrieval_performed",
    },
    "SPEC_STEP_2": {
        "requirement_items", "knowledge_searches", "metric_reuse", "field_sources",
        "table_sources", "definition_notes", "unresolved_mappings",
    },
    "SPEC_STEP_3": {
        "source_layer_lookup", "layering_rules_version", "placement_decision",
        "table_change_decision", "upstream_extensions", "impact_scope", "dependency_order",
    },
    "SPEC_STEP_4": {
        "target_schema", "transformations", "join_logic", "partition_and_incremental",
        "scheduling", "backfill", "data_quality", "tests", "release_and_rollback",
    },
    "SPEC_STEP_5": {
        "input_versions", "consistency_checks", "requirements_traceability",
        "final_spec_path", "confirmed_vs_pending",
    },
    "DEBUG_SQL": {"dialect", "engine_version", "parameters", "checks", "safety", "execution_status"},
}

SPEC_ORDER = {
    "SPEC_STEP_1": 1,
    "SPEC_STEP_2": 2,
    "SPEC_STEP_3": 3,
    "SPEC_STEP_4": 4,
    "SPEC_STEP_5": 5,
}

CLAIM_STATUSES = {"VERIFIED", "USER_CONFIRMED", "USER_STATED", "INFERRED", "UNKNOWN", "CONFLICTED"}
GATE_STATUSES = {"PASS", "CONDITIONAL", "BLOCKED"}
SEVERITIES = {"blocking", "non_blocking"}
STEP1_ALLOWED_EVIDENCE = {"requirement_doc", "user_message", "user_confirmation", "user_attachment"}
STEP1_BANNED_KEYS = {
    "database", "table", "table_name", "source_table", "target_table", "field", "field_name",
    "source_field", "physical_field", "column", "column_name", "metric_id", "knowledge_searches",
    "target_layer", "layer", "placement_decision", "table_change_decision", "lineage",
}
STEP2_BANNED_KEYS = {"target_layer", "placement_decision", "table_change_decision", "upstream_extensions"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: cannot read valid UTF-8 JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return data


def duplicate_values(items: Any, key: str) -> set[str]:
    if not isinstance(items, list):
        return set()
    values = [item.get(key) for item in items if isinstance(item, dict) and item.get(key)]
    return {value for value in values if values.count(value) > 1}


def find_keys(value: Any, banned: set[str], path: str = "payload") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key.lower() in banned:
                found.append(child_path)
            found.extend(find_keys(child, banned, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(find_keys(child, banned, f"{path}[{index}]"))
    return found


def validate_artifact(data: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    missing = sorted(COMMON_KEYS - data.keys())
    if missing:
        errors.append(f"{label}: missing common keys: {', '.join(missing)}")

    if data.get("contract_version") != "2.0":
        errors.append(f"{label}: contract_version must be '2.0'")

    stage = data.get("stage")
    if stage not in STAGE_KEYS:
        errors.append(f"{label}: unsupported stage {stage!r}")

    payload = data.get("payload")
    if not isinstance(payload, dict):
        errors.append(f"{label}: payload must be an object")
    elif stage in STAGE_KEYS:
        payload_missing = sorted(STAGE_KEYS[stage] - payload.keys())
        if payload_missing:
            errors.append(f"{label}: payload missing keys for {stage}: {', '.join(payload_missing)}")

    gate = data.get("status")
    if gate not in GATE_STATUSES:
        errors.append(f"{label}: invalid status {gate!r}")

    mode = data.get("mode")
    if stage == "QA" and mode != "QA":
        errors.append(f"{label}: QA stage must use QA mode")
    if stage != "QA" and mode != "SPEC":
        errors.append(f"{label}: non-QA stage must use SPEC mode")

    for key in ("input_artifact_ids", "claims", "evidence", "decisions", "open_items"):
        if not isinstance(data.get(key), list):
            errors.append(f"{label}: {key} must be a list")

    for collection, id_key in (
        ("claims", "claim_id"), ("evidence", "evidence_id"),
        ("decisions", "decision_id"), ("open_items", "item_id"),
    ):
        duplicates = duplicate_values(data.get(collection), id_key)
        if duplicates:
            errors.append(f"{label}: duplicate {id_key}: {', '.join(sorted(duplicates))}")

    claims = data.get("claims") if isinstance(data.get("claims"), list) else []
    evidence = data.get("evidence") if isinstance(data.get("evidence"), list) else []
    decisions = data.get("decisions") if isinstance(data.get("decisions"), list) else []
    claim_ids = {item.get("claim_id") for item in claims if isinstance(item, dict)}
    evidence_ids = {item.get("evidence_id") for item in evidence if isinstance(item, dict)}

    for claim in claims:
        if not isinstance(claim, dict):
            errors.append(f"{label}: every claim must be an object")
            continue
        claim_id = claim.get("claim_id", "<missing>")
        status = claim.get("status")
        if status not in CLAIM_STATUSES:
            errors.append(f"{label}: claim {claim_id} has invalid status {status!r}")
        refs = claim.get("evidence_ids", [])
        if not isinstance(refs, list):
            errors.append(f"{label}: claim {claim_id} evidence_ids must be a list")
            refs = []
        unknown = set(refs) - evidence_ids
        if unknown:
            errors.append(f"{label}: claim {claim_id} references unknown evidence {sorted(unknown)}")
        if status in {"VERIFIED", "USER_CONFIRMED"} and not refs and not claim.get("origin_artifact_id"):
            errors.append(f"{label}: claim {claim_id} status {status} requires evidence or origin_artifact_id")
        if status == "INFERRED" and not claim.get("rationale"):
            errors.append(f"{label}: inferred claim {claim_id} requires rationale")

    evidence_required = {
        "evidence_id", "source_type", "locator", "observed_at", "supports",
        "summary", "freshness", "directness",
    }
    for item in evidence:
        if not isinstance(item, dict):
            errors.append(f"{label}: every evidence item must be an object")
            continue
        evidence_id = item.get("evidence_id", "<missing>")
        absent = sorted(evidence_required - item.keys())
        if absent:
            errors.append(f"{label}: evidence {evidence_id} missing: {', '.join(absent)}")
        supports = item.get("supports", [])
        if not isinstance(supports, list):
            errors.append(f"{label}: evidence {evidence_id} supports must be a list")
        else:
            unknown = set(supports) - claim_ids
            if unknown:
                errors.append(f"{label}: evidence {evidence_id} supports unknown claims {sorted(unknown)}")

    for decision in decisions:
        if not isinstance(decision, dict):
            errors.append(f"{label}: every decision must be an object")
            continue
        basis = decision.get("basis_claim_ids", [])
        if not isinstance(basis, list):
            errors.append(f"{label}: decision {decision.get('decision_id')} basis_claim_ids must be a list")
        elif set(basis) - claim_ids:
            errors.append(f"{label}: decision {decision.get('decision_id')} references unknown claims")

    open_items = data.get("open_items") if isinstance(data.get("open_items"), list) else []
    blocking = 0
    for item in open_items:
        if not isinstance(item, dict):
            errors.append(f"{label}: every open item must be an object")
            continue
        severity = item.get("severity")
        if severity not in SEVERITIES:
            errors.append(f"{label}: open item {item.get('item_id')} has invalid severity {severity!r}")
        if severity == "blocking":
            blocking += 1

    if gate == "PASS" and blocking:
        errors.append(f"{label}: PASS artifact cannot contain blocking open items")
    if gate == "BLOCKED" and not blocking:
        errors.append(f"{label}: BLOCKED artifact must contain a blocking open item")
    if gate == "CONDITIONAL" and not open_items:
        errors.append(f"{label}: CONDITIONAL artifact must contain an open item")

    if stage == "SPEC_STEP_1" and isinstance(payload, dict):
        if payload.get("knowledge_retrieval_performed") is not False:
            errors.append(f"{label}: Step 1 knowledge_retrieval_performed must be false")
        banned = find_keys(payload, STEP1_BANNED_KEYS)
        if banned:
            errors.append(f"{label}: Step 1 contains knowledge or physical mapping keys: {', '.join(banned)}")
        disallowed_sources = {
            item.get("source_type") for item in evidence
            if isinstance(item, dict) and item.get("source_type") not in STEP1_ALLOWED_EVIDENCE
        }
        if disallowed_sources:
            errors.append(f"{label}: Step 1 contains disallowed evidence source types: {sorted(disallowed_sources)}")

    if stage == "SPEC_STEP_2" and isinstance(payload, dict):
        banned = find_keys(payload, STEP2_BANNED_KEYS)
        if banned:
            errors.append(f"{label}: Step 2 contains Step 3 placement keys: {', '.join(banned)}")

    if stage == "SPEC_STEP_3" and gate == "PASS" and isinstance(payload, dict):
        if not payload.get("layering_rules_version"):
            errors.append(f"{label}: PASS Step 3 requires layering_rules_version")
        if not payload.get("placement_decision") or not payload.get("table_change_decision"):
            errors.append(f"{label}: PASS Step 3 requires placement and table-change decisions")

    if stage == "SPEC_STEP_4" and gate == "PASS" and isinstance(payload, dict):
        if not payload.get("target_schema"):
            errors.append(f"{label}: PASS Step 4 requires a non-empty target_schema")
        if not payload.get("tests"):
            errors.append(f"{label}: PASS Step 4 requires tests")

    if stage == "SPEC_STEP_5" and isinstance(payload, dict):
        if decisions:
            errors.append(f"{label}: Step 5 must not introduce new decisions")
        if gate == "PASS" and not payload.get("requirements_traceability"):
            errors.append(f"{label}: PASS Step 5 requires requirements_traceability")
        if gate == "PASS" and not payload.get("final_spec_path"):
            errors.append(f"{label}: PASS Step 5 requires final_spec_path")

    if stage == "DEBUG_SQL" and isinstance(payload, dict):
        if payload.get("execution_status") not in {"NOT_RUN", "PASSED", "FAILED", "PARTIAL"}:
            errors.append(f"{label}: invalid DEBUG_SQL execution_status")

    return errors


def validate_chain(artifacts: list[dict[str, Any]], labels: list[str]) -> list[str]:
    errors: list[str] = []
    if not artifacts:
        return errors

    request_ids = {item.get("request_id") for item in artifacts}
    if len(request_ids) != 1:
        errors.append(f"chain: request_id values differ: {sorted(str(value) for value in request_ids)}")

    artifact_ids = [item.get("artifact_id") for item in artifacts]
    if len(artifact_ids) != len(set(artifact_ids)):
        errors.append("chain: artifact_id values must be unique")

    seen_ids: set[str] = set()
    last_order = 0
    for artifact, label in zip(artifacts, labels):
        stage = artifact.get("stage")
        order = SPEC_ORDER.get(stage)
        if order is not None and order < last_order:
            errors.append(f"chain: {label} is out of Spec stage order")
        if order is not None:
            last_order = order
        inputs = artifact.get("input_artifact_ids", [])
        if order and order > 1 and not (set(inputs) & seen_ids):
            errors.append(f"chain: {label} does not reference a previous artifact")
        seen_ids.add(artifact.get("artifact_id"))

    prior_ids = {item.get("artifact_id") for item in artifacts[:-1]}
    for artifact, label in zip(artifacts, labels):
        if artifact.get("stage") != "SPEC_STEP_5":
            continue
        for claim in artifact.get("claims", []):
            if not isinstance(claim, dict):
                continue
            origin = claim.get("origin_artifact_id")
            if claim.get("evidence_ids"):
                errors.append(f"chain: {label} claim {claim.get('claim_id')} adds direct evidence in assembly stage")
            if origin not in prior_ids:
                errors.append(f"chain: {label} claim {claim.get('claim_id')} lacks a valid prior origin")
        upstream_statuses = [item.get("status") for item in artifacts[:-1] if item.get("stage") in SPEC_ORDER]
        if artifact.get("status") == "PASS" and any(status != "PASS" for status in upstream_statuses):
            errors.append("chain: PASS Step 5 cannot upgrade a non-PASS upstream stage")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Hive Data Agent JSON handoff artifacts.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--chain", action="store_true", help="validate ordering and cross-stage provenance")
    args = parser.parse_args()

    artifacts: list[dict[str, Any]] = []
    labels: list[str] = []
    errors: list[str] = []
    for path in args.paths:
        try:
            artifact = load_json(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        artifacts.append(artifact)
        labels.append(str(path))
        errors.extend(validate_artifact(artifact, str(path)))

    if args.chain and len(artifacts) == len(args.paths):
        errors.extend(validate_chain(artifacts, labels))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: validated {len(artifacts)} artifact(s){' as a chain' if args.chain else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
