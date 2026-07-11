#!/usr/bin/env python3
"""Cohomological classification of the mixed outer action on A_2(L_-4)."""
from __future__ import annotations
from functools import lru_cache

from collections import deque
from fractions import Fraction
import json
import sys
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

ROOT = Path(__file__).resolve().parents[1]
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from w33_levi_next5_v4_common import (
    build_w33, gf2_rank, gf2_row_basis, point_outer_perm,
    point_transvection_perm, sha256_json, SEEDS,
)


def smith(A: Matrix):
    D, S, T = smith_normal_decomp(DomainMatrix.from_Matrix(A).convert_to(ZZ))
    return D.to_Matrix(), S.to_Matrix(), T.to_Matrix()


def saturated_kernel(A: Matrix) -> Matrix:
    D, _S, T = smith(A)
    zero = [i for i in range(min(D.shape)) if D[i, i] == 0]
    zero += list(range(min(D.shape), A.cols))
    B = T[:, zero]
    assert A * B == Matrix.zeros(A.rows, len(zero))
    return B


def perm_matrix_action(B: Matrix, perm: tuple[int, ...]) -> Matrix:
    inverse = [0] * len(perm)
    for i, j in enumerate(perm):
        inverse[j] = i
    PB = Matrix([[int(B[inverse[r], c]) for c in range(B.cols)] for r in range(B.rows)])
    G = B.T * B
    A = G.inv() * B.T * PB
    assert all(x.q == 1 for x in A)
    A = Matrix([[int(x) for x in A.row(r)] for r in range(A.rows)])
    assert B * A == PB and A.T * G * A == G and abs(int(A.det())) == 1
    return A


def p2_structure(D: Matrix):
    rows = []
    for i in range(D.rows):
        d = abs(int(D[i, i]))
        if d <= 1:
            continue
        a = 0
        t = d
        while t % 2 == 0:
            a += 1
            t //= 2
        if a:
            rows.append({"snf_index": i, "full_order": d, "p_order": 2**a, "odd_part": t})
    return rows


def action_in_p2(A: Matrix, S: Matrix, D: Matrix, parts: list[dict]):
    Sinv = S.inv()
    Adual = A.inv().T
    images = []
    for part in parts:
        y = Matrix.zeros(D.rows, 1)
        y[part["snf_index"], 0] = part["odd_part"]
        z = Sinv * y
        yp = S * (Adual * z)
        coord = []
        for target in parts:
            mod = target["p_order"]
            odd = target["odd_part"] % mod
            val = int(yp[target["snf_index"], 0]) % mod
            coord.append((val * pow(odd, -1, mod)) % mod)
        images.append(tuple(coord))
    return tuple(images)


def add_coord(a, b, mods):
    return tuple((x + y) % m for x, y, m in zip(a, b, mods))


def scale_coord(k, a, mods):
    return tuple((k * x) % m for x, m in zip(a, mods))


def apply_auto(auto, coord, mods):
    out = (0,) * len(mods)
    for k, image in zip(coord, auto):
        if k:
            out = add_coord(out, scale_coord(k, image, mods), mods)
    return out


def torsion_basis(mods):
    out = []
    for i, m in enumerate(mods):
        c = [0] * len(mods)
        c[i] = 1 if m == 2 else 4
        out.append(tuple(c))
    return out


