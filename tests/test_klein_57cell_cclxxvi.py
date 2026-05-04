"""
Tests for Part CCLXXVI — Klein Quartic to the 57-cell / 11-cell / Tomotope Triad.
51 tests: one per named check (50) + meta-check that all 50 pass.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))
from PART_CCLXXVI_KLEIN_57CELL_BRIDGE import build_summary

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


# ── Section A: Consecutive trio (55, 56, 57) ─────────────────────────────────

def test_trio_e11_eq_vk_minus_1():
    assert ok("trio_e11_eq_vk_minus_1")

def test_trio_vk_eq_e7_min_rep():
    assert ok("trio_vk_eq_e7_min_rep")

def test_trio_v57_eq_vk_plus_1():
    assert ok("trio_v57_eq_vk_plus_1")

def test_trio_consecutive():
    assert ok("trio_consecutive")

def test_trio_span():
    assert ok("trio_span")

def test_trio_span_is_LAM():
    assert ok("trio_span_is_LAM")


# ── Section B: 57-cell edges from Klein automorphism order ───────────────────

def test_b_e57_eq_psl27_plus_Q():
    assert ok("b_e57_eq_psl27_plus_Q")

def test_b_e57_eq_2ek_plus_Q():
    assert ok("b_e57_eq_2ek_plus_Q")

def test_b_e57_eq_v57_times_Q():
    assert ok("b_e57_eq_v57_times_Q")

def test_b_psl27_eq_e57_minus_Q():
    assert ok("b_psl27_eq_e57_minus_Q")

def test_b_ek_eq_e57_minus_psl27():
    assert ok("b_ek_eq_e57_minus_psl27")


# ── Section C: 11-cell automorphisms via Klein vertex count ───────────────────

def test_c_v11_eq_K_minus_1():
    assert ok("c_v11_eq_K_minus_1")

def test_c_e11_eq_C_v11_2():
    assert ok("c_e11_eq_C_v11_2")

def test_c_ord_psl2_11_eq_K_e11():
    assert ok("c_ord_psl2_11_eq_K_e11")

def test_c_ord_psl2_11_via_vk():
    assert ok("c_ord_psl2_11_via_vk")


# ── Section D: 57-cell automorphisms via Klein vertex count ───────────────────

def test_d_ord_psl2_19_eq_v57_A5():
    assert ok("d_ord_psl2_19_eq_v57_A5")

def test_d_ord_psl2_19_via_vk():
    assert ok("d_ord_psl2_19_via_vk")

def test_d_gcd_psl2_19_psl27_eq_K():
    assert ok("d_gcd_psl2_19_psl27_eq_K")

def test_d_gcd_psl2_11_psl27_eq_K():
    assert ok("d_gcd_psl2_11_psl27_eq_K")

def test_d_gcd_psl2_11_psl2_19():
    assert ok("d_gcd_psl2_11_psl2_19")


# ── Section E: Tomotope / Klein via Klitzing ladder ──────────────────────────

def test_e_klitzing_rung1_eq_K():
    assert ok("e_klitzing_rung1_eq_K")

def test_e_klitzing_rung2_eq_FK():
    assert ok("e_klitzing_rung2_eq_FK")

def test_e_klitzing_rung3_eq_4K():
    assert ok("e_klitzing_rung3_eq_4K")

def test_e_klitzing_rung4_eq_8K():
    assert ok("e_klitzing_rung4_eq_8K")

def test_e_klitzing_pure_doubling():
    assert ok("e_klitzing_pure_doubling")

def test_e_tomo_flags_eq_psl27_fk():
    assert ok("e_tomo_flags_eq_psl27_fk")

def test_e_tomo_flags_minus_psl27():
    assert ok("e_tomo_flags_minus_psl27")

def test_e_gcd_ord_tomo_psl27():
    assert ok("e_gcd_ord_tomo_psl27")


# ── Section F: E₇ dimension from 57-cell prime P₁₉ ──────────────────────────

def test_f_P19_eq_K_plus_Q_plus_MU():
    assert ok("f_P19_eq_K_plus_Q_plus_MU")

def test_f_v57_eq_Q_times_P19():
    assert ok("f_v57_eq_Q_times_P19")

def test_f_e7_dim_eq_phi6_P19():
    assert ok("f_e7_dim_eq_phi6_P19")

def test_f_e7_dim_div_phi6_eq_P19():
    assert ok("f_e7_dim_div_phi6_eq_P19")

def test_f_v57_div_Q_eq_P19():
    assert ok("f_v57_div_Q_eq_P19")

def test_f_e7_dim_v57_same_P19():
    assert ok("f_e7_dim_v57_same_P19")


# ── Section G: PSL(2,p) tower complete with PHI6 slot ────────────────────────

def test_g_psl_p3_eq_K():
    assert ok("g_psl_p3_eq_K")

def test_g_psl_p5_eq_A5():
    assert ok("g_psl_p5_eq_A5")

def test_g_psl_p7_eq_psl27():
    assert ok("g_psl_p7_eq_psl27")

def test_g_psl_p11_eq_ord_psl2_11():
    assert ok("g_psl_p11_eq_ord_psl2_11")

def test_g_psl_p19_eq_ord_psl2_19():
    assert ok("g_psl_p19_eq_ord_psl2_19")

def test_g_psl27_slot_ratio():
    assert ok("g_psl27_slot_ratio")

def test_g_tower_primes_ascending():
    assert ok("g_tower_primes_ascending")


# ── Section H: W(3,3) cross-identities ───────────────────────────────────────

def test_h_v57_minus_e11_eq_LAM():
    assert ok("h_v57_minus_e11_eq_LAM")

def test_h_v57_plus_vk_prime():
    assert ok("h_v57_plus_vk_prime")

def test_h_e11_plus_e57_eq_226():
    assert ok("h_e11_plus_e57_eq_226")

def test_h_11cell_palindrome():
    assert ok("h_11cell_palindrome")

def test_h_57cell_palindrome():
    assert ok("h_57cell_palindrome")

def test_h_57cell_degree_2Q():
    assert ok("h_57cell_degree_2Q")

def test_h_e57_from_degree():
    assert ok("h_e57_from_degree")

def test_h_e7_rank_is_PHI6():
    assert ok("h_e7_rank_is_PHI6")

def test_h_P19_via_e7_dim():
    assert ok("h_P19_via_e7_dim")


# ── Meta: all 50 checks pass ─────────────────────────────────────────────────

def test_all_50_checks_pass():
    r = _r()
    assert r["checks_total"] == 50, f"Expected 50 checks, got {r['checks_total']}"
    assert r["all_pass"], f"Failed checks: {r['failed_check_names']}"
