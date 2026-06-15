#!/usr/bin/env python3
"""
BT1141 -- Spin and Hodge ordinary-trace a4 coefficients on Ricci-flat K3.

This completes the BT1140 convention split by fixing the operator-specific trace
coefficients used in

    a4(P) = K_norm * (2*r + 30*omega + 180*e2)/720,

where K_norm = int |Rm|^2/(8*pi^2)=24 for Ricci-flat K3.

Conventions used here:

  * scalar positive Laplacian: r=1, omega=0, e2=0;
  * spin Dirac square: complex rank r=4, E=R/4=0 on Ricci-flat K3,
    tr_spin(Omega_ij Omega_ij) = -1/2 |Rm|^2;
  * all-forms Hodge/de Rham Laplacian: ordinary trace over Lambda^*T^*K3,
    rank r=16, tr(Omega_ij Omega_ij) = -4 |Rm|^2, tr(E^2)=|Rm|^2.

The Hodge lane is ordinary trace, not Euler supertrace.
"""

from __future__ import annotations

import json
from fractions import Fraction

K_NORM = 24
N = 440
F4_OVER_2 = 8160
E_EDGES = 240
q_factorial = 6
Phi3 = 13


def a4(rank: int, omega: Fraction, e2: Fraction) -> Fraction:
    return Fraction(K_NORM, 720) * (2 * rank + 30 * omega + 180 * e2)


def product_c4(a4_value: Fraction) -> Fraction:
    return N * a4_value + F4_OVER_2

lanes = {
    "corpus_curvature_norm": {
        "rank": None,
        "omega": None,
        "e2": None,
        "a4": Fraction(24, 1),
        "role": "topological curvature normalization, not an operator heat coefficient",
    },
    "scalar_positive_laplacian": {
        "rank": 1,
        "omega": Fraction(0, 1),
        "e2": Fraction(0, 1),
        "role": "scalar Laplace-Beltrami heat coefficient",
    },
    "spin_dirac_square": {
        "rank": 4,
        "omega": Fraction(-1, 2),
        "e2": Fraction(0, 1),
        "role": "complex spin bundle, Lichnerowicz E=R/4 vanishes when Ricci-flat",
    },
    "hodge_all_forms_ordinary_trace": {
        "rank": 16,
        "omega": Fraction(-4, 1),
        "e2": Fraction(1, 1),
        "role": "ordinary trace over all forms; Euler supertrace deliberately excluded",
    },
}

for name, lane in lanes.items():
    if name == "corpus_curvature_norm":
        a4_value = lane["a4"]
    else:
        a4_value = a4(lane["rank"], lane["omega"], lane["e2"])
    lane["a4"] = a4_value
    lane["product_C4"] = product_c4(a4_value)

payload = {
    "bt": 1141,
    "title": "Spin and Hodge ordinary-trace a4 coefficients on Ricci-flat K3",
    "formula": "a4 = K_norm*(2*r + 30*omega + 180*e2)/720, K_norm=24",
    "lanes": {
        name: {
            key: (str(value) if isinstance(value, Fraction) else value)
            for key, value in lane.items()
        }
        for name, lane in lanes.items()
    },
    "substrate_closure": {
        "corpus_C4": str(lanes["corpus_curvature_norm"]["product_C4"]),
        "corpus_identity": f"{E_EDGES}*{q_factorial}*{Phi3}={E_EDGES*q_factorial*Phi3}",
    },
    "checks": {
        "scalar_a4": lanes["scalar_positive_laplacian"]["a4"] == Fraction(1, 15),
        "spin_a4": lanes["spin_dirac_square"]["a4"] == Fraction(-7, 30),
        "hodge_a4": lanes["hodge_all_forms_ordinary_trace"]["a4"] == Fraction(46, 15),
        "corpus_C4": lanes["corpus_curvature_norm"]["product_C4"] == 18720,
        "spin_product_C4": lanes["spin_dirac_square"]["product_C4"] == Fraction(24172, 3),
        "hodge_product_C4": lanes["hodge_all_forms_ordinary_trace"]["product_C4"] == Fraction(28528, 3),
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())

print(json.dumps(payload, indent=2, sort_keys=True))
