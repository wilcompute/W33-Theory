#!/usr/bin/env python3
"""Passes 5816--5823: Fourier rank stratification of the affine M2(F2) carrier.

The line carrier is the affine translation torsor T=M2(F2).  Its 16 Walsh
characters are indexed by the dual matrix space, which splits under left/right
GL2(2) into rank strata 1+9+6.  This script proves that:

* the zero Fourier character is the trivial constituent;
* the nine rank-one characters are exactly the common W9 seen by point, heavy,
  and Reye-line incidence;
* the six invertible/rank-two characters are exactly the line-only V6 and are
  the common kernel of the point-line and heavy-disjointness Radon transforms;
* point/heavy fibre Fourier bases intertwine with the rank-one line Fourier
  basis by exact formulas R^T u=v, H^T u=-2h, D h=v;
* the full 576-element affine group acts monomially with phase
      (-1)^<Y',X>, Y'=A^{-T} Y B^T,
  and both rank-one and rank-two Fourier sectors have irreducible character
  norm one;
* transpose acts on Fourier labels by Y->Y^T and swaps the two rulings of the
  3x3 rank-one grid.

All arithmetic is integral.  No NumPy/SymPy dependency is required.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "PART_W33_PASS5816_5823_MATRIX_FOURIER_RANK_STRATIFICATION.json"

Vec = tuple[int, int]
Mat = tuple[int, int, int, int]
GroupElt = tuple[Mat, Mat, Mat]
ZERO: Vec = (0, 0)
E1: Vec = (1, 0)
E2: Vec = (0, 1)
E3: Vec = (1, 1)
VALL: list[Vec] = [ZERO, E2, E1, E3]
NONZERO: list[Vec] = [E1, E2, E3]
I: Mat = (1, 0, 0, 1)
ZMAT: Mat = (0, 0, 0, 0)


def dot(a: Vec, b: Vec) -> int:
    return (a[0] & b[0]) ^ (a[1] & b[1])


def vx(a: Vec, b: Vec) -> Vec:
    return (a[0] ^ b[0], a[1] ^ b[1])


def madd(a: Mat, b: Mat) -> Mat:
    return tuple(x ^ y for x, y in zip(a, b))  # type: ignore[return-value]


def mmul(a: Mat, b: Mat) -> Mat:
    a00, a01, a10, a11 = a
    b00, b01, b10, b11 = b
    return (
        (a00 & b00) ^ (a01 & b10),
        (a00 & b01) ^ (a01 & b11),
        (a10 & b00) ^ (a11 & b10),
        (a10 & b01) ^ (a11 & b11),
    )


def mv(a: Mat, v: Vec) -> Vec:
    return ((a[0] & v[0]) ^ (a[1] & v[1]), (a[2] & v[0]) ^ (a[3] & v[1]))


def rmul(v: Vec, a: Mat) -> Vec:
    return ((v[0] & a[0]) ^ (v[1] & a[2]), (v[0] & a[1]) ^ (v[1] & a[3]))


def mt(a: Mat) -> Mat:
    return (a[0], a[2], a[1], a[3])


def det(a: Mat) -> int:
    return (a[0] & a[3]) ^ (a[1] & a[2])


def rank2(a: Mat) -> int:
    if a == ZMAT:
        return 0
    return 2 if det(a) else 1


def minv(a: Mat) -> Mat:
    assert det(a) == 1
    return (a[3], a[1], a[2], a[0])


def invt(a: Mat) -> Mat:
    return mt(minv(a))


def all_mats() -> list[Mat]:
    return [tuple(bits) for bits in itertools.product((0, 1), repeat=4)]  # type: ignore[list-item]


MATS = all_mats()
GL = [m for m in MATS if rank2(m) == 2]
RANK1 = [m for m in MATS if rank2(m) == 1]
assert len(MATS) == 16 and len(RANK1) == 9 and len(GL) == 6


def outer(phi: Vec, w: Vec) -> Mat:
    """Column(phi) * row(w), the rank-one dual matrix for phi(X w)."""
    return (
        phi[0] & w[0],
        phi[0] & w[1],
        phi[1] & w[0],
        phi[1] & w[1],
    )


def pairing(y: Mat, m: Mat) -> int:
    return sum((a & b) for a, b in zip(y, m)) & 1


def chi(y: Mat, m: Mat) -> int:
    return -1 if pairing(y, m) else 1


def affine_matrix_action(g: GroupElt, m: Mat) -> Mat:
    x, a, b = g
    return madd(mmul(mmul(a, m), minv(b)), x)


def dual_action(g: GroupElt, y: Mat) -> tuple[Mat, int]:
    """g v_y = phase * v_y' for point-basis permutation action on lines."""
    x, a, b = g
    yp = mmul(mmul(invt(a), y), mt(b))
    phase = chi(yp, x)
    return yp, phase


