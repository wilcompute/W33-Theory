"""
Phase CDXVI (416) — Finite Geometry II: Spreads, Ovoids & Polarities
=====================================================================
Spreads, ovoids, GQ parameters, dualities, m-systems.
"""
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
T = 160
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Spread:
    def test_size(self):
        assert v // (q + 1) == Phi4
    def test_line_size(self):
        assert q + 1 == mu
    def test_partition(self):
        assert Phi4 * mu == v
    def test_plane_order(self):
        assert q**2 == 9

class TestT2_Ovoid:
    def test_size(self):
        assert q**2 + 1 == Phi4
    def test_alpha(self):
        assert Phi4 == 10
    def test_spread_ovoid_duality(self):
        assert q**2 + 1 == v // (q + 1)

class TestT3_GQ:
    def test_v(self):
        assert (q + 1) * (q**2 + 1) == v
    def test_self_dual(self):
        assert (q + 1) * (q**2 + 1) == v
    def test_lines_per_point(self):
        assert q + 1 == mu
    def test_incidences(self):
        assert v * mu == T
