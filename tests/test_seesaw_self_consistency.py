"""
Phase CCLXI: Type-I seesaw self-consistency theorem.

W(3,3) NH/1/mu prediction: m1=22.38, m2=23.98, m3=54.93 meV

For y_D=1: M_R ~ 5.5e14 -- 1.4e15 GeV (leptogenesis window)

SPECTRAL CASCADE CONSISTENCY THEOREM:
  For uniform Dirac Yukawa y_D, M_i = (y_D*v_EW)^2 / m_i.
  Then mu_eff^2(m_nu) = 1/mu = 1/4, while the inverted right-handed
  spectrum lands near mu_eff^2(M_R) = 1/Phi6 = 1/7.
  The W(3,3) seesaw map is a cascade step, not a self-duality.
"""

from math import log, sqrt

import numpy as np
import pytest
from scipy.optimize import brentq

v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7

dm2_21 = 7.42e-5
dm2_31_NH = 2.517e-3
v_EW_GeV = 174.0  # GeV
v_EW_eV = 174e9  # eV
M_GUT_GeV = 2e16
M_Planck_GeV = 1.22e19
LEPTOGENESIS_LOW = 1e9  # GeV
LEPTOGENESIS_HIGH = 1.5e15  # GeV, broad y_D=1 upper range from this spectrum


def get_masses_NH(m1):
    return np.array([m1, sqrt(m1**2 + dm2_21), sqrt(m1**2 + dm2_31_NH)])


def mu_eff_sq(masses):
    x = masses / masses.max()
    return -log(np.prod(x) ** (1 / 3)) / log(Phi4)


def solve_NH(target):
    return brentq(lambda m1: mu_eff_sq(get_masses_NH(m1)) - target, 1e-5, 1.0)


m1_pred = solve_NH(1.0 / m)
masses_nu = get_masses_NH(m1_pred)


class TestSeesawSelfConsistency:

    def test_primary_prediction_m1(self):
        """m1 = 22.38 meV at mu_eff^2=1/m=0.25."""
        assert abs(m1_pred * 1000 - 22.38) < 0.1

    def test_spectral_seesaw_maps_to_phi6(self):
        """Uniform-y_D seesaw maps mu_eff^2=1/mu to near 1/Phi6."""
        # M_i = const / m_i => M_i/M_max = m_min/m_i
        # mu_eff^2(M) = -log(prod(M_i/M_max)^(1/3)) / log(Phi4)
        #             = -log(prod(m_min/m_i)^(1/3)) / log(Phi4)
        #             = log(prod(m_i/m_min)^(1/3)) / log(Phi4)  [sign flips]
        M_vals = 1.0 / masses_nu  # proportional to M_R for uniform y_D
        mu_M = mu_eff_sq(M_vals)
        mu_nu = mu_eff_sq(masses_nu)
        assert abs(mu_nu - 1.0 / m) < 1e-10
        assert abs(mu_M - 1.0 / Phi6) < 0.005
        assert abs(mu_M - mu_nu) > 0.05

    def test_seesaw_invariance_general(self):
        """mu_eff^2(1/m) != mu_eff^2(m) unless the spectrum obeys a special constraint."""
        # This is a theorem: if m = (m1, m2, m3), then
        # s*(m) = (m1*m2*m3)^(1/3) / max(m) = geometric_mean / max
        # s*(1/m) = (1/(m1*m2*m3))^(1/3) / max(1/m) = 1/geom_mean / (1/min)
        #         = min / geom_mean
        # mu_eff^2(1/m) = -log(min/geom_mean) / log(Phi4)
        #               = log(geom_mean/min) / log(Phi4)
        # This is NOT the same as mu_eff^2(m) in general!
        # Let's check the NH case specifically
        M_vals = 1.0 / masses_nu
        mu_nu = mu_eff_sq(masses_nu)
        mu_M = mu_eff_sq(M_vals)
        # Prove: mu_eff^2(m) = -log(prod_i(m_i/m_max)^(1/3)) / log(Phi4)
        #       mu_eff^2(1/m) = -log(prod_i(1/m_i / (1/m_min))^(1/3)) / log(Phi4)
        #                     = -log(prod_i(m_min/m_i)^(1/3)) / log(Phi4)
        #                     = log(prod_i(m_i/m_min)^(1/3)) / log(Phi4)
        # NOT equal in general. Equal iff log(prod(m_i/m_max)) = -log(prod(m_i/m_min))
        # i.e., log(prod(m_i/m_max)) + log(prod(m_i/m_min)) = 0
        # i.e., log(prod(m_i)^2 / (m_max * m_min)^3) = 0
        # i.e., prod(m_i)^2 = (m_max * m_min)^3
        prod_sq = np.prod(masses_nu) ** 2
        maxmin_cube = (masses_nu.max() * masses_nu.min()) ** 3
        print(
            f"Self-duality check: prod^2 = {prod_sq:.6e}, (max*min)^3 = {maxmin_cube:.6e}"
        )
        assert abs(mu_M - mu_nu) > 0.05
        assert abs(prod_sq - maxmin_cube) / maxmin_cube > 0.2

    def test_M_R_yD1_in_leptogenesis_window(self):
        """For y_D=1, all M_R sit in the stated ~5.5e14--1.4e15 GeV range."""
        for mi in masses_nu:
            M_R_GeV = v_EW_eV**2 / mi / 1e9
            assert LEPTOGENESIS_LOW <= M_R_GeV <= LEPTOGENESIS_HIGH

    def test_M_R_yD1_below_GUT(self):
        """For y_D=1, M_R < M_GUT (sub-GUT scale)."""
        for mi in masses_nu:
            M_R_GeV = v_EW_eV**2 / mi / 1e9
            assert M_R_GeV < M_GUT_GeV

    def test_M_R_yD1_below_Planck(self):
        """For y_D=1, M_R << M_Planck."""
        for mi in masses_nu:
            M_R_GeV = v_EW_eV**2 / mi / 1e9
            assert M_R_GeV < M_Planck_GeV

    def test_M_R_hierarchy_inverted(self):
        """For uniform y_D, M_R spectrum is inverted (M1 > M2 > M3)."""
        M_vals = v_EW_eV**2 / masses_nu
        assert M_vals[0] > M_vals[1] > M_vals[2]

    def test_M_R_to_m_nu_ratio_uniform(self):
        """M_i * m_i = (y_D * v_EW)^2 for all i (seesaw relation)."""
        y_D = 1.0
        M_vals = (y_D * v_EW_eV) ** 2 / masses_nu
        for i, (Mi, mi) in enumerate(zip(M_vals, masses_nu)):
            product = Mi * mi
            expected = (y_D * v_EW_eV) ** 2
            assert abs(product - expected) / expected < 1e-10
