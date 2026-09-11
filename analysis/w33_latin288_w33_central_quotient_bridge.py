#!/usr/bin/env python3
"""Latin-288 / W33 central-quotient bridge.

This resolves the open 576/Latin comparison at the correct structural level.
The 576 labelled order-four Latin squares are NOT a regular W33 576-set; an
older certificate already rules that out.  The right bridge is instead between
an index-two subgroup of the V4 Latin-square stabilizer and a central quotient
of the W33 minimum-vector stabilizer.

For the Klein four Latin square L(r,c)=r+c over F2^2:

  * its full standard paratopy stabilizer has order 576 and is exactly
        C2^4 : (S3 x S3);
  * the subgroup using only even coordinate parastrophes has order 288 and is
        C2^4 : (S3 x C3);
  * an explicit GL(4,2) matrix conjugates this affine 288-group to the standard
        A4 wr C2 = (A4 x A4) : C2 action.

The independently certified W33 minimum-vector stabilizer H has

        H ~= 2^{1+4}_+ : (S3 x C3),
        H/Z(H) ~= A4 wr C2.

Hence the Latin orientation-even stabilizer is explicitly isomorphic to the W33
central quotient H/Z(H).

There is a deeper common quadratic geometry.  The Latin translation kernel is

        N = F2^2 tensor F2^2 ~= M2(F2),

and q(X)=det(X) is invariant under the full S3 x S3 linear complement.  It is
the plus-type 4-dimensional quadratic form: 10 zeros (including 0), 6 nonsingular
vectors, nondegenerate polar form, and six generator lines arranged in two
rulings.  The ruling-preserving isometry group has order 36 = S3 x S3; adjoining
matrix transpose gives all 72 isometries of O^+(4,2).

An explicit central extension of N with factor set

        f(x,y)=x0*y3 + x1*y2

has square map q, center/derived group C2, and element-order census
1^1 2^19 4^12.  It is therefore the extraspecial plus group 2^{1+4}_+, matching
the exact W33 O_2(H) certificate.

Thus the common 288 core B admits two different 576 completions:

  Latin:  B < L = N : (S3 x S3),                 [L:B]=2, split outer doubling
  W33:    1 -> C2 -> H -> B -> 1,               non-split central phase doubling

where the W33 nonsplitting already occurs on 2^{1+4}_+ -> C2^4.

A separate 144 result is also recorded honestly: the small V4 Latin main class
is a regular torsor for S4 x S3 after fixing one column gauge.  That natural
144-group is not A4 x A4 (their derived orders are 36 and 16), so the equality
144=|H^+/Z(H)| is not promoted here.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_latin288_w33_central_quotient_bridge.json"


def parity(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) & 1


def pcompose(g, h):
    return tuple(g[h[i]] for i in range(len(h)))


def pinverse(g):
    out = [0] * len(g)
    for i, j in enumerate(g):
        out[j] = i
    return tuple(out)


def porder(g):
    e = tuple(range(len(g)))
    x = e
    for n in range(1, 65):
        x = pcompose(g, x)
        if x == e:
            return n
    raise AssertionError("order bound")


def generated_perm_group(gens, npts):
    e = tuple(range(npts))
    gens = list(gens)
    if not gens:
        return {e}
    pool = gens + [pinverse(g) for g in gens]
    seen = {e}
    stack = [e]
    while stack:
        x = stack.pop()
        for g in pool:
            y = pcompose(g, x)
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def center_order(group):
    G = list(group)
    return sum(all(pcompose(g, h) == pcompose(h, g) for h in G) for g in G)


def derived_order(group):
    G = list(group)
    comms = set()
    for g in G:
        gi = pinverse(g)
        for h in G:
            hi = pinverse(h)
            comms.add(pcompose(pcompose(pcompose(gi, hi), g), h))
    return len(generated_perm_group(comms, len(G[0])))


def bits2(i):
    return ((i >> 1) & 1, i & 1)


def vadd(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def mat_vec(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(len(v))) & 1 for i in range(len(M)))


def mat_mul(A, B):
    return tuple(
        tuple(sum(A[i][k] * B[k][j] for k in range(len(B))) & 1 for j in range(len(B[0])))
        for i in range(len(A))
    )


def eye(n):
    return tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))


def kron(A, B):
    ra, ca = len(A), len(A[0])
    rb, cb = len(B), len(B[0])
    return tuple(
        tuple(A[i // rb][j // cb] * B[i % rb][j % cb] for j in range(ca * cb))
        for i in range(ra * rb)
    )


def inv_mat(M):
    n = len(M)
    A = [list(M[i]) + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    r = 0
    for c in range(n):
        pivot = next(i for i in range(r, n) if A[i][c])
        A[r], A[pivot] = A[pivot], A[r]
        for i in range(n):
            if i != r and A[i][c]:
                A[i] = [x ^ y for x, y in zip(A[i], A[r])]
        r += 1
    return tuple(tuple(row[n:]) for row in A)


def generated_matrix_group(gens):
    e = eye(4)
    seen = {e}
    stack = [e]
    while stack:
        x = stack.pop()
        for g in gens:
            y = mat_mul(g, x)
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


V2 = tuple(itertools.product((0, 1), repeat=2))
V4 = tuple(itertools.product((0, 1), repeat=4))
GL2 = []
for rows in itertools.product(tuple(itertools.product((0, 1), repeat=2)), repeat=2):
    A = tuple(rows)
    if len({mat_vec(A, v) for v in V2}) == 4:
        GL2.append(A)
GL2 = tuple(GL2)

S4 = tuple(itertools.permutations(range(4)))
S3 = tuple(itertools.permutations(range(3)))
ID4 = tuple(range(4))
ID3 = tuple(range(3))
LATIN = tuple(r ^ c for r in range(4) for c in range(4))


def paratopy(square, rp, cp, sp, coord):
    out = [None] * 16
    for r in range(4):
        for c in range(4):
            t = (rp[r], cp[c], sp[square[4 * r + c]])
            u = (t[coord[0]], t[coord[1]], t[coord[2]])
            out[4 * u[0] + u[1]] = u[2]
    return tuple(out)


def induced_cell_perm(element):
    rp, cp, sp, coord = element
    out = [None] * 16
    for r in range(4):
        for c in range(4):
            t = (rp[r], cp[c], sp[LATIN[4 * r + c]])
            u = (t[coord[0]], t[coord[1]], t[coord[2]])
            assert LATIN[4 * u[0] + u[1]] == u[2]
            out[4 * r + c] = 4 * u[0] + u[1]
    return tuple(out)


def affine_perm(M, t, cell_vecs, cell_index):
    return tuple(cell_index[vadd(mat_vec(M, v), t)] for v in cell_vecs)


def qdet(v):
    a, b, c, d = v
    return (a & d) ^ (b & c)


def build_result():
    assert len(GL2) == 6

    stab = []
    for rp in S4:
        for cp in S4:
            for sp in S4:
                for coord in S3:
                    if paratopy(LATIN, rp, cp, sp, coord) == LATIN:
                        stab.append((rp, cp, sp, coord))
    full = {induced_cell_perm(e) for e in stab}
    even = {induced_cell_perm(e) for e in stab if parity(e[3]) == 0}
    assert len(stab) == len(full) == 576
    assert len(even) == 288
    assert Counter(parity(e[3]) for e in stab) == {0: 288, 1: 288}

    cell_vecs = tuple(bits2(r) + bits2(c) for r in range(4) for c in range(4))
    cell_index = {v: i for i, v in enumerate(cell_vecs)}
    I2 = eye(2)
    C3 = ((0, 1), (1, 1))
    C3sq = mat_mul(C3, C3)
    k_even = {kron(B, A) for A in GL2 for B in (I2, C3, C3sq)}
    k_full = {kron(B, A) for A in GL2 for B in GL2}
    assert len(k_even) == 18 and len(k_full) == 36

    aff_even = {affine_perm(M, t, cell_vecs, cell_index) for M in k_even for t in cell_vecs}
    aff_full = {affine_perm(M, t, cell_vecs, cell_index) for M in k_full for t in cell_vecs}
    assert aff_even == even
    assert aff_full == full

    # Standard A4 wr C2 = (V4:C3)^2 : swap.
    Z2 = ((0, 0), (0, 0))

    def block2(A, B, C, D):
        return (A[0] + B[0], A[1] + B[1], C[0] + D[0], C[1] + D[1])

    u = block2(C3, Z2, Z2, I2)
    v = block2(I2, Z2, Z2, C3)
    swap = block2(Z2, I2, I2, Z2)
    k_wreath = generated_matrix_group((u, v, swap))
    wreath = {affine_perm(M, t, cell_vecs, cell_index) for M in k_wreath for t in cell_vecs}
    assert len(k_wreath) == 18 and len(wreath) == 288

    # Explicit affine intertwiner Latin-even -> A4 wr C2.
    P = (
        (0, 1, 1, 0),
        (1, 0, 1, 1),
        (0, 1, 1, 1),
        (1, 1, 1, 0),
    )
    Pinv = inv_mat(P)
    assert {mat_mul(mat_mul(P, M), Pinv) for M in k_even} == k_wreath
    conj = tuple(cell_index[mat_vec(P, x)] for x in cell_vecs)
    conj_inv = pinverse(conj)
    assert {pcompose(pcompose(conj, g), conj_inv) for g in even} == wreath

    # Plus quadratic geometry q=det on M2(F2).
    q_hist = Counter(qdet(x) for x in cell_vecs)
    assert q_hist == {0: 10, 1: 6}
    assert all(qdet(mat_vec(M, x)) == qdet(x) for M in k_full for x in cell_vecs)
    basis = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    polar = tuple(tuple(qdet(vadd(x, y)) ^ qdet(x) ^ qdet(y) for y in basis) for x in basis)
    assert mat_mul(polar, polar) == eye(4)  # nondegenerate

    zero = (0, 0, 0, 0)
    nonzero = [x for x in cell_vecs if x != zero]
    planes = set()
    for a, b in itertools.combinations(nonzero, 2):
        S = frozenset((zero, a, b, vadd(a, b)))
        if len(S) == 4:
            planes.add(S)
    singular_planes = [S for S in planes if all(qdet(x) == 0 for x in S)]
    assert len(singular_planes) == 6

    # Transpose swaps the two rulings.  k_full is the 36-element ruling-preserving
    # subgroup; adding transpose gives 72 isometries, which saturates the upper
    # bound 3!*3!*2 from the two triples of generator lines.
    transpose = ((1, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 0), (0, 0, 0, 1))
    oplus = generated_matrix_group(tuple(k_full) + (transpose,))
    assert len(oplus) == 72
    assert all(qdet(mat_vec(M, x)) == qdet(x) for M in oplus for x in cell_vecs)

    # Explicit extraspecial plus lift with square map q.
    def factor(x, y):
        return (x[0] & y[3]) ^ (x[1] & y[2])

    def emul(a, b):
        z, x = a[0], a[1:]
        w, y = b[0], b[1:]
        return (z ^ w ^ factor(x, y),) + vadd(x, y)

    E = tuple((z,) + x for z in (0, 1) for x in cell_vecs)
    eid = (0, 0, 0, 0, 0)

    def epow(x, n):
        out = eid
        for _ in range(n):
            out = emul(out, x)
        return out

    def eorder(x):
        for n in range(1, 9):
            if epow(x, n) == eid:
                return n
        raise AssertionError("extraspecial order bound")

    def einverse(x):
        return next(y for y in E if emul(x, y) == eid and emul(y, x) == eid)

    def ecomm(x, y):
        return emul(emul(emul(einverse(x), einverse(y)), x), y)

    ecenter = tuple(x for x in E if all(emul(x, y) == emul(y, x) for y in E))
    ecomms = {ecomm(x, y) for x in E for y in E}
    eorders = Counter(eorder(x) for x in E)
    assert len(ecenter) == 2 and ecomms == set(ecenter)
    assert eorders == {1: 1, 2: 19, 4: 12}
    assert all(emul((0,) + x, (0,) + x)[0] == qdet(x) for x in cell_vecs)

    # Resolve the 144 residual target separately: a distinguished-column gauge
    # gives a regular S4 x S3 torsor on the whole small main class.
    s3_fix0 = tuple(p for p in S4 if p[0] == 0)
    torsor_orbit = {
        paratopy(LATIN, rp, cp, ID4, ID3)
        for rp in S4 for cp in s3_fix0
    }
    full_paratopy_order = 24 ** 3 * 6
    main_class_size = full_paratopy_order // len(stab)
    assert len(s3_fix0) == 6
    assert main_class_size == len(torsor_orbit) == 144

    # Independent W33 certificate.
    w33 = json.loads(
        (ROOT / "data" / "PART_W33_20260828_MINIMUM_STABILIZER_576_STRUCTURE.json")
        .read_text(encoding="utf-8")
    )
    assert w33["status"] == "PASS"
    unsigned = w33["unsignedStabilizer"]
    o2 = unsigned["normalExtraspecial2Subgroup"]
    assert unsigned["order"] == 576
    assert unsigned["structure"] == "2^{1+4}_+ semidirect (S3 x C3)"
    assert unsigned["centerOrder"] == 2
    assert unsigned["derivedOrder"] == 96
    assert "A4 wr C2" in unsigned["quotientReading"]
    assert o2["order"] == 32 and o2["type"] == "extraspecial plus"
    assert o2["centerOrder"] == o2["derivedOrder"] == 2
    assert o2["abelianization"] == "C2^4"
    assert o2["elementOrderCensus"] == {"1": 1, "2": 19, "4": 12}

    full_orders = Counter(porder(g) for g in full)
    even_orders = Counter(porder(g) for g in even)
    full_center = center_order(full)
    even_center = center_order(even)
    full_derived = derived_order(full)
    even_derived = derived_order(even)

    checks = {
        "v4_latin_full_stabilizer_order576": len(full) == 576,
        "latin_even_coordinate_kernel_order288": len(even) == 288,
        "latin_full_equals_affine_C2_4_by_S3xS3": aff_full == full and len(k_full) == 36,
        "latin_even_equals_affine_C2_4_by_S3xC3": aff_even == even and len(k_even) == 18,
        "explicit_GL4_conjugator_to_A4_wr_C2": {pcompose(pcompose(conj, g), conj_inv) for g in even} == wreath,
        "w33_central_quotient_is_A4_wr_C2": "A4 wr C2" in unsigned["quotientReading"],
        "latin_even_matches_w33_central_quotient": len(even) == 288 and len(wreath) == 288,
        "determinant_is_plus_quadratic_form": q_hist == {0: 10, 1: 6} and mat_mul(polar, polar) == eye(4),
        "latin_full_linear_complement_preserves_q": all(qdet(mat_vec(M, x)) == qdet(x) for M in k_full for x in cell_vecs),
        "Oplus4_2_order72_recovered": len(oplus) == 72,
        "explicit_extraspecial_plus_lift_matches_w33_O2_profile": eorders == {1: 1, 2: 19, 4: 12} and len(ecenter) == 2 and o2["elementOrderCensus"] == {"1": 1, "2": 19, "4": 12},
        "latin_and_w33_full_576_groups_are_not_isomorphic": full_center != unsigned["centerOrder"] and full_derived != unsigned["derivedOrder"],
        "small_main_class_is_regular_S4xS3_torsor": main_class_size == len(torsor_orbit) == 144,
    }

    return {
        "schema": "w33.latin288-w33-central-quotient-bridge.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The orientation-even stabilizer of the Klein-four Latin square is explicitly "
            "conjugate to A4 wr C2, hence to the certified W33 quotient H/Z(H).  The shared "
            "C2^4 kernel is M2(F2) with plus quadratic form det, and its explicit extraspecial "
            "central lift has exactly the W33 2^{1+4}_+ profile."
        ),
        "latin_stabilizers": {
            "full_standard_paratopy_group_order": full_paratopy_order,
            "V4_main_class_size": main_class_size,
            "full_stabilizer_order": len(full),
            "full_structure": "C2^4 semidirect (S3 x S3)",
            "full_center_order": full_center,
            "full_derived_order": full_derived,
            "full_element_order_census": {str(k): v for k, v in sorted(full_orders.items())},
            "orientation_even_stabilizer_order": len(even),
            "orientation_even_structure": "C2^4 semidirect (S3 x C3)",
            "orientation_even_center_order": even_center,
            "orientation_even_derived_order": even_derived,
            "orientation_even_element_order_census": {str(k): v for k, v in sorted(even_orders.items())},
            "orientation_character": "parity of the S3 coordinate parastrophe",
            "split_outer_doubling": "L576 = L288 semidirect C2, using any odd coordinate transposition",
        },
        "common_288": {
            "latin_model": "C2^4 semidirect (S3 x C3)",
            "standard_model": "A4 wr C2 = (A4 x A4) semidirect C2",
            "W33_model": "H576/Z(H576)",
            "explicit_GL4_conjugator": [list(row) for row in P],
            "explicit_16_point_conjugator_zero_based": list(conj),
            "linear_complement_orders": {"latin": len(k_even), "wreath": len(k_wreath)},
            "affine_group_order": len(even),
            "proof": "P K_latin P^-1 = K_wreath and the same P transports all 16 translations, so it conjugates the full affine groups on 16 points.",
        },
        "plus_quadratic_geometry": {
            "carrier": "N=C2^4=F2^2 tensor F2^2=M2(F2)",
            "quadratic_form": "q([[a,b],[c,d]])=ad+bc=det over F2",
            "q_value_histogram": {str(k): v for k, v in sorted(q_hist.items())},
            "polar_matrix": [list(row) for row in polar],
            "nonzero_singular_points": 9,
            "nonsingular_points": 6,
            "generator_lines": len(singular_planes),
            "rulings": "two triples of generator lines; same-ruling lines are disjoint and opposite-ruling lines meet once",
            "ruling_preserving_group": "S3 x S3, order 36",
            "full_orthogonal_group": "O^+(4,2) = (S3 x S3) : C2, order 72",
            "transpose_role": "matrix transpose exchanges the two rulings",
        },
        "extraspecial_plus_lift": {
            "factor_set": "f(x,y)=x0*y3+x1*y2 mod2",
            "order": len(E),
            "center_order": len(ecenter),
            "derived_order": len(ecomms),
            "abelianization": "C2^4",
            "element_order_census": {str(k): v for k, v in sorted(eorders.items())},
            "square_map": "(0,x)^2 = z^{q(x)}",
            "isomorphism_class": "2^{1+4}_+",
            "W33_match": "same unique plus-type extraspecial order-32 class and exact element-order profile as O_2(H)",
        },
        "crossed_576_completions": {
            "common_core": "B288 ~= A4 wr C2 ~= C2^4:(S3 x C3)",
            "Latin": "B288 < L576=C2^4:(S3 x S3), split index-two outer/orientation extension",
            "W33": "1 -> C2 -> H576=2^{1+4}_+:(S3 x C3) -> B288 -> 1",
            "W33_extension_nonsplit": "restriction to 2^{1+4}_+ -> C2^4 is extraspecial and nonabelian, so no C2^4 complement can split the central extension",
            "reading": "Latin doubles the complement (restores an odd ruling reflection); W33 doubles the kernel (adds a central extraspecial phase) while sharing the same 288 quotient geometry.",
        },
        "latin_144_resolution": {
            "main_class_size": main_class_size,
            "regular_torsor_group": "S4 x S3",
            "gauge": "arbitrary row permutation x column permutation fixing column label 0; symbols and coordinate order fixed",
            "orbit_size": len(torsor_orbit),
            "regular": len(torsor_orbit) == 24 * 6,
            "not_A4xA4_by_derived_order": "(S4 x S3)' has order 36, whereas (A4 x A4)'=V4 x V4 has order 16",
            "boundary": "This identifies a natural regular 144 action; it does not prove that no other A4 x A4 regular subgroup exists inside the full paratopy action.",
        },
        "claim_boundary": [
            "The Latin-even to A4 wr C2 bridge is an explicit permutation-group conjugacy, not an order coincidence.",
            "The identification with W33 uses the independently certified abstract quotient H/Z(H) ~= A4 wr C2; no conjugator to the original 25,920-point PSp permutation labels is asserted here.",
            "The extraspecial lift is an explicit model of the unique plus-type order-32 class matching W33 O_2(H); equality of embedded subgroups is not claimed.",
            "The crossed-completion language is finite group theory. No physical phase interpretation is added beyond the existing controller/group-theoretic use of the central bit.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "latin_even": result["latin_stabilizers"]["orientation_even_stabilizer_order"],
        "common_core": result["crossed_576_completions"]["common_core"],
        "q": result["plus_quadratic_geometry"]["quadratic_form"],
        "extraspecial": result["extraspecial_plus_lift"]["isomorphism_class"],
        "main144": result["latin_144_resolution"]["regular_torsor_group"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
