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


if __name__ == "__main__":
    test_bt787_r11_is_handle_octet()
    test_bt788_480_compresses_to_ten_packets()
    test_bt789_toroidal_genus_module_bridge()
    print("BT787-BT789 focused tests passed")
