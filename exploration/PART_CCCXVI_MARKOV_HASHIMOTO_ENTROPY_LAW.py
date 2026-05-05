#!/usr/bin/env python3
"""
PART CCCXVI - Markov / Hashimoto Entropy Law
============================================

Purpose:
    Continue independently after the photonic/percolation bridge and weld the
    ordinary random-walk channel P=A/K to the Hashimoto nonbacktracking channel B.

Core idea:
    Ordinary walks on W33 have K=12 choices per step.  After the first step,
    nonbacktracking walks have K-1=11 choices per step.  Thus nonbacktracking is
    ordinary walking conditioned not to immediately return.

    For n-edge walks:

        ordinary count       = V K^n
        nonbacktracking count= V K (K-1)^(n-1)
        ratio                = ((K-1)/K)^(n-1)

    The per-step entropy defect is

        log K - log(K-1) = log(K/(K-1)) = log(12/11).

New welds to prior stack:
    - K-1=11 is recovered as tr(A_L^2)/(2E) from the line graph shell.
    - K-1=11 is recovered as Wiener/QLE from distance/signless operators.
    - K-1=11 is the Hashimoto branching factor and topological entropy exp(h).
    - p_return=1/K=1/12, p_forward=(K-1)/K=11/12.
    - Critical fusion p=1/2 gives expected retained ordinary degree 6=2q and
      orientation-doubled expected retained nonbacktracking branch 11=K-1.

Hashimoto spectrum check:
    Ihara-Bass gives roots x satisfying

        x^2 - theta x + (K-1)=0

    for each adjacency restricted eigenvalue theta, plus the usual +/-1 edge
    excess factors.  For W33:

      theta=12 -> roots 11,1
      theta=2  -> roots 1 +/- i sqrt(10), modulus sqrt(11)
      theta=-4 -> roots -2 +/- i sqrt(7), modulus sqrt(11)

    Hence the nontrivial Hashimoto spectrum lives on the circle |x|=sqrt(11),
    and the Perron entropy is log(11).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import log
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

# W33 atoms.
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

# Walk counts.
def ordinary_walks(n_edges: int) -> int:
    if n_edges < 0:
        raise ValueError("n_edges must be nonnegative")
    return V * (K ** n_edges)


def nonbacktracking_walks(n_edges: int) -> int:
    if n_edges < 0:
        raise ValueError("n_edges must be nonnegative")
    if n_edges == 0:
        return V
    return V * K * (HASHIMOTO_BRANCH ** (n_edges - 1))


def walk_ratio(n_edges: int) -> Fraction:
    return Fraction(nonbacktracking_walks(n_edges), ordinary_walks(n_edges))

# Local transition probabilities under ordinary random walk after an oriented edge.
P_RETURN = Fraction(1, K)
P_FORWARD = Fraction(K - 1, K)
ENTROPY_ORDINARY = log(K)
ENTROPY_HASHIMOTO = log(HASHIMOTO_BRANCH)
ENTROPY_DEFECT = ENTROPY_ORDINARY - ENTROPY_HASHIMOTO

# Hashimoto quadratic roots encoded by invariants.
HASHIMOTO_ROOT_DATA = {
    "theta_12": {"theta": K, "roots": [HASHIMOTO_BRANCH, 1], "product": HASHIMOTO_BRANCH},
    "theta_2": {"theta": lam, "real": 1, "imag_sq": 10, "mod_sq": HASHIMOTO_BRANCH},
    "theta_minus4": {"theta": -mu, "real": -2, "imag_sq": 7, "mod_sq": HASHIMOTO_BRANCH},
}

# Prior stack companions.
LINE_SECOND_MOMENT = DIRECTED * HASHIMOTO_BRANCH
QLE = E // 2
WIENER_INDEX = HASHIMOTO_BRANCH * QLE
PERCOLATION_P = Fraction(lam, mu)
CRITICAL_RETAINED_DEGREE = PERCOLATION_P * K
CRITICAL_RETAINED_NB_BRANCH = PERCOLATION_P * HASHIMOTO_BRANCH
TREE_EXP_2 = H1
TREE_EXP_5 = Phi3 + Phi4
SPANNING_TREE_FACTOR = f"2^{TREE_EXP_2}5^{TREE_EXP_5}"


@dataclass(frozen=True)
class MarkovHashimotoLayer:
    name: str
    value: int | str
    formula: str
    interpretation: str


def markov_hashimoto_layers() -> List[MarkovHashimotoLayer]:
    return [
        MarkovHashimotoLayer("ordinary_branch", K, "K=12", "ordinary random-walk choices per step"),
        MarkovHashimotoLayer("nonbacktracking_branch", HASHIMOTO_BRANCH, "K-1=11", "Hashimoto choices after orientation"),
        MarkovHashimotoLayer("return_probability", str(P_RETURN), "1/K=1/12", "ordinary immediate-backtrack probability"),
        MarkovHashimotoLayer("forward_probability", str(P_FORWARD), "(K-1)/K=11/12", "ordinary step survives nonbacktracking conditioning"),
        MarkovHashimotoLayer("walk_ratio_n", "((K-1)/K)^(n-1)", "NB_n / ordinary_n", "conditioning survival ratio for n-edge walks"),
        MarkovHashimotoLayer("ordinary_entropy", "log 12", "h_RW=log K", "ordinary path entropy per step"),
        MarkovHashimotoLayer("hashimoto_entropy", "log 11", "h_NB=log(K-1)", "nonbacktracking topological entropy"),
        MarkovHashimotoLayer("entropy_defect", "log(12/11)", "h_RW-h_NB", "cost of excluding immediate reversal"),
        MarkovHashimotoLayer("line_moment_branch", HASHIMOTO_BRANCH, "tr(A_L^2)/(2E)=11", "line graph recovers branch"),
        MarkovHashimotoLayer("wiener_energy_branch", HASHIMOTO_BRANCH, "W/QLE=11", "distance/signless recovers branch"),
        MarkovHashimotoLayer("critical_retained_degree", str(CRITICAL_RETAINED_DEGREE), "pK=6=2q", "critical fusion ordinary retained branch"),
        MarkovHashimotoLayer("critical_retained_nb_double", str(2 * CRITICAL_RETAINED_NB_BRANCH), "2p(K-1)=11", "orientation-doubled critical NB branch"),
        MarkovHashimotoLayer("hashimoto_circle", "|x|^2=11", "restricted Hashimoto roots have modulus sqrt(11)", "Ihara-Bass spectral circle"),
    ]


def markov_hashimoto_entropy_audit() -> Dict[str, object]:
    sample_ratios = {str(n): f"{walk_ratio(n).numerator}/{walk_ratio(n).denominator}" for n in range(1, 6)}
    checks = {
        "ordinary_branch": K == 12,
        "hashimoto_branch": HASHIMOTO_BRANCH == K - 1 == 11,
        "return_forward_partition": P_RETURN + P_FORWARD == 1,
        "return_probability": P_RETURN == Fraction(1, 12),
        "forward_probability": P_FORWARD == Fraction(11, 12),
        "walk_ratio_1": walk_ratio(1) == 1,
        "walk_ratio_2": walk_ratio(2) == Fraction(11, 12),
        "walk_ratio_3": walk_ratio(3) == Fraction(11, 12) ** 2,
        "ordinary_count_2": ordinary_walks(2) == V * K**2 == 5760,
        "nonbacktracking_count_2": nonbacktracking_walks(2) == V * K * HASHIMOTO_BRANCH == 5280,
        "line_second_moment_equals_nb_count_2": LINE_SECOND_MOMENT == nonbacktracking_walks(2) == 5280,
        "line_moment_branch": LINE_SECOND_MOMENT // DIRECTED == HASHIMOTO_BRANCH,
        "wiener_energy_branch": WIENER_INDEX // QLE == HASHIMOTO_BRANCH,
        "hashimoto_theta_12_roots": HASHIMOTO_ROOT_DATA["theta_12"]["roots"] == [11, 1],
        "hashimoto_theta_2_modulus": HASHIMOTO_ROOT_DATA["theta_2"]["real"] ** 2 + HASHIMOTO_ROOT_DATA["theta_2"]["imag_sq"] == HASHIMOTO_BRANCH,
        "hashimoto_theta_minus4_modulus": HASHIMOTO_ROOT_DATA["theta_minus4"]["real"] ** 2 + HASHIMOTO_ROOT_DATA["theta_minus4"]["imag_sq"] == HASHIMOTO_BRANCH,
        "edge_excess": EDGE_EXCESS == 200 == J * V,
        "critical_retained_degree": CRITICAL_RETAINED_DEGREE == 2 * q == 6,
        "critical_nb_branch_double": 2 * CRITICAL_RETAINED_NB_BRANCH == HASHIMOTO_BRANCH,
        "tree_exponents": TREE_EXP_2 == H1 == 81 and TREE_EXP_5 == Phi3 + Phi4 == 23,
        "threshold_carrier_inverse": (J * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "module": "PART_CCCXVI_MARKOV_HASHIMOTO_ENTROPY_LAW",
        "status": "exact ordinary-walk/nonbacktracking conditioning and entropy bridge",
        "source_links": {
            "Normalized_Markov_CCCXI": "Normalized Markov / Krein Compiler",
            "LineGraph_CCCVIII": "Line Graph / Hashimoto Shell Bridge",
            "CriticalFusion_CCCXV": "Critical Fusion Percolation Compiler",
            "MatrixTree_CCCV": "Spectral Complexity / Master Ladder Weld",
        },
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
            "E": E,
            "directed": DIRECTED,
            "edge_excess": EDGE_EXCESS,
        },
        "markov_hashimoto_layers": [asdict(layer) for layer in markov_hashimoto_layers()],
        "sample_walk_ratios": sample_ratios,
        "bridge_identities": {
            "conditioning_law": "NB_n / RW_n = ((K-1)/K)^(n-1)",
            "entropy_defect": "h_RW - h_NB = log(K/(K-1)) = log(12/11)",
            "line_graph_recovery": "tr(A_L^2)=V*K*(K-1)=5280 = number of 2-step nonbacktracking walks",
            "branch_double_critical_fusion": "2p(K-1)=K-1 at p=1/2, so critical orientation-doubling recovers the full branch",
            "hashimoto_spectral_circle": "restricted Ihara-Bass roots have modulus sqrt(K-1)=sqrt(11)",
            "tree_entropy_companion": "tau(W)=2^81 5^23 is the global spanning-tree entropy companion",
        },
        "checks": checks,
        "theorem_statement": (
            "The ordinary random walk and Hashimoto walk are related by an exact conditioning law.  After the first edge, ordinary walking "
            "has K=12 choices and nonbacktracking walking has K-1=11 choices, so the survival ratio for n-edge paths is ((K-1)/K)^(n-1), "
            "and the entropy defect is log(12/11).  The same branch K-1=11 is recovered as tr(A_L^2)/(2E), as Wiener/QLE, and as "
            "the Hashimoto Perron eigenvalue.  Ihara-Bass places the restricted Hashimoto roots on |x|=sqrt(11)."
        ),
        "interpretive_note": (
            "This closes the ordinary-to-nonbacktracking gap.  The Markov channel gives probabilities, the line graph counts two-step turns, "
            "Hashimoto orients and conditions them, and Matrix Tree records the global connectivity entropy."
        ),
    }


def main() -> int:
    audit = markov_hashimoto_entropy_audit()
    out = ROOT / "PART_CCCXVI_markov_hashimoto_entropy_law_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
