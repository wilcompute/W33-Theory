"""
Tests for PART CCCC: Signed Graphs and Harary Balance for W(3,3).
"""
import pytest
from exploration.PART_CCCC_SIGNED_GRAPH_BALANCE_BRIDGE import (
    # constants (re-imported via module)
    V, K, LAM, MU, EDGES, MULT_R, MULT_S, R_EIG, S_EIG, TRIANGLES, ALPHA,
    # cycle/cocycle space
    cycle_space_dim, cocycle_space_dim,
    balanced_sign_count_exp, total_sign_count_exp,
    fraction_balanced_exponent, switching_class_count_exp,
    # harary balance
    all_positive_is_balanced, all_negative_is_balanced,
    frustration_all_positive, neg_triangles_count,
    # seidel eigenvalues
    seidel_eig_trivial, seidel_eig_r, seidel_eig_s,
    seidel_trace, seidel_energy,
    # seidel structural
    seidel_sum_squares, seidel_neg_count, seidel_pos_count,
    seidel_trivial_eq_mult_s, seidel_r_eq_neg_mu_plus_1,
    seidel_s_eq_k_minus_mu_minus_1,
    # spectral cut bounds
    max_cut_spectral_upper, max_cut_independence_lb,
    frustration_lb_all_neg, frustration_lb_equals_v_times_lam,
    seidel_eigenvalue_multiplicities_sum, seidel_signed_complete_balanced,
    # top-level
    sm_crosswalk, verify_all, build_cccc_summary,
)


class TestVerifyAll:
    def test_all_pass(self):
        checks, passed, total = verify_all()
        assert passed == total

    def test_count_is_27(self):
        checks, passed, total = verify_all()
        assert total == 27

    def test_no_failures(self):
        checks, passed, total = verify_all()
        failed = [n for n, ok in checks if not ok]
        assert failed == [], f"Failed: {failed}"


class TestConstants:
    def test_V(self):  assert V == 40
    def test_K(self):  assert K == 12
    def test_LAM(self):  assert LAM == 2
    def test_MU(self):  assert MU == 4
    def test_EDGES(self):  assert EDGES == 240
    def test_MULT_R(self):  assert MULT_R == 24
    def test_MULT_S(self):  assert MULT_S == 15
    def test_TRIANGLES(self):  assert TRIANGLES == 160
    def test_ALPHA(self):  assert ALPHA == 10


class TestCycleAndCocycleSpace:
    def test_cycle_space_dim(self):
        assert cycle_space_dim() == 201

    def test_cocycle_space_dim(self):
        assert cocycle_space_dim() == 39

    def test_cycle_plus_cocycle(self):
        # should sum to EDGES = 240
        assert cycle_space_dim() + cocycle_space_dim() == EDGES

    def test_balanced_sign_count_exp(self):
        assert balanced_sign_count_exp() == 39

    def test_balanced_sign_count_eq_cocycle_dim(self):
        assert balanced_sign_count_exp() == cocycle_space_dim()

    def test_total_sign_count_exp(self):
        assert total_sign_count_exp() == EDGES

    def test_fraction_balanced_exponent(self):
        assert fraction_balanced_exponent() == -201

    def test_fraction_balanced_eq_neg_cycle_space(self):
        assert fraction_balanced_exponent() == -cycle_space_dim()

    def test_switching_class_count_exp(self):
        assert switching_class_count_exp() == 200

    def test_switching_class_count_eq_edges_minus_v(self):
        assert switching_class_count_exp() == EDGES - V


class TestHararyBalance:
    def test_all_positive_is_balanced(self):
        assert all_positive_is_balanced() is True

    def test_all_negative_not_balanced(self):
        # W(3,3) has triangles so is not bipartite
        assert all_negative_is_balanced() is False

    def test_frustration_all_positive(self):
        assert frustration_all_positive() == 0

    def test_neg_triangles_count_equals_triangles(self):
        assert neg_triangles_count() == TRIANGLES

    def test_neg_triangles_is_160(self):
        assert neg_triangles_count() == 160

    def test_triangles_nonzero_confirms_unbalanced(self):
        assert TRIANGLES > 0


class TestSeidelEigenvalues:
    def test_seidel_eig_trivial(self):
        assert seidel_eig_trivial() == 15

    def test_seidel_eig_r(self):
        assert seidel_eig_r() == -5

    def test_seidel_eig_s(self):
        assert seidel_eig_s() == 7

    def test_seidel_trace_zero(self):
        assert seidel_trace() == 0

    def test_seidel_trace_manual(self):
        val = 15 * 1 + (-5) * 24 + 7 * 15
        assert val == 0

    def test_seidel_energy(self):
        assert seidel_energy() == EDGES

    def test_seidel_energy_equals_240(self):
        assert seidel_energy() == 240

    def test_seidel_trivial_is_v_minus_2k_minus_1(self):
        assert seidel_eig_trivial() == V - 2 * K - 1

    def test_seidel_r_is_neg_2r_minus_1(self):
        assert seidel_eig_r() == -(2 * R_EIG + 1)

    def test_seidel_s_is_neg_2s_minus_1(self):
        assert seidel_eig_s() == -(2 * S_EIG + 1)


