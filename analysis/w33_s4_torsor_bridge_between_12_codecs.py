#!/usr/bin/env python3
"""S4 torsor bridge between the two 12-codecs.

Previous theorem showed:
  - line-pair 12-codec = Borel subgroup B < GL(2,3), order 12,
    projectivizing to S3, a point stabilizer in PGL(2,3) ~= S4;
  - tetrahedral chiral 12-codec = A4 < S4;
  - B and A4 are not isomorphic as groups.

This verifier identifies the correct bridge.

Both 12-codecs are regular torsors, but for different groups:
  - B acts simply transitively on signed anchored bases of PG(1,3);
  - A4 acts simply transitively on oriented tetrahedral flags.

They meet in the same ambient four-point geometry S4=PGL(2,3).  If H=S3 is the
point stabilizer, then

    S4 = A4 H,
    A4 cap H = C3,

so each element of S4 has exactly 3 decompositions a*h.  The bridge between the
Borel/basis 12 and alternating/chiral 12 is therefore a 3-fold S4 incidence
correspondence, not a canonical group isomorphism.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

q = 3
Perm = tuple[int, ...]
Matrix = tuple[tuple[int, int], tuple[int, int]]


def perm_mul(p: Perm, r: Perm) -> Perm:
    return tuple(p[r[i]] for i in range(len(p)))


def perm_inv(p: Perm) -> Perm:
    out = [0] * len(p)
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def perm_parity(p: Perm) -> int:
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += int(p[i] > p[j])
    return inv % 2


def all_s4() -> list[Perm]:
    return list(itertools.permutations(range(4)))


def a4() -> list[Perm]:
    return [p for p in all_s4() if perm_parity(p) == 0]


def point_stabilizer(point: int = 0) -> list[Perm]:
    return [p for p in all_s4() if p[point] == point]


def det(M: Matrix) -> int:
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % q


def matmul(A: Matrix, B: Matrix) -> Matrix:
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) % q for j in range(2)) for i in range(2))  # type: ignore[return-value]


def gl23() -> list[Matrix]:
    return [((a, b), (c, d)) for a, b, c, d in itertools.product(range(q), repeat=4) if det(((a, b), (c, d))) != 0]


def borel() -> list[Matrix]:
    return [M for M in gl23() if M[1][0] == 0]


def normalize_vec(v: tuple[int, int]) -> tuple[int, int]:
    if v[0] % q:
        inv = 1 if v[0] == 1 else 2
    elif v[1] % q:
        inv = 1 if v[1] == 1 else 2
    else:
        raise ValueError("zero")
    return ((inv * v[0]) % q, (inv * v[1]) % q)


def pg13_points() -> list[tuple[int, int]]:
    return sorted({normalize_vec(v) for v in itertools.product(range(q), repeat=2) if any(v)})


def action_on_pg_line(M: Matrix) -> Perm:
    pts = pg13_points()
    idx = {p: i for i, p in enumerate(pts)}
    image = []
    for x in pts:
        y = ((M[0][0] * x[0] + M[0][1] * x[1]) % q, (M[1][0] * x[0] + M[1][1] * x[1]) % q)
        image.append(idx[normalize_vec(y)])
    return tuple(image)


def orbit_action_regular(group: list[Perm], state_set: list[Perm], base: Perm) -> bool:
    images = [perm_mul(g, base) for g in group]
    return len(images) == len(set(images)) == len(state_set) and set(images) == set(state_set)


def build_payload() -> dict:
    S4 = all_s4()
    A4 = a4()
    H = point_stabilizer(0)
    inter = sorted(set(A4) & set(H))
    products = Counter(perm_mul(a, h) for a in A4 for h in H)

    B = borel()
    B_proj = sorted({action_on_pg_line(M) for M in B})
    PGL = sorted({action_on_pg_line(M) for M in gl23()})
    kernel_sizes = Counter(action_on_pg_line(M) for M in B)

    # Oriented tetrahedral flags: identify them with A4 images of a base oriented flag.
    # As a torsor this is exactly A4 with left multiplication.
    oriented_flags = A4
    base_flag = tuple(range(4))
    a4_regular = orbit_action_regular(A4, oriented_flags, base_flag)

    # Signed anchored line-bases: identify them with B itself. Left multiplication is regular.
    B_products = Counter(matmul(g, h) for g in B for h in B)
    b_left_regular = all(Counter(matmul(g, h) for g in B).values() == Counter({1: len(B)}).values() for h in B)
    # Simpler exact regularity check: each left orbit from each h has all 12 states once.
    b_left_regular = all(len({matmul(g, h) for g in B}) == len(B) for h in B)

    identities = {
        "S4_order_24": len(S4) == 24,
        "A4_order_12": len(A4) == 12,
        "H_point_stabilizer_order_6": len(H) == 6,
        "intersection_A4_H_is_C3_order_3": len(inter) == 3,
        "S4_equals_A4_H": len(products) == 24 and set(products) == set(S4),
        "each_S4_element_has_3_decompositions": set(products.values()) == {3},
        "PGL23_is_S4": len(PGL) == 24,
        "Borel_order_12": len(B) == 12,
        "Borel_projectivizes_to_H_order_6": set(B_proj) == set(H) and len(B_proj) == 6,
        "Borel_kernel_over_H_has_size_2": set(kernel_sizes.values()) == {2},
        "A4_regular_on_oriented_flags": a4_regular,
        "Borel_regular_on_signed_anchored_bases": b_left_regular,
    }
    return {
        "theorem": "s4_torsor_bridge_between_12_codecs",
        "ambient_geometry": {
            "PGL23_order": len(PGL),
            "S4_order": len(S4),
            "statement": "PGL(2,3) acts on the four points of PG(1,3), hence realizes S4.",
        },
        "tetrahedral_chiral_torsor": {
            "group": "A4",
            "order": len(A4),
            "regular_on_oriented_flags": a4_regular,
        },
        "line_basis_torsor": {
            "group": "Borel subgroup of GL(2,3)",
            "order": len(B),
            "projective_image": "H=S3 point stabilizer in S4",
            "projective_image_order": len(B_proj),
            "kernel_size_over_projective_image": sorted(set(kernel_sizes.values())),
            "regular_on_signed_anchored_bases": b_left_regular,
        },
        "s4_incidence_bridge": {
            "H_point_stabilizer_order": len(H),
            "A4_intersection_H_order": len(inter),
            "factorization": "S4 = A4 * H",
            "decompositions_per_S4_element": sorted(set(products.values())),
            "interpretation": "The bridge from A4 chirality to Borel basis data is a 3-fold S4 incidence correspondence through the common C3=A4∩H, not a group isomorphism.",
        },
        "conclusion": "The recurring 12 splits into two non-isomorphic regular torsors. A4 supplies tetrahedral chirality; Borel supplies signed anchored line bases. The ambient S4=PGL(2,3) relates them by the factorization S4=A4H with C3 overlap.",
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_s4_torsor_bridge_between_12_codecs.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
