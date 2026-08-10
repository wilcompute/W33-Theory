"""
Tests for PART CCCLVIII: Eigenvalue Interlacing for Induced Subgraphs of W(3,3).
84 tests across 6 classes.
"""

import json
import pathlib
import pytest
from fractions import Fraction

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCLVIII_INTERLACING_BRIDGE import (
    V, K, LAM, MU, EDGES, MULT_R, MULT_S,
    R_EIG, S_EIG, ABS_S,
    ALPHA, GUT_DIM, GENERATIONS, EW_GAUGE_4, SU5_ADJ, SU5_MATTER,
    srg_eigenvalues, eigenvalue_multiplicities,
    trace_check, frobenius_check,
    hoffman_alpha_bound, hoffman_alpha_int,
    clique_bound_fisher,
    nbhd_size, nbhd_edges, nbhd_degree,
    nbhd_eigenvalue_max, nbhd_eigenvalue_min,
    interlacing_lower_nbhd, interlacing_upper_nbhd,
    nonbhd_size, nonbhd_edges, nonbhd_degree,
    nonbhd_eigenvalue_max,
    alpha_times_mu, eigen_product, eigen_sum_eq_lam_minus_mu,
    ratio_bound_product,
    verify_all, build_ccclviii_summary,
)

JSON_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "PART_CCCLVIII_interlacing_results.json"
)


class TestSRGConstants:
    def test_V(self):             assert V == 40
    def test_K(self):             assert K == 12
    def test_R_EIG(self):         assert R_EIG == 2
    def test_S_EIG(self):         assert S_EIG == -4
    def test_ABS_S(self):         assert ABS_S == 4
    def test_MULT_R(self):        assert MULT_R == 24
    def test_MULT_S(self):        assert MULT_S == 15
    def test_mult_sum(self):      assert 1 + MULT_R + MULT_S == V
    def test_eigenvalues(self):   assert srg_eigenvalues() == (12, 2, -4)
    def test_multiplicities(self): assert eigenvalue_multiplicities() == (1, 24, 15)


class TestEigenvalueIdentities:
    def test_trace_zero(self):          assert trace_check() == 0
    def test_frobenius_eq_vk(self):     assert frobenius_check() == V * K
    def test_frobenius_eq_2edges(self): assert frobenius_check() == 2 * EDGES
    def test_r_plus_s_eq_lam_mu(self):  assert eigen_sum_eq_lam_minus_mu()
    def test_r_plus_s_value(self):      assert R_EIG + S_EIG == -2
    def test_r_plus_s_eq_lam_minus_mu_direct(self): assert R_EIG + S_EIG == LAM - MU
    def test_eigen_product_value(self): assert eigen_product() == LAM - MU
    def test_mult_r_eq_su5adj(self):    assert MULT_R == SU5_ADJ
    def test_mult_s_eq_su5matter(self): assert MULT_S == SU5_MATTER


class TestHoffmanAndClique:
    def test_hoffman_fraction(self):     assert hoffman_alpha_bound() == Fraction(V * ABS_S, K + ABS_S)
    def test_hoffman_value(self):        assert hoffman_alpha_bound() == ALPHA
    def test_hoffman_int(self):          assert hoffman_alpha_int() == ALPHA
    def test_hoffman_eq_10(self):        assert hoffman_alpha_int() == 10
    def test_clique_fisher(self):        assert clique_bound_fisher() == 4
    def test_clique_gen_plus_1(self):    assert clique_bound_fisher() == GENERATIONS + 1
    def test_clique_eq_ew4(self):        assert clique_bound_fisher() == EW_GAUGE_4
    def test_alpha_times_mu(self):       assert alpha_times_mu() == V
    def test_alpha_mu_eq_40(self):       assert ALPHA * MU == 40
    def test_alpha_k_s_eq_v_s(self):     assert ALPHA * (K - S_EIG) == V * ABS_S


