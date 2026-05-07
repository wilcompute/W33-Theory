"""Tests for PART CCCXCVII -- Distance-Regular Algebra and Root System Crosswalk."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))

import pytest
from PART_CCCXCVII_DR_ALGEBRA_BRIDGE import (
    ALPHA,
    ABS_S,
    EDGES,
    EW_GAUGE_4,
    GENERATIONS,
    GUT_DIM,
    K,
    LAM,
    MULT_R,
    MULT_S,
    MU,
    R_EIG,
    S_EIG,
    SU5_ADJ,
    SU5_MATTER,
    V,
    a_params,
    build_cccxcvii_summary,
    char_poly_coeffs,
    eig_quadratic_identities,
    intersection_array,
    second_adjacency_eigenvalues,
    sm_crosswalk,
    sum_all_eigenvalues,
    trace_A_squared,
    verify_all,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
class TestConstants:
    def test_v(self):
        assert V == 40

    def test_k(self):
        assert K == 12

    def test_lam(self):
        assert LAM == 2

    def test_mu(self):
        assert MU == 4

    def test_edges(self):
        assert EDGES == 240

    def test_mult_r(self):
        assert MULT_R == 24

    def test_mult_s(self):
        assert MULT_S == 15

    def test_r_eig(self):
        assert R_EIG == 2

    def test_s_eig(self):
        assert S_EIG == -4

    def test_gut_dim(self):
        assert GUT_DIM == 27


# ---------------------------------------------------------------------------
# Intersection array
# ---------------------------------------------------------------------------
class TestIntersectionArray:
    def test_b0_eq_k(self):
        b0, _, _, _ = intersection_array()
        assert b0 == K

    def test_b1_eq_k_minus_1_minus_lam(self):
        _, b1, _, _ = intersection_array()
        assert b1 == K - 1 - LAM

    def test_b1_value(self):
        _, b1, _, _ = intersection_array()
        assert b1 == 9

    def test_c1_eq_1(self):
        _, _, c1, _ = intersection_array()
        assert c1 == 1

    def test_c2_eq_mu(self):
        _, _, _, c2 = intersection_array()
        assert c2 == MU

    def test_a1_eq_lam(self):
        _, _, _, _ = intersection_array()
        _, a1, _ = a_params()
        assert a1 == LAM

    def test_a2_value(self):
        _, _, a2 = a_params()
        assert a2 == 8


# ---------------------------------------------------------------------------
# Characteristic polynomial
# ---------------------------------------------------------------------------
class TestCharPoly:
    def test_p1(self):
        _, p1, _, _ = char_poly_coeffs()
        assert p1 == -(K + R_EIG + S_EIG)

    def test_p1_value(self):
        _, p1, _, _ = char_poly_coeffs()
        assert p1 == -10

    def test_p2(self):
        _, _, p2, _ = char_poly_coeffs()
        assert p2 == K * R_EIG + K * S_EIG + R_EIG * S_EIG

    def test_p2_value(self):
        _, _, p2, _ = char_poly_coeffs()
        assert p2 == -32

    def test_p3(self):
        _, _, _, p3 = char_poly_coeffs()
        assert p3 == -(K * R_EIG * S_EIG)

    def test_p3_value(self):
        _, _, _, p3 = char_poly_coeffs()
        assert p3 == 96

    def test_trace_A2(self):
        assert trace_A_squared() == 2 * EDGES

    def test_sum_eigs_zero(self):
        assert sum_all_eigenvalues() == 0


# ---------------------------------------------------------------------------
# Second adjacency matrix eigenvalues
# ---------------------------------------------------------------------------
class TestSecondAdjacency:
    def test_ev_k_eq_gut_dim(self):
        ev_k, _, _ = second_adjacency_eigenvalues()
        assert ev_k == GUT_DIM

    def test_ev_k_value(self):
        ev_k, _, _ = second_adjacency_eigenvalues()
        assert ev_k == 27

    def test_ev_r_value(self):
        _, ev_r, _ = second_adjacency_eigenvalues()
        assert ev_r == -3

    def test_ev_s_value(self):
        _, _, ev_s = second_adjacency_eigenvalues()
        assert ev_s == 3

    def test_weighted_sum_zero(self):
        ev_k, ev_r, ev_s = second_adjacency_eigenvalues()
        assert ev_k + MULT_R * ev_r + MULT_S * ev_s == 0

    def test_ev_k_eq_generations_times_b1(self):
        ev_k, _, _ = second_adjacency_eigenvalues()
        _, b1, _, _ = intersection_array()
        assert ev_k == GENERATIONS * b1


# ---------------------------------------------------------------------------
# Eigenvalue quadratic identities
# ---------------------------------------------------------------------------
class TestEigQuadratic:
    def test_r_plus_s_eq_lam_minus_mu(self):
        r_plus_s, _, _ = eig_quadratic_identities()
        assert r_plus_s == LAM - MU

    def test_r_plus_s_value(self):
        r_plus_s, _, _ = eig_quadratic_identities()
        assert r_plus_s == -2

    def test_r_times_s_eq_neg_k_minus_mu(self):
        _, r_times_s, _ = eig_quadratic_identities()
        assert r_times_s == -(K - MU)

    def test_r_times_s_value(self):
        _, r_times_s, _ = eig_quadratic_identities()
        assert r_times_s == -8

    def test_discriminant_36(self):
        _, _, disc = eig_quadratic_identities()
        assert disc == 36

    def test_discriminant_perfect_square(self):
        _, _, disc = eig_quadratic_identities()
        assert disc == 6 ** 2


# ---------------------------------------------------------------------------
# SM crosswalk
# ---------------------------------------------------------------------------
class TestSMCrosswalk:
    def test_alpha(self):
        cw = sm_crosswalk()
        assert cw["alpha"] == ALPHA

    def test_k_minus_r_eq_alpha(self):
        assert K - R_EIG == ALPHA

    def test_k_minus_s_eq_ew4_squared(self):
        assert K - S_EIG == EW_GAUGE_4 ** 2

    def test_alpha_times_k_minus_s_eq_v_mu(self):
        assert (K - R_EIG) * (K - S_EIG) == V * MU

    def test_gut_dim_from_crosswalk(self):
        cw = sm_crosswalk()
        assert cw["gut_dim_from_a2"] == GUT_DIM

    def test_su5_adj(self):
        cw = sm_crosswalk()
        assert cw["su5_adj"] == SU5_ADJ

    def test_su5_matter(self):
        cw = sm_crosswalk()
        assert cw["su5_matter"] == SU5_MATTER

    def test_mult_sum(self):
        cw = sm_crosswalk()
        assert cw["mult_sum"] == V - 1

    def test_mult_total(self):
        cw = sm_crosswalk()
        assert cw["mult_total"] == V


# ---------------------------------------------------------------------------
# verify_all and summary
# ---------------------------------------------------------------------------
class TestVerifyAll:
    def test_all_27_pass(self):
        _, passed, total = verify_all()
        assert passed == total == 27

    def test_summary_status_pass(self):
        summary = build_cccxcvii_summary()
        assert summary["status"] == "PASS"

    def test_summary_checks_pass(self):
        summary = build_cccxcvii_summary()
        assert summary["checks_pass"] == 27

    def test_summary_part(self):
        summary = build_cccxcvii_summary()
        assert summary["part"] == "CCCXCVII"

    def test_discoveries_present(self):
        summary = build_cccxcvii_summary()
        assert len(summary["discoveries"]) >= 5

    def test_intersection_array_field(self):
        summary = build_cccxcvii_summary()
        assert summary["fields"]["intersection_array"] == [12, 9, 1, 4]
