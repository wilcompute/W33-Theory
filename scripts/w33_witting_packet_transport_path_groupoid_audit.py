#!/usr/bin/env python3
"""Exact path-groupoid audit for Witting packet transport.

This lifts the packet-side A2 local system from edge data to the correct
categorical object:

1. a representation of the path groupoid of the 45-point packet transport
   graph into Weyl(A2);
2. a spanning-tree gauge whose nontrivial content sits on the fundamental
   cycles;
3. the coefficient jump from characteristic 0 to F3.

The exact result is that the packet route reaches the same mod-3 transport
shadow as the older center-quad route: no nonzero real flat section, but a
unique invariant projective line [1,2] over F3.
"""

from __future__ import annotations

from collections import deque
from functools import lru_cache
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

from exploration.w33_transport_path_groupoid_bridge import (  # noqa: E402
    MODULUS,
    _adapted_basis,
    _f3_invariant_line,
    _group_closure_matrices,
    _matrix_inverse,
    _rank_mod_p,
    build_transport_path_groupoid_summary,
)
from scripts.w33_witting_packet_transport_local_system_audit import (  # noqa: E402
    _a2_weyl_matrix,
    _packet_transport_seed,
    _permutation_inverse,
    edge_packetline_matching,
)


IDENTITY_2 = np.eye(2, dtype=int)


def directed_a2_edge_matrix(left: int, right: int) -> np.ndarray:
    if left < right:
        permutation = edge_packetline_matching(left, right)
    else:
        permutation = _permutation_inverse(edge_packetline_matching(right, left))
    return _a2_weyl_matrix(permutation)


def path_transport(path: tuple[int, ...]) -> np.ndarray:
    if len(path) < 2:
        return IDENTITY_2.copy()
    transport = IDENTITY_2.copy()
    for left, right in zip(path, path[1:]):
        transport = directed_a2_edge_matrix(left, right) @ transport
    return transport


def _spanning_tree_parent_map(root: int = 0) -> dict[int, int | None]:
    graph = _packet_transport_seed()[0]
    parent: dict[int, int | None] = {root: None}
    queue = deque([root])
    while queue:
        left = queue.popleft()
        for right in sorted(graph.neighbors(left)):
            if right in parent:
                continue
            parent[right] = left
            queue.append(right)
    if len(parent) != graph.number_of_nodes():
        raise AssertionError("packet transport graph should be connected")
    return parent


def _tree_path(root: int, target: int, parent: dict[int, int | None]) -> tuple[int, ...]:
    path = [target]
    current = target
    while current != root:
        parent_vertex = parent[current]
        if parent_vertex is None:
            raise AssertionError("broken parent map")
        path.append(parent_vertex)
        current = parent_vertex
    path.reverse()
    return tuple(path)


@lru_cache(maxsize=1)
def spanning_tree_gauge(root: int = 0) -> dict[int, np.ndarray]:
    parent = _spanning_tree_parent_map(root)
    gauge: dict[int, np.ndarray] = {}
    for vertex in parent:
        gauge[vertex] = path_transport(_tree_path(root, vertex, parent))
    return gauge


def gauge_fixed_edge_matrix(left: int, right: int, root: int = 0) -> np.ndarray:
    gauge = spanning_tree_gauge(root)
    return _matrix_inverse(gauge[right]) @ directed_a2_edge_matrix(left, right) @ gauge[left]


