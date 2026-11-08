"""Hold out DES Y3 cosmic shear and predict it: posterior-predictive elpd for LCDM, fading (c<0 and c>0 modes) and CPL.
Training = plik-lite + tau + DESI + Dovekie SN + lensing + f sigma8 (everything except shear), at the full-data best fits (class_fit_dovekie.json) with the Fisher covariance of that training likelihood (class_holdout machinery, as in ns_cp_fisher.py).
Draws: ND per model from the Fisher Gaussian, truncated to the flat priors (as class_ppd.py).  For each draw the ten DES nuisances are refitted (cheap: cosmology cached) and chi2_shear = des + nuisance-prior is used, a profile approximation to marginalising the nuisances.
elpd_shear = ln < exp(-chi2_shear/2) >.  Run with one threaded CLASS process (see memory: parallel copies are slower).
usage: python3 shear_ppd.py ND"""
import json
import math
import os
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
sys.path.insert(0, BG)
ND = int(sys.argv[1]) if len(sys.argv) > 1 else 20
sys.argv = ["x", os.environ.get("DSET", "dovekie"), "sn"]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py"))
exec(src, g)
F, C, BMASK, SN = g["F"], g["C"], g["BMASK"], g["SN"]
C.STEP.update(w0=0.02, wa=0.08)
sys.argv = ["x", "dovekie", "joint", "LCDM"]
src2 = open("class_des_fit.py", encoding="utf-8").read().split("F = SF(ds_)")[0]
g2 = dict(__name__="x", __file__=os.path.join(BG, "class_des_fit.py"))
exec(src2, g2)
SF, NUIS, PRIM = g2["SF"], g2["NUIS"], g2["PRIM"]
D = SF("dovekie")
BOUNDS = dict(c=(-3.0, 3.0), cp=(0.0, 0.2), w0=(-3.0, 1.0), wa=(-5.0, 3.0), tau=(0.01, 0.2))
FREE = dict(LCDM=[], free_neg=["c", "cp"], free_pos=["c", "cp"], CPL=["w0", "wa"])
DSET = os.environ.get("DSET", "dovekie")
fits = json.load(open(f"class_fit_{DSET}.json"))
rng = np.random.default_rng(20261106)
path = "shear_ppd.json" if DSET == "dovekie" else f"shear_ppd_{DSET}.json"
out = json.load(open(path)) if os.path.exists(path) else {}
start_n = {f"m{i}": float(PRIM[0][i]) for i in range(4)}
start_n.update({f"dz{i}": 0.0 for i in range(4)}, Aia=0.3, eta=0.0)


def ok(q):
    if any(n in q and not (lo <= q[n] <= hi) for n, (lo, hi) in BOUNDS.items()):
        return False
    return not ("w0" in q and q["w0"] + q["wa"] >= 0)


for m in ("LCDM", "free_neg", "free_pos", "CPL"):
    if m in out:
        continue
    kind = "cpl" if m == "CPL" else "fading"
    p0 = dict(fits[m]["p"])
    free = C.NAMES + FREE[m]

    def tr(p):
        F.sn = SN
        BMASK["on"] = True
        return F.resid(p, kind)[0]

    J = []
    for n in free:
        st = C.STEP[n]
        pu, pd = dict(p0), dict(p0)
        pu[n] += st
        pd[n] -= st
        J.append((tr(pu) - tr(pd)) / (2 * st))
    J = np.array(J).T
    cov = np.linalg.inv(J.T @ J)
    Lc = np.linalg.cholesky(cov + 1e-14 * np.eye(len(free)))
    chis, rej, fail = [], 0, 0
    for k in range(ND):
        for _ in range(200):
            q = dict(p0)
            x = Lc @ rng.standard_normal(len(free))
            for i, n in enumerate(free):
                q[n] = p0[n] + x[i]
            if ok(q):
                break
            rej += 1
        try:
            r = D.fit(dict(q, mnu=0.06, **start_n), NUIS, kind=kind, iters=4, log=lambda *a, **k: None)
            chis.append(r["parts"]["des"] + r["parts"]["desp"])
        except Exception as e:
            fail += 1
            print("draw failed", str(e)[-80:], flush=True)
        print(m, k, round(chis[-1], 2) if chis else None, flush=True)
    chis = np.array(chis)
    elpd = float(np.logaddexp.reduce(-0.5 * chis) - math.log(len(chis)))
    out[m] = dict(n=len(chis), elpd_shear=elpd, chi2_q=[float(v) for v in np.quantile(chis, [0.16, 0.5, 0.84])], rejected=rej, failed=fail, sd={n: float(math.sqrt(cov[i, i])) for i, n in enumerate(free) if n in FREE[m]})
    print(m, "elpd_shear %.2f" % elpd, out[m]["chi2_q"], flush=True)
    json.dump(out, open(path, "w"), indent=1)
print("shearppd done", flush=True)
