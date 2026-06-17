#!/usr/bin/env python3
"""BT1220 -- schema-valid mock R3 sample sequence.

Builds a sequence of BT1215-shaped samples with non-null refinement h, shape
quality, and mock eigenvalue arrays.  The sequence is schema-valid but fails
promotion because the operator and metric values are explicitly mock data.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import math

TOPOLOGY = {"chi": 24, "signature": -16, "b2": 22, "intersection_signature": [3, 19]}


def eigen_mock(n: int, count: int = 8) -> list[float]:
    return [round(((k + 1) ** 2) * (1.0 + 1.0 / n), 8) for k in range(count)]


def sample(n: int, previous: str | None) -> dict:
    h = 1.0 / n
    sid = f"k3_mock_refinement_n{n}"
    return {
        "schema": "BT1215_K3_GEOMETRY_SAMPLE_V1",
        "sample_id": sid,
        "topology": TOPOLOGY,
        "metric_block": {
            "source": "mock_sequence_not_physical_metric",
            "volume_normalization": "unit_volume_target",
            "shape_quality": round(1.0 - 0.2 * h, 10),
        },
        "operator_block": {
            "convention": "square_operator_mock_sample",
            "eigenvalue_sample": eigen_mock(n),
            "status": "mock_not_computed",
        },
        "heat_block": {
            "A0": {"value": 1.0, "status": "mock_normalized"},
            "A2": {"value": round(h*h, 12), "status": "mock_converges_to_ricci_flat_target"},
            "A4": {"value": round(24.0 + 2.0*h*h, 12), "status": "mock_converges_to_curvature_target"},
        },
        "curvature_block": {
            "normalized_Rm2_over_8pi2": {"value": round(24.0 + h*h, 12), "status": "mock_sequence"},
            "error_to_target": round(h*h, 12),
        },
        "refinement_block": {
            "h": h,
            "index": n,
            "previous_sample_id": previous,
        },
        "claim_status": "mock_sequence_only",
    }


def nonincreasing(xs: list[float]) -> bool:
    return all(xs[i+1] <= xs[i] for i in range(len(xs)-1))


def nondecreasing(xs: list[float]) -> bool:
    return all(xs[i+1] >= xs[i] for i in range(len(xs)-1))


def build(ns: list[int]) -> dict:
    rows = []
    previous = None
    for n in ns:
        s = sample(n, previous)
        rows.append(s)
        previous = s["sample_id"]
    checks = {
        "all_have_nonnull_h": all(r["refinement_block"]["h"] is not None for r in rows),
        "shape_quality_improves": nondecreasing([r["metric_block"]["shape_quality"] for r in rows]),
        "A2_mock_decreases": nonincreasing([r["heat_block"]["A2"]["value"] for r in rows]),
        "A4_mock_converges_to_24": nonincreasing([abs(r["heat_block"]["A4"]["value"] - 24.0) for r in rows]),
        "curvature_error_decreases": nonincreasing([r["curvature_block"]["error_to_target"] for r in rows]),
        "promotion_allowed": False,
    }
    return {
        "bt": 1220,
        "title": "R3 schema-valid mock refinement sequence",
        "samples": rows,
        "checks": checks,
        "sequence_schema_valid": all(checks[k] for k in checks if k != "promotion_allowed"),
        "promotion_allowed": False,
        "promotion_blocker": "metric and operator blocks are mock_sequence_not_physical_metric / mock_not_computed",
        "interpretation": "This sequence exercises the BT1215 schema and BT1210/BT1213 monotone checks with non-null refinement data, while intentionally refusing promotion to physical R3 evidence.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ns", type=int, nargs="+", default=[8, 16, 32, 64])
    parser.add_argument("--out", type=Path, default=Path("data/bt1220_r3_schema_valid_mock_sequence.json"))
    args = parser.parse_args()
    result = build(args.ns)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1220, "schema_valid": result["sequence_schema_valid"], "promotion_allowed": result["promotion_allowed"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
