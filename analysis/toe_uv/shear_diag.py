"""Why does CPL predict shear worse?  KiDS-Legacy (or DES with SURVEY=des) diagnostic at the stored fixed-background best fits (sign_des[_kids].json: Dovekie full-data cosmologies with nuisances fitted).
For LCDM, fading (c<0) and CPL: model xi minus data per point, in units of the diagonal error; summed per tomographic pair, split into xi+ and xi-; plus the fractional model difference CPL/fading per pair.
Also the lensing-relevant growth: sigma8(z) ratio CPL/fading and Omega_m from the CLASS runs.
usage: SURVEY=kids python3 shear_diag.py"""
import json, os, sys
import numpy as np
BG = os.path.dirname(os.path.abspath(__file__)); os.chdir(BG); sys.path.insert(0, BG)
SURV = os.environ.get("SURVEY", "kids")
sys.argv = ["x", "dovekie", "joint", "LCDM"]
src = open("class_des_fit.py", encoding="utf-8").read().split("F = SF(ds_)")[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_des_fit.py")); exec(src, g)
SF, xi_model, DATA, keep, COV, KB, KJ, ISM, NB = (g[k] for k in ("SF", "xi_model", "DATA", "keep", "COV", "KB", "KJ", "ISM", "NB"))
F = SF("dovekie")
fits = json.load(open("class_fit_dovekie.json"))
nu = json.load(open("sign_des_kids.json" if SURV == "kids" else "sign_des.json"))
err = np.sqrt(np.diag(COV)); d = DATA[keep]; ism = ISM[keep]
out = {}
models = {}
for m in ("LCDM", "free_neg", "CPL"):
    p = dict(fits[m]["p"], mnu=0.06, **nu[m]["nuis"])
    parts, T, info = F.cosmo(p, "cpl" if m == "CPL" else "fading")
    mod = xi_model(T, p)
    models[m] = mod
    r = (mod - d) / err
    per = {}
    for i in range(NB):
        for j in range(i, NB):
            sel = (KB == i) & (KJ == j) | (KB == j) & (KJ == i)
            per[f"{i}{j}"] = dict(plus=float(r[sel & ~ism].sum()), minus=float(r[sel & ism].sum()))
    out[m] = dict(S8=info["S8"], om=info["om"], s8=info["s8"], mean_resid_plus=float(r[~ism].mean()), mean_resid_minus=float(r[ism].mean()), per_pair=per)
    print(m, "S8 %.4f Om %.4f s8 %.4f | mean (model-data)/err: xi+ %+.3f xi- %+.3f" % (info["S8"], info["om"], info["s8"], r[~ism].mean(), r[ism].mean()), flush=True)
# chi2 decomposition with proper sub-covariances: low-z pairs (both bins in the lower half) vs high-z pairs (both in the upper half) vs mixed; xi+ and xi- together
half = NB // 2
lowsel = (KB < half) & (KJ < half)
highsel = (KB >= half) & (KJ >= half)
mixsel = ~(lowsel | highsel)
dec = {}
for m, mod in models.items():
    r = mod - d
    row = {}
    for lab, sel in (("low", lowsel), ("high", highsel), ("mixed", mixsel), ("all", np.ones_like(lowsel))):
        Cs = COV[np.ix_(sel, sel)]
        rs = r[sel]
        row[lab] = float(rs @ np.linalg.solve(Cs, rs))
    dec[m] = row
    print(m, "chi2 blocks", {k: round(v, 2) for k, v in row.items()}, flush=True)
out["chi2_blocks"] = dec
out["cpl_minus_fading_blocks"] = {k: dec["CPL"][k] - dec["free_neg"][k] for k in dec["CPL"]}
out["cpl_minus_lcdm_blocks"] = {k: dec["CPL"][k] - dec["LCDM"][k] for k in dec["CPL"]}
print("CPL - fading by block", {k: round(v, 2) for k, v in out["cpl_minus_fading_blocks"].items()}, flush=True)
rat = models["CPL"] / models["free_neg"]
byp = {}
for i in range(NB):
    for j in range(i, NB):
        sel = ((KB == i) & (KJ == j) | (KB == j) & (KJ == i)) & ~ism
        byp[f"{i}{j}"] = float(np.mean(rat[sel]) - 1)
out["cpl_over_fading_xiplus_minus1_by_pair"] = byp
print("CPL/fading - 1 (xi+) by pair:", {k: round(v * 100, 2) for k, v in byp.items()}, flush=True)
json.dump(out, open(f"shear_diag_{SURV}.json", "w"), indent=1, default=float)
