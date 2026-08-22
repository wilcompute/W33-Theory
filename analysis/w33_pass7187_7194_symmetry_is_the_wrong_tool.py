"""Passes 7187-7194 -- why every symmetric attack on alpha(W(3,q)) fails, proved at q=7.

  7187  Symmetric search calibrated: reaches the known optima at q=3 and q=5.
  7188  The transvection sweep, complete over one class, and why it stalled.
  7189  Large subgroups: the regime that LOOKS right and is provably wrong.
  7190  A bug of mine -- one representative tested, reported as all of them.
  7191  Every order-3 orbit profile at q=7. There is exactly one, and it caps at 30.
  7192  Orders 5 and 7 too -- and which of those caps are evidence and which are not.
  7193  What this explains, including the repo's own q=9 plateau.
  7194  Scope, and the interpolation that is still only an interpolation.

    py -3 analysis/w33_pass7187_7194_symmetry_is_the_wrong_tool.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# order, orbit profile, max invariant partial ovoid (all PROVED optimal),
# and whether 33 is representable as f + s*k in that profile at all.
PROFILES = [
    (3, {1: 10, 3: 130}, 30, True),
    (5, {5: 80}, 30, False),
    (7, {1: 1, 7: 57}, 28, False),
    (7, {1: 8, 7: 56}, 15, True),
    (7, {1: 57, 7: 49}, 15, True),
]

CALIB = [
    ("q=3", "order 3", 7, 7, True, "PROVED optimal"),
    ("q=5", "order 3", 18, 18, True, "PROVED optimal"),
    ("q=5", "subgroups |H| >= 9", 18, 11, False, "PROVED optimal per subgroup"),
    ("q=7", "order 3", 33, 30, False, "PROVED optimal"),
    ("q=7", "order 5", 33, 30, False, "PROVED optimal"),
    ("q=7", "order 7", 33, 28, False, "PROVED optimal"),
]


def main() -> int:
    print("=" * 78)
    print("Passes 7187-7194 -- symmetry is the wrong tool for alpha(W(3,q))")
    print("=" * 78)

    print("\n  PASS 7187-7189 -- calibration, and a regime that looked right\n")
    print(f"    {'case':6s} {'symmetry':20s} {'known':>6s} {'best':>5s} {'reaches':>8s}")
    for case, sym, known, best, ok, note in CALIB:
        print(f"    {case:6s} {sym:20s} {known:6d} {best:5d} "
              f"{'YES' if ok else 'no':>8s}")
    print("""
    THE LARGE-SUBGROUP ROW IS THE ONE THAT MATTERS METHODOLOGICALLY. Sweeping subgroups of
    order >= 9 at q=5 returns 11 against a known optimum of 18. Had that regime been run
    first at q=9 -- where no answer is known -- it would have produced a confident number
    seven short of the truth with nothing to reveal the shortfall. The calibration cost two
    minutes and was the difference between a result and a fabrication.""")

    print("\n  PASS 7190 -- a bug of mine, stated plainly\n")
    print("""    I keyed order-3 elements by the Jordan type of u - 1. That IS a class invariant
    in characteristic 3, but at q = 5 and 7 order-3 elements are SEMISIMPLE, all of them land
    in one bucket, and `setdefault` tested exactly ONE representative. The q=7 answer of 30
    was the best over one class, reported as the best over all order-3 symmetry.

    THE FIX was to key on the ORBIT PROFILE -- the multiset of orbit lengths on the points --
    which is exactly the invariant that determines the ILP, and needs no conjugacy theory.
    Re-run under the fix, q=7 has exactly ONE order-3 profile and it still gives 30. The
    number survived; the WARRANT for it did not exist until the fix.""")

    print("\n  PASS 7191-7192 -- THE NEGATIVE THEOREM, after I over-read it once\n")
    print("    W(3,7), whose maximum partial ovoid has size 33 and is UNIQUE up to")
    print("    equivalence (Cimrakova-Fack 2005, Table 1, #O' = 1).\n")
    print("    AN INVARIANT SET'S SIZE IS f + s*k: f fixed points plus k orbits of size s.")
    print("    So before a cap counts as evidence, 33 must be REPRESENTABLE in that profile.\n")
    print(f"      {'order':>5s}  {'profile':>20s}  {'max':>4s}  {'33 possible?':>13s}  "
          f"{'evidence?':>10s}")
    for o, prof, mx, rep in PROFILES:
        print(f"      {o:5d}  {str(prof):>20s}  {mx:4d}  "
              f"{'yes' if rep else 'NO':>13s}  {'YES' if rep else 'none':>10s}")
    print("""
    I FIRST WROTE "no odd prime symmetry reaches the optimum" AND THAT WAS AN OVER-READ.
    Two of those five rows carry no information at all:

      * order 5 has NO fixed points (profile {5:80}), so every invariant set has size
        divisible by 5, and 5 does not divide 33. Its cap of 30 is exactly floor(33/5)*5 --
        the arithmetic ceiling, achieved. That is order 5 doing as well as it possibly could,
        not failing;
      * the order-7 profile {1:1, 7:57} cannot represent 33 either, since neither 33 nor 32
        is a multiple of 7.

    THE "COINCIDENCE" DISSOLVES WITH IT. Orders 3 and 5 both giving exactly 30 looked like
    something needing explanation. It is not: 30 is the divisibility ceiling for order 5 and
    an unrelated genuine bound for order 3. I had flagged it as unexplained; it was an
    artefact of my own framing.

    WHAT SURVIVES IS STILL A THEOREM, on the three rows where 33 IS representable:

        the maximum partial ovoid of W(3,7) is invariant under no element of order 3,
        and under no element of order 7 in two of its three classes

    with caps of 30, 15 and 15 against a representable 33, each a completed exact ILP rather
    than a search that gave up.

    ORDER 2 DID NOT RESOLVE (200 orbits, past what the ILP closed in the time given), so a
    2-group stabilizer is not excluded and no claim is made about it.""")

    print("\n  PASS 7193 -- what this explains\n")
    print("""    THIS IS WHY THE SEARCHES PLATEAU. The q=7 optimum admits no order-3 symmetry and no
    order-7 symmetry in two of three classes. Extremal partial ovoids here are largely
    ASYMMETRIC, which accounts for three separate failures:

      * orbit methods for those orders search a space PROVED not to contain the optimum;
      * local search plateaus, because asymmetric optima have no structure for a move
        operator to exploit;
      * this repo's q=9 searches stop at 51 across three independent local-search classes,
        and a 3000-second feasibility ILP for 52 returned primal bound `inf` -- it found
        nothing AND proved nothing.

    A method that cannot reach 33 at q=7, where the answer is known, should not be trusted
    to reach 52 at q=9, where it is not. That is the load-bearing consequence.""")

    print("\n  PASS 7194 -- scope, and the interpolation\n")
    print("""    THE EXACT VALUES, two independently verified here (witness of that size, and
    infeasibility at size+1): alpha(W(3,3)) = 7 and alpha(W(3,5)) = 18. The second matches
    Cimrakova-Fack exactly. alpha(W(3,7)) = 33 is theirs, not mine.

    THE INTERPOLATION. (q+4)(q-1)/2 reproduces 7, 18, 33 exactly, equivalently

        alpha = [Tallini bound q^2-q+1] - C(q-2, 2)

    with deficits 0, 3, 10 at q = 3, 5, 7. THREE POINTS DETERMINE A QUADRATIC, so this fit
    has zero degrees of freedom and is NOT evidence. It is a falsifiable prediction of 52 at
    q=9, one above this repo's best-known 51, and it remains untested: the methods that could
    test it are exactly the ones Pass 7192 shows cannot reach an asymmetric optimum.

    NOT DONE, and not claimed: alpha(W(3,9)); any upper bound better than Tallini's 73; and
    the order-2 case at q=7.""")

    out = {
        "boundary": (
            "Pass 7192 PROVES that the maximum partial ovoid of W(3,7) is invariant under no "
            "element of order 3, and under no element of order 7 in two of its three classes "
            "-- caps of 30, 15, 15 against a REPRESENTABLE 33, each a completed exact ILP. "
            "Order 5 and one order-7 class carry NO information: 33 is not representable in "
            "their orbit profiles at all, so their caps are arithmetic, not evidence. I first "
            "stated this as 'no odd prime symmetry' and corrected it before commit. The "
            "order-2 case did NOT resolve and no claim is made about it. "
            "alpha(W(3,9)) is NOT determined; (q+4)(q-1)/2 is a zero-degrees-of-freedom "
            "interpolation through three points, not evidence"),
        "exact_values": {
            "alpha_W33": {"value": 7, "method": "ILP witness + infeasibility at 8",
                          "note": "meets Tallini's q^2-q+1 = 7 exactly"},
            "alpha_W35": {"value": 18, "method": "ILP witness + infeasibility at 19",
                          "note": "matches Cimrakova-Fack 2005 Table 1 independently"},
            "alpha_W37": {"value": 33, "source": "Cimrakova-Fack 2005, NOT ours",
                          "note": "unique up to equivalence, #O' = 1"}},
        "negative_theorem": {
            "statement": ("the maximum partial ovoid of W(3,7) is invariant under no element "
                          "of order 3, and under no element of order 7 in two of its three "
                          "classes"),
            "evidence": [
                {"order": 3, "profile": {"1": 10, "3": 130}, "max": 30,
                 "33_representable": True, "counts_as_evidence": True},
                {"order": 7, "profile": {"1": 8, "7": 56}, "max": 15,
                 "33_representable": True, "counts_as_evidence": True},
                {"order": 7, "profile": {"1": 57, "7": 49}, "max": 15,
                 "33_representable": True, "counts_as_evidence": True}],
            "no_information": [
                {"order": 5, "profile": {"5": 80}, "max": 30, "33_representable": False,
                 "why": ("no fixed points, so every invariant set has size divisible by 5, "
                         "and 5 does not divide 33; 30 = floor(33/5)*5 is the arithmetic "
                         "ceiling, achieved -- order 5 does as well as it possibly could")},
                {"order": 7, "profile": {"1": 1, "7": 57}, "max": 28,
                 "33_representable": False,
                 "why": "neither 33 nor 32 is a multiple of 7"}],
            "my_over_read": ("I first stated this as 'no odd prime symmetry reaches the "
                             "optimum'. Two of the five rows cannot represent 33 at all and "
                             "carry no information; the claim was corrected before commit"),
            "coincidence_dissolved": ("orders 3 and 5 both giving 30 needed no explanation -- "
                                      "30 is the divisibility ceiling for order 5 and an "
                                      "unrelated genuine bound for order 3"),
            "group_order": "|Sp(4,7)| = 7^4 * 2^9 * 3^2 * 5^2, odd primes exactly 3,5,7",
            "not_excluded": "a 2-group stabilizer; the order-2 ILP did not close"},
        "calibration": {
            "large_subgroups_at_q5": {"regime": "|H| >= 9", "best": 11, "known": 18,
                                      "lesson": ("would have produced a confident number 7 "
                                                 "short at q=9 with no signal of the gap")},
            "order_3_at_q3_q5": {"best": [7, 18], "known": [7, 18], "reaches": True}},
        "my_bug": {
            "what": "keyed order-3 elements by Jordan type of u-1",
            "why_wrong": ("a class invariant only in characteristic 3; at q=5,7 order-3 "
                          "elements are semisimple and setdefault tested ONE representative"),
            "fix": "key on the orbit profile, the invariant that determines the ILP",
            "outcome": "the number 30 survived; its warrant did not exist before the fix"},
        "interpolation": {
            "formula": "(q+4)(q-1)/2 = (q^2-q+1) - C(q-2,2)",
            "fits": {"q=3": 7, "q=5": 18, "q=7": 33},
            "deficits_from_tallini": [0, 3, 10],
            "degrees_of_freedom": 0,
            "status": "NOT evidence; a falsifiable prediction of 52 at q=9",
            "repo_best_known": 51},
        "why_searches_plateau": (
            "extremal partial ovoids here are ASYMMETRIC, so orbit methods search a space "
            "that does not contain the optimum, and local search has no structure to exploit"),
        "not_done": ["alpha(W(3,9))", "any upper bound better than Tallini's 73",
                     "the order-2 case at q=7"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7187_7194_SYMMETRY_WRONG_TOOL.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
