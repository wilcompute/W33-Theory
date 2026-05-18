#!/usr/bin/env python3
"""Evaluation lattice of the toroidal metric multiplicity operator.

Let c_m be the metric edge-class multiplicity histogram of the seven
toroidal realizations:

    c_1,c_2,c_3,c_4,c_5,c_6 = 12,48,0,4,1,3.

Use the shifted parity variable s=1+t and define

    W(s)=sum_m c_m s^m
        = 12s + 48s^2 + 0s^3 + 4s^4 + s^5 + 3s^6.

Previous layers used W(1)=68, W(2)=504, and W(-1)=42.  This verifier
records the full small evaluation lattice around the Euler zero:

    W(-2)=392 = 7^2 * 8,
    W(-1)=42  = 7 * 6,
    W(0)=0,
    W(1)=68   = 4 * 17,
    W(2)=504  = 7 * 72 = 7 * 8 * 9.

The pair W(2), W(-2) recovers the even/odd Boolean lifts:

    even Boolean = (W(2)+W(-2))/2 = 448 = 7*64,
    odd Boolean  = (W(2)-W(-2))/2 = 56  = 7*8.

The pair W(1), W(-1) recovers the even/odd metric-class counts:

    even classes = (W(1)+W(-1))/2 = 55 = 5*11,
    odd classes  = (W(1)-W(-1))/2 = 13 = Phi_3.

Thus the values at +/-1 and +/-2 are the class and Boolean parity projectors.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "w33_toroidal_metric_evaluation_lattice.json"

Q = 3
PHI3 = Q * Q + Q + 1
PHI6 = Q * Q - Q + 1
TOMOTOPE_CELLS = 1 + PHI6
CENTERED_SHELL = PHI6 - 1
MIDDLE_EIGENVALUE = 72
CHART_FLAGS = 42
IHARA = 11

C = {1: 12, 2: 48, 3: 0, 4: 4, 5: 1, 6: 3}


def W(s: int) -> int:
    return sum(count * (s ** m) for m, count in C.items())


def build_payload() -> dict[str, Any]:
    values = {s: W(s) for s in [-2, -1, 0, 1, 2]}

    even_classes = (values[1] + values[-1]) // 2
    odd_classes = (values[1] - values[-1]) // 2
    even_boolean = (values[2] + values[-2]) // 2
    odd_boolean = (values[2] - values[-2]) // 2

    identities = {
        "W_minus_2": values[-2] == PHI6 * PHI6 * TOMOTOPE_CELLS == 392,
        "W_minus_1": values[-1] == PHI6 * CENTERED_SHELL == CHART_FLAGS == 42,
        "W_zero": values[0] == 0,
        "W_one": values[1] == 68,
        "W_two": values[2] == PHI6 * MIDDLE_EIGENVALUE == PHI6 * TOMOTOPE_CELLS * (TOMOTOPE_CELLS + 1) == 504,
        "ratio_boolean_total_to_imbalance": values[2] * PHI6 == values[-2] * (TOMOTOPE_CELLS + 1),
        "even_classes": even_classes == 5 * IHARA == 55,
        "odd_classes": odd_classes == PHI3 == 13,
        "even_minus_odd": even_classes - odd_classes == CHART_FLAGS == 42,
        "even_boolean": even_boolean == PHI6 * TOMOTOPE_CELLS * TOMOTOPE_CELLS == 448,
        "odd_boolean": odd_boolean == PHI6 * TOMOTOPE_CELLS == 56,
        "middle_eigenvalue_split": MIDDLE_EIGENVALUE == TOMOTOPE_CELLS + TOMOTOPE_CELLS * TOMOTOPE_CELLS,
        "boolean_ratio": values[2] // PHI6 == 72 and values[-2] // PHI6 == 56,
    }

    theorem = (
        "Toroidal Metric Evaluation-Lattice Theorem.  In the shifted variable "
        "s=1+t, the toroidal metric multiplicity operator W(s)=sum c_m s^m "
        "has the five-point lattice W(-2)=392, W(-1)=42, W(0)=0, W(1)=68, "
        "W(2)=504.  The +/-1 pair gives the class parity projectors "
        "55=5*11 and 13=Phi_3; the +/-2 pair gives the Boolean parity "
        "projectors 448=7*64 and 56=7*8.  Hence W(2)/7=72 is the middle "
        "association-scheme eigenvalue, while W(-2)/7=56 is the signed "
        "Boolean imbalance 7*8."
    )

    return {
        "summary": {
            "W_values": {str(k): v for k, v in values.items()},
            "even_classes_from_pm1": even_classes,
            "odd_classes_from_pm1": odd_classes,
            "even_boolean_from_pm2": even_boolean,
            "odd_boolean_from_pm2": odd_boolean,
            "middle_eigenvalue_per_chart": values[2] // PHI6,
            "all_identities_hold": all(identities.values()),
        },
        "polynomial_shifted": {
            "definition": "W(s)=P(s-1)=sum c_m s^m",
            "W": "12s + 48s^2 + 0s^3 + 4s^4 + s^5 + 3s^6",
            "evaluation_lattice": {str(k): v for k, v in values.items()},
        },
        "class_parity_projectors": {
            "from_values": "W(1)=68, W(-1)=42",
            "even_classes": even_classes,
            "odd_classes": odd_classes,
            "closed_forms": {
                "even": "55 = 5*11 = Csaszar packet * Ihara prime",
                "odd": "13 = Phi3",
                "difference": "42 = one toroidal chart flag count",
            },
        },
        "boolean_parity_projectors": {
            "from_values": "W(2)=504, W(-2)=392",
            "even_boolean": even_boolean,
            "odd_boolean": odd_boolean,
            "closed_forms": {
                "even": "448 = 7*64 = Phi6 * 8^2",
                "odd": "56 = 7*8 = Phi6 * 8",
                "total_per_chart": "72 = 8 + 64",
                "imbalance_per_chart": "56 = 7*8 / 1 chart-normalized after dividing by Phi6 gives 8*7",
            },
        },
        "spectral_bridge": {
            "middle_eigenvalue": "W(2)/7 = 72",
            "signed_boolean_imbalance": "W(-2)=392=7^2*8",
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
        "honesty_boundary": "This is an exact finite evaluation-lattice identity for the toroidal metric edge packet. It does not by itself infer physical dynamics or empirical observables.",
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
