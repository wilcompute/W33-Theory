#!/usr/bin/env python3
"""C3 overlap as the qutrit triangle inside the 12-codec.

Previous theorem:
    The line-pair 12-codec is Borel/basis-type, while the tetrahedral 12-codec
    is A4/chiral-type.  They meet through S4=PGL(2,3), with

        S4 = A4 * H,
        H = S3 point stabilizer,
        A4 cap H = C3.

This verifier identifies the geometric meaning of that C3.

On PG(1,3), fix the anchor point [e0].  The stabilizer H=S3 permutes the three
non-anchor points.  The subgroup A4 cap H is the alternating subgroup A3=C3, and
it acts as a 3-cycle on those three non-anchor projective points.

In the Borel lift B<GL(2,3), the preimage of this C3 has order 6 and is cyclic
C6.  Its unipotent C3 part fixes the actual signed anchor e0 and cycles the three
projective non-anchor choices.  On the six signed non-anchor vector choices for
b, this unipotent C3 has two 3-cycles, one for each b-sign.  Adding the central
sign -I gives the full C6, which is transitive on the six signed b choices.

Thus the overlap C3 is exactly the qutrit triangle / three non-anchor choices
inside the input-line 12-codec.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

q = 3
Perm = tuple[int, ...]
Matrix = tuple[tuple[int, int], tuple[int, int]]
Vec = tuple[int, int]


def perm_mul(p: Perm, r: Perm) -> Perm:
    return tuple(p[r[i]] for i in range(len(p)))


def perm_parity(p: Perm) -> int:
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += int(p[i] > p[j])
    return inv % 2


def perm_order(p: Perm) -> int:
    e = tuple(range(len(p)))
    x = e
    for n in range(1, 50):
        x = perm_mul(p, x)
        if x == e:
            return n
    raise RuntimeError("order too large")


def orbit(items, gens, action):
    seen = set(items[:1]) if isinstance(items, list) else {items}
    queue = deque(seen)
    while queue:
        x = queue.popleft()
        for g in gens:
            y = action(g, x)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return seen


def all_s4() -> list[Perm]:
    return list(itertools.permutations(range(4)))


def a4() -> list[Perm]:
    return [p for p in all_s4() if perm_parity(p) == 0]


def point_stabilizer(point: int = 0) -> list[Perm]:
    return [p for p in all_s4() if p[point] == point]


def cycle_decomposition_on_subset(p: Perm, subset: list[int]) -> list[list[int]]:
    subset_set = set(subset)
    seen = set()
    cycles = []
    for x in subset:
        if x in seen:
            continue
        cyc = []
        y = x
        while y not in seen:
            seen.add(y)
            cyc.append(y)
            y = p[y]
        cycles.append(cyc)
    return cycles


def det(M: Matrix) -> int:
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % q


def matmul(A: Matrix, B: Matrix) -> Matrix:
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(2)) % q for j in range(2)) for i in range(2))  # type: ignore[return-value]


def mat_order(M: Matrix) -> int:
    I = ((1, 0), (0, 1))
    x = I
    for n in range(1, 50):
        x = matmul(M, x)
        if x == I:
            return n
    raise RuntimeError("order too large")


def mat_vec(M: Matrix, v: Vec) -> Vec:
    return ((M[0][0] * v[0] + M[0][1] * v[1]) % q, (M[1][0] * v[0] + M[1][1] * v[1]) % q)


def normalize_vec(v: Vec) -> Vec:
    if v[0] % q:
        inv = 1 if v[0] == 1 else 2
    elif v[1] % q:
        inv = 1 if v[1] == 1 else 2
    else:
        raise ValueError("zero")
    return ((inv * v[0]) % q, (inv * v[1]) % q)


def pg13_points() -> list[Vec]:
    return sorted({normalize_vec(v) for v in itertools.product(range(q), repeat=2) if any(v)})


def gl23() -> list[Matrix]:
    return [((a, b), (c, d)) for a, b, c, d in itertools.product(range(q), repeat=4) if det(((a, b), (c, d))) != 0]


def borel() -> list[Matrix]:
    return [M for M in gl23() if M[1][0] == 0]


def action_on_pg_line(M: Matrix) -> Perm:
    pts = pg13_points()
    idx = {p: i for i, p in enumerate(pts)}
    return tuple(idx[normalize_vec(mat_vec(M, x))] for x in pts)


def subgroup_generated_matrix(gens: list[Matrix]) -> set[Matrix]:
    I = ((1, 0), (0, 1))
    G = {I}
    queue = deque([I])
    while queue:
        x = queue.popleft()
        for s in gens:
            y = matmul(s, x)
            if y not in G:
                G.add(y)
                queue.append(y)
    return G


def cycles_of_matrix_action(group: set[Matrix], states: list[Vec]) -> list[int]:
    remaining = set(states)
    sizes = []
    while remaining:
        start = next(iter(remaining))
        seen = {start}
        queue = deque([start])
        while queue:
            x = queue.popleft()
            for g in group:
                y = mat_vec(g, x)
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        sizes.append(len(seen))
        remaining -= seen
    return sorted(sizes)


def build_payload() -> dict:
    S4 = all_s4()
    A4 = a4()
    H = point_stabilizer(0)
    C3 = sorted(set(A4) & set(H))
    non_anchor = [1, 2, 3]
    c3_orders = Counter(perm_order(p) for p in C3)
    non_anchor_orbits = []
    rem = set(non_anchor)
    while rem:
        start = next(iter(rem))
        seen = {start}
        queue = deque([start])
        while queue:
            x = queue.popleft()
            for g in C3:
                y = g[x]
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        non_anchor_orbits.append(sorted(seen))
        rem -= seen

    B = borel()
    B_proj = {action_on_pg_line(M): M for M in B}
    C3_preimage = [M for M in B if action_on_pg_line(M) in C3]
    C3_preimage_orders = Counter(mat_order(M) for M in C3_preimage)
    unipotent = [((1, t), (0, 1)) for t in range(q)]
    unipotent_group = subgroup_generated_matrix(unipotent)
    signed_b_choices = [(x, y) for x, y in itertools.product(range(q), repeat=2) if y != 0]
    projective_b_choices = sorted({normalize_vec(v) for v in signed_b_choices})
    central_minus = ((2, 0), (0, 2))
    c6_generated = subgroup_generated_matrix([((1, 1), (0, 1)), central_minus])

    unipotent_signed_orbits = cycles_of_matrix_action(unipotent_group, signed_b_choices)
    c6_signed_orbits = cycles_of_matrix_action(c6_generated, signed_b_choices)

    identities = {
        "C3_overlap_order_3": len(C3) == 3,
        "C3_order_distribution": c3_orders == {1: 1, 3: 2},
        "C3_transitive_on_three_non_anchor_points": non_anchor_orbits == [[1, 2, 3]],
        "Borel_order_12": len(B) == 12,
        "preimage_of_C3_has_order_6": len(C3_preimage) == 6,
        "preimage_order_distribution_C6": C3_preimage_orders == {1: 1, 2: 1, 3: 2, 6: 2},
        "unipotent_C3_order_3": len(unipotent_group) == 3,
        "signed_b_choices_6": len(signed_b_choices) == 6 and len(projective_b_choices) == 3,
        "unipotent_has_two_3_cycles_on_signed_b": unipotent_signed_orbits == [3, 3],
        "central_extended_C6_transitive_on_six_signed_b": len(c6_generated) == 6 and c6_signed_orbits == [6],
    }
    return {
        "theorem": "c3_overlap_triangle_codec",
        "projective_overlap": {
            "description": "C3 = A4 ∩ S3 inside S4=PGL(2,3)",
            "order": len(C3),
            "element_order_distribution": dict(c3_orders),
            "non_anchor_points": non_anchor,
            "orbits_on_non_anchor_points": non_anchor_orbits,
            "meaning": "C3 is the cyclic rotation of the three non-anchor points on PG(1,3).",
        },
        "borel_lift": {
            "preimage_order": len(C3_preimage),
            "preimage_element_order_distribution": dict(C3_preimage_orders),
            "unipotent_C3_order": len(unipotent_group),
            "signed_b_choices": signed_b_choices,
            "projective_b_choices": projective_b_choices,
            "unipotent_orbit_sizes_on_signed_b": unipotent_signed_orbits,
            "central_extended_C6_orbit_sizes_on_signed_b": c6_signed_orbits,
        },
        "interpretation": "The C3 overlap is the qutrit triangle of three non-anchor projective b-choices. Its unipotent lift preserves b-sign and gives two 3-cycles; adjoining central sign gives C6, transitive on the six signed b choices in the 12-codec.",
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_c3_overlap_triangle_codec.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
