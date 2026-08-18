"""Passes 7114-7121 -- what is actually known about alpha(W(3,9)), and two free corrections.

  7114  The Tallini bound applies at q=9 and BEATS this repo's own dual bound.
  7115  The repo's 51 is an incumbent with no stored witness -- it cannot re-verify it.
  7116  The published general lower bound for q=9 is 19, and q=9 is excluded from the
        good construction because 9 = 3^2.
  7117  The deficit reformulation: alpha = q^2-q+1 - C(q-2,2), same fit, better shape.
  7118  Why LNS rather than a fourth local-search class.
  7119  What a 52 would and would not mean.
  7120  What the exhaustive ILP is and is not doing.
  7121  Scope.

    py -3 analysis/w33_pass7114_7121_q9_state_of_play.py
"""

from __future__ import annotations

import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main() -> int:
    print("=" * 78)
    print("Passes 7114-7121 -- alpha(W(3,9)): the real state of play")
    print("=" * 78)

    print("\n  PASS 7114 -- Tallini beats the repo's own upper bound, for free\n")
    q = 9
    print(f"    Hoffman / ovoid size  q^2+1      = {q * q + 1}")
    print(f"    repo MILP dual bound (Pass 5658) = 80.84  ->  80")
    print(f"    Tallini  q^2-q+1  (q odd)        = {q * q - q + 1}   <-- PUBLISHED THEOREM")
    print(f"\n    repo recorded:  51 <= alpha(W(3,9)) <= 80")
    print(f"    corrected:      51 <= alpha(W(3,9)) <= {q * q - q + 1}")
    print(f"    the interval shrinks from {80 - 51} to {q * q - q + 1 - 51}, at zero cost")
    print("""
    PASS 5658 SPENT COMPUTE DERIVING A WEAKER BOUND THAN ONE ALREADY IN PRINT. Tallini's
    q^2-q+1 holds for every odd q, is cited in both papers this pass consulted, and gives 73
    where the repo's own MILP dual bound gave 80.84. Nothing was wrong with the computation;
    it was simply unnecessary, and its answer was worse.

    THIS IS THE CHEAPEST CLASS OF ERROR IN THE CORPUS and the easiest to keep making: the
    repo computes a bound it could have cited. A dual bound from a truncated MILP run is
    never better than a theorem, and is not evidence about the true value at all.""")

    print("\n  PASS 7115 -- the incumbent with no witness\n")
    print("""    PASS 5658 RECORDS alpha(W(3,9)) >= 51 "by construction", stored as the single
    integer 51 in a certificate field. THE POINTS WERE NOT SAVED. So the repo asserts a
    lower bound it cannot re-verify, cannot hand to anyone, and cannot extend -- the next
    search has to rediscover 51 before it can try for 52, which is exactly what happened.

    A LOWER BOUND IS A WITNESS, NOT A NUMBER. Storing the number keeps the claim and throws
    away the object, and an unstored witness is indistinguishable from a search bug. Every
    run in this pass writes its points out with the field encoding and the form, so the set
    can be re-checked by anyone from the JSON alone.""")

    print("\n  PASS 7116 -- the published lower bound, and why q=9 misses the good one\n")
    print("""    Ceria, De Beule, Pavese and Smaldore, "On large partial ovoids of symplectic
    and Hermitian polar spaces", arXiv:2203.04553, Table 1, for W(3,q) with q odd:

        lower  (q^{3/2} + 3q - q^{1/2} + 3)/3   for q = p^{2h}, p != 3
        lower  2q + 1                            for q = p^{2h+1} OR q = 3^h   [Tallini]
        upper  q^2 - q + 1                       [Tallini]

    q = 9 IS AN ODD SQUARE, WHICH LOOKS LIKE THE FIRST ROW -- and is excluded from it,
    because 9 = 3^2 has p = 3. It falls in the second row as q = 3^h, so the best PUBLISHED
    general lower bound at q=9 is 2q+1 = 19. (Had p != 3 been allowed, the formula would
    give (27+27-3+3)/3 = 18, which is smaller than 19 anyway at this q.)

    SO THE REPO'S 51, IF IT IS REAL, IS FAR ABOVE EVERY PUBLISHED GENERAL CONSTRUCTION AT
    q=9. That is a statement about general constructions only: Cimrakova-Fack's exhaustive
    method settled q=5 and q=7 and stopped there, and heuristic searches by others may well
    have gone past 19 at q=9 without appearing in that table. So this is NOT a novelty
    claim -- it is a reason to store the witness and let someone check it.""")

    print("\n  PASS 7117 -- the same fit, in a shape that could have a reason\n")
    print(f"    {'q':>3s} {'Tallini':>8s} {'alpha':>6s} {'deficit':>8s} {'C(q-2,2)':>9s}")
    for qq, a in ((3, 7), (5, 18), (7, 33)):
        T = qq * qq - qq + 1
        print(f"    {qq:3d} {T:8d} {a:6d} {T - a:8d} {comb(qq - 2, 2):9d}")
    print(f"\n    alpha(W(3,q)) = q^2 - q + 1 - C(q-2, 2)      [q odd, FITTED on 3 points]")
    print(f"    predictions:  q=9 -> {81 - 9 + 1 - comb(7, 2)}   q=11 -> "
          f"{121 - 11 + 1 - comb(9, 2)}   q=13 -> {169 - 13 + 1 - comb(11, 2)}")
    print("""
    THIS IS THE SAME QUADRATIC AS (q+4)(q-1)/2 and has exactly the same evidential status:
    NONE. Three coefficients, three data points, zero degrees of freedom.

    WHAT CHANGES IS THE SHAPE. Written as a deficit from Tallini, the correction is a
    BINOMIAL COEFFICIENT, C(q-2,2), which is the kind of quantity a counting obstruction
    produces -- pairs drawn from a set of size q-2. An arbitrary quadratic suggests nothing;
    a binomial deficit at least says where to look for a proof. That is a reason to write it
    down, not a reason to believe it.""")

    print("\n  PASS 7118-7120 -- method, and what each run can and cannot settle\n")
    print("""    LNS RATHER THAN A FOURTH LOCAL-SEARCH CLASS. Pass 5784 reports three local
    search classes all plateauing at 51. A fourth is not a plan. Large-neighbourhood search
    destroys a random slice of the incumbent and re-solves that slice EXACTLY by ILP, so it
    can perform a coordinated k-way exchange that no (1,2)-swap neighbourhood contains. That
    is a different move set, not more of the same one.

    THE EXHAUSTIVE ILP IS ASKING A FEASIBILITY QUESTION, not an optimisation one: is there
    an independent set of size 52? It fixes a non-collinear PAIR first, which is legitimate
    rather than heuristic -- the automorphism group is transitive on such pairs, so every
    partial ovoid is equivalent to one containing any chosen pair. At last check it had
    explored ~151,000 nodes with no feasible solution and no proof of infeasibility, which
    settles NOTHING in either direction.

    WHAT EACH OUTCOME WOULD MEAN. A verified 52 beats the repo's incumbent and matches the
    interpolation -- but matching a zero-degree-of-freedom fit at one point is weak
    evidence, and the honest claim would be "52 exists", not "the formula holds". A proof
    that 51 is optimal kills the formula outright and is the more informative outcome. A
    timeout means neither, and must be reported as neither.""")

    print("\n  PASS 7121 -- scope\n")
    print("""    ESTABLISHED HERE, independent of any search: Tallini's q^2-q+1 = 73 supersedes
    this repo's 80.84 dual bound at q=9; the repo's 51 has no stored witness; and the best
    published general lower bound at q=9 is 19 because 9 = 3^2 is excluded from the
    stronger construction.

    NOT ESTABLISHED: alpha(W(3,9)). NOT CLAIMED: that 51 is novel, or that the deficit
    formula is more than an interpolation.""")

    out = {
        "boundary": (
            "This pass establishes three things that need no search: Tallini's q^2-q+1 = 73 "
            "is a PUBLISHED bound that supersedes Pass 5658's 80.84 MILP dual bound at q=9; "
            "the repo's alpha >= 51 is stored as an integer with NO witness and cannot be "
            "re-verified; and the best published general lower bound at q=9 is 2q+1 = 19 "
            "because 9 = 3^2 is excluded from the (q^{3/2}+3q-q^{1/2}+3)/3 construction. "
            "alpha(W(3,9)) itself is NOT determined here, and the deficit formula "
            "q^2-q+1-C(q-2,2) is an interpolation with zero degrees of freedom"),
        "pass_7114": {
            "q": 9,
            "hoffman_q2_plus_1": 82,
            "repo_dual_bound_pass5658": 80.84,
            "tallini_q2_minus_q_plus_1": 73,
            "corrected_interval": [51, 73],
            "previous_interval": [51, 80],
            "lesson": ("a dual bound from a truncated MILP run is never better than a "
                       "theorem; the repo computed a bound it could have cited")},
        "pass_7115": {
            "repo_lower_bound": 51,
            "witness_stored": False,
            "consequence": ("the bound cannot be re-verified, handed on, or extended; the "
                            "next search must rediscover 51 before trying 52"),
            "rule": "a lower bound is a witness, not a number"},
        "pass_7116": {
            "citation": ("M. Ceria, J. De Beule, F. Pavese, V. Smaldore, On large partial "
                         "ovoids of symplectic and Hermitian polar spaces, arXiv:2203.04553, "
                         "Table 1"),
            "lower_bound_odd_square_p_ne_3": "(q^{3/2}+3q-q^{1/2}+3)/3",
            "lower_bound_q_eq_3_pow_h": "2q+1 = 19 at q=9",
            "why_q9_excluded": "9 = 3^2 has p = 3, and the stronger row requires p != 3",
            "upper_bound": "q^2-q+1 = 73",
            "novelty_status": ("NOT a novelty claim -- Cimrakova-Fack settled q=5,7 "
                               "exhaustively and stopped; heuristic searches by others may "
                               "exceed 19 at q=9 without appearing in that table")},
        "pass_7117": {
            "formula": "alpha(W(3,q)) = q^2 - q + 1 - C(q-2,2), q odd",
            "equivalent_to": "(q+4)(q-1)/2",
            "fitted_on": {"3": 7, "5": 18, "7": 33},
            "degrees_of_freedom": 0,
            "evidential_status": "NONE",
            "why_written_down": ("the deficit is a BINOMIAL COEFFICIENT, which is what a "
                                 "counting obstruction over pairs from a (q-2)-set "
                                 "produces -- it says where to look for a proof"),
            "predictions": {"9": 52, "11": 75, "13": 102}},
        "pass_7118_7120": {
            "method": "large-neighbourhood search: destroy a slice, re-solve it exactly",
            "why_not_more_local_search": ("Pass 5784 reports three local-search classes all "
                                          "plateauing at 51; LNS is a different move set, "
                                          "capable of coordinated k-way exchanges"),
            "ilp_reduction": ("fixes a non-collinear pair -- legitimate, since the "
                              "automorphism group is transitive on such pairs"),
            "ilp_status_at_writing": "~151,000 nodes, no feasible 52, no infeasibility proof",
            "outcome_semantics": {
                "verified_52": "beats the incumbent; weak evidence for the formula",
                "proof_51_optimal": "kills the formula; the more informative outcome",
                "timeout": "settles neither, and must be reported as neither"}},
        "pass_7121": {"not_established": ["alpha(W(3,9))"],
                      "not_claimed": ["that 51 is novel",
                                      "that the deficit formula is more than a fit"]},
    }
    fp = ROOT / "data" / "PART_W33_PASS7114_7121_Q9_STATE_OF_PLAY.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
