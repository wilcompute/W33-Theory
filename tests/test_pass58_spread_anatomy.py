"""Pass 58: the spread side of the tax.

  - independent exact-cover enumeration: exactly 36 spreads of W(3,3), each line in 9;
  - service-rate lemma: every spread meets every point-star in exactly one line, so under any optimal
    assignment (Pass 57: failure set = one star) every spread runs at exactly 9/10;
  - anatomy: exactly 20 optima per defect center, center-free pairing (half lit), UNIFORM loading
    (c,c,c,c) with c in {2,3,4}; double occupancy (2,2,2,2) is the minimal (11-ray) class.
"""

import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import w33_master_audit as audit  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402


def _geometry():
    pts, A, lines, B = audit._build(3)
    return pts, lines


def test_spread_count_and_regularity():
    pts, lines = _geometry()
    spreads = anat.enumerate_spreads(lines, len(pts))
    assert len(spreads) == 36
    per_line = [0] * len(lines)
    for S in spreads:
        for li in S:
            per_line[li] += 1
    assert set(per_line) == {9}


def test_service_rate_lemma():
    pts, lines = _geometry()
    spreads = anat.enumerate_spreads(lines, len(pts))
    stars = {
        p: frozenset(li for li, L in enumerate(lines) if p in L)
        for p in range(len(pts))
    }
    assert all(
        len(set(S) & stars[p]) == 1 for S in spreads for p in range(len(pts))
    ), "every spread must contain exactly one line of every star"


def test_optima_anatomy_uniform_loading():
    pts, lines = _geometry()
    sols, star = anat._enumerate_optima_for_center(lines, len(pts), 0)
    assert len(sols) == 20, f"expected exactly 20 optima per center, got {len(sols)}"
    assert sum(1 for s in sols if s[0] == 1) == 10, "exactly half must light the center"
    for s in sols:
        occ = tuple(sorted(sum(s[p] for p in lines[li]) for li in star))
        assert len(set(occ)) == 1, f"defect loading must be uniform, got {occ}"
        assert occ[0] in (2, 3, 4)
    lit = {sum(s) for s in sols}
    assert lit == {11, 12, 13}
