#!/usr/bin/env python3
"""BT1120/BT1131 K3 spectral-action interface.

This is a schema/adapter skeleton, not a curvature solver. It validates that a
K3 spectral-action result reports the convention data needed to interpret the
pure manifold coefficients A0, A2, and A4, then emits a normalized JSON envelope.

BT1131 hardens the interface with the product-heat split from BT1129/BT1130:

    Theta_M(t)=A0*t^-2 + A2*t^-1 + A4 + ...
    Theta_F(t)=N - F2*t + (F4/2)*t^2 + ...

so

    C0 = A0*N
    C2 = A2*N - A0*F2
    C4 = A4*N - A2*F2 + A0*F4/2.

For Ricci-flat K3, A2=0 but C2=-A0*F2, so the finite W33 heat moment fills the
product Lambda^2 slot.
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

PRODUCT_HEAT_FORMULAS = {
    "C0": "A0*N",
    "C2": "A2*N - A0*F2",
    "C4": "A4*N - A2*F2 + A0*F4/2",
}

RICCI_FLAT_K3_PRODUCT_FORMULAS = {
    "condition": "A2=0",
    "C0": "A0*N",
    "C2": "-A0*F2",
    "C4": "A4*N + A0*F4/2",
}

FINITE_RATIO_WARNING = (
    "finite_a2_over_a0 is a finite-factor moment ratio, not the pure K3 A2/A0. "
    "For Ricci-flat K3 the pure A2 coefficient is zero, while the product C2 "
    "coefficient is filled by the finite moment -A0*F2."
)


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


def k3_topology_passes(payload: dict) -> dict:
    topo = payload.get("topological_checks", {})
    if not isinstance(topo, dict):
        return {"available": False}
    chi = topo.get("chi")
    sig = topo.get("signature")
    b2 = topo.get("b2")
    pair = topo.get("intersection_signature")
    checks = {"available": True}
    if isinstance(pair, list) and len(pair) == 2:
        p, n = pair
        checks.update(
            {
                "b2_from_intersection": p + n == b2,
                "signature_from_intersection": p - n == sig,
            }
        )
    checks["euler_from_betti_when_k3"] = (2 + b2 == chi) if isinstance(b2, int) else False
    return checks


def envelope(payload: dict) -> dict:
    errors = validate(payload)
    return {
        "theorem": "BT1120/BT1131 K3 spectral-action result envelope",
        "valid": not errors,
        "errors": errors,
        "input_result": payload,
        "finite_w33_prefactors": FINITE_PREFACTORS,
        "product_heat_formulas": PRODUCT_HEAT_FORMULAS,
        "ricci_flat_k3_product_formulas": RICCI_FLAT_K3_PRODUCT_FORMULAS,
        "k3_topology_checks_evaluated": k3_topology_passes(payload),
        "finite_ratio_warning": FINITE_RATIO_WARNING,
        "done_open_boundary": (
            "finite ratios are seed-independent finite-factor ratios; K3 supplies "
            "geometric multipliers and topology/volume data for gravity scales"
        ),
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
