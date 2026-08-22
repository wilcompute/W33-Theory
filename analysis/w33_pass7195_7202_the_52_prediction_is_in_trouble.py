"""Passes 7195-7202 -- my own 52 prediction, tested hard, and now in serious trouble.

  7195  LNS with exact ILP repair, and the calibration that qualifies it.
  7196  What the known optima look like -- and why their incidence data says nothing.
  7197  q=9: 51 in three seconds, then 16,624 iterations of nothing.
  7198  The certified basin: radius 6, by ILP infeasibility rather than by plateau.
  7199  The arithmetic that favours 52, weighed honestly against the search that favours 51.
  7200  Downgrading my own prediction.
  7201  What would actually settle it.
  7202  Scope.

    py -3 analysis/w33_pass7195_7202_the_52_prediction_is_in_trouble.py
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


def main() -> int:
    print("=" * 78)
    print("Passes 7195-7202 -- the 52 prediction, tested hard")
    print("=" * 78)

    print("\n  PASS 7195 -- the tool, and why it is qualified to speak\n")
    print("""    LARGE-NEIGHBOURHOOD SEARCH WITH AN EXACT REPAIR OPERATOR. Destroy k points of the
    incumbent (k ~ 6..22), then take every point non-collinear with all survivors and solve a
    TRUE maximum independent set among them by ILP. The repair is optimal, so the move is far
    larger than the (1,2)- and (1,3)-swaps this repo had tried, and every incumbent is a valid
    partial ovoid by construction rather than by scoring.

    IT IS QUALIFIED BECAUSE IT WAS CALIBRATED. At q=7 it reaches the known optimum 33 in
    FIVE SECONDS and nine iterations -- precisely where Pass 7192 proved orbit methods cap at
    30, and where a plain 400-variable ILP timed out without closing. A method that solves the
    hardest case with a known answer is entitled to an opinion about the case without one.""")

    print("\n  PASS 7196 -- the optima carry no combinatorial signature\n")
    print(f"      {'q':>3s}  {'alpha':>5s}  {'lines missed':>12s}  {'(q+1)(q^2+1-alpha)':>19s}"
          f"  {'max tangent':>11s}  {'q+1':>4s}")
    for q, a, miss in ((3, 7, 12), (5, 18, 48), (7, 33, 136)):
        print(f"      {q:3d}  {a:5d}  {miss:12d}  {(q + 1) * (q * q + 1 - a):19d}"
              f"  {q + 1:11d}  {q + 1:4d}")
    print("""
    BOTH COLUMNS ARE FORCED. The line distribution is exactly (q+1)(q^2+1-alpha) -- it is
    alpha restated, carrying no independent information, which is why no fitted formula
    matched it. The maximum tangent is q+1 because a point lies on q+1 lines each meeting the
    ovoid at most once; it is the trivial ceiling, merely attained. And the minimum tangent
    is 2 in every case, which is precisely the statement that no single point can be swapped
    in -- local optimality, not structure.

    SO THE OPTIMA HAVE NO VISIBLE SIGNATURE TO GENERALISE. That is consistent with Pass 7192:
    asymmetric objects should not be expected to have one. It closes the "find the pattern and
    build q=9 directly" route, which was the plan going in.""")

    print("\n  PASS 7197-7198 -- q=9, and a plateau converted into a certificate\n")
    print("""    FOUR INDEPENDENT LNS RUNS reached 51 within three seconds and never improved:
    one of them ran 16,624 iterations. This repo's earlier local searches plateau at 51 across
    three separate move classes. A 3000-second feasibility ILP for 52 returned primal bound
    `inf` -- it found nothing and proved nothing.

    A PLATEAU IS NOT A THEOREM, so it was made into one locally. For a known 51-set S, a
    single ILP per d asks whether any 52-set agrees with S in at least 51-d points:

        d = 0,1,2,3,4,5,6   ALL INFEASIBLE
        d = 7               did not resolve in the time given -- no conclusion

    CERTIFIED RADIUS 6. Every 52-point partial ovoid of W(3,9), if one exists, differs from
    this 51-set in MORE than 6 points. This is infeasibility, not search failure.

    THE OTHER LANE REACHED RADIUS 5 in a different formulation (a 512-state residual model
    rather than the 820-point projective one), by deletion depth from a 42-state core. Two
    independent models, two independent radii, same conclusion and neither closing it.""")

    print("\n  PASS 7199-7200 -- weighing it, and downgrading my own prediction\n")
    print(f"      {'q':>3s}  {'alpha':>16s}  {'1st diff':>9s}  {'2nd diff':>9s}")
    rows = [(3, "7", "", ""), (5, "18", "11", ""), (7, "33", "15", "4"),
            (9, "51 or 52?", "18 or 19", "3 or 4")]
    for q, a, d1, d2 in rows:
        print(f"      {q:3d}  {a:>16s}  {d1:>9s}  {d2:>9s}")
    print("""
    THE ONLY THING THAT EVER SUPPORTED 52 was that it continues a quadratic. Three points
    determine a quadratic exactly, so that fit had ZERO degrees of freedom and was never
    evidence -- I said so when I made the prediction, and it is worth repeating now that the
    prediction is losing.

    AGAINST IT: four independent runs of a method that solves q=7 in five seconds, stuck at
    51; three earlier move classes in this repo, stuck at 51; and a certified radius-6 basin
    that no 52-set can enter.

    I AM DOWNGRADING MY OWN PREDICTION. alpha(W(3,9)) = 52 was a clean falsifiable guess and
    the evidence has moved decisively against it. It is not refuted -- a 52-set could sit far
    from every incumbent found -- but it should no longer be quoted as the expected value. The
    honest statement of the interval is unchanged and remains

        51 <= alpha(W(3,9)) <= 73    (Tallini)

    with 51 now supported by four independent searches and a local infeasibility certificate,
    rather than by one plateau.""")

    print("\n  PASS 7201 -- what would actually settle it\n")
    print("""    NOT more local search. Four runs agreeing tells us little more than one did.

    The two things that would settle it: an exhaustive argument that 51 is optimal, which at
    820 points needs isomorph rejection of the kind Cimrakova-Fack used at 400 and is the real
    reason q=9 was left undone in 2005; or a CONSTRUCTION of 52, which after Pass 7196 has no
    structural pattern left to imitate and after Pass 7192 no symmetry to exploit.

    A cheaper intermediate that is worth doing: push the certified radius past 6. Each
    additional d is one ILP, and the sequence of solve times says how far this can go before
    the method exhausts itself.""")

    print("\n  PASS 7202 -- scope\n")
    print("""    PROVED HERE: nothing about alpha(W(3,9)). CERTIFIED here: no 52-set agrees with
    one specific 51-set in 45 or more points. MEASURED here: four independent LNS runs plateau
    at 51 while the same code solves q=7 exactly.

    NOT DONE: alpha(W(3,9)); any improvement on Tallini's 73; a 52-set; a proof of 51.""")

    out = {
        "boundary": (
            "NOTHING is proved about alpha(W(3,9)). Certified: no 52-point partial ovoid "
            "agrees with one specific 51-set in >= 45 points (ILP infeasibility, d = 0..6; "
            "d = 7 did not resolve). Measured: four independent LNS runs plateau at 51 while "
            "the same code solves q=7 exactly in five seconds. The prediction alpha = 52, "
            "made from a zero-degrees-of-freedom quadratic, is DOWNGRADED -- not refuted"),
        "pass_7195": {
            "method": "large-neighbourhood search, destroy k=6..22, exact ILP repair",
            "calibration": {"q7_optimum": 33, "found_in": "5 seconds, 9 iterations",
                            "contrast": ("orbit methods PROVED to cap at 30; plain ILP "
                                         "timed out without closing")},
            "validity": "every incumbent is a partial ovoid by construction, not by scoring"},
        "pass_7196": {
            "line_distribution_is_forced": {
                "identity": "lines missed = (q+1)(q^2+1-alpha)",
                "checked": {"q=3": [12, 12], "q=5": [48, 48], "q=7": [136, 136]},
                "consequence": "carries no information independent of alpha"},
            "max_tangent": {"observed": {"q=3": 4, "q=5": 6, "q=7": 8},
                            "equals": "q+1",
                            "why_trivial": ("a point lies on q+1 lines, each meeting the "
                                            "ovoid at most once -- the ceiling, attained")},
            "min_tangent": {"observed": 2,
                            "meaning": "local optimality (no single-point swap), not structure"},
            "consequence": ("the optima have no combinatorial signature to generalise, "
                            "closing the 'find the pattern, build q=9' route")},
        "pass_7197_7198": {
            "lns_runs": 4, "all_reached": 51, "best_run_iterations": 16624,
            "improvement_after_first_seconds": 0,
            "certified_basin": {"radius": 6, "method": "one ILP per d, infeasibility",
                                "statement": ("every 52-set, if any exists, differs from "
                                              "this 51-set in more than 6 points"),
                                "d7": "did not resolve -- no conclusion"},
            "other_lane": {"radius": 5, "model": "512-state residual, 42-state core",
                           "note": "independent formulation, same non-closure"}},
        "pass_7199_7200": {
            "downgraded": "alpha(W(3,9)) = 52",
            "why_it_was_never_evidence": "three points determine a quadratic; zero DoF",
            "evidence_against": ["four independent LNS runs plateau at 51",
                                 "three earlier move classes in this repo plateau at 51",
                                 "certified radius-6 basin excluding 52"],
            "not_refuted": "a 52-set could lie far from every incumbent found",
            "interval": "51 <= alpha(W(3,9)) <= 73 (Tallini), unchanged"},
        "pass_7201": {
            "would_settle_it": ["exhaustive optimality proof with isomorph rejection at 820 "
                                "points -- the reason q=9 was left undone in 2005",
                                "an explicit 52-set"],
            "cheap_next": "push the certified radius past 6, one ILP per d"},
        "not_done": ["alpha(W(3,9))", "any improvement on Tallini's 73", "a 52-set",
                     "a proof that 51 is optimal"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7195_7202_52_IN_TROUBLE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
