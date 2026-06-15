#!/usr/bin/env python3
"""BT1120 K3 spectral-action interface.

This is a schema/adapter skeleton, not a curvature solver. It validates that a
K3 spectral-action result reports the convention data needed to interpret A0,
A2, and A4, and emits a normalized JSON envelope.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_TOP_LEVEL = [
    "operator_convention",
    "metric_source",
    "volume_normalization",
    "A0",
    "A2",
    "A4",
    "curvature_convention",
    "refinement_h",
    "topological_checks",
]

REQUIRED_TOPOLOGY = ["chi", "signature", "b2", "intersection_signature"]

FINITE_PREFACTORS = {
    "mH2_over_v2": "14/55",
    "lambda_H": "7/55",
    "finite_a2_over_a0": "14/3",
    "finite_a4_over_a2": "55/7",
}


def validate(payload: dict) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED_TOP_LEVEL:
        if key not in payload:
            errors.append(f"missing top-level key: {key}")
    topo = payload.get("topological_checks", {})
    if isinstance(topo, dict):
        for key in REQUIRED_TOPOLOGY:
            if key not in topo:
                errors.append(f"missing topological check: {key}")
    else:
        errors.append("topological_checks must be an object")
    return errors


def envelope(payload: dict) -> dict:
    errors = validate(payload)
    return {
        "theorem": "BT1120 K3 spectral-action result envelope",
        "valid": not errors,
        "errors": errors,
        "input_result": payload,
        "finite_w33_prefactors": FINITE_PREFACTORS,
        "done_open_boundary": "finite ratios are seed-independent; K3 result supplies geometric multipliers for gravity scales",
        "compile_claim": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", help="K3 spectral-action result JSON to validate")
    parser.add_argument("--out", default="data/bt1120_k3_spectral_action_result_envelope.json")
    args = parser.parse_args()

    payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    out = envelope(payload)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0 if out["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
