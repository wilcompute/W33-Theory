#!/usr/bin/env python3
"""Colored incidence tensor between W(3,3) point-star defects and spreads.

The uncolored defect/spread graph is complete: every spread contains exactly one
line through every point.  The useful object is therefore the colored incidence
tensor

    T[point defect, spread frame] = unique carried line clock.

This script verifies that the tensor reconstructs the W(3,3) point graph on the
defect side and a 36-frame overlap scheme on the spread side.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import holonet_node as hn
import numpy as np
from w33_uor_runtime_model import ROOT, all_lines, find_spreads, point_id

DEFAULT_OUTPUT = ROOT / "data" / "w33_defect_spread_tensor.json"


def spectrum_counts(matrix: np.ndarray) -> dict[str, int]:
    values = np.linalg.eigvalsh(matrix)
    rounded = [round(float(value), 8) for value in values]
    return {f"{value:g}": rounded.count(value) for value in sorted(set(rounded))}


def point_line_memberships(lines: list[tuple[int, ...]]) -> list[set[int]]:
    memberships = [set() for _ in hn.POINTS]
    for line_idx, line in enumerate(lines):
        for point_idx in line:
            memberships[point_idx].add(line_idx)
    return memberships


def build_tensor(
    lines: list[tuple[int, ...]], spreads: list[list[int]]
) -> list[list[int]]:
    memberships = point_line_memberships(lines)
    tensor: list[list[int]] = []
    for point_idx in range(len(hn.POINTS)):
        row = []
        for spread in spreads:
            carried = memberships[point_idx] & set(spread)
            if len(carried) != 1:
                raise AssertionError(
                    f"point {point_idx} meets spread in {len(carried)} incident lines"
                )
            row.append(next(iter(carried)))
        tensor.append(row)
    return tensor


def row_label_equalities(tensor: list[list[int]]) -> tuple[np.ndarray, dict[str, int]]:
    row_count = len(tensor)
    reconstructed = np.zeros((row_count, row_count), dtype=int)
    hist: Counter[int] = Counter()
    for left in range(row_count):
        for right in range(left + 1, row_count):
            same = sum(
                1
                for col in range(len(tensor[left]))
                if tensor[left][col] == tensor[right][col]
            )
            hist[same] += 1
            if same == 9:
                reconstructed[left, right] = reconstructed[right, left] = 1
    return reconstructed, {str(key): hist[key] for key in sorted(hist)}


def spread_overlap_matrix(spreads: list[list[int]]) -> np.ndarray:
    count = len(spreads)
    matrix = np.zeros((count, count), dtype=int)
    spread_sets = [set(spread) for spread in spreads]
    for left in range(count):
        for right in range(left + 1, count):
            overlap = len(spread_sets[left] & spread_sets[right])
            matrix[left, right] = matrix[right, left] = overlap
    return matrix


def profile_shape_class_count(rows: list[dict[str, int]]) -> int:
    profiles = {tuple(sorted(row.values())) for row in rows}
    return len(profiles)


def build_report() -> dict[str, Any]:
    lines = all_lines()
    spreads = find_spreads(lines, limit=10000)
    tensor = build_tensor(lines, spreads)
    memberships = point_line_memberships(lines)
    row_graph, row_hist = row_label_equalities(tensor)
    spread_overlap = spread_overlap_matrix(spreads)
    high_overlap_graph = (spread_overlap == 4).astype(int)
    np.fill_diagonal(high_overlap_graph, 0)

    global_line_counts = Counter(label for row in tensor for label in row)
    row_profiles = [
        {str(line_idx): count for line_idx, count in sorted(Counter(row).items())}
        for row in tensor
    ]
    col_profiles = []
    for col_idx, spread in enumerate(spreads):
        col = [tensor[row_idx][col_idx] for row_idx in range(len(tensor))]
        col_profiles.append(
            {str(line_idx): count for line_idx, count in sorted(Counter(col).items())}
        )
        if set(col_profiles[-1]) != {str(line_idx) for line_idx in spread}:
            raise AssertionError("spread column profile does not match spread lines")

    row_degrees = [int(value) for value in row_graph.sum(axis=1)]
    high_overlap_degrees = [int(value) for value in high_overlap_graph.sum(axis=1)]
    weighted_spread_degrees = [int(value) for value in spread_overlap.sum(axis=1)]
    spread_overlap_hist = Counter(
        int(spread_overlap[left, right])
        for left in range(len(spreads))
        for right in range(left + 1, len(spreads))
    )

    theorem_checks = {
        "forty_defects": len(tensor) == 40,
        "thirty_six_spreads": len(spreads) == 36,
        "slot_count_is_1440": len(tensor) * len(spreads) == 1440,
        "each_point_row_has_four_labels_repeated_nine_times": all(
            sorted(Counter(row).values()) == [9, 9, 9, 9] for row in tensor
        ),
        "each_spread_column_has_ten_labels_repeated_four_times": all(
            sorted(
                Counter(
                    tensor[row_idx][col_idx] for row_idx in range(len(tensor))
                ).values()
            )
            == [4] * 10
            for col_idx in range(len(spreads))
        ),
        "each_line_label_occurs_thirty_six_times": set(global_line_counts.values())
        == {36},
        "row_equalities_reconstruct_w33_adjacency": row_hist == {"0": 540, "9": 240},
        "reconstructed_row_graph_degree_twelve": set(row_degrees) == {12},
        "reconstructed_row_graph_spectrum": spectrum_counts(row_graph)
        == {"-4": 15, "2": 24, "12": 1},
        "spread_intersection_scheme": {
            str(key): spread_overlap_hist[key] for key in sorted(spread_overlap_hist)
        }
        == {"1": 360, "4": 270},
        "four_overlap_graph_degree_fifteen": set(high_overlap_degrees) == {15},
        "four_overlap_graph_spectrum": spectrum_counts(high_overlap_graph)
        == {"-3": 20, "3": 15, "15": 1},
        "weighted_spread_overlap_degree_eighty": set(weighted_spread_degrees) == {80},
        "weighted_spread_overlap_spectrum": spectrum_counts(spread_overlap)
        == {"-10": 20, "8": 15, "80": 1},
        "single_defect_profile_shape_class": profile_shape_class_count(row_profiles)
        == 1,
        "single_spread_profile_shape_class": profile_shape_class_count(col_profiles)
        == 1,
    }

    return {
        "schema": "w33.defect_spread_tensor.v1",
        "status": "PASS" if all(theorem_checks.values()) else "FAIL",
        "counts": {
            "defects": len(tensor),
            "spreads": len(spreads),
            "slots": len(tensor) * len(spreads),
            "lines": len(lines),
        },
        "tensor_law": {
            "slot_definition": "T[point defect, spread frame] = unique incident line contained in that spread",
            "row_profile": "4 incident line labels, each repeated 9 times",
            "column_profile": "10 spread line labels, each repeated 4 times",
            "global_line_label_count": "each of the 40 line labels occurs 36 times",
            "sample_rows": [
                {
                    "point": point_id(hn.POINTS[row_idx]),
                    "line_label_counts": row_profiles[row_idx],
                }
                for row_idx in range(3)
            ],
            "sample_columns": [
                {
                    "spread": col_idx,
                    "line_label_counts": col_profiles[col_idx],
                }
                for col_idx in range(3)
            ],
        },
        "defect_side": {
            "row_same_label_pair_histogram": row_hist,
            "reconstructed_graph": "same label in 9 spread frames",
            "degree_histogram": {
                str(value): row_degrees.count(value)
                for value in sorted(set(row_degrees))
            },
            "spectrum": spectrum_counts(row_graph),
            "reading": (
                "Two point-star defects share a carried line in 9 spread frames exactly when the points are "
                "collinear in W(3,3), and in 0 frames otherwise. The colored tensor reconstructs the original "
                "SRG(40,12,2,4) defect graph."
            ),
        },
        "spread_side": {
            "line_intersection_pair_histogram": {
                str(key): spread_overlap_hist[key]
                for key in sorted(spread_overlap_hist)
            },
            "four_line_overlap_graph_degree_histogram": {
                str(value): high_overlap_degrees.count(value)
                for value in sorted(set(high_overlap_degrees))
            },
            "four_line_overlap_graph_spectrum": spectrum_counts(high_overlap_graph),
            "weighted_overlap_degree_histogram": {
                str(value): weighted_spread_degrees.count(value)
                for value in sorted(set(weighted_spread_degrees))
            },
            "weighted_overlap_spectrum": spectrum_counts(spread_overlap),
            "reading": (
                "Distinct spread frames overlap in either 1 or 4 line clocks. The 4-overlap relation is a "
                "15-regular 36-frame graph with spectrum {15, 3^15, -3^20}; the weighted overlap operator "
                "has spectrum {80, 8^15, -10^20}."
            ),
        },
        "profile_orbits": {
            "defect_profile_shape_classes": profile_shape_class_count(row_profiles),
            "spread_profile_shape_classes": profile_shape_class_count(col_profiles),
            "boundary": (
                "These are tensor-profile shape classes, not a GAP automorphism-group orbit computation. They show "
                "that the visible tensor multiplicity data is homogeneous on both sides, ignoring line-label names."
            ),
        },
        "theorem_checks": theorem_checks,
        "interpretation": (
            "The 40 contextual point-star defects and the 36 spread frames are tied by a 1440-slot colored bus. "
            "The bus is not just a count: its row equalities reconstruct W(3,3), while its columns carry a "
            "separate 36-frame overlap scheme. This is the missing dual scheduler object: defects are local "
            "overfull clocks, spreads are global now-frames, and the carried line label is the executable bus."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUTPUT), help="output JSON")
    args = parser.parse_args(argv)

    output = Path(args.out)
    if not output.is_absolute():
        output = ROOT / output
    report = build_report()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"status: {report['status']}")
    print(f"slots: {report['counts']['slots']}")
    print(f"defect spectrum: {report['defect_side']['spectrum']}")
    print(
        f"spread 4-overlap spectrum: {report['spread_side']['four_line_overlap_graph_spectrum']}"
    )
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
