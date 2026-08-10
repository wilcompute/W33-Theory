import importlib.util
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass1511_1515_cover_resolution_frontiers.json"


def payload():
    return json.loads(CERT.read_text(encoding="utf-8"))


def load_base():
    path = ROOT / "analysis" / "w33_pass1416_cokernel_signed_turn_intertwiner.py"
    spec = importlib.util.spec_from_file_location("p1416", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_all_frozen_checks_pass():
    p = payload()
    assert p["status"] == "PASS"
    assert len(p["checks"]) == 17
    assert all(p["checks"].values())


def test_sample_conditioning_and_disjoint_pair():
    p = payload()["pass1511_disjoint_pair_counterexample"]
    assert p["intersection_size"] == 0
    assert p["canonical_orbit"] == 0
    assert p["partner_orbit"] == 29
    assert "fix frame 0" in p["sampling_diagnosis"]


def test_disjoint_partner_frontier_and_graph():
    p = payload()
    q = p["pass1512_disjoint_partner_frontier"]
    assert q["orbit_types_hit"] == 327
    assert q["distinct_disjoint_covers"] == 13648
    assert q["raw_group_images"] == 32464
    g = p["pass1513_disjointness_graph_and_four_packing"]["graph"]
    assert g["edges"] == 188338
    assert g["triangles"] == 494
    assert g["k4_exists"] is False
    assert g["clique_number"] == 3


def test_four_packing_is_exact_and_disjoint():
    p = payload()["pass1513_disjointness_graph_and_four_packing"]
    packing = p["packing"]
    assert len(packing) == 4
    assert len(set().union(*map(set, packing))) == 240
    base = load_base()
    M = base.build_geometry()[5]
    for cover in packing:
        assert len(cover) == 60
        assert np.array_equal(M[cover].sum(axis=0), np.ones(240, dtype=np.int64))
    for i in range(4):
        for j in range(i + 1, 4):
            assert set(packing[i]).isdisjoint(packing[j])


def test_class45_lock():
    p = payload()["pass1514_class45_involution_lock"]
    assert p["involution_total"] == 315
    assert p["involution_class_sizes"] == [45, 270]
    assert p["c2_orbit_class_counts"] == {"45": 228}
    assert p["c2_fixed_profile_counts"] == {"class45_global84_cover12": 228}


def test_residual_fractional_integral_gap():
    p = payload()["pass1515_residual_integrality_gap"]
    assert p["residual_rows"] == 300
    assert p["edge_columns"] == 240
    assert p["row_degree"] == 4
    assert p["column_degree"] == 5
    assert p["fractional_weight_per_row"] == "1/5"
    assert p["fractional_total_weight"] == 60
    assert p["integral_search"]["found"] is False
    assert p["integral_search"]["nodes"] == 2332
    assert p["integral_search"]["forced_steps"] == 18227


def test_release_manifest():
    p = json.loads((ROOT / "data" / "w33_pass1511_1515_release_manifest.json").read_text(encoding="utf-8"))
    assert p["status"] == "PASS"
    assert p["validation"] == {
        "certificate_checks": 17,
        "cpp_sources_compile": True,
        "latex_insert_compiles": True,
        "pytest_tests": 7,
    }
    assert p["boundaries"]["packing"].endswith("remains open.")
