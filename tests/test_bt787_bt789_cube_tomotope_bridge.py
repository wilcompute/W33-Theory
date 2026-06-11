#!/usr/bin/env python3
"""Focused direct tests for BT787-BT789 cube/tomotope bridge packets."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run_script(relpath):
    subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, check=True)


def load_json(relpath):
    with (ROOT / relpath).open() as f:
        return json.load(f)


def test_bt787_r11_is_handle_octet():
    run_script("analysis/bt787_rank4_incidence_r11_handle.py")
    data = load_json("data/bt787_rank4_incidence_r11_handle.json")
    assert data["size8_orbits"] == [9, 10, 11]
    assert data["rank4_revision"]["faces"]["orbits"] == [9, 10]
    assert data["rank4_revision"]["cell_or_handle_octet"]["orbits"] == [11]
    assert data["quotient_paths"]["R11_to_live_edge_R12"] == [11, 13, 8, 12]


def test_bt788_480_compresses_to_ten_packets():
    run_script("analysis/bt788_action_480_orbit_compression.py")
    data = load_json("data/bt788_action_480_orbit_compression.json")
    expected_profile = {"8": 2, "16": 2, "24": 8, "48": 5}
    assert data["five_derivations"]["directed_edges_2E"]["micro_orbit_profile"] == expected_profile
    assert data["five_derivations"]["oriented_triangles_3T"]["micro_orbit_profile"] == expected_profile
    assert len(data["five_derivations"]["directed_edges_2E"]["compressed_48_packets"]) == 10
    assert len(data["five_derivations"]["oriented_triangles_3T"]["compressed_48_packets"]) == 10


def test_bt789_toroidal_genus_module_bridge():
    run_script("analysis/bt789_toroidal_genus_phase_bridge.py")
    data = load_json("data/bt789_toroidal_genus_phase_bridge.json")
    assert data["toroidal_genus_bridge"]["mod12_integral_residues"] == [0, 3, 4, 7]
    assert data["module_repair"]["cube"]["decomposition"] == "1 + 2 over F2"
    assert data["module_repair"]["tomotope"]["decomposition"] == "2 + 2 over F2"
    assert data["gap_witness"]["isomorphic"] == "false"


def test_bt798_residual_tetrahedral_carrier():
    run_script("analysis/bt798_residual_tetrahedral_carrier.py")
    data = load_json("data/bt798_residual_tetrahedral_carrier.json")
    assert data["residual_edge_micro_orbits"] == [1, 2, 13, 14]
    assert data["residual_triangle_micro_orbits"] == [1, 2, 3, 4]
    assert len(data["component_rows"]) == 4
    assert len(data["common_transversal_lines"]) == 4
    assert [row["points"] for row in data["common_transversal_lines"]] == [
        [0, 13, 14, 15],
        [1, 4, 7, 10],
        [2, 31, 35, 39],
        [3, 22, 27, 29],
    ]
    assert all(row["directed_edge_count"] == 12 for row in data["component_rows"])
    assert all(row["triangle_corner_count"] == 12 for row in data["component_rows"])


def test_bt799_transversal_incidence_grammar():
    run_script("analysis/bt799_transversal_incidence_grammar.py")
    data = load_json("data/bt799_transversal_incidence_grammar.json")
    assert data["orbit_grammar"]["R11"]["profile"] == {
        "((0, 0), (0, 0), (0, 0), (1, 1))": 8
    }
    assert data["orbit_grammar"]["R12"]["profile"] == {
        "((1, 0), (1, 0), (1, 0), (1, 0))": 12
    }
    assert data["orbit_grammar"]["R13"]["profile"] == {
        "((0, 0), (0, 0), (0, 0), (0, 0))": 12
    }


def test_bt800_diagonal_quotient_shadow_plane():
    run_script("analysis/bt800_diagonal_quotient_shadow_plane.py")
    data = load_json("data/bt800_diagonal_quotient_shadow_plane.json")
    assert all(row["xor"] == [1, 1, 1] for row in data["quotient_rows"])
    assert len(data["quotient_rows"]) == 4
    assert data["shadow_plane"]["collinearity_structure"] == "K4,4 across the two noncollinearity K4 sheets"
    assert len(data["shadow_plane"]["noncollinearity_components"]) == 2


def test_bt801_global_transversal_repair_atlas():
    run_script("analysis/bt801_global_transversal_repair_atlas.py")
    data = load_json("data/bt801_global_transversal_repair_atlas.json")
    assert data["chart_count"] == 540
    assert data["global_chart_transversal_slots"] == 2160
    assert data["transversal_slot_count_per_line_profile"] == {"54": 40}
    assert data["checks"]["all_shadow_splits_are_4_4"]


if __name__ == "__main__":
    test_bt787_r11_is_handle_octet()
    test_bt788_480_compresses_to_ten_packets()
    test_bt789_toroidal_genus_module_bridge()
    test_bt798_residual_tetrahedral_carrier()
    test_bt799_transversal_incidence_grammar()
    test_bt800_diagonal_quotient_shadow_plane()
    test_bt801_global_transversal_repair_atlas()
    print("BT787-BT801 focused tests passed")
