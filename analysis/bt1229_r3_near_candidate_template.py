#!/usr/bin/env python3
"""BT1229 -- R3 near-candidate template.

Creates a sample with all numerical fields present but one final certification
field missing.  This tests the near-green boundary: data can look complete while
still being blocked from evidence status by missing independent provenance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TOPOLOGY = {"chi": 24, "signature": -16, "b2": 22, "intersection_signature": [3, 19]}


def make_template() -> dict:
    return {
        "schema": "BT1215_K3_GEOMETRY_SAMPLE_V1",
        "sample_id": "k3_near_candidate_n64_template_v1",
        "topology": TOPOLOGY,
        "metric_block": {
            "source": "numeric_metric_family_v1",
            "volume_normalization": "unit_volume_target",
            "shape_quality": 0.996875,
            "independent_metric_certification": False,
        },
        "operator_block": {
            "convention": "square_operator_numeric_sample",
            "eigenvalue_sample": [1.015625, 4.0625, 9.140625, 16.25, 25.390625, 36.5625, 49.765625, 64.0],
            "status": "computed_numeric",
            "independent_operator_certification": False,
        },
        "heat_block": {
            "A0": {"value": 1.0, "status": "computed"},
            "A2": {"value": 0.000244140625, "status": "computed"},
            "A4": {"value": 24.00048828125, "status": "computed"},
        },
        "curvature_block": {
            "normalized_Rm2_over_8pi2": {"value": 24.000244140625, "status": "computed"},
            "error_to_target": 0.000244140625,
        },
        "refinement_block": {
            "h": 0.015625,
            "index": 64,
            "previous_sample_id": "k3_partial_refinement_n32_v1",
        },
        "claim_status": "near_candidate_pending_certification",
    }


def status(sample: dict) -> dict:
    metric_cert = sample["metric_block"].get("independent_metric_certification") is True
    operator_cert = sample["operator_block"].get("independent_operator_certification") is True
    all_numbers_present = (
        sample["refinement_block"].get("h") is not None
        and bool(sample["operator_block"].get("eigenvalue_sample"))
        and sample["heat_block"]["A4"].get("value") is not None
        and sample["curvature_block"].get("error_to_target") is not None
    )
    return {
        "bt": 1229,
        "title": "R3 near-candidate template",
        "sample": sample,
        "status_check": {
            "all_numerical_fields_present": all_numbers_present,
            "independent_metric_certification": metric_cert,
            "independent_operator_certification": operator_cert,
            "validator_expected_level": "near_candidate_blocked_by_certification",
            "candidate_allowed": all_numbers_present and metric_cert and operator_cert,
        },
        "interpretation": "The sample is numerically complete but still blocked because independent metric/operator certification is absent.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/bt1229_r3_near_candidate_template.json"))
    args = parser.parse_args()
    result = status(make_template())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1229, "candidate_allowed": result["status_check"]["candidate_allowed"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
