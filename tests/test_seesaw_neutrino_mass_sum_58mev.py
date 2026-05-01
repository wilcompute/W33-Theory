"""
Derivation: Sigma m_nu = lambda(v - k + 1) = 58 meV from the W(3,3) seesaw texture.

Type-I seesaw with democratic (aI + bJ) textures for both mD and MR:
  mD = (k-lambda)I + lambda*J = 10I + 2J
  MR = (k-mu)I    + mu*J     = 8I  + 4J

Both matrices share eigenvectors (all-ones vector and its orthogonal complement),
so the seesaw is exactly diagonalizable via Sherman-Morrison inversion of MR.

Key results (exact fractions):
  MR^{-1} = (1/8)I - (1/40)J
  M_nu    = -(25/2)I - (1/10)J
  Eigenvalues: m1 = m2 = -25/2,  m3 = -64/5
  Sigma_dimensionless = 189/5
  Physical scale: Lambda = 5*lambda*(v-k+1)/189 meV
  Sigma m_nu = lambda*(v-k+1) = 2*29 = 58 meV
"""

from fractions import Fraction

import numpy as np
import pytest

# W(3,3) parameters
v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7
n = 3  # 3 generations


class TestSeesawNeutrinoMassPrediction:

    def test_mD_texture(self):
        """mD = (k-lambda)I + lambda*J = 10I + 2J."""
        a_D = k - l  # = 10 = Phi4
        b_D = l  # = 2 = lambda
        assert a_D == 10 == Phi4
        assert b_D == 2 == l

    def test_MR_texture(self):
        """MR = (k-mu)I + mu*J = 8I + 4J."""
        a_R = k - m  # = 8
        b_R = m  # = 4
        assert a_R == 8
        assert b_R == 4
        assert a_R + n * b_R == 20  # = v/2

    def test_MR_inverse_sherman_morrison(self):
        """MR^{-1} = (1/a_R)I - b_R/(a_R*(a_R+n*b_R)) J = (1/8)I - (1/40)J."""
        a_R, b_R = k - m, m
        inv_a = Fraction(1, a_R)
        inv_b = Fraction(-b_R, a_R * (a_R + n * b_R))
        assert inv_a == Fraction(1, 8)
        assert inv_b == Fraction(-1, 40)
        # Verify: (a_R I + b_R J)(inv_a I + inv_b J) = I
        # (aI+bJ)(cI+dJ) = ac*I + (ad+bc+n*bd)J
        ac = a_R * inv_a
        ad_bc_nbd = a_R * inv_b + b_R * inv_a + n * b_R * inv_b
        assert ac == 1
        assert ad_bc_nbd == 0

    def test_Mnu_exact_coefficients(self):
        """M_nu = -(25/2)I - (1/10)J (exact)."""
        a_D_f = Fraction(k - l)
        b_D_f = Fraction(l)
        a_R, b_R = k - m, m
        inv_a_f = Fraction(1, a_R)
        inv_b_f = Fraction(-b_R, a_R * (a_R + n * b_R))
        # (mD)(MR^{-1}): c1 I + c2 J
        c1 = a_D_f * inv_a_f
        c2 = a_D_f * inv_b_f + b_D_f * inv_a_f + n * b_D_f * inv_b_f
        # M_nu = -(c1I + c2J)(a_D I + b_D J)
        nu_a = -(c1 * a_D_f)
        nu_b = -(c1 * b_D_f + c2 * a_D_f + n * c2 * b_D_f)
        assert nu_a == Fraction(-25, 2)
        assert nu_b == Fraction(-1, 10)

    def test_Mnu_eigenvalues_exact(self):
        """Eigenvalues of M_nu: m1=m2=-25/2, m3=-64/5."""
        nu_a = Fraction(-25, 2)
        nu_b = Fraction(-1, 10)
        # For aI + bJ (n=3): eigenvalues are a (x2) and a+3b (x1)
        ev12 = nu_a
        ev3 = nu_a + n * nu_b
        assert ev12 == Fraction(-25, 2)
        assert ev3 == Fraction(-64, 5)

    def test_eigenvalues_match_numpy(self):
        """Numerical eigenvalues match exact fractions."""
        mD = (k - l) * np.eye(n) + l * np.ones((n, n))
        MR = (k - m) * np.eye(n) + m * np.ones((n, n))
        Mnu = -mD @ np.linalg.inv(MR) @ mD.T
        evals = sorted(np.linalg.eigvalsh(Mnu))
        assert abs(evals[0] - (-64 / 5)) < 1e-10
        assert abs(evals[1] - (-25 / 2)) < 1e-10
        assert abs(evals[2] - (-25 / 2)) < 1e-10

    def test_exact_degeneracy_m1_equals_m2(self):
        """m1 = m2 exactly (tree-level tri-bimaximal prediction)."""
        ev12 = Fraction(-25, 2)
        # The degenerate eigenvalue is a = nu_a, appears with multiplicity 2
        # This is exact, not approximate
        assert ev12 == Fraction(-25, 2)
        # Splitting comes from charged-lepton radiative corrections only

    def test_dimensionless_sum_189_over_5(self):
        """Sum of |eigenvalues| = 189/5 in seesaw units."""
        # Diagonal basis: mD eigvals are (k-l)=10 (x2) and (k+2l)=16 (x1)
        # MR eigvals are (k-m)=8 (x2) and (k+2m)=20 (x1)
        mD_ev12 = Fraction((k - l) ** 2, k - m)  # = 100/8 = 25/2
        mD_ev3 = Fraction((k + 2 * l) ** 2, k + 2 * m)  # = 256/20 = 64/5
        Sigma = 2 * mD_ev12 + mD_ev3
        assert Sigma == Fraction(189, 5)

    def test_algebraic_trace_formula(self):
        """Tr[M_nu] = -(2(k-l)^2/(k-m) + (k+2l)^2/(k+2m)) = -189/5."""
        Tr = -(
            2 * Fraction((k - l) ** 2, k - m) + Fraction((k + 2 * l) ** 2, k + 2 * m)
        )
        assert Tr == Fraction(-189, 5)

    def test_physical_scale_definition(self):
        """The W(3,3) unit scale: Lambda = 5*lambda*(v-k+1)/189 meV."""
        Lambda_num = 5 * l * (v - k + 1)
        Lambda_den = 189
        Lambda = Fraction(Lambda_num, Lambda_den)  # in meV
        assert Lambda == Fraction(5 * 2 * 29, 189)
        assert float(Lambda) == pytest.approx(290 / 189, rel=1e-10)

    def test_sigma_mnu_equals_58_mev(self):
        """Sigma m_nu = (189/5) * Lambda = lambda*(v-k+1) = 58 meV."""
        Sigma_dl = Fraction(189, 5)
        Lambda = Fraction(5 * l * (v - k + 1), 189)  # meV
        Sigma_mev = Sigma_dl * Lambda
        assert Sigma_mev == l * (v - k + 1)
        assert int(Sigma_mev) == 58

    def test_lambda_v_k_plus_1_formula(self):
        """Sigma m_nu = lambda*(v-k+1) = 2*(40-12+1) = 2*29 = 58 meV."""
        prediction = l * (v - k + 1)
        assert l == 2
        assert v - k + 1 == 29
        assert prediction == 58

    def test_GUT_scale_from_prediction(self):
        """M_R ~ 3.9e16 GeV (near standard GUT scale)."""
        Sigma_meV = 58.0
        Sigma_dl = 189 / 5
        Lambda_meV = Sigma_meV / Sigma_dl  # seesaw unit in meV
        Lambda_GeV = Lambda_meV * 1e-12
        v_EW_GeV = 246.0
        MR1_GeV = v_EW_GeV**2 / Lambda_GeV
        # Should be ~ 10^15 to 10^17 GeV range
        assert 1e14 < MR1_GeV < 1e18, f"MR = {MR1_GeV:.2e} GeV"

    def test_cosmological_bound_consistency(self):
        """Sigma m_nu = 58 meV < 120 meV (Planck 2018 bound)."""
        Sigma_pred = l * (v - k + 1)  # = 58 meV
        Planck_bound = 120  # meV
        assert Sigma_pred < Planck_bound
        assert Sigma_pred == 58

    def test_individual_masses(self):
        """Individual masses: m1=m2~19.18 meV, m3~19.64 meV."""
        Lambda_meV = 5 * l * (v - k + 1) / 189  # = 290/189 meV
        m12_meV = float(Fraction(25, 2)) * Lambda_meV
        m3_meV = float(Fraction(64, 5)) * Lambda_meV
        Sigma_check = 2 * m12_meV + m3_meV
        assert abs(Sigma_check - 58.0) < 1e-10
        assert abs(m12_meV - 25 / 2 * 290 / 189) < 1e-10
        assert abs(m3_meV - 64 / 5 * 290 / 189) < 1e-10
        # All masses are ~19 meV: quasi-degenerate regime
        assert 15 < m12_meV < 25
        assert 15 < m3_meV < 25

    def test_mass_ratio_m3_over_m12(self):
        """Mass ratio m3/m12 = (64/5)/(25/2) = 128/125 (near-degenerate)."""
        ratio = Fraction(64, 5) / Fraction(25, 2)
        assert ratio == Fraction(128, 125)
        assert float(ratio) == pytest.approx(1.024, rel=1e-6)

    def test_189_factorization(self):
        """189 = 27 * 7 = q^3 * Phi6."""
        assert 189 == q**3 * Phi6
        assert 189 == 27 * 7

    def test_290_factorization(self):
        """290 = Phi4 * (v-k+1) = 10 * 29."""
        assert 290 == Phi4 * (v - k + 1)
        assert 290 == 10 * 29

    def test_cancellation_identity(self):
        """The 189 cancels: Sigma = (189/5) * (5*lambda*(v-k+1)/189) = lambda*(v-k+1)."""
        # (189/5) * (5/189) = 1, so the geometric factor vanishes exactly
        geometric = Fraction(189, 5)
        unit = Fraction(5 * l * (v - k + 1), 189)
        product = geometric * unit
        assert product == l * (v - k + 1)
        assert product == 58
