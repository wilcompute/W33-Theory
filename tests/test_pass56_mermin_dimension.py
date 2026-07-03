"""Pass 56: two contextualities separated on W(2), and the realization dimension bound.

  - w33_doily_mermin: the doily's Pauli sign system is UNSATISFIABLE over F_2 (Mermin-Peres), with a
    minimal 6-line certificate of even point-degree and odd -I count, while the selection system
    (exactly one click per context, the demonstrator's CF statistic) is satisfied by the 5-ray ovoid.
    So the even control fabric is sign-contextual yet selection-noncontextual -- the honest boundary
    of the two-arm discriminator.
  - w33_realization_dimension: W(2) admits no complete-basis ray realization in C^3 (mu=3 distinct
    rays cannot fit a 1-dim orthocomplement); q=3 is unobstructed (Witting exists); q=3 is the
    smallest realizable and, by parity, smallest contextual order.
"""

import os
import sys
from collections import Counter

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import w33_doily_mermin as dm  # noqa: E402
import w33_realization_dimension as rd  # noqa: E402


def test_sign_system_unsatisfiable_with_mermin_certificate():
    solvable, cert, signs, lines = dm.find_certificate()
    assert (
        not solvable
    ), "doily Pauli sign system should be unsatisfiable (Mermin-Peres)"
    assert (
        cert is not None and len(cert) == 6
    ), f"minimal certificate should be 6 lines, got {cert}"
    deg = Counter(p for li in cert for p in lines[li])
    assert all(
        d % 2 == 0 for d in deg.values()
    ), "certificate must cover every point evenly"
    assert (
        sum(1 for li in cert if signs[li] == -1) % 2 == 1
    ), "certificate needs odd -I count"


def test_line_signs_are_plus_minus_one():
    pts, lines, signs = dm.line_signs()
    assert len(lines) == 15 and set(signs) <= {1, -1}
    assert sum(1 for s in signs if s == -1) == 3


def test_dimension_bound_obstruction_only_at_q2():
    for q, expect in ((2, True), (3, False), (4, False)):
        r = rd.pair_counts(q)
        assert r["mu"] == [q + 1] and r["lambda"] == [q - 1]
        assert r["obstruction"] is expect, f"q={q} obstruction should be {expect}"
        assert r["collinear_common_mutually_collinear"] is True
