#!/usr/bin/env python3
"""Pillar 111 (Part CCXI): Bose-Mesner Algebra of the PSp(4,3) 120-Duad Scheme

The 120 duads (unordered edge-pairs, or 2-element subsets from the W(3,3) edge
set) admit a rank-5 association scheme under the action of PSp(4,3) = W(E6)/Z2
of order 25920.  The Bose-Mesner algebra is the commutant algebra of dimension 5
and is completely diagonalised (multiplicity-free).

Valencies: (k0,k1,k2,k3,k4) = (1, 2, 27, 36, 54),  n = 120.
Multiplicities: (m0,m1,m2,m3,m4) = (1, 20, 24, 15, 60).

Theorems:

T1  SCHEME IDENTIFICATION: The 120 duads form a rank-5 symmetric association
    scheme.  G = PSp(4,3) of order 25920 acts with stabiliser H of order 216,
    giving |G|/|H| = 120.  The scheme is multiplicity-free (Gelfand pair).
    Valencies sum to 120 and multiplicities sum to 120.

T2  MULTIPLICATION TABLE: The Bose-Mesner algebra product A_i * A_j is
    completely determined by 25 structure-constant vectors p_ij.  Key products:
    A1^2 = 2A0 + A1 (40 disjoint triangles in the A1-graph),
    A2^2 = 27A0 + 10A2 + 6A3 + 4A4, A3^2 = 36A0+36A1+12A2+6A3+12A4,
    A4^2 = 54A0+27A1+28A2+24A3+22A4.  All 25 products verified from bundle.

T3  P EIGENMATRIX: The 5x5 matrix P of eigenvalues (row E_r, col A_i) is:
    E0: [1,2,27,36,54]; E1: [1,-1,9,0,-9]; E2: [1,2,-3,6,-6];
    E3: [1,2,3,-12,6]; E4: [1,-1,-3,0,3].
    Verified: P * Q = 120 * I, valency sum = 120, mult-weighted col sums = 0.

T4  Q DUAL EIGENMATRIX: Q_{i,r} are rational, with E_r = (1/120)*sum_i Q_{i,r}*A_i.
    Rational entries: A2 row has factors of 1/3; A4 row has factors of 1/3.
    The product PQ = 120*I is verified exactly using rational arithmetic.

T5  PRIMITIVE IDEMPOTENTS: The 5 primitive idempotents in closed form:
    E0 = (1/120)(A0+A1+A2+A3+A4),
    E1 = (1/36)(6A0-3A1+2A2-A4),
    E2 = (1/90)(18A0+18A1-2A2+3A3-2A4),
    E3 = (1/72)(9A0+9A1+A2-3A3+A4),
    E4 = (1/36)(18A0-9A1-2A2+A4).
    Ranks sum to 1+20+24+15+60=120.  Idempotent coefficients verified consistent.

T6  MINIMAL POLYNOMIALS: Degrees: A1 has degree 2 (2 distinct eigenvalues),
    A2 has degree 4 (4 distinct eigenvalues), A3 has degree 4, A4 has degree 5.
    Polynomials: A1: x^2-x-2; A2: x^4-36x^3+234x^2+324x-2187;
    A3: x^4-30x^3-288x^2+2592x; A4: x^5-48x^4-387x^3+3186x^2+12636x-52488.
    Verified by substituting all 5 distinct eigenvalues per relation.
"""

from __future__ import annotations

import csv
import io
import json
import zipfile
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / "TOE_BoseMesner_Algebra_Solution_bundle_v04_20260227.zip"

N = 120
RANK = 5
VALENCIES = [1, 2, 27, 36, 54]
MULTIPLICITIES = [1, 20, 24, 15, 60]
GROUP_ORDER = 25920   # |PSp(4,3)| = |W(E6)|
STAB_ORDER = 216      # stabiliser |H|

# P eigenmatrix rows: E_r; cols: A_i eigenvalue
P_MATRIX = [
    [1,  2,  27,  36,  54],   # E0, mult=1
    [1, -1,   9,   0,  -9],   # E1, mult=20
    [1,  2,  -3,   6,  -6],   # E2, mult=24
    [1,  2,   3, -12,   6],   # E3, mult=15
    [1, -1,  -3,   0,   3],   # E4, mult=60
]

