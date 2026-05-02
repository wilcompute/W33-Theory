#!/usr/bin/env python3
"""
PART CLIX - Root-Stabilizer Spectral Action
==========================================

CLVII integrated the heat-kernel / Seeley-DeWitt coefficients:

    a0 = 480
    a2 = 2240
    a4 = 17600
    a2/a0 = 14/3
    a4/a2 = 55/7

CLVIII integrated the global Weyl closure:

    |Sp(4,3)| = |W(E6)| = 51840 = (78-2q)(qE) = 72*720.

This module fuses them.

The key observation is that the spectral action becomes especially clean
when normalized by the global E6/Weyl closure:

    a0 / |W(E6)| = 480/51840   = 1/108
    a2 / |W(E6)| = 2240/51840  = 7/162
    a4 / |W(E6)| = 17600/51840 = 55/162

These are not arbitrary fractions:

    108 = mu*q^3 = directed-edge stabilizer.
    162 = 2*q^4.
    7   = Phi6, the threshold field.
    55  = C(k-1,2), the Hashimoto radial wedge.

So the heat-kernel coefficients are global Weyl-normalized local carriers:

    a0 is the directed-edge carrier normalized by its stabilizer;
    a2 is the Phi6 threshold field over 2q^4;
    a4 is the radial wedge over 2q^4.

This is the root-stabilizer spectral action: the same group that closes the
E6 root orbit also normalizes the local heat-kernel ladder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
V = 40
K = 12
LAM = 2
MU = 4
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
HASHIMOTO_NORM = K - 1
EDGE_COUNT = V * K // 2
DIRECTED_EDGES = 2 * EDGE_COUNT
TRIANGLES = V * K * LAM // 6

E6_DIM = 78
CARTAN_SEED = 2 * Q
E6_ROOTS = E6_DIM - CARTAN_SEED
ROOT_STABILIZER = Q * EDGE_COUNT
WEYL_E6_ORDER = E6_ROOTS * ROOT_STABILIZER
SP43_ORDER = Q**4 * (Q**2 - 1) * (Q**4 - 1)

A0 = DIRECTED_EDGES
A2 = 2240
A4 = 17600
RADIAL_WEDGE = math.comb(HASHIMOTO_NORM, 2)
DIRECTED_EDGE_STABILIZER = SP43_ORDER // DIRECTED_EDGES
TRIANGLE_STABILIZER = SP43_ORDER // TRIANGLES
NORMALIZER_DEN = 2 * Q**4


@dataclass(frozen=True)
class NormalizedCoefficient:
    coefficient: str
    raw_value: int
    global_normalization: str
    normalized_value: str
    structural_identity: str
    interpretation: str


def normalized_coefficients() -> List[NormalizedCoefficient]:
    return [
        NormalizedCoefficient(
            coefficient="a0",
            raw_value=A0,
            global_normalization="a0/|W(E6)|",
            normalized_value=str(Fraction(A0, WEYL_E6_ORDER)),
            structural_identity="1/(mu*q^3)=1/108",
            interpretation="directed-edge carrier normalized by directed-edge stabilizer",
        ),
        NormalizedCoefficient(
            coefficient="a2",
            raw_value=A2,
            global_normalization="a2/|W(E6)|",
            normalized_value=str(Fraction(A2, WEYL_E6_ORDER)),
            structural_identity="Phi6/(2*q^4)=7/162",
            interpretation="threshold field normalized by the 2*q^4 root/triangle scale",
        ),
        NormalizedCoefficient(
            coefficient="a4",
            raw_value=A4,
            global_normalization="a4/|W(E6)|",
            normalized_value=str(Fraction(A4, WEYL_E6_ORDER)),
            structural_identity="C(k-1,2)/(2*q^4)=55/162",
            interpretation="Hashimoto radial wedge normalized by the 2*q^4 root/triangle scale",
        ),
    ]


def root_stabilizer_spectral_action_audit() -> Dict[str, object]:
    norm_a0 = Fraction(A0, WEYL_E6_ORDER)
    norm_a2 = Fraction(A2, WEYL_E6_ORDER)
    norm_a4 = Fraction(A4, WEYL_E6_ORDER)

    checks = {
        "global_order_matches_sp43": WEYL_E6_ORDER == SP43_ORDER == 51840,
        "root_orbit_times_stabilizer": E6_ROOTS * ROOT_STABILIZER == WEYL_E6_ORDER,
        "a0_is_directed_edges": A0 == DIRECTED_EDGES == 480,
        "a0_global_norm_is_inverse_directed_edge_stabilizer": norm_a0 == Fraction(1, DIRECTED_EDGE_STABILIZER) == Fraction(1, 108),
        "a2_global_norm_is_phi6_over_2q4": norm_a2 == Fraction(PHI6, NORMALIZER_DEN) == Fraction(7, 162),
        "a4_global_norm_is_radial_wedge_over_2q4": norm_a4 == Fraction(RADIAL_WEDGE, NORMALIZER_DEN) == Fraction(55, 162),
        "a2_over_a0_survives_global_normalization": norm_a2 / norm_a0 == Fraction(A2, A0) == Fraction(14, 3),
        "a4_over_a2_survives_global_normalization": norm_a4 / norm_a2 == Fraction(A4, A2) == Fraction(55, 7),
        "lambda_H_is_inverse_radial_threshold": Fraction(PHI6, RADIAL_WEDGE) == Fraction(7, 55),
        "normalizer_den_is_half_triangle_stabilizer": NORMALIZER_DEN == TRIANGLE_STABILIZER // 2 == 162,
        "directed_edge_stabilizer_is_mu_q3": DIRECTED_EDGE_STABILIZER == MU * Q**3 == 108,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLIX_ROOT_STABILIZER_SPECTRAL_ACTION",
        "source_links": {
            "CLVII": "spectral-action ladder",
            "CLVIII": "global E6/Weyl closure",
        },
        "w33_atoms": {
            "q": Q,
            "v": V,
            "k": K,
            "lambda": LAM,
            "mu": MU,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "Hashimoto_norm": HASHIMOTO_NORM,
            "edges": EDGE_COUNT,
            "directed_edges": DIRECTED_EDGES,
            "triangles": TRIANGLES,
        },
        "global_closure": {
            "E6_dim": E6_DIM,
            "Cartan_seed_2q": CARTAN_SEED,
            "E6_roots": E6_ROOTS,
            "root_stabilizer_qE": ROOT_STABILIZER,
            "W_E6_order": WEYL_E6_ORDER,
            "Sp_4_3_order": SP43_ORDER,
        },
        "spectral_action": {
            "a0": A0,
            "a2": A2,
            "a4": A4,
            "a2_over_a0": str(Fraction(A2, A0)),
            "a4_over_a2": str(Fraction(A4, A2)),
            "lambda_H": str(Fraction(PHI6, RADIAL_WEDGE)),
        },
        "normalized_coefficients": [asdict(c) for c in normalized_coefficients()],
        "stabilizer_scales": {
            "directed_edge_stabilizer": DIRECTED_EDGE_STABILIZER,
            "triangle_stabilizer": TRIANGLE_STABILIZER,
            "normalizer_den_2q4": NORMALIZER_DEN,
            "normalizer_den_identity": "2*q^4 = triangle_stabilizer/2 = 162",
        },
        "checks": checks,
        "theorem_statement": (
            "The Seeley-DeWitt spectral action is normalized by the global E6/Weyl "
            "root-stabilizer closure.  Dividing by |W(E6)|=51840 gives a0/|W|=1/108, "
            "a2/|W|=Phi6/(2q^4)=7/162, and a4/|W|=C(k-1,2)/(2q^4)=55/162.  Thus "
            "a0 is the directed-edge carrier, a2 is the threshold field, and a4 is the "
            "radial wedge, all expressed in the same global root-stabilizer units."
        ),
        "interpretive_note": (
            "This fuses CLVII and CLVIII.  The heat-kernel ladder is the local spectral "
            "shadow of the E6 root orbit closure: the global Weyl group normalizes the "
            "directed-edge carrier, the Phi6 threshold field, and the Hashimoto radial wedge."
        ),
    }


def main() -> int:
    audit = root_stabilizer_spectral_action_audit()
    out = ROOT / "PART_CLIX_root_stabilizer_spectral_action_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
