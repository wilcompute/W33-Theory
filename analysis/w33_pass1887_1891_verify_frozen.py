#!/usr/bin/env python3
"""Fail-closed verifier for Passes 1887--1891."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    1887: ROOT / "data/w33_pass1887_exact_global_weight5_decoder.json",
    1888: ROOT / "data/w33_pass1888_separator_refined_enumerators.json",
    1889: ROOT / "data/w33_pass1889_integral_carrier_gluing.json",
    1890: ROOT / "data/w33_pass1890_restricted_carrier_commutant_phases.json",
    1891: ROOT / "data/w33_pass1891_tutte_coxeter_voltage_carrier_lift.json",
}
EXPECTED = {
    1887: "7ef1e5ca4e59690117c6d655048cbf23c41d52a3afb1f6662cf6f91ee95134af",
    1888: "ecbfc311286b01bad5868ea64a1104a8b4a867a3e7c18f922e0e9d126c2d0c52",
    1889: "492eded53a985ee29c5a3d11d0b29be6ad67bee17f7023b609ca0ca3c12eab05",
    1890: "4a92e7e9dda57a77ea49524266efbd92a4057ee0c32125845eb2b0cea5637a27",
    1891: "43397493f408c0eeffe763166ff65608d0b90cf99a6f277a0b8e6808ce4bbc4b",
}
AGGREGATE = "4c280f57cadd9bef949b85af6c26bd4a21abbe17da8d6b0c09f0cf7575a5c4eb"


def digest(d: dict) -> str:
    x = dict(d)
    x.pop("sha256_without_hash_field", None)
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> dict:
    data = {p: json.loads(path.read_text()) for p, path in FILES.items()}
    for p, d in data.items():
        assert d["sha256_without_hash_field"] == EXPECTED[p] == digest(d), p
        assert all(d["checks"].values()), p

    d87, d88, d89, d90, d91 = (data[p] for p in range(1887, 1892))
    assert d87["global"] == {
        "BSC_weight5_success_term": "1531165872 * p^5 * (1-p)^235",
        "ambiguous_minimum_weight5": 4747680912,
        "lower_shadow": 84201264,
        "total_weight5": 6363048048,
        "unique_minimum_weight5": 1531165872,
    }
    assert sum((d87["global"][k] for k in ("lower_shadow", "unique_minimum_weight5", "ambiguous_minimum_weight5"))) == d87["global"]["total_weight5"]
    assert d87["weight10_degree"]["maximum_degree"] == 1953

    assert d88["fiber_subcode"]["words"] == 1 << 30
    assert d88["fiber_subcode"]["bins"] == 563
    assert d88["residual_subcode"]["words"] == 1 << 15
    assert d88["residual_subcode"]["s6_orbits"] == 156

    assert d89["single_half_integral_copy"]["extension_index_from_N_to_A"] == 1 << 9
    assert d89["paired_24_90_lattice"]["extension_index_from_N_pair_to_A_pair"] == 1 << 18
    assert d89["clock_order_comparison"]["maximal_order_index"] == 1 << 35
    assert d89["clock_order_comparison"]["absorption"] is False

    assert d90["exceptional_S6"]["commutant_real_dimension"] == 23
    assert d90["exceptional_S6"]["full_114_complex_structure"] is False
    assert d90["exceptional_S6"]["paired_natural_V9_complex_structure"] is True
    assert d90["clock_C4"]["commutant_real_dimension"] == 3260
    assert d90["clock_C4"]["combined_complex_structure"] is True

    assert d91["tutte_coxeter"]["eight_cycle_C4_orbits"] == {"fixed": 2, "free_orbits": 22, "orbit_size_distribution": {"1": 2, "4": 22}}
    assert d91["w33_240_coordinate_lift"]["decomposition"] == {"pair_transfer": 180, "phase": 40, "residual_triangles": 20}
    assert d91["w33_240_coordinate_lift"]["total_coordinate_orbits"] == 62
    assert d91["hashimoto"]["C4_fixed_directed_states"] == [90, 2, 10, 2]

    n = sum(len(d["checks"]) for d in data.values())
    assert n == 35
    aggregate = json.loads((ROOT / "data/w33_pass1887_1891_five_frontiers.json").read_text())
    assert aggregate["sha256_without_hash_field"] == AGGREGATE == digest(aggregate)
    assert aggregate["n_checks"] == aggregate["n_verified"] == n
    assert aggregate["certificates"] == {str(k): v for k, v in EXPECTED.items()}

    out = {
        "status": "PASS_WITH_WEIGHT6_AND_MIXED_ENUMERATOR_BOUNDARIES",
        "n_checks": n,
        "n_verified": n,
        "certificates": EXPECTED,
        "aggregate_sha256": AGGREGATE,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


if __name__ == "__main__":
    main()
