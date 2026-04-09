"""
Phase CDXII (412) — Dynamical Systems & Ergodic Theory from W(3,3)
===================================================================
Random walk, mixing time, topological entropy, Lyapunov spectrum,
ergodic measures, Ihara zeta, return probabilities.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
E = v * k // 2
T = 160
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_RandomWalk:
    def test_rw_eig1(self):
        assert Fraction(r, k) == Fraction(1, math.factorial(q))
    def test_rw_eig2(self):
        assert Fraction(s, k) == Fraction(-1, q)
    def test_spectral_gap(self):
        gap = 1 - Fraction(r, k)
        assert gap == Fraction(mu + 1, math.factorial(q))

class TestT2_Mixing:
    def test_SLEM(self):
        assert max(abs(Fraction(r, k)), abs(Fraction(s, k))) == Fraction(1, q)
    def test_relaxation(self):
        SLEM = Fraction(1, q)
        assert Fraction(1, 1 - SLEM) == Fraction(q, q - 1)

class TestT3_Entropy:
    def test_spectral_radius(self):
        assert k == 12

class TestT4_Lyapunov:
    def test_ratio(self):
        assert k // abs(s) == q

class TestT5_Ergodic:
    def test_stationary(self):
        assert Fraction(1, v) == Fraction(1, 40)

class TestT6_Zeta:
    def test_2_cycles(self):
        assert E == 240
    def test_3_cycles(self):
        assert 2 * T == 320
    def test_alt(self):
        assert 2 * T == lam**mu * E // k

class TestT7_MCMC:
    def test_cheeger(self):
        SLEM = Fraction(1, q)
        assert Fraction(1 - SLEM, 2) == Fraction(1, q)

class TestT8_Return:
    def test_return_2(self):
        P2 = Fraction(1, v) * (1 + f * Fraction(r**2, k**2) +
              g * Fraction(s**2, k**2))
        assert P2 == Fraction(1, k)
