#!/usr/bin/env python3
"""
PART CCCXI - Normalized Markov / Krein Compiler
===============================================

Live inputs:
    PART CCCIX - Normalized Laplacian Spectrum of W(3,3)
    PART CCCX  - Krein Parameters of W(3,3)

Purpose:
    Convert the operator theorem into its probability/dual-association-scheme form.

Breakthrough:
    For W(3,3), the random-walk operator P=A/K has nontrivial eigenvalues

        1/6  and  -1/3.

    Since q=3, these are

        +1/(2q) and -1/q.

    Thus normalized Laplacian dynamics is a q-clock Markov channel:

        L_norm eigenvalues = 0, 1-1/(2q)=5/6, 1+1/q=4/3.

    The two nontrivial normalized eigenvalues encode the same projective/theta
    constants:

        (5/6)+(4/3)=13/6 = Phi3/(2q)
        (5/6)*(4/3)=10/9 = Phi4/q^2
        (4/3)-(5/6)=1/2

    Meanwhile the random-walk square trace gives:

        tr(P^2)=10/3 = Phi4/q.

    This means theta/Fiedler Phi4 is the q-scaled two-step return trace of the
    Markov chain.

Krein weld:
    The Krein algebra already had:

        q^0_11 - q^0_22 = 24 - 15 = 9 = q^2     firewall split
        3 q^2_11 = 40                            vertex count
        3 q^2_22 = 10                            theta/Fiedler/Phi4
        3(q^1_11 + q^1_22) = 64 = 8^2            Cayley carrier square

    CCCXI says the normalized Markov operator is the stochastic shadow of the
    same Krein data: Phi4 is recovered both as 3*q^2_22 and as q*tr(P^2).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

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
Phi3 = q**2 + q + 1
Phi4 = q**2 + 1
Phi6 = q**2 - q + 1
J = 5
J_inv = 8
EW = q + 1
ALBERT = q**3
H1 = q**4
HASHIMOTO_BRANCH = K - 1

# Normalized Laplacian and random-walk spectra.
P_SPECTRUM = [(Fraction(1), 1), (Fraction(r, K), 24), (Fraction(s, K), 15)]
P_NONTRIVIAL_POS = Fraction(r, K)       # 1/6 = 1/(2q)
P_NONTRIVIAL_NEG = Fraction(s, K)       # -1/3 = -1/q
P_TRACE = sum(val * mult for val, mult in P_SPECTRUM)
P_TRACE_SQ = sum((val * val) * mult for val, mult in P_SPECTRUM)
P_TRACE_CUBE = sum((val ** 3) * mult for val, mult in P_SPECTRUM)
P_TRACE_FOURTH = sum((val ** 4) * mult for val, mult in P_SPECTRUM)
P_SLEM = max(abs(P_NONTRIVIAL_POS), abs(P_NONTRIVIAL_NEG))

NL_SPECTRUM = [(Fraction(0), 1), (Fraction(1) - P_NONTRIVIAL_POS, 24), (Fraction(1) - P_NONTRIVIAL_NEG, 15)]
NL_EIG1 = NL_SPECTRUM[1][0]
NL_EIG2 = NL_SPECTRUM[2][0]
NL_TRACE = sum(val * mult for val, mult in NL_SPECTRUM)
NL_TRACE_SQ = sum((val * val) * mult for val, mult in NL_SPECTRUM)
NL_SUM_NONTRIVIAL = NL_EIG1 + NL_EIG2
NL_PROD_NONTRIVIAL = NL_EIG1 * NL_EIG2
NL_DIFF_NONTRIVIAL = NL_EIG2 - NL_EIG1
CHEEGER_LOWER = NL_EIG1 / 2

# Krein data from the live CCCX commit.
KR_11_0 = Fraction(24, 1)
KR_11_1 = Fraction(44, 3)
KR_11_2 = Fraction(40, 3)
KR_12_0 = Fraction(0, 1)
KR_12_1 = Fraction(25, 3)
KR_12_2 = Fraction(32, 3)
KR_22_0 = Fraction(15, 1)
KR_22_1 = Fraction(20, 3)
KR_22_2 = Fraction(10, 3)

KREIN_VERTEX = q * KR_11_2      # 40
KREIN_THETA = q * KR_22_2       # 10
KREIN_FIREWALL = KR_11_0 - KR_22_0  # 9
KREIN_CARRIER_SQUARE = q * (KR_11_1 + KR_22_1)  # 64

# Existing global exponents.
TREE_EXP_2 = H1
TREE_EXP_5 = Phi3 + Phi4


@dataclass(frozen=True)
class NormalizedCompilerLayer:
    name: str
    value: str | int
    formula: str
    interpretation: str


def normalized_compiler_layers() -> List[NormalizedCompilerLayer]:
    return [
        NormalizedCompilerLayer("random_walk_positive_mode", str(P_NONTRIVIAL_POS), "r/K=2/12=1/(2q)", "half-q forward mode"),
        NormalizedCompilerLayer("random_walk_negative_mode", str(P_NONTRIVIAL_NEG), "s/K=-4/12=-1/q", "full q-clock alternating mode"),
        NormalizedCompilerLayer("markov_slem", str(P_SLEM), "max(|1/6|,|-1/3|)=1/q", "stochastic contraction rate"),
        NormalizedCompilerLayer("normalized_gap", str(NL_EIG1), "1-1/(2q)=5/6", "random-walk spectral gap"),
        NormalizedCompilerLayer("normalized_top", str(NL_EIG2), "1+1/q=4/3", "non-bipartite upper normalized Laplacian eigenvalue"),
        NormalizedCompilerLayer("nontrivial_sum", str(NL_SUM_NONTRIVIAL), "5/6+4/3=13/6=Phi3/(2q)", "projective-plane sum channel"),
        NormalizedCompilerLayer("nontrivial_product", str(NL_PROD_NONTRIVIAL), "5/6*4/3=10/9=Phi4/q^2", "theta/Fiedler product channel"),
        NormalizedCompilerLayer("two_step_return_trace", str(P_TRACE_SQ), "tr(P^2)=10/3=Phi4/q", "q-scaled theta return probability"),
        NormalizedCompilerLayer("normalized_second_moment", str(NL_TRACE_SQ), "tr(L_norm^2)=130/3=V+Phi4/q", "normalized Laplacian energy moment"),
        NormalizedCompilerLayer("krein_theta", str(KREIN_THETA), "q*q^2_22=3*(10/3)=10", "dual algebra recovers Phi4/theta"),
        NormalizedCompilerLayer("krein_vertex", str(KREIN_VERTEX), "q*q^2_11=3*(40/3)=40", "dual algebra recovers vertex count"),
        NormalizedCompilerLayer("krein_firewall", str(KREIN_FIREWALL), "q^0_11-q^0_22=24-15=9", "dual multiplicity firewall split"),
        NormalizedCompilerLayer("krein_carrier_square", str(KREIN_CARRIER_SQUARE), "q(q^1_11+q^1_22)=64=8^2", "Cayley carrier square"),
        NormalizedCompilerLayer("tree_entropy_exponents", f"2^{TREE_EXP_2}5^{TREE_EXP_5}", "tau(W)=2^{q^4}5^{Phi3+Phi4}", "global complexity from carrier plus projective/theta moments"),
    ]


def normalized_markov_krein_compiler_audit() -> Dict[str, object]:
    checks = {
        "random_walk_spectrum": P_SPECTRUM == [(Fraction(1), 1), (Fraction(1, 6), 24), (Fraction(-1, 3), 15)],
        "markov_modes_are_q_clock": P_NONTRIVIAL_POS == Fraction(1, 2 * q) and P_NONTRIVIAL_NEG == Fraction(-1, q),
        "p_trace_zero": P_TRACE == 0,
        "p_trace_square_phi4_over_q": P_TRACE_SQ == Fraction(Phi4, q) == Fraction(10, 3),
        "p_trace_cube_triangle_density": P_TRACE_CUBE == Fraction(lam * E * 2 // 3, K**3),
        "p_slem_is_one_over_q": P_SLEM == Fraction(1, q),
        "normalized_laplacian_spectrum": NL_SPECTRUM == [(Fraction(0), 1), (Fraction(5, 6), 24), (Fraction(4, 3), 15)],
        "nl_trace_is_v": NL_TRACE == V == 40,
        "nl_trace_sq": NL_TRACE_SQ == Fraction(130, 3) == Fraction(V) + Fraction(Phi4, q),
        "nl_sum_nontrivial_phi3": NL_SUM_NONTRIVIAL == Fraction(Phi3, 2 * q) == Fraction(13, 6),
        "nl_product_nontrivial_phi4": NL_PROD_NONTRIVIAL == Fraction(Phi4, q**2) == Fraction(10, 9),
        "nl_difference_half": NL_DIFF_NONTRIVIAL == Fraction(1, 2),
        "cheeger_lower": CHEEGER_LOWER == Fraction(J, K) == Fraction(5, 12),
        "krein_vertex": KREIN_VERTEX == V == 40,
        "krein_theta": KREIN_THETA == Phi4 == 10,
        "krein_firewall": KREIN_FIREWALL == q**2 == 9,
        "krein_carrier_square": KREIN_CARRIER_SQUARE == J_inv**2 == 64,
        "krein_q22_matches_markov_return": q * KR_22_2 == q * P_TRACE_SQ == Phi4,
        "tree_exponents": TREE_EXP_2 == H1 == 81 and TREE_EXP_5 == Phi3 + Phi4 == 23,
        "hashimoto_branch": HASHIMOTO_BRANCH == 11,
        "threshold_carrier_inverse": (J * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "module": "PART_CCCXI_NORMALIZED_MARKOV_KREIN_COMPILER",
        "status": "exact probability/dual-association compiler for W(3,3)",
        "source_links": {
            "Normalized_Laplacian_CCCIX": "PART CCCIX Normalized Laplacian Spectrum of W(3,3)",
            "Krein_CCCX": "PART CCCX Krein Parameters of W(3,3)",
            "Seidel_CCCIX": "Seidel switching master compiler",
            "Operator_Tetrahedron_CCCVII": "Operator tetrahedron entropy bridge",
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
            "Phi3": Phi3,
            "Phi4": Phi4,
            "Phi6": Phi6,
            "J": J,
            "J_inverse": J_inv,
            "Albert": ALBERT,
            "H1": H1,
        },
        "normalized_compiler_layers": [asdict(layer) for layer in normalized_compiler_layers()],
        "bridge_identities": {
            "markov_q_clock": "A/K has nontrivial eigenvalues +1/(2q) and -1/q",
            "slem": "second-largest absolute random-walk eigenvalue is 1/q",
            "normalized_sum_product": "5/6+4/3=Phi3/(2q), and (5/6)(4/3)=Phi4/q^2",
            "return_trace": "tr((A/K)^2)=Phi4/q",
            "dual_theta_agreement": "Phi4=q*q^2_22=q*tr(P^2)",
            "dual_firewall": "q^0_11-q^0_22=q^2=9",
            "dual_carrier_square": "q(q^1_11+q^1_22)=8^2",
            "global_entropy": "tau(W)=2^{q^4}5^{Phi3+Phi4}",
        },
        "checks": checks,
        "theorem_statement": (
            "The normalized Laplacian turns the spectral theorem into a q-clock Markov channel.  The random-walk operator A/K has "
            "nontrivial eigenvalues +1/(2q) and -1/q, so its contraction scale is exactly 1/q.  The normalized Laplacian eigenvalues "
            "5/6 and 4/3 have sum Phi3/(2q), product Phi4/q^2, and difference 1/2.  The two-step Markov trace is Phi4/q, matching "
            "the Krein dual identity Phi4=q*q^2_22.  Meanwhile the Krein multiplicity difference q^0_11-q^0_22 gives the q^2 firewall, "
            "and q(q^1_11+q^1_22)=8^2 gives the Cayley carrier square."
        ),
        "interpretive_note": (
            "This converts the latest deterministic operator stack into probability language.  The same constants now appear as Markov rates, "
            "normalized Laplacian moments, and Krein dual structure constants."
        ),
    }


def main() -> int:
    audit = normalized_markov_krein_compiler_audit()
    out = ROOT / "PART_CCCXI_normalized_markov_krein_compiler_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
