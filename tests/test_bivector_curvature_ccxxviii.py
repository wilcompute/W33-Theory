from fractions import Fraction

q, v, k, lam, mu = 3, 40, 12, 2, 4
Phi3, Phi4, Phi6 = 13, 10, 7

A0 = 480
C_EH = 320
A2 = 2240
C6 = 12480
A4 = 17600


def test_bivector_scale():
    assert Fraction(k, lam) == 6
    assert Fraction(k, lam) == Fraction(mu * (mu - 1), 2)


def test_curvature_shell():
    assert lam * Phi4 == 20
    assert lam * Phi4 == Fraction(mu**2 * (mu**2 - 1), 12)


def test_dominant_mode_factorization():
    assert Fraction(k, lam) * (lam * Phi4) == 120


def test_promoted_packet_factorization():
    N = lam * Phi4
    assert A0 == 24 * N
    assert C_EH == (2 ** mu) * N
    assert A2 == Phi6 * (2 ** mu) * N
    assert C6 == (q * Phi3) * (2 ** mu) * N
    assert A4 == 55 * (2 ** mu) * N


def test_packet_ratios():
    assert Fraction(A2, A0) == Fraction(14, 3)
    assert Fraction(A4, A2) == Fraction(55, 7)
    assert Fraction(A4, A0) == Fraction(110, 3)


def test_one_scale_no_go():
    s = Fraction(k, lam)
    N = lam * Phi4
    assert s**2 == 36
    assert s * N == 120
    assert s**2 != s * N
