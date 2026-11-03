"""Two checks on dark_ceiling.py and fading_ds.py.  (1) A denser ceiling, 13 bins with more starts, because the 6 and 9 bin ceilings are not nested and a ceiling is only as good as its optimiser.  (2) Remove supernovae below zmin = 0.1 (full covariance submatrix): the w >= -1 gain sits at z < 0.2, the range where low-z samples are spliced to the high-z ones.
For each cut: LCDM, CPL, uncoupled exponential, fading dark sector with c < 0, ceiling.  Control: at zmin = 0 the CPL and fading values must equal the earlier runs.  usage: py -3 dark_lowz.py dataset data_dir zmin"""
import json
import sys
import numpy as np
from scipy.optimize import minimize

ds_, ddir_, zmin = sys.argv[1], sys.argv[2], float(sys.argv[3])
sys.argv = ["x", ds_, ddir_]
exec(open("fading_ds.py", encoding="utf-8").read().split("out = dict(dataset=ds)")[0])
if zmin > 0:
    keep = sn["ZC"] > zmin
    Cv = np.linalg.inv(sn["IC"])
    IC2 = np.linalg.inv(Cv[keep][:, keep])
    sn = dict(ZC=sn["ZC"][keep], ZH=sn["ZH"][keep], MU=sn["MU"][keep], IC=IC2, sum=IC2.sum(), ones=IC2.sum(1), n=int(keep.sum()))
EDGES = [0, 0.03, 0.07, 0.12, 0.18, 0.25, 0.35, 0.5, 0.7, 1.0, 1.4, 2.0, 3.0, 5.0]
S = [1e-4, 1e-3, 3e-3]
out = dict(dataset=ds_, zmin=zmin, n=sn["n"], edges=EDGES)
lc = nm(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], sn), [0.02223, 0.142, 0.675], S, 800)
out["LCDM"] = dict(chi2=lc.fun, x=list(lc.x))
cp = nm(lambda p: L.chi2(L.E_cpl(p[1], p[2], p[3], p[4]), p[2], p[0], p[1], sn) if p[3] + p[4] < 0 else 1e8, list(lc.x) + [-0.85, -0.5], S + [0.05, 0.2], 1500)
out["CPL"] = dict(delta=cp.fun - lc.fun, w0=cp.x[3], wa=cp.x[4])
un = nm(lambda p: like(p[3], 0.0, p[0], p[1], p[2]) if p[3] >= 0 else 1e8, list(lc.x) + [0.6], S + [0.2], 450)
out["uncoupled"] = dict(delta=un.fun - lc.fun, c=un.x[3])
fd = nm(lambda p: like(p[3], p[4], p[0], p[1], p[2]) if p[3] < 0 and p[4] >= 0 else 1e8, list(lc.x) + [-0.9, 0.05], S + [0.2, 0.01], 700)
out["fading_c_neg"] = dict(delta=fd.fun - lc.fun, c=fd.x[3], cp=fd.x[4])
print(ds_, zmin, sn["n"], {k: {a: round(float(b), 3) for a, b in out[k].items()} for k in ("CPL", "uncoupled", "fading_c_neg")}, flush=True)


def f(p):
    return L.chi2(L.E_binned(p[1], p[2], EDGES, p[3:]), p[2], p[0], p[1], sn)


nb = len(EDGES) - 1
bounds = [(0.020, 0.025), (0.13, 0.155), (0.55, 0.80)] + [(-1.0, 1.0)] * nb
rng = np.random.default_rng(11)
starts = [np.full(nb, -0.95), np.r_[np.full(3, -0.75), np.full(nb - 3, -1.0)], np.r_[np.full(1, -0.5), np.full(nb - 1, -1.0)], np.linspace(-0.7, -1.0, nb)] + [np.clip(rng.normal(-0.9, 0.1, nb), -1, 1) for _ in range(4)]
best, runs = None, []
for w in starts:
    r = minimize(f, np.r_[lc.x, w], method="L-BFGS-B", bounds=bounds, options=dict(maxiter=500, eps=1e-5, ftol=1e-10))
    r2 = minimize(f, r.x, method="Powell", bounds=bounds, options=dict(maxiter=4000, xtol=1e-5, ftol=1e-7))
    runs.append(r2.fun - lc.fun)
    if best is None or r2.fun < best.fun:
        best = r2
out["ceiling_13bins"] = dict(delta=best.fun - lc.fun, w=list(best.x[3:]), h=best.x[2], wbc=best.x[1], all_starts=runs)
print("ceiling", round(best.fun - lc.fun, 3), np.round(best.x[3:], 3).tolist(), "starts", np.round(runs, 2).tolist(), flush=True)
json.dump(out, open(f"dark_lowz_{ds_}_{zmin}.json", "w"), indent=1, default=float)
print("done", flush=True)
