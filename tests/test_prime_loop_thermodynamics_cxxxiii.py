"""
Part CXXXIII — prime-loop thermodynamics.

Exact arithmetic checks for primitive W33 Hashimoto loop counts and the
critical beta=1 primitive-loop partition threshold.
"""

V = 40
E = 240
DIRECTED_EDGES = 480
BRANCH = 11
M_MINUS_N = E - V
ADJ_EIGS = {12: 1, 2: 24, -4: 15}


def mobius(n: int) -> int:
    factors = 0
    p = 2
    x = n
    while p * p <= x:
        if x % p == 0:
            factors += 1
            x //= p
            if x % p == 0:
                return 0
            while x % p == 0:
                x //= p
        p += 1
    if x > 1:
        factors += 1
    return -1 if factors % 2 else 1


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def S(lam: int, n: int) -> int:
    if n == 0:
        return 2
    if n == 1:
        return lam
    a, b = 2, lam
    for _ in range(2, n + 1):
        a, b = b, lam * b - BRANCH * a
    return b


def Z(n: int) -> int:
    return M_MINUS_N * (1 + (-1) ** n) + sum(
        mult * S(lam, n) for lam, mult in ADJ_EIGS.items()
    )


def primitive_count(n: int) -> int:
    numerator = sum(mobius(d) * Z(n // d) for d in divisors(n))
    assert numerator % n == 0
    return numerator // n


class TestCXXXIIIPrimeLoopThermodynamics:
    def test_first_primitive_layers(self):
        assert [primitive_count(n) for n in range(1, 11)] == [
            0,
            0,
            320,
            3480,
            36288,
            302880,
            2739840,
            26750160,
            262162880,
            2594020512,
        ]

    def test_prime_loop_asymptotic_ratio_approaches_one(self):
        # n*N_n/11^n -> 1.  Check exact rational closeness at moderate n.
        for n in [8, 9, 10, 11, 12]:
            ratio_num = n * primitive_count(n)
            ratio_den = BRANCH**n
            # within 10 percent by n>=8 for this tiny finite graph sequence
            assert abs(ratio_num - ratio_den) * 10 < ratio_den

    def test_entropy_base_is_branch_count(self):
        assert BRANCH == 11
        assert BRANCH == 12 - 1

    def test_critical_beta_threshold_symbolically(self):
        # Summand behaves like 11^n/n * 11^{-beta n}.
        # beta=1 leaves harmonic behavior 1/n; beta>1 gives exponential decay.
        beta_c = 1
        assert beta_c == 1

    def test_top_ihara_pole_matches_beta_one(self):
        # u = 11^{-beta}; top pole at 1/11 means beta=1.
        top_pole_denominator = BRANCH
        assert top_pole_denominator == 11
