"""
Tests for PART CCCXCIX — Tutte Polynomial, Spanning Trees, and Laplacian-Chromatic Crosswalk
"""

import pytest
from fractions import Fraction
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCXCIX_TUTTE_BRIDGE import (
    V, K, LAM, MU, EDGES, MULT_R, MULT_S, R_EIG, S_EIG, ABS_S,
    TRIANGLES, ALPHA, OMEGA, q,
    laplacian_eig1, laplacian_eig2, laplacian_eigs,
    cycle_space_dim, cocycle_space_dim,
    spanning_tree_count, span_tree_prime_factorization,
    tutte_1_1, tutte_2_2,
    chromatic_poly_is_zero_at, chromatic_number, fractional_chromatic,
    hoffman_bound, nowhere_zero_2flow_exists,
    laplacian_product, alpha_times_mu_squared, triangles_from_srg,
    sm_crosswalk, verify_all, build_cccxcix_summary,
)


# ---------------------------------------------------------------------------
# TestVerifyAll
# ---------------------------------------------------------------------------

class TestVerifyAll:
    def test_all_checks_pass(self):
        checks, passed, total = verify_all()
        assert passed == total

    def test_total_is_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_no_failed_checks(self):
        checks, passed, total = verify_all()
        failed = [name for name, result in checks if not result]
        assert failed == [], f"Failed: {failed}"


# ---------------------------------------------------------------------------
# TestConstants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_EDGES(self):
        assert EDGES == 240

    def test_MULT_R(self):
        assert MULT_R == 24

    def test_MULT_S(self):
        assert MULT_S == 15

    def test_R_EIG(self):
        assert R_EIG == 2

    def test_S_EIG(self):
        assert S_EIG == -4

    def test_ABS_S(self):
        assert ABS_S == 4

    def test_ALPHA(self):
        assert ALPHA == 10

    def test_OMEGA(self):
        assert OMEGA == 4

    def test_q(self):
        assert q == 3

    def test_TRIANGLES(self):
        assert TRIANGLES == 160

    def test_multiplicity_sum(self):
        assert 1 + MULT_R + MULT_S == V


# ---------------------------------------------------------------------------
# TestLaplacianEigenvalues
# ---------------------------------------------------------------------------

class TestLaplacianEigenvalues:
    def test_eig1_value(self):
        assert laplacian_eig1() == 10

    def test_eig2_value(self):
        assert laplacian_eig2() == 16

    def test_eigs_tuple(self):
        assert laplacian_eigs() == (10, 16)

    def test_eig1_equals_alpha(self):
        """Fiedler value = independence number."""
        assert laplacian_eig1() == ALPHA

    def test_eig2_equals_mu_squared(self):
        """Second Laplacian eigenvalue = μ²."""
        assert laplacian_eig2() == MU ** 2

    def test_eig1_formula(self):
        assert laplacian_eig1() == K - R_EIG

    def test_eig2_formula(self):
        assert laplacian_eig2() == K - S_EIG

    def test_both_positive(self):
        assert laplacian_eig1() > 0
        assert laplacian_eig2() > 0

    def test_eig1_less_than_eig2(self):
        assert laplacian_eig1() < laplacian_eig2()


# ---------------------------------------------------------------------------
# TestCycleSpaces
# ---------------------------------------------------------------------------

class TestCycleSpaces:
    def test_cycle_space_dim(self):
        assert cycle_space_dim() == 201

    def test_cocycle_space_dim(self):
        assert cocycle_space_dim() == 39

    def test_cycle_plus_cocycle(self):
        assert cycle_space_dim() + cocycle_space_dim() == EDGES

    def test_201_factors(self):
        assert cycle_space_dim() == 3 * 67

    def test_cocycle_is_v_minus_1(self):
        assert cocycle_space_dim() == V - 1


# ---------------------------------------------------------------------------
# TestSpanningTreeCount
# ---------------------------------------------------------------------------

class TestSpanningTreeCount:
    def test_numerator_divisible(self):
        assert (10 ** 24 * 16 ** 15) % V == 0

    def test_tau_value(self):
        tau = spanning_tree_count()
        assert tau == 2 ** 81 * 5 ** 23

    def test_tau_positive(self):
        assert spanning_tree_count() > 0

    def test_prime_factorization_2_exponent(self):
        a, b, exact = span_tree_prime_factorization()
        assert a == 81

    def test_prime_factorization_5_exponent(self):
        a, b, exact = span_tree_prime_factorization()
        assert b == 23

    def test_prime_factorization_exact(self):
        a, b, exact = span_tree_prime_factorization()
        assert exact is True

    def test_2_exponent_eq_q4(self):
        a, _, _ = span_tree_prime_factorization()
        assert a == q ** 4

    def test_5_exponent_eq_mult_r_minus_1(self):
        _, b, _ = span_tree_prime_factorization()
        assert b == MULT_R - 1

    def test_q4_equals_81(self):
        assert q ** 4 == 81

    def test_mult_r_minus_1_equals_23(self):
        assert MULT_R - 1 == 23


# ---------------------------------------------------------------------------
# TestTutteEvaluations
# ---------------------------------------------------------------------------

class TestTutteEvaluations:
    def test_tutte_1_1_eq_tau(self):
        assert tutte_1_1() == spanning_tree_count()

    def test_tutte_1_1_value(self):
        assert tutte_1_1() == 2 ** 81 * 5 ** 23

    def test_tutte_2_2_eq_2_to_E(self):
        assert tutte_2_2() == 2 ** EDGES

    def test_tutte_2_2_eq_2_to_240(self):
        assert tutte_2_2() == 2 ** 240


