"""Tests for PART CCCXCVIII -- Graph Polynomial Suite for W(3,3)."""

import pytest
from fractions import Fraction
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))

from PART_CCCXCVIII_GRAPH_POLY_BRIDGE import (
    # constants
    V, K, LAM, MU, EDGES, q, ALPHA, CLIQUE_NU, K4_COUNT, TRIANGLES,
    # clique polynomial
    clique_poly_coeffs, clique_poly_eval, clique_number,
    # independence polynomial seeds
    indep_poly_seed_i0, indep_poly_seed_i1,
    indep_poly_seed_i2, indep_poly_seed_i3,
    independence_number,
    # matching polynomial seeds
    matching_seed_m0, matching_seed_m1, matching_seed_m2,
    matching_number, hosoya_partial,
    # crosswalk / summary
    sm_crosswalk, verify_all, build_cccxcviii_summary,
)


# ── verify_all smoke test ─────────────────────────────────────────────────────

class TestVerifyAll:
    def test_all_27_pass(self):
        checks, passed, total = verify_all()
        assert total == 27
        assert passed == 27

    def test_no_failed_checks(self):
        checks, passed, total = verify_all()
        failed = [c for c in checks if not c["pass"]]
        assert failed == [], f"Failed: {failed}"

    def test_returns_list_of_dicts(self):
        checks, passed, total = verify_all()
        assert isinstance(checks, list)
        assert all(isinstance(c, dict) for c in checks)

    def test_check_keys_present(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert "check" in c and "value" in c and "expected" in c and "pass" in c


# ── Group 1: clique polynomial coefficients ───────────────────────────────────

class TestCliquePolyCoeffs:
    def test_length_five(self):
        assert len(clique_poly_coeffs()) == 5

    def test_c0_empty_clique(self):
        assert clique_poly_coeffs()[0] == 1

    def test_c1_vertices(self):
        assert clique_poly_coeffs()[1] == V == 40

    def test_c2_edges(self):
        assert clique_poly_coeffs()[2] == EDGES == 240

    def test_c3_triangles(self):
        assert clique_poly_coeffs()[3] == TRIANGLES == 160

    def test_c4_tetrahedra(self):
        assert clique_poly_coeffs()[4] == K4_COUNT == 40

    def test_c1_eq_c4(self):
        coeffs = clique_poly_coeffs()
        assert coeffs[1] == coeffs[4]

    def test_all_coeffs_positive(self):
        assert all(c > 0 for c in clique_poly_coeffs())

    def test_sum_of_coeffs_is_481(self):
        assert sum(clique_poly_coeffs()) == 481


# ── Group 2: clique polynomial evaluations ────────────────────────────────────

class TestCliquePolyEval:
    def test_at_0(self):
        assert int(clique_poly_eval(0)) == 1

    def test_at_1_total_cliques(self):
        assert int(clique_poly_eval(1)) == 481

    def test_at_minus1_eq_q4(self):
        assert int(clique_poly_eval(-1)) == q ** 4 == 81

    def test_at_2(self):
        assert int(clique_poly_eval(2)) == 2961

    def test_at_q_equals_9841(self):
        assert int(clique_poly_eval(q)) == 9841

    def test_at_1_eq_V_times_K_plus_1(self):
        assert int(clique_poly_eval(1)) == V * K + 1

    def test_returns_fraction(self):
        assert isinstance(clique_poly_eval(Fraction(1, 2)), Fraction)

    def test_at_half(self):
        # C(G;1/2) = 1 + 20 + 60 + 20 + 5/2 = 103.5 = 207/2
        result = clique_poly_eval(Fraction(1, 2))
        assert result == Fraction(207, 2)

    def test_clique_number_is_4(self):
        assert clique_number() == 4


# ── Group 3: independence polynomial seeds ────────────────────────────────────

class TestIndepPolySeeds:
    def test_i0_is_1(self):
        assert indep_poly_seed_i0() == 1

    def test_i1_is_V(self):
        assert indep_poly_seed_i1() == V == 40

    def test_i2_formula(self):
        expected = V * (V - 1) // 2 - EDGES  # C(40,2) - 240 = 540
        assert indep_poly_seed_i2() == expected == 540

    def test_i3_is_3240(self):
        assert indep_poly_seed_i3() == 3240

    def test_i3_eq_q4_times_V(self):
        assert indep_poly_seed_i3() == q ** 4 * V

    def test_i3_over_i2_eq_6(self):
        assert Fraction(indep_poly_seed_i3(), indep_poly_seed_i2()) == Fraction(6, 1)

    def test_i3_over_i2_eq_q_factorial(self):
        import math
        assert Fraction(indep_poly_seed_i3(), indep_poly_seed_i2()) == math.factorial(q)

    def test_independence_number_is_10(self):
        assert independence_number() == 10 == ALPHA

    def test_i2_nonneg(self):
        assert indep_poly_seed_i2() > 0

    def test_i3_nonneg(self):
        assert indep_poly_seed_i3() > 0

    def test_i_sequence_decreasing_ratio(self):
        # i1/i0 > i2/i1 > ... sanity: i2/i1 = 540/40 = 13.5
        assert Fraction(indep_poly_seed_i2(), indep_poly_seed_i1()) == Fraction(27, 2)


# ── Group 4: matching polynomial seeds ───────────────────────────────────────

class TestMatchingPolySeeds:
    def test_m0_is_1(self):
        assert matching_seed_m0() == 1

    def test_m1_is_edges(self):
        assert matching_seed_m1() == EDGES == 240

    def test_m2_is_26040(self):
        assert matching_seed_m2() == 26040

    def test_m2_formula(self):
        expected = EDGES * (EDGES - 1) // 2 - V * (K * (K - 1) // 2)
        assert matching_seed_m2() == expected

    def test_matching_number_is_20(self):
        assert matching_number() == V // 2 == 20

    def test_hosoya_partial_is_26281(self):
        assert hosoya_partial() == 1 + 240 + 26040 == 26281

    def test_m1_lt_m2(self):
        assert matching_seed_m1() < matching_seed_m2()

    def test_m2_positive(self):
        assert matching_seed_m2() > 0


# ── Group 5: SM crosswalk ─────────────────────────────────────────────────────

class TestSMCrosswalk:
    def test_C_at_minus1_eq_q4(self):
        cxw = sm_crosswalk()
        assert cxw["C_at_minus1"] == q ** 4

    def test_ambient_space_order(self):
        cxw = sm_crosswalk()
        assert cxw["ambient_space_order"] == 81

    def test_i3_crosswalk(self):
        cxw = sm_crosswalk()
        assert cxw["i3"] == 3240

    def test_i3_eq_q4_V(self):
        cxw = sm_crosswalk()
        assert cxw["i3_eq_q4_times_V"] is True

    def test_q_factorial(self):
        cxw = sm_crosswalk()
        assert cxw["q_factorial"] == 6

    def test_total_cliques_eq_VK_plus_1(self):
        cxw = sm_crosswalk()
        assert cxw["total_cliques"] == cxw["V_times_K_plus_1"] == 481

    def test_alpha_times_omega_eq_V(self):
        cxw = sm_crosswalk()
        assert cxw["alpha_times_omega"] == V

    def test_triangles_eq_V_mu(self):
        cxw = sm_crosswalk()
        assert cxw["triangles_eq_V_mu"] is True

    def test_clique_number_times_indep_number(self):
        assert CLIQUE_NU * ALPHA == V

    def test_c4_over_c3_eq_inv_MU(self):
        assert Fraction(K4_COUNT, TRIANGLES) == Fraction(1, MU)

    def test_triangles_formula_consistent(self):
        # TRIANGLES = V*K*LAM//6 = 160, also = V*MU
        assert V * K * LAM // 6 == V * MU == TRIANGLES


# ── build_summary ─────────────────────────────────────────────────────────────

class TestBuildSummary:
    def test_summary_pass_status(self):
        s = build_cccxcviii_summary()
        assert s["status"] == "PASS"

    def test_summary_checks_27(self):
        s = build_cccxcviii_summary()
        assert s["checks_total"] == 27
        assert s["checks_pass"] == 27

    def test_summary_part_label(self):
        s = build_cccxcviii_summary()
        assert s["part"] == "CCCXCVIII"

    def test_summary_has_discoveries(self):
        s = build_cccxcviii_summary()
        assert len(s["discoveries"]) >= 6

    def test_summary_fields_C_at_minus1(self):
        s = build_cccxcviii_summary()
        assert s["fields"]["C_at_minus1"] == 81

    def test_summary_fields_i3(self):
        s = build_cccxcviii_summary()
        assert s["fields"]["i3"] == 3240

    def test_summary_fields_m2(self):
        s = build_cccxcviii_summary()
        assert s["fields"]["m2"] == 26040

    def test_summary_fields_hosoya_partial(self):
        s = build_cccxcviii_summary()
        assert s["fields"]["hosoya_partial"] == 26281


# ── Constant sanity checks ────────────────────────────────────────────────────

class TestConstants:
    def test_V_eq_40(self):
        assert V == 40

    def test_K_eq_12(self):
        assert K == 12

    def test_EDGES_eq_240(self):
        assert EDGES == 240

    def test_q_eq_3(self):
        assert q == 3

    def test_TRIANGLES_eq_160(self):
        assert TRIANGLES == 160

    def test_K4_COUNT_eq_40(self):
        assert K4_COUNT == 40

    def test_K4_count_eq_V(self):
        assert K4_COUNT == V

    def test_ALPHA_eq_10(self):
        assert ALPHA == 10

    def test_q4_eq_81(self):
        assert q ** 4 == 81
