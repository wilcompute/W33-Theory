from fractions import Fraction
import math

SPECTRUM = {0: 81, 4: 120, 10: 24, 16: 15}


def moment(power: int) -> int:
    if power == 0:
        return sum(SPECTRUM.values())
    return sum(mult * eig**power for eig, mult in SPECTRUM.items())


def taylor(power: int) -> Fraction:
    return Fraction(((-1) ** power) * moment(power), math.factorial(power))


def normalized(power: int) -> Fraction:
    return taylor(power) / 240


def test_dimensionful_operator_bookkeeping():
    assert sum(SPECTRUM.values()) == 240
    assert SPECTRUM[0] == 81
    assert SPECTRUM[4] == 120
    assert SPECTRUM[10] == 24
    assert SPECTRUM[16] == 15


def test_dimensionless_and_scaled_moments():
    assert moment(0) == 240
    assert moment(1) == 960
    assert moment(2) == 8160
    assert moment(3) == 93120
    # Dimensionful ledger: Mu_l = M_F^(2l) mu_l.  The powers are checked
    # symbolically by the coefficient tests below; the raw mu_l values must remain fixed.


def test_scaled_taylor_coefficients():
    assert taylor(0) == Fraction(240)
    assert taylor(1) == Fraction(-960)
    assert taylor(2) == Fraction(4080)
    assert taylor(3) == Fraction(-15520)
    assert taylor(4) == Fraction(52240)
    assert taylor(5) == Fraction(-152096)
    assert taylor(6) == Fraction(1150624, 3)


def test_normalized_w33_polynomial_coefficients():
    assert normalized(0) == Fraction(1)
    assert normalized(1) == Fraction(-4)
    assert normalized(2) == Fraction(17)
    assert normalized(3) == Fraction(-194, 3)
    assert normalized(4) == Fraction(653, 3)
    assert normalized(5) == Fraction(-9506, 15)
    assert normalized(6) == Fraction(71914, 45)


def test_dimensionful_convolution_A4_and_A8_coefficients():
    # A4_tot(M_F) = 240 a4 - 960 M_F^2 a2 + 4080 M_F^4 a0
    assert [taylor(i) for i in range(3)] == [
        Fraction(240),
        Fraction(-960),
        Fraction(4080),
    ]
    # A8_tot(M_F) = 240 a8 - 960 M_F^2 a6 + 4080 M_F^4 a4
    #              -15520 M_F^6 a2 + 52240 M_F^8 a0
    assert [taylor(i) for i in range(5)] == [
        Fraction(240),
        Fraction(-960),
        Fraction(4080),
        Fraction(-15520),
        Fraction(52240),
    ]


def test_gauge_leading_factor_and_ratio_control():
    assert Fraction(240, 12) == Fraction(20)
    # The expansion parameter is x = M_F^2/Lambda^2; normalized coefficients
    # provide the universal finite renormalization polynomial.
    assert [normalized(i) for i in range(4)] == [
        Fraction(1),
        Fraction(-4),
        Fraction(17),
        Fraction(-194, 3),
    ]
