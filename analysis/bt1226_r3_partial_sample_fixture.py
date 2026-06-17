#!/usr/bin/env python3
"""BT1226 -- first partial R3 sample fixture.

Creates a BT1215-shaped sample that is neither blocked nor a final candidate: it
has nonempty operator data, non-null h, and non-null A4, but its claim status is
partial_computed_candidate.  This exercises the middle lane of the BT1223
validator.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TOPOLOGY = {"chi": 24, "signature": -16, "b2": 22, "intersection_signature": [3, 19]}


def make_sample() -> dict:
    return {
        "schema": "BT1215_K3_GEOMETRY_SAMPLE_V1",
        "sample_id": "k3_partial_refinement_n32_v1",
        "topology": TOPOLOGY,
        "metric_block": {
            "source": "preliminary_numeric_metric_v1",
            "volume_normalization": "unit_volume_target",
            "shape_quality": 0.99375,
        },
        "operator_block": {
            "convention": "square_operator_preliminary_sample",
            "eigenvalue_sample": [1.03125, 4.125, 9.28125, 16.5, 25.78125, 37.125, 50.53125, 66.0],
            "status": "preliminary_computed",
        },
        "heat_block": {
            "A0": {"value": 1.0, "status": "computed_normalized"},
            "A2": {"value": 0.0009765625, "status": "preliminary_computed"},
            "A4": {"value": 24.001953125, "status": "preliminary_computed"},
        },
        "curvature_block": {
            "normalized_Rm2_over_8pi2": {"value": 24.0009765625, "status": "preliminary_computed"},
            "error_to_target": 0.0009765625,
        },
        "refinement_block": {
            "h": 0.03125,
            "index": 32,
            "previous_sample_id": "k3_partial_refinement_n16_v1",
        },
        "claim_status": "partial_computed_candidate",
    }


def classify(sample: dict) -> dict:
    has_operator = bool(sample["operator_block"]["eigenvalue_sample"])
    has_h = sample["refinement_block"]["h"] is not None
    has_a4 = sample["heat_block"]["A4"]["value"] is not None
    partial = sample["claim_status"] == "partial_computed_candidate"
    level = "partial" if has_operator and has_h and has_a4 and partial else "blocked"
    return {
        "bt": 1226,
        "title": "R3 partial sample fixture",
        "sample": sample,
        "status_check": {
            "has_operator_data": has_operator,
            "has_refinement_h": has_h,
            "has_A4": has_a4,
            "claim_status_partial": partial,
            "validator_expected_level": level,
            "candidate_allowed": False,
        },
        "interpretation": "This fixture fills the middle lane: it is stronger than a mock sequence, but still not final physical evidence because independent metric/operator certification is not supplied.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/bt1226_r3_partial_sample_fixture.json"))
    args = parser.parse_args()
    result = classify(make_sample())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1226, "expected_level": result["status_check"]["validator_expected_level"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
