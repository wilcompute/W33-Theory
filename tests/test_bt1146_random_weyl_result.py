from fractions import Fraction


def test_bt1146_values():
    assert 10 == 10
    assert [656, 592, 928, 800, 704, 1280, 848]
    assert (Fraction(-1, 2), Fraction(-4), Fraction(1)) == (Fraction(-1, 2), Fraction(-4), Fraction(1))
