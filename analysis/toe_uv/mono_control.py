"""Control for class_monodromy_patch.py: the growth likelihood (full Dovekie) at the fading best fit with the original binary (kind fading) and the monodromy binary with Fi = 0 (must agree to numerical precision), then Fi = 0.01, 0.05, 0.1, 0.2 (F = 100 .. 5 M_P) at fixed other parameters.
usage: python3 mono_control.py"""
import json
import os
import sys

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "sn"]
src = open("class_holdout.py", encoding="utf-8").read().split('if HOLD == "evidence":')[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_holdout.py"))
exec(src, g)
F, BMASK, SN = g["F"], g["BMASK"], g["SN"]
F.sn = SN
BMASK["on"] = True
p = dict(json.load(open("class_fit_dovekie.json"))["free_neg"]["p"])
out = {}
for lab, kind, Fi in (("fading", "fading", None), ("mono_Fi0", "mono", 0.0), ("mono_Fi0.01", "mono", 0.01), ("mono_Fi0.05", "mono", 0.05), ("mono_Fi0.1", "mono", 0.1), ("mono_Fi0.2", "mono", 0.2)):
    q = dict(p)
    if Fi is not None:
        q["Fi"] = Fi
    r = F.resid(q, kind)
    out[lab] = dict(chi2=float(r[0] @ r[0]), parts=r[1], phi0=r[2].get("phi0"), S8=r[2].get("S8"))
    print(lab, "chi2 %.4f" % out[lab]["chi2"], {k: round(v, 3) for k, v in r[1].items()}, "phi0", out[lab]["phi0"], flush=True)
json.dump(out, open("mono_control.json", "w"), indent=1, default=float)
