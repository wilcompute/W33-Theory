#!/usr/bin/env python3
"""Passes 7401--7408: global E8 A2 geometry and Eisenstein-W33 leaf incidence.

Builds the 240 E8 roots exactly (scaled by 2), enumerates all 1120 A2 root
subsystems, builds their orthogonality graph, reconstructs the unique A2^4
completion through every orthogonal A2 pair, verifies the resulting 4-class
association scheme, and then combines it with the already-certified regular
order-3 Eisenstein normalizer data to count all W(3,3) leaves inside E8.

No claim here depends on a numerical coincidence alone: the A2/A2^4 geometry is
rebuilt directly from the roots.  The global leaf counts use the exact group
orders already certified in Passes 1020/1029 and the current Passes 7229--7400.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PASS7401_7408_E8_A2_GLOBAL_GEOMETRY_results.json"

WE8 = 696_729_600
CENTRALIZER_REGULAR_C3 = 155_520
NORMALIZER_REGULAR_C3 = 311_040
D4_TOTAL = 3_150
D4_PER_LEAF = 90


def build_e8_roots_scaled2() -> list[tuple[int, ...]]:
    roots: list[tuple[int, ...]] = []
    # Roots ±e_i ±e_j, scaled by 2.
    for i, j in itertools.combinations(range(8), 2):
        for si in (2, -2):
            for sj in (2, -2):
                v = [0] * 8
                v[i], v[j] = si, sj
                roots.append(tuple(v))
    # Half-integral roots, scaled by 2: all ±1 with even number of minus signs.
    for signs in itertools.product((1, -1), repeat=8):
        if sum(s == -1 for s in signs) % 2 == 0:
            roots.append(tuple(signs))
    assert len(roots) == 240
    assert len(set(roots)) == 240
    return roots


def dot(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(a, b))


def add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))


def neg(a: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(-x for x in a)


def enumerate_a2(roots: list[tuple[int, ...]]):
    index = {r: i for i, r in enumerate(roots)}
    a2 = set()
    for i, j in itertools.combinations(range(240), 2):
        # Original roots have norm 2; scaled dot=-4 corresponds to inner product -1.
        if dot(roots[i], roots[j]) != -4:
            continue
        s = add(roots[i], roots[j])
        k = index[s]
        block = frozenset(
            (
                i, j, k,
                index[neg(roots[i])],
                index[neg(roots[j])],
                index[neg(s)],
            )
        )
        assert len(block) == 6
        a2.add(block)
    return sorted(a2, key=lambda s: tuple(sorted(s)))


def choose_basis(block, roots):
    ids = sorted(block)
    for i, j in itertools.combinations(ids, 2):
        if dot(roots[i], roots[j]) == -4:
            return i, j
    raise AssertionError("A2 basis not found")


def build_orthogonality_graph(a2, roots):
    bases = [choose_basis(S, roots) for S in a2]
    n = len(a2)
    A = np.zeros((n, n), dtype=np.uint8)
    for i in range(n):
        ai, bi = bases[i]
        for j in range(i + 1, n):
            aj, bj = bases[j]
            if (
                dot(roots[ai], roots[aj]) == 0
                and dot(roots[ai], roots[bj]) == 0
                and dot(roots[bi], roots[aj]) == 0
                and dot(roots[bi], roots[bj]) == 0
            ):
                A[i, j] = A[j, i] = 1
    return A


def exact_spectrum(A):
    vals = np.linalg.eigvalsh(A.astype(float))
    c = Counter(int(round(x)) for x in vals)
    assert all(abs(x - round(x)) < 1e-7 for x in vals)
    return dict(sorted(c.items(), reverse=True))


def relation_scheme(A):
    n = A.shape[0]
    C = A.astype(np.int16) @ A.astype(np.int16)
    I = np.eye(n, dtype=np.uint8)

    adjacent_cn = sorted(set(int(x) for x in C[A.astype(bool)]))
    nonmask = (A == 0) & (I == 0)
    non_cn = sorted(set(int(x) for x in C[nonmask]))
    assert adjacent_cn == [2]
    assert non_cn == [10, 16, 40]

    rels = [I, A.copy()]
    for value in non_cn:
        rels.append((nonmask & (C == value)).astype(np.uint8))
    valencies = [int(R.sum(axis=1)[0]) for R in rels]
    assert all(np.all(R.sum(axis=1) == valencies[k]) for k, R in enumerate(rels))
    assert valencies == [1, 120, 648, 270, 81]
    assert np.all(sum(rels) == 1)

    # It is enough to verify closure under multiplication by A=R1:
    # the five relation matrices are linearly independent, and the resulting
    # 5x5 multiplication operator has five distinct eigenvalues, hence R1
    # generates the full five-dimensional Bose-Mesner algebra.
    labels = np.zeros((n, n), dtype=np.int8)
    for k, R in enumerate(rels):
        labels[R.astype(bool)] = k

    A_mult = []
    for j, Rj in enumerate(rels):
        prod = A.astype(np.int16) @ Rj.astype(np.int16)
        coeffs = []
        for k in range(5):
            values = np.unique(prod[labels == k])
            assert len(values) == 1
            coeffs.append(int(values[0]))
        A_mult.append(coeffs)

    # Columns are A*R_j coefficients in basis (R0,...,R4).
    M = np.array(A_mult, dtype=int).T
    lev = np.linalg.eigvals(M.astype(float))
    algebra_eigs = sorted((int(round(x.real)) for x in lev), reverse=True)
    assert all(abs(x.imag) < 1e-8 and abs(x.real - round(x.real)) < 1e-8 for x in lev)
    assert algebra_eigs == [120, 20, 8, -4, -40]

    return C, rels, valencies, A_mult


def unique_a2_4_lines(A, C):
    n = A.shape[0]
    lines = set()
    for i in range(n):
        for j in range(i + 1, n):
            if not A[i, j]:
                continue
            common = tuple(int(x) for x in np.where((A[i] == 1) & (A[j] == 1))[0])
            assert len(common) == 2
            u, v = common
            # Edge-regular lambda=2 is stronger here: the two common neighbors are adjacent,
            # giving one K4 and therefore one A2^4 through the edge.
            assert A[u, v] == 1
            lines.add(tuple(sorted((i, j, u, v))))
    assert len(lines) == 11_200

    edge_cover = Counter()
    for L in lines:
        for e in itertools.combinations(L, 2):
            assert A[e[0], e[1]] == 1
            edge_cover[tuple(sorted(e))] += 1
    assert len(edge_cover) == 67_200
    assert set(edge_cover.values()) == {1}
    return sorted(lines)


def main():
    roots = build_e8_roots_scaled2()
    a2 = enumerate_a2(roots)
    assert len(a2) == 1_120

    A = build_orthogonality_graph(a2, roots)
    degrees = A.sum(axis=1)
    assert set(int(x) for x in degrees) == {120}
    edges = int(A.sum() // 2)
    assert edges == 67_200

    C, rels, valencies, A_mult = relation_scheme(A)
    lines = unique_a2_4_lines(A, C)

    spectrum = exact_spectrum(A)
    assert spectrum == {120: 1, 20: 84, 8: 300, -4: 700, -40: 35}

    # Unordered pair-class counts and per-vertex subdegrees.
    pair_counts = {}
    for k, name in enumerate(("identity", "orthogonal", "mu10", "mu16", "mu40")):
        if k == 0:
            pair_counts[name] = 1_120
        else:
            pair_counts[name] = int(rels[k].sum() // 2)

    # Every A2 lies on 40 A2^4 lines.
    line_rep = Counter()
    for L in lines:
        for x in L:
            line_rep[x] += 1
    assert set(line_rep.values()) == {40}

    # Eisenstein W33 leaves = conjugates of the regular cyclic C3 structure.
    regular_order3_elements = WE8 // CENTRALIZER_REGULAR_C3
    leaves = WE8 // NORMALIZER_REGULAR_C3
    assert regular_order3_elements == 4_480
    assert leaves == 2_240
    assert regular_order3_elements == 2 * leaves  # J and J^{-1}

    # Per leaf: W(3,3) has 40 A2 points, 240 orthogonal pairs, 40 A2^4 lines.
    # Current Pass7229-7236 also gives 90 J-stable D4 subsystems.
    incidences = {
        "A2": {
            "global_objects": 1_120,
            "per_leaf": 40,
            "replication": leaves * 40 // 1_120,
        },
        "2A2_orthogonal_pairs": {
            "global_objects": edges,
            "per_leaf": 240,
            "replication": leaves * 240 // edges,
        },
        "4A2_lines": {
            "global_objects": len(lines),
            "per_leaf": 40,
            "replication": leaves * 40 // len(lines),
        },
        "D4": {
            "global_objects": D4_TOTAL,
            "per_leaf": D4_PER_LEAF,
            "replication": leaves * D4_PER_LEAF // D4_TOTAL,
        },
    }
    assert {k: v["replication"] for k, v in incidences.items()} == {
        "A2": 80,
        "2A2_orthogonal_pairs": 8,
        "4A2_lines": 8,
        "D4": 64,
    }

    result = {
        "schema": "w33.pass7401_7408.e8_a2_global_geometry.v1",
        "status": "PASS",
        "passes": "7401-7408",
        "e8": {
            "root_count": 240,
            "A2_subsystems": len(a2),
            "orthogonality_graph": {
                "vertices": len(a2),
                "degree": 120,
                "edges": edges,
                "spectrum": {str(k): v for k, v in spectrum.items()},
                "adjacent_common_neighbors": [2],
                "nonadjacent_common_neighbors": [10, 16, 40],
                "relation_valencies": valencies,
                "pair_class_counts": pair_counts,
                "A_times_relation_coefficients": A_mult,
                "association_scheme_rank": 5,
            },
            "A2_4_lines": {
                "count": len(lines),
                "points_per_line": 4,
                "lines_per_A2": 40,
                "unique_line_through_each_orthogonal_pair": True,
            },
        },
        "eisenstein_W33_leaf_family": {
            "WE8_order": WE8,
            "regular_C3_centralizer_order": CENTRALIZER_REGULAR_C3,
            "regular_C3_normalizer_order": NORMALIZER_REGULAR_C3,
            "regular_order3_elements": regular_order3_elements,
            "cyclic_Eisenstein_structures_or_W33_leaves": leaves,
            "incidence_replications": incidences,
        },
        "boundary": (
            "The 1120-point A2 geometry and its 11200 A2^4 lines are rebuilt directly "
            "from the E8 roots. The count 2240 uses the previously certified regular-C3 "
            "normalizer order 311040. D4 replication uses the current certified count "
            "90 J-stable D4s per leaf. This is a finite root-system theorem, not a "
            "claim that E8 or W33 by themselves constitute a physical theory."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "A2": len(a2),
        "degree": 120,
        "spectrum": result["e8"]["orthogonality_graph"]["spectrum"],
        "A2^4": len(lines),
        "W33_leaves": leaves,
        "replications": {k: v["replication"] for k, v in incidences.items()},
    }, indent=2))
    return result


if __name__ == "__main__":
    main()
