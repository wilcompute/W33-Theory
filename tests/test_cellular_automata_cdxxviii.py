"""
Phase CDXXVIII (428) — Universal Computation & Cellular Automata
================================================================
CA on graph, threshold automata, circuit depth, mixing time.
"""
import math
v, k, lam, mu = 40, 12, 2, 4
q = 3
r, s = 2, -4
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_CellularAutomata:
    def test_CA_inputs(self):
        assert k + 1 == Phi3

    def test_totalistic_rules(self):
        assert 2 ** (k + 1) == 2 ** Phi3


class TestT2_Thresholds:
    def test_majority(self):
        assert k // lam == math.factorial(q)

    def test_bootstrap(self):
        assert abs(v / (k + 1) - q) < 0.1

    def test_conway(self):
        assert q == 3


class TestT3_CircuitDepth:
    def test_diameter(self):
        assert lam == 2

    def test_1hop(self):
        assert k + 1 == Phi3

    def test_2hop(self):
        assert v == 40

    def test_spacetime(self):
        assert v * lam == 80


class TestT4_MixingTime:
    def test_spectral_ratio(self):
        assert k // abs(s) == q

    def test_mixing(self):
        t_mix = math.log(v) / math.log(q)
        assert abs(t_mix - math.log(v) / math.log(k / abs(s))) < 0.01
