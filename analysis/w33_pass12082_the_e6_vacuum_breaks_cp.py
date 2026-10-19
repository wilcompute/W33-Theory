"""Pass 12082: the E6 clock vacuum breaks every flavour CP -- spontaneous CP violation by clock condensation
(Claude track; 12077-12080, the Nelson-Barr chain 12004-12044).

Using the 1080 bosonic CPs of 12080 (antilinear Weyl elements e with e^2 = +1 and 8 fixed events) and their action on
the 120 clocks (parity vectors), exact counts:
  * one clock (e7 + a1): preserved by exactly 72 CPs (every clock; 1080 x 8 / 120).
  * two clocks: a non-Klein pair (d6 + 2a1) is preserved by exactly 8 CPs; a Klein pair (product a clock) by NONE.
  * hence a Klein triple -- the e6 + u(1)^2 vacuum chosen by clock dynamics and bosonic loops (12077-12078) -- is
    preserved by no bosonic CP; Kramers reversals preserve no clock at all (12080).
Reading. The single-clock vacuum is CP-symmetric; the step to the grand-unified e6 + u(1)^2 Klein vacuum breaks every
flavour-type (bosonic) CP. CP violation then arises spontaneously at the scale where the second clock condenses --
the structure that Nelson-Barr models assume (CP exact in the fundamental theory, broken spontaneously), and which the
flavour chain needs (the Barr row, 12004-12005, 12044). Scope: W(E8)-level symmetry statements; no computation of
theta-bar or of the CP-violating phase magnitude.
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402
from w33_pass12053_gate_sets_and_real_forms import setup, sp43_from_ticks  # noqa: E402
from w33_pass12080_cp_compatible_clocks import inverting_involution  # noqa: E402

OUT = ROOT / "data" / "w33_pass12082_the_e6_vacuum_breaks_cp.json"


def main():
    checks, res = {}, {}
    R, C, fib, refl, perm = build()
    Adj, invs, tick, _ = setup()
    G = sp43_from_ticks(tick)
    w = perm(inverting_involution(C, refl))
    ptof = np.empty(240, int)
    for x in range(40):
        for i in fib[x]:
            ptof[i] = x
    Pc = np.array([s for k, s in invs if k == "clock"])
    cps = []
    for g in G:
        e = w[g]
        pp = np.array([ptof[e[fib[x][0]]] for x in range(40)])
        if np.array_equal(pp[pp], np.arange(40)) and int(np.sum(pp == np.arange(40))) == 8:
            cps.append(e)
    keep = np.array([[np.array_equal(Pc[i][e], Pc[i]) for i in range(120)] for e in cps])
    checks["1080 bosonic CPs; each clock preserved by exactly 72"] = len(cps) == 1080 and set(keep.sum(0)) == {72}
    pc = Counter()
    for a in range(120):
        for b in range(a + 1, 120):
            kl = bool((Pc == (Pc[a] ^ Pc[b])).all(1).any())
            pc[(kl, int(np.sum(keep[:, a] & keep[:, b])))] += 1
    res["pairs"] = {str(k): v for k, v in pc.items()}
    checks["clock pairs: 3780 non-Klein preserved by exactly 8 CPs; 3360 Klein pairs by none"] = pc == Counter({(False, 8): 3780, (True, 0): 3360})
    trip = set()
    for a in range(120):
        for b in range(a + 1, 120):
            m = np.where((Pc == (Pc[a] ^ Pc[b])).all(1))[0]
            if len(m):
                trip.add(tuple(sorted((a, b, int(m[0])))))
    checks["no CP preserves any of the 1120 Klein triples (the e6 + u(1)^2 vacua)"] = len(trip) == 1120 and all(
        not keep[:, list(t)].all(1).any() for t in trip)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
