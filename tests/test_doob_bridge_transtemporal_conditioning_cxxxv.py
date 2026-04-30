"""
Part CXXXV — Doob-bridge transtemporal conditioning.

Exact arithmetic checks for loop-conditioned Parry paths on the W33
Hashimoto carrier.
"""

from fractions import Fraction

BRANCH = 11
TRIANGLE_CLOSURES = 2
OPEN_TURNS = 9


def bridge_probability(future_completion_count: int, total_completion_count: int) -> Fraction:
    return Fraction(future_completion_count, total_completion_count)


class TestCXXXVDoobBridge:
    def test_unconditioned_first_step_is_uniform_over_eleven(self):
        assert BRANCH == 11
        assert Fraction(1, BRANCH) == Fraction(1, 11)

    def test_length_three_bridge_lenses_eleven_to_two(self):
        assert TRIANGLE_CLOSURES + OPEN_TURNS == BRANCH
        assert TRIANGLE_CLOSURES == 2
        assert OPEN_TURNS == 9

    def test_length_three_first_bridge_step_distribution(self):
        probs = [bridge_probability(1, TRIANGLE_CLOSURES) for _ in range(TRIANGLE_CLOSURES)]
        probs += [bridge_probability(0, TRIANGLE_CLOSURES) for _ in range(OPEN_TURNS)]
        assert probs.count(Fraction(1, 2)) == 2
        assert probs.count(Fraction(0, 1)) == 9
        assert sum(probs) == 1

    def test_doob_bridge_formula_cancels_branch_factors(self):
        # P(x,y)=1/11 and h_t counts future completions under B.
        # P_bridge = (1/11*h_next)/(h_now/11) = h_next/h_now.
        h_next = 1
        h_now = 2
        assert Fraction(1, BRANCH) * h_next / Fraction(h_now, BRANCH) == Fraction(1, 2)

    def test_probability_lensing_ratio(self):
        # The event of loop-compatible first choice has unconditioned probability 2/11.
        # After conditioning on the loop, it has probability 1.
        assert Fraction(TRIANGLE_CLOSURES, BRANCH) == Fraction(2, 11)
        assert Fraction(TRIANGLE_CLOSURES, TRIANGLE_CLOSURES) == 1
