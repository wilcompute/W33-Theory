"""
Part CXXV — A2 overlap null plane for complete two-qutrit MUB frames.

This test uses only the pair-overlap laws established by Parts CXX-CXXIV.
It does not assume the unresolved fine split inside the 3-cycle layer.
"""

TYPES = ("E+", "E-", "O")
SECTOR_SIZE = 12
SELF_OVERLAP = 10
FOUR = 4
ONE = 1

# Four-overlap neighbor counts per frame by target sector.
# CXXIV gives 3 inside the same chirality/type sector and 6 in each other sector.
FOUR_OVERLAP_QUOTIENT = (
    (3, 6, 6),
    (6, 3, 6),
    (6, 6, 3),
)

# Total-overlap row sums per source frame into each target sector.
# Same sector: self contributes 10; among the 11 other frames, 3 have overlap 4
# and 8 have overlap 1. Cross sector: 6 have overlap 4 and 6 have overlap 1.
TOTAL_OVERLAP_QUOTIENT = (
    (30, 30, 30),
    (30, 30, 30),
    (30, 30, 30),
)


def mat_vec(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M)))


def det3(M):
    return (
        M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
        - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
        + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
    )


class TestCXXVForcedQuotient:
    def test_four_overlap_graph_is_15_regular(self):
        assert [sum(row) for row in FOUR_OVERLAP_QUOTIENT] == [15, 15, 15]
        assert SECTOR_SIZE * len(TYPES) == 36
        assert (36 * 15) // 2 == 270

    def test_total_overlap_balances_each_sector(self):
        for row in TOTAL_OVERLAP_QUOTIENT:
            assert row == (30, 30, 30)
            assert sum(row) == 90

    def test_same_and_cross_sector_counts_force_30(self):
        same_sector_total = SELF_OVERLAP + 3 * FOUR + 8 * ONE
        cross_sector_total = 6 * FOUR + 6 * ONE
        assert same_sector_total == 30
        assert cross_sector_total == 30

    def test_edge_count_decomposition(self):
        within_edges = len(TYPES) * (SECTOR_SIZE * 3 // 2)
        cross_edges = 3 * (SECTOR_SIZE * 6)
        assert within_edges == 54
        assert cross_edges == 216
        assert within_edges + cross_edges == 270


class TestCXXVA2NullPlane:
    def test_four_overlap_quotient_has_a2_eigenvalue_minus_3(self):
        a2_1 = (1, -1, 0)
        a2_2 = (1, 1, -2)
        assert mat_vec(FOUR_OVERLAP_QUOTIENT, (1, 1, 1)) == (15, 15, 15)
        assert mat_vec(FOUR_OVERLAP_QUOTIENT, a2_1) == tuple(-3 * x for x in a2_1)
        assert mat_vec(FOUR_OVERLAP_QUOTIENT, a2_2) == tuple(-3 * x for x in a2_2)

    def test_total_overlap_quotient_kills_a2_plane(self):
        a2_1 = (1, -1, 0)
        a2_2 = (1, 1, -2)
        assert mat_vec(TOTAL_OVERLAP_QUOTIENT, (1, 1, 1)) == (90, 90, 90)
        assert mat_vec(TOTAL_OVERLAP_QUOTIENT, a2_1) == (0, 0, 0)
        assert mat_vec(TOTAL_OVERLAP_QUOTIENT, a2_2) == (0, 0, 0)

    def test_total_overlap_quotient_is_rank_one(self):
        assert det3(TOTAL_OVERLAP_QUOTIENT) == 0
        assert TOTAL_OVERLAP_QUOTIENT[0] == TOTAL_OVERLAP_QUOTIENT[1] == TOTAL_OVERLAP_QUOTIENT[2]
