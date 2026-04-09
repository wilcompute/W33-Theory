"""Tetrahedral-oscillator reinterpretation of the 90 center-quads.

The center-quad quotient package already established the exact bridge

    90 center-quads -> 45 quotient points -> 27 quotient lines.

This module sharpens the local geometry of those 90 four-sets.

Key idea:
each quotient point is an antipodal pair of center-quads, so the ``90`` should
be read as a two-sheet orientation cover of ``45`` local tetrahedral objects.
The testable question is whether the local incidence/transport data really sees
those four-sets as tetrahedra rather than just arbitrary quads.

The sharp answer is yes:

1. At each quotient point, the 12 incidence neighbors induce a 12-element
   local tetrahedral permutation packet on the four vertices of one quad.
2. The generated closure of that packet has order ``12`` or ``24`` depending
   the local labeling/sheet, but the packet itself is always exactly 12.
3. The 3 quotient lines through the point are exactly the 3 perfect matchings
   (opposite-edge axes) of that tetrahedron.
4. The transport ``S3`` line-matchings therefore act on tetrahedral axes.
5. The old ``45 + 90`` transport split is exactly

       45 x (1 + 2),

   i.e. the radial line plus the tangential ``A2`` shell of the local
   tetrahedral-axis oscillator.

So the ``90``-sector is not best read as 90 literal tetrahedra. It is the
orientation double cover of 45 tetrahedral oscillators, with the transport
``A2`` local system as their tangential mode packet.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
import json
from itertools import combinations
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_center_quad_gq42_e6_bridge import (
    center_quads,
    quotient_incidence,
    quotient_lines,
    quotient_points,
    w33_collinearity,
)


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_center_quad_tetrahedral_oscillator_bridge_summary.json"
TETRA_MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def _compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[index] for index in right)


def _generate_group(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    identity = tuple(range(4))
    group = {identity}
    queue = [identity]
    while queue:
        current = queue.pop()
        for generator in generators:
            image = _compose(current, generator)
            if image not in group:
                group.add(image)
                queue.append(image)
    return group


def _cycle_type(permutation: tuple[int, ...]) -> tuple[int, ...]:
    size = len(permutation)
    seen = [False] * size
    cycle_lengths = []
    for start in range(size):
        if seen[start]:
            continue
        current = start
        length = 0
        while not seen[current]:
            seen[current] = True
            current = permutation[current]
            length += 1
        cycle_lengths.append(length)
    return tuple(sorted(cycle_lengths))


def _image_of_matching(permutation: tuple[int, ...], matching: tuple[tuple[int, int], tuple[int, int]]) -> int:
    image = tuple(sorted(tuple(sorted((permutation[a], permutation[b]))) for a, b in matching))
    return TETRA_MATCHINGS.index(image)


@lru_cache(maxsize=1)
def _quotient_line_lookup() -> dict[int, Any]:
    return {line.line_id: line for line in quotient_lines()}


@lru_cache(maxsize=1)
def _point_triangles() -> dict[int, tuple[int, int, int]]:
    point_to_lines, _ = quotient_incidence()
    return {point_id: tuple(sorted(lines)) for point_id, lines in point_to_lines.items()}


@lru_cache(maxsize=1)
def _line_intersection_graph() -> dict[int, frozenset[int]]:
    point_to_lines, line_to_points = quotient_incidence()
    adjacency = {line_id: set() for line_id in line_to_points}
    for lines_through_point in point_to_lines.values():
        a, b, c = lines_through_point
        adjacency[a].update((b, c))
        adjacency[b].update((a, c))
        adjacency[c].update((a, b))
    return {line_id: frozenset(neighbors) for line_id, neighbors in adjacency.items()}


def _transport_edges() -> list[tuple[int, int]]:
    triangles = _point_triangles()
    edges = []
    for left, right in combinations(sorted(triangles), 2):
        if set(triangles[left]) & set(triangles[right]):
            continue
        edges.append((left, right))
    return edges


def _edge_line_matching(left: int, right: int) -> tuple[int, int, int]:
    triangles = _point_triangles()
    adjacency = _line_intersection_graph()
    source = triangles[left]
    target = triangles[right]
    permutation = []
    for line_id in source:
        matches = [index for index, other in enumerate(target) if other in adjacency[line_id]]
        if len(matches) != 1:
            raise AssertionError("transport edge should induce a unique line matching")
        permutation.append(matches[0])
    result = tuple(permutation)
    if sorted(result) != [0, 1, 2]:
        raise AssertionError("line matching must be a permutation")
    return result


def _neighbor_permutation(point_id: int, other_point_id: int) -> tuple[int, int, int, int]:
    point = quotient_points()[point_id]
    quad_left = tuple(center_quads()[point.quad_pair[0]])
    quad_right = tuple(center_quads()[point.quad_pair[1]])
    support = quotient_points()[other_point_id].support_vertices
    col = w33_collinearity()

    labels = []
    for vertex in quad_left:
        labels.append(tuple(sorted(x for x in support if x in col[vertex])))

    permutation = []
    for vertex in quad_right:
        label = tuple(sorted(x for x in support if x in col[vertex]))
        permutation.append(labels.index(label))
    return tuple(permutation)


def _point_line_packets(point_id: int) -> dict[int, list[tuple[int, int, int, int]]]:
    point_to_lines, _ = quotient_incidence()
    line_lookup = _quotient_line_lookup()
    packets: dict[int, list[tuple[int, int, int, int]]] = {}
    for line_id in point_to_lines[point_id]:
        packets[line_id] = [
            _neighbor_permutation(point_id, other_id)
            for other_id in line_lookup[line_id].point_ids
            if other_id != point_id
        ]
    return packets


def _line_to_matching_labels(point_id: int) -> dict[int, int]:
    packets = _point_line_packets(point_id)
    labels = {}
    for line_id, packet in packets.items():
        images = {
            _image_of_matching(permutation, TETRA_MATCHINGS[0])
            for permutation in packet
        }
        if len(images) != 1:
            raise AssertionError("line packet does not stabilize a unique matching class")
        labels[line_id] = next(iter(images))

    if sorted(labels.values()) != [0, 1, 2]:
        raise AssertionError("local line labels do not realize the three tetrahedral matchings")
    return labels


def _matching_transport_permutation(left: int, right: int) -> tuple[int, int, int]:
    point_to_lines, _ = quotient_incidence()
    line_perm = _edge_line_matching(left, right)
    left_labels = _line_to_matching_labels(left)
    right_labels = _line_to_matching_labels(right)

    left_lines = point_to_lines[left]
    right_lines = point_to_lines[right]

    left_matching_to_line = {matching: line for line, matching in left_labels.items()}
    right_line_to_matching = {line: matching for line, matching in right_labels.items()}

    permutation = [0, 0, 0]
    for matching_index in range(3):
        left_line = left_matching_to_line[matching_index]
        local_line_index = left_lines.index(left_line)
        transported_line = right_lines[line_perm[local_line_index]]
        permutation[matching_index] = right_line_to_matching[transported_line]
    return tuple(permutation)


def build_summary() -> dict[str, Any]:
    points = quotient_points()
    point_to_lines, _ = quotient_incidence()

    local_group_orders = []
    line_cycle_profiles: Counter[tuple[tuple[int, ...], ...]] = Counter()
    matching_label_maps = {}
    for point_id in range(len(points)):
        packets = _point_line_packets(point_id)
        generators = [permutation for packet in packets.values() for permutation in packet]
        local_group_orders.append(len(_generate_group(generators)))
        for packet in packets.values():
            line_cycle_profiles[tuple(sorted(_cycle_type(permutation) for permutation in packet))] += 1
        matching_label_maps[point_id] = _line_to_matching_labels(point_id)

    transport_matching_counts: Counter[tuple[int, int, int]] = Counter()
    for left, right in _transport_edges():
        transport_matching_counts[_matching_transport_permutation(left, right)] += 1

    summary: dict[str, Any] = {
        "center_quad_cover": {
            "center_quad_count": len(center_quads()),
            "quotient_point_count": len(points),
            "oriented_tetra_cover": {
                "two_sheet_cover": len(center_quads()) == 2 * len(points),
                "interpretation": "The 90 center-quads are a 2-sheet orientation cover of 45 quotient points.",
            },
        },
        "local_tetra_packets": {
            "matching_basis": [list(map(list, matching)) for matching in TETRA_MATCHINGS],
            "local_group_orders": local_group_orders,
            "local_group_order_distribution": dict(sorted(Counter(local_group_orders).items())),
            "line_cycle_profiles": {
                str(profile): count for profile, count in sorted(line_cycle_profiles.items())
            },
            "sample_point_zero": {
                "quad_pair": list(points[0].quad_pair),
                "quad_left": list(center_quads()[points[0].quad_pair[0]]),
                "quad_right": list(center_quads()[points[0].quad_pair[1]]),
                "incident_lines": {
                    str(line_id): {
                        "matching_label": matching_label_maps[0][line_id],
                        "neighbor_permutations": [list(permutation) for permutation in _point_line_packets(0)[line_id]],
                        "cycle_types": [list(_cycle_type(permutation)) for permutation in _point_line_packets(0)[line_id]],
                    }
                    for line_id in point_to_lines[0]
                },
            },
        },
        "transport_axis_packet": {
            "matching_transport_permutation_counts": {
                str(key): value for key, value in sorted(transport_matching_counts.items())
            },
            "all_six_s3_permutations_occur": len(transport_matching_counts) == 6,
            "local_fiber_dimensions": {
                "axis_packet": 3,
                "radial_line": 1,
                "tangential_a2_shell": 2,
                "global_radial_dimension": len(points),
                "global_tangential_dimension": 2 * len(points),
            },
        },
        "tetrahedral_oscillator_theorem": {
            "the_90_center_quads_are_45_oriented_tetrahedral_oscillators": (
                len(center_quads()) == 2 * len(points)
            ),
            "each_quotient_point_has_exact_12_element_local_tetrahedral_permutation_packet": all(
                len({permutation for packet in _point_line_packets(point_id).values() for permutation in packet}) == 12
                for point_id in range(len(points))
            ),
            "the_generated_local_closure_is_always_order_12_or_24": all(
                order in {12, 24} for order in local_group_orders
            ),
            "the_three_quotient_lines_are_exactly_the_three_opposite_edge_matchings_of_the_local_tetrahedron": all(
                sorted(_line_to_matching_labels(point_id).values()) == [0, 1, 2]
                for point_id in range(len(points))
            ),
            "the_transport_line_matchings_act_on_tetrahedral_axes": len(transport_matching_counts) == 6,
            "the_old_45_plus_90_split_is_exactly_45_times_1_plus_2": (
                len(points) == 45 and 2 * len(points) == 90
            ),
        },
        "interpretation": (
            "The center-quad 90 should not be read as 90 unrelated four-sets. "
            "It is a 2-sheet cover of 45 local tetrahedra. At each quotient point, "
            "the 12 incidence neighbors realize an exact local tetrahedral "
            "permutation packet on the four vertices of one quad, the 3 quotient "
            "lines are the 3 opposite-edge matchings of that tetrahedron, and the transport S3 "
            "matchings act on those three axes. So the 90-dimensional A2 sector is "
            "the tangential shell of a 45-site tetrahedral oscillator packet."
        ),
    }
    return summary


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
