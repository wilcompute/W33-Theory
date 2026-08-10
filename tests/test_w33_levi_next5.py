"""Regression tests for rank, trade, E8, fault-stack, and runtime G-set closures."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis"))

import w33_levi_next5 as next5  # noqa: E402
import holonet_typed_fault_stack as stack  # noqa: E402
import holonet_cmd  # noqa: E402
import bt1880_bt982_to_bt1875_mapper as mapper  # noqa: E402


def result() -> dict:
    return next5.analyze()


def test_all_five_tracks_pass() -> None:
    data = result()
    assert data["status"] == "PASS"
    assert data["checks"] == {"all_five_present": True, "all_five_pass": True}


def test_odd_q_rank_theorem_closed() -> None:
    track = result()["tracks"]["1_odd_q_rank_theorem"]
    assert track["status"] == "PROVED"
    assert track["formulas"]["rank_M"] == "(q(q+1)^2+2)/2"
    assert track["formulas"]["rank_A_point"] == "q(q^2+1)/2+1"
    assert track["formulas"]["rank_A_line"] == "q^2+1"
    assert track["formulas"]["J2_blocks"] == 0


def test_pass158_trade_module_is_one_plus_u14minus() -> None:
    track = result()["tracks"]["2_pass158_trade_bridge"]
    assert track["status"] == "PROVED"
    assert track["fixed_line_coordinate_mask"] == "0x7fff"
    assert track["quotient"]["dimension"] == 14
    assert track["quotient"]["image_order"] == 25920
    assert track["intertwiner"]["solution_space_dimension"] == 1
    assert track["intertwiner"]["rank"] == 14


def test_integral_e8_intertwiner() -> None:
    track = result()["tracks"]["3_integral_E8_intertwiner"]
    assert track["status"] == "PROVED"
    assert track["control_smith_invariants"] == [1] * 8
    assert track["checks"]["control_maps_to_payload"]
    assert track["checks"]["exact_intertwining"]
    assert track["checks"]["raw_incidence_matches_projected_mod2"]
    assert track["checks"]["payload_gram_is_E8"]


def test_adversarial_fault_census() -> None:
    data = stack.TypedFaultStack().adversarial_census(seed=7, trials_per_fault=24)
    assert data["all_pass"]
    assert data["outcomes"]["clean/accepted"] == 24
    assert data["outcomes"]["authenticated_type_confusion/rejected"] == 24
    assert data["outcomes"]["route_failure/retry"] == 24


def test_retry_load_is_bounded() -> None:
    data = stack.TypedFaultStack().retry_load(seed=11, packets_per_class=32)
    assert data["all_pass"]
    assert data["observed_mean_attempts"] < 1.6


def test_fault_stack_cli_dispatch() -> None:
    with pytest.raises(SystemExit) as exc:
        holonet_cmd.main(["packet-fault-stack"])
    assert exc.value.code == 0


def test_fault_stack_cli_rejects_arguments() -> None:
    with pytest.raises(SystemExit):
        holonet_cmd.main(["packet-fault-stack", "extra"])


def test_explicit_runtime_gsets() -> None:
    track = result()["tracks"]["5_explicit_runtime_G_sets"]
    assert track["status"] == "PROVED"
    assert track["sets"]["X48"]["size"] == 48
    assert track["sets"]["X192_tomotope_flags"]["orbits"] == [96, 96]
    assert track["sets"]["X2160_mirror_bus"]["D12_orbits"] == 180
    assert track["sets"]["X51840_runtime"]["G48_orbits"] == 1080
    assert all(track["checks"].values())


def test_bt982_basis_is_materialized() -> None:
    data = json.loads((ROOT / "data/bt982_explicit_integral_e8_basis.json").read_text(encoding="utf-8"))
    assert data["det_B"] == 1
    assert data["matches_standard_e8_cartan"] is True
    assert len(data["final_integral_basis_B"]) == 8


def test_mapper_uses_materialized_basis_and_closed_controls() -> None:
    summary = mapper.theorem_summary()
    assert summary["all_pass"]
    assert summary["materialized_bt982_json_present"] is True
    assert all(row["status"] == "canonical_chain_control_crosswalk_closed" for row in mapper.mapped_rows())


def test_certificate_matches_recomputation() -> None:
    certificate = json.loads((ROOT / "data/PART_2026_07_10_LEVI_NEXT5_results.json").read_text(encoding="utf-8"))
    assert certificate["status"] == result()["status"] == "PASS"
