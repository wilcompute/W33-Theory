"""The ceiling for all uncoupled dark energy obeying the null energy condition: canonical fields, any number, any potential, k-essence with positive kinetic term.  All have w >= -1, so rho_DE never increases.
Fit piecewise constant w(z) with w >= -1 on six bins (ceiling), and with w free (control: must reach at least about the CPL gain).  Several starts per fit, since a ceiling is only as good as the optimiser.
Controls also: LCDM and CPL with the same likelihood against published w0, wa.  usage: py -3 dark_ceiling.py dataset data_dir"""
import json
import sys
import numpy as np
from scipy.optimize import minimize
import dark_like as L

ds, ddir = sys.argv[1], sys.argv[2]
sn = L.load_sn(ds, ddir)
EDGES = [0, 0.15, 0.35, 0.6, 1.0, 1.6, 2.5]
EDGES2 = [0, 0.1, 0.2, 0.35, 0.5, 0.7, 1.0, 1.4, 2.0, 3.0]


def nm(fn, x0):
    return minimize(fn, x0, method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-3, maxiter=4000, maxfev=4000))


out = dict(dataset=ds, n=None if sn is None else sn["n"], cal=L.CAL)
lc = nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], sn), [0.02223, 0.142, 0.675])
out["LCDM"] = dict(chi2=lc.fun, wb=lc.x[0], wbc=lc.x[1], h=lc.x[2], parts=L.chi2(L.E_lcdm(lc.x[1], lc.x[2]), lc.x[2], lc.x[0], lc.x[1], sn, parts=True))
cp = nm(lambda p: L.chi2(L.E_cpl(p[1], p[2], p[3], p[4]), p[2], p[0], p[1], sn) if p[3] + p[4] < 0 else 1e8, [0.02223, 0.142, 0.675, -0.85, -0.5])
out["CPL"] = dict(chi2=cp.fun, delta=cp.fun - lc.fun, wb=cp.x[0], wbc=cp.x[1], h=cp.x[2], w0=cp.x[3], wa=cp.x[4])
print({k: (v if k == "dataset" else v) for k, v in out.items() if k in ("LCDM", "CPL")}, flush=True)


def fitbins(edges, lower, upper=1.0):
    nb = len(edges) - 1
    def f(p):
        return L.chi2(L.E_binned(p[1], p[2], edges, p[3:]), p[2], p[0], p[1], sn)
    bounds = [(0.020, 0.025), (0.13, 0.155), (0.55, 0.80)] + [(lower, upper)] * nb
    best = None
    rng = np.random.default_rng(5)
    starts = [np.full(nb, -0.9), np.linspace(-0.75, -0.98, nb), np.linspace(-0.98, -0.6, nb)]
    if lower < -1:
        starts += [np.linspace(-0.7, -1.4, nb)]
    starts += [np.clip(rng.normal(-0.85, 0.15, nb), lower, upper) for _ in range(2)]
    for w in starts:
        r = minimize(f, np.r_[lc.x, w], method="L-BFGS-B", bounds=bounds, options=dict(maxiter=400, eps=1e-5, ftol=1e-9))
        r2 = minimize(f, r.x, method="Powell", bounds=bounds, options=dict(maxiter=3000, xtol=1e-5, ftol=1e-7))
        if best is None or r2.fun < best.fun:
            best = r2
    return dict(chi2=best.fun, delta=best.fun - lc.fun, wb=best.x[0], wbc=best.x[1], h=best.x[2], w=list(best.x[3:]), edges=edges)


for label, edges, lower in (("ceiling_6bins", EDGES, -1.0), ("free_6bins", EDGES, -6.0), ("ceiling_9bins", EDGES2, -1.0), ("free_9bins", EDGES2, -6.0)):
    out[label] = fitbins(edges, lower)
    print(label, round(out[label]["delta"], 3), np.round(out[label]["w"], 3).tolist(), flush=True)
    json.dump(out, open(f"dark_ceiling_{ds}.json", "w"), indent=1, default=float)
