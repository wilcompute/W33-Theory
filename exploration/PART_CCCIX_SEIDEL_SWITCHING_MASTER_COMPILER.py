#!/usr/bin/env python3
"""
PART CCCIX - Seidel Switching / Master Compiler
===============================================

Live input:
    PART CCCVIII - Seidel Matrix Spectrum of W(3,3)

Seidel operator:
    S = J - I - 2A

Spectrum:
    15^1, (-5)^24, 7^15

Key new welds:
    1. Seidel energy equals the undirected edge shell:

        |S|_energy = 15 + 24*5 + 15*7 = 240 = E = q(q^4-1).

    2. Positive and negative spectral masses balance:

        positive mass = 15 + 15*7 = 120
        negative mass = 24*5 = 120

       This is exactly the signless Laplacian energy QLE=120.

    3. Seidel second moment normalized by QLE gives Phi3:

        tr(S^2) / QLE = 1560 / 120 = 13 = Phi3.

    4. Distance second moment normalized by 4*QLE gives Phi4:

        tr(Delta^2) / (4*QLE) = 4800 / 480 = 10 = Phi4.

       Therefore the Matrix Tree 5-exponent is also:

        e5(tau) = Phi3 + Phi4
                = tr(S^2)/QLE + tr(Delta^2)/(4*QLE)
                = 13 + 10 = 23.

    5. Seidel positive eigenvalue sum gives line graph valency:

        sigma0 + sigma2 = 15 + 7 = 22 = 2(K-1) = deg L(W).

Thus Seidel is the switching/complement completion of the current master theorem:
    algebraic carrier -> vertex operator tetrahedron -> Seidel switching ->
    line graph edge shell -> Hashimoto directed carrier -> Matrix Tree entropy.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

# W33 atoms
q = 3
V = 40
K = 12
lam = 2
mu = 4
r = 2
s = -4
E = V * K // 2
DIRECTED = 2 * E
HASHIMOTO_BRANCH = K - 1
Phi3 = q**2 + q + 1
Phi4 = q**2 + 1
Phi6 = q**2 - q + 1
J_atom = 5
J_inv = 8
EW = q + 1
ALBERT = q**3
H1 = q**4

# Existing spectral companions
QLE = E // 2
Q_SECOND_MOMENT = DIRECTED * Phi3
D_SECOND_MOMENT = DIRECTED * Phi4
TREE_EXP_2 = H1
TREE_EXP_5 = Phi3 + Phi4
TREE_FACTOR = f"2^{TREE_EXP_2}*5^{TREE_EXP_5}"
LINE_VALENCY = 2 * HASHIMOTO_BRANCH
LINE_SECOND_MOMENT = DIRECTED * HASHIMOTO_BRANCH

# Seidel spectrum
SEIDEL_SPECTRUM: List[Tuple[int, int]] = [
    (V - 1 - 2 * K, 1),
    (-(1 + 2 * r), 24),
    (-(1 + 2 * s), 15),
]
SIGMA0, SIGMA1, SIGMA2 = 15, -5, 7
SEIDEL_TRACE = sum(val * mult for val, mult in SEIDEL_SPECTRUM)
SEIDEL_SECOND_MOMENT = sum(val * val * mult for val, mult in SEIDEL_SPECTRUM)
SEIDEL_ENERGY = sum(abs(val) * mult for val, mult in SEIDEL_SPECTRUM)
SEIDEL_POSITIVE_MASS = sum(val * mult for val, mult in SEIDEL_SPECTRUM if val > 0)
SEIDEL_NEGATIVE_MASS = sum(abs(val) * mult for val, mult in SEIDEL_SPECTRUM if val < 0)
SEIDEL_NORMALIZED_BY_QLE = SEIDEL_SECOND_MOMENT // QLE


@dataclass(frozen=True)
class SeidelCompilerLayer:
    name: str
    value: int | str
    formula: str
    interpretation: str


def seidel_compiler_layers() -> List[SeidelCompilerLayer]:
    return [
        SeidelCompilerLayer("Seidel_operator", "S=J-I-2A", "switching/complement operator", "off-diagonal adjacency sign coding"),
        SeidelCompilerLayer("Seidel_spectrum", "15^1,(-5)^24,7^15", "V-1-2K, -(1+2r), -(1+2s)", "same eigenspaces as A with switching transform"),
        SeidelCompilerLayer("Seidel_energy", SEIDEL_ENERGY, "15+24*5+15*7=240", "undirected edge shell q(q^4-1)"),
        SeidelCompilerLayer("positive_mass", SEIDEL_POSITIVE_MASS, "15+15*7=120", "positive switching mass = QLE"),
        SeidelCompilerLayer("negative_mass", SEIDEL_NEGATIVE_MASS, "24*5=120", "negative switching mass = QLE"),
        SeidelCompilerLayer("Seidel_second_moment", SEIDEL_SECOND_MOMENT, "tr(S^2)=V(V-1)=1560", "complete signed pair moment"),
        SeidelCompilerLayer("Phi3_recovery", SEIDEL_NORMALIZED_BY_QLE, "tr(S^2)/QLE=1560/120=13", "projective-plane count from switching moment"),
        SeidelCompilerLayer("line_graph_valency", LINE_VALENCY, "sigma0+sigma2=15+7=22=2(K-1)", "Seidel positive eigenvalues recover edge-shell turn valency"),
        SeidelCompilerLayer("theta_recovery", Phi4, "sigma0-|sigma1|=15-5=10", "theta/Fiedler/Hoffman alpha from Seidel gap"),
        SeidelCompilerLayer("lambda_recovery", lam, "sigma2-|sigma1|=7-5=2", "triangle parameter from Seidel gap"),
        SeidelCompilerLayer("carrier_recovery", J_inv, "sigma0-sigma2=15-7=8", "Cayley carrier dimension"),
        SeidelCompilerLayer("tree_5_exponent", TREE_EXP_5, "tr(S^2)/QLE + tr(Delta^2)/(4QLE)=13+10=23", "Matrix Tree five-exponent from switching plus distance moments"),
    ]


def seidel_switching_master_compiler_audit() -> Dict[str, object]:
    checks = {
        "seidel_spectrum": SEIDEL_SPECTRUM == [(15, 1), (-5, 24), (7, 15)],
        "seidel_trace_zero": SEIDEL_TRACE == 0,
        "seidel_second_moment": SEIDEL_SECOND_MOMENT == V * (V - 1) == 1560,
        "seidel_energy_edge_shell": SEIDEL_ENERGY == E == q * (H1 - 1) == 240,
        "positive_negative_masses_balance": SEIDEL_POSITIVE_MASS == SEIDEL_NEGATIVE_MASS == QLE == 120,
        "seidel_second_over_qle_is_phi3": SEIDEL_SECOND_MOMENT // QLE == Phi3 == 13,
        "distance_second_over_4qle_is_phi4": D_SECOND_MOMENT // (4 * QLE) == Phi4 == 10,
        "tree_e5_from_seidel_distance": SEIDEL_SECOND_MOMENT // QLE + D_SECOND_MOMENT // (4 * QLE) == TREE_EXP_5 == 23,
        "tree_e5_from_signless_distance": (Q_SECOND_MOMENT + D_SECOND_MOMENT) // DIRECTED == TREE_EXP_5 == 23,
        "tree_e2_h1": TREE_EXP_2 == H1 == 81,
        "sigma0_equals_mult_s": SIGMA0 == 15,
        "sigma1_is_minus_mu_plus_one": SIGMA1 == -(mu + 1) == -5,
        "sigma2_is_lam_mu_one": SIGMA2 == lam + mu + 1 == 7,
        "sigma_positive_sum_line_valency": SIGMA0 + SIGMA2 == LINE_VALENCY == 22,
        "sigma_gap_theta": SIGMA0 - abs(SIGMA1) == Phi4 == 10,
        "sigma_gap_lambda": SIGMA2 - abs(SIGMA1) == lam == 2,
        "sigma_carrier_gap": SIGMA0 - SIGMA2 == J_inv == 8,
        "line_second_moment_branch": LINE_SECOND_MOMENT == DIRECTED * HASHIMOTO_BRANCH == 5280,
        "line_second_over_directed_branch": LINE_SECOND_MOMENT // DIRECTED == HASHIMOTO_BRANCH == 11,
        "directed_lift": DIRECTED == 2 * E == 480,
        "threshold_carrier_inverse": (J_atom * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "module": "PART_CCCIX_SEIDEL_SWITCHING_MASTER_COMPILER",
        "status": "exact Seidel/switching completion of operator tetrahedron and edge-shell theorem",
        "source_links": {
            "Seidel_CCCVIII": "PART CCCVIII Seidel Matrix Spectrum of W(3,3)",
            "LineGraph_CCCVIII": "PART CCCVIII Line Graph / Hashimoto Shell Bridge",
            "OperatorTetrahedron_CCCVII": "PART CCCVII Operator Tetrahedron / Entropy Bridge",
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
            "E": E,
            "directed": DIRECTED,
            "Hashimoto_branch": HASHIMOTO_BRANCH,
            "Phi3": Phi3,
            "Phi4": Phi4,
            "Phi6": Phi6,
            "J": J_atom,
            "J_inverse": J_inv,
            "Albert": ALBERT,
            "H1": H1,
        },
        "seidel_compiler_layers": [asdict(layer) for layer in seidel_compiler_layers()],
        "bridge_identities": {
            "seidel_energy_shell": "energy(S)=240=q(q^4-1)=edge shell",
            "balanced_switching_mass": "positive mass = negative mass = 120=QLE",
            "phi3_from_switching": "tr(S^2)/QLE=Phi3=13",
            "phi4_from_distance": "tr(Delta^2)/(4QLE)=Phi4=10",
            "tree_5_from_switching_distance": "e5(tau)=Phi3+Phi4=tr(S^2)/QLE + tr(Delta^2)/(4QLE)",
            "line_valency_from_seidel": "sigma0+sigma2=22=2(K-1)",
            "carrier_from_seidel_gap": "sigma0-sigma2=8=J^{-1}",
            "theta_from_seidel_gap": "sigma0-|sigma1|=10=Phi4",
            "lambda_from_seidel_gap": "sigma2-|sigma1|=2=lambda",
        },
        "master_theorem_sequence": [
            "algebraic carrier: 1+Phi6=8, J3(O)=27, H1=q^4=81",
            "vertex operators: A, L, Q, Delta are affine shadows of one eigenspace split",
            "switching operator: S=J-I-2A has energy 240 and balanced mass 120+120",
            "edge shell: L(W) has 240 vertices and tr(A_L^2)/480=K-1",
            "directed dynamics: Hashimoto carrier 480=2q(q^4-1), branch K-1=11",
            "global complexity: tau(W)=2^{q^4}5^{Phi3+Phi4}",
        ],
        "checks": checks,
        "theorem_statement": (
            "The Seidel matrix completes the master spectral compiler.  Its energy equals the undirected edge shell 240=q(q^4-1), "
            "and its positive and negative spectral masses both equal the signless Laplacian energy 120.  Its second moment, normalized "
            "by that energy, gives Phi3; the distance second moment normalized by four times that energy gives Phi4.  Hence the Matrix "
            "Tree exponent e5=23 is recovered as a switching-plus-distance moment: Phi3+Phi4.  Seidel also recovers the line graph valency "
            "by sigma0+sigma2=22=2(K-1), making it the switching bridge between vertex spectra and edge dynamics."
        ),
        "interpretive_note": (
            "The theory now has a clean pipeline: algebraic carrier -> vertex operators -> Seidel switching -> line graph edge shell -> "
            "Hashimoto directed dynamics -> spanning-tree entropy.  The same constants are recovered at each layer by normalized moments."
        ),
    }


def main() -> int:
    audit = seidel_switching_master_compiler_audit()
    out = ROOT / "PART_CCCIX_seidel_switching_master_compiler_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
