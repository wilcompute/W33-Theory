#!/usr/bin/env python3
"""Pass 171: the binary rank ladder of W(3,q) extended to even q.

The parallel Levi track proved (and Lean-formalized) for odd prime powers:

  rank_2 M_q   = (q(q+1)^2 + 2)/2,
  rank_2 A_P   = q(q^2+1)/2 + 1,
  rank_2 A_L   = q^2 + 1,

with M_q the binary point-line incidence of W(3,q), A_P = M M^T mod 2,
A_L = M^T M mod 2.  For even q the quadrangle W(3,q) is SELF-dual, so
A_P and A_L are conjugate and the two Gram formulas cannot both survive
(they agree only at q = 1).  This witness computes the exact ranks at
q = 2, 3, 4, 5, 8 -- both even values from scratch over GF(4), GF(8) --
and records which formulas extend, handing the even-q behaviour to the
Lean track as data.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT = ROOT / "data" / "w33_pass171_even_q_rank_ladder.json"

FIELD_POLYS = {4: 0b111, 8: 0b1011, 16: 0b10011}  # x^2+x+1, x^3+x+1, x^4+x+1


def field_tables(q):
    """Addition and multiplication tables for GF(q), q in {2,3,4,5,8}."""
    if q in (2, 3, 5, 7, 11, 13):  # prime fields
        add = [[(a + b) % q for b in range(q)] for a in range(q)]
        mul = [[(a * b) % q for b in range(q)] for a in range(q)]
        neg = [(-a) % q for a in range(q)]
        return add, mul, neg
    poly = FIELD_POLYS[q]
    bits = q.bit_length() - 1

    def gf_mul(a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & q:
                a ^= poly
        return result

    add = [[a ^ b for b in range(q)] for a in range(q)]
    mul = [[gf_mul(a, b) for b in range(q)] for a in range(q)]
    neg = list(range(q))  # characteristic 2
    return add, mul, neg


def build_w3q(q):
    add, mul, neg = field_tables(q)
    inverse = {a: next(b for b in range(1, q) if mul[a][b] == 1) for a in range(1, q)}

    def normalize(v):
        for x in v:
            if x:
                inv = inverse[x]
                return tuple(mul[inv][y] for y in v)
        return None

    vectors = [
        (a, b, c, d)
        for a in range(q)
        for b in range(q)
        for c in range(q)
        for d in range(q)
        if (a, b, c, d) != (0, 0, 0, 0)
    ]
    points = sorted({normalize(v) for v in vectors})

    def symp(x, y):
        t1 = mul[x[0]][y[2]]
        t2 = mul[x[2]][y[0]]
        t3 = mul[x[1]][y[3]]
        t4 = mul[x[3]][y[1]]
        return add[add[t1][neg[t2]]][add[t3][neg[t4]]]

    index = {p: n for n, p in enumerate(points)}
    n_points = len(points)
    lines = set()
    for a in range(n_points):
        for b in range(a + 1, n_points):
            if symp(points[a], points[b]):
                continue
            line = set()
            for s in range(q):
                combo = tuple(add[points[a][k]][mul[s][points[b][k]]] for k in range(4))
                line.add(index[normalize(combo)])
            line.add(index[points[b]])
            lines.add(frozenset(line))
    return points, sorted(lines, key=sorted)


def f2_rank(matrix):
    work = matrix.astype(np.uint8).copy()
    rows, cols = work.shape
    rank = 0
    for col in range(cols):
        pivot = None
        for r in range(rank, rows):
            if work[r, col]:
                pivot = r
                break
        if pivot is None:
            continue
        work[[rank, pivot]] = work[[pivot, rank]]
        mask = work[:, col].copy().astype(bool)
        mask[rank] = False
        work[mask] ^= work[rank]
        rank += 1
        if rank == rows:
            break
    return rank


def main():
    checks = {}
    table = {}
    for q in (2, 3, 4, 5, 8):
        points, lines = build_w3q(q)
        v_expected = (q + 1) * (q * q + 1)
        checks[f"q{q}_point_count"] = len(points) == v_expected
        checks[f"q{q}_line_count"] = len(lines) == v_expected
        per_line = {len(line) for line in lines}
        checks[f"q{q}_points_per_line"] = per_line == {q + 1}

        incidence = np.zeros((len(lines), len(points)), dtype=np.uint8)
        for row, line in enumerate(lines):
            for p in line:
                incidence[row, p] = 1

        rank_m = f2_rank(incidence % 2)
        a_p = (incidence.T.astype(np.int64) @ incidence.astype(np.int64)) % 2
        a_l = (incidence.astype(np.int64) @ incidence.T.astype(np.int64)) % 2
        rank_ap = f2_rank(a_p.astype(np.uint8))
        rank_al = f2_rank(a_l.astype(np.uint8))

        formula_m = (q * (q + 1) ** 2 + 2) // 2
        formula_ap = q * (q * q + 1) // 2 + 1
        formula_al = q * q + 1

        table[str(q)] = {
            "points": len(points),
            "rank2_M": int(rank_m),
            "formula_M": formula_m,
            "M_formula_holds": rank_m == formula_m,
            "rank2_AP": int(rank_ap),
            "formula_AP": formula_ap,
            "AP_formula_holds": rank_ap == formula_ap,
            "rank2_AL": int(rank_al),
            "formula_AL": formula_al,
            "AL_formula_holds": rank_al == formula_al,
            "self_dual": q % 2 == 0,
        }
        checks[f"q{q}_ranks_computed"] = rank_m > 0

    # the odd-q theorem re-verified independently at q = 3, 5
    checks["odd_q_theorem_reverified"] = all(
        table[str(q)]["M_formula_holds"]
        and table[str(q)]["AP_formula_holds"]
        and table[str(q)]["AL_formula_holds"]
        for q in (3, 5)
    )
    checks["even_self_duality_verified"] = all(
        table[str(q)]["rank2_AP"] == table[str(q)]["rank2_AL"]
        for q in (2, 4, 8)
    )
    checks["even_AL_formula_survives"] = all(
        table[str(q)]["AL_formula_holds"] for q in (2, 4, 8)
    )
    checks["even_M_odd_formula_not_universal"] = (
        table["2"]["M_formula_holds"]
        and not table["4"]["M_formula_holds"]
        and not table["8"]["M_formula_holds"]
    )
    checks["even_AP_odd_formula_fails"] = all(
        not table[str(q)]["AP_formula_holds"] for q in (2, 4, 8)
    )

    # the even-q incidence rank fits the cubic (q^3 + 12q - 12)/2 at the
    # three anchors; test the conjecture at a fourth anchor q = 16
    def even_conjecture(q):
        return (q**3 + 12 * q - 12) // 2

    checks["even_cubic_fits_2_4_8"] = all(
        table[str(q)]["rank2_M"] == even_conjecture(q) for q in (2, 4, 8)
    )
    points16, lines16 = build_w3q(16)
    checks["q16_point_count"] = len(points16) == 17 * 257
    incidence16 = np.zeros((len(lines16), len(points16)), dtype=np.uint8)
    for row, line in enumerate(lines16):
        for p in line:
            incidence16[row, p] = 1
    rank16 = f2_rank(incidence16)
    table["16"] = {
        "points": len(points16),
        "rank2_M": int(rank16),
        "even_cubic_prediction": even_conjecture(16),
        "even_cubic_holds": rank16 == even_conjecture(16),
    }
    checks["q16_rank_exact_1890"] = rank16 == 1890
    checks["even_cubic_refuted_at_q16"] = rank16 != even_conjecture(16)

    even_verdict = {
        "M_extends": all(table[str(q)]["M_formula_holds"] for q in (2, 4, 8)),
        "AP_extends": all(table[str(q)]["AP_formula_holds"] for q in (2, 4, 8)),
        "AL_extends": all(table[str(q)]["AL_formula_holds"] for q in (2, 4, 8)),
        "AP_equals_AL_by_self_duality": all(
            table[str(q)]["rank2_AP"] == table[str(q)]["rank2_AL"] for q in (2, 4, 8)
        ),
    }

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass171.even_q_rank_ladder.v1",
        "status": "PASS" if all_pass else "FAIL",
        "table": table,
        "even_q_verdict": even_verdict,
        "reading": (
            "the odd-q Levi rank theorem is reverified at q=3,5; for "
            "even q the self-duality of W(3,q) forces rank A_P = rank A_L, "
            "the A_L formula survives at q=2,4,8 while the odd-q incidence "
            "formula only coincides accidentally at q=2 and the A_P formula "
            "fails.  The q=16 rank 1890 also refutes the "
            "cubic interpolant through q=2,4,8; these are anchor data, not "
            "an even-q closed form"
        ),
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
