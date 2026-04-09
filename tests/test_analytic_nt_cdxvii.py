"""
Phase CDXVII (417) — Analytic Number Theory & L-functions
==========================================================
Prime counting, Bernoulli denominators, twin primes, Dirichlet.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


def _is_prime(n):
    return n > 1 and all(n % d != 0 for d in range(2, int(n**0.5) + 1))


class TestT1_PrimeCounting:
    def test_pi_v(self):
        assert sum(1 for p in range(2, v + 1) if _is_prime(p)) == k
    def test_pi_k(self):
        assert sum(1 for p in range(2, k + 1) if _is_prime(p)) == mu + 1
    def test_pi_Phi4(self):
        assert sum(1 for p in range(2, Phi4 + 1) if _is_prime(p)) == mu
    def test_pi_E(self):
        assert sum(1 for p in range(2, E + 1) if _is_prime(p)) == mu * Phi3

class TestT2_Bernoulli:
    def test_B2(self):
        assert math.factorial(q) == 6
    def test_B4(self):
        assert v - Phi4 == 30
    def test_B6(self):
        assert v + lam == 42
    def test_B12(self):
        assert lam * q * (mu + 1) * Phi6 * Phi3 == 2730

class TestT3_Primes:
    def test_count(self):
        primes = [p for p in range(2, v + 1) if _is_prime(p)]
        assert len(primes) == 12
    def test_primorial_3(self):
        assert 2 * 3 * 5 == v - Phi4

class TestT4_Gaps:
    def test_max_gap(self):
        primes = [p for p in range(2, v + 1) if _is_prime(p)]
        gaps = [primes[i + 1] - primes[i] for i in range(len(primes) - 1)]
        assert max(gaps) == math.factorial(q)
    def test_twin_pairs(self):
        primes = [p for p in range(2, v + 1) if _is_prime(p)]
        gaps = [primes[i + 1] - primes[i] for i in range(len(primes) - 1)]
        assert sum(1 for g in gaps if g == 2) == mu + 1
