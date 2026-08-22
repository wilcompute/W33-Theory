"""Pass 7200 -- attacking the UPPER bound at q=9, which nobody has moved since Tallini.

THE GAP. 51 <= alpha(W(3,9)) <= 73. The lower end has four independent searches and a
certified basin behind it; the upper end is Tallini's q^2-q+1, a general bound for all odd q,
and Tallini is visibly loose as q grows: it is tight at q=3 (7 = 7), off by 3 at q=5 (18 vs
21) and off by 10 at q=7 (33 vs 43).

WHY THE SPECTRAL MACHINERY CANNOT HELP, computed here rather than assumed. The collinearity
graph is SRG(820,90,8,10) with eigenvalues 8 and -10, so the Hoffman ratio bound is
820*10/(90+10) = 82, and for a two-class association scheme with a_1 forced to 0 the Delsarte
LP gives the same 82. Both are WORSE than Tallini's 73. Anyone reaching for theta or Delsarte
here is wasting the run, and that is worth recording.

WHAT CAN ACTUALLY MOVE IT. A branch-and-bound DUAL bound is a rigorous upper bound whether or
not the solve closes. So: maximise honestly, with the LINE formulation -- a partial ovoid meets
each of the 820 lines in at most one point, giving 820 clique constraints of size q+1 = 10
instead of ~36,900 edge constraints, a far tighter relaxation -- and read off the dual bound.

If it drops below 73, that is a genuine improvement on Tallini AT q=9, rigorously certified by
the solver's own bound. If it does not, the run reports the number it reached and claims
nothing. The dual bound is only quoted when the solver reports one.

    py -3 analysis/w33_pass7200_q9_dual_bound.py [--q 9] [--timelimit 5400]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7187_q9_orbit_attack import Field, geometry  # noqa: E402
from w33_pass7196_optima_structure import lines_of  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=9)
    ap.add_argument("--timelimit", type=float, default=5400.0)
    args = ap.parse_args()
    q = args.q

    print("=" * 78)
    print(f"Pass 7200 -- rigorous upper bound on alpha(W(3,{q})) by ILP dual bound")
    print("=" * 78)

    F = Field(q)
    P, idx, adj, B = geometry(F)
    n = len(P)
    k = q * (q + 1)
    lam, mu = q - 1, q + 1
    D = (lam - mu) ** 2 + 4 * (k - mu)
    import math
    s = (lam - mu - math.isqrt(D)) // 2
    hoff = n * (-s) // (k - s)
    tall = q * q - q + 1
    print(f"\n  W(3,{q}): SRG({n},{k},{lam},{mu}), smallest eigenvalue {s}")
    print(f"    Hoffman / Delsarte LP bound : {hoff}")
    print(f"    Tallini q^2-q+1            : {tall}   <- the one to beat")
    print(f"    best known lower bound      : 51 (this repo)\n", flush=True)

    L = lines_of(P, idx, F, adj)
    print(f"  {len(L)} lines, each a clique of size {q + 1} "
          f"-- using the LINE formulation", flush=True)

    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    r, c, v = [], [], []
    for e, line in enumerate(L):
        for p in line:
            r.append(e)
            c.append(p)
            v.append(1.0)
    A = coo_matrix((v, (r, c)), shape=(len(L), n))
    print(f"  solving (time limit {args.timelimit:.0f}s) ...", flush=True)
    res = milp(c=-np.ones(n),
               constraints=LinearConstraint(A, -np.inf, 1),
               integrality=np.ones(n), bounds=Bounds(0, 1),
               options={"mip_rel_gap": 0.0, "time_limit": args.timelimit,
                        "presolve": True, "disp": True})

    print(f"\n  status {res.status}: {res.message}")
    incumbent = int(round(-res.fun)) if res.fun is not None else None
    dual = None
    mip = getattr(res, "mip_dual_bound", None)
    if mip is not None and np.isfinite(mip):
        dual = int(math.floor(-mip + 1e-9))
    print(f"  incumbent (lower bound) : {incumbent}")
    print(f"  DUAL BOUND (upper)      : {dual if dual is not None else 'not reported'}")
    verdict = "no improvement"
    if dual is not None:
        if dual < tall:
            verdict = f"IMPROVES Tallini at q={q}: {dual} < {tall}"
            print(f"\n  *** {verdict} ***")
            print(f"  alpha(W(3,{q})) <= {dual}, certified by the solver's dual bound.")
        else:
            verdict = f"dual {dual} does not beat Tallini {tall}"
            print(f"\n  {verdict} -- no claim made.")
    out = ROOT / "data" / f"PART_W33_PASS7200_Q{q}_DUAL_BOUND.json"
    out.write_text(json.dumps(
        {"boundary": (f"an ILP dual bound is a rigorous upper bound whether or not the solve "
                      f"closes. Reported here: {verdict}. No lower-bound claim is made"),
         "q": q, "srg": [n, k, lam, mu], "hoffman_delsarte": hoff, "tallini": tall,
         "incumbent": incumbent, "dual_bound": dual, "verdict": verdict,
         "note": ("Hoffman and the two-class Delsarte LP both give "
                  f"{hoff}, WORSE than Tallini's {tall} -- spectral methods cannot help here")},
        indent=2), encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
