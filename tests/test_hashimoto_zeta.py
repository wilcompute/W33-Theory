"""
Phase CCLI: Hashimoto-Ihara zeta function of W(3,3).

zeta_{W(3,3)}(u)^{-1} = (1-u^2)^200 * p0(u)^1 * p1(u)^24 * p2(u)^15
  p0(u) = 1 - 12u + 11u^2   [trivial eigenvalue k=12]
  p1(u) = 1 - 2u  + 11u^2   [r-eigenvalue r=2, sqrt(Phi4) in poles]
  p2(u) = 1 + 4u  + 11u^2   [s-eigenvalue s=-4, sqrt(Phi6) in poles]

Key results:
  - W(3,3) IS a Ramanujan graph: |r|,|s| <= 2*sqrt(k-1)
  - Graph Riemann Hypothesis holds: all nontrivial poles on |u|=1/sqrt(k-1)
  - Poles of p1: (1 ± i*sqrt(Phi4))/11 = (1 ± i*sqrt(10))/(k-1)
  - Poles of p2: (-2 ± i*sqrt(Phi6))/11 = (2 ± i*sqrt(7))/(k-1) (negated)
  - Spectral gap: Delta = r-s = 6 = k/lambda = s_param
"""

from math import sqrt

import numpy as np
import pytest
from sympy import Abs, Rational, Symbol, roots, simplify
from sympy import sqrt as ssqrt

v, k, l, m, q = 40, 12, 2, 4, 3
Phi3, Phi4, Phi6 = 13, 10, 7
f_dim, g_dim = 24, 15
E_edges = 240
ev_r, ev_s = 2, -4
s_param = k // l  # = 6

u = Symbol("u")
p0 = 1 - k * u + (k - 1) * u**2
p1 = 1 - ev_r * u + (k - 1) * u**2
p2 = 1 - ev_s * u + (k - 1) * u**2


class TestHashimotoZeta:

    def test_p0_roots(self):
        """p0 has roots u=1 and u=1/(k-1)=1/11."""
        r0 = sorted([float(x) for x in roots(p0, u).keys()])
        assert abs(r0[0] - 1 / 11) < 1e-10
        assert abs(r0[1] - 1.0) < 1e-10

    def test_p1_poles_contain_sqrt_Phi4(self):
        """p1 poles: (1 ± i*sqrt(Phi4))/(k-1)."""
        # p1 = (k-1)u^2 - r*u + 1 = 11u^2 - 2u + 1
        # roots: u = (2 ± sqrt(4-44))/22 = (1 ± i*sqrt(10))/11
        disc = ev_r**2 - 4 * (k - 1)
        assert disc == 4 - 44 == -40
        assert -disc == 40 == 4 * Phi4
        sqrt_val_sq = -disc // 4  # = 10 = Phi4
        assert sqrt_val_sq == Phi4

    def test_p2_poles_contain_sqrt_Phi6(self):
        """p2 poles: (-2 ± i*sqrt(Phi6))/(k-1)."""
        # p2 = 11u^2 + 4u + 1  (since ev_s = -4, so -ev_s*u = +4u)
        # roots: u = (-4 ± sqrt(16-44))/22 = (-2 ± i*sqrt(7))/11
        disc = ev_s**2 - 4 * (k - 1)  # 16 - 44 = -28
        assert disc == -28
        assert -disc == 28 == 4 * Phi6
        sqrt_val_sq = -disc // 4  # = 7 = Phi6
        assert sqrt_val_sq == Phi6

    def test_p1_pole_modulus(self):
        """|poles of p1| = 1/sqrt(k-1)."""
        # |u|^2 = (1^2 + Phi4) / (k-1)^2 = 11/121 = 1/11
        modulus_sq = (1 + Phi4) / (k - 1) ** 2
        assert abs(modulus_sq - 1 / (k - 1)) < 1e-12
        assert 1 + Phi4 == k - 1  # 1 + 10 = 11 !
        assert 1 + Phi4 == k - 1

    def test_p2_pole_modulus(self):
        """|poles of p2| = 1/sqrt(k-1)."""
        # |u|^2 = (4 + Phi6) / (k-1)^2 = (4+7)/121 = 11/121 = 1/11
        modulus_sq = (4 + Phi6) / (k - 1) ** 2
        assert abs(modulus_sq - 1 / (k - 1)) < 1e-12
        assert 4 + Phi6 == k - 1  # 4 + 7 = 11 !
        # Actually: re-part^2 + im-part^2 = (|s|/2)^2 + Phi6 = 4+7=11 = k-1
        assert (abs(ev_s) // 2) ** 2 + Phi6 == k - 1

    def test_Ramanujan_condition_r(self):
        """|r| <= 2*sqrt(k-1): W(3,3) is Ramanujan."""
        assert abs(ev_r) <= 2 * sqrt(k - 1)

    def test_Ramanujan_condition_s(self):
        """|s| <= 2*sqrt(k-1): W(3,3) is Ramanujan."""
        assert abs(ev_s) <= 2 * sqrt(k - 1)

    def test_graph_RH_holds(self):
        """All nontrivial poles of zeta on |u| = 1/sqrt(k-1)."""
        # Equivalent to Ramanujan condition
        moduli = [
            sqrt((1 + Phi4) / (k - 1) ** 2),  # p1 poles
            sqrt((4 + Phi6) / (k - 1) ** 2),  # p2 poles
        ]
        for mod in moduli:
            assert abs(mod - 1 / sqrt(k - 1)) < 1e-10

    def test_pole_radius_is_1_over_sqrt_Phi3_minus_2(self):
        """Pole radius 1/sqrt(k-1) = 1/sqrt(11) = 1/sqrt(Phi3-2)."""
        assert k - 1 == Phi3 - 2  # 11 = 13 - 2
        assert abs(1 / sqrt(k - 1) - 1 / sqrt(Phi3 - 2)) < 1e-12

    def test_spectral_gap_equals_s_param(self):
        """Spectral gap r-s = 6 = s_param = k/lambda."""
        Delta = ev_r - ev_s
        assert Delta == 6
        assert Delta == s_param
        assert Delta == k // l

    def test_1_plus_Phi4_equals_k_minus_1(self):
        """1 + Phi4 = k-1 = 11: key arithmetic identity for p1 poles."""
        assert 1 + Phi4 == k - 1

    def test_4_plus_Phi6_equals_k_minus_1(self):
        """4 + Phi6 = k-1 = 11: key arithmetic identity for p2 poles."""
        assert 4 + Phi6 == k - 1
        assert (abs(ev_s) // 2) ** 2 + Phi6 == k - 1

    def test_correction_exponent(self):
        """Edge correction exponent E - v = 240 - 40 = 200."""
        assert E_edges - v == 200

    def test_trivial_pole_at_u_1(self):
        """p0 has a pole at u=1 (trivial zero of zeta)."""
        val = 1 - k + (k - 1)  # p0 at u=1
        assert val == 0

    def test_trivial_pole_at_u_1_over_k_minus_1(self):
        """p0 has a pole at u=1/(k-1)=1/11 (trivial zero)."""
        u_val = 1 / (k - 1)
        val = 1 - k * u_val + (k - 1) * u_val**2
        assert abs(val) < 1e-12
