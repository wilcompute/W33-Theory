#!/usr/bin/env python3
"""Pass 1080: the preregistered "contextual fraction = 1/10" is not the contextual
fraction.

WHY THIS PASS EXISTS.  `analysis/bt1901_cf_preregistration_audit.py` preregisters

    CF(W(3,3)) = 1/10

with the falsification criterion "any measured CF != 1/10 refutes the W(3,3)
substrate", justified by "three independent routes from {q, v, mu, Phi_4}, zero
free parameters".  A preregistered falsifier is the most expensive kind of claim
to get wrong: it is designed to be acted on, and if the predicted quantity is
misnamed the experiment refutes the wrong thing.  So it is audited before it is
measured, not after.

Two separate findings, kept separate because they have different consequences.

FINDING 1 -- the three routes are not three.  Routes 2 and 3 are the SAME
identity for every q, not merely at q=3:

    mu/v = (q+1) / ((q^4-1)/(q-1)) = (q+1)(q-1)/(q^4-1) = (q^2-1)/(q^4-1)
         = 1/(q^2+1) = 1/Phi_4(q).

That is an algebraic identity, so their agreement is not corroboration.  Route 1,
`1 - (q!)^2/v`, is a different function which agrees with them at q=3 and nowhere
else -- and for q >= 4 it returns a NEGATIVE "fraction", so it is not a fraction.
"Three independent routes agree" is therefore one identity plus one coincidence.

FINDING 2 -- and this is the one that matters -- 1/10 is not the contextual
fraction of this model.  For the Abramsky-Barbosa contextual fraction (the
standard operational definition, and the one the cited Budroni et al. review
uses), the following is a theorem:

    a model is STRONGLY CONTEXTUAL  <=>  CF = 1,

and a model is strongly contextual exactly when its support admits no global
section.  For the KS ray model on W(3,3) -- points = the 40 Witting rays,
contexts = the 40 orthonormal tetrads, one ray per context assigned 1 -- a global
section IS an ovoid.  W(3,3) has ZERO ovoids.  Therefore

    CF(W(3,3)) = 1,  not 1/10,

and this holds for EVERY quantum state, because a state can only shrink the
support, which can only remove global sections, never create one.

The physics the preregistration is reaching for survives intact: W(3,3) is
contextual and W(2,2) is not, which is what the magic-distillation argument needs
(HWVE requires CF > 0, and 1 > 0).  What fails is the LABEL and the falsifier.
1/10 is some other observable -- note that
`analysis/bt1901_contextual_fraction_estimator.py` actually estimates a CLICK
RATE, `signal_clicks / signal_rows`, which is not an Abramsky-Barbosa contextual
fraction at all.  Until that observable is derived, "measured CF != 1/10 refutes
the substrate" would misfire.

POSITIVE CONTROL.  The same machinery is run on the doily, where global sections
DO exist (6 ovoids), and returns CF = 0 -- reproducing the preregistration's own
null.  A method that returns 1 on the case of interest and 0 on the control is
being tested, not just asserted.

PRIOR ART -- cited, not reclaimed:
  * analysis/w33_ovoid_construct.py (in CI) -- ovoid = KS colouring, exists iff q
    even.  OWNS the contextuality statement.
  * analysis/w33_pass1021_corollary_ovoid_orientation.py -- OWNS the recount
    W(3,3) = (36 spreads, 0 ovoids), Q(4,3) = (0 spreads, 36 ovoids), and the
    point-vs-line orientation that makes the KS reading the physical one.
  * analysis/bt1901_cf_preregistration_audit.py -- the claim under audit.
  * analysis/bt1901_contextual_fraction_estimator.py -- the estimator whose
    observable is a click rate.
  * Abramsky & Brandenburger (2011); Abramsky & Barbosa, "The logic of
    contextuality" / contextual fraction; Thas (1981); Budroni et al., Rev. Mod.
    Phys. 94 (2022).
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1080_contextual_fraction_audit.json"


def build(q: int):
    """Points and totally isotropic lines of W(q) for q in {2,3}."""
    def canon(v):
        for a in v:
            if a % q:
                inv = pow(a % q, -1, q)
                return tuple((inv * x) % q for x in v)
        return None

    pts, seen = [], []
    seenset = set()
    for v in itertools.product(range(q), repeat=4):
        if any(v):
            c = canon(v)
            if c not in seenset:
                seenset.add(c)
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
                        w = tuple((a * pts[i][k] + b * pts[j][k]) % q for k in range(4))
                        if any(w):
                            span.add(idx[canon(w)])
                if len(span) == q + 1:
                    lines.add(frozenset(span))
    return pts, sorted((sorted(L) for L in lines))


def ovoids(pts, lines):
    """Global sections of the KS model: hit every line exactly once."""
    n = len(pts)
    onpt = [[li for li, L in enumerate(lines) if p in L] for p in range(n)]
    sols = []

    def rec(chosen, covered):
        if len(covered) == len(lines):
            sols.append(tuple(sorted(chosen)))
            return
        li = min(l for l in range(len(lines)) if l not in covered)
        for p in lines[li]:
            if any(p in lines[c] for c in covered):
                continue
            new = covered | set(onpt[p])
            if len(new) != len(covered) + len(onpt[p]):
                continue
            rec(chosen + [p], new)

    rec([], set())
    return sols


def contextual_fraction(pts, lines, sections):
    """Abramsky-Barbosa CF for the uniform empirical model, by linear programming.

    Maximise the total weight lambda of a noncontextual subdistribution supported
    on the global sections, subject to not exceeding the empirical probability of
    any outcome.  CF = 1 - lambda.  With no global sections the LP is empty and
    lambda = 0, i.e. CF = 1 -- which is the strong-contextuality theorem, obtained
    here as the LP's answer rather than assumed.
    """
    if not sections:
        return Fraction(1), 0.0, "no global sections: strongly contextual"

    import numpy as np
    from scipy.optimize import linprog

    # one variable per global section; one constraint per (context, outcome)
    rows, rhs = [], []
    for L in lines:
        for p in L:
            rows.append([1.0 if p in s else 0.0 for s in sections])
            rhs.append(1.0 / len(L))       # uniform empirical model
    res = linprog(
        c=[-1.0] * len(sections),
        A_ub=np.array(rows), b_ub=np.array(rhs),
        bounds=[(0, None)] * len(sections),
        method="highs",
    )
    lam = float(-res.fun) if res.success else 0.0
    return None, lam, "LP over global sections"


def main() -> int:
    checks = {}

    # ---- FINDING 1: the three routes ------------------------------------
    def routes(q: int):
        v = (q ** 4 - 1) // (q - 1)
        import math
        r1 = Fraction(v - math.factorial(q) ** 2, v)   # 1 - (q!)^2/v
        r2 = Fraction(q + 1, v)                        # mu/v
        r3 = Fraction(1, q * q + 1)                    # 1/Phi_4(q)
        return v, r1, r2, r3

    table = {}
    for q in (2, 3, 4, 5):
        v, r1, r2, r3 = routes(q)
        table[q] = {"v": v, "route1_1_minus_KSbudget": str(r1),
                    "route2_mu_over_v": str(r2), "route3_inv_Phi4": str(r3),
                    "route2_equals_route3": r2 == r3,
                    "all_three_agree": r1 == r2 == r3,
                    "route1_is_a_fraction": 0 <= r1 <= 1}

    checks["routes_2_and_3_are_identical_for_every_q"] = all(
        table[q]["route2_equals_route3"] for q in table)
    checks["all_three_agree_ONLY_at_q3"] = (
        table[3]["all_three_agree"] and not any(
            table[q]["all_three_agree"] for q in (2, 4, 5)))
    checks["route1_is_not_even_a_fraction_for_q_ge_4"] = not any(
        table[q]["route1_is_a_fraction"] for q in (4, 5))

    # ---- FINDING 2: the actual contextual fraction ------------------------
    p3, l3 = build(3)
    p2, l2 = build(2)
    checks["w33_is_40_points_40_lines"] = len(p3) == 40 and len(l3) == 40
    checks["doily_is_15_points_15_lines"] = len(p2) == 15 and len(l2) == 15

    ov3, ov2 = ovoids(p3, l3), ovoids(p2, l2)
    checks["w33_has_zero_ovoids"] = len(ov3) == 0
    checks["doily_has_six_ovoids"] = len(ov2) == 6

    cf3_exact, lam3, why3 = contextual_fraction(p3, l3, ov3)
    _, lam2, why2 = contextual_fraction(p2, l2, ov2)
    cf3 = 1.0 - lam3
    cf2 = 1.0 - lam2

    checks["w33_contextual_fraction_is_ONE"] = abs(cf3 - 1.0) < 1e-9
    checks["w33_contextual_fraction_is_NOT_one_tenth"] = abs(cf3 - 0.1) > 0.5
    # positive control: the method must return 0 where sections exist
    checks["doily_contextual_fraction_is_ZERO"] = abs(cf2) < 1e-9
    checks["method_separates_the_two_cases"] = cf3 > cf2
    # the physics the preregistration needs still holds
    checks["HWVE_condition_CF_gt_0_still_satisfied_at_q3"] = cf3 > 0

    out = {
        "schema": "w33.pass1080.contextual_fraction_audit.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The preregistered CF = 1/10 is not the contextual fraction. For the "
            "Abramsky-Barbosa contextual fraction, strong contextuality is "
            "equivalent to CF = 1, and the W(3,3) KS ray model is strongly "
            "contextual because a global section is an ovoid and W(3,3) has none. "
            "So CF(W(3,3)) = 1 for every state, computed here as the answer of the "
            "LP rather than assumed. The doily positive control returns CF = 0, "
            "reproducing the preregistration's own null. Separately, the claimed "
            "'three independent routes' to 1/10 are one algebraic identity "
            "(mu/v = 1/Phi_4(q) for all q) plus one coincidence that holds only at "
            "q=3 and returns negative values for q >= 4."),
        "route_table": {str(k): v for k, v in table.items()},
        "contextual_fraction": {
            "W33": {"value": cf3, "method": why3, "ovoids": len(ov3)},
            "doily": {"value": cf2, "method": why2, "ovoids": len(ov2)},
        },
        "what_survives": (
            "The substrate claim the preregistration actually needs is unaffected: "
            "W(3,3) is contextual and W(2,2) is not, so the HWVE magic-distillation "
            "condition CF > 0 holds at q=3 and fails at q=2. Only the numerical "
            "value, its name, and the corroboration argument are withdrawn."),
        "what_must_change": (
            "The falsification criterion 'any measured CF != 1/10 refutes the W(3,3) "
            "substrate' cannot stand as written: the Abramsky-Barbosa CF of this "
            "model is 1, so a faithful measurement of the contextual fraction would "
            "'refute' the substrate on a labelling error. Note also that "
            "bt1901_contextual_fraction_estimator.py estimates signal_clicks / "
            "signal_rows -- a click rate, not a contextual fraction. Either derive "
            "which observable 1/10 predicts and rename it, or drop the falsifier."),
        "scope": (
            "An audit of a preregistered number, not an experiment and not a claim "
            "about hardware. The contextual fraction is computed for the uniform "
            "empirical model; the CF = 1 conclusion is state-independent because it "
            "follows from the emptiness of the set of global sections, which no "
            "state can enlarge. No claim is made about what observable 1/10 is."),
        "prior_art": [
            "analysis/w33_ovoid_construct.py -- ovoid = KS colouring, exists iff q even",
            "analysis/w33_pass1021_corollary_ovoid_orientation.py -- 0 ovoids, orientation",
            "analysis/bt1901_cf_preregistration_audit.py -- the claim audited here",
            "analysis/bt1901_contextual_fraction_estimator.py -- estimates a click rate",
            "Abramsky-Barbosa: strong contextuality <=> CF = 1",
            "Thas (1981): W(q) has ovoids iff q is even",
        ],
        "checks": checks,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": out["status"], "CF_W33": cf3, "CF_doily": cf2,
                      "checks": checks}, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