# ---------------------------------------------------------------------------
# TestChromaticPolynomial
# ---------------------------------------------------------------------------

class TestChromaticPolynomial:
    def test_P_0_is_zero(self):
        assert chromatic_poly_is_zero_at(0)

    def test_P_1_is_zero(self):
        assert chromatic_poly_is_zero_at(1)

    def test_P_2_is_zero(self):
        assert chromatic_poly_is_zero_at(2)

    def test_P_3_is_zero(self):
        assert chromatic_poly_is_zero_at(3)

    def test_P_4_nonzero(self):
        assert not chromatic_poly_is_zero_at(4)

    def test_P_5_nonzero(self):
        assert not chromatic_poly_is_zero_at(5)

    def test_chi(self):
        assert chromatic_number() == 4

    def test_chi_eq_omega(self):
        assert chromatic_number() == OMEGA

    def test_fractional_chromatic(self):
        assert fractional_chromatic() == Fraction(4)

    def test_chi_f_eq_chi(self):
        assert fractional_chromatic() == chromatic_number()

    def test_chi_f_formula(self):
        assert fractional_chromatic() == Fraction(V, ALPHA)


# ---------------------------------------------------------------------------
# TestHoffmanBound
# ---------------------------------------------------------------------------

class TestHoffmanBound:
    def test_hoffman_bound_value(self):
        assert hoffman_bound() == Fraction(10)

    def test_hoffman_bound_equals_alpha(self):
        assert hoffman_bound() == ALPHA

    def test_hoffman_formula(self):
        assert hoffman_bound() == Fraction(V * ABS_S, K + ABS_S)

    def test_hoffman_equality_form(self):
        """α·(K+|S|) = V·|S|"""
        assert ALPHA * (K + ABS_S) == V * ABS_S


# ---------------------------------------------------------------------------
# TestProductIdentity
# ---------------------------------------------------------------------------

class TestProductIdentity:
    def test_laplacian_product(self):
        assert laplacian_product() == 160

    def test_laplacian_product_eq_triangles(self):
        assert laplacian_product() == TRIANGLES

    def test_alpha_mu2(self):
        assert alpha_times_mu_squared() == 160

    def test_alpha_mu2_eq_triangles(self):
        assert alpha_times_mu_squared() == TRIANGLES

    def test_laplacian_product_eq_alpha_mu2(self):
        assert laplacian_product() == alpha_times_mu_squared()

    def test_triangles_from_srg(self):
        assert triangles_from_srg() == 160

    def test_triangles_from_srg_eq_triangles(self):
        assert triangles_from_srg() == TRIANGLES


# ---------------------------------------------------------------------------
# TestFlowAndEulerian
# ---------------------------------------------------------------------------

class TestFlowAndEulerian:
    def test_k_is_even(self):
        assert K % 2 == 0

    def test_nowhere_zero_2flow_exists(self):
        assert nowhere_zero_2flow_exists()


# ---------------------------------------------------------------------------
# TestSMCrosswalk
# ---------------------------------------------------------------------------

class TestSMCrosswalk:
    def setup_method(self):
        self.cw = sm_crosswalk()

    def test_part(self):
        assert self.cw["part"] == "CCCXCIX"

    def test_tau_2_exp(self):
        assert self.cw["tau_2_exp"] == 81

    def test_tau_5_exp(self):
        assert self.cw["tau_5_exp"] == 23

    def test_q_4(self):
        assert self.cw["q_4"] == 81

    def test_MULT_R_minus_1(self):
        assert self.cw["MULT_R_minus_1"] == 23

    def test_tau_2exp_eq_q4(self):
        assert self.cw["tau_2exp_eq_q4"] is True

    def test_tau_5exp_eq_MR_minus1(self):
        assert self.cw["tau_5exp_eq_MR_minus1"] is True

    def test_tau_exact(self):
        assert self.cw["tau_exact_2_5"] is True

    def test_lap_eig1_eq_alpha(self):
        assert self.cw["lap_eig1_eq_alpha"] is True

    def test_lap_eig2_eq_mu2(self):
        assert self.cw["lap_eig2_eq_mu2"] is True

    def test_lap_product_eq_triangles(self):
        assert self.cw["lap_product_eq_triangles"] is True

    def test_alpha_mu2_eq_triangles(self):
        assert self.cw["alpha_mu2_eq_triangles"] is True

    def test_hoffman_tight(self):
        assert self.cw["hoffman_tight"] is True

    def test_chi_eq_omega(self):
        assert self.cw["chi_eq_omega"] is True

    def test_chi_f_eq_chi(self):
        assert self.cw["chi_f_eq_chi"] is True

    def test_nowhere_zero_2flow(self):
        assert self.cw["nowhere_zero_2flow"] is True


# ---------------------------------------------------------------------------
# TestBuildSummary
# ---------------------------------------------------------------------------

class TestBuildSummary:
    def setup_method(self):
        self.s = build_cccxcix_summary()

    def test_part(self):
        assert self.s["part"] == "CCCXCIX"

    def test_status_pass(self):
        assert self.s["status"] == "PASS"

    def test_checks_pass(self):
        assert self.s["checks_pass"] == 27

    def test_checks_total(self):
        assert self.s["checks_total"] == 27

    def test_no_failed(self):
        assert self.s["failed_checks"] == []

    def test_discoveries_nonempty(self):
        assert len(self.s["discoveries"]) >= 7

    def test_tau_field(self):
        tau = spanning_tree_count()
        assert self.s["fields"]["tau"] == str(tau)

    def test_lap_product_eq_triangles_in_fields(self):
        assert self.s["fields"]["lap_product_eq_triangles"] is True
