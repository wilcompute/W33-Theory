#!/usr/bin/env python3
"""C3 overlap as oriented Fano-line triangle.

Previous theorem identified C3=A4∩S3 as the cyclic rotation of the three
non-anchor points on PG(1,3).  This file makes the careful Fano bridge.

The bridge is not an equality of fields F3 and F2.  It is an equality of the
three-point oriented incidence object:

    non-anchor points of PG(1,3) with C3 cyclic orientation
        ~=
    nonzero vectors of F2^2 on one Fano line, with orientation-preserving C3.

For F2^2, the three nonzero vectors {u,v,w} obey the Fano triple law

    u + v + w = 0,
    u + v = w,
    v + w = u,
    w + u = v.

The full automorphism group of this Fano line is GL(2,2)=S3.  The overlap C3 is
its orientation-preserving subgroup A3.  Thus the qutrit triangle from PG(1,3)
can carry the same oriented Fano-line wedge/dot cyclic order after choosing an
orientation; transpositions are the orientation-reversing dot/dual flips.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

Perm = tuple[int, ...]
Vec2 = tuple[int, int]


def perm_mul(p: Perm, r: Perm) -> Perm:
    return tuple(p[r[i]] for i in range(len(p)))


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


def restrict_to_nonanchor(p: Perm, nonanchor=(1, 2, 3)) -> Perm:
    idx = {x: i for i, x in enumerate(nonanchor)}
    return tuple(idx[p[x]] for x in nonanchor)


def add2(a: Vec2, b: Vec2) -> Vec2:
    return ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)


def det2(M: tuple[Vec2, Vec2]) -> int:
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % 2


def gl22() -> list[tuple[Vec2, Vec2]]:
    return [((a, b), (c, d)) for a, b, c, d in itertools.product(range(2), repeat=4) if det2(((a, b), (c, d))) == 1]


def mat_vec(M: tuple[Vec2, Vec2], v: Vec2) -> Vec2:
    return ((M[0][0] * v[0] + M[0][1] * v[1]) % 2, (M[1][0] * v[0] + M[1][1] * v[1]) % 2)


def action_gl22_on_nonzero(M: tuple[Vec2, Vec2], basis: list[Vec2]) -> Perm:
    idx = {v: i for i, v in enumerate(basis)}
    return tuple(idx[mat_vec(M, v)] for v in basis)


def perm_order(p: Perm) -> int:
    e = tuple(range(len(p)))
    x = e
    for n in range(1, 20):
        x = perm_mul(p, x)
        if x == e:
            return n
    raise RuntimeError("too large")


def preserves_fano_sum(perm: Perm, basis: list[Vec2]) -> bool:
    for a, b in itertools.product(basis, repeat=2):
        s = add2(a, b)
        if s == (0, 0):
            continue
        idx = {v: i for i, v in enumerate(basis)}
        left = basis[perm[idx[s]]]
        right = add2(basis[perm[idx[a]]], basis[perm[idx[b]]])
        if left != right:
            return False
    return True


def oriented_pairs_from_cycle(cycle: Perm) -> set[tuple[int, int, int]]:
    # For a 3-cycle on indices 0,1,2, return its cyclic oriented triples.
    out = set()
    for start in range(3):
        a = start
        b = cycle[a]
        c = cycle[b]
        out.add((a, b, c))
    return out


def build_payload() -> dict:
    A4 = a4()
    H = point_stabilizer(0)
    C3_S4 = sorted(set(A4) & set(H))
    C3_restricted = sorted({restrict_to_nonanchor(p) for p in C3_S4})

    fano_nonzero = [(1, 0), (0, 1), (1, 1)]
    GL22 = gl22()
    GL22_image = sorted({action_gl22_on_nonzero(M, fano_nonzero) for M in GL22})
    A3_GL22_image = sorted([p for p in GL22_image if perm_parity(p) == 0])

    c3_orders = Counter(perm_order(p) for p in C3_restricted)
    gl22_orders = Counter(perm_order(p) for p in GL22_image)
    a3_orders = Counter(perm_order(p) for p in A3_GL22_image)
    sum_law = {str((a, b)): add2(a, b) for a, b in itertools.combinations(fano_nonzero, 2)}
    orientation_cycle = next(p for p in C3_restricted if perm_order(p) == 3)
    oriented_triples = oriented_pairs_from_cycle(orientation_cycle)

    identities = {
        "C3_from_S4_overlap_order_3": len(C3_S4) == 3 and len(C3_restricted) == 3,
        "C3_restricted_is_A3_on_three_points": c3_orders == {1: 1, 3: 2} and all(perm_parity(p) == 0 for p in C3_restricted),
        "GL22_order_6_and_is_S3_on_fano_line": len(GL22) == 6 and len(GL22_image) == 6 and gl22_orders == {1: 1, 2: 3, 3: 2},
        "A3_GL22_equals_C3_overlap_after_labeling": set(A3_GL22_image) == set(C3_restricted),
        "all_GL22_preserve_fano_sum": all(preserves_fano_sum(p, fano_nonzero) for p in GL22_image),
        "C3_preserves_fano_sum_and_orientation": all(preserves_fano_sum(p, fano_nonzero) and perm_parity(p) == 0 for p in C3_restricted),
        "fano_sum_triple_law": add2(fano_nonzero[0], fano_nonzero[1]) == fano_nonzero[2] and add2(fano_nonzero[1], fano_nonzero[2]) == fano_nonzero[0] and add2(fano_nonzero[2], fano_nonzero[0]) == fano_nonzero[1],
        "orientation_has_three_cyclic_triples": len(oriented_triples) == 3,
    }
    return {
        "theorem": "c3_fano_triangle_orientation",
        "field_warning": "This is not an identification F3=F2. It is an identification of the three-point oriented incidence object with the three nonzero vectors of F2^2.",
        "projective_qutrit_triangle": {
            "source": "three non-anchor points of PG(1,3) after fixing anchor",
            "C3_overlap_restricted": C3_restricted,
            "order_distribution": dict(c3_orders),
            "meaning": "orientation-preserving cycle of the three non-anchor qutrit choices",
        },
        "fano_line_model": {
            "nonzero_vectors_F2_2": fano_nonzero,
            "sum_law_pairs": sum_law,
            "GL22_image_on_three_points": GL22_image,
            "A3_orientation_subgroup": A3_GL22_image,
            "GL22_order_distribution": dict(gl22_orders),
            "A3_order_distribution": dict(a3_orders),
        },
        "orientation": {
            "chosen_cycle": orientation_cycle,
            "oriented_cyclic_triples": sorted(oriented_triples),
            "interpretation": "Cyclic order gives wedge orientation; odd permutations are dot/dual orientation reversals.",
        },
        "conclusion": "The C3 overlap is the orientation-preserving automorphism group of a Fano-line triple. The qutrit triangle of PG(1,3) can therefore carry the same cyclic wedge/dot orientation as the nonzero F2^2 triple {u,v,u+v}, after choosing an orientation.",
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_c3_fano_triangle_orientation.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