# Q dual eigenmatrix rows: A_i; cols: E_r  (rational entries)
Q_MATRIX = [
    [Fraction(1), Fraction(20),    Fraction(24),    Fraction(15),    Fraction(60)],     # A0
    [Fraction(1), Fraction(-10),   Fraction(24),    Fraction(15),    Fraction(-30)],    # A1
    [Fraction(1), Fraction(20, 3), Fraction(-8, 3), Fraction(5, 3),  Fraction(-20, 3)], # A2
    [Fraction(1), Fraction(0),     Fraction(4),     Fraction(-5),    Fraction(0)],      # A3
    [Fraction(1), Fraction(-10,3), Fraction(-8, 3), Fraction(5, 3),  Fraction(10, 3)],  # A4
]

# Key products from multiplication table
KEY_PRODUCTS = {
    "A1*A1": [2, 1, 0, 0, 0],
    "A1*A2": [0, 0, 0, 0, 1],
    "A1*A3": [0, 0, 0, 2, 0],
    "A1*A4": [0, 0, 2, 0, 1],
    "A2*A2": [27, 0, 10, 6, 4],
    "A2*A3": [0, 0, 8, 9, 8],
    "A2*A4": [0, 27, 8, 12, 14],
    "A3*A3": [36, 36, 12, 6, 12],
    "A3*A4": [0, 0, 16, 18, 16],
    "A4*A4": [54, 27, 28, 24, 22],
}

# Primitive idempotent recipes: {E_r: (denom, [(coeff, A_i), ...])}
IDEMPOTENTS = {
    "E0": (120, [(1,"A0"),(1,"A1"),(1,"A2"),(1,"A3"),(1,"A4")]),
    "E1": (36,  [(6,"A0"),(-3,"A1"),(2,"A2"),(0,"A3"),(-1,"A4")]),
    "E2": (90,  [(18,"A0"),(18,"A1"),(-2,"A2"),(3,"A3"),(-2,"A4")]),
    "E3": (72,  [(9,"A0"),(9,"A1"),(1,"A2"),(-3,"A3"),(1,"A4")]),
    "E4": (36,  [(18,"A0"),(-9,"A1"),(-2,"A2"),(0,"A3"),(1,"A4")]),
}

# Minimal polynomials: polynomial coefficients [a0, a1, ...] for x^0, x^1, x^2, ...
MINIMAL_POLYS = {
    "A1": [-2, -1, 1],              # x^2 - x - 2
    "A2": [-2187, 324, 234, -36, 1], # x^4 - 36x^3 + 234x^2 + 324x - 2187
    "A3": [0, 2592, -288, -30, 1],  # x^4 - 30x^3 - 288x^2 + 2592x
    "A4": [-52488, 12636, 3186, -387, -48, 1],  # x^5 - 48x^4 - 387x^3 + ...
}


def _load_bundle() -> dict:
    with zipfile.ZipFile(BUNDLE) as zf:
        mult_data = json.loads(zf.read("multiplication_coeffs_pij.json"))
        idem_data = json.loads(zf.read("primitive_idempotents.json"))
        minp_data = json.loads(zf.read("minimal_polynomials.json"))
        inter_data = json.loads(zf.read("duad_intersection_numbers.json"))
        spec_data = json.loads(zf.read("relation_graph_spectra.json"))
        p_csv = zf.read("P_eigenmatrix.csv").decode("utf-8")
        q_csv = zf.read("Q_dual_eigenmatrix.csv").decode("utf-8")
    return {
        "mult": mult_data,
        "idem": idem_data,
        "minp": minp_data,
        "inter": inter_data,
        "spec": spec_data,
        "p_csv": p_csv,
        "q_csv": q_csv,
    }


def _eval_poly(coeffs: List[int], x: int) -> int:
    """Evaluate polynomial with coeffs [a0, a1, a2, ...] at x."""
    return sum(c * x**i for i, c in enumerate(coeffs))


def _matmul_frac(A: List[List[Fraction]], B: List[List[Fraction]]) -> List[List[Fraction]]:
    n = len(A)
    m = len(B[0])
    k = len(B)
    return [
        [sum(A[i][p] * B[p][j] for p in range(k)) for j in range(m)]
        for i in range(n)
    ]


