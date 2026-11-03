"""Fits of Lambda + Casimir + sparse tower with casimir_fast.py.  Compressed CMB, background only.  Free: omega_b, omega_bc, h, prod = f b, eps; slope n b with n = 4 unless scanned.
1 control: casimir_fast against dm_drag.solve at the same parameters.
2 for b in (1/sqrt 2, sqrt(6/7), 1, sqrt(3/2)), both signs of eps, several starts.
3 profile in eps at b = 1/sqrt 2, s = -1, for the interval on eps and so on R.
4 scan of the exponent n: does the data pick 4?
5 the no-drag control, prod -> 0.
R from eps: |V_C| = |N| (3 zeta(5)/(64 pi^6)) / R^4; N = 5 for the 5D graviton alone.
usage: py -3 casimir_fits.py dataset data_dir"""
import json
import math
import sys
import time
import numpy as np
from scipy.optimize import minimize
import dark_like as L
import casimir_fast as CF

ds, dd = sys.argv[1], sys.argv[2]
sn = L.load_sn(ds, dd)
S = [1e-4, 1e-3, 3e-3]
COEF = 3 * 1.0369277551433699 / (64 * math.pi ** 6)
HC = 0.1973269804


def nm(fn, x0, steps, maxiter):
    x0 = np.asarray(x0, float)
    return minimize(fn, x0, method="Nelder-Mead", options=dict(xatol=3e-5, fatol=3e-3, maxiter=maxiter, maxfev=maxiter, initial_simplex=np.vstack([x0] + [x0 + np.eye(len(x0))[i] * steps[i] for i in range(len(x0))])))


def X(b, prod, n, Z, wb, wbc, h):
    if not (0 < prod <= b):
        return 1e8
    try:
        return L.chi2(CF.solve(b, prod, n, Z, wb, wbc, h), h, wb, wbc, sn)
    except Exception:
        return 1e8


lc = nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], sn), [0.02223, 0.142, 0.675], S, 800)
prev = json.load(open(f"fading_ds_{ds}.json"))
fn = prev["free_c_neg"]
x0 = [fn["wb"], fn["wbc"], fn["h"]]
out = dict(dataset=ds, LCDM=lc.fun, fading_neg=fn["delta"], fading_pos=prev["free_c_pos"]["delta"], c_neg=fn["c"], c_pos=prev["free_c_pos"]["c"])
name = f"casimir_fits_{ds}.json"
t = time.time()
for _ in range(10):
    X(0.7071, 0.05, 4.0, -0.5, *x0)
out["seconds_per_eval"] = (time.time() - t) / 10
print("seconds per eval", out["seconds_per_eval"], flush=True)


def eps_of(b, prod, n, Z, x):
    try:
        return CF.solve(b, prod, n, Z, x[0], x[1], x[2], want=True)[1]["eps"]
    except Exception:
        return None  # the optimiser ended on a rejected point


def Rs(eps, h):
    crit = 3 * (100 * h * 1000 / 3.085677581491367e22 * 6.582119569e-16) ** 2 * (2.435e27) ** 2
    return {str(N): HC * (N * COEF / (abs(eps) * crit)) ** 0.25 for N in (1, 5, 7, 20)}


def rec(b, n, r):
    wb, wbc, h, prod, Z = r.x
    _, inf = CF.solve(b, prod, n, Z, wb, wbc, h, want=True)
    eps = inf["eps"]
    return dict(delta=r.fun - lc.fun, wb=wb, wbc=wbc, h=h, prod=prod, f=prod / b, Z=Z, eps=eps, R_micron=Rs(eps, h), info=inf)


def save():
    json.dump(out, open(name, "w"), indent=1, default=float)


# 2 best fits, resumed from an earlier run of this script when present
import os
out["best"] = json.load(open(name))["best"] if os.path.exists(name) else {}
for b in (0.7071, 0.9258, 1.0, 1.2247):
    for s_ in (-1, 1):
        if f"{b}_{s_}" in out["best"]:
            continue
        best = None
        for prod0, e0 in ((0.05, 0.2), (0.04, 0.4), (0.03, 0.1)):
            Z0 = s_ * e0 * math.exp(4 * b * 0.3)
            r = nm(lambda p: X(b, p[3], 4.0, p[4], p[0], p[1], p[2]) if p[4] * s_ > 0 else 1e8, x0 + [prod0, Z0], S + [0.008, 0.1 * Z0], 600)
            if best is None or r.fun < best.fun:
                best = r
        k = f"{b}_{s_}"
        out["best"][k] = rec(b, 4.0, best)
        v = out["best"][k]
        print(k, "delta", round(v["delta"], 2), "prod", round(v["prod"], 4), "f", round(v["f"], 4), "eps", round(v["eps"], 4), "c_eff", round(v["info"]["c_eff"], 3), "dlnm", round(v["info"]["dln_mKK_rec_to_0"], 3), "R5", round(v["R_micron"]["5"], 2), "w", {a: round(c, 3) for a, c in v["info"]["w_phi"].items()}, flush=True)
        save()
base = out["best"]["0.7071_-1"]
xb = [base["wb"], base["wbc"], base["h"]]
# 3 profile in eps
out["eps_profile"] = {}
for mult in (0.0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.7, 0.85, 1.0, 1.2, 1.5, 2.0, 3.0):
    zz = mult * base["Z"]
    r = nm(lambda p: X(0.7071, p[3], 4.0, zz, p[0], p[1], p[2]), xb + [base["prod"]], S + [0.008], 350)
    e = eps_of(0.7071, r.x[3], 4.0, zz, r.x) if zz else 0.0
    out["eps_profile"][str(mult)] = dict(Z=zz, eps=e, delta=r.fun - lc.fun, prod=r.x[3], h=r.x[2], R5=(Rs(e, r.x[2])["5"] if e else None))
    print("Z mult", mult, "eps", e, round(r.fun - lc.fun, 2), "prod", round(r.x[3], 4), flush=True)
    save()
# 4 exponent scan
out["n_scan"] = {}
for n in (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 12.0):
    best = None
    for e0 in (base["eps"], base["eps"] * 4 / n):
        z0 = e0 * math.exp(n * 0.7071 * base["info"]["chi0"])
        r = nm(lambda p: X(0.7071, p[3], n, p[4], p[0], p[1], p[2]) if p[4] < 0 else 1e8, xb + [base["prod"], z0], S + [0.008, 0.1 * z0], 450)
        if best is None or r.fun < best.fun:
            best = r
    en = eps_of(0.7071, best.x[3], n, best.x[4], best.x)
    out["n_scan"][str(n)] = dict(delta=best.fun - lc.fun, prod=best.x[3], Z=best.x[4], eps=en)
    print("n", n, round(best.fun - lc.fun, 2), "prod", round(best.x[3], 4), "eps", en, flush=True)
    save()
# 5 no drag
r = nm(lambda p: X(0.7071, 1e-7, 4.0, p[3], p[0], p[1], p[2]) if p[3] < 0 else 1e8, xb + [base["Z"]], S + [0.1 * base["Z"]], 400)
out["no_drag"] = dict(delta=r.fun - lc.fun, Z=r.x[3], eps=eps_of(0.7071, 1e-7, 4.0, r.x[3], r.x))
print("no drag", round(r.fun - lc.fun, 2), out["no_drag"]["eps"], flush=True)
save()
print("done", flush=True)
