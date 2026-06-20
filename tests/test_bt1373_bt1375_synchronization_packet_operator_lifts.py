#!/usr/bin/env python3
"""Regression tests for BT1373-BT1375."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(relpath: str) -> None:
    subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, check=True)


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def test_bt1373_improved_s3_synchronization() -> None:
    run_script("analysis/bt1373_s3_gauge_synchronization_improved_counterconnection.py")
    data = load_json(
        "data/bt1373_s3_gauge_synchronization_improved_counterconnection.json"
    )
    assert data["verified"] is True
    assert data["spanning_tree_baseline"]["nonidentity_corrections"] == 380
    assert data["improved_synchronization_gauge"]["nonidentity_corrections"] == 330
    assert data["improved_synchronization_gauge"]["identity_edges"] == 210
    assert data["improved_synchronization_gauge"]["best_single_line_delta"] == -5
    assert data["improved_synchronization_gauge"]["residual_order_profile"] == {
        "1": 210,
        "2": 240,
        "3": 90,
    }


def test_bt1374_packet_route_lowers_to_q6_edges() -> None:
    run_script("analysis/bt1374_q6_tomotope_packet_route_compiler.py")
    data = load_json("data/bt1374_q6_tomotope_packet_route_compiler.json")
    assert data["verified"] is True
    stress = next(
        program
        for program in data["compiled_programs"]
        if program["program"] == "six_digit_stress"
    )
    assert stress["level"] == 6
    assert stress["route_bound"] == 48
    assert len(set(stress["q6_edge_indices"])) == 6
    for program in data["compiled_programs"]:
        for row in program["packet_rows"]:
            assert row["tomotope_flag"] == 4 * row["tomotope_block"] + (
                row["mirror_slot"] % 4
            )
            assert len(row["q6_endpoint_a"]) == 6
            assert len(row["q6_endpoint_b"]) == 6
    assert data["atlas_ingress_summary"]["distinct_tomotope_flags"] == 6
    assert data["atlas_ingress_summary"]["routes"] == 540


def test_bt1375_steinberg_operator_scheduler() -> None:
    run_script("analysis/bt1375_steinberg_cycle_operator_scheduler_lift.py")
    data = load_json("data/bt1375_steinberg_cycle_operator_scheduler_lift.json")
    assert data["verified"] is True
    assert data["chain_complex"]["rank_gains_mod_boundaries"] == [27, 27, 27]
    assert data["central_operator"]["cycle_length_profile"] == {"3": 27}
    assert data["central_operator"]["nilpotent_rank_profile"] == [54, 27, 0]
    assert data["central_operator"]["kernel_dimensions"] == [27, 54, 81]
    assert (
        data["scheduler_alignment"]["matter_state_factorization"]
        == "27 = 3 BT865 free copies * 9 central cosets"
    )
    assert data["scheduler_alignment"]["three_epoch_uniform_count_per_basis"] == 80


def test_bt1373_bt1375_docs_index_card_present() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert (
        "BT1373&ndash;BT1375: synchronization, packet route, and operator scheduler lifts"
        in text
    )
    assert "BT1373_BT1375_synchronization_packet_operator_lifts.md" in text
    assert "330" in text
    assert "rank(Z-I), rank((Z-I)<sup>2</sup>), rank((Z-I)<sup>3</sup>)" in text


if __name__ == "__main__":
    test_bt1373_improved_s3_synchronization()
    test_bt1374_packet_route_lowers_to_q6_edges()
    test_bt1375_steinberg_operator_scheduler()
    test_bt1373_bt1375_docs_index_card_present()
    print("BT1373-BT1375 focused tests passed")
