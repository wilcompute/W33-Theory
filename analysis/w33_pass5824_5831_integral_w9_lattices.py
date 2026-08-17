#!/usr/bin/env python3
"""Passes 5824--5831: integral forms of the common q=5 W9 sector.

The rational W9 is common to point, heavy and line carriers, but the ambient
integral lattices are not identical.  This verifier proves:

* point/heavy saturated W9 lattices are A3^3, discriminant 2^6;
* after an explicit GL4(2) coordinate relabeling, the line saturated W9 lattice
  is A3 tensor A3, discriminant 2^12;
* the rank-one Walsh sublattices have saturation indices 2^6 on point/heavy and
  2^12 on line;
* the saturated Radon maps R^T and D have SNF 1^5 2^2 4^2 (cokernel 2^6),
  while H^T has SNF 1^2 2^5 4^2 (cokernel 2^9);
* ambient incidence and centered-kernel Smith forms are frozen as an explicit
  characteristic-two firewall.

Requires SymPy only for exact Smith normal forms.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "PART_W33_PASS5824_5831_INTEGRAL_W9_LATTICES.json"

Vec = tuple[int, int]
Mat = tuple[int, int, int, int]
ZERO: Vec = (0, 0)
E1: Vec = (1, 0)
E2: Vec = (0, 1)
E3: Vec = (1, 1)
VALL: list[Vec] = [ZERO, E2, E1, E3]
NONZERO: list[Vec] = [E1, E2, E3]
ZMAT: Mat = (0, 0, 0, 0)


def dot(a: Vec, b: Vec) -> int:
    return (a[0] & b[0]) ^ (a[1] & b[1])


def mv(a: Mat, v: Vec) -> Vec:
    return ((a[0] & v[0]) ^ (a[1] & v[1]), (a[2] & v[0]) ^ (a[3] & v[1]))


def rmul(v: Vec, a: Mat) -> Vec:
    return ((v[0] & a[0]) ^ (v[1] & a[2]), (v[0] & a[1]) ^ (v[1] & a[3]))


def det2(a: Mat) -> int:
    return (a[0] & a[3]) ^ (a[1] & a[2])


def outer(phi: Vec, w: Vec) -> Mat:
    return (
        phi[0] & w[0], phi[0] & w[1],
        phi[1] & w[0], phi[1] & w[1],
    )


def pairing(y: Mat, m: Mat) -> int:
    return sum((a & b) for a, b in zip(y, m)) & 1


def chi(y: Mat, m: Mat) -> int:
    return -1 if pairing(y, m) else 1


def all_mats() -> list[Mat]:
    return [tuple(bits) for bits in itertools.product((0, 1), repeat=4)]  # type: ignore[list-item]


MATS = all_mats()
GL = [m for m in MATS if det2(m)]
RANK1 = [m for m in MATS if m != ZMAT and not det2(m)]


def snf_diag(a: sp.Matrix) -> list[int]:
    s = smith_normal_form(a, domain=ZZ)
    return [abs(int(s[i, i])) for i in range(min(s.rows, s.cols)) if s[i, i] != 0]


def multiplicative_index(diag: list[int]) -> int:
    return math.prod(diag)


def rank_mod2(a: sp.Matrix) -> int:
    rows = [[int(a[i, j]) & 1 for j in range(a.cols)] for i in range(a.rows)]
    r = 0
    for c in range(a.cols):
        p = next((i for i in range(r, a.rows) if rows[i][c]), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(a.rows):
            if i != r and rows[i][c]:
                rows[i] = [x ^ y for x, y in zip(rows[i], rows[r])]
        r += 1
    return r


def inv4_mod2(a: list[list[int]]) -> list[list[int]]:
    n = 4
    aug = [[(a[i][j] & 1) for j in range(n)] + [int(i == j) for j in range(n)] for i in range(n)]
    r = 0
    for c in range(n):
        p = next(i for i in range(r, n) if aug[i][c])
        aug[r], aug[p] = aug[p], aug[r]
        for i in range(n):
            if i != r and aug[i][c]:
                aug[i] = [x ^ y for x, y in zip(aug[i], aug[r])]
        r += 1
    return [row[n:] for row in aug]


def act4(a: list[list[int]], v: Mat) -> Mat:
    return tuple(sum((a[i][j] & v[j]) for j in range(4)) & 1 for i in range(4))  # type: ignore[return-value]


def main() -> None:
    P = [(w, x) for w in NONZERO for x in VALL]
    H = [(phi, psi) for phi in NONZERO for psi in VALL]
    pidx = {p: i for i, p in enumerate(P)}
    hidx = {h: i for i, h in enumerate(H)}
    midx = {m: i for i, m in enumerate(MATS)}

    R = sp.Matrix([[int(mv(m, w) == x) for m in MATS] for w, x in P])
    Hinc = sp.Matrix([[
        int((dot(phi, x) ^ dot(psi, w)) == 1) for phi, psi in H
    ] for w, x in P])
    D = sp.Matrix([[int(rmul(phi, m) == psi) for phi, psi in H] for m in MATS])
    J12 = sp.ones(12, 12)
    K = R * R.T - J12
    CR = 4 * R - sp.ones(12, 16)
    CH = 2 * Hinc - J12
    Bcross = (CR.T * CH) / 4
    assert all(x.q == 1 for x in Bcross)
    Bcross = sp.Matrix([[int(Bcross[i, j]) for j in range(Bcross.cols)] for i in range(Bcross.rows)])

    # A3^3 bases: within each 4-fibre use e_i-e_3, i=0,1,2.
    PB_cols: list[list[int]] = []
    for w in NONZERO:
        inds = [pidx[(w, x)] for x in VALL]
        for i in range(3):
            z = [0] * 12
            z[inds[i]], z[inds[3]] = 1, -1
            PB_cols.append(z)
    PB = sp.Matrix.hstack(*[sp.Matrix(c) for c in PB_cols])

    HB_cols: list[list[int]] = []
    for phi in NONZERO:
        inds = [hidx[(phi, psi)] for psi in VALL]
        for i in range(3):
            z = [0] * 12
            z[inds[i]], z[inds[3]] = 1, -1
            HB_cols.append(z)
    HB = sp.Matrix.hstack(*[sp.Matrix(c) for c in HB_cols])

    A3_gram = sp.Matrix([[2, 1, 1], [1, 2, 1], [1, 1, 2]])
    assert PB.T * PB == sp.diag(A3_gram, A3_gram, A3_gram)
    assert HB.T * HB == sp.diag(A3_gram, A3_gram, A3_gram)
    point_disc = int((PB.T * PB).det())
    assert point_disc == 64

    # Explicit dual-label map L sends the rank-one determinant quadric to the
    # product-nonzero labels {(alpha,beta): alpha!=0,beta!=0}.
    L = [
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [0, 1, 1, 1],
        [1, 0, 0, 1],
    ]
    Linv = inv4_mod2(L)
    C = [[Linv[j][i] for j in range(4)] for i in range(4)]  # C=L^{-T}
    Cinv = inv4_mod2(C)
    assert [[Cinv[j][i] for j in range(4)] for i in range(4)] == L
    product_nonzero = {
        (a[0], a[1], b[0], b[1]) for a in NONZERO for b in NONZERO
    }
    assert {act4(L, y) for y in RANK1} == product_nonzero

    # Coordinate isometry Q_C on the 16 line positions.
    qperm = [midx[act4(C, m)] for m in MATS]
    assert sorted(qperm) == list(range(16))

    def qvec(z: sp.Matrix) -> sp.Matrix:
        out = [0] * 16
        for i, j in enumerate(qperm):
            out[j] = int(z[i, 0])
        return sp.Matrix(out)

    # In new coordinates, the common line W9 is the row/column-zero lattice,
    # with basis (e_i-e_3) tensor (e_j-e_3): exactly A3 tensor A3.
    pair_idx = {(a, b): midx[a + b] for a in VALL for b in VALL}
    LB_cols: list[list[int]] = []
    for i in range(3):
        for j in range(3):
            z = [0] * 16
            for ai, ca in ((i, 1), (3, -1)):
                for bj, cb in ((j, 1), (3, -1)):
                    z[pair_idx[(VALL[ai], VALL[bj])]] += ca * cb
            LB_cols.append(z)
    LB = sp.Matrix.hstack(*[sp.Matrix(c) for c in LB_cols])
    line_gram = LB.T * LB
    assert line_gram == sp.kronecker_product(A3_gram, A3_gram)
    line_disc = int(line_gram.det())
    assert line_disc == 4096

    # Transformed rank-one Walsh vectors span the same rational subspace.
    rank1_walsh = [sp.Matrix([chi(y, m) for m in MATS]) for y in RANK1]
    transformed_walsh = [qvec(v) for v in rank1_walsh]
    assert sp.Matrix.hstack(*transformed_walsh).rank() == 9
    for v in transformed_walsh:
        grid = [[int(v[pair_idx[(a, b)], 0]) for b in VALL] for a in VALL]
        assert all(sum(row) == 0 for row in grid)
        assert all(sum(grid[i][j] for i in range(4)) == 0 for j in range(4))

    # Walsh sublattices and their saturation indices.
    PW_cols, HW_cols, LW_cols = [], [], []
    for w in NONZERO:
        for phi in NONZERO:
            u = [0] * 12
            for x in VALL:
                u[pidx[(w, x)]] = -1 if dot(phi, x) else 1
            PW_cols.append(u)
            h = [0] * 12
            for psi in VALL:
                h[hidx[(phi, psi)]] = -1 if dot(psi, w) else 1
            HW_cols.append(h)
            y = outer(phi, w)
            LW_cols.append([chi(y, m) for m in MATS])
    PW = sp.Matrix.hstack(*[sp.Matrix(c) for c in PW_cols])
    HW = sp.Matrix.hstack(*[sp.Matrix(c) for c in HW_cols])
    LW = sp.Matrix.hstack(*[sp.Matrix(c) for c in LW_cols])
    pw_snf = snf_diag(PW)
    hw_snf = snf_diag(HW)
    lw_snf = snf_diag(LW)
    assert pw_snf == hw_snf == [1, 1, 1, 2, 2, 2, 2, 2, 2]
    assert lw_snf == [1, 2, 2, 2, 2, 4, 4, 4, 4]
    assert multiplicative_index(pw_snf) == 64
    assert multiplicative_index(lw_snf) == 4096

    # Coordinate extractors for the saturated bases.
    pcoords = []
    for w in NONZERO:
        pcoords.extend(pidx[(w, VALL[i])] for i in range(3))
    hcoords = []
    for phi in NONZERO:
        hcoords.extend(hidx[(phi, VALL[i])] for i in range(3))
    lcoords = [pair_idx[(VALL[i], VALL[j])] for i in range(3) for j in range(3)]
    assert PB.extract(pcoords, range(9)) == sp.eye(9)
    assert HB.extract(hcoords, range(9)) == sp.eye(9)
    assert LB.extract(lcoords, range(9)) == sp.eye(9)

    def coords_line(z_old: sp.Matrix) -> sp.Matrix:
        z = qvec(z_old)
        c = z.extract(lcoords, [0])
        assert LB * c == z
        return c

    # Saturated Radon maps.
    TR = sp.zeros(9, 9)
    TD = sp.zeros(9, 9)
    TH = sp.zeros(9, 9)
    for k in range(9):
        TR[:, k] = coords_line(R.T * PB[:, k])
        TD[:, k] = coords_line(D * HB[:, k])
        zh = Hinc.T * PB[:, k]
        ch = zh.extract(hcoords, [0])
        assert HB * ch == zh
        TH[:, k] = ch

    tr_snf = snf_diag(TR)
    td_snf = snf_diag(TD)
    th_snf = snf_diag(TH)
    assert tr_snf == td_snf == [1, 1, 1, 1, 1, 2, 2, 4, 4]
    assert th_snf == [1, 1, 2, 2, 2, 2, 2, 4, 4]
    assert abs(int(TR.det())) == abs(int(TD.det())) == 64
    assert abs(int(TH.det())) == 512

    # Ambient Smith forms and modular ranks.
    ambient = {
        "R": snf_diag(R),
        "H": snf_diag(Hinc),
        "D": snf_diag(D),
        "K9": snf_diag(K),
        "Bcross": snf_diag(Bcross),
        "CR": snf_diag(CR),
        "CH": snf_diag(CH),
    }
    assert ambient["R"] == ambient["D"] == [1] * 8 + [2, 2]
    assert ambient["H"] == [1] * 4 + [2] * 6
    assert ambient["K9"] == [1, 1, 1] + [4] * 6
    assert ambient["Bcross"] == ambient["CR"] == [1] + [4] * 6 + [8] * 2
    assert ambient["CH"] == [1] + [2] * 4 + [4] * 4
    mod2 = {name: rank_mod2(mat) for name, mat in {
        "R": R, "H": Hinc, "D": D, "K9": K, "Bcross": Bcross, "CR": CR, "CH": CH,
    }.items()}
    assert mod2 == {"R": 8, "H": 4, "D": 8, "K9": 3, "Bcross": 1, "CR": 1, "CH": 1}

    point_gram_snf = snf_diag(PB.T * PB)
    line_gram_snf = snf_diag(line_gram)
    assert point_gram_snf == [1] * 6 + [4] * 3
    assert line_gram_snf == [1] * 4 + [4] * 4 + [16]

    result = {
        "schema": "w33.pass5824_5831.integral_w9_lattices.v1",
        "status": "PASS",
        "pass_5824_saturated_lattices": {
            "point_W9": "A3^3",
            "heavy_W9": "A3^3",
            "line_W9": "A3 tensor A3 after explicit GL4(2) coordinate relabel",
            "point_heavy_discriminant": point_disc,
            "line_discriminant": line_disc,
            "point_heavy_gram_snf": point_gram_snf,
            "line_gram_snf": line_gram_snf,
            "line_discriminant_group": "(Z/4)^4 x Z/16",
            "point_heavy_discriminant_group": "(Z/4)^3",
        },
        "pass_5825_explicit_GL4_relabel": {
            "dual_label_map_L_rows": L,
            "primal_coordinate_map_C_rows": C,
            "identity": "C^{-T}=L",
            "rank_one_labels_map_to_product_nonzero_3x3_labels": True,
            "deduction": "the transformed line W9 saturation is exactly the row-and-column-zero 4x4 lattice A3 tensor A3",
        },
        "pass_5826_walsh_saturation_indices": {
            "point_Walsh_snf": pw_snf,
            "heavy_Walsh_snf": hw_snf,
            "line_Walsh_snf": lw_snf,
            "point_heavy_Walsh_index_in_saturation": multiplicative_index(pw_snf),
            "line_Walsh_index_in_saturation": multiplicative_index(lw_snf),
        },
        "pass_5827_saturated_radon_snf": {
            "R_transpose_A3cubed_to_A3tensorA3": tr_snf,
            "D_A3cubed_to_A3tensorA3": td_snf,
            "H_transpose_A3cubed_to_A3cubed": th_snf,
            "R_D_cokernel": "(Z/2)^2 x (Z/4)^2, order 64",
            "H_cokernel": "(Z/2)^5 x (Z/4)^2, order 512",
        },
        "pass_5828_ambient_smith_forms": ambient,
        "pass_5829_characteristic_two_firewall": {
            "mod2_ranks": mod2,
            "rational_common_W9_dimension": 9,
            "deduction": "the rational W9 equivalence does not descend to equality of integral or mod-2 carrier lattices; the exact obstruction is 2-primary",
        },
        "pass_5830_structural_summary": {
            "rational": "P,H,L share one absolutely irreducible W9",
            "integral": "P,H use A3^3; L uses A3 tensor A3",
            "radon_gluing": "R^T and D have saturated cokernel order 2^6; H^T has order 2^9",
            "mod2": "ambient ranks split R/D=8, H=4, K9=3, centered cross transforms=1",
        },
        "boundary": "Exact integral lattice and Smith-normal-form theorem. It strengthens the characteristic-two firewall: rational carrier equivalence must not be promoted to integral or binary equivalence.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS5824-5831: PASS")
    print("W9 lattices: A3^3, A3^3, A3 tensor A3; exact 2-primary Radon SNFs frozen")


if __name__ == "__main__":
    main()
