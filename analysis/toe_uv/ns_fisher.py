"""Item 1: is the model-dependence of DESI's pull on n_s significant?  Fisher posteriors at the lowest-training fits of the neutral holdouts (Pass 12597): trained with BAO (SN held out) and without BAO (BAO held out), for LCDM, exponential, CPL, fading.  sigma(n_s) from the inverse Fisher of the training residuals, marginalised over all other parameters.
Pull significance: (n_s with BAO - n_s without) / sigma_without.  The two training sets share the CMB, so this is a rough indicator, not a proper difference test.
Likelihood: plik-lite + tau prior + lensing + f sigma8 + the other probe; not ACT DR6 primary spectra, which are not available here.
usage: python3 ns_fisher.py"""
import json
import math
import os
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
out = {}
for HOLD in ("sn", "bao"):
    sys.argv = ["x", "dovekie", HOLD]
    src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
    g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py"))
    exec(src, g)
    F, C, BMASK, SN, FREE, kind_of = g["F"], g["C"], g["BMASK"], g["SN"], g["FREE"], g["kind_of"]
    neu = json.load(open(f"class_holdout_dovekie_{HOLD}_neutral.json"))
    for m in ("LCDM", "exp", "cpl", "free_neg"):
        best = min(neu["rows"][m], key=lambda r: r["train_chi2"])
        p0 = dict(best["p"])
        k = kind_of(m)
        free = C.NAMES + FREE[m]

        def tr(p):
            F.sn = None if HOLD == "sn" else SN
            BMASK["on"] = True
            r = F.resid(p, k)[0]
            F.sn = SN
            BMASK["on"] = False
            return r

        J = []
        for n in free:
            st = C.STEP[n]
            pu, pd = dict(p0), dict(p0)
            pu[n] += st
            pd[n] -= st
            J.append((tr(pu) - tr(pd)) / (2 * st))
        J = np.array(J).T
        cov = np.linalg.inv(J.T @ J)
        i = free.index("ns")
        key = f"{m}_without_{'sn' if HOLD == 'sn' else 'bao'}"
        out[key] = dict(ns=p0["ns"], sigma=float(math.sqrt(cov[i, i])))
        print(key, "ns %.4f +- %.4f" % (p0["ns"], math.sqrt(cov[i, i])), flush=True)
        json.dump(out, open("ns_fisher.json", "w"), indent=1)
sig = {}
for m in ("LCDM", "exp", "cpl", "free_neg"):
    a, b = out[f"{m}_without_sn"], out[f"{m}_without_bao"]
    sig[m] = dict(pull=a["ns"] - b["ns"], sigma_without_bao=b["sigma"], significance=(a["ns"] - b["ns"]) / b["sigma"], distance_from_0965_sigma=(a["ns"] - 0.965) / a["sigma"])
out["pull_significance"] = sig
json.dump(out, open("ns_fisher.json", "w"), indent=1)
print("pull", {m: (round(v["pull"], 4), round(v["significance"], 2), round(v["distance_from_0965_sigma"], 2)) for m, v in sig.items()}, flush=True)
