"""Tests for Part MCLVII: Normalized Laplacian and Cheeger Constant for W(3,3)."""
import pytest
from fractions import Fraction
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'analysis'))
from w33_normalized_laplacian import (
    verify_normalized_laplacian,
    cheeger_constant_bounds,
    normalized_spectral_moments,
    normalized_effective_resistance,
    von_neumann_entropy,
    novel_identities,
    normalized_laplacian_main,
    mu_r, mu_s, mu_0, m_mur, m_mus,
)

V, K = 40, 12


class TestNormalizedLaplacianParams:
    def test_eigenvalues(self):
        assert mu_0 == Fraction(0)
        assert mu_r == Fraction(5, 6)
        assert mu_s == Fraction(4, 3)

    def test_eigenvalues_in_range(self):
        assert mu_0 >= 0
        assert mu_r > 0
        assert mu_r < 2
        assert mu_s > 0
        assert mu_s < 2  # Ramanujan-type: largest eigenvalue < 2

    def test_trace(self):
        trace = 1 * mu_0 + m_mur * mu_r + m_mus * mu_s
        assert trace == Fraction(V)  # tr(L_hat) = v for k-regular with tr(A)=0

    def test_verify_params(self):
        assert verify_normalized_laplacian() is True


class TestCheegerBounds:
    def setup_method(self):
        self.res = cheeger_constant_bounds()

    def test_lower_bound(self):
        assert self.res["lower_bound"] == Fraction(5, 12)

    def test_upper_sq(self):
        assert self.res["upper_bound_squared"] == Fraction(5, 3)

    def test_numerical_bounds(self):
        lo = self.res["lower_float"]
        hi = self.res["upper_float"]
        assert 0.41 < lo < 0.42
        assert 1.28 < hi < 1.30

    def test_bounds_ordered(self):
        assert self.res["lower_float"] < self.res["upper_float"]


class TestSpectralMoments:
    def setup_method(self):
        self.m = normalized_spectral_moments()

    def test_M0_equals_v(self):
        assert self.m[0] == Fraction(V)

    def test_M1_equals_v(self):
        # tr(L_hat) = v (since tr(A)=0)
        assert self.m[1] == Fraction(V)

    def test_M2(self):
        # 24*(5/6)^2 + 15*(4/3)^2 = 24*25/36 + 15*16/9 = 50/3 + 80/3 = 130/3
        assert self.m[2] == Fraction(130, 3)

    def test_M3(self):
        # 24*(5/6)^3 + 15*(4/3)^3 = 24*125/216 + 15*64/27 = 125/9 + 320/9 = 445/9
        assert self.m[3] == Fraction(445, 9)


class TestKemenyFromLhat:
    def test_kemeny_from_normalized(self):
        res = normalized_effective_resistance()
        assert res["K_sum_verify"] == Fraction(801, 20)

    def test_kemeny_formula(self):
        # K = m_r/mu_r + m_s/mu_s
        K = Fraction(m_mur, 1) / mu_r + Fraction(m_mus, 1) / mu_s
        assert K == Fraction(801, 20)


class TestVonNeumannEntropy:
    def setup_method(self):
        self.vne = von_neumann_entropy()

    def test_equal_aggregate_split(self):
        assert self.vne["equal_aggregate_split"] is True

    def test_p_r_equals_half(self):
        assert self.vne["p_r_aggregate"] == Fraction(1, 2)

    def test_p_s_equals_half(self):
        assert self.vne["p_s_aggregate"] == Fraction(1, 2)

    def test_p_i_r(self):
        assert self.vne["p_i_r"] == Fraction(1, 48)

    def test_p_i_s(self):
        assert self.vne["p_i_s"] == Fraction(1, 30)

    def test_entropy_positive(self):
        assert self.vne["entropy_numerical"] > 0


class TestNovelIdentities:
    def setup_method(self):
        self.n = novel_identities()

    def test_equal_energy(self):
        assert self.n["equal_energy"] is True
        assert self.n["m_r_mu_r"] == Fraction(20)
        assert self.n["m_s_mu_s"] == Fraction(20)

    def test_spectral_gap(self):
        assert self.n["spectral_gap_lhat"] == Fraction(5, 6)

    def test_mu_product(self):
        assert self.n["mu_r_times_mu_s"] == Fraction(10, 9)

    def test_cheeger_lower(self):
        assert self.n["cheeger_lower"] == Fraction(5, 12)

    def test_sum_sq(self):
        assert self.n["sum_mu_squared"] == Fraction(130, 3)

    def test_kemeny(self):
        assert self.n["kemeny_from_lhat"] == Fraction(801, 20)


class TestFullPacket:
    def test_main_runs(self):
        results = normalized_laplacian_main()
        assert results["n_verified"] == 20
        assert results["novel_identities"]["equal_energy"] == "True"