class TestSeidelStructural:
    def test_seidel_sum_squares(self):
        assert seidel_sum_squares() == V * (V - 1)

    def test_seidel_sum_squares_is_1560(self):
        assert seidel_sum_squares() == 1560

    def test_seidel_neg_count(self):
        assert seidel_neg_count() == EDGES

    def test_seidel_pos_count(self):
        assert seidel_pos_count() == 540

    def test_seidel_neg_plus_pos_eq_complete_graph(self):
        assert seidel_neg_count() + seidel_pos_count() == V * (V - 1) // 2

    def test_seidel_trivial_eq_mult_s(self):
        assert seidel_trivial_eq_mult_s() is True

    def test_seidel_trivial_eq_15(self):
        assert seidel_eig_trivial() == MULT_S

    def test_seidel_r_eq_neg_mu_plus_1(self):
        assert seidel_r_eq_neg_mu_plus_1() is True

    def test_seidel_r_eq_neg5(self):
        assert seidel_eig_r() == -(MU + 1)

    def test_seidel_s_eq_k_minus_mu_minus_1(self):
        assert seidel_s_eq_k_minus_mu_minus_1() is True

    def test_seidel_s_eq_7(self):
        assert seidel_eig_s() == K - MU - 1


class TestSpectralCutBounds:
    def test_max_cut_spectral_upper(self):
        assert max_cut_spectral_upper() == TRIANGLES

    def test_max_cut_spectral_upper_is_160(self):
        assert max_cut_spectral_upper() == 160

    def test_max_cut_independence_lb(self):
        assert max_cut_independence_lb() == EDGES // 2

    def test_max_cut_independence_lb_is_120(self):
        assert max_cut_independence_lb() == 120

    def test_frustration_lb_all_neg(self):
        assert frustration_lb_all_neg() == 80

    def test_frustration_lb_eq_edges_minus_max_cut(self):
        assert frustration_lb_all_neg() == EDGES - max_cut_spectral_upper()

    def test_frustration_lb_equals_v_times_lam(self):
        assert frustration_lb_equals_v_times_lam() is True

    def test_frustration_lb_is_v_times_lam(self):
        assert frustration_lb_all_neg() == V * LAM

    def test_seidel_eigenvalue_multiplicities_sum(self):
        assert seidel_eigenvalue_multiplicities_sum() == V

    def test_seidel_eigenvalue_multiplicities_sum_is_40(self):
        assert seidel_eigenvalue_multiplicities_sum() == 40

    def test_seidel_signed_complete_not_balanced(self):
        assert seidel_signed_complete_balanced() is False


class TestSMCrosswalk:
    def test_sm_crosswalk_returns_dict(self):
        cw = sm_crosswalk()
        assert isinstance(cw, dict)

    def test_sm_crosswalk_has_seidel_energy(self):
        cw = sm_crosswalk()
        assert "seidel_energy_eq_edges" in cw

    def test_sm_crosswalk_has_seidel_trivial(self):
        cw = sm_crosswalk()
        assert "seidel_trivial_eq_SU5_matter" in cw

    def test_sm_crosswalk_has_cycle_generations(self):
        cw = sm_crosswalk()
        assert "cycle_space_201_generations" in cw

    def test_sm_crosswalk_7_keys(self):
        cw = sm_crosswalk()
        assert len(cw) == 7


class TestBuildSummary:
    def test_build_returns_pass(self):
        s = build_cccc_summary()
        assert s["status"] == "PASS"

    def test_build_checks_pass_27(self):
        s = build_cccc_summary()
        assert s["checks_pass"] == 27

    def test_build_checks_total_27(self):
        s = build_cccc_summary()
        assert s["checks_total"] == 27

    def test_build_part_cccc(self):
        s = build_cccc_summary()
        assert s["part"] == "CCCC"

    def test_build_discoveries_nonempty(self):
        s = build_cccc_summary()
        assert len(s["discoveries"]) >= 5

    def test_json_written(self):
        import pathlib
        s = build_cccc_summary()
        root = pathlib.Path(__file__).resolve().parents[1]
        p = root / "PART_CCCC_SIGNED_GRAPH_BALANCE_results.json"
        assert p.exists()
