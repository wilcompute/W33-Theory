#!/usr/bin/env python3
"""Pass 2799: exact transpose/time-reversal construction at q=5 and q=7."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def mm(a, b, q):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n)) % q for j in range(n)) for i in range(n))


def transpose(a):
    return tuple(zip(*a))


def identity(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def inv(a, q):
    n = len(a)
    aug = [list(a[i]) + [int(i == j) for j in range(n)] for i in range(n)]
    row = 0
    for column in range(n):
        pivot = next(i for i in range(row, n) if aug[i][column] % q)
        aug[row], aug[pivot] = aug[pivot], aug[row]
        scale = pow(aug[row][column], -1, q)
        aug[row] = [(scale * x) % q for x in aug[row]]
        for i in range(n):
            if i != row and aug[i][column] % q:
                factor = aug[i][column] % q
                aug[i] = [(aug[i][j] - factor * aug[row][j]) % q for j in range(2 * n)]
        row += 1
    return tuple(tuple(line[n:]) for line in aug)


def scalar_matrix(s, a, q):
    return tuple(tuple(s * x % q for x in row) for row in a)


def group_order_sp4(q):
    return q**4 * (q**2 - 1) * (q**4 - 1)


def verify(q):
    minus = q - 1
    J = ((0, 1, 0, 0), (minus, 0, 0, 0), (0, 0, 0, 1), (0, 0, minus, 0))
    T = ((0, 0, 1, 0), (0, 0, 0, minus), (1, 0, 0, 0), (0, minus, 0, 0))
    cx_pf = ((1, 0, 0, 0), (0, 1, 0, minus), (1, 0, 1, 0), (0, 0, 0, 1))
    cx_fp = ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, minus, 0, 1))
    fp = ((0, minus, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    ff = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, minus), (0, 0, 1, 0))

    t2 = mm(T, T, q)
    multiplier_form = mm(mm(transpose(T), J, q), T, q)
    conjugate = mm(mm(T, cx_pf, q), inv(T, q), q)
    local_fourier = mm(mm(mm(fp, inv(ff, q), q), cx_pf, q), mm(inv(fp, q), ff, q), q)
    roots = [s for s in range(1, q) if s * s % q == minus]
    rescaled = None
    if roots:
        rescaled = scalar_matrix(roots[0], T, q)
        assert mm(mm(transpose(rescaled), J, q), rescaled, q) == J

    checks = {
        "T_squared_identity": t2 == identity(4),
        "multiplier_minus_one": multiplier_form == scalar_matrix(minus, J, q),
        "conjugates_cx_directions": conjugate == cx_fp,
        "local_fourier_identity": local_fourier == cx_fp,
        "minus_one_square_matches_q_mod4": bool(roots) == (q % 4 == 1),
        "projectively_inner_at_q5": (q != 5) or bool(roots),
        "projectively_outer_at_q7": (q != 7) or not roots,
    }
    assert all(checks.values())
    sp_order = group_order_sp4(q)
    return {
        "q": q,
        "q_mod_4": q % 4,
        "minus_one_square_roots": roots,
        "multiplier": -1,
        "Sp4_order": sp_order,
        "PSp4_order": sp_order // 2,
        "classification": "projectively symplectic / inner diagonal class" if roots else "nontrivial PGSp/PSp diagonal outer class",
        "symplectic_rescaling": roots[0] if roots else None,
        "checks": checks,
    }


def main():
    rows = [verify(5), verify(7)]
    checks = {
        "q5_inner": rows[0]["symplectic_rescaling"] == 2,
        "q7_outer": rows[1]["symplectic_rescaling"] is None,
        "q5_order": rows[0]["Sp4_order"] == 9_360_000,
        "q7_order": rows[1]["Sp4_order"] == 276_595_200,
    }
    assert all(checks.values())
    output = {
        "schema": "w33.pass2799.transpose_q5_q7.v1",
        "status": "EXACT",
        "matrix": [[0, 0, 1, 0], [0, 0, 0, -1], [1, 0, 0, 0], [0, -1, 0, 0]],
        "all_odd_q_identity": "T^2=I, T^T J T=-J, and T CX_pf T^-1=CX_fp",
        "criterion": "The projective class is inner exactly when -1 is a square, equivalently q congruent to 1 mod 4; it is the nontrivial diagonal outer class when q congruent to 3 mod 4.",
        "rows": rows,
        "checks": checks,
    }
    path = ROOT / "data/PART_BT2799_TRANSPOSE_Q5_Q7_results.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
