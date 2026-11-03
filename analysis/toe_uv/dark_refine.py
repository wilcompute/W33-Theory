"""Global refinement of the w >= -1 ceiling: differential evolution seeded from the best local fit in dark_lowz_*.json, then a bounded local polish.  Also the same search with w free, on the same 13 bins, so ceiling and free are comparable.  The result is still the best found, so a lower limit on the true gain; it is reported with the spread between two seeds.
Also c' alone (c = 0) and c alone (c' = 0, from dark_lowz) with and without the cut, to see which parameter carries the fading dark sector gain.  usage: py -3 dark_refine.py dataset data_dir zmin"""
import json
import sys
import numpy as np
from scipy.optimize import differential_evolution, minimize

ds_, ddir_, zmin = sys.argv[1], sys.argv[2], float(sys.argv[3])
sys.argv = ["x", ds_, ddir_]
exec(open("fading_ds.py", encoding="utf-8").read().split("out = dict(dataset=ds)")[0])
if zmin > 0:
    keep = sn["ZC"] > zmin
    Cv = np.linalg.inv(sn["IC"])
    IC2 = np.linalg.inv(Cv[keep][:, keep])
    sn = dict(ZC=sn["ZC"][keep], ZH=sn["ZH"][keep], MU=sn["MU"][keep], IC=IC2, sum=IC2.sum(), ones=IC2.sum(1), n=int(keep.sum()))
prev = json.load(open(f"dark_lowz_{ds_}_{zmin}.json"))
EDGES = prev["edges"]
nb = len(EDGES) - 1
lc0 = prev["LCDM"]
lcx = lc0["x"]
S = [1e-4, 1e-3, 3e-3]


def f(p):
    return L.chi2(L.E_binned(p[1], p[2], EDGES, p[3:]), p[2], p[0], p[1], sn)


out = dict(dataset=ds_, zmin=zmin, edges=EDGES, lcdm_chi2=lc0["chi2"], local_best=prev["ceiling_13bins"]["delta"])
x0 = np.r_[prev["ceiling_13bins"].get("wb", lcx[0]), prev["ceiling_13bins"]["wbc"], prev["ceiling_13bins"]["h"], prev["ceiling_13bins"]["w"]]
for label, lo in (("ceiling", -1.0), ("free", -6.0)):
    bounds = [(0.0215, 0.023), (0.135, 0.150), (0.62, 0.74)] + [(lo, 1.0)] * nb
    res = []
    for seed in (1, 2):
        rng = np.random.default_rng(seed)
        np_ = 80
        init = np.tile(x0, (np_, 1))
        init[:, :3] += rng.normal(size=(np_, 3)) * [2e-4, 1e-3, 5e-3]
        init[:, 3:] += rng.normal(size=(np_, nb)) * (0.1 if lo == -1.0 else 0.35)
        init = np.clip(init, [b[0] for b in bounds], [b[1] for b in bounds])
        init[0] = np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds])
        d = differential_evolution(f, bounds, init=init, maxiter=350, tol=1e-4, seed=seed, polish=False, mutation=(0.4, 0.9), recombination=0.7)
        r = minimize(f, d.x, method="Powell", bounds=bounds, options=dict(maxiter=4000, xtol=1e-5, ftol=1e-7))
        res.append(dict(delta=r.fun - lc0["chi2"], w=list(r.x[3:]), h=r.x[2], wbc=r.x[1]))
        print(label, seed, round(res[-1]["delta"], 3), np.round(r.x[3:], 2).tolist(), flush=True)
        out[label] = res
        json.dump(out, open(f"dark_refine_{ds_}_{zmin}.json", "w"), indent=1, default=float)
cp = nm(lambda p: like(0.0, p[3], p[0], p[1], p[2]) if p[3] >= 0 else 1e8, list(lcx) + [0.05], S + [0.01], 450)
out["cprime_only"] = dict(delta=cp.fun - lc0["chi2"], cp=cp.x[3])
print("c' only", out["cprime_only"], flush=True)
json.dump(out, open(f"dark_refine_{ds_}_{zmin}.json", "w"), indent=1, default=float)
print("done", flush=True)
