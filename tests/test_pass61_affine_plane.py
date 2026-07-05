"""Pass 61: the ground states are an affine plane.

  - ILP-free characterization: the 27 non-neighbors carry exactly 81 four-centric triads whose
    center-quads split {all-4-in-perp: 9, exactly-1: 72}; the grounds are exactly the first class;
  - the affine plane law at q=3: 9 grounds = AG(2,3) = the Hesse configuration, neighbors = lines,
    defect lines = parallel classes;
  - the q=5 closure is exhaustive: 52 = 2(q^2+1) optima, grounds = AG(2,5).
"""

import os
import sys
from collections import Counter
from itertools import combinations

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import w33_ground_affine_plane as gap  # noqa: E402
import w33_master_audit as audit  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402


def test_triad_space_and_ilp_free_characterization():
    triads, nb, nonn = gap.four_centric_triads(3)
    assert len(triads) == 81
    in_nb = Counter(sum(1 for c in perp if c in nb) for (t, perp) in triads)
    assert in_nb == Counter({4: 9, 1: 72})
    pts, A, lines, B = audit._build(3)
    n = len(pts)
    star = [li for li, L in enumerate(lines) if 0 in L]
    sols, _ = anat._enumerate_optima_for_center(lines, n, 0)
    _, ok, grounds = gap.affine_plane_checks(3, sols, lines, nb, star)
    assert ok
    gtriples = {tuple(sorted(g - nb)) for g in grounds}
    assert gtriples == {t for (t, perp) in triads if all(c in nb for c in perp)}


def test_q5_closure_exhaustive_affine_plane():
    pts, A, lines, B = audit._build(5)
    n = len(pts)
    nb = frozenset(j for j in range(n) if A[0][j])
    star = [li for li, L in enumerate(lines) if 0 in L]
    sols, _ = anat._enumerate_optima_for_center(lines, n, 0, cap=400)
    assert len(sols) == 52, "q=5 optima per center must close at 2(q^2+1) = 52"
    facts, ok, grounds = gap.affine_plane_checks(5, sols, lines, nb, star)
    assert ok and len(grounds) == 25
    assert facts["ground_lit_pairwise_intersection"] == [19]
