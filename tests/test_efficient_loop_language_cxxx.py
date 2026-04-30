"""
Part CXXX — efficient loop language.

Regression tests for the trit-weighted loop language formulation and its
uniform-cost reduction to W33 Hashimoto loop probability.
"""

from fractions import Fraction

DIRECTED_EDGES = 480
BRANCH = 11
LAMBDA = 2


def uniform_cost_weight(n: int) -> Fraction:
    # 3^{-n log_3(11)} = 11^{-n}.
    return Fraction(1, BRANCH**n)


def efficient_partition_uniform(n: int, closed_histories_per_edge: int) -> Fraction:
    return closed_histories_per_edge * uniform_cost_weight(n)


class TestCXXXEfficientLoopLanguage:
    def test_local_language_cardinality(self):
        assert BRANCH == 11
        assert [BRANCH**n for n in range(4)] == [1, 11, 121, 1331]

    def test_uniform_cost_reduction(self):
        for n, closed in [(3, 2), (4, 29), (5, 378), (6, 3788)]:
            assert efficient_partition_uniform(n, closed) == Fraction(closed, BRANCH**n)

    def test_first_selection_event(self):
        local_words = BRANCH**3
        realized_words = LAMBDA
        assert local_words == 1331
        assert realized_words == 2
        assert Fraction(realized_words, local_words) == Fraction(2, 1331)

    def test_cct_dictionary_dimensions(self):
        assert DIRECTED_EDGES == 480
        assert BRANCH == 11
        assert LAMBDA == 2
        assert BRANCH == LAMBDA + 9

    def test_weighted_measure_normalizes_on_admissible_histories(self):
        # Example with two admissible histories of different trit costs.
        weights = [Fraction(1, 3), Fraction(1, 9)]
        Z = sum(weights)
        probs = [w / Z for w in weights]
        assert Z == Fraction(4, 9)
        assert probs == [Fraction(3, 4), Fraction(1, 4)]
        assert sum(probs) == 1
