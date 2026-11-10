"""Pass 12645 item 2: structure of the unique optimiser of the d = 25 single cover (min F = 13/75).  Polish the optimum, then report the
full Weyl profile |<W_u>| over ALL 624 nonzero u (covered / uncovered split), values identified as rationals or square roots, the set of
u with |<W_u>| = 1 (the state's stabiliser subgroup), and the same for the pentad optimiser.  If the optimiser is an eigenstate of a
nontrivial Weyl subgroup, its exact form can be derived inside that eigenspace.
usage: py -3 analysis/w33_d25_optimiser_structure.py"""
import json, os, contextlib, io, itertools
from collections import Counter
import numpy as np, mpmath as mp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
mf = {"__name__": "x", "__file__": os.path.join(HERE, "w33_minF_covered_points.py")}
_src = open(os.path.join(HERE, "w33_minF_covered_points.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index(chr(10) + "res = {}")], mf)
weyl, ops_for = mf["weyl"], mf["ops_for"]
def polish(p, n, pts, cov, starts, seed):
    d = p ** n; Ws = ops_for(p, n, pts, cov); rng = np.random.default_rng(seed)
    def fg(z):
        v = z[:d] + 1j * z[d:]; nv = np.vdot(v, v).real
        Wv = Ws @ v; f = np.einsum("i,ki->k", v.conj(), Wv); WHv = np.einsum("kji,j->ki", Ws.conj(), v)
        g = float(np.sum(abs(f) ** 2)) / d
        dg = (np.einsum("ki,k->i", Wv, f.conj()) + np.einsum("ki,k->i", WHv, f)) / d
        gr = 2 * dg / nv ** 2 - 4 * g * v / nv ** 3
        return g / nv ** 2, np.concatenate([gr.real, gr.imag])
    best = min((minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(maxiter=50000, gtol=1e-15, ftol=1e-18)) for _ in range(starts)), key=lambda r: r.fun)
    v = best.x[:d] + 1j * best.x[d:]; return best.fun, v / np.linalg.norm(v)
def profile(p, n, v, cov_pts, pts):
    d = p ** n; rows = []
    covset = set()
    for i in cov_pts:
        for k in range(1, p): covset.add(tuple((k * x) % p for x in pts[i]))
    allu = [u for u in itertools.product(range(p), repeat=2 * n) if any(u)]
    vals = {u: abs(np.vdot(v, weyl(p, n, u) @ v)) for u in allu}
    cov = Counter(round(vals[u], 6) for u in allu if u in covset); unc = Counter(round(vals[u], 6) for u in allu if u not in covset)
    stab = [u for u in allu if vals[u] > 1 - 1e-8]
    mp.mp.dps = 15
    ids = {str(k): str(mp.identify(k ** 2, tol=1e-6)) for k in set(cov) | set(unc)}
    return dict(covered_profile={str(k): c for k, c in sorted(cov.items())}, uncovered_profile={str(k): c for k, c in sorted(unc.items())},
                stabiliser_size=len(stab), squared_value_ids=ids)
res = {}
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index(chr(10) + "res = {}")], cs)
pts, lag, w = cs["geometry"](3, 2); mps, _ = cs["maximal_partial_spreads"](lag)
S = next(sorted(S) for S in mps if len(S) == 5); cov = sorted(frozenset().union(*[lag[L] for L in S]))
f, v = polish(3, 2, pts, cov, 40, 1)
res["pentad"] = dict(min_F=f, **profile(3, 2, v, cov, pts)); print("pentad", res["pentad"], flush=True)
qs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_ququint_sentinel_search.py")}
_src = open(os.path.join(HERE, "w33_ququint_sentinel_search.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("res = {}")], qs)
pts, lag, w = qs["geometry"](5, 2)
with contextlib.redirect_stdout(io.StringIO()):
    r = qs["search"](5, 1)
cov = sorted(frozenset().union(*[lag[L] for L in r["lines"]]))
f, v = polish(5, 2, pts, cov, 30, 2)
res["d25_single_cover"] = dict(min_F=f, **profile(5, 2, v, cov, pts)); print("d25", res["d25_single_cover"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_d25_optimiser_structure.json"), "w"), indent=1)
