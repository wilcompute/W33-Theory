#!/usr/bin/env python3
"""Pass 1033: complete Bose--Mesner algebra of the 120-sheet selector scheme.

Reconstruct the line-phase coset action of PSp(4,3), build all five orbital
relations, and compute exact intersection numbers, eigenmatrices, primitive
idempotent coefficient vectors, multiplicities, and Krein parameters.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

from analysis.w33_pass1031_dual_120_phase_carriers import (
    Perm,
    act_line,
    act_point_matching,
    build_w33,
    compose,
    generate_psp,
    inverse,
    perfect_matchings,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "w33_pass1033_selector_orbital_algebra.json"


def left_cosets(group: set[Perm], subgroup: list[Perm]) -> tuple[list[Perm], dict[Perm, int]]:
    unseen = set(group)
    reps: list[Perm] = []
    element_to_coset: dict[Perm, int] = {}
    hset = set(subgroup)
    while unseen:
        rep = min(unseen)
        coset = {compose(rep, h) for h in hset}
        idx = len(reps)
        reps.append(rep)
        for g in coset:
            element_to_coset[g] = idx
        unseen -= coset
    return reps, element_to_coset


def rational_json(x: sp.Expr) -> int | str:
    x = sp.simplify(x)
    if x.is_Integer:
        return int(x)
    if x.is_Rational:
        return f"{int(x.p)}/{int(x.q)}"
    return str(x)


def matrix_json(M: sp.Matrix) -> list[list[int | str]]:
    return [[rational_json(M[i, j]) for j in range(M.cols)] for i in range(M.rows)]


def main() -> None:
    p1032 = json.loads((DATA / "w33_pass1032_selector_orbital_fusion_shadow.json").read_text())
    design = json.loads((DATA / "w33_BREAKTHROUGH_360_selector_zmin_sheet_design.json").read_text())

    points, lines = build_w33()
    group = generate_psp(points)

    base_line = lines[0]
    line_matchings = perfect_matchings(list(base_line))
    line_stabilizer = [g for g in group if act_line(g, base_line) == base_line]
    H = [g for g in line_stabilizer if act_point_matching(g, line_matchings[0]) == line_matchings[0]]

    reps, element_to_coset = left_cosets(group, H)
    n = len(reps)
    assert n == 120 and len(H) == 216

    unseen = set(range(n))
    orbits: list[list[int]] = []
    while unseen:
        j = min(unseen)
        orbit = sorted({element_to_coset[compose(h, reps[j])] for h in H})
        orbits.append(orbit)
        unseen -= set(orbit)
    orbits.sort(key=lambda o: (len(o), o))
    subdegrees = [len(o) for o in orbits]
    assert subdegrees == [1, 2, 27, 36, 54]
    base_relation = {j: r for r, orbit in enumerate(orbits) for j in orbit}

    relations = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        inv_i = inverse(reps[i])
        for j in range(n):
            relative = compose(inv_i, reps[j])
            relations[i, j] = base_relation[element_to_coset[relative]]

    adjacency = [(relations == r).astype(np.int64) for r in range(5)]
    symmetric = [bool(np.array_equal(A, A.T)) for A in adjacency]
    partition_ok = np.array_equal(sum(adjacency), np.ones((n, n), dtype=np.int64))
    diagonal_ok = np.array_equal(adjacency[0], np.eye(n, dtype=np.int64))
    valencies = [int(A[0].sum()) for A in adjacency]

    p = [[[0 for _k in range(5)] for _j in range(5)] for _i in range(5)]
    closure_ok = True
    for i in range(5):
        for j in range(5):
            product_matrix = adjacency[i] @ adjacency[j]
            reconstructed = np.zeros((n, n), dtype=np.int64)
            for k in range(5):
                vals = set(int(x) for x in product_matrix[relations == k])
                if len(vals) != 1:
                    closure_ok = False
                    value = -1
                else:
                    value = vals.pop()
                p[i][j][k] = value
                reconstructed += value * adjacency[k]
            if not np.array_equal(product_matrix, reconstructed):
                closure_ok = False

    commutative = all(p[i][j] == p[j][i] for i in range(5) for j in range(5))
    L = [sp.Matrix([[p[i][j][k] for k in range(5)] for j in range(5)]) for i in range(5)]
    combo = sum(((i + 1) * L[i] for i in range(5)), sp.zeros(5))
    eigenspaces = combo.eigenvects()
    assert sum(mult for _ev, mult, _vecs in eigenspaces) == 5
    rows: list[list[sp.Expr]] = []
    for _ev, mult, vecs in eigenspaces:
        assert mult == 1 and len(vecs) == 1
        v = vecs[0]
        lambdas: list[sp.Expr] = []
        for Li in L:
            w = Li * v
            pivot = next(t for t in range(5) if v[t] != 0)
            lam = sp.simplify(w[pivot] / v[pivot])
            assert all(sp.simplify(w[t] - lam * v[t]) == 0 for t in range(5))
            lambdas.append(lam)
        rows.append(lambdas)

    trivial = [sp.Integer(k) for k in valencies]
    triv_rows = [r for r in rows if all(sp.simplify(r[i] - trivial[i]) == 0 for i in range(5))]
    assert len(triv_rows) == 1
    others = [r for r in rows if r is not triv_rows[0]]
    others.sort(key=lambda r: tuple(str(sp.simplify(x)) for x in r))
    Pmat = sp.Matrix([triv_rows[0]] + others)
    mvec = Pmat.T.LUsolve(sp.Matrix([n, 0, 0, 0, 0]))
    assert all(x.is_Integer and x > 0 for x in mvec)
    multiplicities = [int(x) for x in mvec]
    Qmat = sp.simplify(n * Pmat.inv())

    Mdiag = sp.diag(*multiplicities)
    Kdiag = sp.diag(*valencies)
    orth1 = sp.simplify(Pmat.T * Mdiag * Pmat - n * Kdiag) == sp.zeros(5)
    orth2 = sp.simplify(Pmat * Kdiag.inv() * Pmat.T - n * Mdiag.inv()) == sp.zeros(5)
    pq_ok = sp.simplify(Pmat * Qmat - n * sp.eye(5)) == sp.zeros(5)

    krein: list[list[list[sp.Expr]]] = []
    krein_nonnegative = True
    for a in range(5):
        row_a = []
        for b in range(5):
            coeffs = []
            for c in range(5):
                value = sp.simplify(sum(Qmat[l, a] * Qmat[l, b] * Pmat[c, l] for l in range(5)) / n)
                coeffs.append(value)
                if value.is_real is not False and value.is_number and value < 0:
                    krein_nonnegative = False
            row_a.append(coeffs)
        krein.append(row_a)
    krein_rational = all(x.is_Rational for aa in krein for bb in aa for x in bb)

    overlap_by_relation = [108, 54, 4, 12, 2]
    expected_profile = {int(k): int(v) for k, v in design["profiles"]["base_sheet_intersections"].items()}
    checks = {
        "source_certificates_pass": p1032["status"] == "PASS" and design["summary"]["all_identities_hold"],
        "group_order_is_25920": len(group) == 25920,
        "phase_stabilizer_order_is_216": len(H) == 216,
        "degree_is_120": n == 120,
        "relations_partition_square": partition_ok,
        "diagonal_relation_is_identity": diagonal_ok,
        "all_relations_are_symmetric": all(symmetric),
        "valencies_are_1_2_27_36_54": valencies == [1, 2, 27, 36, 54],
        "overlap_profile_matches_relations": {overlap_by_relation[i]: valencies[i] for i in range(5)} == expected_profile,
        "intersection_numbers_close_exactly": closure_ok,
        "scheme_is_commutative": commutative,
        "eigenmatrix_is_nonsingular": Pmat.det() != 0,
        "multiplicities_sum_to_120": sum(multiplicities) == 120,
        "multiplicities_are_positive_integers": all(x > 0 for x in multiplicities),
        "PQ_equals_120I": pq_ok,
        "first_orthogonality_relation": orth1,
        "second_orthogonality_relation": orth2,
        "krein_parameters_are_nonnegative": krein_nonnegative,
        "krein_parameters_are_rational": krein_rational,
    }
    if not all(checks.values()):
        raise AssertionError([k for k, v in checks.items() if not v])

    result: dict[str, Any] = {
        "schema": "w33.pass1033.selector_orbital_algebra.python.v1",
        "status": "PASS",
        "headline": "The 120-sheet golden-selector design is a symmetric rank-five association scheme. Its five overlap relations are exactly the five orbitals, and its complete Bose--Mesner algebra, eigenmatrices, primitive-idempotent multiplicities, and Krein parameters are determined exactly.",
        "relation_order": [{"index": i, "overlap": overlap_by_relation[i], "valency": valencies[i]} for i in range(5)],
        "intersection_numbers": p,
        "left_multiplication_matrices": [matrix_json(M) for M in L],
        "first_eigenmatrix_P": matrix_json(Pmat),
        "second_eigenmatrix_Q": matrix_json(Qmat),
        "multiplicities": multiplicities,
        "primitive_idempotents": [{"index": r, "rank": multiplicities[r], "coefficients_in_A_basis": [rational_json(Qmat[i, r] / n) for i in range(5)]} for r in range(5)],
        "krein_parameters": [[[rational_json(x) for x in coeffs] for coeffs in row] for row in krein],
        "checks": checks,
        "check_count": len(checks),
        "boundary": "This is the exact finite orbital algebra. It does not by itself choose a flat selector correction; any correction must be tested as a cochain against the quadrangle boundary operator.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Pass1033 PASS", multiplicities)


if __name__ == "__main__":
    main()
