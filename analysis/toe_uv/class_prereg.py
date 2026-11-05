"""Pre-registered predictions: the only truly blind test available.  All data so far were seen before the models were chosen.  So freeze, under a git commit, predictions with bands for observables not yet published at this precision, and score them later.  No result here is evidence until new data arrive.
Models: LCDM and fading (c, c' free), plus the relaxing radion at its best fit, trained on plik-lite + tau prior + DESI DR2 + SN + ACT/Planck lensing + f sigma8.
Observables: D_M/r_d and D_H/r_d at DESI redshifts; f sigma8(z) at 0.1 to 1.5; S8; sigma8(z); C_L^kk at L = 40, 100, 400, 1000; the matter fraction; a drift-of-mass number for fading: m_DM(z)/m_DM(0); growth index gamma(z) = dln f / dln Om(z) style, defined as ln f / ln Om_m(z) with Om_m the actual clustering fraction.
Bands: Gaussian draws from the inverse Fisher at the best fit.  This underestimates the width along the c, c' direction, where the posterior is not Gaussian (the Fisher gives c' = 0.052 +- 0.008 while Delta chi2 implies 0.052 +- 0.017), so the c' block is inflated by a stated factor INFL = 2.  Read the bands as approximate.
usage: python3 class_prereg.py dataset [ndraw]"""
import hashlib
import json
import math
import os
import subprocess
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
ds_ = sys.argv[1]
ND = int(sys.argv[2]) if len(sys.argv) > 2 else 24
sys.argv = ["x", ds_, "none"]
src = open("class_growth_fit.py", encoding="utf-8").read().split("F = GF(ds)")[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_growth_fit.py"))
exec(src, g)
C, GF, sigma8_from, MBIN = (g[k] for k in ("C", "GF", "sigma8_from", "MBIN"))
INFL = 2.0
base = json.load(open(f"class_growth_{ds_}_none.json"))
F = GF(ds_)
ZB = [0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33]
ZF = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
ZP = sorted({round(z + d, 3) for z in ZF for d in (-0.03, 0.0, 0.03)})
LS = [40, 100, 400, 1000]
FREE = dict(LCDM=[], free_neg=["c", "cp"], relax=["prod", "Zn"])


def obs(p):
    extra = "z_pk=" + ",".join(map(str, ZP)) + "\nz_max_pk=2.0"
    binp = C.CLASSBIN
    if "Zn" in p:
        b = p["b"]
        extra += f"\nscf_parameters={4 * b},{b},2.0,{p['Zn']},{p['lnxi']},2,0.0,0.0\nf_idm={1 - p['prod'] / b}"
        binp = MBIN
    kp = {}
    cl, z, H, dc, info = C.run_class(p, "fading", extra=extra, binp=binp, keep=kp)
    t = kp["tag"]
    h = p["h"]
    s8 = {zz: sigma8_from(f"{t}/o_z{i + 1}_pk.dat", h) for i, zz in enumerate(ZP)}
    d = np.loadtxt(t + "/o_cl_lensed.dat")
    cols = C.titles(t + "/o_cl_lensed.dat")
    ell = d[:, 0]
    pp = d[:, cols.index("phiphi")] * 2 * np.pi / (ell * (ell + 1))
    kk = (ell * (ell + 1)) ** 2 * pp / 4
    bc = kp["cols"]
    raw = kp["raw"][::-1]
    zb = raw[:, bc.index("z")]
    rc = raw[:, bc.index("(.)rho_cdm")] + (raw[:, bc.index("(.)rho_idm")] if "(.)rho_idm" in bc else 0.0)
    rb = raw[:, bc.index("(.)rho_b")]
    Hb = raw[:, bc.index("H [1/Mpc]")]
    subprocess.run(["rm", "-rf", t])
    rd = info["rd"]
    o = {}
    for zz in ZB:
        o[f"DM_rd_{zz}"] = float(np.interp(zz, z, dc)) / rd
        o[f"DH_rd_{zz}"] = 1 / float(np.interp(zz, z, H)) / rd
    for zz in ZF:
        a, b_ = round(zz - 0.03, 3), round(zz + 0.03, 3)
        fs = -(1 + zz) * (s8[b_] - s8[a]) / (b_ - a)
        o[f"fs8_{zz}"] = fs
        o[f"s8_{zz}"] = s8[round(zz, 3)]
        Om = float(np.interp(zz, zb, (rc + rb) / Hb ** 2))
        fg = fs / s8[round(zz, 3)]
        o[f"gamma_{zz}"] = math.log(fg) / math.log(Om)
    for L in LS:
        o[f"Ckk_{L}"] = float(np.interp(L, ell, kk))
    o["S8"] = info["S8"]
    o["om"] = info["om"]
    rc3 = rc * (1 + 0) / (1 + zb) ** 3
    for zz in (0.5, 1.0, 2.0, 1090.0):
        o[f"rhoc_a3_ratio_{zz}"] = float(np.interp(zz, zb, rc3) / rc3[0])
    return o


path = f"class_prereg_{ds_}.json"
out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds_, trained_on="plik-lite + tau + DESI DR2 + SN + ACT/Planck lensing + f sigma8", inflation_c_block=INFL, models={})
rng = np.random.default_rng(20261105)
for m in ("LCDM", "free_neg", "relax"):
    if m in out["models"]:
        continue
    p = dict(base[m]["p"])
    best = obs(p)
    row = dict(best=best, p=p)
    if m != "relax":
        free = C.NAMES + FREE[m]
        J = []
        for n in free:
            st = C.STEP[n]
            pu, pd = dict(p), dict(p)
            pu[n] += st
            pd[n] -= st
            J.append((F.resid(pu, "fading")[0] - F.resid(pd, "fading")[0]) / (2 * st))
        J = np.array(J).T
        cov = np.linalg.inv(J.T @ J)
        for i, n in enumerate(free):
            if n in FREE[m]:
                cov[i, :] *= INFL
                cov[:, i] *= INFL
        L = np.linalg.cholesky(cov + 1e-14 * np.eye(len(free)))
        draws = []
        for k in range(ND):
            x = L @ rng.standard_normal(len(free))
            q = dict(p)
            for i, n in enumerate(free):
                q[n] = p[n] + x[i]
            q["tau"] = max(q["tau"], 0.01)
            try:
                draws.append(obs(q))
            except Exception as e:
                print("draw failed", str(e)[-100:], flush=True)
        row["ndraw"] = len(draws)
        row["sd"] = {k: float(np.std([d[k] for d in draws], ddof=1)) for k in best}
        row["cov_diag"] = {n: float(cov[i, i]) for i, n in enumerate(free)}
    out["models"][m] = row
    print(m, "done", row.get("ndraw"), flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)
out["sha256_of_models"] = hashlib.sha256(json.dumps(out["models"], sort_keys=True, default=float).encode()).hexdigest()
json.dump(out, open(path, "w"), indent=1, default=float)
print("preregdone", out["sha256_of_models"], flush=True)
