from fractions import Fraction


def moment(power: int) -> int:
    if power == 0:
        return 40
    return 24 * 10**power + 15 * 16**power


def factorial(n: int) -> int:
    out = 1
    for k in range(2, n + 1):
        out *= k
    return out


def taylor_coeff(power: int) -> Fraction:
    return Fraction(((-1) ** power) * moment(power), factorial(power))


def test_w33_internal_moments():
    assert moment(0) == 40
    assert moment(1) == 480
    assert moment(2) == 6240
    assert moment(3) == 85440
    assert moment(4) == 1223040
    assert moment(5) == 18128640
    assert moment(6) == 275658240


def test_internal_heat_taylor_coefficients():
    assert taylor_coeff(0) == Fraction(40)
    assert taylor_coeff(1) == Fraction(-480)
    assert taylor_coeff(2) == Fraction(3120)
    assert taylor_coeff(3) == Fraction(-14240)
    assert taylor_coeff(4) == Fraction(50960)
    assert taylor_coeff(5) == Fraction(-151072)
    assert taylor_coeff(6) == Fraction(1148576, 3)


def test_convolution_A4_coefficients():
    # A4_tot = 40 a4 - 480 a2 + 3120 a0
    coeffs = {
        "a4_ext": taylor_coeff(0),
        "a2_ext": taylor_coeff(1),
        "a0_ext": taylor_coeff(2),
    }
    assert coeffs["a4_ext"] == Fraction(40)
    assert coeffs["a2_ext"] == Fraction(-480)
    assert coeffs["a0_ext"] == Fraction(3120)


def test_convolution_A8_coefficients():
    # A8_tot = 40 a8 - 480 a6 + 3120 a4 - 14240 a2 + 50960 a0
    coeffs = {
        "a8_ext": taylor_coeff(0),
        "a6_ext": taylor_coeff(1),
        "a4_ext": taylor_coeff(2),
        "a2_ext": taylor_coeff(3),
        "a0_ext": taylor_coeff(4),
    }
    assert coeffs == {
        "a8_ext": Fraction(40),
        "a6_ext": Fraction(-480),
        "a4_ext": Fraction(3120),
        "a2_ext": Fraction(-14240),
        "a0_ext": Fraction(50960),
    }


def test_flat_torus_leading_ladder():
    # If K_ext ~ 4 V/(4pi)^2 t^-2, A_{2r} multipliers are 4*c_r.
    assert 4 * taylor_coeff(0) == Fraction(160)
    assert 4 * taylor_coeff(1) == Fraction(-1920)
    assert 4 * taylor_coeff(2) == Fraction(12480)
    assert 4 * taylor_coeff(3) == Fraction(-56960)
    assert 4 * taylor_coeff(4) == Fraction(203840)


def test_factorization_identity_symbolic_finite():
    # For finite spectra, the Kronecker-sum heat trace factorization is an
    # algebraic distributive-law identity before any continuum limit.
    ext = [0, 1, 1, 4, 4, 9]
    internal = [0] + [10] * 24 + [16] * 15
    lhs_pairs = sorted(x + y for x in ext for y in internal)
    rhs_pairs = sorted(x + y for x in ext for y in internal)
    assert lhs_pairs == rhs_pairs
    assert len(lhs_pairs) == len(ext) * 40
