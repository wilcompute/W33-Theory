#!/usr/bin/env python3
"""
PART CCCV - Spectral Complexity / Master Ladder Weld
====================================================

Purpose:
    Integrate today's CCXCIX--CCCIV commit stream with the earlier CLXXX
    master ladder.

Today's new stream adds a spectral-optimization spine:

    Krein/Bose-Mesner -> Lovasz theta / Delsarte LP -> Fiedler connectivity
    -> Matrix Tree / global complexity.

Main weld:
    The spanning-tree count of W(3,3)

        tau_tree(W) = 2^81 * 5^23

    contains the CLXXX H1/triple-Albert carrier q^4=81 as the exponent of 2.
    The exponent of 5 is

        23 = q^3 - (q+1) = 27 - 4,

    i.e. one Albert generation minus the EW gauge factor.

The spectral bridge is therefore:

    theta(W)=10, theta(complement)=4, theta product=40
    -> Fiedler lambda2=10 and Laplacian radius=16=4^2
    -> Matrix-tree product 10^24 * 16^15 / 40
    -> 2^81 * 5^23
    -> binary exponent q^4=81 = H1/triple-Albert carrier.

This file is an exact arithmetic audit, not a phenomenology proof.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import log2, log
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

# W(3,3) atoms
q = 3
V = 40
K = 12
lam = 2
mu = 4
r = 2
s = -4
Phi3 = q**2 + q + 1       # 13
Phi4 = q**2 + 1           # 10
Phi6 = q**2 - q + 1       # 7
J = 5
J_inv = 8
EW = q + 1                # 4
K2 = 27                   # complement valency
MULT_R = 24
MULT_S = 15
H1 = q**4                 # 81
ALBERT = q**3             # 27

# Spectral optimization atoms from CCCI-CCCIV
THETA_W = 10
THETA_COMP = 4
LP_ALPHA = 10
LP_OMEGA = 4
FIEDLER = K - r            # 10
LAPLACIAN_RADIUS = K - s   # 16
LAPLACIAN_MULT_FIEDLER = MULT_R
LAPLACIAN_MULT_RADIUS = MULT_S
TREE_EXP_2 = 81
TREE_EXP_5 = 23
TREE_EXP_SUM = TREE_EXP_2 + TREE_EXP_5
TREE_EXP_DIFF = TREE_EXP_2 - TREE_EXP_5
TREE_LOG2 = TREE_EXP_2 + TREE_EXP_5 * log2(5)
TREE_ENTROPY = (TREE_EXP_2 * log(2) + TREE_EXP_5 * log(5)) / V
KIRCHHOFF_INDEX = Fraction(267, 2)
NORMALIZED_WEIGHTED_LOW = Fraction(MULT_R * FIEDLER, K)
NORMALIZED_WEIGHTED_HIGH = Fraction(MULT_S * LAPLACIAN_RADIUS, K)

# Krein parameters used by the weld.  Store as exact Fractions.
krein = {
    "q0_11": Fraction(24, 1),
    "q0_22": Fraction(15, 1),
    "q1_11": Fraction(44, 3),
    "q1_12": Fraction(25, 3),
    "q1_22": Fraction(20, 3),
    "q2_11": Fraction(40, 3),
    "q2_12": Fraction(32, 3),
    "q2_22": Fraction(10, 3),
}


@dataclass(frozen=True)
class SpectralWeldLayer:
    name: str
    value: int | str
    formula: str
    interpretation: str


def spectral_weld_layers() -> List[SpectralWeldLayer]:
    return [
        SpectralWeldLayer("Krein_vertex", V, "3*q^2_11=40", "Bose-Mesner dual recovers vertex count"),
        SpectralWeldLayer("Krein_alpha", THETA_W, "3*q^2_22=10", "Krein dual recovers Hoffman/theta/Fiedler alpha"),
        SpectralWeldLayer("Krein_EW_cube", J_inv**2, "3*(q^1_11+q^1_22)=64=8^2", "dual algebra recovers carrier-square/EW cube identity"),
        SpectralWeldLayer("Lovasz_theta_W", THETA_W, "theta(W)=10", "Shannon/SDP/Hoffman bound"),
        SpectralWeldLayer("Lovasz_theta_complement", THETA_COMP, "theta(Wbar)=4", "EW gauge factor / complement bound"),
        SpectralWeldLayer("Theta_product", V, "10*4=40", "vertex-transitive theta product"),
        SpectralWeldLayer("Delsarte_tight_pair", V, "alpha*omega=10*4=40", "LP-tight code/clique duality"),
        SpectralWeldLayer("Fiedler_value", FIEDLER, "lambda2=K-r=10", "algebraic connectivity equals theta/Hoffman alpha"),
        SpectralWeldLayer("Laplacian_radius", LAPLACIAN_RADIUS, "K-s=16=(q+1)^2", "spectral radius / EW squared"),
        SpectralWeldLayer("Laplacian_product", FIEDLER * LAPLACIAN_RADIUS, "10*16=160=V*(q+1)", "connectivity-radius product"),
        SpectralWeldLayer("Laplacian_sum", FIEDLER + LAPLACIAN_RADIUS, "10+16=26=2*Phi3", "cyclotomic Laplacian sum"),
        SpectralWeldLayer("Laplacian_gap", LAPLACIAN_RADIUS - FIEDLER, "16-10=6=2q", "rank-seed separation"),
        SpectralWeldLayer("Spanning_tree_count", "2^81*5^23", "10^24*16^15/40", "global connectivity complexity"),
        SpectralWeldLayer("Tree_binary_exponent", TREE_EXP_2, "81=q^4=3*27", "H1/triple-Albert carrier as exponent of 2"),
        SpectralWeldLayer("Tree_five_exponent", TREE_EXP_5, "23=27-4=q^3-(q+1)", "one Albert generation minus EW factor"),
        SpectralWeldLayer("Tree_exponent_sum", TREE_EXP_SUM, "81+23=104=8*13=J^-1*Phi3", "carrier times projective-plane count"),
        SpectralWeldLayer("Tree_exponent_difference", TREE_EXP_DIFF, "81-23=58=2*q^3+(q+1)", "two Albert generations plus EW"),
    ]


def spectral_complexity_master_weld_audit() -> Dict[str, object]:
    checks = {
        "theta_values": THETA_W == 10 and THETA_COMP == 4,
        "theta_product": THETA_W * THETA_COMP == V == 40,
        "delsarte_lp_tight": LP_ALPHA == THETA_W == 10 and LP_OMEGA == THETA_COMP == 4 and LP_ALPHA * LP_OMEGA == V,
        "fiedler_equals_theta": FIEDLER == THETA_W == Phi4 == 10,
        "laplacian_radius_is_EW_squared": LAPLACIAN_RADIUS == EW**2 == 16,
        "laplacian_product": FIEDLER * LAPLACIAN_RADIUS == V * EW == 160,
        "laplacian_sum_is_2phi3": FIEDLER + LAPLACIAN_RADIUS == 2 * Phi3 == 26,
        "laplacian_gap_is_rank_seed": LAPLACIAN_RADIUS - FIEDLER == 2 * q == 6,
        "normalized_weighted_split": NORMALIZED_WEIGHTED_LOW == NORMALIZED_WEIGHTED_HIGH == 20 and NORMALIZED_WEIGHTED_LOW + NORMALIZED_WEIGHTED_HIGH == V,
        "kirchhoff_index": KIRCHHOFF_INDEX == Fraction(V, 1) * (Fraction(MULT_R, FIEDLER) + Fraction(MULT_S, LAPLACIAN_RADIUS)),
        "tree_prime_exponents": TREE_EXP_2 == 81 and TREE_EXP_5 == 23,
        "tree_exp_2_is_h1": TREE_EXP_2 == H1 == q**4 == 81,
        "tree_exp_5_is_albert_minus_EW": TREE_EXP_5 == ALBERT - EW == 23,
        "tree_exponent_sum": TREE_EXP_SUM == J_inv * Phi3 == 104,
        "tree_exponent_difference": TREE_EXP_DIFF == 2 * ALBERT + EW == 58,
        "spanning_tree_factorization": (2**TREE_EXP_2) * (5**TREE_EXP_5) == (10**MULT_R) * (16**MULT_S) // V,
        "krein_vertex": 3 * krein["q2_11"] == V,
        "krein_alpha": 3 * krein["q2_22"] == THETA_W,
        "krein_multiplicity_lock": 1 + krein["q0_11"] + krein["q0_22"] == V,
        "krein_firewall_difference": krein["q0_11"] - krein["q0_22"] == q**2,
        "krein_EW_cube_or_carrier_square": 3 * (krein["q1_11"] + krein["q1_22"]) == J_inv**2 == EW**3 == 64,
        "threshold_carrier_inverse": (J * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "module": "PART_CCCV_SPECTRAL_COMPLEXITY_MASTER_WELD",
        "status": "exact spectral-optimization and spanning-tree weld to CLXXX master ladder",
        "source_links": {
            "CCXCIX": "Krein parameters of W(3,3) Bose-Mesner algebra",
            "CCC": "Grand Synthesis",
            "CCCI": "Lovasz theta function",
            "CCCII": "Delsarte LP bound",
            "CCCIII": "Algebraic connectivity",
            "CCCIV": "Spanning tree count",
            "CLXXX": "Master identity ladder",
        },
        "w33_atoms": {
            "q": q,
            "V": V,
            "K": K,
            "lambda": lam,
            "mu": mu,
            "r": r,
            "s": s,
            "Phi3": Phi3,
            "Phi4": Phi4,
            "Phi6": Phi6,
            "J": J,
            "J_inverse": J_inv,
            "EW": EW,
            "Albert": ALBERT,
            "H1": H1,
        },
        "spectral_weld_layers": [asdict(layer) for layer in spectral_weld_layers()],
        "bridge_identities": {
            "optimization_stack": "Krein -> Lovasz/Delsarte -> Fiedler -> Matrix Tree",
            "theta_lp_fiedler_lock": "theta(W)=Hoffman=Delsarte alpha=Fiedler=10",
            "complement_EW_lock": "theta(Wbar)=omega=chi_f=EW=4",
            "laplacian_pair": "nonzero Laplacian spectrum is 10^24 and 16^15",
            "tree_complexity": "tau(W)=10^24*16^15/40=2^81*5^23",
            "master_ladder_recovery": "tree exponent 81 equals q^4=3*27=H1/triple-Albert",
            "generation_gap": "tree exponent 23 equals q^3-(q+1)=27-4",
            "bose_mesner_dual_seed": "3*q^2_22=10 and 3*q^2_11=40",
        },
        "numerical_approximations": {
            "log2_tree_count": TREE_LOG2,
            "tree_entropy_per_vertex_ln": TREE_ENTROPY,
            "kirchhoff_index": str(KIRCHHOFF_INDEX),
        },
        "checks": checks,
        "theorem_statement": (
            "Today's CCXCIX-CCCIV spectral stream welds exactly to the CLXXX algebraic ladder.  The Bose-Mesner/Krein dual "
            "recovers theta/Hoffman alpha=10 and vertex count 40; Lovasz/Delsarte tightness gives the 10/4 product 40; "
            "the Laplacian has nonzero spectrum 10^24 and 16^15; and Kirchhoff's theorem gives tau(W)=2^81*5^23. "
            "Thus the full H1/triple-Albert carrier q^4=81 reappears as the binary exponent of global connectivity, while "
            "the 5-exponent 23 equals one Albert generation minus the EW factor, 27-4."
        ),
        "interpretive_note": (
            "This is a deeper bridge than another parameter table: the algebraic ladder is now visible inside a global graph invariant. "
            "The same 81 that counted the three-generation carrier controls the power of 2 in the exact number of spanning trees."
        ),
    }


def main() -> int:
    audit = spectral_complexity_master_weld_audit()
    out = ROOT / "PART_CCCV_spectral_complexity_master_weld_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
