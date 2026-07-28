from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(number: int) -> dict:
    matches = sorted((ROOT / "data").glob(f"w33_pass{number}_*.json"))
    assert len(matches) == 1, matches
    data = json.loads(matches[0].read_text(encoding="utf-8"))
    assert data["status"] == "PASS"
    assert data["checks"] and all(data["checks"].values())
    return data


def test_pass1193_s5_a5_coset_bridge() -> None:
    data = load(1193)
    assert data["theorem"]["intersection"] == "S5 ∩ PSp(4,3) = A5"
    assert data["theorem"]["three_copies"] == 3
    for record in data["records"]:
        assert record["we6_stabilizer"]["order"] == 120
        assert record["psp43_intersection"]["order"] == 60
        assert record["coset_models"]["we6_over_s5_index"] == 432
        assert record["coset_models"]["psp43_over_a5_index"] == 432


def test_pass1194_residual_central_idempotents() -> None:
    data = load(1194)
    assert data["residual_dimension"] == 1952
    assert data["center_dimension"] == 10
    assert data["commutant_dimension"] == 1109
    assert sum(item["residual_rank"] for item in data["projectors"]) == 1952
    assert {item["irrep"] for item in data["projectors"]} == {"1", "6", "15", "15a", "20", "24", "30", "60a", "64", "90"}


def test_pass1195_hashimoto_packets() -> None:
    data = load(1195)
    packets = data["spectral_packets"]
    assert [packets[key]["dimension"] for key in ("x_minus_11", "x_minus_1", "x_plus_1", "x2_minus_2x_plus_11", "x2_plus_4x_plus_11")] == [1, 201, 200, 48, 30]
    assert sum(packet["dimension"] for packet in packets.values()) == 480
    assert packets["x_minus_1"]["module"] == "30_outer_negative + 81_plus + 90"
    assert packets["x_plus_1"]["module"] == "15a + 20 + 24 + 60a + 81_plus"


def test_pass1196_primitive_cycle_orbits() -> None:
    data = load(1196)
    literal = data["literal_orbit_frontier"]["data"]
    totals = data["degree40_continuation"]["primitive_total"]
    assert [literal[str(n)]["primitive_oriented_rotation_classes"] for n in range(3, 7)] == [320, 3480, 36288, 302880]
    assert [literal[str(n)]["PSp(4,3)"]["orbit_count"] for n in range(3, 7)] == [1, 2, 3, 18]
    assert [literal[str(n)]["W(E6)"]["orbit_count"] for n in range(3, 7)] == [1, 2, 2, 13]
    assert [totals[str(n)] for n in range(3, 7)] == [320, 3480, 36288, 302880]
    assert totals["40"] == 11314813892043987952589222211358740216768


def test_pass1197_parallel_collision_guard() -> None:
    data = load(1197)
    assert data["registry"]["registered_pass_count"] >= 74
    assert data["registry"]["minimum_baseline_registered"] == 74
    assert data["registry"]["collisions"] == []
    assert data["registry"]["unregistered_modern_files"] == []
    assert data["current_block"]["range"] == "1193-1197"
    assert data["current_block"]["status"] == "COMPLETE"
    assert all(data["gate_checks"].values())
