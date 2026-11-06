"""Sign of the fading coupling against real DES Y3 cosmic shear (class_des_fit.py likelihood: published covariance, n(z), m, dz, NLA IA).
Cosmology fixed at the full-data Dovekie best fits (LCDM, fading c<0, fading c>0, CPL; class_fit_dovekie.json); only the ten DES nuisances are fitted, so each model costs one CLASS run.
This asks which sign the shear prefers at fixed background, not a joint refit; chi2 differences are lower bounds on what a refit could not recover.
usage: nice -n 10 python3 sign_des.py"""
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
SF, NUIS, PRIM = g["SF"], g["NUIS"], g["PRIM"]
F = SF("dovekie")
fits = json.load(open("class_fit_dovekie.json"))
start = {f"m{i}": float(PRIM[0][i]) for i in range(4)}
start.update({f"dz{i}": 0.0 for i in range(4)}, Aia=0.3, eta=0.0)
out = {}
for m in ("LCDM", "free_neg", "free_pos", "CPL"):
    x0 = dict(fits[m]["p"], mnu=0.06, **start)
    r = F.fit(x0, NUIS, kind="cpl" if m == "CPL" else "fading", iters=6)
    out[m] = dict(des=r["parts"]["des"], desp=r["parts"]["desp"], S8=r["info"]["S8"], c=fits[m]["p"].get("c"), cp=fits[m]["p"].get("cp"), nuis={k: r["p"][k] for k in NUIS})
    print(m, "des chi2 %.2f  nuisance prior %.2f  S8 %.4f" % (r["parts"]["des"], r["parts"]["desp"], r["info"]["S8"]), flush=True)
    json.dump(out, open("sign_des.json", "w"), indent=1, default=float)
