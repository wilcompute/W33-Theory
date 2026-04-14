"""
Phase V49 — Unified closure rigidity summary
============================================

One rigidity packet joins inflation, mass, and lepton closure.
"""

from fractions import Fraction as Fr

q = 3
v = 40
k = 12
lam = 2
mu = 4
g = 15
Phi4 = 10
Phi6 = 7
alpha_inv = 137
nn = 27
E = v * k // 2


class TestV49UnifiedClosure:
    def test_inflation_bridge(self):
        assert E // mu == 2 * (v - Phi4) == 60

    def test_inflation_packet(self):
        ns = Fr(29, 30)
        r = Fr(1, 300)
        running = Fr(-1, 1800)
        nt = Fr(-1, 2400)
        fnl = Fr(-1, 72)

        assert r == 3 * (1 - ns) ** 2
        assert running == -r / 6
        assert nt == -r / 8
        assert fnl == -Fr(5, 12) * (1 - ns)

    def test_mass_packet(self):
        assert Fr(3, 136) / Fr(1, 136) == q
        assert Fr(1, 600) / Fr(1, 20) == Fr(1, v - Phi4)
        assert Fr(1, 14) == Fr(1, 2 * Phi6)
        assert Fr(7, 15) == Fr(Phi6, g)
        assert Fr(1, 14) * Fr(7, 15) == Fr(1, v - Phi4)

    def test_lepton_packet(self):
        assert Fr(1, k + q + lam) == Fr(1, 17)
        assert Fr(1, alpha_inv + v + nn + lam) == Fr(1, 206)
        assert Fr(1, 17) * Fr(1, 206) == Fr(1, 3502)
        assert 206 - alpha_inv == v + nn + lam == 69

    def test_unified_rigidity(self):
        inflation = E // mu == 2 * (v - Phi4) == 60
        mass = Fr(1, 14) * Fr(7, 15) == Fr(1, v - Phi4)
        lepton = Fr(1, 17) * Fr(1, 206) == Fr(1, 3502)
        assert all([inflation, mass, lepton])
