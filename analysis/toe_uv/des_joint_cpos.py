"""Joint refit of fading c>0 including real DES Y3 shear (class_des_fit.py 'joint' set: plik-lite + tau + DESI + Dovekie SN + lensing + f sigma8 + DES Y3), for comparison with the existing joint LCDM (2466.92) and fading c<0 (2456.22) rows of class_des_dovekie_joint.json.
Does adding shear flip the preferred sign of c?  Compare with the existing joint free_neg row (2456.22).  Start: class_fit_dovekie free_pos best fit + DES nuisance starts.
usage: python3 des_joint_cpl.py"""
import json
import os
import sys

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "joint", "LCDM"]
src = open("class_des_fit.py", encoding="utf-8").read().split("F = SF(ds_)")[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_des_fit.py"))
exec(src, g)
SF, NUIS, PRIM, C = g["SF"], g["NUIS"], g["PRIM"], g["C"]
C.STEP.update(w0=0.02, wa=0.08)
F = SF("dovekie")
p = dict(json.load(open("class_fit_dovekie.json"))["free_pos"]["p"])
x0 = dict(p, mnu=0.06, **{f"m{i}": float(PRIM[0][i]) for i in range(4)}, **{f"dz{i}": 0.0 for i in range(4)}, Aia=0.3, eta=0.0)
r = F.fit(x0, C.NAMES + ["c", "cp"] + NUIS, kind="fading", iters=8)
json.dump(r, open("des_joint_cpos.json", "w"), indent=1, default=float)
print("fading c>0 joint", round(r["chi2"], 2), {k: round(v, 2) for k, v in r["parts"].items()}, "S8", round(r["info"]["S8"], 4), "c %.3f cp %.4f" % (r["p"]["c"], r["p"]["cp"]), flush=True)
