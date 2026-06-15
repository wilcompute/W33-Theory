from fractions import Fraction


def test_k3_weyl_signature_split():
    chi = Fraction(24)
    tau = Fraction(-16)
    total = chi
    diff = Fraction(3, 2) * tau
    plus = (total + diff) / 2
    minus = (total - diff) / 2
    assert diff == -24
    assert plus == 0
    assert minus == 24


def test_k3_weyl_c4_total():
    assert 440 * 24 + 8160 == 18720
