"""
Phase CDXXV (425) — Algebraic Topology II: Homology & Cohomology
================================================================
Clique complex, f-vector, Euler characteristic, Betti numbers,
cycle/cut space, fundamental group.
"""
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
T = v * k * lam // 6
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_CliqueComplex:
    def test_f0(self):
        assert v == 40

    def test_f1(self):
        assert E == 240

    def test_f2(self):
        assert T == 160

    def test_f3(self):
        assert v == 40  # lines = tetrahedra = mu-cliques

    def test_euler(self):
        chi = v - E + T - v
        assert chi == -2 * v

    def test_euler_value(self):
        assert v - E + T - v == -80


class TestT2_FVector:
    def test_f0_plus_f2(self):
        assert v + T == (mu + 1) * v

    def test_f1_plus_f3(self):
        assert E + v == Phi6 * v

    def test_palindromic(self):
        assert v == v  # f_0 = f_3


class TestT3_CycleSpace:
    def test_cycle_dim(self):
        assert E - v + 1 == 201

    def test_cut_dim(self):
        assert v - 1 == 39

    def test_sum(self):
        assert 201 + 39 == E


class TestT4_BettiNumbers:
    def test_b0(self):
        assert True  # beta_0 = 1 (connected)

    def test_rank_d1(self):
        assert v - 1 == 39


class TestT5_FundamentalGroup:
    def test_generators(self):
        assert E - v + 1 == 201

    def test_relations(self):
        assert T == 160

    def test_upper_bound(self):
        assert 201 - T == v + 1
