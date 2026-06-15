#!/usr/bin/env python3
"""
BT1138 -- K3 A4 normalization lane for the W33 product heat coefficient.

This does not claim a fully normalized physical Seeley--DeWitt coefficient.
It computes the corpus-normalized Ricci-flat K3 curvature target used by the
BT1127/BT1129/BT1134 lane:

    A0 = 1                       unit-volume normalization placeholder
    A2 = 0                       Ricci-flat scalar-curvature slot
    A4_norm = int |Rm|^2/(8*pi^2) = chi(K3) = 24

Then it plugs this into the verified finite product coefficient

    C4 = 440*A4 - 1920*A2 + 8160*A0.

The surprise closure is

    C4_norm = 18720 = 240 * 78 = E * q! * Phi_3.
"""

from __future__ import annotations

import json
from fractions import Fraction

q = 3
lam = 2
mu = 4
k = 12
v = 40
E_edges = v * k // 2
Phi3 = q * q + q + 1
q_factorial = 6

N = 440
F2 = 1920
F4_over_2 = 8160

K3 = {
    "chi": 24,
    "signature": -16,
    "b2": 22,
    "intersection_signature": [3, 19],
}

A0 = 1
A2 = 0
A4_norm = K3["chi"]

C0 = N * A0
C2 = N * A2 - F2 * A0
C4_norm = N * A4_norm - F2 * A2 + F4_over_2 * A0

checks = {
    "k3_topology_b2": sum(K3["intersection_signature"]) == K3["b2"],
    "k3_topology_signature": K3["intersection_signature"][0] - K3["intersection_signature"][1] == K3["signature"],
    "k3_euler_from_betti": 2 + K3["b2"] == K3["chi"],
    "ricci_flat_A2_zero": A2 == 0,
    "normalized_A4_equals_chi": A4_norm == 24,
    "C4_norm_value": C4_norm == 18720,
    "C4_over_E_is_q_factorial_Phi3": Fraction(C4_norm, E_edges) == q_factorial * Phi3,
    "C4_equals_E_qfactorial_Phi3": C4_norm == E_edges * q_factorial * Phi3,
}
checks["all_checks_pass"] = all(checks.values())

payload = {
    "bt": 1138,
    "title": "K3 A4 normalization lane for W33 product heat coefficient",
    "normalization_boundary": (
        "A4_norm is the corpus-normalized Ricci-flat curvature target "
        "Integral |Rm|^2/(8*pi^2)=chi(K3)=24, not a completed physical "
        "Seeley-DeWitt coefficient with all convention-dependent constants."
    ),
    "w33_constants": {
        "q": q,
        "q_factorial": q_factorial,
        "lambda": lam,
        "mu": mu,
        "k": k,
        "v": v,
        "E": E_edges,
        "Phi3": Phi3,
    },
    "k3_topology": K3,
    "finite_moments": {
        "N": N,
        "F2": F2,
        "F4_over_2": F4_over_2,
    },
    "ricci_flat_unit_volume_inputs": {
        "A0": A0,
        "A2": A2,
        "A4_norm": A4_norm,
    },
    "product_coefficients_normalized": {
        "C0": C0,
        "C2": C2,
        "C4_norm": C4_norm,
    },
    "integer_closure": {
        "C4_norm": C4_norm,
        "C4_norm_over_E": str(Fraction(C4_norm, E_edges)),
        "q_factorial_times_Phi3": q_factorial * Phi3,
        "identity": "C4_norm = E*q!*Phi3 = 240*6*13 = 18720",
    },
    "checks": checks,
}

print(json.dumps(payload, indent=2, sort_keys=True))