def _tree_edges(parent: dict[int, int | None]) -> set[tuple[int, int]]:
    return {
        (min(vertex, parent_vertex), max(vertex, parent_vertex))
        for vertex, parent_vertex in parent.items()
        if parent_vertex is not None
    }


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    graph = _packet_transport_seed()[0]
    root = 0
    parent = _spanning_tree_parent_map(root)
    tree_edges = _tree_edges(parent)

    gauge_fixed_non_tree = []
    tree_identity_ok = True
    for left, right in sorted(graph.edges()):
        forward = gauge_fixed_edge_matrix(left, right, root)
        backward = gauge_fixed_edge_matrix(right, left, root)
        if (left, right) in tree_edges:
            tree_identity_ok &= np.array_equal(forward, IDENTITY_2)
            tree_identity_ok &= np.array_equal(backward, IDENTITY_2)
        else:
            gauge_fixed_non_tree.extend([forward, backward])

    holonomy_group = _group_closure_matrices(gauge_fixed_non_tree)
    real_constraint = np.vstack([matrix - IDENTITY_2 for matrix in holonomy_group])
    real_fixed_dimension = 2 - int(np.linalg.matrix_rank(real_constraint.astype(float)))

    reduced_group = [matrix % MODULUS for matrix in holonomy_group]
    f3_constraint = np.vstack([matrix - IDENTITY_2 for matrix in reduced_group]) % MODULUS
    f3_fixed_dimension = 2 - _rank_mod_p(f3_constraint)
    invariant_line = _f3_invariant_line(reduced_group)
    basis, basis_inverse = _adapted_basis(invariant_line)
    adapted = [(basis_inverse @ matrix @ basis) % MODULUS for matrix in reduced_group]
    quotient_character_values = sorted({int(matrix[1, 1]) for matrix in adapted})

    first_neighbor = min(graph.neighbors(root))
    sample_path = (root, first_neighbor, root)
    sample_inverse = tuple(reversed(sample_path))

    center_summary = build_transport_path_groupoid_summary()

    theorem = {
        "the_packet_transport_a2_data_defines_an_exact_path_groupoid_representation": (
            graph.number_of_nodes() == 45
            and graph.number_of_edges() == 720
            and np.array_equal(path_transport(sample_inverse), _matrix_inverse(path_transport(sample_path)))
        ),
        "the_packet_spanning_tree_gauge_trivializes_all_tree_edges_and_realizes_full_weyl_a2_on_fundamental_cycles": (
            len(tree_edges) == 44
            and graph.number_of_edges() - len(tree_edges) == 676
            and tree_identity_ok is True
            and len(holonomy_group) == 6
        ),
        "the_packet_path_groupoid_has_no_nonzero_real_flat_section": (
            real_fixed_dimension == 0
        ),
        "the_packet_path_groupoid_has_a_unique_invariant_projective_line_12_over_f3": (
            f3_fixed_dimension == 1 and invariant_line == (1, 2)
        ),
        "the_packet_mod3_quotient_character_is_the_exact_binary_shadow": (
            all(int(matrix[1, 0]) == 0 for matrix in adapted)
            and quotient_character_values == [1, 2]
        ),
        "the_packet_path_groupoid_recovers_the_same_mod3_transport_shadow_as_the_centerquad_route": (
            center_summary["real_local_system"]["common_fixed_subspace_dimension"] == real_fixed_dimension
            and center_summary["ternary_reduction"]["common_fixed_subspace_dimension"] == f3_fixed_dimension
            and center_summary["ternary_reduction"]["unique_invariant_projective_line"] == list(invariant_line)
            and center_summary["ternary_reduction"]["quotient_character_values"] == quotient_character_values
        ),
    }
    theorem["the_witting_packet_layer_carries_the_exact_transport_path_groupoid_shadow"] = all(theorem.values())

    return {
        "status": "ok",
        "path_groupoid": {
            "objects": graph.number_of_nodes(),
            "undirected_generating_edges": graph.number_of_edges(),
            "directed_generating_morphisms": 2 * graph.number_of_edges(),
            "sample_closed_path": list(sample_path),
            "sample_path_transport": [list(row) for row in path_transport(sample_path)],
            "sample_inverse_transport": [list(row) for row in path_transport(sample_inverse)],
            "path_transport_respects_inversion": np.array_equal(
                path_transport(sample_inverse), _matrix_inverse(path_transport(sample_path))
            ),
        },
        "spanning_tree_gauge": {
            "root_vertex": root,
            "tree_edges": len(tree_edges),
            "fundamental_cycles": graph.number_of_edges() - len(tree_edges),
            "all_tree_edges_gauge_trivialized": tree_identity_ok,
            "fundamental_cycle_holonomy_group_order": len(holonomy_group),
            "fundamental_cycle_holonomies_realize_full_weyl_a2": len(holonomy_group) == 6,
        },
        "real_local_system": {
            "common_fixed_subspace_dimension": real_fixed_dimension,
            "has_nonzero_flat_section": real_fixed_dimension > 0,
        },
        "ternary_reduction": {
            "modulus": MODULUS,
            "common_fixed_subspace_dimension": f3_fixed_dimension,
            "unique_invariant_projective_line": list(invariant_line),
            "adapted_basis": [list(row) for row in basis],
            "adapted_group_is_upper_triangular": all(int(matrix[1, 0]) == 0 for matrix in adapted),
            "quotient_character_values": quotient_character_values,
            "quotient_character_is_exact_binary_shadow": quotient_character_values == [1, 2],
        },
        "invariant_crosswalk": {
            "real_flat_section_dimension_matches_centerquad": (
                center_summary["real_local_system"]["common_fixed_subspace_dimension"] == real_fixed_dimension
            ),
            "ternary_flat_section_dimension_matches_centerquad": (
                center_summary["ternary_reduction"]["common_fixed_subspace_dimension"] == f3_fixed_dimension
            ),
            "invariant_line_matches_centerquad": (
                center_summary["ternary_reduction"]["unique_invariant_projective_line"] == list(invariant_line)
            ),
            "binary_shadow_matches_centerquad": (
                center_summary["ternary_reduction"]["quotient_character_values"] == quotient_character_values
            ),
        },
        "packet_transport_path_groupoid_theorem": theorem,
        "bridge_verdict": (
            "The packet-side transport A2 data already carries the full path-groupoid shadow. A spanning-tree "
            "gauge trivializes every tree edge, the fundamental cycles realize the full Weyl(A2) holonomy "
            "group, over characteristic 0 there is no nonzero flat section, and over F3 there is a unique "
            "invariant projective line [1,2] with exact binary shadow {1,2}. So the mod-3 transport shadow is "
            "not exclusive to the older center-quad route; it is already present on the Witting packet side."
        ),
    }


def main() -> int:
    timer = time.perf_counter()
    payload = analyze()
    output_dir = ROOT / "checks"
    output_dir.mkdir(exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXXVI_witting_packet_transport_path_groupoid_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2, default=int), encoding="utf-8")

    print("W33 Witting packet transport path-groupoid audit")
    for key, value in payload["packet_transport_path_groupoid_theorem"].items():
        print(f"  [{'PASS' if value else 'FAIL'}] {key}")
    print(f"  Wrote: {output_path}")
    print(f"  Runtime: {time.perf_counter() - timer:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
