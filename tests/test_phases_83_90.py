from fractions import Fraction

q = 3
v = 40
k = 12
lam = 2
mu = 4
r = 2
s = -4


def test_phase_83_lqg():
    j_r = r // lam
    j_s = abs(s) // lam
    assert j_r == 1 and j_s == 2
    assert j_s * (j_s + 1) == q * j_r * (j_r + 1)


def test_phase_84_ncg():
    assert mu == 4


def test_phase_85_langlands():
    assert q + 1 == mu


def test_phase_86_topo_anyons():
    assert mu == 4


def test_phase_87_holocode():
    assert Fraction(1, mu) == Fraction(1, mu)
    assert v // lam == 20


def test_phase_88_cobordism():
    assert q + 1 == mu


def test_phase_89_experimental():
    assert (mu + 1) ** q == 125
    assert v - mu + lam == 38


def test_phase_90_release():
    assert True
