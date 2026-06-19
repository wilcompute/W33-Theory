#!/usr/bin/env python3
"""Focused regression for BT1316-BT1319 toroidal heptad/Q4 bridge."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(relpath: str) -> None:
    subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, check=True)


def load_json(relpath: str) -> dict:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def test_bt1316_toroidal_authoritative_data_lock() -> None:
    run_script("analysis/bt1316_toroidal_authoritative_data_lock.py")
    data = load_json("data/bt1316_toroidal_authoritative_data_lock.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["authoritative_values"]["csaszar"] == {
        "vertices": 7,
        "edges": 21,
        "faces": 14,
        "genus": 1,
    }
    assert data["authoritative_values"]["szilassi"] == {
        "vertices": 14,
        "edges": 21,
        "faces": 7,
        "genus": 1,
    }
    assert data["raw"]["family_counts"] == {"Csaszar": 5, "Szilassi": 2}


def test_bt1317_toroidal_tomotope_pipeline_consolidator() -> None:
    run_script("analysis/bt1317_toroidal_tomotope_pipeline_consolidator.py")
    data = load_json("data/bt1317_toroidal_tomotope_pipeline_consolidator.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    chain = data["pipeline_chain"]
    assert chain["raw_heptad"] == 7
    assert chain["active_packet_weight"] == 168
    assert chain["tomotope_weight"] == 192
    assert chain["oriented_transports"] == 42
    assert chain["weighted_active_transport"] == 168
    assert chain["nontrivial_second_moment"] == "21/16"
    assert chain["moment_ladder"] == {
        "times_16": 21,
        "times_2": 42,
        "times_stabilizer_4": 168,
    }


def test_bt1318_toroidal_c2_axis_assignment() -> None:
    run_script("analysis/bt1318_toroidal_c2_axis_assignment.py")
    data = load_json("data/bt1318_toroidal_c2_axis_assignment.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["csaszar_abstract_automorphism_group"]["order"] == 42
    assert data["csaszar_abstract_automorphism_group"]["order_profile"] == {
        "1": 1,
        "2": 7,
        "3": 14,
        "6": 14,
        "7": 6,
    }
    assert data["metric_axis_records"]["csaszar_axis_perm"] == [1, 0, 3, 2, 5, 4, 6]
    assert data["metric_axis_records"]["szilassi_face_axis_perm"] == [
        2,
        5,
        0,
        6,
        4,
        1,
        3,
    ]
    assert (
        data["axis_assignment"]["realization_to_involution_bijection_status"]
        == "not_proved_current_labels"
    )


def test_bt1319_toroidal_q4_hypercube_holonet_bridge() -> None:
    run_script("analysis/bt1319_toroidal_q4_hypercube_holonet_bridge.py")
    data = load_json("data/bt1319_toroidal_q4_hypercube_holonet_bridge.json")
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["four_by_four_square"]["ordinary_knight_edges"] == 24
    assert data["four_by_four_square"]["ordinary_degree_profile"] == {
        "2": 4,
        "3": 8,
        "4": 4,
    }
    assert data["q4_packet"]["dimension_edge_counts"] == {
        "0": 8,
        "1": 8,
        "2": 8,
        "3": 8,
    }
    assert data["tomotope_codec"]["reading"] == "(2+7+7)*12 = 16*12 = 192"
    assert (
        data["tetrahedral_clifford_scale_marker"]["evaluated_at_Phi_4"]
        == data["tetrahedral_clifford_scale_marker"]["expected_11_to_4"]
        == data["tetrahedral_clifford_scale_marker"]["p_Ih_power_mu"]
        == 14641
    )
    assert data["holonet_interface"]["local_ecube_max_hops"] == 4
    assert data["holonet_interface"]["slot_factorization"] == "540*4 = 2160"
    assert data["protected_router_lift"]["parameters"] == {
        "length": 8,
        "dimension": 4,
        "distance": 4,
        "codewords": 16,
    }


if __name__ == "__main__":
    test_bt1316_toroidal_authoritative_data_lock()
    test_bt1317_toroidal_tomotope_pipeline_consolidator()
    test_bt1318_toroidal_c2_axis_assignment()
    test_bt1319_toroidal_q4_hypercube_holonet_bridge()
    print("BT1316-BT1319 toroidal heptad/Q4 bridge tests passed")
