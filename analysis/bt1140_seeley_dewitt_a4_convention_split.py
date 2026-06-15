#!/usr/bin/env python3
"""
BT1140 -- convention split for K3 a4 lanes.

The previous BT1138 lane used the corpus-normalized curvature scalar

    K = int |Rm|^2/(8*pi^2) = chi(K3) = 24.

This script separates that normalization from operator-specific heat-kernel
coefficients.  For a Ricci-flat four-manifold and a Laplace-type operator

    P = -(g^{ij} nabla_i nabla_j + E)

with bundle rank r, connection curvature Omega_ij, and

    tr(Omega_ij Omega_ij) = omega_coeff |Rm|^2,
    tr(E^2) = e2_coeff |Rm|^2,

Gilkey's local a4 density reduces to

    a4(P) = K * (2*r + 30*omega_coeff + 180*e2_coeff) / 720.

This gives a clean conversion table:

  * corpus curvature normalization: A4_norm = K = 24;
  * scalar positive Laplacian: r=1, omega=e2=0, so a4=K/360=1/15;
  * spin Dirac/Hodge Dirac lanes are not silently identified with K; they are
    explicit operator lanes requiring their representation trace coefficients.
"""

from __future__ import annotations

import json
from fractions import Fraction

K_NORM = 24
N = 440
F2 = 1920
F4_OVER_2 = 8160


def a4_from_coeffs(rank: int, omega_coeff: Fraction, e2_coeff: Fraction) -> Fraction:
    return Fraction(K_NORM, 720) * (2 * rank + 30 * omega_coeff + 180 * e2_coeff)


scalar_a4 = a4_from_coeffs(1, Fraction(0), Fraction(0))
corpus_product_C4 = N * K_NORM + F4_OVER_2
scalar_product_C4 = N * scalar_a4 + F4_OVER_2

payload = {
    "bt": 1140,
    "title": "Seeley-DeWitt a4 convention split for Ricci-flat K3 lanes",
    "ricci_flat_reduction_formula": {
        "K_norm": "Integral |Rm|^2/(8*pi^2)=24",
        "generic_laplace_type": "a4 = K_norm*(2*r + 30*omega_coeff + 180*e2_coeff)/720",
        "coefficient_definitions": {
            "r": "bundle rank",
            "omega_coeff": "tr(Omega_ij Omega_ij)/|Rm|^2 in the chosen sign convention",
            "e2_coeff": "tr(E^2)/|Rm|^2 in the chosen Laplace-type convention",
        },
    },
    "lanes": {
        "corpus_curvature_norm": {
            "A4_norm": K_NORM,
            "product_C4": corpus_product_C4,
            "identity": "C4_norm = 18720 = E*q!*Phi3",
        },
        "scalar_positive_laplacian_gilkey": {
            "rank": 1,
            "omega_coeff": "0",
            "e2_coeff": "0",
            "a4": str(scalar_a4),
            "product_C4": str(scalar_product_C4),
            "note": "This is the scalar heat coefficient, not the corpus curvature normalization.",
        },
        "spin_dirac_square": {
            "rank_complex_4d": 4,
            "E_ricci_flat": "0 from Lichnerowicz R/4 term when R=0",
            "a4_template": "K_norm*(8 + 30*omega_spin)/720",
            "boundary": "omega_spin is the spin representation trace coefficient with sign convention fixed by the chosen Clifford normalization.",
        },
        "hodge_de_rham_laplacian_all_forms": {
            "rank_all_forms_4d": 16,
            "a4_template": "K_norm*(32 + 30*omega_hodge + 180*e2_hodge)/720",
            "boundary": "omega_hodge and e2_hodge are the ordinary-trace Weitzenbock coefficients; do not replace them by the Euler supertrace.",
        },
    },
    "checks": {
        "scalar_a4_is_1_over_15": scalar_a4 == Fraction(1, 15),
        "corpus_C4_is_18720": corpus_product_C4 == 18720,
        "scalar_lane_distinct_from_corpus_lane": scalar_a4 != K_NORM,
        "scalar_product_C4_fraction": str(scalar_product_C4),
        "all_checks_pass": scalar_a4 == Fraction(1, 15) and corpus_product_C4 == 18720 and scalar_a4 != K_NORM,
    },
}

print(json.dumps(payload, indent=2, sort_keys=True))
