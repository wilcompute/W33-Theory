from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "w33_pass1365_1369_rational_schur_completion.json"


def certificate():
    raw = DATA.read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def test_frozen_certificate():
    result, digest = certificate()
    assert digest == "0e6e4d5c7d9cd7981496e179e116f8280cc08dae2d1fc2c34d5f2020e84fe7aa"
    assert result["status"] == "PASS"


def test_rational_terwilliger_wedderburn():
    result, _ = certificate()
    record = result["pass1365_rational_terwilliger_wedderburn"]
    assert record["center_dimension_over_Q"] == 10
    assert record["rational_wedderburn"] == "Q^3 + M2(Q)^2 + M3(Q)^3 + M4(Q) + M5(Q)"
    assert [b["simple_block_size"] for b in record["blocks"]] == [1, 1, 1, 2, 2, 3, 3, 3, 4, 5]
    assert [b["module_multiplicity"] for b in record["blocks"]] == [3, 12, 14, 1, 2, 4, 4, 8, 8, 1]


def test_geometric_single_splitter():
    result, _ = certificate()
    record = result["pass1366_geometric_defect_splitter"]
    assert record["intersecting_shell_splitter"]["ordered_pairs"] == 108
    assert record["misaligned_shell_splitter"]["ordered_pairs"] == 432
    expected = {
        "T": 79,
        "T_plus_S2": 81,
        "T_plus_S4": 81,
        "T_plus_S2_plus_S4_as_one_generator": 83,
    }
    for profile in record["closure_dimensions_mod_good_primes"].values():
        assert profile == expected


def test_rational_orbital_refinement():
    result, _ = certificate()
    record = result["pass1367_rational_orbital_wedderburn"]
    assert record["center_dimension_over_Q"] == 14
    assert record["rational_wedderburn"] == "Q^7 + M2(Q)^2 + M3(Q)^3 + M4(Q) + M5(Q)"
    assert "14-10" in record["defect_explanation"]
    assert len(record["blocks"]) == 14


def test_coherent_configuration():
    result, _ = certificate()
    record = result["pass1368_coherent_configuration"]
    assert record["fiber_sizes"] == [1, 2, 36, 27, 54]
    assert record["orbitals"] == 83
    assert record["symmetric_orbitals"] == 29
    assert record["transpose_pairs"] == 27
    assert record["nonzero_intersection_constants"] == 4277
    assert record["sparse_intersection_tensor_sha256"] == "0473ae71069dbb62d63456f0cb3fea55e25c9e2286ac43b6f420b31feb526c34"
