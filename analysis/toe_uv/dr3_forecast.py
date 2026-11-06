"""Can DESI DR3 BAO tell fading, CPL and LCDM apart?  Asimov comparison of the frozen point predictions (dr3_prereg.json, sha 6d76b63b).
Errors: DESI DR2 (dark_like.DATA) scaled by sqrt(3/5) for five years of data instead of three (a rough volume scaling, my assumption); the DR2 DM-DH correlations kept.
Delta chi2(A|B) = (pred_A - pred_B)^T C^-1 (pred_A - pred_B) over the DR2 redshifts.  This is an UPPER bound on discrimination: the models are not refitted to each other's mock data, and refitting absorbs part of the difference.
Also: the same with the actual DR2 errors (unscaled), as a control that should give smaller numbers.
usage: py -3 dr3_forecast.py"""
import itertools
import json
import math
import numpy as np
import dark_like as L

pr = json.load(open("dr3_prereg.json"))
ZA = pr["z_aniso"]


def vec(f):
    v = [f["DV_rd_0295"]]
    for d in L.DATA[1:]:
        i = ZA.index(d[0])
        v += [f["DM_rd"][i], f["DH_rd"][i]]
    return np.array(v)


def cov(scale):
    n = 1 + 2 * (len(L.DATA) - 1)
    Cm = np.zeros((n, n))
    Cm[0, 0] = L.DATA[0][3] ** 2
    for j, d in enumerate(L.DATA[1:]):
        a, b = 1 + 2 * j, 2 + 2 * j
        Cm[a, a], Cm[b, b] = d[3] ** 2, d[5] ** 2
        Cm[a, b] = Cm[b, a] = d[6] * d[3] * d[5]
    return Cm * scale ** 2


out = {}
for ds in ("dovekie", "desy5"):
    for lab, s in (("DR2_errors", 1.0), ("DR3_sqrt35", math.sqrt(3 / 5))):
        ic = np.linalg.inv(cov(s))
        res = {}
        for a, b in itertools.combinations(("LCDM", "CPL", "free_neg", "free_pos"), 2):
            d = vec(pr["fits"][f"{ds}_{a}"]) - vec(pr["fits"][f"{ds}_{b}"])
            res[f"{a}_vs_{b}"] = float(d @ ic @ d)
        out[f"{ds}_{lab}"] = res
        print(ds, lab, {k: round(v, 2) for k, v in res.items()})
json.dump(out, open("dr3_forecast.json", "w"), indent=1)
