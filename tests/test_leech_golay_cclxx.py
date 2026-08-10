"""Tests for Part CCLXX — Leech Lattice, Golay Code & Conway/Mathieu Groups.

All 40 bridge identities plus cross-cutting aggregate and JSON checks.
"""

from __future__ import annotations
import importlib, json, pathlib, sys
import pytest

# ── load bridge module ────────────────────────────────────────────────────────
ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "exploration"))
bridge = importlib.import_module("PART_CCLXX_LEECH_GOLAY_BRIDGE")

# Convenience: index checks by id
_by_id = {c["id"]: c for c in bridge.checks}

def ok(bid: str) -> bool:
    return _by_id[bid]["ok"]


# ═══════════════════════════════════════════════════════════════════════════════
# § 1  Extended Binary Golay Code
# ═══════════════════════════════════════════════════════════════════════════════

def test_golay_length_equals_2K():
    assert ok("B01")

def test_golay_dimension_equals_K():
    assert ok("B02")

def test_golay_min_distance_equals_2mu():
    assert ok("B03")

def test_golay_covering_radius_equals_mu():
    assert ok("B04")

def test_golay_length_equals_q_times_d():
    assert ok("B05")

def test_golay_weight_distribution_sum():
    assert ok("B06")

def test_golay_octad_count():
    assert ok("B07")

def test_golay_dodecad_count():
    assert ok("B08")


# ═══════════════════════════════════════════════════════════════════════════════
# § 2  Leech Lattice Λ₂₄
# ═══════════════════════════════════════════════════════════════════════════════

def test_leech_dim_equals_2K():
    assert ok("B09")

def test_leech_min_norm_equals_mu():
    assert ok("B10")

def test_leech_det_is_1():
    assert ok("B11")

def test_leech_kissing_number():
    assert ok("B12")

def test_kissing_over_edges():
    assert ok("B13")

def test_leech_dim_minus_min_norm():
    assert ok("B14")


# ═══════════════════════════════════════════════════════════════════════════════
# § 3  Theta Series
# ═══════════════════════════════════════════════════════════════════════════════

def test_theta_4_equals_kissing():
    assert ok("B15")

def test_theta_6_formula():
    assert ok("B16")

def test_two_to_K_minus_1_factorisation():
    assert ok("B17")

def test_theta_6_over_2K():
    assert ok("B18")


# ═══════════════════════════════════════════════════════════════════════════════
# § 4  Steiner System & Monstrous Moonshine
# ═══════════════════════════════════════════════════════════════════════════════

def test_steiner_system_octad_count():
    assert ok("B19")

def test_h_E7_coxeter_number():
    assert ok("B20")

def test_monster_head_dim_moonshine():
    assert ok("B21")

def test_j_const_744():
    assert ok("B22")


# ═══════════════════════════════════════════════════════════════════════════════
# § 5  Conway Groups
# ═══════════════════════════════════════════════════════════════════════════════

def test_co1_order_factorisation():
    assert ok("B23")

def test_phi3_divides_co1():
    assert ok("B24")

def test_phi6_divides_co1():
    assert ok("B25")

def test_phi6_divides_co2():
    assert ok("B26")

def test_phi6_divides_co3():
    assert ok("B27")

def test_co0_over_co1_equals_lambda():
    assert ok("B28")


# ═══════════════════════════════════════════════════════════════════════════════
# § 6  Mathieu Groups
# ═══════════════════════════════════════════════════════════════════════════════

def test_m24_order_factorisation():
    assert ok("B29")

def test_m24_over_m23_equals_degree():
    assert ok("B30")

def test_m23_order_factorisation():
    assert ok("B31")

def test_m22_order_factorisation():
    assert ok("B32")

def test_m12_order_factorisation():
    assert ok("B33")

def test_m12_over_m11_equals_K():
    assert ok("B34")


# ═══════════════════════════════════════════════════════════════════════════════
# § 7  Cross-connections & Niemeier Lattices
# ═══════════════════════════════════════════════════════════════════════════════

def test_niemeier_count_equals_2K():
    assert ok("B35")

def test_leech_dim_minus_golay_d_equals_lap_top():
    assert ok("B36")

def test_golay_covering_equals_leech_min_norm():
    assert ok("B37")

def test_nontrivial_golay_equals_theta6_over_2K():
    assert ok("B38")

def test_m11_order_factorisation():
    assert ok("B39")

def test_3_to_9_divides_co1():
    assert ok("B40")


# ═══════════════════════════════════════════════════════════════════════════════
# Aggregate checks
# ═══════════════════════════════════════════════════════════════════════════════

def test_all_40_pass():
    failures = [c["id"] for c in bridge.checks if not c["ok"]]
    assert failures == [], f"Failed: {failures}"

def test_count_is_40():
    assert len(bridge.checks) == 40

def test_verified_flag():
    assert bridge.verified is True

# Numerical spot-checks independent of bridge module logic
def test_kissing_number_value():
    assert bridge.LEECH_KISS == 196560

def test_theta_6_value():
    assert bridge.THETA_6 == 16773120

def test_monster_head_value():
    assert bridge.MONSTER_HEAD == 196884

def test_co1_value():
    assert bridge.CO1 == 4_157_776_806_543_360_000

def test_m24_value():
    assert bridge.M24 == 244_823_040

def test_octads_value():
    assert bridge.OCTADS == 759

def test_dodecads_value():
    assert bridge.DODECADS == 2576


# ═══════════════════════════════════════════════════════════════════════════════
# JSON output checks
# ═══════════════════════════════════════════════════════════════════════════════

JSON_PATH = ROOT / "PART_CCLXX_leech_golay_results.json"

@pytest.fixture(scope="module")
def results():
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))

def test_json_exists():
    assert JSON_PATH.exists()

def test_json_part(results):
    assert results["part"] == "CCLXX"

def test_json_verified(results):
    assert results["verified"] is True

def test_json_checks_passed(results):
    assert results["checks_passed"] == 40

def test_json_checks_total(results):
    assert results["checks_total"] == 40

def test_json_kissing(results):
    assert results["data"]["leech"]["kissing_number"] == 196560

def test_json_m24(results):
    assert results["data"]["mathieu"]["M24"] == 244_823_040
