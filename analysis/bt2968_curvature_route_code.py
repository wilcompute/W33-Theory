#!/usr/bin/env python3
"""Pass 2968: curvature-aware route code for the ten-mode spread router.

For K10, edge-parity faults live in F2^45 and triangle curvature residuals
are H e in F2^120. The verifier proves ker(H) is exactly the 9-dimensional
vertex-switching cut space, hence the finite router carries a [45,9,9] gauge
code. Every non-gauge fault through weight eight is detected and every fault
through weight four is correctable modulo gauge.
"""
from __future__ import annotations

import collections
import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT2968_CURVATURE_ROUTE_CODE_results.json"
VERTICES = tuple(range(10))
EDGES = list(itertools.combinations(VERTICES, 2))
TRIANGLES = list(itertools.combinations(VERTICES, 3))
TETRAHEDRA = list(itertools.combinations(VERTICES, 4))
EDGE_INDEX = {edge: i for i, edge in enumerate(EDGES)}
TRIANGLE_INDEX = {triangle: i for i, triangle in enumerate(TRIANGLES)}


def gf2_rref(matrix):
    a = np.asarray(matrix, dtype=np.uint8).copy() % 2
    rows, cols = a.shape
    pivots = []
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i, c]), None)
        if pivot is None:
            continue
        a[[r, pivot]] = a[[pivot, r]]
        for i in range(rows):
            if i != r and a[i, c]:
                a[i] ^= a[r]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return a, pivots


def gf2_rank(matrix):
    return len(gf2_rref(matrix)[1])


H = np.zeros((len(TRIANGLES), len(EDGES)), dtype=np.uint8)
for ti, triangle in enumerate(TRIANGLES):
    for edge in itertools.combinations(triangle, 2):
        H[ti, EDGE_INDEX[tuple(sorted(edge))]] = 1
B = np.zeros((len(TETRAHEDRA), len(TRIANGLES)), dtype=np.uint8)
for qi, tetrahedron in enumerate(TETRAHEDRA):
    for face in itertools.combinations(tetrahedron, 3):
        B[qi, TRIANGLE_INDEX[tuple(sorted(face))]] = 1


def cut_vector(subset):
    subset = set(subset)
    return np.array([
        int((u in subset) ^ (v in subset)) for u, v in EDGES
    ], dtype=np.uint8)


def vector_key(vector):
    return bytes(np.packbits(np.asarray(vector, dtype=np.uint8)))


def main():
    rank_h = gf2_rank(H)
    assert rank_h == 36
    assert np.count_nonzero((B @ H) % 2) == 0
    singleton_cuts = np.stack([cut_vector([v]) for v in VERTICES])
    assert gf2_rank(singleton_cuts) == 9

    all_cuts = {}
    for mask in range(1 << 10):
        subset = [v for v in VERTICES if (mask >> v) & 1]
        vector = cut_vector(subset)
        all_cuts[vector_key(vector)] = vector
    assert len(all_cuts) == 512
    assert all(np.count_nonzero((H @ vector) % 2) == 0 for vector in all_cuts.values())
    assert 45 - rank_h == 9

    weight_enumerator = collections.Counter(
        int(np.count_nonzero(vector)) for vector in all_cuts.values()
    )
    expected_enumerator = {0: 1, 9: 10, 16: 45, 21: 120, 24: 210, 25: 126}
    assert dict(sorted(weight_enumerator.items())) == expected_enumerator
    minimum_distance = min(weight for weight in weight_enumerator if weight)
    assert minimum_distance == 9

    _, row_pivots = gf2_rref(H.T)
    independent_triangle_indices = row_pivots
    assert len(independent_triangle_indices) == 36
    H36 = H[independent_triangle_indices]
    assert gf2_rank(H36) == 36

    column_weights = [int(np.count_nonzero(H[:, j])) for j in range(45)]
    assert set(column_weights) == {8}
    assert len({vector_key(H[:, j]) for j in range(45)}) == 45
    pair_syndrome_weights = collections.Counter()
    for a, b in itertools.combinations(range(45), 2):
        pair_syndrome_weights[int(np.count_nonzero(H[:, a] ^ H[:, b]))] += 1
    assert pair_syndrome_weights == collections.Counter({14: 360, 16: 630})

    checks = {
        "triangle_edge_matrix_shape_120x45": H.shape == (120, 45),
        "triangle_coboundary_rank_36": rank_h == 36,
        "kernel_dimension_9": 45 - rank_h == 9,
        "kernel_equals_512_vertex_switching_cuts": len(all_cuts) == 512,
        "cut_code_parameters_45_9_9": minimum_distance == 9,
        "tetrahedral_bianchi_BH_zero": np.count_nonzero((B @ H) % 2) == 0,
        "all_single_edge_faults_have_unique_weight8_syndromes":
            set(column_weights) == {8}
            and len({vector_key(H[:, j]) for j in range(45)}) == 45,
        "all_weight_at_most_8_nongauge_faults_detected": minimum_distance == 9,
        "all_weight_at_most_4_faults_correctable_modulo_gauge": minimum_distance >= 9,
        "36_independent_triangle_checks_suffice": gf2_rank(H36) == 36,
    }
    assert all(checks.values())
    result = {
        "schema": "w33.pass2968.curvature_route_code.v1",
        "status": "COMPLETE_EXACT_BINARY_GAUGE_CODE",
        "checks": {key: bool(value) for key, value in checks.items()},
        "check_count": len(checks),
        "raw_registers": {
            "spread_modes": 10,
            "transport_edges": 45,
            "triangle_curvature_checks": 120,
            "independent_syndrome_bits": 36,
            "tetrahedral_bianchi_relations": 210,
        },
        "code": {
            "kernel": "vertex-switching cut space of K10",
            "parameters": "[45,9,9]_2",
            "weight_enumerator": {str(k): v for k, v in sorted(weight_enumerator.items())},
            "minimum_undetectable_weight": 9,
            "correctable_fault_weight_modulo_gauge": 4,
            "detectable_nongauge_fault_weight": 8,
        },
        "syndromes": {
            "single_edge_syndrome_weight": 8,
            "single_edge_syndromes_unique": True,
            "two_edge_syndrome_weight_histogram": {
                str(k): v for k, v in sorted(pair_syndrome_weights.items())
            },
            "independent_triangle_indices": [int(i) for i in independent_triangle_indices],
            "independent_triangles": [list(TRIANGLES[i]) for i in independent_triangle_indices],
        },
        "decoder_statement": (
            "Compare observed triangle parities with the Pass-2967 baseline. "
            "The residual is H e. Decode to a minimum-weight edge-fault coset; "
            "two faults differing by a cut are gauge-equivalent."
        ),
        "headline": (
            "The spread router's parity curvature is an exact [45,9,9]_2 gauge code: "
            "120 triangle checks compress to 36 independent syndrome bits, all faults "
            "through weight four are correctable modulo vertex gauge, and the first "
            "undetectable patterns are precisely weight-nine gauge cuts."
        ),
        "claim_boundary": (
            "This detects parity faults in the finite S4 routing table. It does not "
            "detect even-permutation errors, optical amplitude loss, phase drift inside "
            "a fixed parity class, or detector faults unless separately mapped to flips."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS", len(checks), "/", len(checks), result["headline"])


if __name__ == "__main__":
    main()