class TestNeighbourhoodSubgraph:
    def test_nbhd_size(self):            assert nbhd_size() == K
    def test_nbhd_size_val(self):        assert nbhd_size() == 12
    def test_nbhd_edges(self):           assert nbhd_edges() == 12
    def test_nbhd_edges_formula(self):   assert nbhd_edges() == K * LAM // 2
    def test_nbhd_degree(self):          assert nbhd_degree() == LAM
    def test_nbhd_degree_val(self):      assert nbhd_degree() == 2
    def test_nbhd_eig_max(self):         assert nbhd_eigenvalue_max() == LAM
    def test_nbhd_eig_min(self):         assert nbhd_eigenvalue_min() == -LAM
    def test_interlacing_lower(self):    assert interlacing_lower_nbhd()
    def test_interlacing_upper(self):    assert interlacing_upper_nbhd()
    def test_nbhd_min_ge_s(self):        assert nbhd_eigenvalue_min() >= S_EIG
    def test_nbhd_max_le_k(self):        assert nbhd_eigenvalue_max() <= K


class TestNonNeighbourhoodSubgraph:
    def test_nonbhd_size(self):          assert nonbhd_size() == V - K - 1
    def test_nonbhd_size_gut(self):      assert nonbhd_size() == GUT_DIM
    def test_nonbhd_size_val(self):      assert nonbhd_size() == 27
    def test_nonbhd_edges(self):         assert nonbhd_edges() == 108
    def test_nonbhd_edges_formula(self): assert nonbhd_edges() == (V - K - 1) * (K - MU) // 2
    def test_nonbhd_degree(self):        assert nonbhd_degree() == K - MU
    def test_nonbhd_degree_val(self):    assert nonbhd_degree() == 8
    def test_nonbhd_eig_max(self):       assert nonbhd_eigenvalue_max() == K - MU
    def test_nonbhd_eig_max_val(self):   assert nonbhd_eigenvalue_max() == 8
    def test_ratio_product(self):        assert ratio_bound_product() == V * EW_GAUGE_4
    def test_ratio_product_val(self):    assert ratio_bound_product() == 160


class TestVerifyAllAndSummary:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_exactly_27_checks(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_27_pass(self):
        _, passed, total = verify_all()
        assert passed == total == 27

    def test_no_failures(self):
        checks, _, _ = verify_all()
        failed = [c["label"] for c in checks if not c["pass"]]
        assert failed == []

    def test_summary_part(self):
        s = build_ccclviii_summary()
        assert s["part"] == "CCCLVIII"

    def test_summary_status_pass(self):
        s = build_ccclviii_summary()
        assert s["status"] == "PASS"

    def test_summary_checks_pass_27(self):
        s = build_ccclviii_summary()
        assert s["checks_pass"] == 27

    def test_summary_checks_total_27(self):
        s = build_ccclviii_summary()
        assert s["checks_total"] == 27

    def test_summary_hoffman_alpha(self):
        s = build_ccclviii_summary()
        assert s["fields"]["hoffman_alpha"] == ALPHA

    def test_summary_clique_bound(self):
        s = build_ccclviii_summary()
        assert s["fields"]["clique_bound"] == EW_GAUGE_4

    def test_summary_nonbhd_size(self):
        s = build_ccclviii_summary()
        assert s["fields"]["nonbhd_size"] == GUT_DIM

    def test_summary_alpha_times_mu(self):
        s = build_ccclviii_summary()
        assert s["fields"]["alpha_times_mu"] == V

    def test_summary_discoveries_nonempty(self):
        s = build_ccclviii_summary()
        assert len(s["discoveries"]) >= 1

    def test_json_exists(self):
        assert JSON_PATH.exists()

    def test_json_status_pass(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["status"] == "PASS"

    def test_json_checks_pass_27(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["checks_pass"] == 27

    def test_json_part_label(self):
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert data["part"] == "CCCLVIII"
