"""Item 2: small, structured strongly unextendible sets in d = 25.  Integer program over W(3,q):
binary x_s (split s = {b, b-perp} used as a sentinel), y_L (line in the partial spread), c_p (point covered by the spread):
   sum_{L ni p} y_L = c_p                      (spread lines disjoint, cover exactly the covered points)
   sum_{s ni p} x_s = m (1 - c_p)              (uncovered points covered exactly m times by sentinels)
   sum_{p in L} c_p >= 1 for every line L      (maximality: every line meets the spread)
minimise sum y (smallest such sets).  Control: q = 3, m = 2 must find a pentad (5 lines, 5 splits).  Then certify each solution with
delta* = lambda_min(Pi M Pi | Sym^2) (twirl formula) and report the sentinel group structure (pairwise orders of S_k S_l).
usage: py -3 analysis/w33_ququint_sentinel_search.py"""
import itertools, json, os
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
qq = {"__name__": "x", "__file__": os.path.join(HERE, "w33_ququint_umub.py")}
_src = open(os.path.join(HERE, "w33_ququint_umub.py"), encoding="utf-8").read()
exec(_src[: _src.index("out = {}")], qq)
geometry, delta_from_cover = qq["geometry"], qq["delta_from_cover"]
def splits_of(p, pts, w):
    idx = {q: i for i, q in enumerate(pts)}
    def norm(v):
        c = next(x for x in v if x); inv = pow(c, -1, p); return tuple((x * inv) % p for x in v)
    planes = set()
    for a, b in itertools.combinations(range(len(pts)), 2):
        if w(pts[a], pts[b]) != 0:
            planes.add(frozenset(idx[norm(tuple((x * pts[a][k] + y * pts[b][k]) % p for k in range(4)))] for x in range(p) for y in range(p) if (x, y) != (0, 0)))
    perp = lambda S2: frozenset(i for i in range(len(pts)) if all(w(pts[i], pts[j]) == 0 for j in S2))
    return [tuple(s) for s in {frozenset((S2, perp(S2))) for S2 in planes}]
def search(p, m, exclude=()):
    pts, lag, w = geometry(p, 2)
    sp_ = splits_of(p, pts, w)
    nS, nL, nP = len(sp_), len(lag), len(pts)
    N = nS + nL + nP
    A, lo, hi = [], [], []
    for pt in range(nP):
        row = np.zeros(N)
        for L in range(nL):
            if pt in lag[L]: row[nS + L] = 1
        row[nS + nL + pt] = -1
        A.append(row); lo.append(0); hi.append(0)
        row = np.zeros(N)
        for s, (b, bp) in enumerate(sp_):
            if pt in b or pt in bp: row[s] = 1
        row[nS + nL + pt] = m
        A.append(row); lo.append(m); hi.append(m)
    for L in range(nL):
        row = np.zeros(N)
        for pt in lag[L]: row[nS + nL + pt] = 1
        A.append(row); lo.append(1); hi.append(np.inf)
    for ex in exclude:  # no-good cuts on line sets
        row = np.zeros(N)
        for L in ex: row[nS + L] = 1
        A.append(row); lo.append(-np.inf); hi.append(len(ex) - 1)
    cobj = np.zeros(N); cobj[nS:nS + nL] = 1
    r = milp(cobj, constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.ones(N), bounds=Bounds(0, 1), options=dict(time_limit=600))
    if r.x is None:
        return None
    x = np.round(r.x).astype(int)
    lines = [L for L in range(nL) if x[nS + L]]
    sents = [s for s in range(nS) if x[s]]
    cov = frozenset().union(*[lag[L] for L in lines]) if lines else frozenset()
    return dict(p=p, m=m, n_lines=len(lines), n_sentinels=len(sents), delta=delta_from_cover(p, 2, pts, cov), status=r.status, lines=lines)
res = {}
ctrl = search(3, 2)
res["control_q3_m2"] = ctrl
print("control q=3 m=2:", {k: v for k, v in ctrl.items() if k != "lines"} if ctrl else None, flush=True)
for m in (2, 1):
    r = search(5, m)
    res[f"q5_m{m}"] = r
    print("q=5 m=%d:" % m, {k: v for k, v in r.items() if k != "lines"} if r else "infeasible", flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_ququint_sentinel_search.json"), "w"), indent=1, default=str)