def transpose(a: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*a)]


def matvec(a: list[list[int]], v: list[int]) -> list[int]:
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def rank_q(a: list[list[int]]) -> int:
    m = [[Fraction(x) for x in row] for row in a]
    nr = len(m)
    nc = len(m[0]) if nr else 0
    r = 0
    for c in range(nc):
        p = next((i for i in range(r, nr) if m[i][c]), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        q = m[r][c]
        m[r] = [x / q for x in m[r]]
        for i in range(nr):
            if i != r and m[i][c]:
                q = m[i][c]
                m[i] = [x - q * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


def gram(vectors: list[list[int]]) -> list[list[int]]:
    return [[sum(x * y for x, y in zip(a, b)) for b in vectors] for a in vectors]


def main() -> None:
    # Carriers.
    P = [(w, x) for w in NONZERO for x in VALL]
    H = [(phi, psi) for phi in NONZERO for psi in VALL]
    pidx = {p: i for i, p in enumerate(P)}
    hidx = {h: i for i, h in enumerate(H)}
    midx = {m: i for i, m in enumerate(MATS)}

    # Point-line incidence R[p,M]=1 iff x=Mw.
    R = [[0] * 16 for _ in range(12)]
    for i, (w, x) in enumerate(P):
        for j, m in enumerate(MATS):
            R[i][j] = int(mv(m, w) == x)

    # Point-heavy incidence Hinc and line-heavy disjointness D.
    Hinc = [[0] * 12 for _ in range(12)]
    for i, (w, x) in enumerate(P):
        for j, (phi, psi) in enumerate(H):
            Hinc[i][j] = int((dot(phi, x) ^ dot(psi, w)) == 1)
    D = [[0] * 12 for _ in range(16)]
    for i, m in enumerate(MATS):
        for j, (phi, psi) in enumerate(H):
            D[i][j] = int(rmul(phi, m) == psi)

    assert rank_q(R) == rank_q(Hinc) == rank_q(D) == 10

    # Full line Walsh basis v_Y(M)=(-1)^<Y,M>.
    line_fourier = {y: [chi(y, m) for m in MATS] for y in MATS}
    gf = gram([line_fourier[y] for y in MATS])
    assert gf == [[16 if i == j else 0 for j in range(16)] for i in range(16)]

    # Rank-one labels are exactly nonzero phi x nonzero w, bijectively.
    rank1_from_pairs = {outer(phi, w) for phi in NONZERO for w in NONZERO}
    assert rank1_from_pairs == set(RANK1)

    # Point and heavy fibre-Walsh bases, indexed by the same (w,phi).
    point_w9: dict[tuple[Vec, Vec], list[int]] = {}
    heavy_w9: dict[tuple[Vec, Vec], list[int]] = {}
    for w in NONZERO:
        for phi in NONZERO:
            u = [0] * 12
            for x in VALL:
                u[pidx[(w, x)]] = -1 if dot(phi, x) else 1
            point_w9[(w, phi)] = u

            h = [0] * 12
            for psi in VALL:
                h[hidx[(phi, psi)]] = -1 if dot(psi, w) else 1
            heavy_w9[(w, phi)] = h

    assert gram(list(point_w9.values())) == [[4 if i == j else 0 for j in range(9)] for i in range(9)]
    assert gram(list(heavy_w9.values())) == [[4 if i == j else 0 for j in range(9)] for i in range(9)]

    # Exact Radon/Fourier formulas.
    Rt = transpose(R)
    Ht = transpose(Hinc)
    for (w, phi), u in point_w9.items():
        y = outer(phi, w)
        v = line_fourier[y]
        assert matvec(Rt, u) == v
        assert matvec(Ht, u) == [-2 * z for z in heavy_w9[(w, phi)]]
        assert matvec(D, heavy_w9[(w, phi)]) == v

    # The six invertible Fourier characters are exactly the invisible line sector.
    for y in GL:
        v = line_fourier[y]
        assert matvec(R, v) == [0] * 12
        assert matvec(transpose(D), v) == [0] * 12
    assert rank_q([line_fourier[y] for y in GL]) == 6

    # No nonzero rank-one Fourier vector is killed by R or D^T.
    for y in RANK1:
        assert matvec(R, line_fourier[y]) != [0] * 12
        assert matvec(transpose(D), line_fourier[y]) != [0] * 12

    # 16=1+9+6 is the exact rank stratification of the line Fourier basis.
    zero_sector = [line_fourier[ZMAT]]
    w9_sector = [line_fourier[y] for y in RANK1]
    v6_sector = [line_fourier[y] for y in GL]
    assert rank_q(zero_sector + w9_sector + v6_sector) == 16

    # Exhaust the affine group and verify the signed monomial Fourier action.
    G: list[GroupElt] = [(x, a, b) for x in MATS for a in GL for b in GL]
    assert len(G) == 576
    rank1_chars: list[int] = []
    rank2_chars: list[int] = []
    for g in G:
        # Directly verify on all 16 Fourier vectors.
        perm = [midx[affine_matrix_action(g, m)] for m in MATS]
        for y in MATS:
            yp, phase = dual_action(g, y)
            direct = [0] * 16
            vy = line_fourier[y]
            for i, j in enumerate(perm):
                direct[j] = vy[i]
            assert direct == [phase * z for z in line_fourier[yp]]
            assert rank2(yp) == rank2(y)

        c1 = 0
        for y in RANK1:
            yp, phase = dual_action(g, y)
            if yp == y:
                c1 += phase
        c2 = 0
        for y in GL:
            yp, phase = dual_action(g, y)
            if yp == y:
                c2 += phase
        rank1_chars.append(c1)
        rank2_chars.append(c2)

    norm1 = sum(c * c for c in rank1_chars) // 576
    norm2 = sum(c * c for c in rank2_chars) // 576
    cross = sum(a * b for a, b in zip(rank1_chars, rank2_chars)) // 576
    assert norm1 == norm2 == 1
    assert cross == 0

    # Translation subgroup acts diagonally by all rank-stratum characters.
    translation_signatures_rank1 = {
        y: tuple(chi(y, x) for x in MATS) for y in RANK1
    }
    translation_signatures_rank2 = {
        y: tuple(chi(y, x) for x in MATS) for y in GL
    }
    assert len(set(translation_signatures_rank1.values())) == 9
    assert len(set(translation_signatures_rank2.values())) == 6

    # Transpose acts on Fourier labels Y->Y^T and swaps the two rank-one factors.
    for y in MATS:
        v = line_fourier[y]
        transposed = [0] * 16
        for i, m in enumerate(MATS):
            transposed[midx[mt(m)]] = v[i]
        assert transposed == line_fourier[mt(y)]
        assert rank2(mt(y)) == rank2(y)
    for w in NONZERO:
        for phi in NONZERO:
            assert mt(outer(phi, w)) == outer(w, phi)

    # Projective finite-quadric observation, proved here by enumeration: over F2
    # each nonzero matrix is one projective point, det=0 gives exactly the 9
    # rank-one points, arranged as a 3x3 product grid (phi,w).
    assert len(RANK1) == 3 * 3
    assert all(det(y) == 0 and y != ZMAT for y in RANK1)
    assert all(det(y) == 1 for y in GL)

    result = {
        "schema": "w33.pass5816_5823.matrix_fourier_rank_stratification.v1",
        "status": "PASS",
        "pass_5816_line_walsh_decomposition": {
            "line_carrier": "T=M2(F2), 16-point affine translation torsor",
            "fourier_label_space": "T^*=M2(F2) under Frobenius pairing",
            "rank_stratum_sizes": [1, 9, 6],
            "decomposition": "Q^16_L = 1 + W9(rank-one Fourier) + V6(invertible Fourier)",
            "walsh_gram": "16 I_16",
        },
        "pass_5817_rank_one_common_W9": {
            "labels": "Y=phi^T w^T with 0!=phi in V*, 0!=w in W",
            "label_count": 9,
            "point_basis": "u_(w,phi)=sum_x (-1)^phi(x) e_(w,x)",
            "heavy_basis": "h_(w,phi)=sum_psi (-1)^psi(w) e_(phi,psi)",
            "line_basis": "v_Y=sum_M (-1)^<Y,M> e_M",
            "exact_intertwiners": ["R^T u_(w,phi)=v_Y", "H^T u_(w,phi)=-2 h_(w,phi)", "D h_(w,phi)=v_Y"],
        },
        "pass_5818_line_only_V6": {
            "labels": "six invertible/rank-two Y in GL2(2)",
            "dimension": 6,
            "kernel_identity": "V6 = ker(R) = ker(D^T) inside the 16-line carrier",
            "rank_one_vectors_survive_both_radon_transforms": True,
        },
        "pass_5819_affine_monomial_action": {
            "formula": "g v_Y = (-1)^<Y',X> v_Y', Y'=A^{-T} Y B^T",
            "verified_pairs": 576 * 16,
            "rank_preserved": True,
            "rank_one_character_norm": norm1,
            "rank_two_character_norm": norm2,
            "rank_one_rank_two_character_inner_product": cross,
            "deduction": "both W9 and V6 Fourier sectors are absolutely irreducible over Q (explicit rational realization, complex character norm 1)",
        },
        "pass_5820_translation_spectrum": {
            "normal_group": "T=M2(F2)_+",
            "W9_restriction": "nine distinct nontrivial rank-one additive characters",
            "V6_restriction": "six distinct invertible/rank-two additive characters",
            "full_line_restriction": "all 16 additive characters exactly once",
        },
        "pass_5821_transpose_fourier_action": {
            "line_fourier": "Theta v_Y = v_(Y^T)",
            "rank_one_factor_swap": "Y=phi^T w^T -> Y^T=w^T phi^T",
            "rank_strata_preserved": True,
            "deduction": "the point/heavy transpose outer involution swaps the two rulings of the 3x3 rank-one label grid while preserving the 6-unit sector",
        },
        "pass_5822_projective_rank_quadric": {
            "nonzero_projective_points_in_PG3_2": 15,
            "det_zero_rank_one_points": 9,
            "det_one_invertible_points": 6,
            "rank_one_grid": "3 x 3 labels (phi,w)",
            "boundary": "This is an algebraic/projective observation from det(Y)=0; no physical meaning is assigned.",
        },
        "boundary": "Exact finite Fourier, incidence, and representation theorem. The 1+9+6 matrix-rank strata are not particle multiplets, qubit states, or physical sectors absent a separately verified physical map.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS5816-5823: PASS")
    print("M2(F2)^*: rank strata 1+9+6; W9=rank-one Fourier; V6=unit Fourier; Radon intertwiners exact")


if __name__ == "__main__":
    main()
