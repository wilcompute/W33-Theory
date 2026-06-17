#!/usr/bin/env python3
"""BT1215 -- K3 geometry sample schema.

Defines the next R3 compute-lane contract.  This is a validation stub only: it
has K3 topology and required fields, but no computed metric spectrum yet.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TOPOLOGY = {
    "chi": 24,
    "signature": -16,
    "b2": 22,
    "intersection_signature": [3, 19],
}

REQUIRED = [
    "schema",
    "sample_id",
    "topology",
    "metric_block",
    "operator_block",
    "heat_block",
    "curvature_block",
    "refinement_block",
    "claim_status",
]


def sample_stub() -> dict:
    return {
        "schema": "BT1215_K3_GEOMETRY_SAMPLE_V1",
        "sample_id": "k3_geometry_sample_stub_v1",
        "topology": TOPOLOGY,
        "metric_block": {
            "source": "placeholder_not_computed",
            "volume_normalization": "unit_volume_target",
            "shape_quality": None,
        },
        "operator_block": {
            "convention": "square_operator_sample_required",
            "eigenvalue_sample": [],
            "status": "not_computed",
        },
        "heat_block": {
            "A0": {"value": 1.0, "status": "normalization_placeholder"},
            "A2": {"value": 0.0, "status": "ricci_flat_target_placeholder"},
            "A4": {"value": None, "status": "not_computed"},
        },
        "curvature_block": {
            "normalized_Rm2_over_8pi2": {"value": 24.0, "status": "topology_target"},
            "error_to_target": None,
        },
        "refinement_block": {
            "h": None,
            "index": None,
            "previous_sample_id": None,
        },
        "claim_status": "schema_stub_only",
    }


def validate(sample: dict) -> dict:
    errors = []
    for key in REQUIRED:
        if key not in sample:
            errors.append(f"missing {key}")
    for key, expected in TOPOLOGY.items():
        if sample.get("topology", {}).get(key) != expected:
            errors.append(f"topology mismatch {key}")
    if sample.get("claim_status") != "schema_stub_only":
        errors.append("claim_status must be schema_stub_only")
    return {"valid": not errors, "errors": errors, "required": REQUIRED, "required_topology": TOPOLOGY}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/bt1215_k3_geometry_sample_stub.json"))
    parser.add_argument("--validation", type=Path, default=Path("data/bt1215_k3_geometry_schema_validation.json"))
    args = parser.parse_args()
    stub = sample_stub()
    report = {"bt": 1215, "title": "K3 geometry compute-lane schema", **validate(stub)}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(stub, indent=2) + "\n")
    args.validation.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"bt": 1215, "valid": report["valid"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
