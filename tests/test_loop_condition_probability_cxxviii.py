"""
Part CXXVIII — loop-conditioned probability.

Exact arithmetic tests for the W33 Hashimoto loop partition function.
"""

V = 40
E_UNDIRECTED = 240
DIRECTED_EDGES = 2 * E_UNDIRECTED
K = 12
BRANCH = K - 1
M_MINUS_N = E_UNDIRECTED - V

ADJ_EIGS = {12: 1, 2: 24, -4: 15}


def S(lam: int, n: int) -> int:
    """Power sum for the two Hashimoto roots over adjacency eigenvalue lam."""
    if n == 0:
        return 2
    if n == 1:
        return lam
    a, b = 2, lam
    for _ in range(2, n + 1):
        a, b = b, lam * b - BRANCH * a
    return b


def Z(n: int) -> int:
    """Trace(B^n) from Ihara-Bass for the 12-regular W33 graph."""
    return M_MINUS_N * (1 + (-1) ** n) + sum(
        mult * S(lam, n) for lam, mult in ADJ_EIGS.items()
    )


def closed_histories_per_directed_edge(n: int) -> int:
    z = Z(n)
    assert z % DIRECTED_EDGES == 0
    return z // DIRECTED_EDGES


class TestCXXVIIIHashimotoTrace:
    def test_first_trace_values(self):
        assert [Z(n) for n in range(7)] == [480, 0, 0, 960, 13920, 181440, 1818240]

    def test_first_nontrivial_loop_at_three(self):
        assert closed_histories_per_directed_edge(1) == 0
        assert closed_histories_per_directed_edge(2) == 0
        assert closed_histories_per_directed_edge(3) == 2

    def test_triangle_loop_probability(self):
        numerator = closed_histories_per_directed_edge(3)
        denominator = BRANCH**3
        assert numerator == 2
        assert denominator == 1331

    def test_later_loop_counts_per_edge(self):
        assert closed_histories_per_directed_edge(4) == 29
        assert closed_histories_per_directed_edge(5) == 378
        assert closed_histories_per_directed_edge(6) == 3788


class TestCXXVIIIStructure:
    def test_ihara_backtracking_term(self):
        assert M_MINUS_N == 200 == 5 * V
        assert DIRECTED_EDGES == 480
        assert BRANCH == 11

    def test_power_sum_recurrence_seed(self):
        for lam in ADJ_EIGS:
            assert S(lam, 0) == 2
            assert S(lam, 1) == lam
            assert S(lam, 2) == lam * lam - 2 * BRANCH

    def test_unconditioned_branch_space(self):
        # Without a closure condition, all local non-backtracking histories survive.
        assert BRANCH**0 == 1
        assert BRANCH**1 == 11
        assert BRANCH**2 == 121
        assert BRANCH**3 == 1331

    def test_loop_condition_selects_triangle_branches_from_11_way_space(self):
        # At the first loop, the two lambda=2 triangle branches close;
        # the remaining 9 open branches do not close at length three.
        assert 2 + 9 == BRANCH
        assert closed_histories_per_directed_edge(3) == 2
