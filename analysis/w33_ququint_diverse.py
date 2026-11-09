"""Item 1: diverse uniform-cover maximal partial spreads in d = 25 (random objectives + no-good cuts), certified by delta*; report
(size, #sentinels, multiplicity, lambda_max(R) from delta* via the sentinel formula, delta*).  Looking for any certified small set.
usage: py -3 analysis/w33_ququint_diverse.py"""
import json, os, random
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
qs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_ququint_sentinel_search.py")}
_src = open(os.path.join(HERE, "w33_ququint_sentinel_search.py"), encoding="utf-8").read()
exec(_src[: _src.index("res = {}")], qs)
geometry, splits_of, delta_from_cover = qs["geometry"], qs["splits_of"], qs["delta_from_cover"]
p = 5
pts, lag, w = geometry(p, 2); sp_ = splits_of(p, pts, w)
nS, nL, nP = len(sp_), len(lag), len(pts)
N = nS + nL + nP
def base_rows(m):
    A, lo, hi = [], [], []
    for pt in range(nP):
        r = np.zeros(N)
        for L in range(nL):
            if pt in lag[L]: r[nS + L] = 1
        r[nS + nL + pt] = -1; A.append(r); lo.append(0); hi.append(0)
        r = np.zeros(N)
        for s, (b, bp) in enumerate(sp_):
            if pt in b or pt in bp: r[s] = 1
        r[nS + nL + pt] = m; A.append(r); lo.append(m); hi.append(m)
    for L in range(nL):
        r = np.zeros(N)
        for pt in lag[L]: r[nS + nL + pt] = 1
        A.append(r); lo.append(1); hi.append(np.inf)
    return A, lo, hi
rng = random.Random(11)
rows = []
for m in (2, 1):
    A, lo, hi = base_rows(m)
    found = []
    for trial in range(6):
        Ac, loc, hic = list(A), list(lo), list(hi)
        for ex in found:
            r = np.zeros(N)
            for L in ex: r[nS + L] = 1
            Ac.append(r); loc.append(-np.inf); hic.append(len(ex) - 1)
        c = np.zeros(N); c[nS:nS + nL] = [rng.uniform(0.5, 1.5) for _ in range(nL)]
        res = milp(c, constraints=LinearConstraint(np.array(Ac), loc, hic), integrality=np.ones(N), bounds=Bounds(0, 1), options=dict(time_limit=120))
        if res.x is None: break
        x = np.round(res.x).astype(int)
        lines = [L for L in range(nL) if x[nS + L]]; sents = [s for s in range(nS) if x[s]]
        found.append(lines)
        cov = frozenset().union(*[lag[L] for L in lines])
        dl = delta_from_cover(p, 2, pts, cov)
        d = 25
        lam = (d - 1 + 2 * len(sents) / m - d * dl) * m / (2 * p)
        rows.append(dict(m=m, size=len(lines), sentinels=len(sents), delta=dl, lambda_max_R=lam, threshold=m * (d - 1) / (2 * p) + len(sents) / p))
        print("m=%d size %2d sentinels %2d  delta* %+.4f  lambda_max(R) %.3f  threshold %.3f" % (m, len(lines), len(sents), dl, lam, rows[-1]["threshold"]), flush=True)
json.dump(dict(rows=rows, certified=[r for r in rows if r["delta"] > 1e-6]), open(os.path.join(ROOT, "data", "w33_ququint_diverse.json"), "w"), indent=1)
