#!/usr/bin/env python3
"""Passes 5798--5799: heavy-line disjointness is the transpose Reye copy.

Uses the exact Klein chart from Pass5776--5783.  It proves that the 16 Reye
lines and 12 heavy blocks form a second Reye 12_4,16_3 incidence geometry when
incidence means disjointness; matrix transpose is an explicit isomorphism from
the original point-line Reye copy to this heavy-line copy.  It also freezes the
signed cross-incidence partial isometry between the common rank-nine sectors.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "PART_W33_PASS5776_5783_REYE_LATIN_COMMON_CORE.json"
OUTPUT = ROOT / "data" / "PART_W33_PASS5798_5799_REYE_DISJOINTNESS_DUALITY.json"

Vec = tuple[int, int]
Mat = tuple[int, int, int, int]
ZERO: Vec = (0, 0)
E1: Vec = (1, 0)
E2: Vec = (0, 1)
E3: Vec = (1, 1)
VALL: list[Vec] = [ZERO, E2, E1, E3]
NONZERO: list[Vec] = [E1, E2, E3]


def vx(a: Vec, b: Vec) -> Vec:
    return (a[0] ^ b[0], a[1] ^ b[1])


def dot(a: Vec, b: Vec) -> int:
    return (a[0] & b[0]) ^ (a[1] & b[1])


def mv(m: Mat, v: Vec) -> Vec:
    return ((m[0] & v[0]) ^ (m[1] & v[1]), (m[2] & v[0]) ^ (m[3] & v[1]))


def rmul(v: Vec, m: Mat) -> Vec:
    return ((v[0] & m[0]) ^ (v[1] & m[2]), (v[0] & m[1]) ^ (v[1] & m[3]))


def mt(m: Mat) -> Mat:
    return (m[0], m[2], m[1], m[3])


def matrix_from_columns(r: Vec, c: Vec) -> Mat:
    return (r[0], c[0], r[1], c[1])


def transpose(a: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matrix_equal(a: list[list[int]], b: list[list[int]]) -> bool:
    return a == b


def rank_q(a: list[list[int]]) -> int:
    from fractions import Fraction
    m = [[Fraction(x) for x in row] for row in a]
    nr = len(m)
    nc = len(m[0]) if nr else 0
    r = 0
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if m[i][c]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        q = m[r][c]
        m[r] = [x / q for x in m[r]]
        for i in range(nr):
            if i != r and m[i][c]:
                q = m[i][c]
                m[i] = [x - q * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


def main() -> None:
    prev = json.loads(SOURCE.read_text())
    chart = prev["pass_5778_reye_td34_klein_latin"]["explicit_cover_coordinate_chart"]
    assert chart["law"] == "symbol = row XOR column"

    P = [(w, x) for w in NONZERO for x in VALL]
    p_index = {p: i for i, p in enumerate(P)}
    H = [(phi, psi) for phi in NONZERO for psi in VALL]

    line_mats = [matrix_from_columns(r, c) for r in VALL for c in VALL]
    assert len(set(line_mats)) == 16
    line_index = {m: i for i, m in enumerate(line_mats)}
    line_transpose_perm = [line_index[mt(m)] for m in line_mats]
    assert sorted(line_transpose_perm) == list(range(16))
    assert all(line_transpose_perm[line_transpose_perm[i]] == i for i in range(16))

    # Original point-line incidence: x=Mw.
    R = [[0] * 16 for _ in range(12)]
    line_supports: list[set[int]] = []
    for j, m in enumerate(line_mats):
        supp = set()
        for i, (w, x) in enumerate(P):
            if mv(m, w) == x:
                R[i][j] = 1
                supp.add(i)
        assert len(supp) == 3
        line_supports.append(supp)

    # Point-heavy incidence from the Pass5793 affine hyperplane equation.
    Hinc = [[0] * 12 for _ in range(12)]
    heavy_supports: list[set[int]] = []
    for j, (phi, psi) in enumerate(H):
        supp = {
            i for i, (w, x) in enumerate(P)
            if (dot(phi, x) ^ dot(psi, w)) == 1
        }
        assert len(supp) == 6
        heavy_supports.append(supp)
        for i in supp:
            Hinc[i][j] = 1

    # Heavy-line disjointness D: line side 16, heavy side 12.
    D = [[0] * 12 for _ in range(16)]
    intersections = []
    criterion_ok = True
    for i, (m, ls) in enumerate(zip(line_mats, line_supports)):
        for j, ((phi, psi), hs) in enumerate(zip(H, heavy_supports)):
            n = len(ls & hs)
            intersections.append(n)
            disjoint = n == 0
            algebraic = rmul(phi, m) == psi
            criterion_ok &= disjoint == algebraic
            D[i][j] = int(disjoint)
    assert criterion_ok
    assert sorted(set(intersections)) == [0, 2]
    assert {x: intersections.count(x) for x in sorted(set(intersections))} == {0: 48, 2: 144}
    assert {sum(row) for row in D} == {3}
    assert {sum(D[i][j] for i in range(16)) for j in range(12)} == {4}

    # Exact transpose incidence isomorphism.  The point->heavy map is indexwise
    # (w,x)->(w^T,x^T) in the chosen bases; line M goes to M^T.
    for i in range(16):
        ti = line_transpose_perm[i]
        for j in range(12):
            assert D[i][j] == R[j][ti]

    # Hence the heavy-line disjointness copy has the same point Gram as Reye.
    DtD = matmul(transpose(D), D)
    RRt = matmul(R, transpose(R))
    assert DtD == RRt

    # Signed cross transform between the common W9 copies.
    # C_R=4R-J and C_H=2H-J are integer centerings.
    CR = [[4 * R[i][j] - 1 for j in range(16)] for i in range(12)]
    CH = [[2 * Hinc[i][j] - 1 for j in range(12)] for i in range(12)]
    cross_raw = matmul(transpose(CR), CH)
    assert all(x % 4 == 0 for row in cross_raw for x in row)
    B = [[x // 4 for x in row] for row in cross_raw]
    assert {x for row in B for x in row} == {-3, 1}
    assert all(sum(row) == 0 for row in B)
    assert all(sum(B[i][j] for i in range(16)) == 0 for j in range(12))
    assert B == [[1 - 4 * D[i][j] for j in range(12)] for i in range(16)]
    assert rank_q(B) == 9

    BBt = matmul(B, transpose(B))
    BtB = matmul(transpose(B), B)
    CRtCR = matmul(transpose(CR), CR)
    CHtCH = matmul(transpose(CH), CH)
    assert BBt == CRtCR
    assert BtB == [[4 * x for x in row] for row in CHtCH]

    # Projector identities: U=B/8 has UU^T=E_L and U^TU=E_H.
    assert matmul(CRtCR, CRtCR) == [[64 * x for x in row] for row in CRtCR]
    assert matmul(CHtCH, CHtCH) == [[16 * x for x in row] for row in CHtCH]

    result = {
        "schema": "w33.pass5798_5799.reye_disjointness_duality.v1",
        "status": "PASS",
        "source": str(SOURCE.relative_to(ROOT)),
        "pass_5798_heavy_line_reye_copy": {
            "line_heavy_intersection_spectrum": [[0, 48], [2, 144]],
            "disjointness_row_degree_on_16_lines": 3,
            "disjointness_column_degree_on_12_heavies": 4,
            "criterion": "L_M disjoint H_(phi,psi) iff psi = phi M",
            "incidence_isomorphism": "(w,x),M -> (w^T,x^T),M^T",
            "exact_matrix_identity": "D[M,h] = R[F^{-1}(h), M^T]",
            "heavy_line_point_gram_equals_original_reye_point_gram": True,
            "deduction": "the same 16 lines with heavy-disjointness form a second Reye 12_4,16_3 copy, transpose-isomorphic to the original point-line copy",
        },
        "pass_5799_signed_partial_isometry": {
            "integer_centerings": "C_R=4R-J_(12x16), C_H=2H-J_12",
            "cross_matrix": "B=(C_R^T C_H)/4 = J_(16x12)-4D",
            "B_entries": [-3, 1],
            "B_rank": 9,
            "B_row_and_column_sums_zero": True,
            "quadratic_identities": [
                "B B^T = C_R^T C_R",
                "B^T B = 4 C_H^T C_H",
                "(C_R^T C_R)^2 = 64(C_R^T C_R)",
                "(C_H^T C_H)^2 = 16(C_H^T C_H)",
            ],
            "partial_isometry": "U=B/8 has U U^T=E_(W9,line) and U^T U=E_(W9,heavy)",
            "deduction": "the disjointness Reye matrix is the signed cross-transform that canonically identifies the two common rank-nine sectors",
        },
        "boundary": "Exact finite incidence and rational partial-isometry theorem; no quantum, continuum, dynamical, or particle-physics identification follows.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS5798-5799: PASS")
    print("heavy-line disjointness is Reye; transpose incidence isomorphism; rank-9 signed partial isometry")


if __name__ == "__main__":
    main()
