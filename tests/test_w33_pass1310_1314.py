"""Regression tests for the literal A5 coset correction packet."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "w33_pass1310_1314_literal_a5_coset_correction.json"


def load_result() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_literal_group_and_carrier_counts() -> None:
    result = load_result()
    construction = result["construction"]
    assert result["status"] == "PASS"
    assert construction["e8_roots"] == 240
    assert construction["a2_triples"] == 2240
    assert construction["we6_order"] == 51840
    assert construction["psp43_order"] == 25920
    assert construction["number_of_432_carriers"] == 3


def test_all_three_carriers_have_literal_a5_census() -> None:
    result = load_result()["literal_432_carrier_theorem"]
    assert result["all_three_carriers_agree"] is True
    assert result["exact_fixed_point_vector"] == [432, 24, 36, 2, 2]
    assert result["exact_hecke_dimension"] == 26
    for record in result["records"]:
        assert record["carrier_size"] == 432
        assert record["s5_stabilizer_order"] == 120
        assert record["a5_intersection_order"] == 60
        assert record["a5_orbit_count"] == 26
        assert sum(record["a5_orbit_sizes"]) == 432
        assert len(record["a5_orbit_sizes"]) == 26


def test_exact_a5_character_decomposition() -> None:
    result = load_result()["literal_432_carrier_theorem"]
    expected = {"1": 26, "3": 16, "3prime": 16, "4": 40, "5": 30}
    dimensions = {"1": 1, "3": 3, "3prime": 3, "4": 4, "5": 5}
    for record in result["records"]:
        multiplicities = record["a5_permutation_character_multiplicities"]
        assert multiplicities == expected
        assert sum(dimensions[k] * multiplicities[k] for k in dimensions) == 432
        assert sum(value * value for value in multiplicities.values()) == 3688


def test_recent_candidate_and_carrier_conflation_are_rejected() -> None:
    corrections = load_result()["corrections"]
    assert corrections["pass1260_1263_burnside_value"] == "43/5"
    assert corrections["pass1260_1263_claimed_value"] == 9
    firewall = corrections["carrier_firewall"]
    assert firewall["coset_carrier_dimension"] == 432
    assert firewall["hashimoto_packet_dimensions"] == [1, 201, 200, 48, 30]
    assert firewall["hashimoto_packet_sum"] == 480
    assert firewall["hashimoto_packet_sum"] != firewall["coset_carrier_dimension"]


def test_all_certificate_checks_are_fail_closed() -> None:
    checks = load_result()["checks"]
    assert checks
    assert all(checks.values())
