#!/usr/bin/env python3
"""
BT840 - Clifford rook sentinel sheet completing the 57-cell flag count.

BT837 supplies 3240 W33 Petersen-home flags:

    36 schedules * 6 A5 cores per schedule * 15 Petersen edges = 3240.

BT839 noticed that the 57-cell full flag count needs exactly

    3420 - 3240 = 180 = k*g.

This verifier identifies that 180 as an actual object from the previously
verified Clifford L/R boundary: the zero-overlap graph on the 36 L/R cells is
the 6 x 6 rook graph.  Its 180 edges decompose as

    12 row/column fibers * C(6,2) duads = k*g.

Each fiber is a six-object carrier, and each fiber's 15 duads are the same
K6/hemi-icosahedral edge count that appears in the 11-cell cell.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_clifford_lr_spread_scheme_boundary import clifford_lr_scheme_report  # noqa: E402


def psl2_order(p: int) -> int:
    return p * (p * p - 1) // 2


def rook_cells() -> list[tuple[int, int]]:
    return [(row, col) for row in range(6) for col in range(6)]


def rook_fibers() -> dict[str, list[tuple[int, int]]]:
    fibers: dict[str, list[tuple[int, int]]] = {}
    for row in range(6):
        fibers[f"L{row}"] = [(row, col) for col in range(6)]
    for col in range(6):
        fibers[f"R{col}"] = [(row, col) for row in range(6)]
    return fibers


def sentinel_edges() -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for fiber_label, members in rook_fibers().items():
        for left, right in combinations(members, 2):
            edges.append(
                {
                    "fiber": fiber_label,
                    "duad": [list(left), list(right)],
                }
            )
    return edges


def main() -> None:
    k, g = 12, 15
    bt837 = json.loads((ROOT / "data" / "bt837_schedule_library_geometry.json").read_text())
    lr_report = clifford_lr_scheme_report()

    cells = rook_cells()
    fibers = rook_fibers()
    edges = sentinel_edges()
    edge_keys = {
        tuple(sorted(tuple(cell) for cell in row["duad"]))
        for row in edges
    }
    degree = Counter()
    fiber_edge_profile = Counter()
    row_column_split = Counter(row["fiber"][0] for row in edges)
    for row in edges:
        fiber_edge_profile[row["fiber"]] += 1
        a, b = (tuple(item) for item in row["duad"])
        degree[a] += 1
        degree[b] += 1

    w33_petersen_flags = int(bt837["t3"]["total_flags"])
    completed_57_flags = w33_petersen_flags + len(edges)
    petersen_cores = w33_petersen_flags // g
    completed_cores = completed_57_flags // g

    checks = {
        "rook_has_36_cells": len(cells) == 36,
        "twelve_row_column_fibers": len(fibers) == k == 12,
        "each_fiber_has_six_cells": Counter(len(members) for members in fibers.values()) == {6: 12},
        "each_fiber_has_fifteen_duads": Counter(fiber_edge_profile.values()) == {15: 12},
        "sentinel_sheet_has_180_edges": len(edges) == len(edge_keys) == k * g == 180,
        "rook_degree_is_ten": Counter(degree.values()) == {10: 36},
        "row_column_split_is_90_90": row_column_split == {"L": 90, "R": 90},
        "matches_clifford_zero_overlap_edge_count": lr_report["overlap_0_graph"]["edge_count"] == 180,
        "matches_clifford_zero_overlap_profile": lr_report["vertex_overlap_profile"] == {"0": 180, "4": 450},
        "bt837_petersen_flags_are_3240": w33_petersen_flags == 3240,
        "petersen_home_cores_are_216": petersen_cores == 216,
        "sentinel_sheet_is_twelve_extra_petersen_duad_fibers": completed_cores == petersen_cores + k == 228,
        "completed_count_is_57_cell_flags": completed_57_flags == psl2_order(19) == 3420,
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT840 check failed: {name}")

    out = {
        "theorem": "BT840 Clifford rook sentinel sheet",
        "sentinel_sheet": {
            "source": "Clifford L/R zero-overlap rook graph",
            "cells": len(cells),
            "fibers": len(fibers),
            "fiber_labels": sorted(fibers),
            "duads_per_fiber": dict(sorted(Counter(fiber_edge_profile.values()).items())),
            "edge_count": len(edges),
            "factorization": "180 = 12*C(6,2) = k*g",
            "row_column_split": dict(sorted(row_column_split.items())),
            "sample_edges": edges[:12],
        },
        "gc_completion": {
            "w33_petersen_home_flags": w33_petersen_flags,
            "sentinel_edges": len(edges),
            "completed_flags": completed_57_flags,
            "psl2_19_order": psl2_order(19),
            "core_count_reading": {
                "w33_cores": petersen_cores,
                "sentinel_fibers": k,
                "completed_cores": completed_cores,
                "edge_or_duad_count_per_core": g,
            },
        },
        "hexagon_11cell_hint": {
            "six_object_fiber": "each rook row/column is a six-object carrier",
            "duads": "C(6,2)=15 is the hemi-icosahedral K6 edge count of the 11-cell cell",
            "boundary": "this supplies the missing k*g sheet; it does not assert PSL(2,19) acts on the W33 carrier",
        },
        "checks": checks,
    }
    path = ROOT / "data" / "bt840_clifford_rook_sentinel_sheet.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
