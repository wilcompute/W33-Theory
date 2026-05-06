"""
Tests for PART CCCLIV — Seidel Matrix and Two-Graphs of W(3,3).

Coverage:
  - SRG constants used by the bridge
  - Seidel matrix entry values
  - Seidel eigenvalues and trace
  - S^2 combinatorial entries
  - Seidel–SRG arithmetic relations
  - Physics connections
  - verify_all() integrity
  - Summary structure
"""

import json, pathlib, sys
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCLIV_SEIDEL_MATRIX_BRIDGE import (
    # constants
    V, K, LAM, MU, EDGES, MULT_R, MULT_S, L,
    R_EIG, S_EIG, ABS_S, ALPHA, EW_GAUGE_4, GENERATIONS,
    GUT_DIM, SU5_ADJ, SU5_MATTER,
    # entry functions
    s_diagonal, s_adj, s_non_adj,
    minus_one_per_row, plus_one_per_row, frobenius_sq,
    # eigenvalue functions
    sigma_trivial, sigma_r, sigma_s, trace_seidel,
    # S^2 functions
    s2_diag, s2_adj, s2_non_adj, s2_eigenvalue_er, s2_eigenvalue_es,
    # arithmetic relations
    sum_sigma_r_sigma_s, abs_sum_sigma, sigma_product_relation,
    sigma_spread, row_sum_s, sigma_trivial_eq_mult_s,
    # physics
    sigma_r_abs_half_alpha, sigma_s_gauge_gen,
    count_minus_one_entries, count_plus_one_entries, spectral_sum_of_squares,
    sigma_r_sq_eq_mult_r_plus_1,
    # harness
    verify_all, build_cccliv_summary,
)


# ── Constants ─────────────────────────────────────────────────────────────────

class TestSRGConstants:
    def test_V(self):             assert V == 40
    def test_K(self):             assert K == 12
    def test_LAM(self):           assert LAM == 2
    def test_MU(self):            assert MU == 4
    def test_EDGES(self):         assert EDGES == 240
    def test_MULT_R(self):        assert MULT_R == 24
    def test_MULT_S(self):        assert MULT_S == 15
    def test_L(self):             assert L == 27
    def test_R_EIG(self):         assert R_EIG == 2
    def test_S_EIG(self):         assert S_EIG == -4
    def test_ABS_S(self):         assert ABS_S == 4
    def test_ALPHA(self):         assert ALPHA == 10
    def test_EW_GAUGE_4(self):    assert EW_GAUGE_4 == 4
    def test_GENERATIONS(self):   assert GENERATIONS == 3
    def test_SU5_ADJ(self):       assert SU5_ADJ == 24
    def test_SU5_MATTER(self):    assert SU5_MATTER == 15
    def test_mult_sum(self):      assert MULT_R + MULT_S + 1 == V
    def test_edges_formula(self): assert EDGES == V * K // 2


# ── Seidel matrix entry values ────────────────────────────────────────────────

class TestSeidelEntries:
    def test_diagonal_zero(self):
        assert s_diagonal() == 0

    def test_adj_minus_one(self):
        assert s_adj() == -1

    def test_non_adj_plus_one(self):
        assert s_non_adj() == 1

    def test_minus_one_per_row(self):
        assert minus_one_per_row() == K

    def test_plus_one_per_row(self):
        assert plus_one_per_row() == V - 1 - K

    def test_minus_plus_per_row_sum(self):
        # -1 entries + +1 entries = V - 1  (total off-diagonal per row)
        assert minus_one_per_row() + plus_one_per_row() == V - 1

    def test_frobenius_sq(self):
        assert frobenius_sq() == V * (V - 1)

    def test_frobenius_sq_value(self):
        assert frobenius_sq() == 1560

    def test_plus_one_per_row_value(self):
        assert plus_one_per_row() == 27

    def test_entry_squared_is_one(self):
        # all off-diagonal entries ±1 → entry^2 = 1
        assert s_adj() ** 2 == 1
        assert s_non_adj() ** 2 == 1

    def test_adj_plus_non_adj_entry(self):
        # sum of the two off-diagonal entry types
        assert s_adj() + s_non_adj() == 0


# ── Seidel eigenvalues ────────────────────────────────────────────────────────

class TestSeidelEigenvalues:
    def test_sigma_trivial_formula(self):
        assert sigma_trivial() == V - 1 - 2 * K

    def test_sigma_trivial_value(self):
        assert sigma_trivial() == 15

    def test_sigma_r_formula(self):
        assert sigma_r() == -1 - 2 * R_EIG

    def test_sigma_r_value(self):
        assert sigma_r() == -5

    def test_sigma_s_formula(self):
        assert sigma_s() == -1 - 2 * S_EIG

    def test_sigma_s_value(self):
        assert sigma_s() == 7

    def test_trace_seidel(self):
        assert trace_seidel() == 0

    def test_trace_decomposition(self):
        assert (1 * sigma_trivial()
                + MULT_R * sigma_r()
                + MULT_S * sigma_s()) == 0

    def test_sigma_r_negative(self):
        assert sigma_r() < 0

    def test_sigma_s_positive(self):
        assert sigma_s() > 0

    def test_sigma_trivial_positive(self):
        assert sigma_trivial() > 0


# ── S^2 entries ───────────────────────────────────────────────────────────────

