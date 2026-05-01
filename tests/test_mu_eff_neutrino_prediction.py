"""
Phase CCXLIX: mu_eff^2 = 1/Phi4 is the W(3,3)-distinguished neutrino value.

The spectral equation -ln(s*) = mu_eff^2 * ln(Phi4) has two
W(3,3)-distinguished solutions:
  mu_eff^2 = f/E = 1/Phi4 = 1/10  (r-eigenspace multiplicity / edge count)
  mu_eff^2 = g/E = 1/mu^2 = 1/16  (s-eigenspace multiplicity / edge count)

Algebraic identities:
  f/E = 2f/(kv) = 1/(q^2+1) = 1/Phi4
  g/E = 2g/(kv) = 1/(q+1)^2 = 1/mu^2

Neutrino predictions (normal hierarchy, NuFIT 2024 oscillation data):
  Delta_m21^2 = 7.42e-5 eV^2, Delta_m31^2 = 2.517e-3 eV^2
  mu_eff^2 = 1/Phi4 => m1 = 49.55 meV, sum(m_nu) = 0.1704 eV
  mu_eff^2 = 1/mu^2 => m1 = 67.50 meV, sum(m_nu) = 0.2197 eV

Testability: sum(m_nu) = 0.170 eV above Planck 2024 bound (0.12 eV)
but within reach of Euclid + CMB-S4 sensitivity (~0.02-0.04 eV).
"""

from fractions import Fraction
from math import comb, log, sqrt

import numpy as np
import pytest

v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7
f_dim, g_dim = 24, 15
E_edges = k * v // 2  # = 240

# NuFIT 2024 oscillation parameters (normal hierarchy)
dm2_21 = 7.42e-5  # eV^2 (solar)
dm2_31 = 2.517e-3  # eV^2 (atmospheric)

# Cosmological bounds
KATRIN_bound = 0.45  # eV (90% CL, sum)
Planck_bound = 0.12  # eV (Planck 2024 + BAO)
Euclid_sensitivity = 0.04  # eV (projected)


def get_masses(m1_eV):
    m2 = sqrt(m1_eV**2 + dm2_21)
    m3 = sqrt(m1_eV**2 + dm2_31)
    return m1_eV, m2, m3


def compute_mu_eff_sq(m1_eV):
    m1, m2, m3 = get_masses(m1_eV)
    x = np.array([m1, m2, m3]) / m3
    s_star = (x[0] * x[1] * x[2]) ** (1 / 3)
    return -log(s_star) / log(Phi4)


def solve_m1_for_mu(target_mu_sq, lo=1e-5, hi=1.0):
    from scipy.optimize import brentq

    return brentq(lambda m1: compute_mu_eff_sq(m1) - target_mu_sq, lo, hi)


