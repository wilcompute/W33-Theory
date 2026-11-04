"""Full Planck plik-lite + DESI + SNe for Lambda + Casimir of gravitons and massive bulk fermions + sparse tower, two fluids, with class_massive_patch.py.  Grid in x_0 = M R today around where the 4D minimum changes sign; Zn and prod free, as in casimir_massive.py, from whose fits it starts.
Control: H(z) against casimir_massive.solve at the same parameters is printed.  usage: python3 class_massive_fits.py dataset"""
import json
import math
import os
import sys
import numpy as np
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
MBIN = C.HOME + "/class_massive/class"
_run = C.run_class
C.STEP.update(prod=0.004, Zn=0.002)
ds = sys.argv[1]
NF = 2


def run(p, kind="fading", extra="", binp=None, keep=None):
    b = p["b"]
    f = p["prod"] / b
    add = f"scf_parameters={4 * b},{b},2.0,{p['Zn']},{p['lnxi']},{NF},0.0,0.0\nf_idm={1 - f}"
    return _run(p, kind, extra=(extra + "\n" + add).strip(), binp=MBIN, keep=keep)


C.run_class = run
F = C.Fitter(ds)
base = json.load(open(os.path.join(BG, f"class_fit_{ds}.json")))
comp = json.load(open(os.path.join(BG, f"casimir_massive_fine_{ds}.json")))
path = os.path.join(BG, f"class_massive_{ds}.json")
out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds, LCDM=base["LCDM"]["chi2"], free_neg=base["free_neg"]["chi2"])
st = base["free_neg"]["p"]
b = 0.7071
for k in ("0.5", "0.6", "1.0"):
    if k in out or k not in comp["rows"] or "Zn" not in comp["rows"][k]:
        continue
    c0 = comp["rows"][k]
    lnxi = math.log(float(k)) - b * c0["chi0"]
    print(ds, "x0", k, flush=True)
    try:
        C.STEP["Zn"] = 0.1 * c0["Zn"]
        r = F.fit(dict(st, b=b, prod=c0["prod"], Zn=c0["Zn"], lnxi=lnxi), C.NAMES + ["prod", "Zn"], iters=8)
        r["delta"] = r["chi2"] - base["LCDM"]["chi2"]
        r["x0"] = math.exp(lnxi + b * r["info"]["phi0"])
    except Exception as e:
        r = dict(failed=str(e)[-300:])
    out[k] = r
    print(k, r.get("delta"), r.get("x0"), r.get("p"), r.get("info"), r.get("failed"), flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)
# the radion starts at the minimum: x_i = x_min, casimir_relax.py
rel = json.load(open(os.path.join(BG, f"casimir_relax_{ds}.json")))
if "relax" not in out and "0.7071" in rel["rows"]:
    c0 = rel["rows"]["0.7071"]
    lnxi = math.log(rel["xmin"])
    print(ds, "relax", flush=True)
    try:
        C.STEP["Zn"] = 0.1 * c0["Zn"]
        r = F.fit(dict(st, b=b, prod=c0["prod"], Zn=c0["Zn"], lnxi=lnxi), C.NAMES + ["prod", "Zn"], iters=8)
        r["delta"] = r["chi2"] - base["LCDM"]["chi2"]
        r["x0"] = math.exp(lnxi + b * r["info"]["phi0"])
    except Exception as e:
        r = dict(failed=str(e)[-300:])
    out["relax"] = r
    print("relax", r.get("delta"), r.get("x0"), r.get("p"), r.get("parts"), r.get("info"), r.get("failed"), flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)
print("massivedone", flush=True)
