#!/usr/bin/env python3
"""Exact carrier identification of the Parseval anti-line quotient.

This sharpens the target-side Parseval story beyond graph isomorphism.

After the fixed symplectic coordinate conversion between the line-carrier and
center-quad conventions,

1. the 90 Parseval anti-lines are exactly the 90 center-quads,
2. the duplicate anti-line feature pairing is exactly the antipodal quad
   involution,
3. the resulting 45 quotient classes are canonically the 45 quotient points of
   dual GQ(4,2),
4. the positive and negative anti-line sign graphs are exactly the transport
   graph SRG(45,32,22,24) and the quotient point graph SRG(45,12,3,3) on that
   same canonical labeling.

So the 90 -> 45 collapse in the Parseval audit is not an accidental feature
degeneracy. It is the existing center-quad/quotient transport carrier written
in the line-module convention.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
for extra in (ROOT, ROOT / "exploration"):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from exploration.w33_center_quad_gq42_e6_bridge import (  # noqa: E402
    center_quad_pairing,
    center_quads,
    quotient_incidence,
    quotient_lines,
    quotient_points,
    w33_points,
)
from exploration.w33_center_quad_transport_bridge import (  # noqa: E402
    reconstructed_quotient_graph,
)
from exploration.w33_line_spread_intertwiner_bridge import (  # noqa: E402
    _projective_points_f3_4,
)
from scripts.w33_parseval_measurement_frame_audit import (  # noqa: E402
    _build_parseval_probe_data,
)


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_parseval_transport_carrier_audit_summary.json"


def _normalize_projective(vector: tuple[int, int, int, int], q: int = 3) -> tuple[int, int, int, int]:
    reduced = tuple(entry % q for entry in vector)
    if not any(reduced):
        raise ValueError("zero vector is not projective")
    for entry in reduced:
        if entry:
            inv = 1 if entry == 1 else 2
            return tuple((inv * value) % q for value in reduced)
    raise AssertionError("unreachable projective normalization state")


def _line_to_center_convention(point: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    # The line carrier uses the symplectic pairings (0,1) and (2,3), while the
    # center-quad carrier uses (0,2) and (1,3). Swapping the middle coordinates
    # converts one convention to the other.
    return _normalize_projective((point[0], point[2], point[1], point[3]))


def _sign_adjacency(gram: np.ndarray, *, positive: bool) -> np.ndarray:
    size = gram.shape[0]
    adjacency = np.zeros((size, size), dtype=int)
    for left in range(size):
        for right in range(left + 1, size):
            value = int(gram[left, right])
            if positive and value > 0:
                adjacency[left, right] = adjacency[right, left] = 1
            if (not positive) and value < 0:
                adjacency[left, right] = adjacency[right, left] = 1
    return adjacency


def _graph_parameters(adjacency: np.ndarray) -> dict[str, int]:
    degrees = adjacency.sum(axis=1)
    degree_values = sorted(set(map(int, degrees)))
    if len(degree_values) != 1:
        raise AssertionError(f"graph is not regular: {degree_values}")

    adjacent_common = set()
    nonadjacent_common = set()
    for left in range(adjacency.shape[0]):
        for right in range(left + 1, adjacency.shape[0]):
            common = int(np.dot(adjacency[left], adjacency[right]))
            if adjacency[left, right]:
                adjacent_common.add(common)
            else:
                nonadjacent_common.add(common)

    return {
        "vertices": int(adjacency.shape[0]),
        "degree": degree_values[0],
        "lambda": next(iter(adjacent_common)),
        "mu": next(iter(nonadjacent_common)),
        "edge_count": int(adjacency.sum() // 2),
    }


def _quotient_point_graph() -> np.ndarray:
    point_to_lines, line_to_points = quotient_incidence()
    adjacency = np.zeros((len(point_to_lines), len(point_to_lines)), dtype=int)
    for line_points in line_to_points.values():
        for left, right in combinations(line_points, 2):
            adjacency[left, right] = adjacency[right, left] = 1
    return adjacency


def _support_mask(vertices: tuple[int, ...]) -> int:
    mask = 0
    for vertex in vertices:
        mask |= 1 << vertex
    return mask


def _five_cliques(adjacency: np.ndarray) -> list[tuple[int, int, int, int, int]]:
    cliques = []
    for vertices in combinations(range(adjacency.shape[0]), 5):
        if all(adjacency[left, right] for left, right in combinations(vertices, 2)):
            cliques.append(vertices)
    return cliques


@lru_cache(maxsize=1)
def build_parseval_transport_carrier_summary() -> dict[str, Any]:
    built = _build_parseval_probe_data()
    anti_projective_lines = built["anti_projective_lines"]
    R5 = built["R5"]

    line_points = _projective_points_f3_4()
    center_points = w33_points()
    center_point_index = {point: index for index, point in enumerate(center_points)}
    center_quad_list = center_quads()
    center_quad_index = {quad: index for index, quad in enumerate(center_quad_list)}
    center_pairing = center_quad_pairing()
    quotient_point_list = quotient_points()
    quotient_line_list = quotient_lines()
    pair_to_point_id = {point.quad_pair: point.point_id for point in quotient_point_list}

    converted_points = [_line_to_center_convention(point) for point in line_points]
    mapped_anti_lines = [
        tuple(sorted(center_point_index[_line_to_center_convention(point)] for point in anti_line))
        for anti_line in anti_projective_lines
    ]
    anti_line_quad_ids = [center_quad_index[quad] for quad in mapped_anti_lines]

    anti_column_classes: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for column_index in range(R5.shape[1]):
        anti_column_classes[tuple(int(value) for value in R5[:, column_index])].append(column_index)

    duplicate_pairs_by_point_id: dict[int, tuple[int, int]] = {}
    ordered_class_vectors: list[np.ndarray] = [np.zeros(40, dtype=int) for _ in quotient_point_list]
    ordered_supports: list[tuple[int, ...]] = [tuple() for _ in quotient_point_list]
    support_match_flags = []
    pairing_match_flags = []

    for vector_key, columns in anti_column_classes.items():
        pair = tuple(sorted(anti_line_quad_ids[column] for column in columns))
        expected_pair = tuple(sorted((pair[0], center_pairing[pair[0]])))
        pairing_match_flags.append(len(columns) == 2 and pair == expected_pair)
        point_id = pair_to_point_id[pair]
        duplicate_pairs_by_point_id[point_id] = pair
        ordered_class_vectors[point_id] = np.array(vector_key, dtype=int)

        support = tuple(sorted(set(center_quad_list[pair[0]]) | set(center_quad_list[pair[1]])))
        ordered_supports[point_id] = support
        support_match_flags.append(support == quotient_point_list[point_id].support_vertices)

    support_masks = [_support_mask(support) for support in ordered_supports]
    recovered_lines = []
    for point_ids in combinations(range(len(ordered_supports)), 5):
        union = 0
        ok = True
        for point_id in point_ids:
            mask = support_masks[point_id]
            if union & mask:
                ok = False
                break
            union |= mask
        if ok and union.bit_count() == 40:
            recovered_lines.append(point_ids)
    expected_lines = sorted(line.point_ids for line in quotient_line_list)
    recovered_lines = sorted(recovered_lines)

    quotient_point_adjacency = _quotient_point_graph()
    negative_graph_five_cliques = sorted(_five_cliques(quotient_point_adjacency))

    point_to_lines, _line_to_points = quotient_incidence()
    recovered_point_incidence = {point_id: 0 for point_id in range(len(ordered_supports))}
    for line in recovered_lines:
        for point_id in line:
            recovered_point_incidence[point_id] += 1

    ordered_columns = np.column_stack(ordered_class_vectors)
    anti_class_gram = ordered_columns.T @ ordered_columns
    positive_sign_graph = _sign_adjacency(anti_class_gram, positive=True)
    negative_sign_graph = _sign_adjacency(anti_class_gram, positive=False)

    transport_graph, _raw = reconstructed_quotient_graph()
    transport_adjacency = np.zeros((45, 45), dtype=int)
    for left, right in transport_graph.edges():
        transport_adjacency[left, right] = transport_adjacency[right, left] = 1

    summary = {
        "status": "ok",
        "coordinate_conversion": {
            "line_carrier_to_center_quad": "(x0,x1,x2,x3) -> (x0,x2,x1,x3)",
            "all_40_projective_points_match_after_permutation": set(converted_points) == set(center_points),
        },
        "anti_line_center_quad_bridge": {
            "anti_line_count": len(anti_projective_lines),
            "center_quad_count": len(center_quad_list),
            "mapped_anti_lines_equal_center_quads": set(mapped_anti_lines) == set(center_quad_list),
            "duplicate_class_count": len(anti_column_classes),
            "duplicate_class_size_distribution": dict(sorted(Counter(len(columns) for columns in anti_column_classes.values()).items())),
            "duplicate_pairing_equals_center_quad_antipodes": all(pairing_match_flags),
        },
        "quotient_point_bridge": {
            "quotient_point_count": len(quotient_point_list),
            "duplicate_pairs_equal_quotient_point_quad_pairs": set(duplicate_pairs_by_point_id.values())
            == {point.quad_pair for point in quotient_point_list},
            "duplicate_pair_supports_equal_quotient_point_supports": all(support_match_flags),
        },
        "quotient_line_bridge": {
            "quotient_line_count": len(quotient_line_list),
            "recovered_support_partitions_equal_quotient_lines": recovered_lines == expected_lines,
            "negative_sign_graph_five_cliques_equal_quotient_lines": negative_graph_five_cliques
            == expected_lines,
            "recovered_line_size_distribution": dict(sorted(Counter(len(line) for line in recovered_lines).items())),
            "recovered_point_line_incidence_distribution": dict(
                sorted(Counter(recovered_point_incidence.values()).items())
            ),
            "quotient_point_line_incidence_distribution": dict(
                sorted(Counter(len(point_to_lines[point_id]) for point_id in point_to_lines).items())
            ),
        },
        "canonical_graph_identification": {
            "positive_sign_graph_equals_transport_graph": bool(np.array_equal(positive_sign_graph, transport_adjacency)),
            "negative_sign_graph_equals_quotient_point_graph": bool(np.array_equal(negative_sign_graph, quotient_point_adjacency)),
            "transport_graph_parameters": _graph_parameters(transport_adjacency),
            "quotient_point_graph_parameters": _graph_parameters(quotient_point_adjacency),
        },
    }

    summary["theorem"] = {
        "the_90_parseval_anti_lines_are_exactly_the_90_center_quads_after_coordinate_conversion": (
            summary["coordinate_conversion"]["all_40_projective_points_match_after_permutation"]
            and summary["anti_line_center_quad_bridge"]
            == {
                "anti_line_count": 90,
                "center_quad_count": 90,
                "mapped_anti_lines_equal_center_quads": True,
                "duplicate_class_count": 45,
                "duplicate_class_size_distribution": {2: 45},
                "duplicate_pairing_equals_center_quad_antipodes": True,
            }
        ),
        "the_duplicate_anti_line_columns_are_exactly_the_45_quotient_points_of_dual_gq_4_2": (
            summary["quotient_point_bridge"]
            == {
                "quotient_point_count": 45,
                "duplicate_pairs_equal_quotient_point_quad_pairs": True,
                "duplicate_pair_supports_equal_quotient_point_supports": True,
            }
        ),
        "the_same_anti_line_carrier_recovers_the_full_27_line_dual_gq_4_2_incidence": (
            summary["quotient_line_bridge"]
            == {
                "quotient_line_count": 27,
                "recovered_support_partitions_equal_quotient_lines": True,
                "negative_sign_graph_five_cliques_equal_quotient_lines": True,
                "recovered_line_size_distribution": {5: 27},
                "recovered_point_line_incidence_distribution": {3: 45},
                "quotient_point_line_incidence_distribution": {3: 45},
            }
        ),
        "the_full_dual_gq_4_2_incidence_is_recoverable_from_the_negative_sign_graph_alone": (
            summary["quotient_line_bridge"]["negative_sign_graph_five_cliques_equal_quotient_lines"]
        ),
        "the_positive_and_negative_anti_line_sign_graphs_are_exactly_the_transport_and_quotient_point_graphs": (
            summary["canonical_graph_identification"]
            == {
                "positive_sign_graph_equals_transport_graph": True,
                "negative_sign_graph_equals_quotient_point_graph": True,
                "transport_graph_parameters": {
                    "vertices": 45,
                    "degree": 32,
                    "lambda": 22,
                    "mu": 24,
                    "edge_count": 720,
                },
                "quotient_point_graph_parameters": {
                    "vertices": 45,
                    "degree": 12,
                    "lambda": 3,
                    "mu": 3,
                    "edge_count": 270,
                },
            }
        ),
    }

    summary["interpretation"] = (
        "The Parseval anti-line quotient is not merely isomorphic to the 45-point transport graph. "
        "After the fixed symplectic coordinate conversion, the 90 anti-lines are the 90 center-quads "
        "themselves, the duplicate-column collapse is exactly the antipodal quad involution, and the 45 "
        "unique anti-line classes are canonically the quotient points of dual GQ(4,2), with the 27 quotient "
        "lines recovered directly as the 5-tuples of class supports that partition the 40 vertices; equivalently, "
        "they are exactly the 27 five-cliques of the negative sign graph. On that same labeling, negative inner "
        "product is the quotient point graph SRG(45,12,3,3) and positive inner product is its transport complement "
        "SRG(45,32,22,24)."
    )
    return summary


def write_summary(output_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    output_path.write_text(
        json.dumps(build_parseval_transport_carrier_summary(), indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    output_path = write_summary()
    summary = build_parseval_transport_carrier_summary()

    print("=" * 72)
    print("W33 PARSEVAL TRANSPORT CARRIER AUDIT")
    print("=" * 72)
    print(f"wrote: {output_path}")
    for key, value in summary["theorem"].items():
        print(f"  [{'PASS' if value else 'FAIL'}] {key}")


if __name__ == "__main__":
    main()