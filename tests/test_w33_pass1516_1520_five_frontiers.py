from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "w33_pass1516_1520_five_frontiers.json"
SCRIPT = ROOT / "analysis" / "w33_pass1516_1520_five_frontiers.py"
EXPECTED_CERT_SHA = "603380fbc9370b97b08273a67785b43f9c52960610d84661f99228bbe020ab48"


def payload() -> dict:
    return json.loads(CERT.read_text(encoding="utf-8"))


def load_worker():
    spec = importlib.util.spec_from_file_location("pass1516_1520", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_certificate_digest_schema_and_rebuild():
    assert hashlib.sha256(CERT.read_bytes()).hexdigest() == EXPECTED_CERT_SHA
    data = payload()
    assert data["schema"] == "w33.pass1516_1520.five_frontiers.v1"
    assert data["status"] == "PASS"
    assert load_worker().build() == data


def test_pass1516_relation_frontier():
    p = payload()["pass1516_radical_graded_relations"]
    assert p["p2"]["tensor_path_dimensions_degrees_0_through_loewy"] == [38, 29, 45, 59]
    assert p["p2"]["associated_graded_radical_layer_dimensions"] == [38, 29, 16, 0]
    assert p["p2"]["relation_kernel_dimensions"] == [0, 0, 29, 59]
    assert p["p2"]["quadratic_relation_dimension"] == 29
    assert len(p["p2"]["connected_components"]) == 6
    assert p["p3"]["tensor_path_dimensions_degrees_0_through_loewy"] == [11, 23, 92, 333, 1231, 4560, 16952]
    assert p["p3"]["associated_graded_radical_layer_dimensions"] == [11, 23, 22, 13, 10, 4, 0]
    assert p["p3"]["relation_kernel_dimensions"] == [0, 0, 70, 320, 1221, 4556, 16952]
    assert p["p3"]["quadratic_relation_dimension"] == 70
    assert len(p["p3"]["connected_components"]) == 1


def test_pass1517_coordinate_free_fourier():
    p = payload()["pass1517_coordinate_free_fourier"]
    assert p["canonical_isotypic_ranks"] == [1, 2, 2, 4, 4, 8, 8, 2, 4, 12, 12, 24, 32, 5]
    assert p["module_dimension_sum_m_times_d"] == 120
    assert p["selector_commutant_dimension_sum_m_squared"] == 83
    assert p["dual_image_dimension_sum_d_squared"] == 335
    assert p["tensor_factorization_gauge_group_dimension"] == 404


def test_pass1518_d4_no_go():
    p = payload()["pass1518_apartment_d4_obstruction"]
    assert p["local_mask_orbit_sizes"] == [4, 4]
    assert p["sheet_rank_distribution"] == {"70": 4, "76": 1, "81": 19}
    assert p["sheet_rank_count_mod_4"] == {"70": 0, "76": 1, "81": 3}
    assert p["global_rank_preserving_d4_lift_exists"] is False
    assert p["bridge_census_alone_has_cardinality_obstruction"] is False


def test_pass1519_arithmetic_support():
    p = payload()["pass1519_maximal_order_arithmetic"]
    assert p["z_rank"] == 83
    assert p["local_defect_lengths"] == {"2": 36, "3": 113}
    assert p["orbital_discriminant_valuations"] == {"2": 72, "3": 226}
    assert p["local_equality_away_from_2_3"] is True
    assert p["conductor_support_subset"] == [2, 3]
    assert p["unlabeled_equal_block_permutation_group_order"] == 60480


def test_pass1520_equivariant_morita_refinement():
    p = payload()["pass1520_equivariant_morita"]
    assert p["equivalence_bimodule_dimension"] == 120 * 81
    assert p["pairings_G_equivariant"] is True
    assert p["strict_G_equivariant_Morita_context"] is True
    assert p["equivariant_Brauer_obstruction"] == "zero"
    assert p["G_fixed_cross_map_present"] is False
    assert p["apartment_generator_span_dimension"] == 75
    assert p["saturated_bimodule_dimension"] == 9720


def test_report_and_insert_preserve_boundaries():
    report = (ROOT / "analysis" / "BT1516_BT1520_five_frontiers.md").read_text(encoding="utf-8")
    insert = (ROOT / "paper" / "sections" / "sec_bt1516_bt1520_five_frontiers.tex").read_text(encoding="utf-8")
    assert EXPECTED_CERT_SHA in report
    assert r"complete Ext\(^2\) or Yoneda multiplication table" in report
    assert "no global rank-preserving" in report
    assert "Hom}_G(W,V)=0" in insert
    assert "not an equivariant Morita obstruction" in insert
