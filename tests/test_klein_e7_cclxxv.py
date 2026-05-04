"""
Tests for Part CCLXXV — Klein Quartic, PSL(2,7) and the E₇-56 bridge.
60 tests: one per named check (59) + meta-check that all 59 pass.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))
from PART_CCLXXV_KLEIN_E7_BRIDGE import build_summary

_RESULTS = None


def _r():
    global _RESULTS
    if _RESULTS is None:
        _RESULTS = build_summary()
    return _RESULTS


def ok(name: str) -> bool:
    hits = [c for c in _r()["checks"] if c["name"] == name]
    assert hits, f"Check '{name}' not found in results"
    return hits[0]["pass"]


# ── Section A: PSL(2,7) = GL(3,2) group arithmetic ───────────────────────────

def test_psl27_order():
    assert ok("psl27_order")

def test_psl27_phi6_times_24():
    assert ok("psl27_phi6_times_24")

def test_gl32_order():
    assert ok("gl32_order")

def test_psl27_eq_gl32():
    assert ok("psl27_eq_gl32")

def test_psl27_factored():
    assert ok("psl27_factored")

def test_psl27_div_phi6_is_2K():
    assert ok("psl27_div_phi6_is_2K")

def test_psl27_is_Q_VK():
    assert ok("psl27_is_Q_VK")

def test_psl27_is_phi6_FK():
    assert ok("psl27_is_phi6_FK")


# ── Section B: Klein quartic combinatorics ────────────────────────────────────

def test_klein_vertices():
    assert ok("klein_vertices")

def test_klein_edges():
    assert ok("klein_edges")

def test_klein_faces():
    assert ok("klein_faces")

def test_klein_euler_char():
    assert ok("klein_euler_char")

def test_klein_genus_from_chi():
    assert ok("klein_genus_from_chi")

def test_klein_genus_is_Q():
    assert ok("klein_genus_is_Q")

def test_klein_V_2_MU_PHI6():
    assert ok("klein_V_2_MU_PHI6")

def test_klein_E_PHI6_K():
    assert ok("klein_E_PHI6_K")

def test_klein_F_2K():
    assert ok("klein_F_2K")

def test_klein_face_val_PHI6():
    assert ok("klein_face_val_PHI6")

def test_klein_vertex_deg_Q():
    assert ok("klein_vertex_deg_Q")

def test_klein_handshaking_E():
    assert ok("klein_handshaking_E")

def test_klein_handshaking_V():
    assert ok("klein_handshaking_V")

def test_klein_aut_is_2EK():
    assert ok("klein_aut_is_2EK")


# ── Section C: Hurwitz (2,3,7)-triangle group ─────────────────────────────────

def test_hurwitz_r_is_PHI6():
    assert ok("hurwitz_r_is_PHI6")

def test_hurwitz_sum_value():
    assert ok("hurwitz_sum_value")

def test_hurwitz_sum_lt_1():
    assert ok("hurwitz_sum_lt_1")

def test_hurwitz_defect():
    assert ok("hurwitz_defect")

def test_hurwitz_bound():
    assert ok("hurwitz_bound")

def test_hurwitz_achieved():
    assert ok("hurwitz_achieved")


# ── Section D: E₇ Lie algebra ────────────────────────────────────────────────

def test_e7_rank_is_PHI6():
    assert ok("e7_rank_is_PHI6")

def test_e7_dim_phi6_factor():
    assert ok("e7_dim_phi6_factor")

def test_e7_pos_roots():
    assert ok("e7_pos_roots")

def test_e7_dim_from_structure():
    assert ok("e7_dim_from_structure")

def test_e7_min_rep_is_VK():
    assert ok("e7_min_rep_is_VK")

def test_e7_min_rep_2_MU_PHI6():
    assert ok("e7_min_rep_2_MU_PHI6")


# ── Section E: Theta characteristics and bitangents ──────────────────────────

def test_theta_total_2_2g():
    assert ok("theta_total_2_2g")

def test_theta_odd_value():
    assert ok("theta_odd_value")

def test_theta_even_value():
    assert ok("theta_even_value")

def test_theta_sum():
    assert ok("theta_sum")

def test_theta_odd_is_MU_PHI6():
    assert ok("theta_odd_is_MU_PHI6")

def test_bitangents_eq_theta_odd():
    assert ok("bitangents_eq_theta_odd")

def test_theta_2g_galois_period():
    assert ok("theta_2g_galois_period")


# ── Section F: Heawood graph bridge ──────────────────────────────────────────

def test_heawood_V_2_PHI6():
    assert ok("heawood_V_2_PHI6")

def test_heawood_CHR_PHI6():
    assert ok("heawood_CHR_PHI6")

def test_klein_E_MU_heawood_E():
    assert ok("klein_E_MU_heawood_E")

def test_klein_V_MU_heawood_V():
    assert ok("klein_V_MU_heawood_V")

def test_psl27_div_heawood_V_K():
    assert ok("psl27_div_heawood_V_K")

def test_psl27_2MU_heawood_E():
    assert ok("psl27_2MU_heawood_E")

def test_klein_E_heawood_e7():
    assert ok("klein_E_heawood_e7")


# ── Section G: W(3,3) arithmetic cross-identities ────────────────────────────

def test_cross_VK_minus_V():
    assert ok("cross_VK_minus_V")

def test_cross_psl27_mod_V():
    assert ok("cross_psl27_mod_V")

def test_cross_EK_mod_V():
    assert ok("cross_EK_mod_V")

def test_cross_total_4_V1():
    assert ok("cross_total_4_V1")

def test_cross_e7_rank_hurwitz_r():
    assert ok("cross_e7_rank_hurwitz_r")

def test_cross_genus_from_triple():
    assert ok("cross_genus_from_triple")

def test_cross_EK_Q_bitangents():
    assert ok("cross_EK_Q_bitangents")

def test_cross_VK_2_bitangents():
    assert ok("cross_VK_2_bitangents")

def test_cross_psl27_6_bitangents():
    assert ok("cross_psl27_6_bitangents")

def test_cross_phi6_unifier():
    assert ok("cross_phi6_unifier")

def test_cross_phi6_unifier2():
    assert ok("cross_phi6_unifier2")


# ── Meta: all 59 pass ─────────────────────────────────────────────────────────

def test_all_59_pass():
    r = _r()
    assert r["checks_passed"] == r["checks_total"] == 59, (
        f"Expected 59/59 but got {r['checks_passed']}/{r['checks_total']}; "
        f"failed: {r['failed_check_names']}"
    )
