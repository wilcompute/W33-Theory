"""Pass 12091: three families are the only anomaly-free chirality an order-3 shift gives a Standard-Model grading
(Claude track; 12087, 12090).

Setting. A flag-built Standard-Model grading V (12087) keeps su(3) + su(2) + u(1)^5 with exact SM hypercharges. Add an
order-3 torus element t (E8/3E8: 6561 classes, phase alpha -> 3 alpha.t mod 3) that keeps every SM gauge root
(phase 0) -- an order-3 orbifold shift compatible with the grading. Per complex plane, the net number of left-handed
copies of a field F is N(F) = (#weights of F with phase 1 - #weights of its conjugate with phase 1) / dim F, for the
generation Q(3,2)_{1/6}, u^c(3bar)_{-2/3}, d^c(3bar)_{1/3}, L(1,2)_{-1/2}, e^c(1)_{1}.
Exact results (three independent flag-built SM gradings, all 6561 classes):
  * 242 non-trivial gauge-compatible shifts; their (N(Q), N(u), N(d), N(L), N(e)) patterns are tabulated.
  * The ONLY non-zero anomaly-free patterns (N equal on all five fields) are (3,3,3,3,3) and (-3,-3,-3,-3,-3), each for
    exactly 10 shifts, and these are exactly the shifts with fixed algebra e6 + a2 (dimension 86).
  * Every other chiral shift is anomalous (unequal N), e.g. (2,1,5,-3,-3), (-2,2,1,0,0).
  * The family a2 is usually NOT a W(3,3) event fibre: 0, 0 and 2 of the 20 shifts in the three gradings tested.
Reading. Combined with the Standard-Model grading, an order-3 twist can produce a consistent chiral spectrum only with
exactly three families, through E8 > E6 x SU(3) with the families as the SU(3) triplet. The E6 x SU(3) three-family
mechanism is classical (Z3 orbifolds with standard-type embedding); new is the exclusivity statement inside the
W(3,3) clock/split grading: no other non-zero anomaly-free family number occurs. Scope: per-plane untwisted counting on
the E8 adjoint, Z2 projections of the grading and twisted sectors not included.
"""

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402
from w33_pass12087_standard_model_sectors import Gradings  # noqa: E402

OUT = ROOT / "data" / "w33_pass12091_three_families_are_the_only_anomaly_free_chirality.json"
SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
GEN = {"Q": (6, 1), "uc": (3, -4), "dc": (3, 2), "L": (2, -3), "ec": (1, 6)}


def main():
    checks, res = {}, {}
    g = Gradings()
    R, fib = g.R, g.fib
    Adj, invs, tick, _ = setup()
    ptof = {i: x for x in range(40) for i in fib[x]}
    coefs = np.array(list(itertools.product(range(3), repeat=8)))
    PH = np.round((coefs @ SIMPLE) @ R.T).astype(int) % 3
    per_seed, all_ok = {}, True
    for seed in (7, 8, 9):
        gens = g.sm_flag(seed)
        V = g.span_of(gens)
        sec, Y, xy = g.sectors(gens)
        gauge = [i for c in g.comps(g.fixedmask(V)) for i in c]
        Y6 = np.round(R @ Y * 6).astype(int)
        orbsize = np.zeros(240, int)
        for i in range(240):
            orb, st = {i}, [i]
            while st:
                a = st.pop()
                for b in gauge:
                    j = g.rkey[tuple(np.round((R[a] - (R[a] @ R[b]) * R[b]) * 2).astype(int))]
                    if j not in orb:
                        orb.add(j)
                        st.append(j)
            orbsize[i] = len(orb)
        out, fibres = Counter(), []
        for ph in PH:
            if np.any(ph[gauge] != 0) or not ph.any():
                continue
            N = []
            for o, y in GEN.values():
                a = int(np.sum((orbsize == o) & (Y6 == y) & (ph == 1)) - np.sum((orbsize == o) & (Y6 == -y) & (ph == 1)))
                N.append(a // o if a % o == 0 else None)
            key = (tuple(N), 8 + int(np.sum(ph == 0)))
            out[key] += 1
            if len(set(N)) == 1 and N[0] not in (0, None):
                comps = g.comps(ph == 0)
                a2 = next(c for c in comps if len(c) == 6)
                fibres.append(len({ptof[i] for i in a2}) == 1)
        uniform = {k: v for k, v in out.items() if None not in k[0] and len(set(k[0])) == 1 and k[0][0] != 0}
        per_seed[seed] = dict(n_shifts=sum(out.values()), patterns={str(k): v for k, v in out.items()}, uniform={str(k): v for k, v in uniform.items()},
                              family_a2_is_event_fibre=sum(fibres))
        all_ok &= sum(out.values()) == 242 and uniform == {((3,) * 5, 86): 10, ((-3,) * 5, 86): 10}
    res["per_grading"] = per_seed
    checks["three SM gradings: 242 gauge-compatible order-3 shifts each"] = all(v["n_shifts"] == 242 for v in per_seed.values())
    checks["only non-zero anomaly-free patterns: (3,3,3,3,3) and (-3,...,-3), 10 shifts each, fixed algebra e6 + a2 (dim 86)"] = bool(all_ok)
    checks["the family a2 is an event fibre for 0, 0, 2 of the 20 shifts (gradings 7, 8, 9): generally not"] = [per_seed[k]["family_a2_is_event_fibre"] for k in (7, 8, 9)] == [0, 0, 2]
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
