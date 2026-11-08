"""Profile likelihood in the fading coupling's potential slope c (replaces sign_grid.py, whose fixed-background grid was under-resolved: chi2 rose by tens per grid step in c' because nothing compensated the shift in today's DM density).
Full Dovekie data (plik-lite + tau + DESI + SN + lensing + f sigma8, the modes_laplace likelihood).  At each fixed c, all other parameters (7 base + c') are refitted by Fitter.fit, warm-started from the nearer mode's best fit.
P(c>0) is estimated as  int_{c>0} exp(-chi2_prof/2) dc / int exp(-chi2_prof/2) dc  (flat prior on c in [-3, 3]); this ignores the change of the conditional width in the other parameters along c (a profile, not a marginal), stated as a limitation.
Resumable: c_profile.json.  usage: python3 c_profile.py"""
import json
import os
import sys
import numpy as np

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "sn"]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py"))
exec(src, g)
F, C, BMASK, SN = g["F"], g["C"], g["BMASK"], g["SN"]
F.sn = SN
BMASK["on"] = True
fits = json.load(open("class_fit_dovekie.json"))
CS = [-2.0, -1.4, -0.9, -0.5, -0.2, 0.2, 0.5, 0.7, 1.0, 1.4, 2.0]
path = "c_profile.json"
out = json.load(open(path)) if os.path.exists(path) else {}
for c in CS:
    key = f"{c:+.2f}"
    if key in out:
        continue
    start = dict(fits["free_neg" if c < 0 else "free_pos"]["p"], c=c)
    r = F.fit(start, C.NAMES + ["cp"], kind="fading", iters=6, log=lambda *a, **k: None)
    out[key] = dict(c=c, chi2=r["chi2"], cp=r["p"]["cp"], parts=r["parts"], p=r["p"])
    print("c %+.2f  chi2 %.2f  c' %.4f" % (c, r["chi2"], r["p"]["cp"]), flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)
rows = sorted(out.values(), key=lambda r: r["c"])
cc = np.array([r["c"] for r in rows])
ch = np.array([r["chi2"] for r in rows])
grid = np.linspace(-3, 3, 601)
prof = np.interp(grid, cc, ch, left=ch[0], right=ch[-1])
w = np.exp(-(prof - prof.min()) / 2)
pp = float(w[grid > 0].sum() / w.sum())
res = dict(rows=rows, P_c_positive_profile=pp, chi2_min=float(ch.min()), c_at_min=float(cc[np.argmin(ch)]), chi2_at_small_c=dict(zip([f"{c:+.1f}" for c in cc], [float(x) for x in ch])))
json.dump(dict(out, summary=res), open(path, "w"), indent=1, default=float)
print("P(c>0) from profile = %.3f; min chi2 %.2f at c = %+.2f" % (pp, ch.min(), cc[np.argmin(ch)]), flush=True)