class TestS2Entries:
    def test_s2_diag(self):
        assert s2_diag() == V - 1

    def test_s2_diag_value(self):
        assert s2_diag() == 39

    def test_s2_adj(self):
        assert s2_adj() == LAM

    def test_s2_adj_value(self):
        assert s2_adj() == 2

    def test_s2_non_adj(self):
        assert s2_non_adj() == LAM + MU

    def test_s2_non_adj_value(self):
        assert s2_non_adj() == 6

    def test_s2_non_adj_greater_adj(self):
        assert s2_non_adj() > s2_adj()

    def test_s2_eigenvalue_er(self):
        assert s2_eigenvalue_er() == sigma_r() ** 2

    def test_s2_eigenvalue_er_value(self):
        assert s2_eigenvalue_er() == 25

    def test_s2_eigenvalue_es(self):
        assert s2_eigenvalue_es() == sigma_s() ** 2

    def test_s2_eigenvalue_es_value(self):
        assert s2_eigenvalue_es() == 49

    def test_s2_eigenvalue_trivial(self):
        # on E_0: S^2 eigenvalue = sigma_trivial^2 = 225
        assert sigma_trivial() ** 2 == 225


# ── Seidel–SRG arithmetic ─────────────────────────────────────────────────────

class TestSeidelSRGArithmetic:
    def test_sum_sigma_r_sigma_s(self):
        assert sum_sigma_r_sigma_s() == LAM

    def test_sum_sigma_r_sigma_s_value(self):
        assert sum_sigma_r_sigma_s() == 2

    def test_abs_sum_sigma(self):
        assert abs_sum_sigma() == K

    def test_abs_sum_sigma_value(self):
        assert abs_sum_sigma() == 12

    def test_sigma_product_relation(self):
        assert sigma_product_relation() == MU

    def test_sigma_product_relation_value(self):
        assert sigma_product_relation() == 4

    def test_sigma_spread(self):
        assert sigma_spread() == K

    def test_sigma_spread_value(self):
        assert sigma_spread() == 12

    def test_row_sum_s(self):
        assert row_sum_s() == sigma_trivial()

    def test_row_sum_s_value(self):
        assert row_sum_s() == 15

    def test_sigma_trivial_eq_mult_s(self):
        assert sigma_trivial_eq_mult_s() == MULT_S

    def test_sigma_trivial_eq_mult_s_value(self):
        assert sigma_trivial_eq_mult_s() == 15


# ── Physics connections ───────────────────────────────────────────────────────

class TestPhysicsConnections:
    def test_sigma_r_abs_half_alpha(self):
        assert sigma_r_abs_half_alpha() == ALPHA // 2

    def test_sigma_r_abs_half_alpha_value(self):
        assert sigma_r_abs_half_alpha() == 5

    def test_sigma_s_gauge_gen(self):
        assert sigma_s_gauge_gen() == EW_GAUGE_4 + GENERATIONS

    def test_sigma_s_gauge_gen_value(self):
        assert sigma_s_gauge_gen() == 7

    def test_count_minus_one(self):
        assert count_minus_one_entries() == 2 * EDGES

    def test_count_minus_one_value(self):
        assert count_minus_one_entries() == 480

    def test_count_plus_one(self):
        assert count_plus_one_entries() == V * (V - 1) - 2 * EDGES

    def test_count_plus_one_value(self):
        assert count_plus_one_entries() == 1080

    def test_count_total(self):
        assert count_minus_one_entries() + count_plus_one_entries() == frobenius_sq()

    def test_spectral_sum_of_squares(self):
        assert spectral_sum_of_squares() == V * (V - 1)

    def test_spectral_sum_of_squares_value(self):
        assert spectral_sum_of_squares() == 1560

    def test_mult_r_eq_su5_adj(self):
        assert MULT_R == SU5_ADJ

    def test_mult_s_eq_su5_matter(self):
        assert MULT_S == SU5_MATTER

    def test_sigma_r_sq_mult_r_plus_1(self):
        # sigma_r^2 = 25 = MULT_R + 1
        assert sigma_r_sq_eq_mult_r_plus_1() == MULT_R + 1


# ── verify_all ────────────────────────────────────────────────────────────────

class TestVerifyAll:
    def test_all_pass(self):
        _, passed, total = verify_all()
        assert passed == total

    def test_exactly_27_checks(self):
        checks, _, total = verify_all()
        assert total == L
        assert len(checks) == L

    def test_each_check_has_keys(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert "name" in c
            assert "got" in c
            assert "expected" in c
            assert "passed" in c

    def test_no_check_fails(self):
        checks, _, _ = verify_all()
        failures = [c["name"] for c in checks if not c["passed"]]
        assert failures == []


# ── Summary ───────────────────────────────────────────────────────────────────

class TestSummary:
    def test_part_label(self):
        s = build_cccliv_summary()
        assert s["part"] == "CCCLIV"

    def test_status_pass(self):
        s = build_cccliv_summary()
        assert s["status"] == "PASS"

    def test_checks_pass(self):
        s = build_cccliv_summary()
        assert s["checks_pass"] == 27

    def test_checks_total(self):
        s = build_cccliv_summary()
        assert s["checks_total"] == 27

    def test_fields_present(self):
        s = build_cccliv_summary()
        for key in ("sigma_trivial", "sigma_r", "sigma_s",
                    "s2_adj", "s2_non_adj", "frobenius_sq"):
            assert key in s["fields"]

    def test_fields_sigma_trivial(self):
        s = build_cccliv_summary()
        assert s["fields"]["sigma_trivial"] == 15

    def test_fields_sigma_r(self):
        s = build_cccliv_summary()
        assert s["fields"]["sigma_r"] == -5

    def test_fields_sigma_s(self):
        s = build_cccliv_summary()
        assert s["fields"]["sigma_s"] == 7

    def test_discoveries_nonempty(self):
        s = build_cccliv_summary()
        assert len(s["discoveries"]) >= 4
