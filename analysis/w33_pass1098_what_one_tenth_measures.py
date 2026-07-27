#!/usr/bin/env python3
"""Pass 1098: what the demonstrator's 1/10 target would have to be, and whether
the geometry supplies it.

WHERE THIS LEFT OFF.  Pass 1080 showed that 1/10 is not the Abramsky-Barbosa
contextual fraction (which is 1 for W(3,3), because a global section is an ovoid
and W(3,3) has none).  The parallel track's Pass 1086 accepted that, retired the
name, and relabelled 1/10 an "unidentified demonstrator click-rate target".
Something preregistered but unidentified is worse than either a prediction or
nothing, so this pass asks what quantity it could be, and computes that quantity.

THE ONE READING THAT IS NOT ARBITRARY.  The retracted derivation was

    CF = 1 - (q!)^2 / v = 1 - 36/40 = 4/40 = 1/10,

with 36/40 called "the maximum fraction of measurement contexts that CAN be
satisfied by a classical 0/1 colouring".  Read literally that is a real,
computable quantity, and a natural observable: the contexts are the 40 lines, a
classical assignment is a PARTIAL OVOID (a set of pairwise non-collinear points),
and because every point lies on exactly q+1 = 4 lines and a partial ovoid puts no
two points on a common line, a partial ovoid of size m satisfies exactly 4m
distinct contexts.  So

    satisfiable contexts = 4 * (max partial ovoid),
    unsatisfiable fraction = (40 - 4m) / 40.

For that fraction to be 1/10 requires 4m = 36, i.e. **m = 9**.

So the preregistration is testable after all, and this pass tests it: compute the
maximum partial ovoid of W(3,3) exactly.  If m = 9 the 1/10 target is recovered
with a genuine derivation.  If not, 1/10 is refuted in the one reading that gave
it geometric content, and the correct number is reported instead.

The doily is computed the same way as a control, where the answer is known: q = 2
is even, ovoids exist, so m should reach the full ovoid size st+1 = 5 and the
unsatisfiable fraction should be 0.

PRIOR ART -- cited, not reclaimed:
  * analysis/w33_pass1080_contextual_fraction_audit.py -- CF = 1, and the
    demolition of the "three independent routes".
  * data/w33_pass1086_contextuality_claim_firewall.json (parallel track) --
    accepted that and retired the label.
  * analysis/bt1901_cf_preregistration_audit.py -- the source of 36/40.
  * analysis/w33_ovoid_construct.py -- OWNS the contextuality statement and
    already records a partial-ovoid obstruction for q = 3.
  * Thas (1981) -- W(q) has ovoids iff q is even.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1098_what_one_tenth_measures.json"


def build(q: int):
    """Points and totally isotropic lines of W(q)."""
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


def max_partial_ovoid(pts, lines):
    """Exact maximum set of pairwise non-collinear points, by branch and bound.

    Collinear = lying on a common totally isotropic line.  This is a maximum
    independent set in the collinearity graph; at 40 vertices of degree 12 the
    exact answer is cheap, so no heuristic is used and no bound is assumed.
    """
    n = len(pts)
    adj = [0] * n
    for L in lines:
        for a in L:
            for b in L:
                if a != b:
                    adj[a] |= 1 << b

    best = [0, ()]

    def rec(cand: int, chosen: tuple):
        if len(chosen) + bin(cand).count("1") <= best[0]:
            return
        if cand == 0:
            if len(chosen) > best[0]:
                best[0], best[1] = len(chosen), chosen
            return
        # branch on the lowest remaining candidate
        v = (cand & -cand).bit_length() - 1
        # take v
        rec(cand & ~(1 << v) & ~adj[v], chosen + (v,))
        # skip v
        rec(cand & ~(1 << v), chosen)

    rec((1 << n) - 1, ())
    return best[0], best[1]


def analyse(q: int) -> dict:
    pts, lines = build(q)
    m, witness = max_partial_ovoid(pts, lines)
    per_point = q + 1                      # lines through each point
    satisfied = per_point * m              # distinct, since no two are collinear
    total = len(lines)
    unsat = Fraction(total - satisfied, total)
    full_ovoid = q * q + 1                 # st + 1
    return {
        "q": q,
        "points": len(pts),
        "lines_contexts": total,
        "lines_per_point": per_point,
        "max_partial_ovoid": m,
        "full_ovoid_size_st_plus_1": full_ovoid,
        "is_a_full_ovoid": m == full_ovoid,
        "contexts_satisfied": satisfied,
        "contexts_unsatisfiable": total - satisfied,
        "unsatisfiable_fraction": str(unsat),
        "unsatisfiable_fraction_float": float(unsat),
        "witness_partial_ovoid": sorted(witness),
    }


def main() -> int:
    w33 = analyse(3)
    doily = analyse(2)

    # what the preregistration needed
    needed_m = Fraction(36, 4)             # 4m = 36
    checks = {}
    checks["w33_has_40_points_and_40_contexts"] = (
        w33["points"] == 40 and w33["lines_contexts"] == 40)
    checks["doily_has_15_points_and_15_contexts"] = (
        doily["points"] == 15 and doily["lines_contexts"] == 15)

    # CONTROL: q even, so a full ovoid exists and nothing is unsatisfiable
    checks["doily_reaches_a_full_ovoid"] = doily["is_a_full_ovoid"]
    checks["doily_unsatisfiable_fraction_is_zero"] = (
        doily["unsatisfiable_fraction"] == "0")

    # THE TEST
    checks["w33_has_no_full_ovoid"] = not w33["is_a_full_ovoid"]
    checks["one_tenth_would_require_max_partial_ovoid_9"] = (needed_m == 9)
    checks["max_partial_ovoid_is_NOT_9"] = w33["max_partial_ovoid"] != 9
    checks["unsatisfiable_fraction_is_NOT_one_tenth"] = (
        w33["unsatisfiable_fraction"] != "1/10")

    m = w33["max_partial_ovoid"]
    frac = w33["unsatisfiable_fraction"]
    out = {
        "schema": "w33.pass1098.what_one_tenth_measures.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            f"In the one reading that gives 1/10 geometric content -- the fraction "
            f"of measurement contexts that no classical assignment can satisfy -- "
            f"the answer is {frac}, not 1/10. A partial ovoid of size m satisfies "
            f"exactly 4m of the 40 contexts, so 1/10 would require a maximum "
            f"partial ovoid of 9. The exact maximum is {m}, giving "
            f"{w33['contexts_satisfied']} contexts satisfied and "
            f"{w33['contexts_unsatisfiable']} unsatisfiable. The preregistration's "
            f"'36 satisfiable contexts' is (q!)^2, which counts nothing in this "
            f"geometry. The doily control reaches a full ovoid and returns 0, "
            f"as it must for even q."),
        "W33": w33,
        "doily_control": doily,
        "the_arithmetic": {
            "contexts_satisfied_by_partial_ovoid_of_size_m": "4 * m",
            "one_tenth_requires": "4m = 36, i.e. m = 9",
            "actual_max_partial_ovoid": m,
            "actual_unsatisfiable_fraction": frac,
            "preregistered_value": "1/10",
        },
        "reading": (
            "This does not restore 1/10 and does not rescue the falsifier. It "
            "closes the question the firewall left open -- 'unidentified "
            "click-rate target' -- by showing that the most natural identification, "
            "the one the retracted derivation itself gestured at, yields a "
            "different number. Any surviving claim for 1/10 must now name a "
            "different observable entirely, because this one is computed and it "
            "is not 1/10."),
        "scope": (
            "Exact combinatorics on W(3,3) and W(2,2): a maximum independent set "
            "in the collinearity graph, computed by branch and bound with no "
            "heuristic and no assumed bound. It fixes the value of one specific "
            "observable. It is not a statement about what the demonstrator "
            "hardware measures, and it does not derive any replacement target."),
        "prior_art": [
            "analysis/w33_pass1080_contextual_fraction_audit.py -- CF = 1",
            "data/w33_pass1086_contextuality_claim_firewall.json -- label retired",
            "analysis/bt1901_cf_preregistration_audit.py -- source of 36/40",
            "analysis/w33_ovoid_construct.py -- owns the contextuality statement",
            "Thas (1981) -- W(q) has ovoids iff q is even",
        ],
        "checks": checks,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": out["status"],
        "max_partial_ovoid_W33": m,
        "contexts_satisfied": w33["contexts_satisfied"],
        "unsatisfiable_fraction": frac,
        "doily_control": doily["unsatisfiable_fraction"],
        "checks": checks}, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
