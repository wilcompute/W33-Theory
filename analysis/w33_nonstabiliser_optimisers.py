"""Pass 12644 item 2: the optimal states where min F lies below the stabiliser value: two-qutrit pentads (0.14711) and d = 25 single covers
(0.17333).  F(v) = (1/d) sum_{covered nonzero u} |<v|W_u|v>|^2 (Pass 12643).  For each: polish the minimum (many starts, tight tolerance),
report the value to ~1e-13 and candidate identifications (mpmath.identify / findpoly), the multiset of |<W_u>| over covered u, the
Schmidt coefficients (2-party split of the two qudits), the probability pattern over the set's basis states, and how many optimal states
are found up to phase (distinct |<W_u>| profiles).
usage: py -3 analysis/w33_nonstabiliser_optimisers.py"""
import json, os, contextlib, io, itertools
from collections import Counter
import numpy as np, mpmath as mp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
mf = {"__name__": "x", "__file__": os.path.join(HERE, "w33_minF_covered_points.py")}
_src = open(os.path.join(HERE, "w33_minF_covered_points.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("res = {}")], mf)
weyl, ops_for = mf["weyl"], mf["ops_for"]
def optimise(p, n, pts, cov, starts, seed):
    d = p ** n; Ws = ops_for(p, n, pts, cov); rng = np.random.default_rng(seed)
    def fg(z):
        v = z[:d] + 1j * z[d:]; nv = np.vdot(v, v).real
        Wv = Ws @ v; f = np.einsum("i,ki->k", v.conj(), Wv); WHv = np.einsum("kji,j->ki", Ws.conj(), v)
        g = float(np.sum(abs(f) ** 2)) / d
        dg = (np.einsum("ki,k->i", Wv, f.conj()) + np.einsum("ki,k->i", WHv, f)) / d
        gr = 2 * dg / nv ** 2 - 4 * g * v / nv ** 3
        return g / nv ** 2, np.concatenate([gr.real, gr.imag])
    sols = []
    for _ in range(starts):
        r = minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-14, ftol=1e-16))
        v = r.x[:d] + 1j * r.x[d:]; v /= np.linalg.norm(v); sols.append((r.fun, v))
    sols.sort(key=lambda t: t[0]); best = sols[0][0]
    opt = [v for f, v in sols if f < best + 1e-9]
    prof = lambda v: tuple(sorted(np.round(np.abs([np.vdot(v, W @ v) for W in Ws]), 6)))
    profiles = Counter(prof(v) for v in opt)
    v = opt[0]
    schmidt = np.linalg.svd(v.reshape(p ** (n // 2), -1), compute_uv=False) if n == 2 else None
    absW = Counter(np.round(np.abs([np.vdot(v, W @ v) for W in Ws]), 6))
    return best, len(opt), starts, profiles, schmidt, absW
def ident(x):
    mp.mp.dps = 20
    return dict(identify=str(mp.identify(x, tol=1e-11)), poly_deg4=str(mp.findpoly(x, 4, maxcoeff=2000, tol=1e-10)), as_fraction=str(mp.identify(x, tol=1e-11, constants=[])))
res = {}
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("\nres = {}")], cs)
pts, lag, w = cs["geometry"](3, 2); mps, _ = cs["maximal_partial_spreads"](lag)
S = next(sorted(S) for S in mps if len(S) == 5); cov = sorted(frozenset().union(*[lag[L] for L in S]))
best, nopt, st, profiles, schmidt, absW = optimise(3, 2, pts, cov, 120, 1)
res["pentad"] = dict(min_F=best, ident=ident(best), n_optimal=nopt, starts=st, n_profiles=len(profiles), schmidt=[float(s) for s in schmidt], absW_hist={str(k): c for k, c in sorted(absW.items())})
print("pentad", res["pentad"], flush=True)
qs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_ququint_sentinel_search.py")}
_src = open(os.path.join(HERE, "w33_ququint_sentinel_search.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("res = {}")], qs)
pts, lag, w = qs["geometry"](5, 2)
with contextlib.redirect_stdout(io.StringIO()):
    r = qs["search"](5, 1)
cov = sorted(frozenset().union(*[lag[L] for L in r["lines"]]))
best, nopt, st, profiles, schmidt, absW = optimise(5, 2, pts, cov, 60, 2)
res["d25_single_cover"] = dict(min_F=best, ident=ident(best), n_optimal=nopt, starts=st, n_profiles=len(profiles), schmidt=[float(s) for s in schmidt], absW_hist={str(k): c for k, c in sorted(absW.items())})
print("d25", res["d25_single_cover"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_nonstabiliser_optimisers.json"), "w"), indent=1)