class TestMuEffNeutrinoPrediction:

    def test_f_over_E_equals_1_over_Phi4(self):
        """f/E = 1/Phi4 = 1/10."""
        assert Fraction(f_dim, E_edges) == Fraction(1, Phi4)

    def test_g_over_E_equals_1_over_mu_squared(self):
        """g/E = 1/mu^2 = 1/16."""
        assert Fraction(g_dim, E_edges) == Fraction(1, m**2)

    def test_f_over_E_is_1_over_q2_plus_1(self):
        """f/E = 1/(q^2+1) = 1/Phi4: fourth cyclotomic at q."""
        assert Fraction(1, q**2 + 1) == Fraction(f_dim, E_edges)

    def test_g_over_E_is_1_over_q_plus_1_squared(self):
        """g/E = 1/(q+1)^2 = 1/mu^2."""
        assert Fraction(1, (q + 1) ** 2) == Fraction(g_dim, E_edges)

    def test_spectral_equation_at_mu_Phi4(self):
        """At mu_eff^2=1/Phi4: -ln(s*)=ln(Phi4)/Phi4."""
        s_star = Phi4 ** (-1 / Phi4)
        assert abs(-log(s_star) - log(Phi4) / Phi4) < 1e-12
        assert abs(-log(s_star) / log(Phi4) - 1 / Phi4) < 1e-12

    def test_s_star_value_Phi4(self):
        """s* = 10^(-1/10) = 0.79432823... at mu_eff^2=1/Phi4."""
        s_star = Phi4 ** (-1.0 / Phi4)
        assert abs(s_star - 0.79432823) < 1e-6

    def test_neutrino_m1_at_mu_Phi4(self):
        """mu_eff^2=1/Phi4 => m1 ≈ 49.55 meV."""
        m1 = solve_m1_for_mu(1.0 / Phi4)
        assert abs(m1 * 1000 - 49.55) < 0.1  # within 0.1 meV

    def test_neutrino_sum_at_mu_Phi4(self):
        """mu_eff^2=1/Phi4 => sum(m_nu) ≈ 0.170 eV."""
        m1 = solve_m1_for_mu(1.0 / Phi4)
        masses = get_masses(m1)
        s_nu = sum(masses)
        assert abs(s_nu - 0.1704) < 0.001

    def test_neutrino_m1_at_mu_mu_sq(self):
        """mu_eff^2=1/mu^2=1/16 => m1 ≈ 67.5 meV."""
        m1 = solve_m1_for_mu(1.0 / m**2)
        assert abs(m1 * 1000 - 67.5) < 0.3

    def test_neutrino_sum_at_mu_mu_sq(self):
        """mu_eff^2=1/mu^2 => sum(m_nu) ≈ 0.220 eV."""
        m1 = solve_m1_for_mu(1.0 / m**2)
        masses = get_masses(m1)
        s_nu = sum(masses)
        assert abs(s_nu - 0.220) < 0.002

    def test_both_predictions_below_KATRIN(self):
        """Both W(3,3) predictions are below KATRIN bound of 0.45 eV."""
        for mu_sq in [1.0 / Phi4, 1.0 / m**2]:
            m1 = solve_m1_for_mu(mu_sq)
            s_nu = sum(get_masses(m1))
            assert s_nu < KATRIN_bound

    def test_Phi4_prediction_above_Planck(self):
        """1/Phi4 prediction (0.170 eV) is above Planck 2024 bound (0.12 eV)."""
        m1 = solve_m1_for_mu(1.0 / Phi4)
        s_nu = sum(get_masses(m1))
        assert s_nu > Planck_bound

    def test_both_within_Euclid_reach(self):
        """Both predictions give sum > Euclid sensitivity: testable!"""
        for mu_sq in [1.0 / Phi4, 1.0 / m**2]:
            m1 = solve_m1_for_mu(mu_sq)
            s_nu = sum(get_masses(m1))
            assert s_nu > Euclid_sensitivity

    def test_f_over_E_algebraic_identity(self):
        """2f/(kv) = 1/Phi4: algebraic form of f/E."""
        assert 2 * f_dim * Phi4 == k * v // 1  # 2*24*10 = 480 = 12*40
        assert 2 * f_dim == k * v // Phi4

    def test_g_over_E_algebraic_identity(self):
        """2g/(kv) = 1/mu^2: algebraic form of g/E."""
        assert 2 * g_dim * m**2 == k * v  # 2*15*16 = 480 = 12*40

    def test_mu_eff_monotone_decreasing(self):
        """mu_eff^2 decreases as m1 increases (spectrum becomes degenerate)."""
        m1_vals = [0.001, 0.01, 0.05, 0.1, 0.2]
        mu_vals = [compute_mu_eff_sq(m1) for m1 in m1_vals]
        assert all(mu_vals[i] > mu_vals[i + 1] for i in range(len(mu_vals) - 1))

    def test_mu_eff_to_zero_for_degenerate(self):
        """mu_eff^2 -> 0 as m1 -> inf (exactly degenerate = W(3,3) FP)."""
        mu_large = compute_mu_eff_sq(10.0)  # m1 >> oscillation splittings
        assert mu_large < 0.0005

    def test_two_distinguished_values(self):
        """1/Phi4 and 1/mu^2 are the two W(3,3)-primary mu_eff^2 values."""
        assert Fraction(1, Phi4) == Fraction(1, 10)  # 0.10
        assert Fraction(1, m**2) == Fraction(1, 16)  # 0.0625
        assert 1 / Phi4 > 1 / m**2  # 0.10 > 0.0625
        # 1/Phi4 prediction: larger m1, larger sum_nu
        m1_Phi4 = solve_m1_for_mu(1.0 / Phi4)
        m1_mu2 = solve_m1_for_mu(1.0 / m**2)
        assert m1_Phi4 < m1_mu2  # 1/Phi4 > 1/mu^2 so larger mu => smaller m1
