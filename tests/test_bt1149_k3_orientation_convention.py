from fractions import Fraction


def split(tau):
    chi = Fraction(24)
    diff = Fraction(3, 2) * tau
    return (chi + diff) / 2, (chi - diff) / 2


def test_base_orientation_is_tau_minus_16():
    plus, minus = split(Fraction(-16))
    assert plus == 0
    assert minus == 24


def test_orientation_reversal_swaps_chiral_slots():
    plus, minus = split(Fraction(16))
    assert plus == 24
    assert minus == 0
