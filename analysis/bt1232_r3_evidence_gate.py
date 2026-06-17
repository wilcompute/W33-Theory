#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from pathlib import Path

LANES = ["schema_stub", "blocked", "partial", "near_candidate", "candidate"]
BLOCKERS = ("mock", "placeholder", "not_computed", "stub", "schema_stub")
REQUIRED_BLOCKS = ["metric_block", "operator_block", "heat_block", "curvature_block", "refinement_block"]


def contains_blocker(x):
    if isinstance(x, str):
        return any(w in x for w in BLOCKERS)
    if isinstance(x, dict):
        return any(contains_blocker(v) for v in x.values())
    if isinstance(x, list):
        return any(contains_blocker(v) for v in x)
    return False


def has_numbers(sample):
    return (
        sample.get("refinement_block", {}).get("h") is not None and
        bool(sample.get("operator_block", {}).get("eigenvalue_sample")) and
        sample.get("heat_block", {}).get("A4", {}).get("value") is not None and
        sample.get("curvature_block", {}).get("error_to_target") is not None
    )


def classify(sample):
    missing = [b for b in REQUIRED_BLOCKS if b not in sample]
    status = sample.get("claim_status", "unknown")
    metric_cert = sample.get("metric_block", {}).get("independent_metric_certification") is True
    op_cert = sample.get("operator_block", {}).get("independent_operator_certification") is True
    numeric = has_numbers(sample)
    blockers = contains_blocker(sample)
    if status == "schema_stub_only" or missing:
        lane = "schema_stub"
    elif blockers:
        lane = "blocked"
    elif not numeric:
        lane = "partial"
    elif numeric and not (metric_cert and op_cert):
        lane = "near_candidate"
    else:
        lane = "candidate"
    return {
        "sample_id": sample.get("sample_id", "unknown"),
        "lane": lane,
        "missing_blocks": missing,
        "all_numerical_fields_present": numeric,
        "independent_metric_certification": metric_cert,
        "independent_operator_certification": op_cert,
        "candidate_allowed": lane == "candidate",
    }


def demo_samples():
    base = {
        "schema": "BT1215_K3_GEOMETRY_SAMPLE_V1",
        "sample_id": "base",
        "topology": {"chi":24,"signature":-16,"b2":22,"intersection_signature":[3,19]},
        "metric_block": {"shape_quality": 0.99},
        "operator_block": {"eigenvalue_sample": [1,4,9]},
        "heat_block": {"A4": {"value": 24.0}},
        "curvature_block": {"error_to_target": 0.01},
        "refinement_block": {"h": 0.03125},
    }
    schema = {"sample_id":"schema_stub", "claim_status":"schema_stub_only"}
    blocked = dict(base, sample_id="blocked_mock", metric_block={"source":"mock_metric"}, claim_status="mock_sequence")
    partial = dict(base, sample_id="partial_missing_A4", heat_block={"A4":{"value": None}}, claim_status="partial_computed_candidate")
    near = dict(base, sample_id="near_complete_uncertified", metric_block={"shape_quality":0.996875,"independent_metric_certification":False}, operator_block={"eigenvalue_sample":[1,4,9],"independent_operator_certification":False}, claim_status="near_candidate_pending_certification")
    cand = dict(base, sample_id="candidate_certified", metric_block={"shape_quality":0.999,"independent_metric_certification":True}, operator_block={"eigenvalue_sample":[1,4,9],"independent_operator_certification":True}, claim_status="certified_candidate")
    return [schema, blocked, partial, near, cand]


def build():
    rows = [classify(s) for s in demo_samples()]
    counts = {lane: sum(r["lane"] == lane for r in rows) for lane in LANES}
    return {
        "bt": 1232,
        "title": "Unified R3 evidence gate",
        "lanes": LANES,
        "required_blocks": REQUIRED_BLOCKS,
        "promotion_rule": "candidate iff numerical fields are present and independent metric/operator certifications are both true",
        "demo_classifications": rows,
        "demo_counts": counts,
        "near_candidate_promoted": any(r["sample_id"] == "near_complete_uncertified" and r["candidate_allowed"] for r in rows),
        "certified_candidate_promoted": any(r["sample_id"] == "candidate_certified" and r["candidate_allowed"] for r in rows),
        "fail_closed": True,
        "interpretation": "The R3 gate distinguishes numerical completeness from evidence status. A near-candidate remains blocked until independent metric and operator certifications are true."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1232_r3_evidence_gate_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1232, "fail_closed": True, "out": str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