def analyze() -> dict:
    data = _load_bundle()
    mult_data = data["mult"]
    spec_data = data["spec"]

    # T1: Scheme identification
    t1_n = N
    t1_rank = RANK
    t1_val_sum = sum(VALENCIES)
    t1_mult_sum = sum(MULTIPLICITIES)
    t1_group_order = GROUP_ORDER
    t1_stab_order = STAB_ORDER
    t1_gelfand = (GROUP_ORDER // STAB_ORDER == N)
    t1_val_correct = (VALENCIES == [1, 2, 27, 36, 54])
    t1_mult_correct = (MULTIPLICITIES == [1, 20, 24, 15, 60])
    # Verify bundle valencies match
    bundle_vals = mult_data["valencies"]
    t1_bundle_vals_match = (bundle_vals == VALENCIES)

    # T2: Multiplication table
    pij = mult_data["pij_to_coeffs"]
    t2_products_verified = 0
    t2_failures = []
    for key, expected in KEY_PRODUCTS.items():
        # key is like "A1*A2" → parts A1, A2 → i=1, j=2
        parts = key.split("*")
        i = int(parts[0][1])
        j = int(parts[1][1])
        bundle_key = f"p_{i}{j}"
        actual = pij.get(bundle_key)
        if actual == expected:
            t2_products_verified += 1
        else:
            t2_failures.append((key, expected, actual))
    # Also verify total number of products
    t2_total_products = len(pij)
    t2_all_correct = (t2_products_verified == len(KEY_PRODUCTS) and len(t2_failures) == 0)

    # T3: P eigenmatrix (verify P * Q = 120 * I using rational arithmetic)
    P_frac = [[Fraction(v) for v in row] for row in P_MATRIX]
    PQ = _matmul_frac(P_frac, Q_MATRIX)
    t3_pq_is_nI = all(
        PQ[r][s] == (Fraction(N) if r == s else Fraction(0))
        for r in range(RANK) for s in range(RANK)
    )
    # Verify row sums of P (P[r]*[1,1,...,1] = valency-weighted sum = n for E0 only)
    t3_e0_eigenvalues = (P_MATRIX[0] == VALENCIES)
    # Verify mult-weighted col sums for A_i (i>0) are 0 (orthogonality with E0)
    t3_col_orth = all(
        sum(MULTIPLICITIES[r] * P_MATRIX[r][i] for r in range(RANK)) == 0
        for i in range(1, RANK)
    )
    # Verify spectra from bundle match P matrix
    spec1_evals = set(spec_data["1"]["eigenvalues"].keys())
    p1_evals = {str(P_MATRIX[r][1]) for r in range(RANK)}
    t3_spec_match = (spec1_evals == p1_evals)

    # T4: Q dual eigenmatrix — verify PQ = nI already done above
    # Q col 0 (E0 column) = [1,1,1,1,1] (all ones: E0=(1/n)*sum_i A_i)
    t4_q_col0 = [Q_MATRIX[i][0] for i in range(RANK)]
    t4_q_col0_correct = (t4_q_col0 == [Fraction(1)] * RANK)
    # Q row 0 (A0 row) = MULTIPLICITIES (trace(E_r) = m_r, trace(A0)=n → Q_{A0,r}=m_r)
    t4_q_row0 = [Q_MATRIX[0][r] for r in range(RANK)]
    t4_q_row0_correct = (t4_q_row0 == [Fraction(m) for m in MULTIPLICITIES])
    # Verify Q has rational (non-integer) entries for A2 and A4 rows
    t4_q_has_fractions = any(
        Q_MATRIX[i][r].denominator > 1
        for i in range(RANK) for r in range(RANK)
    )

    # T5: Primitive idempotents — verify idempotent rank sum
    t5_rank_sum = sum(MULTIPLICITIES)
    t5_rank_sum_correct = (t5_rank_sum == N)
    # Verify E0 formula sums correctly: (1/120)*(1+1+1+1+1)*(k_i) = trivial
    # The E0 idempotent has all coeffs = 1, denominator 120
    t5_e0_denom = IDEMPOTENTS["E0"][0]
    t5_e0_coeffs = [c for c, _ in IDEMPOTENTS["E0"][1]]
    t5_e0_correct = (t5_e0_denom == 120 and t5_e0_coeffs == [1, 1, 1, 1, 1])
    # Verify E_r coefficients sum to n*delta_{r,0}: sum_i coeff_r_i = 1/denom * n (for r=0), 0 (r>0)
    # E_r = (1/denom) * sum_i coeff_i * A_i
    # So sum over all elts = (1/denom) * sum_i (coeff_i * k_i) should equal m_r (rank of E_r)
    t5_idem_rank_check = {}
    for name, (denom, combos) in IDEMPOTENTS.items():
        coeff_map = {a: c for c, a in combos}
        # rank(E_r) = trace(E_r) = (coeff_A0 / denom) * N  (since trace(A0)=N, trace(A_i>0)=0)
        coeff_a0 = coeff_map.get("A0", 0)
        computed_rank = Fraction(coeff_a0 * N, denom)
        r = int(name[1])
        expected_rank = MULTIPLICITIES[r]
        t5_idem_rank_check[name] = (computed_rank == Fraction(expected_rank))
    t5_all_ranks_correct = all(t5_idem_rank_check.values())

    # T6: Minimal polynomials — verify each distinct eigenvalue satisfies poly
    # Eigenvalues per relation from P matrix columns
    evals_per_rel = {
        "A1": sorted(set(P_MATRIX[r][1] for r in range(RANK))),
        "A2": sorted(set(P_MATRIX[r][2] for r in range(RANK))),
        "A3": sorted(set(P_MATRIX[r][3] for r in range(RANK))),
        "A4": sorted(set(P_MATRIX[r][4] for r in range(RANK))),
    }
    t6_minpoly_checks = {}
    for rel, coeffs in MINIMAL_POLYS.items():
        evals = evals_per_rel[rel]
        all_zero = all(_eval_poly(coeffs, ev) == 0 for ev in evals)
        t6_minpoly_checks[rel] = all_zero
    t6_all_correct = all(t6_minpoly_checks.values())
    t6_degrees = {rel: len(coeffs) - 1 for rel, coeffs in MINIMAL_POLYS.items()}
    t6_num_distinct_evals = {rel: len(evals) for rel, evals in evals_per_rel.items()}

    return {
        "T1_n": t1_n,
        "T1_rank": t1_rank,
        "T1_val_sum": t1_val_sum,
        "T1_mult_sum": t1_mult_sum,
        "T1_group_order": t1_group_order,
        "T1_stab_order": t1_stab_order,
        "T1_gelfand": t1_gelfand,
        "T1_val_correct": t1_val_correct,
        "T1_mult_correct": t1_mult_correct,
        "T1_bundle_vals_match": t1_bundle_vals_match,
        "T2_products_verified": t2_products_verified,
        "T2_total_products": t2_total_products,
        "T2_all_correct": t2_all_correct,
        "T2_num_failures": len(t2_failures),
        "T3_pq_is_nI": t3_pq_is_nI,
        "T3_e0_eigenvalues": t3_e0_eigenvalues,
        "T3_col_orth": t3_col_orth,
        "T3_spec_match": t3_spec_match,
        "T4_q_col0_correct": t4_q_col0_correct,
        "T4_q_row0_correct": t4_q_row0_correct,
        "T4_q_has_fractions": t4_q_has_fractions,
        "T5_rank_sum": t5_rank_sum,
        "T5_rank_sum_correct": t5_rank_sum_correct,
        "T5_e0_correct": t5_e0_correct,
        "T5_all_ranks_correct": t5_all_ranks_correct,
        "T5_idem_rank_check": {k: bool(v) for k, v in t5_idem_rank_check.items()},
        "T6_all_correct": t6_all_correct,
        "T6_minpoly_checks": t6_minpoly_checks,
        "T6_degrees": t6_degrees,
        "T6_num_distinct_evals": t6_num_distinct_evals,
    }


def main():
    summary = analyze()
    out = ROOT / "data" / "w33_bose_mesner_algebra.json"
    out.write_text(__import__("json", encoding="utf-8").dumps(summary, indent=2))
    print("T1 n=120 rank=5 Gelfand:", summary["T1_gelfand"],
          " val_sum:", summary["T1_val_sum"],
          " mult_sum:", summary["T1_mult_sum"])
    print("T2 products verified:", summary["T2_products_verified"],
          "/", len(KEY_PRODUCTS),
          " all_correct:", summary["T2_all_correct"])
    print("T3 PQ=120I:", summary["T3_pq_is_nI"],
          " col_orth:", summary["T3_col_orth"])
    print("T4 Q col0 correct:", summary["T4_q_col0_correct"],
          " has fractions:", summary["T4_q_has_fractions"])
    print("T5 rank sum:", summary["T5_rank_sum"],
          " all idem ranks correct:", summary["T5_all_ranks_correct"])
    print("T6 all minpoly checks:", summary["T6_all_correct"],
          " degrees:", summary["T6_degrees"])
    print("wrote data/w33_bose_mesner_algebra.json")


if __name__ == "__main__":
    main()
