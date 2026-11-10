"""Pass 12644: exact identification of the pentad optimum.  Polish the optimal state, read the two levels |<W_u>|^2 (24 + 16 covered
vectors) at full precision, identify each in Q(sqrt57) and check F = (24 a + 16 b)/9 against (207 - 19 sqrt57)/432.
usage: py -3 analysis/w33_pentad_optimum_levels.py"""
import json, os, contextlib, io
import numpy as np, mpmath as mp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_nonstabiliser_optimisers.py")}
_src = open(os.path.join(HERE, "w33_nonstabiliser_optimisers.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index(chr(10) + "res = {}")], ns)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("\nres = {}")], cs)
pts, lag, w = cs["geometry"](3, 2); mps, _ = cs["maximal_partial_spreads"](lag)
S = next(sorted(S) for S in mps if len(S) == 5); cov = sorted(frozenset().union(*[lag[L] for L in S]))
Ws = ns["ops_for"](3, 2, pts, cov); d = 9
def F(z):
    v = z[:d] + 1j * z[d:]; v = v / np.linalg.norm(v)
    return float(np.sum(np.abs(np.einsum("i,kij,j->k", v.conj(), Ws, v)) ** 2)) / d
rng = np.random.default_rng(3)
best = min((minimize(F, rng.standard_normal(2 * d), method="BFGS", options=dict(gtol=1e-13)) for _ in range(40)), key=lambda r: r.fun)
v = best.x[:d] + 1j * best.x[d:]; v /= np.linalg.norm(v)
lv = np.sort(np.abs(np.einsum("i,kij,j->k", v.conj(), Ws, v)) ** 2)
a, b = float(np.mean(lv[:24])), float(np.mean(lv[24:]))
mp.mp.dps = 25
s57 = mp.sqrt(57)
ida = mp.identify(a, ["sqrt(57)"], tol=1e-12); idb = mp.identify(b, ["sqrt(57)"], tol=1e-12)
res = dict(F=best.fun, level_low=a, level_high=b, spread_low=float(np.ptp(lv[:24])), spread_high=float(np.ptp(lv[24:])), id_low=str(ida), id_high=str(idb),
           F_candidate=str((207 - 19 * s57) / 432), F_diff=float(best.fun - (207 - 19 * s57) / 432))
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_pentad_optimum_levels.json"), "w"), indent=1)
