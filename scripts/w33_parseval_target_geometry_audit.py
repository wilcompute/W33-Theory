#!/usr/bin/env python3
"""Exact target-side geometry and Naimark-shadow audit for the Parseval frame.

This packages the theorem chain behind Parts LXXIV--LXXVII:

1. the spread target is an exact ETF(36,15),
2. the anti-line target collapses to a doubled 45-vector two-distance tight
   frame in the 24-sector,
3. both targets expose the same hidden Naimark shadow split 21 = 1 + 20,
4. the Naimark complement swaps the positive and negative target-side SRG
   signatures on both channels.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
for extra in (ROOT, ROOT / "exploration", ROOT / "pillars"):
    extra_str = str(extra)
    if extra_str not in sys.path:
        sys.path.insert(0, extra_str)

from exploration._optional_deps import require_networkx  # noqa: E402
from exploration.w33_center_quad_transport_bridge import (  # noqa: E402
    reconstructed_quotient_graph,
)
from scripts.w33_parseval_measurement_frame_audit import (  # noqa: E402
    _build_parseval_probe_data,
)
from scripts.w33_parseval_transport_carrier_audit import (  # noqa: E402
    build_parseval_transport_carrier_summary,
)


nx = require_networkx("scripts/w33_parseval_target_geometry_audit.py")

DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_parseval_target_geometry_audit_summary.json"


def _fraction_string(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _spectrum(matrix: np.ndarray) -> dict[str, int]:
    eigenvalues = np.rint(np.linalg.eigvalsh(matrix.astype(float))).astype(int)
    return {str(key): value for key, value in sorted(Counter(int(x) for x in eigenvalues).items())}


def _sign_graph(gram: np.ndarray, positive: bool) -> np.ndarray:
    size = gram.shape[0]
    adjacency = np.zeros((size, size), dtype=int)
    for left in range(size):
        for right in range(left + 1, size):
            value = float(gram[left, right])
            if positive and value > 1e-9:
                adjacency[left, right] = adjacency[right, left] = 1
            if (not positive) and value < -1e-9:
                adjacency[left, right] = adjacency[right, left] = 1
    return adjacency


def _graph_parameters(adjacency: np.ndarray) -> dict[str, Any]:
    degrees = adjacency.sum(axis=1)
    degree_values = sorted(set(map(int, degrees)))
    if len(degree_values) != 1:
        raise AssertionError(f"Graph is not regular: {degree_values}")

    adjacent_common: set[int] = set()
    nonadjacent_common: set[int] = set()
    for left in range(adjacency.shape[0]):
        for right in range(left + 1, adjacency.shape[0]):
            common = int(np.dot(adjacency[left], adjacency[right]))
            if adjacency[left, right]:
                adjacent_common.add(common)
            else:
                nonadjacent_common.add(common)

    adjacency_spectrum = _spectrum(adjacency)
    return {
        "vertices": int(adjacency.shape[0]),
        "degree": degree_values[0],
        "lambda": next(iter(adjacent_common)),
        "mu": next(iter(nonadjacent_common)),
        "edge_count": int(adjacency.sum() // 2),
        "spectrum": adjacency_spectrum,
    }


def _naimark_parseval_gram(columns: np.ndarray) -> np.ndarray:
    frame_operator = columns @ columns.T
    eigenvalues, eigenvectors = np.linalg.eigh(frame_operator.astype(float))
    positive = eigenvalues > 1e-9
    inverse_sqrt = eigenvectors[:, positive] @ np.diag(eigenvalues[positive] ** -0.5) @ eigenvectors[:, positive].T
    parseval_columns = inverse_sqrt @ columns
    return parseval_columns.T @ parseval_columns


def _fraction_values_from_gram(gram: np.ndarray) -> tuple[Fraction, list[Fraction]]:
    diagonal_values = {Fraction(str(round(float(gram[index, index]), 12))).limit_denominator() for index in range(gram.shape[0])}
    if len(diagonal_values) != 1:
        raise AssertionError(f"Expected one diagonal value, found {sorted(diagonal_values)}")
    off_diagonal_values = {
        Fraction(str(round(float(gram[left, right]), 12))).limit_denominator()
        for left in range(gram.shape[0])
        for right in range(gram.shape[0])
        if left != right
    }
    return next(iter(diagonal_values)), sorted(off_diagonal_values)


def _matrix_graph_to_networkx(adjacency: np.ndarray) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(adjacency.shape[0]))
    for left in range(adjacency.shape[0]):
        for right in range(left + 1, adjacency.shape[0]):
            if adjacency[left, right]:
                graph.add_edge(left, right)
    return graph


@lru_cache(maxsize=1)
def build_parseval_target_geometry_summary() -> dict[str, Any]:
    built = _build_parseval_probe_data()
    B4 = built["B4"]
    R5 = built["R5"]
    anti_lines = built["anti_projective_lines"]
    transport_carrier = build_parseval_transport_carrier_summary()

    spread_integer_gram = B4.T @ B4
    spread_gram = spread_integer_gram / 16.0
    spread_parseval_gram = spread_integer_gram / 288.0
    spread_shadow_parseval_gram = np.eye(36) - spread_parseval_gram

    anti_column_classes: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for column_index in range(R5.shape[1]):
        anti_column_classes[tuple(int(value) for value in R5[:, column_index])].append(column_index)
    duplicate_classes = list(anti_column_classes.values())
    unique_anti_integer_columns = np.array(list(anti_column_classes.keys()), dtype=int).T
    anti_unique_integer_gram = unique_anti_integer_columns.T @ unique_anti_integer_columns
    anti_unique_gram = anti_unique_integer_gram / 25.0
    anti_unique_parseval_gram = anti_unique_integer_gram / 450.0
    anti_shadow_parseval_gram = np.eye(45) - anti_unique_parseval_gram

    spread_positive_graph = _sign_graph(spread_gram, positive=True)
    spread_negative_graph = _sign_graph(spread_gram, positive=False)
    anti_positive_graph = _sign_graph(anti_unique_gram, positive=True)
    anti_negative_graph = _sign_graph(anti_unique_gram, positive=False)
    spread_shadow_positive_graph = _sign_graph(spread_shadow_parseval_gram, positive=True)
    spread_shadow_negative_graph = _sign_graph(spread_shadow_parseval_gram, positive=False)
    anti_shadow_positive_graph = _sign_graph(anti_shadow_parseval_gram, positive=True)
    anti_shadow_negative_graph = _sign_graph(anti_shadow_parseval_gram, positive=False)

    overlap_by_spread_sign = Counter()
    BtB = built["B"].T @ built["B"]
    for left in range(BtB.shape[0]):
        for right in range(left + 1, BtB.shape[0]):
            sign = "+" if spread_gram[left, right] > 0 else "-"
            overlap_by_spread_sign[(sign, int(BtB[left, right]))] += 1

    duplicate_pairs_are_disjoint = all(
        len(set(anti_lines[group[0]]) & set(anti_lines[group[1]])) == 0 for group in duplicate_classes
    )

    transport_graph, _raw = reconstructed_quotient_graph()
    anti_positive_graph_is_transport = nx.is_isomorphic(
        _matrix_graph_to_networkx(anti_positive_graph),
        transport_graph,
    )

    spread_diag, spread_off = _fraction_values_from_gram(spread_gram)
    anti_diag, anti_off = _fraction_values_from_gram(anti_unique_gram)
    spread_shadow_diag, spread_shadow_off = _fraction_values_from_gram(spread_shadow_parseval_gram)
    anti_shadow_diag, anti_shadow_off = _fraction_values_from_gram(anti_shadow_parseval_gram)

    summary = {
        "status": "ok",
        "target_side_frame_geometry": {
            "spread_etf": {
                "frame_type": "ETF(36,15)",
                "vector_count": 36,
                "sector_dimension": 15,
                "column_norm_squared": _fraction_string(spread_diag),
                "off_diagonal_inner_products": [_fraction_string(value) for value in spread_off],
                "normalized_coherence": _fraction_string(abs(spread_off[-1]) / spread_diag),
                "welch_bound_squared": "1/25",
                "frame_operator_spectrum": _spectrum(spread_gram),
                "positive_sign_graph": _graph_parameters(spread_positive_graph),
                "negative_sign_graph": _graph_parameters(spread_negative_graph),
                "positive_sign_equals_overlap_4_graph": overlap_by_spread_sign[("+", 4)] == 270,
                "negative_sign_equals_overlap_1_graph": overlap_by_spread_sign[("-", 1)] == 360,
            },
            "anti_line_quotient": {
                "frame_type": "doubled two-distance tight frame(45,24)",
                "anti_line_count": 90,
                "duplicate_class_count": 45,
                "duplicate_multiplicity": 2,
                "duplicate_pairs_are_disjoint": duplicate_pairs_are_disjoint,
                "sector_dimension": 24,
                "column_norm_squared": _fraction_string(anti_diag),
                "off_diagonal_inner_products": [_fraction_string(value) for value in anti_off],
                "frame_operator_spectrum": _spectrum(anti_unique_gram),
                "positive_sign_graph": _graph_parameters(anti_positive_graph),
                "negative_sign_graph": _graph_parameters(anti_negative_graph),
                "positive_sign_isomorphic_to_transport_graph": anti_positive_graph_is_transport,
                "canonical_transport_carrier": {
                    "coordinate_conversion": transport_carrier["coordinate_conversion"][
                        "line_carrier_to_center_quad"
                    ],
                    "anti_lines_equal_center_quads_after_coordinate_conversion": transport_carrier[
                        "anti_line_center_quad_bridge"
                    ]["mapped_anti_lines_equal_center_quads"],
                    "duplicate_pairing_equals_center_quad_antipodes": transport_carrier[
                        "anti_line_center_quad_bridge"
                    ]["duplicate_pairing_equals_center_quad_antipodes"],
                    "duplicate_classes_equal_quotient_point_quad_pairs": transport_carrier[
                        "quotient_point_bridge"
                    ]["duplicate_pairs_equal_quotient_point_quad_pairs"],
                    "paired_supports_equal_quotient_point_supports": transport_carrier[
                        "quotient_point_bridge"
                    ]["duplicate_pair_supports_equal_quotient_point_supports"],
                    "quotient_line_count": transport_carrier["quotient_line_bridge"]["quotient_line_count"],
                    "support_partitions_equal_quotient_lines": transport_carrier["quotient_line_bridge"][
                        "recovered_support_partitions_equal_quotient_lines"
                    ],
                    "line_size_distribution": transport_carrier["quotient_line_bridge"][
                        "recovered_line_size_distribution"
                    ],
                    "point_line_incidence_distribution": transport_carrier["quotient_line_bridge"][
                        "recovered_point_line_incidence_distribution"
                    ],
                    "negative_sign_graph_five_cliques_equal_quotient_lines": transport_carrier[
                        "quotient_line_bridge"
                    ]["negative_sign_graph_five_cliques_equal_quotient_lines"],
                    "positive_sign_equals_transport_graph_without_relabeling": transport_carrier[
                        "canonical_graph_identification"
                    ]["positive_sign_graph_equals_transport_graph"],
                    "negative_sign_equals_quotient_point_graph_without_relabeling": transport_carrier[
                        "canonical_graph_identification"
                    ]["negative_sign_graph_equals_quotient_point_graph"],
                },
            },
        },
        "common_naimark_shadow": {
            "shared_shadow_dimension": 21,
            "shared_shadow_split": "1 + 20",
            "shared_shadow_arithmetic": {
                "21_equals_q_phi6": "3 * 7",
                "20_equals_edge_count_over_degree": "240 / 12",
            },
            "spread_shadow": {
                "frame_type": "ETF(36,21)",
                "parseval_diagonal": _fraction_string(spread_shadow_diag),
                "parseval_off_diagonal": [_fraction_string(value) for value in spread_shadow_off],
                "normalized_coherence": _fraction_string(abs(spread_shadow_off[-1]) / spread_shadow_diag),
                "positive_sign_graph": _graph_parameters(spread_shadow_positive_graph),
                "negative_sign_graph": _graph_parameters(spread_shadow_negative_graph),
            },
            "anti_line_shadow": {
                "frame_type": "two-distance shadow frame(45,21)",
                "vector_count": 45,
                "parseval_diagonal": _fraction_string(anti_shadow_diag),
                "parseval_off_diagonal": [_fraction_string(value) for value in anti_shadow_off],
                "normalized_off_diagonal": [
                    _fraction_string(value / anti_shadow_diag) for value in anti_shadow_off
                ],
                "positive_sign_graph": _graph_parameters(anti_shadow_positive_graph),
                "negative_sign_graph": _graph_parameters(anti_shadow_negative_graph),
            },
        },
        "naimark_sign_duality": {
            "spread_shadow_positive_equals_visible_negative": bool(
                np.array_equal(spread_shadow_positive_graph, spread_negative_graph)
            ),
            "spread_shadow_negative_equals_visible_positive": bool(
                np.array_equal(spread_shadow_negative_graph, spread_positive_graph)
            ),
            "anti_shadow_positive_equals_visible_negative": bool(
                np.array_equal(anti_shadow_positive_graph, anti_negative_graph)
            ),
            "anti_shadow_negative_equals_visible_positive": bool(
                np.array_equal(anti_shadow_negative_graph, anti_positive_graph)
            ),
        },
    }

    summary["theorem"] = {
        "the_centered_spread_features_form_the_exact_etf_36_15": (
            summary["target_side_frame_geometry"]["spread_etf"]
            == {
                "frame_type": "ETF(36,15)",
                "vector_count": 36,
                "sector_dimension": 15,
                "column_norm_squared": "15/2",
                "off_diagonal_inner_products": ["-3/2", "3/2"],
                "normalized_coherence": "1/5",
                "welch_bound_squared": "1/25",
                "frame_operator_spectrum": {"0": 21, "18": 15},
                "positive_sign_graph": {
                    "vertices": 36,
                    "degree": 15,
                    "lambda": 6,
                    "mu": 6,
                    "edge_count": 270,
                    "spectrum": {"-3": 20, "3": 15, "15": 1},
                },
                "negative_sign_graph": {
                    "vertices": 36,
                    "degree": 20,
                    "lambda": 10,
                    "mu": 12,
                    "edge_count": 360,
                    "spectrum": {"-4": 15, "2": 20, "20": 1},
                },
                "positive_sign_equals_overlap_4_graph": True,
                "negative_sign_equals_overlap_1_graph": True,
            }
        ),
        "the_anti_line_channel_collapses_to_a_doubled_45_vector_transport_frame_in_the_24_sector": (
            summary["target_side_frame_geometry"]["anti_line_quotient"]
            == {
                "frame_type": "doubled two-distance tight frame(45,24)",
                "anti_line_count": 90,
                "duplicate_class_count": 45,
                "duplicate_multiplicity": 2,
                "duplicate_pairs_are_disjoint": True,
                "sector_dimension": 24,
                "column_norm_squared": "48/5",
                "off_diagonal_inner_products": ["-12/5", "3/5"],
                "frame_operator_spectrum": {"0": 21, "18": 24},
                "positive_sign_graph": {
                    "vertices": 45,
                    "degree": 32,
                    "lambda": 22,
                    "mu": 24,
                    "edge_count": 720,
                    "spectrum": {"-4": 20, "2": 24, "32": 1},
                },
                "negative_sign_graph": {
                    "vertices": 45,
                    "degree": 12,
                    "lambda": 3,
                    "mu": 3,
                    "edge_count": 270,
                    "spectrum": {"-3": 24, "3": 20, "12": 1},
                },
                "positive_sign_isomorphic_to_transport_graph": True,
                "canonical_transport_carrier": {
                    "coordinate_conversion": "(x0,x1,x2,x3) -> (x0,x2,x1,x3)",
                    "anti_lines_equal_center_quads_after_coordinate_conversion": True,
                    "duplicate_pairing_equals_center_quad_antipodes": True,
                    "duplicate_classes_equal_quotient_point_quad_pairs": True,
                    "paired_supports_equal_quotient_point_supports": True,
                    "quotient_line_count": 27,
                    "support_partitions_equal_quotient_lines": True,
                    "line_size_distribution": {5: 27},
                    "point_line_incidence_distribution": {3: 45},
                    "negative_sign_graph_five_cliques_equal_quotient_lines": True,
                    "positive_sign_equals_transport_graph_without_relabeling": True,
                    "negative_sign_equals_quotient_point_graph_without_relabeling": True,
                },
            }
        ),
        "the_anti_line_transport_target_is_the_existing_center_quad_quotient_carrier": (
            summary["target_side_frame_geometry"]["anti_line_quotient"]["canonical_transport_carrier"]
            == {
                "coordinate_conversion": "(x0,x1,x2,x3) -> (x0,x2,x1,x3)",
                "anti_lines_equal_center_quads_after_coordinate_conversion": True,
                "duplicate_pairing_equals_center_quad_antipodes": True,
                "duplicate_classes_equal_quotient_point_quad_pairs": True,
                "paired_supports_equal_quotient_point_supports": True,
                "quotient_line_count": 27,
                "support_partitions_equal_quotient_lines": True,
                "line_size_distribution": {5: 27},
                "point_line_incidence_distribution": {3: 45},
                "negative_sign_graph_five_cliques_equal_quotient_lines": True,
                "positive_sign_equals_transport_graph_without_relabeling": True,
                "negative_sign_equals_quotient_point_graph_without_relabeling": True,
            }
        ),
        "the_anti_line_transport_target_recovers_the_full_27_line_dual_gq_4_2_incidence": (
            summary["target_side_frame_geometry"]["anti_line_quotient"]["canonical_transport_carrier"]
            == {
                "coordinate_conversion": "(x0,x1,x2,x3) -> (x0,x2,x1,x3)",
                "anti_lines_equal_center_quads_after_coordinate_conversion": True,
                "duplicate_pairing_equals_center_quad_antipodes": True,
                "duplicate_classes_equal_quotient_point_quad_pairs": True,
                "paired_supports_equal_quotient_point_supports": True,
                "quotient_line_count": 27,
                "support_partitions_equal_quotient_lines": True,
                "line_size_distribution": {5: 27},
                "point_line_incidence_distribution": {3: 45},
                "negative_sign_graph_five_cliques_equal_quotient_lines": True,
                "positive_sign_equals_transport_graph_without_relabeling": True,
                "negative_sign_equals_quotient_point_graph_without_relabeling": True,
            }
        ),
        "the_full_dual_gq_4_2_incidence_is_already_recoverable_from_the_negative_sign_graph_five_cliques": (
            summary["target_side_frame_geometry"]["anti_line_quotient"]["canonical_transport_carrier"]
            == {
                "coordinate_conversion": "(x0,x1,x2,x3) -> (x0,x2,x1,x3)",
                "anti_lines_equal_center_quads_after_coordinate_conversion": True,
                "duplicate_pairing_equals_center_quad_antipodes": True,
                "duplicate_classes_equal_quotient_point_quad_pairs": True,
                "paired_supports_equal_quotient_point_supports": True,
                "quotient_line_count": 27,
                "support_partitions_equal_quotient_lines": True,
                "line_size_distribution": {5: 27},
                "point_line_incidence_distribution": {3: 45},
                "negative_sign_graph_five_cliques_equal_quotient_lines": True,
                "positive_sign_equals_transport_graph_without_relabeling": True,
                "negative_sign_equals_quotient_point_graph_without_relabeling": True,
            }
        ),
        "both_target_systems_share_the_same_hidden_naimark_shadow_split_21_equals_1_plus_20": (
            summary["common_naimark_shadow"]
            == {
                "shared_shadow_dimension": 21,
                "shared_shadow_split": "1 + 20",
                "shared_shadow_arithmetic": {
                    "21_equals_q_phi6": "3 * 7",
                    "20_equals_edge_count_over_degree": "240 / 12",
                },
                "spread_shadow": {
                    "frame_type": "ETF(36,21)",
                    "parseval_diagonal": "7/12",
                    "parseval_off_diagonal": ["-1/12", "1/12"],
                    "normalized_coherence": "1/7",
                    "positive_sign_graph": {
                        "vertices": 36,
                        "degree": 20,
                        "lambda": 10,
                        "mu": 12,
                        "edge_count": 360,
                        "spectrum": {"-4": 15, "2": 20, "20": 1},
                    },
                    "negative_sign_graph": {
                        "vertices": 36,
                        "degree": 15,
                        "lambda": 6,
                        "mu": 6,
                        "edge_count": 270,
                        "spectrum": {"-3": 20, "3": 15, "15": 1},
                    },
                },
                "anti_line_shadow": {
                    "frame_type": "two-distance shadow frame(45,21)",
                    "vector_count": 45,
                    "parseval_diagonal": "7/15",
                    "parseval_off_diagonal": ["-1/30", "2/15"],
                    "normalized_off_diagonal": ["-1/14", "2/7"],
                    "positive_sign_graph": {
                        "vertices": 45,
                        "degree": 12,
                        "lambda": 3,
                        "mu": 3,
                        "edge_count": 270,
                        "spectrum": {"-3": 24, "3": 20, "12": 1},
                    },
                    "negative_sign_graph": {
                        "vertices": 45,
                        "degree": 32,
                        "lambda": 22,
                        "mu": 24,
                        "edge_count": 720,
                        "spectrum": {"-4": 20, "2": 24, "32": 1},
                    },
                },
            }
        ),
        "naimark_complement_swaps_the_positive_and_negative_target_side_srg_signatures": all(
            summary["naimark_sign_duality"].values()
        ),
    }

    summary["interpretation"] = (
        "The Parseval measurement machine has a fully rigid target-side geometry. The spread channel is an "
        "exact ETF(36,15), the anti-line channel collapses to a doubled 45-vector two-distance tight frame "
        "on the same canonical center-quad / quotient-point carrier whose 27 support partitions recover the full "
        "dual GQ(4,2) incidence and are already visible as the 27 five-cliques of the negative sign graph, and "
        "whose positive sign graph is the 45-point transport graph. Both targets expose the same hidden Naimark "
        "shadow 21 = 1 + 20. Passing to the "
        "Naimark complement flips the sign graphs exactly, so the visible target geometries and their shadows "
        "are related by a finite sign-complement duality rather than by unrelated frame completions."
    )
    return summary


def write_summary(output_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    output_path.write_text(
        json.dumps(build_parseval_target_geometry_summary(), indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    output_path = write_summary()
    summary = build_parseval_target_geometry_summary()

    print("=" * 72)
    print("W33 PARSEVAL TARGET GEOMETRY AUDIT")
    print("=" * 72)
    print(f"wrote: {output_path}")
    for key, value in summary["theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()