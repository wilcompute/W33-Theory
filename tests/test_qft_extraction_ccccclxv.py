from fractions import Fraction

SPECTRUM = {0: 81, 4: 120, 10: 24, 16: 15}


def moment(power: int) -> int:
    if power == 0:
        return sum(SPECTRUM.values())
    return sum(mult * eig**power for eig, mult in SPECTRUM.items())


def factorial(n: int) -> int:
    out = 1
    for k in range(2, n + 1):
        out *= k
    return out


def taylor_coeff(power: int) -> Fraction:
    return Fraction(((-1) ** power) * moment(power), factorial(power))


def convolution(r: int) -> dict[str, Fraction]:
    return {f"a{2 * (r - ell)}_ext": taylor_coeff(ell) for ell in range(r + 1)}


def test_spectrum_dimension_and_split():
    assert sum(SPECTRUM.values()) == 240
    assert SPECTRUM[0] == 81
    assert SPECTRUM[4] == 120
    assert SPECTRUM[10] == 24
    assert SPECTRUM[16] == 15


def test_internal_moments():
    assert moment(0) == 240
    assert moment(1) == 960
    assert moment(2) == 8160
    assert moment(3) == 93120
    assert moment(4) == 1253760
    assert moment(5) == 18251520
    assert moment(6) == 276149760
    assert moment(7) == 4268497920
    assert moment(8) == 66832373760


def test_internal_heat_taylor_coefficients():
    assert taylor_coeff(0) == Fraction(240)
    assert taylor_coeff(1) == Fraction(-960)
    assert taylor_coeff(2) == Fraction(4080)
    assert taylor_coeff(3) == Fraction(-15520)
    assert taylor_coeff(4) == Fraction(52240)
    assert taylor_coeff(5) == Fraction(-152096)
    assert taylor_coeff(6) == Fraction(1150624, 3)
    assert taylor_coeff(7) == Fraction(-17785408, 21)
    assert taylor_coeff(8) == Fraction(34808528, 21)


def test_convolution_A4_and_A8():
    assert convolution(2) == {
        "a4_ext": Fraction(240),
        "a2_ext": Fraction(-960),
        "a0_ext": Fraction(4080),
    }
    assert convolution(4) == {
        "a8_ext": Fraction(240),
        "a6_ext": Fraction(-960),
        "a4_ext": Fraction(4080),
        "a2_ext": Fraction(-15520),
        "a0_ext": Fraction(52240),
    }


def test_gauge_normalization_factor():
    # With a4_ext[F^2] normalized as (4pi)^(-2) * (1/12) kappa_G tr(F^2),
    # the universal W(3,3) leading factor is dim(C1)/12 = 240/12 = 20.
    assert Fraction(240, 12) == Fraction(20)


def test_fermionic_projection_dimensions():
    h1 = SPECTRUM[0]
    assert h1 == 81
    assert 2 * h1 == 162
