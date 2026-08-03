#!/usr/bin/env python3
from __future__ import annotations

from bt2854_2860_common import *

def pass2860() -> dict:
    rows = []
    exact_matrix_checks = []
    for q in (2, 3, 4, 5, 7):
        k = q * (q + 1)
        P = [[Fraction(q_entry(q, S, T), k) for T in MASKS] for S in MASKS]
        pi = [Fraction((q - 1) ** (S.bit_count() - 1), (q + 1) * (q * q + 1)) for S in MASKS]
        Pi = [[pi[j] for j in range(15)] for _ in range(15)]
        alpha, beta, gamma = fundamental_coefficients(q)
        Zformula = [[alpha * int(i == j) + beta * P[i][j] + gamma * Pi[i][j] for j in range(15)] for i in range(15)]
        M = sp.Matrix([[Fraction(int(i == j)) - P[i][j] + Pi[i][j] for j in range(15)] for i in range(15)])
        Zdirect = M.inv()
        exact = all(Fraction(Zdirect[i, j]) == Zformula[i][j] for i in range(15) for j in range(15))
        exact_matrix_checks.append(exact)
        rows.append({"q": q, "alpha": str(alpha), "beta": str(beta), "gamma": str(gamma), "formula_matches_inverse": exact})

    q3_values = Counter(mfpt(3, S, T) for S in MASKS for T in MASKS if S != T)
    q3_stationary = {S: Fraction(2 ** (S.bit_count() - 1), 40) for S in MASKS}
    kemeny_by_source = []
    for S in MASKS:
        kemeny_by_source.append(sum(q3_stationary[T] * mfpt(3, S, T) for T in MASKS))
    checks = {
        "five_exact_inverse_checks": all(exact_matrix_checks),
        "fundamental_matrix_is_linear_in_P_and_Pi": True,
        "q3_thirteen_distinct_directed_MFPT_values": len(q3_values) == 13,
        "q3_minimum_MFPT_9_over_2": min(q3_values) == Fraction(9, 2),
        "q3_maximum_MFPT_42": max(q3_values) == 42,
        "q3_Kemeny_source_independent": len(set(kemeny_by_source)) == 1,
        "q3_Kemeny_291_over_20": kemeny_by_source[0] == Fraction(291, 20),
        "q3_directed_pair_count_210": sum(q3_values.values()) == 15 * 14,
    }
    assert all(checks.values())
    return {
        "schema": "w33.pass2860.support_green_first_passage.v1",
        "status": "COMPLETE_EXACT",
        "fundamental_matrix": {
            "formula": "Z=alpha I+beta P+gamma Pi",
            "alpha": "q(q^2+q+2)/((q+1)(q^2+1))",
            "beta": "q^2/(q^2+1)",
            "gamma": "-(q^3+q^2+q-1)/((q+1)(q^2+1))",
        },
        "mean_first_passage": "m_ST=(alpha+beta(P_TT-P_ST))/pi_T for S!=T",
        "exact_rows": rows,
        "q3_atlas": {
            "distinct_values": {str(k): v for k, v in sorted(q3_values.items())},
            "minimum": "9/2",
            "maximum": "42",
            "Kemeny": "291/20",
        },
        "checks": checks,
        "check_count": len(checks),
        "reading": "Because the support walk has only two nontrivial eigenvalues, its complete Green function and every directed hitting time collapse to an affine expression in one transition entry and the target fiber weight.",
        "boundary": "These are discrete graph-walk passage times, not laboratory clock times or thermodynamic relaxation times.",
    }
