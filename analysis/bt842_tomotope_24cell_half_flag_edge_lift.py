#!/usr/bin/env python3
"""
BT842 - Tomotope half-flags are the 24-cell edge lift of the Reye spine.

MCXCIII proved that the tomotope middle layer and the 24-cell share the same
Reye configuration:

    12 axes x 16 hexagon planes with 48 incidences.

This verifier adds the missing edge-level statement.  In the D4-root model of
the 24-cell, every edge lies in a unique central hexagon plane.  Its endpoints
use two of the three axes in that plane, leaving a unique missing axis.  Thus
each 24-cell edge maps to one Reye incidence (missing axis, hexagon plane), and
each incidence has exactly two preimage edges:

    96 edges = 2 * 48 Reye incidences.

That is exactly the tomotope omnitruncated half-flag count from BT839 and half
of the BT814 192 full flags.

The user-suggested hexagon/11-cell hint is also tested: each central hexagon is
a six-vertex carrier.  Completing its cyclic C6 edges to the full K6 duad
system gives 15 duads, the hemi-icosahedral skeleton count of the 11-cell cell.
Across the 16 hexagons this gives 240 duad slots, the W33 edge/E8-root count.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


Vector4 = tuple[int, int, int, int]


def d4_roots() -> list[Vector4]:
    roots: list[Vector4] = []
    for left, right in combinations(range(4), 2):
        for left_sign in (-1, 1):
            for right_sign in (-1, 1):
                vector = [0, 0, 0, 0]
                vector[left] = left_sign
                vector[right] = right_sign
                roots.append(tuple(vector))  # type: ignore[arg-type]
    return sorted(roots)


def rank_rational(vectors: list[Vector4]) -> int:
    matrix = [[Fraction(entry) for entry in vector] for vector in vectors]
    rank = 0
    for col in range(4):
        pivot = None
        for row in range(rank, len(matrix)):
            if matrix[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][col]
        matrix[rank] = [entry / scale for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][col]:
                factor = matrix[row][col]
                matrix[row] = [matrix[row][idx] - factor * matrix[rank][idx] for idx in range(4)]
        rank += 1
    return rank


def twenty_four_cell_axes(roots: list[Vector4]) -> list[tuple[Vector4, Vector4]]:
    seen: set[Vector4] = set()
    axes: list[tuple[Vector4, Vector4]] = []
    for root in roots:
        if root in seen:
            continue
        opposite = tuple(-entry for entry in root)  # type: ignore[assignment]
        axis = tuple(sorted((root, opposite)))  # type: ignore[assignment]
        axes.append(axis)
        seen.add(root)
        seen.add(opposite)
    return sorted(axes)


def twenty_four_cell_hexagon_planes(roots: list[Vector4], axes: list[tuple[Vector4, Vector4]]) -> list[tuple[int, int, int]]:
    planes: list[tuple[int, int, int]] = []
    for triple in combinations(range(len(axes)), 3):
        plane_vectors = [vector for axis_index in triple for vector in axes[axis_index]]
        if rank_rational(plane_vectors) != 2:
            continue
        roots_in_this_plane = [root for root in roots if rank_rational([*plane_vectors, root]) == 2]
        if len(roots_in_this_plane) == 6:
            planes.append(triple)
    return planes


def dot(left: Vector4, right: Vector4) -> int:
    return sum(a * b for a, b in zip(left, right))


def axis_index_map(axes: list[tuple[Vector4, Vector4]]) -> dict[Vector4, int]:
    out: dict[Vector4, int] = {}
    for idx, axis in enumerate(axes):
        for root in axis:
            out[root] = idx
    return out


def roots_in_plane(roots: list[Vector4], axes: list[tuple[Vector4, Vector4]], plane: tuple[int, int, int]) -> list[Vector4]:
    plane_vectors = [root for axis_index in plane for root in axes[axis_index]]
    return [root for root in roots if rank_rational([*plane_vectors, root]) == 2]


def is_connected_cycle(vertices: list[Vector4], edges: list[tuple[Vector4, Vector4]]) -> bool:
    if len(vertices) != 6 or len(edges) != 6:
        return False
    graph = {vertex: set() for vertex in vertices}
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    if Counter(len(neighbors) for neighbors in graph.values()) != {2: 6}:
        return False
    seen = {vertices[0]}
    queue: deque[Vector4] = deque([vertices[0]])
    while queue:
        current = queue.popleft()
        for nxt in graph[current]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return len(seen) == 6


def main() -> None:
    roots = d4_roots()
    axes = twenty_four_cell_axes(roots)
    axis_of = axis_index_map(axes)
    planes = twenty_four_cell_hexagon_planes(roots, axes)
    bt814 = json.loads((ROOT / "data" / "bt814_tomotope_middle_layer_from_residual_tetrahedra.json").read_text())
    bt839 = json.loads((ROOT / "data" / "bt839_gc_operation_euler_flag_audit.json").read_text())

    edges24 = [
        tuple(sorted((left, right)))
        for left, right in combinations(roots, 2)
        if dot(left, right) == 1
    ]

    incidence_to_edges: dict[tuple[int, int], list[tuple[Vector4, Vector4]]] = defaultdict(list)
    edge_rows = []
    for edge in edges24:
        left, right = edge
        used_axes = tuple(sorted((axis_of[left], axis_of[right])))
        containing_planes = [
            idx for idx, plane in enumerate(planes)
            if used_axes[0] in plane and used_axes[1] in plane
        ]
        if len(containing_planes) != 1:
            raise AssertionError(f"edge {edge} has plane candidates {containing_planes}")
        plane_index = containing_planes[0]
        missing_axis = next(axis for axis in planes[plane_index] if axis not in used_axes)
        incidence_to_edges[(missing_axis, plane_index)].append(edge)
        edge_rows.append(
            {
                "edge": [list(left), list(right)],
                "used_axes": list(used_axes),
                "hexagon_plane": plane_index,
                "missing_axis_reye_label": missing_axis,
            }
        )

    hexagon_rows = []
    k6_duad_slots = []
    for plane_index, plane in enumerate(planes):
        plane_roots = sorted(roots_in_plane(roots, axes, plane))
        plane_edges = [
            tuple(sorted((left, right)))
            for left, right in combinations(plane_roots, 2)
            if dot(left, right) == 1
        ]
        all_duads = [
            tuple(sorted((left, right)))
            for left, right in combinations(plane_roots, 2)
        ]
        for duad in all_duads:
            k6_duad_slots.append((plane_index, duad))
        hexagon_rows.append(
            {
                "plane_index": plane_index,
                "axes": list(plane),
                "root_count": len(plane_roots),
                "cycle_edge_count": len(plane_edges),
                "k6_duad_count": len(all_duads),
                "is_c6": is_connected_cycle(plane_roots, plane_edges),
            }
        )

    duad_multiplicity = Counter(duad for _plane, duad in k6_duad_slots)
    duad_dot_profile = Counter(dot(left, right) for _plane, (left, right) in k6_duad_slots)
    distinct_duad_dot_profile = Counter(dot(left, right) for left, right in duad_multiplicity)
    incidence_preimage_profile = Counter(len(value) for value in incidence_to_edges.values())
    half_flags_bt814 = bt814["f_vector_from_transversal_tetrahedra"]["flags_if_each_block_has_2x2_fiber"] // 2
    half_flags_bt839 = bt839["flag_bridge"]["tomotope_partial_b"]["omnitruncated_vertices"]

    checks = {
        "d4_roots_are_24": len(roots) == 24,
        "axes_are_12": len(axes) == 12,
        "hexagon_planes_are_16": len(planes) == 16,
        "twenty_four_cell_edges_are_96": len(edges24) == 96,
        "spine_has_48_reye_incidences": sum(len(plane) for plane in planes) == 48,
        "edge_to_reye_incidence_has_48_targets": len(incidence_to_edges) == 48,
        "each_reye_incidence_has_two_edge_lifts": incidence_preimage_profile == {2: 48},
        "edge_lift_is_tomotope_half_flags": len(edges24) == half_flags_bt814 == half_flags_bt839 == 96,
        "each_hexagon_is_c6_on_six_roots": Counter((row["root_count"], row["cycle_edge_count"], row["is_c6"]) for row in hexagon_rows)
        == {(6, 6, True): 16},
        "each_hexagon_completion_is_k6_with_15_duads": Counter(row["k6_duad_count"] for row in hexagon_rows) == {15: 16},
        "hexagon_k6_duad_slots_total_240": len(k6_duad_slots) == 16 * 15 == 240,
        "k6_duad_dot_profile_is_96_96_48": duad_dot_profile == {-2: 48, -1: 96, 1: 96},
        "distinct_duads_are_204_with_axis_repeats": len(duad_multiplicity) == 204 and Counter(duad_multiplicity.values()) == {1: 192, 4: 12},
        "distinct_duad_dot_profile_is_96_96_12": distinct_duad_dot_profile == {-2: 12, -1: 96, 1: 96},
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT842 check failed: {name}")

    out = {
        "theorem": "BT842 tomotope 24-cell half-flag edge lift",
        "edge_lift": {
            "twenty_four_cell_edges": len(edges24),
            "reye_incidences": len(incidence_to_edges),
            "preimage_profile": dict(sorted(incidence_preimage_profile.items())),
            "identity": "96 = 2*48",
            "tomotope_half_flags": {
                "BT814_half_of_192": half_flags_bt814,
                "BT839_omnitruncated_half_flags": half_flags_bt839,
            },
            "sample_edge_rows": edge_rows[:12],
        },
        "hexagon_k6_completion": {
            "hexagon_planes": len(hexagon_rows),
            "roots_per_hexagon": 6,
            "cycle_edges_per_hexagon": 6,
            "k6_duads_per_hexagon": 15,
            "duad_slots_total": len(k6_duad_slots),
            "duad_dot_profile_with_multiplicity": dict(sorted(duad_dot_profile.items())),
            "distinct_duad_count": len(duad_multiplicity),
            "distinct_duad_multiplicity_profile": dict(sorted(Counter(duad_multiplicity.values()).items())),
            "distinct_duad_dot_profile": dict(sorted(distinct_duad_dot_profile.items())),
            "sample_hexagons": hexagon_rows[:6],
        },
        "hexagon_11cell_reading": {
            "central_hexagon": "the 24-cell supplies a C6 on six D4 roots",
            "completion": "completing C6 to K6 gives 15 duads, the hemi-icosahedral skeleton count of the 11-cell cell",
            "w33_e8_count": "16 completed hexagons give 240 duad slots, matching W33 edges / E8 roots",
            "boundary": "the 24-cell uses the cyclic six edges; the 11-cell cell uses the full K6 duad completion",
        },
        "checks": checks,
    }
    path = ROOT / "data" / "bt842_tomotope_24cell_half_flag_edge_lift.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
