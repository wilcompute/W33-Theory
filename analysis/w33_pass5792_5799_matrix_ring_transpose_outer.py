#!/usr/bin/env python3
"""Passes 5792--5799: M2(F2) affine left/right model of the q=5 Latin carrier.

Starting from the Pass5776--5783 Klein-V4 coordinate chart, construct the full
576-element autoparatopy carrier as

    Hom(W,V) : (GL(V) x GL(W)),  V=W=F_2^2.

After choosing bases, Hom(W,V)=M_2(F_2).  The script proves at object level:

* the 12 q=5 heavy supports are exactly the affine hyperplanes
      phi(x) + psi(w) = 1
  on the 12 point carrier P={(w,x): w!=0};
* their complements are exactly the Klein intercalate supports;
* the 576 affine left/right transformations reproduce the frozen point,
  heavy, and Reye-line rank-3 character pairings;
* matrix transpose normalizes the 576-group and induces the factor-swap outer
  automorphism
      (X,A,B) -> (X^T, B^{-T}, A^{-T});
* the point carrier twisted by this automorphism is exactly the heavy carrier;
* point and heavy stabilizers are not internally conjugate: their intersections
  with the normal M_2(F_2) translation group are, respectively, fixed-right-
  kernel and fixed-left-image subspaces, which left/right multiplication cannot
  exchange.

The M_2(F_2) connection here is finite algebra.  It does not identify the q=5
carrier with the two-qubit Pauli/projective-ring geometry.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "PART_W33_PASS5776_5783_REYE_LATIN_COMMON_CORE.json"
SOURCE_5667 = ROOT / "data" / "PART_W33_PASS5667_5674_Q5_REYE_EQUIVARIANT_ORIENTATION.json"
OUTPUT = ROOT / "data" / "PART_W33_PASS5792_5799_MATRIX_RING_TRANSPOSE_OUTER.json"

Vec = tuple[int, int]
Mat = tuple[int, int, int, int]  # row-major a,b,c,d
GroupElt = tuple[Mat, Mat, Mat]  # X,A,B

ZERO: Vec = (0, 0)
E1: Vec = (1, 0)
E2: Vec = (0, 1)
E3: Vec = (1, 1)
VALL: list[Vec] = [ZERO, E2, E1, E3]  # integer/XOR labels 0,1,2,3
NONZERO: list[Vec] = [E1, E2, E3]
I: Mat = (1, 0, 0, 1)


def vx(a: Vec, b: Vec) -> Vec:
    return (a[0] ^ b[0], a[1] ^ b[1])


def dot(a: Vec, b: Vec) -> int:
    return (a[0] & b[0]) ^ (a[1] & b[1])


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


def minv(a: Mat) -> Mat:
    assert det(a) == 1
    # In F2 det=1 and minus=plus.
    return (a[3], a[1], a[2], a[0])


def invt(a: Mat) -> Mat:
    return mt(minv(a))


def all_mats() -> list[Mat]:
    return [tuple(bits) for bits in itertools.product((0, 1), repeat=4)]  # type: ignore[list-item]


MATS = all_mats()
GL = [a for a in MATS if det(a) == 1]
assert len(MATS) == 16 and len(GL) == 6


def affine_matrix_action(g: GroupElt, m: Mat) -> Mat:
    x, a, b = g
    return madd(mmul(mmul(a, m), minv(b)), x)


def tau(g: GroupElt) -> GroupElt:
    x, a, b = g
    return (mt(x), invt(b), invt(a))


def point_action(g: GroupElt, p: tuple[Vec, Vec]) -> tuple[Vec, Vec]:
    """P={(w,x):w!=0}, induced from matrix evaluation M(w)=x."""
    xmat, a, b = g
    w, x = p
    wb = mv(b, w)
    return wb, vx(mv(a, x), mv(xmat, wb))


def heavy_action(g: GroupElt, h: tuple[Vec, Vec]) -> tuple[Vec, Vec]:
    """Dual affine hyperplanes phi(x)+psi(w)=1."""
    xmat, a, b = g
    phi, psi = h
    phip = rmul(phi, minv(a))
    psip = vx(rmul(psi, minv(b)), rmul(phip, xmat))
    return phip, psip


def point_to_heavy_factor_swap(p: tuple[Vec, Vec]) -> tuple[Vec, Vec]:
    """Basis transpose: vector w/x become row covectors w^T/x^T."""
    w, x = p
    return w, x


def perm_parity(perm: list[int]) -> int:
    inv = sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm)))
    return -1 if inv % 2 else 1


def span_rank(vs: list[Vec]) -> int:
    s = set(vs)
    if not any(v != ZERO for v in s):
        return 0
    nz = [v for v in s if v != ZERO]
    if len(set(nz)) == 1:
        return 1
    return 2


def support(phi: Vec, psi: Vec, rhs: int, points: list[tuple[Vec, Vec]]) -> frozenset[int]:
    return frozenset(i for i, (w, x) in enumerate(points) if (dot(phi, x) ^ dot(psi, w)) == rhs)


def main() -> None:
    prev = json.loads(SOURCE.read_text())
    prev5667 = json.loads(SOURCE_5667.read_text())
    chart = prev["pass_5778_reye_td34_klein_latin"]["explicit_cover_coordinate_chart"]

    # P order matches the chart: row, column, symbol; values 0,1,2,3.
    P = [(w, x) for w in NONZERO for x in VALL]
    p_index = {p: i for i, p in enumerate(P)}
    H = [(phi, psi) for phi in NONZERO for psi in VALL]
    h_index = {h: i for i, h in enumerate(H)}

    row_cover = chart["row_index_to_cover_position"]
    col_cover = chart["column_index_to_cover_position"]
    sym_cover = chart["xor_symbol_index_to_cover_position"]
    point_to_cover = row_cover + col_cover + sym_cover
    assert len(point_to_cover) == 12 and len(set(point_to_cover)) == 12

    # Heavy hyperplanes and intercalate complements.
    heavy_supports_idx = {support(phi, psi, 1, P) for phi, psi in H}
    inter_supports_idx = {support(phi, psi, 0, P) for phi, psi in H}
    assert len(heavy_supports_idx) == len(inter_supports_idx) == 12
    assert all(len(s) == 6 for s in heavy_supports_idx | inter_supports_idx)
    assert {frozenset(set(range(12)) - set(s)) for s in heavy_supports_idx} == inter_supports_idx

    heavy_cover_model = {
        frozenset(point_to_cover[i] for i in s) for s in heavy_supports_idx
    }
    heavy_cover_frozen = {
        frozenset(block)
        for block in prev5667["pass_5673_5674_heavy_dual"]["heavy_blocks_in_cover_positions"]
    }
    assert heavy_cover_model == heavy_cover_frozen

    # The 16 Latin/TD lines on P.
    line_supports: list[frozenset[int]] = []
    for r in VALL:
        for c in VALL:
            s = vx(r, c)
            line_supports.append(
                frozenset((p_index[(E1, r)], p_index[(E2, c)], p_index[(E3, s)]))
            )
    assert len(set(line_supports)) == 16
    line_index = {line: i for i, line in enumerate(line_supports)}

    G: list[GroupElt] = [(x, a, b) for x in MATS for a in GL for b in GL]
    assert len(G) == 576

    point_perms: list[tuple[int, ...]] = []
    heavy_perms: list[tuple[int, ...]] = []
    line_perms: list[tuple[int, ...]] = []
    char_rows: list[tuple[int, int, int, int]] = []

    for g in G:
        pp = tuple(p_index[point_action(g, p)] for p in P)
        hp = tuple(h_index[heavy_action(g, h)] for h in H)
        assert len(set(pp)) == 12 and len(set(hp)) == 12
        lp_list = []
        for line in line_supports:
            image = frozenset(pp[i] for i in line)
            assert image in line_index
            lp_list.append(line_index[image])
        lp = tuple(lp_list)
        point_perms.append(pp)
        heavy_perms.append(hp)
        line_perms.append(lp)
        fp = sum(i == j for i, j in enumerate(pp))
        fh = sum(i == j for i, j in enumerate(hp))
        fl = sum(i == j for i, j in enumerate(lp))
        eps = perm_parity(list(pp))
        char_rows.append((fp, fh, fl, eps))

    assert len(set(point_perms)) == 576
    assert len(set(heavy_perms)) == 576
    assert len(set(line_perms)) == 576

    def ip(i: int, j: int, sign: bool = False) -> int:
        total = sum((row[3] if sign else 1) * row[i] * row[j] for row in char_rows)
        assert total % 576 == 0
        return total // 576

    char_gram = [[ip(i, j) for j in range(3)] for i in range(3)]
    signed_point = [ip(0, j, True) for j in range(3)]
    assert char_gram == [[3, 2, 2], [2, 3, 2], [2, 2, 3]]
    assert signed_point == [0, 0, 0]

    # Point action rank/subdegrees for a base point; heavy likewise.
    def orbit_of(base: int, perms: list[tuple[int, ...]], stabilizer_only: bool = False) -> set[int]:
        use = [p for p in perms if (p[base] == base if stabilizer_only else True)]
        return {p[base] for p in use}

    def subdegrees(base: int, perms: list[tuple[int, ...]]) -> list[int]:
        stab = [p for p in perms if p[base] == base]
        unseen = set(range(len(perms[0])))
        sizes = []
        while unseen:
            x = min(unseen)
            orb = {p[x] for p in stab}
            sizes.append(len(orb))
            unseen -= orb
        return sorted(sizes)

    assert len(orbit_of(0, point_perms)) == 12
    assert len(orbit_of(0, heavy_perms)) == 12
    assert sum(p[0] == 0 for p in point_perms) == 48
    assert sum(p[0] == 0 for p in heavy_perms) == 48
    assert subdegrees(0, point_perms) == [1, 3, 8]
    assert subdegrees(0, heavy_perms) == [1, 3, 8]

    # Transpose normalizer and factor-swap intertwiner.
    for g in G:
        tg = tau(g)
        assert tau(tg) == g
        # Conjugation by transpose on all 16 affine matrices.
        for m in MATS:
            lhs = mt(affine_matrix_action(g, mt(m)))
            rhs = affine_matrix_action(tg, m)
            assert lhs == rhs
        # Point carrier twisted by tau is literally the heavy carrier.
        for p in P:
            lhs_h = point_to_heavy_factor_swap(point_action(g, p))
            rhs_h = heavy_action(tg, point_to_heavy_factor_swap(p))
            assert lhs_h == rhs_h

    # Transpose is not one of the 576 affine left/right maps.
    transpose_perm = tuple(MATS.index(mt(m)) for m in MATS)
    affine_perms = {
        tuple(MATS.index(affine_matrix_action(g, m)) for m in MATS) for g in G
    }
    assert len(affine_perms) == 576
    assert transpose_perm not in affine_perms
    assert sum(i == j for i, j in enumerate(transpose_perm)) == 8

    # Translation-subgroup stabilizer types certify outerness intrinsically.
    T = [(x, I, I) for x in MATS]
    p0 = P[0]
    h0 = H[0]
    tp = [x for x, a, b in T if point_action((x, a, b), p0) == p0]
    th = [x for x, a, b in T if heavy_action((x, a, b), h0) == h0]
    assert len(tp) == len(th) == 4

    # P stabilizer translations have a common right-kernel; their aggregate
    # image spans all V. H stabilizer translations have image in one fixed line.
    all_vecs = VALL
    image_span_p = span_rank([mv(x, v) for x in tp for v in all_vecs])
    image_span_h = span_rank([mv(x, v) for x in th for v in all_vecs])
    assert image_span_p == 2
    assert image_span_h == 1

    # A fixed-right-kernel subspace remains of that type under X->A X B^-1;
    # a fixed-left-image subspace remains of the second type.  Hence these
    # stabilizer intersections cannot be conjugate inside G, while transpose
    # exchanges them.
    tp_t = {mt(x) for x in tp}
    assert tp_t == set(th)

    # Ring-theoretic census of the normal matrix space.
    units = [m for m in MATS if det(m) == 1]
    zero_divisors = [m for m in MATS if det(m) == 0]
    assert len(units) == 6 and len(zero_divisors) == 10

    results = {
        "schema": "w33.pass5792_5799.matrix_ring_transpose_outer.v1",
        "status": "PASS",
        "source": str(SOURCE.relative_to(ROOT)),
        "pass_5792_affine_left_right_group": {
            "normal_translation_space": "Hom(F2^2,F2^2) = M2(F2) additive",
            "translation_order": 16,
            "left_GL2_order": 6,
            "right_GL2_order": 6,
            "group_order": 576,
            "group_model": "M2(F2) : (GL2(2) x GL2(2))",
            "matrix_units": len(units),
            "matrix_singular_elements": len(zero_divisors),
        },
        "pass_5793_point_heavy_hyperplane_model": {
            "point_carrier": "P={(w,x): 0!=w in F2^2, x in F2^2}",
            "heavy_carrier": "H={(phi,psi): 0!=phi in (F2^2)^*, psi in (F2^2)^*}",
            "heavy_support_equation": "phi(x) + psi(w) = 1",
            "intercalate_complement_equation": "phi(x) + psi(w) = 0",
            "heavy_supports_match_frozen_q5_blocks": True,
            "carrier_sizes": [12, 12],
        },
        "pass_5794_character_replay": {
            "point_action_faithful_order": len(set(point_perms)),
            "heavy_action_faithful_order": len(set(heavy_perms)),
            "line_action_faithful_order": len(set(line_perms)),
            "point_stabilizer_order": 48,
            "heavy_stabilizer_order": 48,
            "point_subdegrees": subdegrees(0, point_perms),
            "heavy_subdegrees": subdegrees(0, heavy_perms),
            "permutation_character_gram_P_H_L": char_gram,
            "sign_twisted_point_pairings_with_P_H_L": signed_point,
        },
        "pass_5795_transpose_normalizer": {
            "formula": "tau(X,A,B)=(X^T,B^{-T},A^{-T})",
            "tau_is_involution": True,
            "transpose_normalizes_affine_group": True,
            "transpose_is_inside_affine_group": False,
            "transpose_fixed_matrices": 8,
        },
        "pass_5796_outer_carrier_intertwiner": {
            "factor_swap_bijection": "F(w,x)=(w^T,x^T)",
            "identity": "F(g.p)=tau(g).F(p)",
            "point_stabilizer_translation_intersection_order": len(tp),
            "heavy_stabilizer_translation_intersection_order": len(th),
            "point_type_aggregate_image_span_dimension": image_span_p,
            "heavy_type_aggregate_image_span_dimension": image_span_h,
            "transpose_exchanges_translation_stabilizer_types": True,
            "deduction": "tau is outer and exchanges the two nonconjugate degree-12 carrier types",
        },
        "pass_5797_two_qubit_ring_boundary": {
            "external_prior_art": "Saniga--Planat--Pracna use the noncommutative ring M2(F2), with 16 elements, six units and ten zero-divisors, in projective-ring models of two-qubit Pauli geometry.",
            "exact_repo_bridge": "the q5 Klein-Latin normal 16-space is the additive M2(F2) space and its 576 group is the affine left/right unit action; transpose realizes the carrier-factor swap",
            "not_claimed": "No identification of q5 W33 carrier points with two-qubit observables, projective-ring points, entanglement classes, or physical states is made.",
        },
        "boundary": "Exact finite affine/Latin/group-action theorem. M2(F2) is used here as an additive matrix space with left/right unit action; ring-projective quantum geometry is external prior art and is not imported as a W33 physical identification.",
    }
    OUTPUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print("PASS5792-5799: PASS")
    print("M2(F2):(GL2xGL2) order 576; transpose outer; q5 point/heavy carriers exchanged")


if __name__ == "__main__":
    main()
