#!/usr/bin/env python3
"""Regression tests for BT1320-BT1325 hypercube tower and holonet bridges."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(relpath: str) -> None:
    subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, check=True)


def load_json(relpath: str) -> dict:
    import json
    with (ROOT / relpath).open(encoding="utf-8") as fh:
        return json.load(fh)


def test_bt1320_q5_holonet_bridge() -> None:
    run_script("analysis/bt1320_q5_holonet_bridge.py")
    data = load_json("data/bt1320_q5_holonet_bridge.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["q5"]["vertices"] == 32
    assert data["q5"]["edges"] == 80
    assert data["q5"]["diameter"] == 5
    assert data["q5"]["q4_subcubes"] == 10
    assert data["rm14_code"]["distance"] == 8
    assert data["rm14_code"]["codewords"] == 32


def test_bt1321_q6_holonet_bridge() -> None:
    run_script("analysis/bt1321_q6_holonet_bridge.py")
    data = load_json("data/bt1321_q6_holonet_bridge.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["q6"]["vertices"] == 64
    assert data["q6"]["edges"] == 192
    assert data["tomotope_flag_identity"]["q6_edges"] == 192
    assert data["rm15_code"]["distance"] == 16


def test_bt1322_inter_quadrant_routing() -> None:
    run_script("analysis/bt1322_inter_quadrant_routing_protocol.py")
    data = load_json("data/bt1322_inter_quadrant_routing_protocol.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["error_protection"]["distance_doubles_each_layer"] is True
    assert data["d12_mirror_bus_interface"]["transversals_per_chart"] == 4
    assert data["d12_mirror_bus_interface"]["total_mirror_slots"] == 2160


def test_bt1323_physical_realizability() -> None:
    run_script("analysis/bt1323_toroidal_heptad_physical_realizability.py")
    data = load_json("data/bt1323_toroidal_heptad_physical_realizability.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["heptad_geometry"]["csaszar"]["V"] == 7
    assert data["heptad_geometry"]["csaszar"]["E"] == 21
    assert data["optical_parameters"]["csaszar_total_insertion_loss_dB"] == 2.1
    assert data["q4_router"]["degree"] == 4


def test_bt1324_holonet_simulation() -> None:
    run_script("analysis/bt1324_holonet_simulation.py")
    data = load_json("data/bt1324_holonet_simulation.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["routing_efficiency"]["gray_code"]["unique_states"] == 16
    assert data["latency_budget"]["total_latency_ns"] == 15.0
    assert data["simulation_parameters"]["random_seed"] == 33


def test_bt1325_tower_summary() -> None:
    run_script("analysis/bt1325_hypercube_tower_summary.py")
    data = load_json("data/bt1325_hypercube_tower_summary.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["tower_invariants"]["q6_edge_tomotope_identity"]["identity_holds"] is True
    assert data["tower_invariants"]["code_distance_doubles_each_layer"] is True
    assert len(data["open_problems"]) == 4
    assert data["heptad_carrier"]["realizations"] == 7
    assert data["bt_packet_range"] == "BT1316-BT1325"


if __name__ == "__main__":
    test_bt1320_q5_holonet_bridge()
    test_bt1321_q6_holonet_bridge()
    test_bt1322_inter_quadrant_routing()
    test_bt1323_physical_realizability()
    test_bt1324_holonet_simulation()
    test_bt1325_tower_summary()
    print("BT1320-BT1325 hypercube tower tests passed")
