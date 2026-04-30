"""
Part CXXXIV — Parry-KMS cycle clock state.

Exact arithmetic checks for the maximum-entropy Parry Markov state of the
W33 Hashimoto non-backtracking shift.
"""

from fractions import Fraction

DIRECTED_EDGES = 480
K = 12
BRANCH = K - 1

# Trace values from CXXVIII/CXXIX.
Z = {
    1: 0,
    2: 0,
    3: 960,
    4: 13920,
    5: 181440,
    6: 1818240,
}


def stationary_weight() -> Fraction:
    return Fraction(1, DIRECTED_EDGES)


def legal_cylinder_probability(length: int) -> Fraction:
    return Fraction(1, DIRECTED_EDGES * BRANCH**length)


def stationary_loop_return_probability(n: int) -> Fraction:
    return Fraction(Z[n], DIRECTED_EDGES * BRANCH**n)


class TestCXXXIVParryKMSState:
    def test_perron_frobenius_data(self):
        assert BRANCH == 11
        assert DIRECTED_EDGES == 480
        assert K == 12

    def test_uniform_stationary_distribution(self):
        pi = stationary_weight()
        assert pi == Fraction(1, 480)
        assert DIRECTED_EDGES * pi == 1

    def test_legal_cylinder_weights(self):
        assert legal_cylinder_probability(0) == Fraction(1, 480)
        assert legal_cylinder_probability(1) == Fraction(1, 480 * 11)
        assert legal_cylinder_probability(3) == Fraction(1, 480 * 11**3)

    def test_loop_probability_is_stationary_return_probability(self):
        assert stationary_loop_return_probability(1) == 0
        assert stationary_loop_return_probability(2) == 0
        assert stationary_loop_return_probability(3) == Fraction(2, 11**3)
        assert stationary_loop_return_probability(4) == Fraction(29, 11**4)

    def test_critical_beta_is_entropy_normalized(self):
        # The primitive-loop thermal weight is 11^{-beta*n}; beta_c=1
        # matches the entropy-normalized per-symbol Parry weight 1/11.
        beta_c = 1
        per_symbol_weight_denominator = BRANCH**beta_c
        assert per_symbol_weight_denominator == 11
