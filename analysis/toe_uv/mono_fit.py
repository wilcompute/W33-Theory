"""Does the data accept the axion-monodromy coupling's intrinsic running (dc'/dphi = Fi^2/2 + 2 c'^2 >= 2 c'^2, nonzero even as F -> infinity)?
Full Dovekie growth likelihood; refit base + c + c' at fixed Fi in {0 (constant-c' fading, control), 0.001 (F = 1000 M_P, minimal running), 0.05, 0.1}, same fitter and start (class_fit_dovekie free_neg), 6 iterations each.
usage: python3 mono_fit.py"""
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
F, C, BMASK, SN = g["F"], g["C"], g["BMASK"], g["SN"]
F.sn = SN
BMASK["on"] = True
p0 = dict(json.load(open("class_fit_dovekie.json"))["free_neg"]["p"])
path = "mono_fit.json"
out = json.load(open(path)) if os.path.exists(path) else {}
for Fi in (0.0, 0.001, 0.05, 0.1):
    key = f"Fi{Fi:g}"
    if key in out:
        continue
    kind = "fading" if Fi == 0 else "mono"
    x0 = dict(p0, Fi=Fi)
    r = F.fit(x0, C.NAMES + ["c", "cp"], kind=kind, iters=6, log=lambda *a, **k: None)
    out[key] = dict(Fi=Fi, chi2=r["chi2"], parts=r["parts"], c=r["p"]["c"], cp=r["p"]["cp"])
    print(key, "chi2 %.2f" % r["chi2"], "c %.3f cp %.4f" % (r["p"]["c"], r["p"]["cp"]), {k: round(v, 2) for k, v in r["parts"].items()}, flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)
