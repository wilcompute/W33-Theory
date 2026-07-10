"""Regression tests for the five Levi frontiers packet."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_levi_five_frontiers.py"
RESULT_PATH = ROOT / "data" / "PART_2026_07_10_LEVI_FIVE_FRONTIERS_results.json"

SPEC = importlib.util.spec_from_file_location("w33_levi_five_frontiers", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MOD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)


def fast_result() -> dict:
    return MOD.analyze([3, 5])


def committed_result() -> dict:
    return json.loads(RESULT_PATH.read_text(encoding="utf-8"))


def test_fast_packet_passes_all_five_tracks() -> None:
    result = fast_result()
    assert result["status"] == "PASS"
    assert len(result["tracks"]) == 5
    assert all(track["all_pass"] for track in result["tracks"].values())


def test_odd_q_jordan_law_at_q3_and_q5() -> None:
    orders = fast_result()["tracks"]["1_odd_q_jordan_census"]["orders"]
    q3, q5 = orders
    assert q3["dirac_rank_ladder"] == {"1": 50, "2": 26, "3": 2, "4": 0}
    assert q3["jordan_blocks"] == {"1": 6, "2": 0, "3": 22, "4": 2}
    assert q5["dirac_rank_ladder"] == {"1": 182, "2": 92, "3": 2, "4": 0}
    assert q5["jordan_blocks"] == {"1": 40, "2": 0, "3": 88, "4": 2}
    assert all(row["d3_top_is_all_ones_matrix"] and row["d3_bottom_is_all_ones_matrix"] for row in orders)


def test_deep_certificate_contains_gf9_scan() -> None:
    result = committed_result()
    orders = result["tracks"]["1_odd_q_jordan_census"]["orders"]
    assert [row["q"] for row in orders] == [3, 5, 7, 9]
    q9 = orders[-1]
    assert q9["field_model"] == "GF(9)=F3[w]/(w^2+1)"
    assert q9["points"] == q9["lines"] == 820
    assert q9["dirac_rank_ladder"] == {"1": 902, "2": 452, "3": 2, "4": 0}
    assert q9["jordan_blocks"] == {"1": 288, "2": 0, "3": 448, "4": 2}


def test_discriminant_lift_recovers_plus_types() -> None:
    track = fast_result()["tracks"]["2_integral_discriminant_lift"]
    assert track["halves"]["point"]["orthogonal_type"] == "O+_8(2)"
    assert track["halves"]["point"]["nonzero_isotropic_vectors"] == 135
    assert track["halves"]["line"]["orthogonal_type"] == "O+_20(2)"
    assert track["halves"]["line"]["nonzero_isotropic_vectors"] == 524799
    assert track["direct_sum"]["rank"] == 28
    assert track["direct_sum"]["orthogonal_type"] == "O+_28(2)"


def test_terminal_selector_and_typed_abi() -> None:
    result = fast_result()["tracks"]
    terminal = result["3_rank_two_terminal_selector"]
    assert terminal["terminal_plane_dimension"] == 2
    assert terminal["abstract_ray_permutation_group"] == "GL(2,2) = S3"
    abi = result["4_typed_packet_abi"]
    assert abi["abi"]["point_type"]["syndrome_width"] == 8
    assert abi["abi"]["line_type"]["syndrome_width"] == 20
    assert all(abi["canonical_basis_trials"]["point_basis_raw_retag_rejected"])
    assert all(abi["canonical_basis_trials"]["line_basis_raw_retag_rejected"])
    assert abi["common_kernel"]["dimension"] == 15


def test_centralizer_quotient_matches_d12_middleware_profile() -> None:
    track = fast_result()["tracks"]["5_centralizer_middleware_bridge"]
    assert track["centralizer_order_digits"] == 618
    assert track["terminal_quotient"]["group"] == "GL(2,2) = S3"
    assert track["middleware_bridge"]["D12_order_profile"] == {"1": 1, "2": 7, "3": 2, "6": 2}
    assert track["checks"]["runtime_factorization_24_45_48"] is True
    assert track["checks"]["mirror_bus_orbit_stabilizer"] is True
