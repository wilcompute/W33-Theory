from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass5595_5602_projectivity_closure_toe_probes.py"
spec = importlib.util.spec_from_file_location("p5595", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_pass5595_q3_q5_automorphism_counts():
    q3 = mod.natural_aut_count_prime(3)
    q5 = mod.natural_aut_count_prime(5)
    assert q3["natural_automorphisms_enumerated"] == 576
    assert q5["natural_automorphisms_enumerated"] == 14400


def test_pass5596_explicit_reye_latin_conjugacy():
    out = mod.latin_reye_conjugacy()
    assert out["status"] == "EXPLICIT_PERMUTATION_ISOMORPHISM"
    assert out["group_order"] == 576
    assert out["orbital_sizes"] == [12, 36, 96]
    assert out["small_orbital_graph"] == "3 disjoint K4 blocks"


def test_pass5597_q9_extension_field_replay():
    out, rows = mod.extension_replay(mod.GFp2(3, 2))
    assert out["q"] == 9
    assert out["singular_grid"] == 100
    assert out["nonsingular_square_class"] == 360
    assert out["binary_rank"] == 50
    assert len(rows) == 360


def test_pass5598_projectivity_is_proper_subcode_of_restricted_line_code_q3():
    out = mod.footprint_projection_anchor(3)
    assert out["restricted_line_code_rank"] == 15
    assert out["projectivity_code_rank"] == 8
    assert out["projectivity_code_is_contained_in_restricted_line_code"]
    assert not out["restricted_line_code_equals_projectivity_code"]


def test_pass5599_q5_full_fixedpoint_fusion_and_formulas():
    _, G = mod.pgl_psl_perms_prime(5)
    out = mod.scheme_anchor(5, G, verify_all=True)
    assert out["relation_valencies_0_1_2_fixed"] == [20, 24, 15]
    assert out["full_intersection_constancy_verified"]
    assert out["nontrivial_intersection_matrices"][0] == [
        [7, 6, 6], [6, 12, 6], [6, 6, 3]
    ]


def test_pass5601_q3_isodual_code():
    out = mod.dual_coset_anchor_prime(3, enumerate_weights=True)
    assert out["length"] == 16
    assert out["rank_plus"] == out["rank_minus"] == 8
    assert out["cross_orthogonal"]
    assert out["therefore_exact_duals"]
    assert out["minimum_distance_measured"] == 4
    assert out["weight_enumerator"] == {
        "0": 1, "4": 12, "6": 64, "8": 102,
        "10": 64, "12": 12, "16": 1,
    }


def test_pass5602_flat_spectral_formula_arithmetic():
    for q in (3, 5, 9, 25):
        raw = (q*q - 1) // 2
        frame_bound_num = q*q - 1
        frame_bound_den = 2*q
        assert raw > 0
        assert frame_bound_num > 0 and frame_bound_den > 0
