"""Weight of the two signs of the fading coupling by direct 2D integration (replaces the invalid Laplace weights of Pass 12625 and emcee's untrustworthy mode weights).
Full Dovekie data (plik-lite + tau + DESI + SN + lensing + f sigma8), base cosmology held at each mode's best fit (class_fit_dovekie free_neg / free_pos), grid over the sign's half-plane:
   c in [-3, 0) or (0, 3], c' in [0, 0.2], flat priors (the prior volumes are equal, so they cancel in the ratio).
Z_sign = sum exp(-(chi2 - chi2_ref)/2) dA.  The base parameters are not marginalised: the ratio ignores differences in base-parameter volume between the modes (Laplace base log-det difference is small, Pass 12625: 103.92 vs 104.00 including c, c').
Grid NxN per sign (default 15); refines nothing; reports P(c>0), the grid maxima and the posterior mass near c' = 0 (where the sign is undefined).
usage: python3 sign_grid.py [N]"""
import json
import math
import os
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
sys.path.insert(0, BG)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 15
sys.argv = ["x", "dovekie", "sn"]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py"))
exec(src, g)
F, BMASK, SN = g["F"], g["BMASK"], g["SN"]
fits = json.load(open("class_fit_dovekie.json"))
path = "sign_grid.json"
out = json.load(open(path)) if os.path.exists(path) else {}
cps = np.linspace(0.0, 0.2, N + 1)[1:] - 0.1 / N
for sign, key in (("neg", "free_neg"), ("pos", "free_pos")):
    cs = (np.linspace(0, 3, N + 1)[1:] - 1.5 / N) * (-1 if sign == "neg" else 1)
    base = dict(fits[key]["p"])
    grid = out.get(sign, {}).get("chi2")
    grid = np.array(grid) if grid is not None else np.full((N, N), np.nan)
    for i, c in enumerate(cs):
        for j, cp in enumerate(cps):
            if np.isfinite(grid[i, j]):
                continue
            q = dict(base, c=float(c), cp=float(cp))
            try:
                F.sn = SN
                BMASK["on"] = True
                r = F.resid(q, "fading")[0]
                grid[i, j] = float(r @ r)
            except Exception as e:
                grid[i, j] = np.inf
                print("fail", c, cp, str(e)[-60:], flush=True)
            out[sign] = dict(c=cs.tolist(), cp=cps.tolist(), chi2=[[float(v) for v in row] for row in grid])
            json.dump(out, open(path, "w"), indent=1)
        print(sign, "row", i, "min chi2 so far %.2f" % np.nanmin(grid), flush=True)
ref = min(np.nanmin(np.array(out[s]["chi2"])) for s in ("neg", "pos"))
Z = {}
for s in ("neg", "pos"):
    ch = np.array(out[s]["chi2"])
    w = np.exp(-(ch - ref) / 2)
    w[~np.isfinite(w)] = 0
    Z[s] = float(w.sum())
    k = np.unravel_index(np.nanargmin(ch), ch.shape)
    out[s]["best"] = dict(c=out[s]["c"][k[0]], cp=out[s]["cp"][k[1]], chi2=float(ch[k]))
    out[s]["mass_cp_below_0p02"] = float(w[:, np.array(out[s]["cp"]) < 0.02].sum() / max(w.sum(), 1e-300))
out["P_c_positive"] = Z["pos"] / (Z["pos"] + Z["neg"])
out["note"] = "base parameters fixed at each mode's best fit; not marginalised"
json.dump(out, open(path, "w"), indent=1)
print("P(c>0) = %.3f" % out["P_c_positive"], {s: out[s]["best"] for s in ("neg", "pos")}, flush=True)
