#!/usr/bin/env python3
"""Compare the line-pair 12-codec with the tetrahedral chiral 12-codec.

Previous result:
    The 12 states over an anchored disjoint line pair are choices of an ordered
    input-line basis (a,b) where [a] is fixed and b is not proportional to a.

This verifier identifies the native group law of that 12-state line codec.

On the input projective line PG(1,3), choose coordinates with anchor [e0].
The 12 choices (a,b) are exactly the invertible 2x2 matrices whose first column
is a nonzero multiple of e0:

    B = { [[alpha, x], [0, delta]] : alpha, delta in F3^*, x in F3 }.

So the line codec is the Borel point-stabilizer of GL(2,3), order 12.
Its structure is C2 x S3.  Projectivizing by the central +/-I gives S3, the
stabilizer of one point in PGL(2,3) ~= S4.

The tetrahedral chiral 12-codec, by contrast, is A4, the even permutations of
four vertices.  These two order-12 groups are not isomorphic:

    B has a central element of order 2 and elements of order 6;
    A4 has trivial center and no elements of order 6.

Therefore the two 12-codecs are not canonically the same as groups.  They are
linked through the ambient tetrahedral/projective group PGL(2,3) ~= S4:

    line codec projectivizes to an S3 vertex stabilizer in S4;
    tetrahedral chirality is the A4 even subgroup of S4.

This is a useful correction: the recurring 12 is real, but it appears in two
native forms, Borel/basis and alternating/chiral.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

q = 3

Matrix = tuple[tuple[int, int], tuple[int, int]]
Perm = tuple[int, ...]


def det(M: Matrix) -> int:
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % q


def matmul(A: Matrix, B: Matrix) -> Matrix:
    return tuple(
        tuple(sum(A[i][k] * B[k][j] for k in range(2)) % q for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def eye() -> Matrix:
    return ((1, 0), (0, 1))


def gl23() -> list[Matrix]:
    return [((a, b), (c, d)) for a, b, c, d in itertools.product(range(q), repeat=4) if det(((a, b), (c, d))) != 0]


def borel_anchor_stabilizer() -> list[Matrix]:
    return [M for M in gl23() if M[1][0] == 0]


def mat_order(M: Matrix) -> int:
    x = eye()
    for n in range(1, 100):
        x = matmul(M, x)
        if x == eye():
            return n
    raise RuntimeError("order too large")


def center(group: list[Matrix]) -> list[Matrix]:
    return [g for g in group if all(matmul(g, h) == matmul(h, g) for h in group)]


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


def perm_mul(p: Perm, r: Perm) -> Perm:
    return tuple(p[r[i]] for i in range(len(p)))


def perm_order(p: Perm) -> int:
    e = tuple(range(len(p)))
    x = e
    for n in range(1, 100):
        x = perm_mul(p, x)
        if x == e:
            return n
    raise RuntimeError("order too large")


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


def perm_center(group: list[Perm]) -> list[Perm]:
    return [g for g in group if all(perm_mul(g, h) == perm_mul(h, g) for h in group)]


def subgroup_generated(gens: list[Perm]) -> set[Perm]:
    e = tuple(range(4))
    G = {e}
    queue = deque([e])
    while queue:
        x = queue.popleft()
        for s in gens:
            y = perm_mul(s, x)
            if y not in G:
                G.add(y)
                queue.append(y)
    return G


def build_payload() -> dict:
    B = borel_anchor_stabilizer()
    B_orders = Counter(mat_order(g) for g in B)
    B_center = center(B)
    PGL_image = sorted({action_on_pg_line(M) for M in gl23()})
    B_proj = sorted({action_on_pg_line(M) for M in B})
    A4 = a4()
    A4_orders = Counter(perm_order(g) for g in A4)
    A4_center = perm_center(A4)

    fixed_point = action_on_pg_line(B[0])[0]  # B fixes projective point index 0 by construction with sorted coords.
    B_proj_fixed_sets = Counter(tuple(i for i in range(4) if p[i] == i) for p in B_proj)

    identities = {
        "GL23_order_48": len(gl23()) == 48,
        "PGL23_image_order_24": len(PGL_image) == 24,
        "PGL23_is_S4_by_order_on_4_points": len(PGL_image) == len(all_s4()) == 24,
        "Borel_order_12": len(B) == 12,
        "Borel_projective_image_order_6": len(B_proj) == 6,
        "Borel_center_order_2": len(B_center) == 2,
        "Borel_has_order_6_elements": B_orders[6] > 0,
        "A4_order_12": len(A4) == 12,
        "A4_center_trivial": len(A4_center) == 1,
        "A4_has_no_order_6_elements": A4_orders[6] == 0,
        "Borel_not_isomorphic_to_A4_by_invariants": len(B_center) != len(A4_center) and B_orders[6] > 0 and A4_orders[6] == 0,
    }
    return {
        "theorem": "line_codec_vs_tetrahedral_chirality",
        "line_codec_group": {
            "description": "Borel subgroup of GL(2,3) fixing the projective anchor [e0] on PG(1,3)",
            "order": len(B),
            "element_order_distribution": dict(B_orders),
            "center_size": len(B_center),
            "center": B_center,
            "structure": "C2 x S3",
            "projective_image_order": len(B_proj),
            "projective_image": "S3 point stabilizer inside PGL(2,3) ~= S4",
        },
        "tetrahedral_chiral_group": {
            "description": "A4, the even permutations / chiral rotations of the tetrahedron",
            "order": len(A4),
            "element_order_distribution": dict(A4_orders),
            "center_size": len(A4_center),
            "center": A4_center,
            "structure": "A4",
        },
        "ambient_bridge": {
            "PGL23_order": len(PGL_image),
            "PGL23_identification": "PGL(2,3) acts faithfully on the four points of PG(1,3), hence is S4",
            "line_codec_role": "preimage in GL(2,3) of an S3 point stabilizer in S4",
            "tetrahedral_role": "A4 even/chiral subgroup of S4",
        },
        "comparison": "The two 12-codecs are not isomorphic as native groups. The line-pair codec is Borel/basis-type; the tetrahedral codec is alternating/chiral-type. They meet in the ambient S4=PGL(2,3) geometry but should not be identified without specifying a noncanonical torsor bijection or extra structure.",
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_line_codec_vs_tetrahedral_chirality.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
