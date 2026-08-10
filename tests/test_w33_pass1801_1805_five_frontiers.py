from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def test_frozen_exact_five_frontier_certificate() -> None:
    payload = load("w33_pass1801_1805_five_frontiers.json")
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())
    assert payload["certificate_sha256"] == "0e79393320a6e50e5f2f9e4e0ff4982d8fb211b13951781ab4e0be4ba5adfec7"

    brauer = payload["pass1801_bockstein_brauer"]
    assert brauer["filtration_dimensions"] == [1, 9, 10, 16, 30]
    assert brauer["successive_factors_over_F2"] == ["1", "8_F2", "1", "6", "14"]
    assert brauer["composition_factors_over_alg_closure"] == [
        "1",
        "4a",
        "4b",
        "1",
        "6",
        "14",
    ]
    assert brauer["factor_certificates"]["8_F2"] == {
        "algebra": 32,
        "centralizer": 2,
        "center": "F4 via z^2+z+1",
    }

    xor_data = payload["pass1802_xor_resolution"]
    assert xor_data["rank_summary"]["base"] == [2100, 2760]
    assert xor_data["rank_summary"]["aug_sym"] == [2349, 2511]
    assert xor_data["new_global_XOR_directions"] == 240

    transfer = payload["pass1803_three_body_orbit_transfer"]
    assert len(transfer["triple_orbits"]) == 6
    assert len(transfer["four_subset_orbits"]) == 20
    assert transfer["transfer_sha256"] == "b046eeac796e13eebb71ef72b12aebb4ddf577591c93a55d9f6938dd36e0339e"

    decoder = payload["pass1804_optimal_low_weight_decoder"]
    assert decoder["minimum_weight_decoder_coefficients"] == {
        "0": 1,
        "1": 240,
        "2": 25440,
        "3": 1576000,
    }
    assert decoder["syndrome_orbit_count_through_weight3"] == 110

    outer = payload["pass1805_full_weyl_coexact_extension"]
    assert outer["canonical_multiplier_minus_one_outer"] == {
        "trace": 2,
        "plus_eigenspace": 16,
        "minus_eigenspace": 14,
        "determinant": 1,
    }


def test_frozen_components_and_bounded_milp_artifact() -> None:
    expected = {
        1801: "e90179321e1f038fbf2fbb754dd56122280cd2912518bdfa9f64c14422c667f0",
        1802: "ba0e5da60490f40511d729d856429c6c0be96f15fec65eaa05ae36bc346d490d",
        1803: "b3c058831de4450a489cc96f5b3e67c4effdce5edd41d8f40b8363a05b59251c",
        1804: "54836f6ef44573db34f85a6e3ca798c0ef1cc75a111df86b22c6eff76135f295",
        1805: "766cba3b97d2e6fcef7101e8f7051dceae9432fc3e2dc5da807894694b11fd4a",
    }
    for number, digest in expected.items():
        payload = load(f"w33_pass{number}_component.json")
        assert payload["status"] == "PASS"
        assert payload["sha256"] == digest

    frozen = load("w33_pass1802_xor_milp_falsifier.json")
    assert frozen["status"] == "BOUNDED_EXPERIMENT"
    assert frozen["model"] == {
        "variables": 4860,
        "binary_variables": 4860,
        "equality_constraints": 3105,
        "frame_color_equations": 540,
        "edge_color_equations": 2160,
        "octet_exact8_equations": 405,
        "symmetry_fixed_variables": 9,
        "matrix_nnz": 53460,
        "model_sha256": "dac90bab2946d49d77680444f751c162f029896db7b90ecc4c55c91e81d1ece2",
    }
    assert frozen["solver"]["has_incumbent"] is False
    assert frozen["solver"]["status_code"] == 1
