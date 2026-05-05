#!/usr/bin/env python3
"""
PART CCCXVII - Ihara Zeta / Tree Entropy Compiler
=================================================

Purpose:
    Continue independently from CCCXVI and close the bridge between Hashimoto
    nonbacktracking dynamics and Matrix Tree entropy.

Ihara-Bass for a k-regular graph:

    Z_G(u)^(-1) = (1-u^2)^(E-V) det(I - uA + u^2(k-1)I).

For W33:

    k=12, E=240, V=40, E-V=200, k-1=11.

Adjacency spectrum:

    12^1, 2^24, (-4)^15.

Therefore the determinant factor is

    (1 - 12u + 11u^2)
    (1 - 2u + 11u^2)^24
    (1 + 4u + 11u^2)^15.

Breakthrough:
    At u=1, each restricted Ihara quadratic becomes a Laplacian eigenvalue:

        1 - theta + (k-1) = k - theta.

    Hence

        (1 - 2 + 11)^24 (1 + 4 + 11)^15 = 10^24 16^15

    is exactly the reduced Laplacian pseudo-determinant.  Therefore

        tau(W) = 10^24 16^15 / 40 = 2^81 5^23.

Prime-exponent bridge:
    Since 10 = 2*5 and 16 = 2^4,

        e2 = 24 + 4*15 - v2(40) = 24 + 60 - 3 = 81 = q^4.
        e5 = 24 - v5(40)        = 24 - 1      = 23 = Phi3 + Phi4.

Thus the Ihara determinant explains why the spanning-tree count sees both:

        q^4 = 81
        Phi3 + Phi4 = 23.

The Hashimoto spectral circle |x|=sqrt(11) and the Matrix Tree exponents are
not separate facts; they are two evaluations of the same Ihara-Bass polynomial.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

# W33 atoms
q = 3
lam = q - 1
mu = q + 1
V = q**2 * (q**2 + 1)
K = q * (q + 1)
Phi3 = q**2 + q + 1
Phi4 = q**2 + 1
Phi6 = q**2 - q + 1
J = 5
J_inv = 8
H1 = q**4
ALBERT = q**3
E = V * K // 2
DIRECTED = 2 * E
HASHIMOTO_BRANCH = K - 1
EDGE_EXCESS = E - V

# Spectra and multiplicities.
ADJ_SPECTRUM: List[Tuple[int, int]] = [(K, 1), (lam, 24), (-mu, 15)]
LAPLACIAN_SPECTRUM: List[Tuple[int, int]] = [(0, 1), (K - lam, 24), (K + mu, 15)]
RESTRICTED_LAPLACIAN_PRODUCT = (K - lam) ** 24 * (K + mu) ** 15
TREE_COUNT = RESTRICTED_LAPLACIAN_PRODUCT // V
TREE_EXP_2 = 81
TREE_EXP_5 = 23

# Ihara determinant factors at u=1.
IHARA_BRANCH = HASHIMOTO_BRANCH
IHARA_THETA_K_FACTOR_U1 = 1 - K + IHARA_BRANCH  # zero
IHARA_THETA_R_FACTOR_U1 = 1 - lam + IHARA_BRANCH
IHARA_THETA_S_FACTOR_U1 = 1 + mu + IHARA_BRANCH
IHARA_RESTRICTED_PRODUCT_U1 = IHARA_THETA_R_FACTOR_U1 ** 24 * IHARA_THETA_S_FACTOR_U1 ** 15

# Reduced factor around u=1 for the trivial adjacency eigenvalue.
# 1 - Ku + (K-1)u^2 = (1-u)(1-(K-1)u).
TRIVIAL_FACTOR_RESIDUE_U1_ABS = K - 2  # abs(1-(K-1)) = K-2 = 10
SIGNED_TRIVIAL_FACTOR_RESIDUE_U1 = 2 - K
SIGNED_REDUCED_IHARA_LIMIT = SIGNED_TRIVIAL_FACTOR_RESIDUE_U1 * IHARA_RESTRICTED_PRODUCT_U1
ABS_REDUCED_IHARA_LIMIT = abs(SIGNED_REDUCED_IHARA_LIMIT)

# Prime exponent derivation.
V2_OF_V = 3
V5_OF_V = 1
E2_FROM_IHARA_TREE = 24 + 4 * 15 - V2_OF_V
E5_FROM_IHARA_TREE = 24 - V5_OF_V

# Hashimoto root circle.
HASHIMOTO_ROOT_DATA = {
    "theta_12": {"theta": K, "roots": [HASHIMOTO_BRANCH, 1], "product": HASHIMOTO_BRANCH},
    "theta_2": {"theta": lam, "real": 1, "imag_sq": 10, "mod_sq": HASHIMOTO_BRANCH},
    "theta_minus4": {"theta": -mu, "real": -2, "imag_sq": 7, "mod_sq": HASHIMOTO_BRANCH},
}

# Companion identities.
TRIANGLES = V * K * lam // 6
TR_A3 = 6 * TRIANGLES
LINE_SECOND_MOMENT = DIRECTED * HASHIMOTO_BRANCH
SPANNING_TREE_FACTOR = f"2^{TREE_EXP_2}5^{TREE_EXP_5}"


@dataclass(frozen=True)
class IharaTreeLayer:
    name: str
    value: int | str
    formula: str
    interpretation: str


def ihara_tree_layers() -> List[IharaTreeLayer]:
    return [
        IharaTreeLayer("ihara_edge_excess", EDGE_EXCESS, "E-V=240-40=200=5V", "Ihara prefactor exponent"),
        IharaTreeLayer("ihara_branch", IHARA_BRANCH, "K-1=11", "Hashimoto branch / Perron value"),
        IharaTreeLayer("restricted_factor_r", IHARA_THETA_R_FACTOR_U1, "1-r+11=10=Phi4", "Fiedler/Laplacian restricted factor"),
        IharaTreeLayer("restricted_factor_s", IHARA_THETA_S_FACTOR_U1, "1-s+11=16=(q+1)^2", "Laplacian radius restricted factor"),
        IharaTreeLayer("restricted_product", "10^24*16^15", "prod_{theta != K}(K-theta)^mult", "reduced Laplacian pseudo-determinant"),
        IharaTreeLayer("tree_count", SPANNING_TREE_FACTOR, "10^24*16^15/40", "Matrix Tree count from Ihara at u=1"),
        IharaTreeLayer("tree_e2", TREE_EXP_2, "24+4*15-3=81=q^4", "binary exponent from Ihara factors"),
        IharaTreeLayer("tree_e5", TREE_EXP_5, "24-1=23=Phi3+Phi4", "five-exponent from r-multiplicity minus vertex denominator"),
        IharaTreeLayer("trivial_residue", TRIVIAL_FACTOR_RESIDUE_U1_ABS, "abs((1-12u+11u^2)/(1-u)) at u=1 = 10", "trivial Ihara zero residue"),
        IharaTreeLayer("reduced_limit_abs", "400*tau(W)", "10*10^24*16^15", "absolute reduced Ihara limit after removing one (1-u)"),
        IharaTreeLayer("hashimoto_circle", "|x|=sqrt(11)", "x^2-theta x+11=0", "restricted Hashimoto spectral circle"),
    ]


def ihara_zeta_tree_entropy_audit() -> Dict[str, object]:
    checks = {
        "basic_atoms": (q, V, K, E, DIRECTED, HASHIMOTO_BRANCH) == (3, 40, 12, 240, 480, 11),
        "edge_excess": EDGE_EXCESS == E - V == 200 == J * V,
        "adjacency_spectrum": ADJ_SPECTRUM == [(12, 1), (2, 24), (-4, 15)],
        "laplacian_spectrum": LAPLACIAN_SPECTRUM == [(0, 1), (10, 24), (16, 15)],
        "ihara_u1_trivial_zero": IHARA_THETA_K_FACTOR_U1 == 0,
        "ihara_u1_restricted_factors": (IHARA_THETA_R_FACTOR_U1, IHARA_THETA_S_FACTOR_U1) == (Phi4, mu**2) == (10, 16),
        "ihara_restricted_product_equals_laplacian_pseudodet": IHARA_RESTRICTED_PRODUCT_U1 == RESTRICTED_LAPLACIAN_PRODUCT,
        "tree_count": TREE_COUNT == 2**81 * 5**23,
        "matrix_tree": RESTRICTED_LAPLACIAN_PRODUCT == V * TREE_COUNT,
        "tree_e2_from_ihara": E2_FROM_IHARA_TREE == H1 == 81,
        "tree_e5_from_ihara": E5_FROM_IHARA_TREE == Phi3 + Phi4 == 23,
        "trivial_factor_residue": TRIVIAL_FACTOR_RESIDUE_U1_ABS == K - 2 == Phi4 == 10,
        "signed_reduced_limit": SIGNED_REDUCED_IHARA_LIMIT == -(K - 2) * RESTRICTED_LAPLACIAN_PRODUCT,
        "abs_reduced_limit": ABS_REDUCED_IHARA_LIMIT == (K - 2) * V * TREE_COUNT == 400 * TREE_COUNT,
        "hashimoto_theta_12_roots": HASHIMOTO_ROOT_DATA["theta_12"]["roots"] == [11, 1],
        "hashimoto_theta_2_circle": HASHIMOTO_ROOT_DATA["theta_2"]["real"] ** 2 + HASHIMOTO_ROOT_DATA["theta_2"]["imag_sq"] == HASHIMOTO_BRANCH,
        "hashimoto_theta_minus4_circle": HASHIMOTO_ROOT_DATA["theta_minus4"]["real"] ** 2 + HASHIMOTO_ROOT_DATA["theta_minus4"]["imag_sq"] == HASHIMOTO_BRANCH,
        "line_second_moment": LINE_SECOND_MOMENT == DIRECTED * HASHIMOTO_BRANCH == 5280,
        "triangle_trace": TR_A3 == 960,
        "threshold_carrier_inverse": (J * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "module": "PART_CCCXVII_IHARA_ZETA_TREE_ENTROPY_COMPILER",
        "status": "exact Ihara-Bass bridge from Hashimoto spectrum to Matrix Tree factorization",
        "w33_atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "V": V,
            "K": K,
            "Phi3": Phi3,
            "Phi4": Phi4,
            "Phi6": Phi6,
            "J": J,
            "J_inverse": J_inv,
            "H1": H1,
            "Albert": ALBERT,
            "E": E,
            "directed": DIRECTED,
            "Hashimoto_branch": HASHIMOTO_BRANCH,
            "edge_excess": EDGE_EXCESS,
        },
        "ihara_factorization": {
            "reciprocal_zeta": "(1-u^2)^200(1-12u+11u^2)(1-2u+11u^2)^24(1+4u+11u^2)^15",
            "restricted_at_u1": "10^24*16^15",
            "matrix_tree": "tau(W)=10^24*16^15/40=2^81*5^23",
        },
        "ihara_tree_layers": [asdict(layer) for layer in ihara_tree_layers()],
        "bridge_identities": {
            "u1_laplacian": "1-theta+(K-1)=K-theta, so Ihara restricted factors at u=1 are Laplacian eigenvalues",
            "tree_pseudodeterminant": "restricted Ihara determinant at u=1 equals reduced Laplacian pseudo-determinant 10^24*16^15",
            "tree_e2": "e2=24+4*15-v2(40)=81=q^4",
            "tree_e5": "e5=24-v5(40)=23=Phi3+Phi4",
            "hashimoto_circle": "restricted Hashimoto roots lie on |x|=sqrt(11)",
            "reduced_limit": "removing the simple (1-u) zero gives absolute limit 400*tau(W)",
        },
        "checks": checks,
        "theorem_statement": (
            "Ihara-Bass is the missing bridge between Hashimoto dynamics and Matrix Tree entropy.  The W33 reciprocal zeta determinant "
            "has restricted factors (1-2u+11u^2)^24 and (1+4u+11u^2)^15.  Evaluating these factors at u=1 gives 10^24*16^15, "
            "exactly the reduced Laplacian pseudo-determinant.  Dividing by V=40 gives tau(W)=2^81*5^23.  The exponent 81 is "
            "24+4*15-v2(40), while 23 is 24-v5(40)=Phi3+Phi4."
        ),
        "interpretive_note": (
            "The Hashimoto spectral circle and the spanning-tree factorization are two faces of the same Ihara-Bass polynomial.  "
            "Nonbacktracking dynamics supplies the quadratic factors; the u=1 specialization turns them into Laplacian eigenvalues and tree entropy."
        ),
    }


def main() -> int:
    audit = ihara_zeta_tree_entropy_audit()
    out = ROOT / "PART_CCCXVII_ihara_zeta_tree_entropy_compiler_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
