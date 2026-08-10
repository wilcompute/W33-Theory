from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(d: dict) -> str:
    x = dict(d)
    x.pop("sha256_without_hash_field", None)
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load(name: str) -> dict:
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def test_pass1887_exact_global_decoder_partition() -> None:
    d = load("w33_pass1887_exact_global_weight5_decoder.json")
    assert d["sha256_without_hash_field"] == digest(d) == "7ef1e5ca4e59690117c6d655048cbf23c41d52a3afb1f6662cf6f91ee95134af"
    assert all(d["checks"].values())
    g = d["global"]
    assert g["unique_minimum_weight5"] == 1_531_165_872
    assert g["ambiguous_minimum_weight5"] == 4_747_680_912
    assert g["lower_shadow"] + g["unique_minimum_weight5"] + g["ambiguous_minimum_weight5"] == g["total_weight5"] == 6_363_048_048
    assert d["fixed_coordinate"]["global_unique_weight5"] * 48 == g["unique_minimum_weight5"]


def test_pass1888_1891_structural_frontiers() -> None:
    d88 = load("w33_pass1888_separator_refined_enumerators.json")
    d89 = load("w33_pass1889_integral_carrier_gluing.json")
    d90 = load("w33_pass1890_restricted_carrier_commutant_phases.json")
    d91 = load("w33_pass1891_tutte_coxeter_voltage_carrier_lift.json")
    expected = {
        1888: "ecbfc311286b01bad5868ea64a1104a8b4a867a3e7c18f922e0e9d126c2d0c52",
        1889: "492eded53a985ee29c5a3d11d0b29be6ad67bee17f7023b609ca0ca3c12eab05",
        1890: "4a92e7e9dda57a77ea49524266efbd92a4057ee0c32125845eb2b0cea5637a27",
        1891: "43397493f408c0eeffe763166ff65608d0b90cf99a6f277a0b8e6808ce4bbc4b",
    }
    for p, d in zip(range(1888, 1892), (d88, d89, d90, d91)):
        assert d["sha256_without_hash_field"] == digest(d) == expected[p]
        assert all(d["checks"].values())
    assert d88["fiber_subcode"]["bins"] == 563
    assert d88["residual_subcode"]["s6_orbits"] == 156
    assert d89["paired_24_90_lattice"]["extension_index_from_N_pair_to_A_pair"] == 2**18
    assert d89["clock_order_comparison"]["absorption"] is False
    assert d90["exceptional_S6"]["commutant_real_dimension"] == 23
    assert d90["clock_C4"]["commutant_real_dimension"] == 3260
    assert d91["w33_240_coordinate_lift"]["pair_transfer_theorem"].startswith("Each pair-transfer coordinate")
    assert d91["hashimoto"]["C4_fixed_directed_states"] == [90, 2, 10, 2]


def test_aggregate_certificate() -> None:
    d = load("w33_pass1887_1891_five_frontiers.json")
    assert d["sha256_without_hash_field"] == digest(d) == "4c280f57cadd9bef949b85af6c26bd4a21abbe17da8d6b0c09f0cf7575a5c4eb"
    assert d["n_checks"] == d["n_verified"] == 35
    assert d["critical_values"]["global_unique_weight5"] == 1_531_165_872
    assert d["critical_values"]["pair_transfer_nonincidence_coordinates"] == 180
