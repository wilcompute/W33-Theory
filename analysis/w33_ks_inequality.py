#!/usr/bin/env python3
"""
The bench gets a test statistic: a noncontextual inequality the substrate violates, classical <= 36 vs
quantum 40. Pass 42 derived the contextual fraction 1/10 from the no-ovoid geometry; this pass turns
that into an explicit, falsifiable INEQUALITY with a number an experiment can read off. Define, over the
40 measurement contexts (the totally-isotropic lines of W(3,3), each an orthonormal tetrad of Witting
rays), the score S = the number of contexts that return exactly one outcome. Quantum mechanically every
context is an orthonormal basis, so a measurement always yields exactly one outcome: S = 40 with
certainty. A NONCONTEXTUAL hidden-variable model must instead pre-assign each of the 40 rays a fixed
0/1 value independent of which context it is measured in, and then S counts the contexts whose four
pre-assigned values sum to exactly one. By exact integer programming over all such assignments the
maximum is exactly 36 -- the best classical strategy (computed here: it lights up 11 of the 40 rays)
satisfies 36 contexts and FAILS exactly 4. So the noncontextual inequality is S <= 36, and the
substrate achieves S = 40: a violation of 4, with the normalized violation (40 - 36)/40 = 1/10 = 1/Phi_4
being precisely the contextual fraction. This is a STATE-INDEPENDENT inequality (it holds for any input
state, because orthonormal-basis exclusivity is state-independent), so the benchtop test needs no
special preparation: measure all 40 contexts, count how many show exact single-outcome exclusivity, and
any value above 36 refutes noncontextual realism. With finite samples the estimator S-hat rejects
noncontextuality once it clears 36 with confidence -- and the 1/10 contextual fraction is the signal
size the earlier shot-count budget (~225 valid coincidences for 5 sigma) was sized against. So the
substrate's nonclassicality is now a concrete number on a meter: 40 versus a classical ceiling of 36.

This turns the contextual fraction into an explicit noncontextual inequality: it computes the classical
bound (36) by exact integer programming, exhibits the optimal classical assignment and its 4 failed
contexts, states the quantum value (40), and reports the violation and the test statistic.

THE INEQUALITY.
    score S        S = number of the 40 contexts returning exactly one outcome.
    noncontextual  S <= 36 (exact ILP over 0/1 ray-assignments; best strategy lights 11 rays, fails 4).
    quantum        S = 40 (every context is an orthonormal basis -> exactly one outcome, state-independent).
    violation      40 - 36 = 4; normalized (40-36)/40 = 1/10 = 1/Phi_4 = the contextual fraction.
    test statistic measure all 40 contexts, count exact-exclusivity; S-hat > 36 refutes noncontextuality.

Honest scope: the classical bound 36 and the optimal assignment (with its 4 failed contexts) are
computed exactly here from the W(3,3) line incidence; the quantum value 40 is the state-independent
exclusivity of orthonormal-basis measurement, guaranteed once the 40 contexts are realised as
orthonormal tetrads -- the Witting realisation in C^4 (corpus two-carrier result). So the inequality
S <= 36 (NCHV) vs 40 (QM) is a derived, state-independent KS inequality; the finite-sample test
statistic connects to the demonstrator shot budget. This is the logical/possibilistic form (counting
contexts with exact single-outcome exclusivity).

Verifies the noncontextual bound S <= 36 by exact ILP, the optimal classical assignment failing exactly
4 contexts, and the resulting violation (quantum 40) and contextual fraction 1/10.
"""
from __future__ import annotations

