"""Pass 60: the perp states.

  - the special (3,3,3,3) optimum at center p is exactly the deleted perp Gamma(p); its flip is the
    full perp (a geometric hyperplane); the defining GQ axiom is the optimality proof, at every order;
  - the tax load spectrum {q-1, q, q+1} = {ground states, deleted perp, full perp};
  - the nine ground states are stabilizer-transitive and their out-triples partition the 27
    non-neighbors into nine pairwise non-collinear triads (common-perp size 4 each).
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
import w33_perp_states as ps  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402


def test_gq_axiom_and_perp_profiles():
    for q in (2, 3, 4):
        assert ps.gq_axiom_holds(q)
        pr = ps.perp_state_profile(q)
        assert pr["non_star_all_satisfied"] is True
        assert pr["star_loading_deleted"] == [q] * (q + 1)
        assert pr["star_loading_full"] == [q + 1] * (q + 1)
        assert pr["deleted_perp_size"] == q * (q + 1)


def test_special_optimum_is_deleted_perp():
    pts, A, lines, B = audit._build(3)
    n = len(pts)
    sols, star = anat._enumerate_optima_for_center(lines, n, 0)
    nb = frozenset(j for j in range(n) if A[0][j])
    specials = [
        frozenset(i for i in range(n) if s[i])
        for s in sols
        if s[0] == 0
        and tuple(sorted(sum(s[p] for p in lines[li]) for li in star)) == (3, 3, 3, 3)
    ]
    assert len(specials) == 1 and specials[0] == nb


def test_ground_state_triads_partition_27():
    pts, A, lines, B = audit._build(3)
    n = len(pts)
    sols, star = anat._enumerate_optima_for_center(lines, n, 0)
    nb = frozenset(j for j in range(n) if A[0][j])
    grounds = [
        frozenset(i for i in range(n) if s[i])
        for s in sols
        if s[0] == 0
        and tuple(sorted(sum(s[p] for p in lines[li]) for li in star)) == (2, 2, 2, 2)
    ]
    assert len(grounds) == 9
    outs = [sorted(g - nb) for g in grounds]
    flat = [x for o in outs for x in o]
    assert len(set(flat)) == 27 and set(flat) == set(range(1, n)) - nb
    for o in outs:
        for i, a in enumerate(o):
            for b in o[i + 1 :]:
                assert not A[a][b], "out-triples must be pairwise non-collinear"
