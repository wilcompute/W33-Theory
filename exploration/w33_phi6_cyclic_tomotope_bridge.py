"""Phi6 cyclic arithmetic bridge to the toroidal/tomotope packet.

This module compresses four exact packets that had previously appeared in
separate files:

1. The toroidal genus law at n = 7 gives the exact numerator 12.
2. The seven toroidal realizations span a 7D operator heptad with a centered
   6D shell.
3. The tetrahedral atlas has 6 undirected bridges and 12 directed bridges.
4. The tomotope has f-vector (4,12,16,8) and flag count 192.

The user's 1/7 hint turns out to fit this packet exactly.  In base 10, 1/7 has
repetend length 6 with cyclic word 142857.  So the decimal cyclicity of 7 sees
the same 6/12 packet as the toroidal/tetrahedral geometry:

    ord_7(10) = 6,
    2 * ord_7(10) = 12.

This does not prove that base-10 arithmetic is fundamental physics.  It does
show that the repo's live heptad packet already has an exact arithmetic shadow:
the centered shell is 6, its oriented lift is 12, and those are precisely the
repetend length and oriented double coming from 1/7.
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

from exploration.w33_tetrahedral_chart_oscillator_bridge import build_summary as build_tetrahedral_summary
from exploration.w33_toroidal_genus_fourier_bridge import build_summary as build_genus_summary
from exploration.w33_toroidal_heptad_projector_bridge import build_summary as build_heptad_summary
from exploration.w33_tomotope_order_bridge import build_tomotope_order_summary


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_phi6_cyclic_tomotope_bridge_summary.json"


def decimal_repetend(numerator: int, denominator: int) -> tuple[str, int]:
    remainder = numerator % denominator
    seen: dict[int, int] = {}
    digits: list[str] = []
    index = 0

    while remainder and remainder not in seen:
        seen[remainder] = index
        remainder *= 10
        digits.append(str(remainder // denominator))
        remainder %= denominator
        index += 1

    if remainder == 0:
        return ("", 0)

    start = seen[remainder]
    repetend = "".join(digits[start:])
    return (repetend, len(repetend))


def build_summary() -> dict[str, Any]:
    tetra = build_tetrahedral_summary()
    genus = build_genus_summary()
    heptad = build_heptad_summary()
    tomotope = build_tomotope_order_summary()["tomotope"]

    repetend, repetend_length = decimal_repetend(1, 7)

    chart_vertices = len(tetra["tetrahedral_chart_frame"]["chart_names"])
    undirected_bridges = tetra["edge_transition_packet"]["undirected_edge_count"]
    directed_bridges = tetra["edge_transition_packet"]["directed_edge_count"]
    centered_shell = heptad["projector_heptad"]["centered_span_rank"]
    genus_numerator = genus["genus_dictionary"]["primal_numerator_at_phi6"]

    triangles_from_tetra_packet = chart_vertices + directed_bridges
    cells_from_tetra_packet = 2 * chart_vertices
    flags_from_edge_triangle_packet = directed_bridges * triangles_from_tetra_packet

    summary: dict[str, Any] = {
        "cyclic_packet": {
            "phi6": 7,
            "decimal_repetend_1_over_7": repetend,
            "decimal_repetend_length": repetend_length,
        },
        "geometric_packet": {
            "chart_vertices": chart_vertices,
            "undirected_bridges": undirected_bridges,
            "directed_bridges": directed_bridges,
            "centered_heptad_shell": centered_shell,
            "toroidal_genus_numerator": genus_numerator,
        },
        "tomotope_packet": tomotope,
        "derived_tomotope_packet_from_tetra": {
            "vertices": chart_vertices,
            "edges": directed_bridges,
            "triangles": triangles_from_tetra_packet,
            "cells": cells_from_tetra_packet,
            "flags": flags_from_edge_triangle_packet,
        },
        "phi6_cyclic_tomotope_theorem": {
            "one_seventh_has_exact_cyclic_word_142857": repetend == "142857",
            "the_repetend_length_of_one_seventh_equals_the_centered_heptad_shell": (
                repetend_length == centered_shell
            ),
            "the_repetend_length_of_one_seventh_equals_the_undirected_tetrahedral_bridge_count": (
                repetend_length == undirected_bridges
            ),
            "the_oriented_double_of_the_repetend_length_equals_the_toroidal_genus_numerator": (
                2 * repetend_length == genus_numerator
            ),
            "the_oriented_double_of_the_repetend_length_equals_the_tomotope_edge_count": (
                2 * repetend_length == tomotope["edges"]
            ),
            "the_tomotope_edges_are_exactly_the_directed_tetrahedral_bridges": (
                tomotope["edges"] == directed_bridges
            ),
            "the_tomotope_triangle_count_is_vertices_plus_directed_bridges": (
                tomotope["triangles"] == triangles_from_tetra_packet
            ),
            "the_tomotope_cell_count_is_twice_the_chart_vertex_count": (
                tomotope["tetrahedra"] + tomotope["hemioctahedra"] == cells_from_tetra_packet
            ),
            "the_tomotope_flag_count_is_edge_count_times_triangle_count": (
                tomotope["flags"] == flags_from_edge_triangle_packet
            ),
        },
        "interpretation": (
            "The decimal cyclicity of 1/7 sees the same packet as the toroidal/tetrahedral "
            "geometry: length 6 for the centered shell, and oriented double 12 for the edge "
            "packet. The tomotope then appears as the natural oriented lift of that packet: "
            "(4,12,16,8) = (chart vertices, directed bridges, chart vertices plus directed "
            "bridges, twice chart vertices), with 192 = 12*16 flags."
        ),
    }
    return summary


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["phi6_cyclic_tomotope_theorem"], indent=2))


if __name__ == "__main__":
    main()