import itertools
import json

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def build_w33_lines():
    inv = {1: 1, 2: 2}

    def norm(v):
        for c in v:
            if c != 0:
                return tuple((x * inv[c]) % 3 for x in v)

    pts = sorted({norm(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    pidx = {p: i for i, p in enumerate(pts)}

    def B(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % 3

    n = len(pts)

    def span(p, q):
        S = set()
        for a in range(3):
            for b in range(3):
                v = tuple((a * p[t] + b * q[t]) % 3 for t in range(4))
                if any(v):
                    S.add(norm(v))
        return frozenset(pidx[x] for x in S)

    lines = sorted(
        {
            tuple(sorted(span(pts[i], pts[j])))
            for i in range(n)
            for j in range(i + 1, n)
            if B(pts[i], pts[j]) == 0
        }
    )
    return n, lines


def main():
    out = {}
    n, lines = build_w33_lines()
    m = len(lines)
    print(
        "== the bench gets a test statistic: a noncontextual inequality, classical <= 36 vs quantum 40 =="
    )
    print(
        f"\n[score]  S = number of the {m} contexts (orthonormal tetrads) returning exactly one outcome"
    )

    # noncontextual bound via exact ILP: maximize #contexts with exactly-one selected ray
    nv = n + m
    rows, lb, ub = [], [], []
    for li, L in enumerate(lines):
        r1 = np.zeros(nv)
        r1[n + li] = 1
        for p in L:
            r1[p] -= 1
        rows.append(r1)
        lb.append(-np.inf)
        ub.append(0)
        r2 = np.zeros(nv)
        r2[n + li] = 1
        for p in L:
            r2[p] += 1
        rows.append(r2)
        lb.append(-np.inf)
        ub.append(2)
    c = np.zeros(nv)
    c[n:] = -1
    res = milp(
        c=c,
        constraints=LinearConstraint(np.array(rows), np.array(lb), np.array(ub)),
        integrality=np.ones(nv),
        bounds=Bounds(0, 1),
    )
    x = np.round(res.x[:n]).astype(int)
    sat = [1 if sum(x[p] for p in L) == 1 else 0 for L in lines]
    classical = sum(sat)
    failed = [li for li, s in enumerate(sat) if s == 0]
    print(
        f"[noncontextual]  S <= {classical} (exact ILP; best 0/1 ray-assignment lights {int(x.sum())} rays, fails {len(failed)} contexts)"
    )
    assert classical == 36 and len(failed) == 4
    out["noncontextual_bound"] = {
        "S_max": classical,
        "rays_lit": int(x.sum()),
        "contexts_failed": len(failed),
    }

    quantum = m
    violation = quantum - classical
    cf = violation / m
    print(
        f"[quantum]        S = {quantum} (every context is an orthonormal basis -> exactly one outcome, state-independent)"
    )
    print(
        f"[violation]      {quantum} - {classical} = {violation}; normalized (40-36)/40 = {cf} = 1/10 = 1/Phi_4 = contextual fraction"
    )
    assert violation == 4 and abs(cf - 0.1) < 1e-12
    out["quantum_value"] = quantum
    out["violation"] = {
        "absolute": violation,
        "normalized": cf,
        "closed_form": "1/10 = 1/Phi_4",
    }
    out["inequality"] = (
        "S <= 36 (noncontextual)  vs  S = 40 (quantum); state-independent"
    )
    out["test_statistic"] = (
        "measure all 40 contexts; count exact single-outcome exclusivity; S-hat > 36 refutes noncontextuality"
    )

    print(
        "\nRESULT: the substrate's nonclassicality is now a number on a meter. Over the 40 measurement"
    )
    print(
        "  contexts -- the orthonormal tetrads of Witting rays that are the lines of W(3,3) -- let S"
    )
    print(
        "  count the contexts returning exactly one outcome. A noncontextual hidden-variable model"
    )
    print(
        "  pre-assigns each ray a fixed 0/1 value, and by exact integer programming the most contexts"
    )
    print(
        "  it can make exact is 36: the best classical strategy lights 11 of the 40 rays and still"
    )
    print(
        "  fails 4 contexts. So the noncontextual inequality is S <= 36. Quantum mechanically every"
    )
    print(
        "  context is an orthonormal basis, so a measurement always yields exactly one outcome and"
    )
    print(
        "  S = 40 with certainty -- a violation of 4, whose normalized size (40-36)/40 = 1/10 = 1/Phi_4"
    )
    print(
        "  is exactly the contextual fraction. The inequality is state-independent (it needs no special"
    )
    print(
        "  input state), so the bench test is: measure all 40 contexts, count exact single-outcome"
    )
    print(
        "  exclusivity, and any S above 36 refutes noncontextual realism -- with the 1/10 fraction the"
    )
    print(
        "  signal size the ~225-coincidence shot budget was sized against. Honest: the classical bound"
    )
    print(
        "  36 and the 4 failed contexts are computed exactly; the quantum value 40 is the"
    )
    print(
        "  state-independent exclusivity of orthonormal-basis measurement on the Witting realisation."
    )

    out["summary"] = (
        "the bench gets a test statistic: a noncontextual inequality the substrate violates, classical "
        "<= 36 vs quantum 40. Over the 40 measurement contexts (orthonormal tetrads of Witting rays = "
        "the lines of W(3,3)), let S = the number of contexts returning exactly one outcome. "
        "Noncontextual hidden-variable models pre-assign each ray a fixed 0/1 value; by exact ILP the "
        "maximum is S = 36 (the optimal assignment lights 11 rays and fails exactly 4 contexts), so the "
        "inequality is S <= 36. Quantum mechanically every context is an orthonormal basis -> exactly "
        "one outcome always, so S = 40 (state-independent). Violation = 40 - 36 = 4; normalized "
        "(40-36)/40 = 1/10 = 1/Phi_4 = the contextual fraction. State-independent test: measure all 40 "
        "contexts, count exact single-outcome exclusivity, S-hat > 36 refutes noncontextual realism; the "
        "1/10 fraction is the signal size the demonstrator shot budget (~225 valid coincidences for 5 "
        "sigma) was sized against. HONEST: the classical bound 36 and the 4 failed contexts are computed "
        "exactly from the W(3,3) line incidence; the quantum value 40 is the state-independent "
        "exclusivity of orthonormal-basis measurement, guaranteed once the 40 contexts are realised as "
        "orthonormal tetrads (the Witting realisation in C^4, corpus two-carrier); this is the logical/"
        "possibilistic form (counting contexts with exact single-outcome exclusivity)."
    )
    out["sources"] = [
        "W(3,3) line incidence (40 contexts; computed); noncontextual bound via exact ILP (scipy milp); "
        "Witting rays as orthonormal tetrads in C^4 (corpus two-carrier); state-independent contextuality "
        "/ KS noncontextual inequalities (Cabello, Yu-Oh style); contextual fraction 1/10 = 1/Phi_4 "
        "(Pass 42); shot budget (Pass 39)."
    ]
    with open("data/w33_ks_inequality.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_ks_inequality.json")


if __name__ == "__main__":
    main()
