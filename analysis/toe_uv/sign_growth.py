"""Growth predictions for the two signs of the fading coupling (free_neg c<0 vs free_pos c>0, same c' ~0.053), full-data fits on Dovekie and DES-SN5YR.
BAO cannot see the sign (dr3_forecast: Delta chi2 0.13-0.27 even at DR3 depth), so does growth?  Reports f sigma8 at the six data redshifts, S8, sigma8, and the chi2 of the current f sigma8 + lensing data at each fit.
usage: nice -n 19 python3 sign_growth.py"""
import json
import os
import sys

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
sys.path.insert(0, BG)
sys.argv = ["x", "dovekie", "none"]
src = open("class_growth_fit.py", encoding="utf-8").read().split("F = GF(ds)")[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_growth_fit.py"))
exec(src, g)
GF = g["GF"]
F = GF("none")
out = {}
for ds in ("dovekie", "desy5"):
    fits = json.load(open(f"class_fit_{ds}.json"))
    for m in ("LCDM", "free_neg", "free_pos", "CPL"):
        p = dict(fits[m]["p"])
        r, parts, info = F.resid(p, "cpl" if m == "CPL" else "fading")
        out[f"{ds}_{m}"] = dict(c=p.get("c"), cp=p.get("cp"), fs8=info["fs8"], S8=info["S8"], s8=info["s8"], chi2_fs8=parts["fs8"], chi2_lens=parts["lens"], chi2_cmb=parts["cmb"])
        print(ds, m, "S8 %.4f" % info["S8"], {k: round(v, 4) for k, v in info["fs8"].items()}, "chi2 fs8 %.2f lens %.2f" % (parts["fs8"], parts["lens"]), flush=True)
        json.dump(out, open("sign_growth.json", "w"), indent=1)
