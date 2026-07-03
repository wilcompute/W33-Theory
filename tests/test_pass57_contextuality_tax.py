"""Pass 57: the contextuality tax -- the defect is one movable point-star (exhaustive).

The synthesis of the contextual-fraction arc and the OS/scheduler arc:
  - deficit law: n - max_sat = 0 for even q (ovoid) and q+1 (one star) for odd q, so CF = 1/(q^2+1);
  - the NEW exact classification at q=3: enumerating ALL optimal failure sets by ILP + no-good cuts
    terminates with exactly 40 sets, each the point-star of one point, one per point -- the scheduler
    arc's "movable point-star defect" as a theorem;
  - the parity corollary: even q has alpha = Hoffman (no selection gap even in principle).
"""

import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import w33_contextuality_tax as tax  # noqa: E402


def test_deficit_law():
    rows = tax.deficit_law((2, 3, 4))
    by_q = {r["q"]: r for r in rows}
    assert by_q[2]["deficit"] == 0 and by_q[4]["deficit"] == 0
    assert by_q[3]["deficit"] == 4  # q+1: one star


def test_gap_by_parity():
    rows = tax.deficit_law((2, 3, 4))
    by_q = {r["q"]: r for r in rows}
    assert by_q[2]["selection_gap_hoffman_minus_alpha"] == 0
    assert by_q[4]["selection_gap_hoffman_minus_alpha"] == 0
    assert by_q[3]["selection_gap_hoffman_minus_alpha"] == 3  # 10 - 7


def test_exhaustive_star_classification():
    target, found, all_stars, star_points = tax.classify_failure_sets(3)
    assert target == 36
    assert (
        len(found) == 40
    ), f"expected exactly 40 optimal failure sets, got {len(found)}"
    assert all_stars, "every optimal failure set must be a point-star"
    assert (
        len({p for p in star_points if p is not None}) == 40
    ), "the star must be movable to every point"
    # each failure set is 4 distinct lines
    assert all(len(F) == 4 for F in found)
