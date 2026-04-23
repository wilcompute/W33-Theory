#!/usr/bin/env python3
"""Exact local-system audit for the Witting packet transport layer.

This packages the operator and A2 side of the Witting packet transport bridge.

Starting from the exact 45-point packet transport graph and the unique packet-
line matching on each transport edge:
1. The matchings define a canonical 135-dimensional connection adjacency on
   the packet-line bundle (45 leaves x 3 packet lines).
2. That bundle splits exactly as 45 + 90, with the 45-dimensional trivial
   sector equal to the transport adjacency and the 90-dimensional standard
   sector carrying the exact spectrum 8, -1, -16.
3. The parity of the same edge matchings defines a signed holonomy operator
   S with exact quadratic identity S^2 = 4S + 32I.
4. Triangle holonomy cycle types are exactly 240 identities, 2880 three-cycles,
   and 2160 transpositions.
5. The difference lattice of the three local packet-line states is the A2 root
   lattice, and the induced 90-dimensional A2 operator satisfies the exact
   cubic relation H^3 + 9H^2 - 120H - 128I = 0.

So the Witting packet layer already carries the full exact 135 = 45 + 90
transport local system and its A2 standard sector, not just the transport
graph beneath them.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys
import time
from typing import Any

import networkx as nx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration", ROOT / "pillars"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from exploration.w33_center_quad_transport_a2_bridge import (  # noqa: E402
    A2_CARTAN,
    A2_DUAL_LEFT_INVERSE,
    A2_ROOT_BASIS,
    build_center_quad_transport_a2_summary,
    rounded_real_spectrum,
)
from exploration.w33_center_quad_transport_complement_bridge import (  # noqa: E402
    build_center_quad_transport_complement_summary,
)
from exploration.w33_center_quad_transport_holonomy_bridge import (  # noqa: E402
    build_center_quad_transport_holonomy_summary,
)
from exploration.w33_center_quad_transport_operator_bridge import (  # noqa: E402
    TOL,
    build_center_quad_transport_operator_summary,
    local_trivial_and_standard_bases,
    rounded_integer_spectrum,
)
from scripts.w33_witting_packet_quotient_geometry_audit import (  # noqa: E402
    _build_leaf_list,
    _leaf_graph,
    _line_graph,
    _packet_lines,
)
from scripts.w33_witting_packet_transport_complement_audit import _leaf_packet_lines  # noqa: E402


def _permutation_inverse(permutation: tuple[int, int, int]) -> tuple[int, int, int]:
    out = [0, 0, 0]
    for index, image in enumerate(permutation):
        out[image] = index
    return tuple(out)


def _permutation_compose(
    left: tuple[int, int, int], right: tuple[int, int, int]
) -> tuple[int, int, int]:
    return tuple(right[left[index]] for index in range(3))


def _permutation_parity(permutation: tuple[int, int, int]) -> int:
    inversions = 0
    for i in range(3):
        for j in range(i + 1, 3):
            inversions += permutation[i] > permutation[j]
    return inversions % 2


def _cycle_type(permutation: tuple[int, int, int]) -> str:
    if permutation == (0, 1, 2):
        return "identity"
    if _permutation_parity(permutation) == 0:
        return "three_cycle"
    return "transposition"


def _permutation_matrix(permutation: tuple[int, int, int]) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=float)
    for source, target in enumerate(permutation):
        matrix[source, target] = 1.0
    return matrix


@lru_cache(maxsize=1)
def _packet_transport_seed() -> tuple[nx.Graph, list[tuple[int, ...]], nx.Graph, list[tuple[int, int, int]]]:
    leaves = _build_leaf_list()
    point_graph = _leaf_graph(leaves)
    transport_graph = nx.complement(point_graph)
    packet_lines = _packet_lines(leaves)
    packet_line_graph = _line_graph(packet_lines)
    leaf_packet_lines = _leaf_packet_lines(packet_lines, len(leaves))
    return transport_graph, packet_lines, packet_line_graph, leaf_packet_lines


def edge_packetline_matching(left: int, right: int) -> tuple[int, int, int]:
    transport_graph, _packet_lines_data, packet_line_graph, leaf_packet_lines = _packet_transport_seed()
    if not transport_graph.has_edge(left, right):
        raise AssertionError("packetline matching is only defined on transport edges")
    source = leaf_packet_lines[left]
    target = leaf_packet_lines[right]
    permutation = []
    for packet_line in source:
        matches = [index for index, other in enumerate(target) if packet_line_graph.has_edge(packet_line, other)]
        if len(matches) != 1:
            raise AssertionError("transport edge should induce a unique packet-line matching")
        permutation.append(matches[0])
    result = tuple(permutation)
    if sorted(result) != [0, 1, 2]:
        raise AssertionError("packet-line matching must be a permutation")
    return result


def _directed_packetline_matching(left: int, right: int) -> tuple[int, int, int]:
    if left < right:
        return edge_packetline_matching(left, right)
    return _permutation_inverse(edge_packetline_matching(right, left))


def _packet_connection_adjacency() -> np.ndarray:
    transport_graph, _packet_lines_data, _packet_line_graph, _leaf_packet_lines_data = _packet_transport_seed()
    node_count = transport_graph.number_of_nodes()
    matrix = np.zeros((3 * node_count, 3 * node_count), dtype=float)
    for left, right in sorted(transport_graph.edges()):
        block = _permutation_matrix(edge_packetline_matching(left, right))
        matrix[3 * left : 3 * left + 3, 3 * right : 3 * right + 3] = block
        matrix[3 * right : 3 * right + 3, 3 * left : 3 * left + 3] = block.T
    return matrix


def _packet_signed_holonomy_operator() -> np.ndarray:
    transport_graph, _packet_lines_data, _packet_line_graph, _leaf_packet_lines_data = _packet_transport_seed()
    node_count = transport_graph.number_of_nodes()
    matrix = np.zeros((node_count, node_count), dtype=int)
    for left, right in sorted(transport_graph.edges()):
        sign = -1 if _permutation_parity(edge_packetline_matching(left, right)) else 1
        matrix[left, right] = sign
        matrix[right, left] = sign
    return matrix


def _a2_weyl_matrix(permutation: tuple[int, int, int]) -> np.ndarray:
    matrix = A2_DUAL_LEFT_INVERSE @ _permutation_matrix(permutation) @ A2_ROOT_BASIS
    result = np.rint(matrix).astype(int)
    if np.max(np.abs(matrix - result)) > TOL:
        raise AssertionError("expected integral A2 Weyl matrix")
    return result


def _packet_a2_operator() -> np.ndarray:
    transport_graph, _packet_lines_data, _packet_line_graph, _leaf_packet_lines_data = _packet_transport_seed()
    node_count = transport_graph.number_of_nodes()
    operator = np.zeros((2 * node_count, 2 * node_count), dtype=int)
    for left, right in sorted(transport_graph.edges()):
        forward = _a2_weyl_matrix(edge_packetline_matching(left, right))
        reverse = _a2_weyl_matrix(edge_packetline_matching(right, left))
        operator[2 * left : 2 * left + 2, 2 * right : 2 * right + 2] = forward
        operator[2 * right : 2 * right + 2, 2 * left : 2 * left + 2] = reverse
    return operator


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    transport_graph, packet_lines, _packet_line_graph, _leaf_packet_lines_data = _packet_transport_seed()
    node_count = transport_graph.number_of_nodes()

    connection = _packet_connection_adjacency()
    signed = _packet_signed_holonomy_operator()
    a2_operator = _packet_a2_operator()

    trivial_basis, standard_basis = local_trivial_and_standard_bases(node_count)
    transport_adjacency = nx.to_numpy_array(transport_graph, nodelist=sorted(transport_graph.nodes()), dtype=float)
    trivial_block = trivial_basis.T @ connection @ trivial_basis
    standard_block = standard_basis.T @ connection @ standard_basis
    cross_block = trivial_basis.T @ connection @ standard_basis

    holonomy_counts = Counter()
    triangle_count = 0
    for a, b, c in combinations(sorted(transport_graph.nodes()), 3):
        if not (transport_graph.has_edge(a, b) and transport_graph.has_edge(a, c) and transport_graph.has_edge(b, c)):
            continue
        triangle_count += 1
        holonomy = _permutation_compose(
            _directed_packetline_matching(a, b),
            _permutation_compose(
                _directed_packetline_matching(b, c),
                _directed_packetline_matching(c, a),
            ),
        )
        holonomy_counts[_cycle_type(holonomy)] += 1

    packet_permutation_counts = Counter(
        edge_packetline_matching(left, right) for left, right in sorted(transport_graph.edges())
    )

    packet_parity_distribution = Counter(
        _permutation_parity(permutation)
        for permutation, count in packet_permutation_counts.items()
        for _ in range(count)
    )

    signed_relation = signed @ signed - 4 * signed - 32 * np.eye(node_count, dtype=int)
    a2_cubic = (
        a2_operator @ a2_operator @ a2_operator
        + 9 * (a2_operator @ a2_operator)
        - 120 * a2_operator
        - 128 * np.eye(a2_operator.shape[0], dtype=int)
    )

    center_operator = build_center_quad_transport_operator_summary()
    center_holonomy = build_center_quad_transport_holonomy_summary()
    center_a2 = build_center_quad_transport_a2_summary()
    center_matching = build_center_quad_transport_complement_summary()["local_s3_matching"]
    packet_weyl_matrices = {
        tuple(map(tuple, _a2_weyl_matrix(edge_packetline_matching(left, right))))
        for left, right in sorted(transport_graph.edges())
    }

    theorem = {
        "the_packet_transport_matchings_define_an_exact_135dimensional_connection_bundle": (
            connection.shape == (135, 135)
            and rounded_integer_spectrum(connection) == {-16: 6, -4: 20, -1: 64, 2: 24, 8: 20, 32: 1}
        ),
        "the_packet_connection_bundle_splits_exactly_as_45_plus_90": (
            trivial_block.shape == (45, 45)
            and standard_block.shape == (90, 90)
            and float(np.max(np.abs(cross_block))) < TOL
            and float(np.max(np.abs(trivial_block - transport_adjacency))) < TOL
            and rounded_integer_spectrum(trivial_block) == {-4: 20, 2: 24, 32: 1}
            and rounded_integer_spectrum(standard_block) == {-16: 6, -1: 64, 8: 20}
        ),
        "the_packet_signed_holonomy_operator_satisfies_s2_equals_4s_plus_32i": (
            np.array_equal(signed_relation, np.zeros_like(signed_relation))
            and rounded_integer_spectrum(signed.astype(float)) == {-4: 30, 8: 15}
        ),
        "the_packet_triangle_holonomy_cycle_types_are_exactly_240_2880_2160": (
            triangle_count == 5280
            and dict(sorted(holonomy_counts.items())) == {
                "identity": 240,
                "three_cycle": 2880,
                "transposition": 2160,
            }
        ),
        "the_packet_a2_operator_has_exact_spectrum_and_cubic_relation": (
            a2_operator.shape == (90, 90)
            and rounded_real_spectrum(a2_operator.astype(float)) == {-16: 6, -1: 64, 8: 20}
            and np.array_equal(a2_cubic, np.zeros_like(a2_cubic))
        ),
    }
    theorem["the_packet_local_system_recovers_the_same_transport_operator_holonomy_and_a2_invariants_as_the_centerquad_route"] = (
        center_operator["connection_bundle"]["adjacency_spectrum"] == rounded_integer_spectrum(connection)
        and center_operator["trivial_standard_split"]["standard_block_spectrum"]
        == rounded_integer_spectrum(standard_block)
        and center_operator["signed_holonomy_operator"]["spectrum"] == rounded_integer_spectrum(signed.astype(float))
        and center_holonomy["triangle_holonomy"]["cycle_type_counts"] == dict(sorted(holonomy_counts.items()))
        and center_a2["a2_transport_operator"]["spectrum"] == rounded_real_spectrum(a2_operator.astype(float))
    )
    theorem["the_witting_packet_layer_carries_the_full_exact_transport_local_system"] = all(theorem.values())

    return {
        "status": "ok",
        "packet_connection_bundle": {
            "base_vertices": node_count,
            "fiber_dimension": 3,
            "total_dimension": int(connection.shape[0]),
            "adjacency_spectrum": rounded_integer_spectrum(connection),
            "laplacian_spectrum": rounded_integer_spectrum(32.0 * np.eye(connection.shape[0]) - connection),
            "trace_a_squared": int(round(float(np.trace(connection @ connection)))),
            "trace_a_cubed": int(round(float(np.trace(connection @ connection @ connection)))),
        },
        "packet_trivial_standard_split": {
            "trivial_dimension": int(trivial_block.shape[0]),
            "standard_dimension": int(standard_block.shape[0]),
            "trivial_standard_coupling_max_abs": float(np.max(np.abs(cross_block))),
            "trivial_block_equals_transport_adjacency": float(np.max(np.abs(trivial_block - transport_adjacency))) < TOL,
            "trivial_block_spectrum": rounded_integer_spectrum(trivial_block),
            "standard_block_spectrum": rounded_integer_spectrum(standard_block),
            "standard_block_laplacian_spectrum": rounded_integer_spectrum(
                32.0 * np.eye(standard_block.shape[0]) - standard_block
            ),
        },
        "packet_signed_holonomy_operator": {
            "dimension": int(signed.shape[0]),
            "spectrum": rounded_integer_spectrum(signed.astype(float)),
            "quadratic_identity_s_squared_equals_4s_plus_32i": bool(
                np.array_equal(signed_relation, np.zeros_like(signed_relation))
            ),
            "trace_s_squared": int(np.trace(signed @ signed)),
            "trace_s_cubed": int(np.trace(signed @ signed @ signed)),
        },
        "packet_triangle_holonomy": {
            "transport_triangles": triangle_count,
            "cycle_type_counts": dict(sorted(holonomy_counts.items())),
        },
        "packet_a2_local_system": {
            "rank": 2,
            "cartan_matrix": A2_CARTAN.tolist(),
            "spectrum": rounded_real_spectrum(a2_operator.astype(float)),
            "laplacian_spectrum": rounded_real_spectrum(
                32.0 * np.eye(a2_operator.shape[0]) - a2_operator.astype(float)
            ),
            "trace_h_squared": int(np.trace(a2_operator @ a2_operator)),
            "trace_h_cubed": int(np.trace(a2_operator @ a2_operator @ a2_operator)),
            "cubic_relation_h3_plus_9h2_minus_120h_minus_128i": bool(
                np.array_equal(a2_cubic, np.zeros_like(a2_cubic))
            ),
            "all_six_weyl_matrices_realized": len(packet_weyl_matrices) == 6,
            "all_edge_weyl_matrices_preserve_cartan": all(
                np.array_equal(np.array(matrix).T @ A2_CARTAN @ np.array(matrix), A2_CARTAN)
                for matrix in packet_weyl_matrices
            ),
        },
        "label_gauge_dictionary": {
            "packet_sorted_label_permutation_counts": {
                "".join(map(str, permutation)): count
                for permutation, count in sorted(packet_permutation_counts.items())
            },
            "packet_sorted_label_parity_distribution": dict(sorted(packet_parity_distribution.items())),
            "centerquad_sorted_label_permutation_counts": center_matching["permutation_counts_under_sorted_labels"],
            "centerquad_sorted_label_parity_distribution": {
                str(parity): count for parity, count in sorted({
                    0: sum(
                        count
                        for label, count in center_matching["permutation_counts_under_sorted_labels"].items()
                        if _permutation_parity(tuple(int(ch) for ch in label)) == 0
                    ),
                    1: sum(
                        count
                        for label, count in center_matching["permutation_counts_under_sorted_labels"].items()
                        if _permutation_parity(tuple(int(ch) for ch in label)) == 1
                    ),
                }.items())
            },
            "sorted_label_permutation_counts_match_centerquad": (
                {
                    "".join(map(str, permutation)): count
                    for permutation, count in sorted(packet_permutation_counts.items())
                }
                == center_matching["permutation_counts_under_sorted_labels"]
            ),
        },
        "invariant_crosswalk": {
            "connection_bundle_spectrum_matches_centerquad": (
                center_operator["connection_bundle"]["adjacency_spectrum"] == rounded_integer_spectrum(connection)
            ),
            "standard_sector_spectrum_matches_centerquad": (
                center_operator["trivial_standard_split"]["standard_block_spectrum"]
                == rounded_integer_spectrum(standard_block)
            ),
            "signed_operator_spectrum_matches_centerquad": (
                center_operator["signed_holonomy_operator"]["spectrum"] == rounded_integer_spectrum(signed.astype(float))
            ),
            "triangle_holonomy_counts_match_centerquad": (
                center_holonomy["triangle_holonomy"]["cycle_type_counts"] == dict(sorted(holonomy_counts.items()))
            ),
            "a2_operator_spectrum_matches_centerquad": (
                center_a2["a2_transport_operator"]["spectrum"] == rounded_real_spectrum(a2_operator.astype(float))
            ),
        },
        "packet_transport_local_system_theorem": theorem,
        "bridge_verdict": (
            "The Witting packet layer now carries the full exact transport local system. The 45 packet leaves "
            "and their unique edge packet-line matchings define the same 135-dimensional connection bundle, "
            "the same exact 45 + 90 split, the same signed holonomy operator, the same 240 / 2880 / 2160 "
            "triangle holonomy law, and the same A2 standard sector as the older center-quad route. What "
            "does depend on local labels is the raw six-permutation edge count under a chosen sorted packet "
            "labeling; the exact content lives at the operator, holonomy, and A2-invariant level."
        ),
    }


def main() -> int:
    timer = time.perf_counter()
    payload = analyze()
    output_dir = ROOT / "checks"
    output_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXXV_witting_packet_transport_local_system_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 Witting packet transport local-system audit")
    for key, value in payload["packet_transport_local_system_theorem"].items():
        print(f"  [{'PASS' if value else 'FAIL'}] {key}")
    print(f"  Wrote: {output_path}")
    print(f"  Runtime: {time.perf_counter() - timer:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
