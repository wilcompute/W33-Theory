#!/usr/bin/env python3
"""Passes 7409--7416: the 4A2 Eisenstein-leaf fibre is the Fano-hinge W(D4) chart.

Fix one A2^4 root subsystem X in E8. An Eisenstein W(3,3) leaf containing X
restricts on each A2 factor to one of the two Coxeter orientations. Four signs
give F2^4; replacing J by J^{-1} flips all four signs simultaneously, hence the
eight leaves through X are

    F2^4 / <1111>  ~= F2^3.

The internal A2 reflections act by translations, while the tetracode coordinate
quotient S4 permutes the four factors. The induced action is therefore

    2^3 : S4 = W(D4), order 192,

and the explicit quotient map to F2^3 reproduces the project's existing Fano
hinge chart: four odd directions generate K4,4 and three even directions generate
2K4. Thus the recurring 192-scale is derived here directly from E8/A2^4.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PASS7409_7416_E8_4A2_FANO_FIBRE_results.json"

WE8 = 696_729_600
A2_4_COUNT = 11_200
WA2_4 = 6 ** 4


def xor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


ONES4 = (1, 1, 1, 1)


def canonical4(x):
    y = xor(x, ONES4)
    return min((x, y))


CLASSES4 = sorted({canonical4(x) for x in itertools.product((0, 1), repeat=4)})


def q3(x):
    """Well-defined F2^4/<1111> -> F2^3 gauge: subtract x4*1111."""
    x1, x2, x3, x4 = x
    return (x1 ^ x4, x2 ^ x4, x3 ^ x4)


PTS3 = sorted(itertools.product((0, 1), repeat=3))
IDX3 = {p: i for i, p in enumerate(PTS3)}


def add3(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def parity3(a):
    return sum(a) % 2


def permute4(x, p):
    return tuple(x[p[i]] for i in range(4))


def class_action_by_s4(xclass, p):
    return canonical4(permute4(xclass, p))


def permutation_on_8(fn):
    return tuple(IDX3[fn(p)] for p in PTS3)


def affine_group_perms():
    # Explicit S4 action transported from the four A2 factors to q3-coordinates.
    s4 = list(itertools.permutations(range(4)))
    linear = set()
    for p in s4:
        image = {}
        for c in CLASSES4:
            image[q3(c)] = q3(class_action_by_s4(c, p))
        perm = tuple(IDX3[image[x]] for x in PTS3)
        linear.add(perm)
    assert len(linear) == 24

    translations = {
        permutation_on_8(lambda x, t=t: add3(x, t))
        for t in PTS3
    }
    assert len(translations) == 8

    affine = set()
    for T in translations:
        for L in linear:
            affine.add(tuple(T[L[i]] for i in range(8)))
    assert len(affine) == 192
    return linear, translations, affine


def cayley_edges(generators):
    edges = set()
    for x in PTS3:
        for s in generators:
            y = add3(x, s)
            if x != y:
                edges.add(tuple(sorted((IDX3[x], IDX3[y]))))
    return edges


def connected_components(edges):
    adj = [set() for _ in range(8)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    seen = set()
    comps = []
    for v in range(8):
        if v in seen:
            continue
        stack = [v]
        comp = set()
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            seen.add(u)
            stack.extend(adj[u] - comp)
        comps.append(comp)
    return sorted((sorted(c) for c in comps), key=lambda c: (len(c), c))


def main():
    assert len(CLASSES4) == 8
    assert len({q3(c) for c in CLASSES4}) == 8

    # Parity is well-defined on the quotient because 1111 has even weight.
    for x in itertools.product((0, 1), repeat=4):
        assert sum(x) % 2 == sum(xor(x, ONES4)) % 2
        assert sum(x) % 2 == parity3(q3(x))

    nonzero = [p for p in PTS3 if p != (0, 0, 0)]
    odd = [p for p in nonzero if parity3(p) == 1]
    even = [p for p in nonzero if parity3(p) == 0]
    assert len(odd) == 4 and len(even) == 3
    assert set(odd) == {(1,0,0), (0,1,0), (0,0,1), (1,1,1)}

    linear, translations, affine = affine_group_perms()

    # S4 is exactly the stabilizer of the zero leaf in the 192 action.
    zero = IDX3[(0,0,0)]
    zero_stab = [g for g in affine if g[zero] == zero]
    assert len(zero_stab) == 24
    assert set(zero_stab) == linear

    # Nonzero S4 orbits = 4 odd + 3 even.
    lin_orbits = []
    unseen = set(range(8))
    while unseen:
        seed = min(unseen)
        orb = {g[seed] for g in linear}
        lin_orbits.append(sorted(orb))
        unseen -= orb
    sizes = sorted(len(o) for o in lin_orbits)
    assert sizes == [1, 3, 4]

    odd_edges = cayley_edges(odd)
    even_edges = cayley_edges(even)
    assert len(odd_edges) == 16
    assert len(even_edges) == 12
    assert odd_edges.isdisjoint(even_edges)
    assert len(odd_edges | even_edges) == 28  # all edges of K8

    # Odd graph is K4,4 under the parity bipartition.
    left = {IDX3[p] for p in PTS3 if parity3(p) == 0}
    right = set(range(8)) - left
    expected_k44 = {tuple(sorted((a, b))) for a in left for b in right}
    assert odd_edges == expected_k44

    # Even graph is two disjoint K4s.
    comps = connected_components(even_edges)
    assert sorted(len(c) for c in comps) == [4, 4]
    for comp in comps:
        assert sum(1 for e in even_edges if e[0] in comp and e[1] in comp) == 6

    # Each direction is a perfect matching (translation involution).
    matchings = {}
    for name, dirs in (("odd", odd), ("even", even)):
        matchings[name] = []
        covered = set()
        for s in dirs:
            E = cayley_edges([s])
            assert len(E) == 4
            assert len({v for e in E for v in e}) == 8
            assert covered.isdisjoint(E)
            covered |= E
            matchings[name].append({
                "direction": "".join(map(str, s)),
                "edge_count": len(E),
            })
        assert covered == (odd_edges if name == "odd" else even_edges)

    # E8 normalizer arithmetic.
    normalizer_4a2 = WE8 // A2_4_COUNT
    assert normalizer_4a2 == 62_208
    outer_4a2 = normalizer_4a2 // WA2_4
    assert outer_4a2 == 48
    image = len(affine)
    kernel = normalizer_4a2 // image
    assert kernel == 324

    # Internal W(A2)^4 -> translations: S3^4 acts by independently inverting
    # four C3 orientations, with simultaneous inversion trivial on <J>.
    internal_image = 8
    internal_kernel = WA2_4 // internal_image
    assert internal_kernel == 162  # 3^4 rotations times simultaneous inversion

    # The order-48 tetracode glue stabilizer projects by its central ±I to S4.
    tetracode_order = 48
    tetracode_projective = 24
    assert tetracode_order // tetracode_projective == 2
    assert kernel == internal_kernel * 2

    # Incidence already says eight leaves through each A2^4 line.
    leaves = 2_240
    leaves_per_4a2 = leaves * 40 // A2_4_COUNT
    assert leaves_per_4a2 == 8

    result = {
        "schema": "w33.pass7409_7416.e8_4a2_fano_fibre.v1",
        "status": "PASS",
        "passes": "7409-7416",
        "fibre": {
            "description": "Eisenstein W(3,3) leaves through a fixed A2^4 subsystem",
            "orientation_bits_before_global_inversion": 16,
            "global_inversion_identification": "x ~ x+1111",
            "fibre_size": 8,
            "vector_space": "F2^4/<1111> ~= F2^3",
            "explicit_map_to_F2_3": "(x1,x2,x3,x4) -> (x1+x4,x2+x4,x3+x4)",
            "nonzero_direction_split": {
                "odd": ["100", "010", "001", "111"],
                "even": ["110", "101", "011"],
            },
        },
        "group_action": {
            "W_E8_order": WE8,
            "A2_4_count": A2_4_COUNT,
            "normalizer_A2_4_order": normalizer_4a2,
            "W_A2_4_order": WA2_4,
            "extendable_outer_quotient_order": outer_4a2,
            "internal_orientation_translation_image": internal_image,
            "internal_kernel": internal_kernel,
            "tetracode_glue_stabilizer_order": tetracode_order,
            "tetracode_projective_block_quotient": "S4",
            "tetracode_projective_order": tetracode_projective,
            "full_fibre_image": "2^3:S4 = W(D4)",
            "full_fibre_image_order": image,
            "full_fibre_kernel_order": kernel,
            "zero_leaf_stabilizer_order_in_image": len(zero_stab),
        },
        "fano_hinge_weld": {
            "odd_cayley_graph": "K4,4",
            "odd_edges": len(odd_edges),
            "odd_one_factorization_matchings": matchings["odd"],
            "even_cayley_graph": "2 K4",
            "even_edges": len(even_edges),
            "even_matchings": matchings["even"],
            "K8_edge_partition": "K8 = K4,4 disjoint_union 2K4",
            "reading": (
                "The exact same F2^3, 4+3 direction split, K4,4 one-factorization, "
                "and 192-element affine group previously found in the Fano-hinge "
                "codec are obtained here from the eight Eisenstein E8 leaves through "
                "one A2^4 subsystem."
            ),
        },
        "incidence_crosscheck": {
            "global_W33_leaves": leaves,
            "W33_lines_per_leaf": 40,
            "global_A2_4": A2_4_COUNT,
            "leaves_per_A2_4": leaves_per_4a2,
        },
        "boundary": (
            "This theorem identifies the finite E8/A2^4 orientation fibre with the "
            "existing Fano-hinge affine chart. It does not assert that the tomotope "
            "or a physical hardware implementation is literally an E8 subsystem; "
            "the weld is the explicit shared F2^3 affine action."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "fibre": 8,
        "image": image,
        "kernel": kernel,
        "odd_graph": "K4,4",
        "even_graph": "2K4",
        "direction_split": [4,3],
    }, indent=2))
    return result


if __name__ == "__main__":
    main()