def torsion_mask(coord, mods):
    mask = 0
    for i, (x, m) in enumerate(zip(coord, mods)):
        bit = x & 1 if m == 2 else (x // 4) & 1
        if bit:
            mask |= 1 << i
    return mask


def torsion_cols(auto, mods):
    return tuple(torsion_mask(apply_auto(auto, b, mods), mods) for b in torsion_basis(mods))


def apply_cols(cols, v):
    out = 0
    while v:
        b = v & -v
        out ^= cols[b.bit_length() - 1]
        v ^= b
    return out


def gf2_nullspace_map(cols: tuple[int, ...], dim: int) -> list[int]:
    rows = []
    for r in range(dim):
        row = 0
        for c, image in enumerate(cols):
            if (image >> r) & 1:
                row |= 1 << c
        rows.append(row)
    from w33_levi_next5_v4_common import gf2_nullspace
    return gf2_nullspace(rows, dim)


def in_span(v: int, basis: list[int]) -> bool:
    tagged = {}
    for row in gf2_row_basis(basis):
        tagged[row.bit_length() - 1] = row
    x = v
    for p in sorted(tagged, reverse=True):
        if (x >> p) & 1:
            x ^= tagged[p]
    return x == 0


def common_numerator(coord, parts, S, D, G):
    y = Matrix.zeros(D.rows, 1)
    for c, part in zip(coord, parts):
        y[part["snf_index"], 0] = part["odd_part"] * c
    v = G.inv() * (S.inv() * y)
    w = []
    for x in v:
        y8 = x * 8
        assert y8.q == 1
        w.append(int(y8) % 8)
    return w


def q_num128(coord, parts, S, D, G):
    w = Matrix(common_numerator(coord, parts, S, D, G))
    return int((w.T * G * w)[0]) % 128


@lru_cache(maxsize=1)
def analyze() -> dict:
    geom = build_w33()
    M = Matrix(geom.incidence.tolist())
    B = saturated_kernel(M)
    G = B.T * B
    D, S, _T = smith(G)
    parts = p2_structure(D)
    mods = [part["p_order"] for part in parts]
    assert sorted(mods) == [2] * 14 + [8]

    perms = [point_transvection_perm(geom.points, v) for v in SEEDS]
    perms.append(point_outer_perm(geom.points))
    lattice_actions = [perm_matrix_action(B, p) for p in perms]
    autos = [action_in_p2(A, S, D, parts) for A in lattice_actions]
    outer = autos[-1]

    h_index = mods.index(8)
    h = tuple(1 if i == h_index else 0 for i in range(15))
    outer_h = apply_auto(outer, h, mods)
    five_h = tuple(5 if i == h_index else 0 for i in range(15))
    u_coord = add_coord(outer_h, scale_coord(-1, five_h, mods), mods)
    u = torsion_mask(u_coord, mods)

    T = torsion_cols(outer, mods)
    identity = tuple(1 << i for i in range(15))
    N = tuple(T[i] ^ identity[i] for i in range(15))
    kernel_basis = gf2_nullspace_map(N, 15)
    image_basis = gf2_row_basis(N)
    h1_dim = len(kernel_basis) - len(image_basis)
    u_is_cocycle = apply_cols(N, u) == 0
    u_is_coboundary = in_span(u, image_basis)

    fixed_line = 1 << h_index
    fixed_line_is_cocycle = apply_cols(N, fixed_line) == 0

    quotient_basis = list(image_basis)
    h1_reps: list[int] = []
    for v in kernel_basis:
        if not in_span(v, quotient_basis):
            h1_reps.append(v)
            quotient_basis = gf2_row_basis(quotient_basis + [v])

    from w33_levi_next5_v4_common import tagged_basis, coordinates
    tagged = tagged_basis(image_basis + h1_reps)
    rem, tag_u = coordinates(u, tagged)
    assert rem == 0
    rem, tag_f = coordinates(fixed_line, tagged)
    assert rem == 0
    h1_u = tag_u >> len(image_basis)
    h1_f = tag_f >> len(image_basis)

    q_u = Fraction(q_num128(u_coord, parts, S, D, G), 64)
    while q_u >= 2:
        q_u -= 2

    checks = {
        "p2_module_type": sorted(mods) == [2] * 14 + [8],
        "outer_difference_is_2_torsion": all((x in (0, 1) if m == 2 else x in (0, 4)) for x, m in zip(u_coord, mods)),
        "cocycle_condition": u_is_cocycle,
        "h1_dimension_positive": h1_dim > 0,
        "mixed_class_nontrivial": not u_is_coboundary,
        "fixed_line_is_cocycle": fixed_line_is_cocycle,
        "outer_is_involution_on_torsion": all(apply_cols(T, apply_cols(T, 1 << i)) == (1 << i) for i in range(15)),
        "h1_representatives_match_dimension": len(h1_reps) == h1_dim,
    }

    relation = "same" if h1_u == h1_f else "independent" if gf2_rank([h1_u, h1_f]) == 2 else "distinct-dependent"
    theorem = (
        "The mixed displacement u=tau(h)-5h is a 1-cocycle for C2 acting on A_2(L_-4)[2]. "
        "Its class is nonzero in H^1(C2,A[2]); hence no order-two rechoice h->h+v removes the mixing."
    )
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "module": {"type": "(Z/2)^14 + Z/8", "torsion_dimension": 15, "h_index": h_index},
        "outer": {
            "h_image": list(outer_h),
            "five_h": list(five_h),
            "mixed_displacement": list(u_coord),
            "mixed_displacement_mask": hex(u),
            "q_u": str(q_u),
        },
        "cohomology": {
            "complex": "H^1(C2,A[2]) = ker(1+tau)/im(1+tau)",
            "kernel_dimension": len(kernel_basis),
            "coboundary_dimension": len(image_basis),
            "H1_dimension": h1_dim,
            "representatives_hex": [hex(x) for x in h1_reps],
            "mixed_class_coordinates": hex(h1_u),
            "fixed_line_class_coordinates": hex(h1_f),
            "relation_to_fixed_line": relation,
            "removable_by_h_shift": u_is_coboundary,
        },
        "digests": {
            "outer_torsion_action": sha256_json(T),
            "cohomology_representatives": sha256_json(h1_reps),
        },
        "theorem": theorem,
    }


def main() -> int:
    out = analyze()
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
