#!/usr/bin/env python3
"""Pass 1099: the exact Kochen-Specker maximum for W(3,3) is 36, and that
vindicates the demonstrator's 1/10 -- while Pass 1098 was wrong.

TWO THINGS AT ONCE, and the first is a retraction of my own pass from an hour ago.

RETRACTION OF PASS 1098.  Pass 1098 asked what observable the demonstrator's 1/10
target could be, modelled "a classical assignment satisfying contexts" as a PARTIAL
OVOID (pairwise non-collinear points), computed the maximum partial ovoid of W(3,3)
to be 7, and concluded that only 4*7 = 28 of the 40 contexts are satisfiable, for a
defect of 3/10.  The maximum partial ovoid is indeed 7 -- but the model is wrong,
and it is wrong in a way the corpus had already recorded.

A context is SATISFIED when it contains exactly one marked ray.  A partial ovoid
gets every context it touches, but it can only touch 4m of them.  A larger marking
may put two marks on some contexts -- losing those -- while hitting many more
exactly once.  Restricting to partial ovoids is not a conservative simplification;
it is a different and strictly weaker optimisation.

BT818 T2 had already found a marking of size 13 satisfying 36 of the 40 contexts,
and had already flagged that 36 = (q!)^2 = the spread count.  My Pass 1098 did not
cite it.  The rediscovery guard could not have caught this: the colliding results
are the bare integers 7 and 36, and bare integers are excluded from the guard's
token classes by deliberate calibration (Pass 328 measured that they flag 78% of
files).  This is the guard's known blind spot, hit for real.

WHAT THIS PASS ADDS.  BT818 left the exact maximum open -- "True maximum lies in
[36, 39] (40 is impossible: an exactly-once marking of all contexts is an ovoid)".
That bracket is now closed by exact integer programming:

    the maximum number of simultaneously satisfiable contexts is EXACTLY 36,

so the defect is exactly 4/40 = 1/10.

The encoding is exact and the optimum is certified by the solver, not sampled.
With x_p in {0,1} marking rays and y_L in {0,1} claiming context L is satisfied,
"y_L = 1 iff exactly one ray of L is marked" is enforced by the two linear
inequalities

    y_L <= sum_{p in L} x_p          (so y_L = 1 forces at least one mark)
    3 y_L + sum_{p in L} x_p <= 4    (so y_L = 1 forces at most one)

which are tight at every value: sum = 0 gives y <= 0; sum = 1 gives y <= 1;
sum >= 2 gives y <= 2/3, hence 0.

CONSEQUENCE FOR THE DEMONSTRATOR.  The preregistered 1/10 is the RIGHT NUMBER for
this observable, and Pass 1080 remains correct that it is not the Abramsky-Barbosa
contextual fraction (which is 1, by strong contextuality).  The two coexist:

    Abramsky-Barbosa contextual fraction    = 1      (Pass 1080)
    KS satisfiability defect (this pass)    = 1/10

The preregistration's DERIVATION is still not rehabilitated -- "1 - (q!)^2/v" with
(q!)^2 asserted to be the satisfiable count was numerology, and BT818 had already
noted the 36 = (q!)^2 coincidence without claiming it was a derivation.  What
changes is that the target value now has an exact combinatorial meaning, so the
demonstrator has something real to measure.

PRIOR ART -- cited, not reclaimed:
  * analysis/BT818_ovoid_nogo_theta_gap.md OWNS: alpha(W(3,3)) = 7, the >= 36
    marking of size 13, the [36,39] bracket, the impossibility of 40, and the
    observation 36 = (q!)^2.  This pass closes its open question and claims
    nothing else from it.
  * analysis/w33_pass1098_what_one_tenth_measures.py -- retracted here.
  * analysis/w33_pass1080_contextual_fraction_audit.py -- CF = 1; unaffected.
  * data/w33_pass1086_contextuality_claim_firewall.json (parallel track) --
    retired the CF label; this supplies the replacement identification.
  * analysis/w33_ovoid_construct.py -- owns the contextuality statement.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1099_exact_ks_maximum.json"


def build(q: int):
    def canon(v):
        for a in v:
            if a % q:
                inv = pow(a % q, -1, q)
                return tuple((inv * x) % q for x in v)
        return None

    pts, seen = [], set()
    for v in itertools.product(range(q), repeat=4):
        if any(v):
            c = canon(v)
            if c not in seen:
                seen.add(c)
                pts.append(c)
    idx = {p: i for i, p in enumerate(pts)}

    def form(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % q

    lines = set()
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if form(pts[i], pts[j]) == 0:
                span = set()
                for a in range(q):
                    for b in range(q):
                        w = tuple((a * pts[i][k] + b * pts[j][k]) % q
                                  for k in range(4))
                        if any(w):
                            span.add(idx[canon(w)])
                if len(span) == q + 1:
                    lines.add(frozenset(span))
    return pts, [sorted(L) for L in sorted(lines, key=sorted)]


def exact_ks_maximum(pts, lines):
    """Maximum number of contexts satisfiable at once, by exact ILP."""
    P, L = len(pts), len(lines)
    n = P + L
    rows, ub = [], []
    for li, Ln in enumerate(lines):
        r = np.zeros(n); r[P + li] = 1.0
        for p in Ln:
            r[p] -= 1.0
        rows.append(r); ub.append(0.0)
        r = np.zeros(n); r[P + li] = 3.0
        for p in Ln:
            r[p] += 1.0
        rows.append(r); ub.append(4.0)
    c = np.zeros(n); c[P:] = -1.0
    res = milp(c=c,
               constraints=LinearConstraint(np.array(rows),
                                            -np.inf * np.ones(len(ub)),
                                            np.array(ub)),
               integrality=np.ones(n), bounds=Bounds(0, 1))
    x = np.round(res.x).astype(int)
    marking = [i for i in range(P) if x[i]]
    # recount from the marking itself, never from the objective
    satisfied = sum(1 for Ln in lines if sum(x[p] for p in Ln) == 1)
    return res, satisfied, marking


def main() -> int:
    pts, lines = build(3)
    res, satisfied, marking = exact_ks_maximum(pts, lines)
    total = len(lines)
    defect = Fraction(total - satisfied, total)

    checks = {}
    checks["forty_points_forty_contexts"] = len(pts) == 40 and total == 40
    checks["solver_proved_optimality"] = res.status == 0
    checks["objective_matches_independent_recount"] = (
        int(round(-res.fun)) == satisfied)
    # BT818's bracket, closed
    checks["at_least_36_as_BT818_found"] = satisfied >= 36
    checks["at_most_39_as_BT818_bounded"] = satisfied <= 39
    checks["exact_maximum_is_36"] = satisfied == 36
    checks["defect_is_one_tenth"] = defect == Fraction(1, 10)
    # and the retraction of Pass 1098
    checks["pass1098_partial_ovoid_model_is_beaten"] = satisfied > 28
    checks["so_defect_is_NOT_three_tenths"] = defect != Fraction(3, 10)

    out = {
        "schema": "w33.pass1099.exact_ks_maximum.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "retracts": (
            "analysis/w33_pass1098_what_one_tenth_measures.py -- its 3/10 came "
            "from restricting classical assignments to partial ovoids, which is "
            "not the right optimisation. A marking may place two marks on a "
            "context, losing it, while hitting many more exactly once."),
        "headline": (
            f"The exact Kochen-Specker maximum for W(3,3) is {satisfied} of "
            f"{total} contexts, certified optimal by integer programming. This "
            f"closes BT818's open bracket [36,39]. The defect is therefore "
            f"{defect}, so the demonstrator's preregistered 1/10 is the right "
            f"number for this observable -- while Pass 1080 remains correct that "
            f"1/10 is not the Abramsky-Barbosa contextual fraction, which is 1. "
            f"Pass 1098's 3/10 is withdrawn."),
        "exact_maximum_satisfiable_contexts": satisfied,
        "total_contexts": total,
        "defect": str(defect),
        "witness_marking": sorted(marking),
        "witness_marking_size": len(marking),
        "two_quantities_that_coexist": {
            "abramsky_barbosa_contextual_fraction": 1,
            "ks_satisfiability_defect": str(defect),
            "why_both": (
                "CF = 1 because no global section exists at all (W(3,3) has no "
                "ovoid), which is a statement about exact colourings. The KS "
                "defect asks instead how CLOSE one can get, and the answer is "
                "36/40. A model can be maximally contextual in the sheaf sense "
                "and still admit a marking that misses only four contexts."),
        },
        "derivation_still_not_rehabilitated": (
            "The preregistration reached 1/10 as 1 - (q!)^2/v, asserting (q!)^2 = "
            "36 to be the satisfiable count. That was numerology and BT818 had "
            "already flagged 36 = (q!)^2 as a coincidence rather than a "
            "derivation. The value is now confirmed by exact optimisation; the "
            "route to it is not."),
        "prior_art": [
            "analysis/BT818_ovoid_nogo_theta_gap.md -- OWNS alpha=7, the >=36 "
            "marking, the [36,39] bracket, 40 impossible, and 36=(q!)^2",
            "analysis/w33_pass1098_what_one_tenth_measures.py -- retracted here",
            "analysis/w33_pass1080_contextual_fraction_audit.py -- CF=1, unaffected",
            "data/w33_pass1086_contextuality_claim_firewall.json -- retired the label",
        ],
        "guard_note": (
            "The rediscovery guard could not have caught Pass 1098's collision "
            "with BT818: the shared results are the bare integers 7 and 36, and "
            "bare integers are excluded from the guard's token classes by "
            "deliberate calibration (Pass 328 measured that they flag 78% of "
            "files). This is a real instance of that known blind spot, and it "
            "cost one pass."),
        "scope": (
            "Exact integer programming over the 40 rays and 40 contexts of "
            "W(3,3), with the exactly-once condition encoded by two tight linear "
            "inequalities per context. The optimum is certified by the solver and "
            "independently recounted from the returned marking. No claim is made "
            "about q != 3 and none about what the hardware measures."),
        "checks": checks,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": out["status"],
                      "exact_maximum": satisfied,
                      "defect": str(defect),
                      "marking_size": len(marking),
                      "checks": checks}, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
