"""Local tomotope incidence from the tetrahedral Fourier/Clifford packet.

The repo already records the tomotope local incidence law

    flags per edge = 2 * 4 * 2 = 16,
    total flags    = 12 * 16 = 192.

This bridge identifies those factors directly inside the live tetrahedral
packet:

    - 2 = source/target orientation on an undirected tetrahedral bridge;
    - 4 = the four chart vertices;
    - 2 = the positive/negative chirality classes from the local
          Fourier/Clifford frame split.

So the tomotope flag packet is not just numerically compatible with the local
tetrahedral atlas.  Its local edge-incidence law is exactly the oriented
tetrahedral bridge packet dressed by the Clifford chirality bit.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from exploration.w33_surface_neighborly_bridge import tomotope_flag_count_from_local_incidence
from exploration.w33_tetrahedral_chart_oscillator_bridge import build_summary as build_tetrahedral_summary
from exploration.w33_tetrahedral_fourier_clifford_bridge import build_summary as build_fourier_summary
from exploration.w33_tomotope_order_bridge import build_tomotope_order_summary


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_tomotope_local_incidence_clifford_bridge_summary.json"


def build_summary() -> dict[str, Any]:
    tetra = build_tetrahedral_summary()
    fourier = build_fourier_summary()
    tomotope = build_tomotope_order_summary()["tomotope"]

    chart_vertices = len(tetra["tetrahedral_chart_frame"]["chart_names"])
    undirected_bridges = tetra["edge_transition_packet"]["undirected_edge_count"]
    directed_bridges = tetra["edge_transition_packet"]["directed_edge_count"]
    chirality_classes = int(bool(fourier["chirality_packet"]["positive_count"])) + int(
        bool(fourier["chirality_packet"]["negative_count"])
    )

    orientations_per_undirected_bridge = directed_bridges // undirected_bridges
    cells_from_chart_chirality = chart_vertices * chirality_classes
    local_flags_per_edge = (
        orientations_per_undirected_bridge * chart_vertices * chirality_classes
    )
    total_flags = directed_bridges * local_flags_per_edge

    summary: dict[str, Any] = {
        "tetrahedral_packet": {
            "chart_vertices": chart_vertices,
            "undirected_bridges": undirected_bridges,
            "directed_bridges": directed_bridges,
            "orientations_per_undirected_bridge": orientations_per_undirected_bridge,
        },
        "clifford_packet": {
            "positive_charts": fourier["chirality_packet"]["positive_charts"],
            "negative_charts": fourier["chirality_packet"]["negative_charts"],
            "chirality_class_count": chirality_classes,
        },
        "tomotope_packet": tomotope,
        "derived_local_incidence_packet": {
            "cells_from_chart_vertices_times_chirality_classes": cells_from_chart_chirality,
            "flags_per_edge_from_orientation_vertices_chirality": local_flags_per_edge,
            "total_flags_from_directed_edges_times_local_flags_per_edge": total_flags,
        },
        "tomotope_local_incidence_clifford_theorem": {
            "the_tomotope_edges_are_the_directed_tetrahedral_bridges": tomotope["edges"] == directed_bridges,
            "two_orientations_per_undirected_bridge_recover_the_directed_bridge_count": (
                orientations_per_undirected_bridge * undirected_bridges == directed_bridges
            ),
            "the_tomotope_cells_equal_chart_vertices_times_chirality_classes": (
                tomotope["tetrahedra"] + tomotope["hemioctahedra"] == cells_from_chart_chirality
            ),
            "the_tomotope_local_flags_per_edge_equal_two_times_four_times_two": (
                local_flags_per_edge == 16
            ),
            "the_tomotope_local_flags_per_edge_match_the_surface_neighborly_formula": (
                local_flags_per_edge * tomotope["edges"] == tomotope_flag_count_from_local_incidence()
            ),
            "the_total_tomotope_flag_count_equals_directed_bridges_times_local_flags_per_edge": (
                tomotope["flags"] == total_flags
            ),
        },
        "interpretation": (
            "The tomotope local edge-incidence law is exactly the tetrahedral "
            "Fourier/Clifford packet in disguise: 2 orientations on each undirected "
            "bridge, 4 chart vertices, and 2 chirality classes. That reproduces both "
            "the 8 tomotope cells and the 192 tomotope flags."
        ),
    }
    return summary


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["tomotope_local_incidence_clifford_theorem"], indent=2))


if __name__ == "__main__":
    main()
