#!/usr/bin/env python3
"""Hadamard area invariant of the toroidal metric evaluation lattice.

The shifted metric polynomial W(s) has evaluations

    W(-2)=392, W(-1)=42, W(0)=0, W(1)=68, W(2)=504.

The +/-1 Hadamard transform gives class parity projectors:

    C_even = (W(1)+W(-1))/2 = 55,
    C_odd  = (W(1)-W(-1))/2 = 13.

The +/-2 Hadamard transform gives Boolean-lift parity projectors:

    B_even = (W(2)+W(-2))/2 = 448,
    B_odd  = (W(2)-W(-2))/2 = 56.

Per toroidal chart, the Boolean vector is b=(64,8).  The class vector is
c=(55,13).  Their wedge/determinant is

    det[[55,64],[13,8]] = -392 = -7^2 * 8 = -W(-2).

Using the full Boolean vector (448,56), the determinant becomes

    det[[55,448],[13,56]] = -2744 = -(2*7)^3.

Thus the toroidal metric parity projectors have a quantized symplectic area:
the class/Boolean mismatch is exactly the signed Boolean imbalance W(-2),
and the seven-chart total area is the cube of the doubled heptad.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "w33_toroidal_metric_hadamard_area.json"

PHI6 = 7
TOMOTOPE_CELLS = 8
CHART_FLAGS = 42
MIDDLE_EIGENVALUE = 72
IHARA = 11
PHI3 = 13

W_VALUES = {-2: 392, -1: 42, 0: 0, 1: 68, 2: 504}


def det2(a: tuple[int, int], b: tuple[int, int]) -> int:
    return a[0] * b[1] - a[1] * b[0]


def build_payload() -> dict[str, Any]:
    class_even = (W_VALUES[1] + W_VALUES[-1]) // 2
    class_odd = (W_VALUES[1] - W_VALUES[-1]) // 2
    bool_even = (W_VALUES[2] + W_VALUES[-2]) // 2
    bool_odd = (W_VALUES[2] - W_VALUES[-2]) // 2
    bool_even_per_chart = bool_even // PHI6
    bool_odd_per_chart = bool_odd // PHI6

    class_vec = (class_even, class_odd)
    bool_vec = (bool_even, bool_odd)
    bool_chart_vec = (bool_even_per_chart, bool_odd_per_chart)
    raw_eval_vec_plus = (W_VALUES[1], W_VALUES[-1])
    raw_eval_vec_bool = (W_VALUES[2], W_VALUES[-2])

    area_chart = det2(class_vec, bool_chart_vec)
    area_total = det2(class_vec, bool_vec)
    area_raw = det2(raw_eval_vec_plus, raw_eval_vec_bool)

    identities = {
        "class_vector": class_vec == (5 * IHARA, PHI3) == (55, 13),
        "boolean_vector": bool_vec == (PHI6 * TOMOTOPE_CELLS * TOMOTOPE_CELLS, PHI6 * TOMOTOPE_CELLS) == (448, 56),
        "boolean_chart_vector": bool_chart_vec == (TOMOTOPE_CELLS * TOMOTOPE_CELLS, TOMOTOPE_CELLS) == (64, 8),
        "middle_eigenvalue": sum(bool_chart_vec) == MIDDLE_EIGENVALUE,
        "class_difference_flags": class_even - class_odd == CHART_FLAGS,
        "chart_area": area_chart == -W_VALUES[-2] == -(PHI6 * PHI6 * TOMOTOPE_CELLS) == -392,
        "total_area": area_total == -(2 * PHI6) ** 3 == -2744,
        "raw_area": area_raw == 2 * (2 * PHI6) ** 3 == 5488,
        "raw_area_relation": area_raw == -2 * area_total,
    }

    theorem = (
        "Toroidal Metric Hadamard-Area Theorem.  The +/-1 Hadamard transform "
        "of the metric evaluation lattice gives the class parity vector "
        "c=(55,13)=(5*11,Phi_3), while the +/-2 transform gives the Boolean "
        "parity vector B=(448,56)=7*(64,8).  Per chart, b=(64,8), and the "
        "wedge determinant det(c,b)=-392=-7^2*8=-W(-2).  On the full heptad, "
        "det(c,B)=-2744=-(2*7)^3.  Thus the mismatch between class parity "
        "and Boolean parity is a quantized heptadic symplectic area."
    )

    return {
        "summary": {
            "class_parity_vector": list(class_vec),
            "boolean_parity_vector_total": list(bool_vec),
            "boolean_parity_vector_per_chart": list(bool_chart_vec),
            "chart_area": area_chart,
            "total_area": area_total,
            "raw_evaluation_area": area_raw,
            "all_identities_hold": all(identities.values()),
        },
        "evaluation_lattice": {str(k): v for k, v in W_VALUES.items()},
        "hadamard_projectors": {
            "class_from_pm1": {
                "even": class_even,
                "odd": class_odd,
                "vector": list(class_vec),
                "closed_form": "c=(55,13)=(5*11,Phi3)",
            },
            "boolean_from_pm2": {
                "even": bool_even,
                "odd": bool_odd,
                "vector_total": list(bool_vec),
                "vector_per_chart": list(bool_chart_vec),
                "closed_form": "B=7*(64,8); b=(64,8)=(8^2,8)",
            },
        },
        "area_invariants": {
            "chart_normalized_area": area_chart,
            "chart_normalized_area_closed_form": "-392 = -7^2*8 = -W(-2)",
            "full_heptad_area": area_total,
            "full_heptad_area_closed_form": "-2744 = -(2*7)^3",
            "raw_evaluation_area": area_raw,
            "raw_evaluation_area_closed_form": "5488 = 2*(2*7)^3 = -2*full_heptad_area",
        },
        "spectral_bridge": {
            "middle_eigenvalue": "64+8=72",
            "flag_difference": "55-13=42",
            "signed_boolean_imbalance": "392=7^2*8",
            "target_spectrum": [
                "648^1",
                "(144 + 36*sqrt(6))^24",
                "72^30",
                "(144 - 36*sqrt(6))^24",
                "40^81",
            ],
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": "This is an exact finite Hadamard/determinant identity for the toroidal metric edge packet. It does not by itself imply physical dynamics or empirical observables.",
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
