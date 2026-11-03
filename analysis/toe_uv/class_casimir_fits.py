"""Lambda + Casimir + sparse tower on full Planck plik-lite + DESI + SNe, two cold fluids, with class_casimir_patch.py.  Free: LCDM parameters, prod = f b, and Z, where V = H0^2 (A + Z exp(-4 b phi)), A shot.  Starts from casimir_fits_*.json.
Controls: Z = 0 and f = 1 at c' -> small returns Lambda; H(z) against the independent solver dm_drag.solve at the same parameters.  Lensing post hoc through class_lens.
usage: python3 class_casimir_fits.py dataset [dataset...]"""
import json
import math
import os
import sys
import numpy as np
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
CBIN = C.HOME + "/class_casimir/class"
_run = C.run_class
C.STEP.update(prod=0.004, Z=0.06)


def run(p, kind="fading", extra="", binp=None, keep=None):
    b = p["b"]
    f = p["prod"] / b
    add = f"scf_parameters={4 * b},{b},2.0,{p['Z']},0.0,0.0"
    if f < 1:
        add += f"\nf_idm={1 - f}"
    return _run(p, kind, extra=(extra + "\n" + add).strip(), binp=CBIN, keep=keep)


C.run_class = run
for ds in sys.argv[1:]:
    F = C.Fitter(ds)
    base = json.load(open(os.path.join(BG, f"class_fit_{ds}.json")))
    comp = json.load(open(os.path.join(BG, f"casimir_fits_{ds}.json")))["best"]
    path = os.path.join(BG, f"class_casimir_{ds}.json")
    out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds, LCDM=base["LCDM"]["chi2"], free_neg=base["free_neg"]["chi2"], free_pos=base["free_pos"]["chi2"], casimir_line=base["casimir"]["chi2"])
    st = base["free_neg"]["p"]
    for name, b, s in (("b707_neg", 0.7071, "-1"), ("b707_pos", 0.7071, "1"), ("b1000_neg", 1.0, "-1")):
        if name in out or f"{b}_{s}" not in comp:
            continue
        c0 = comp[f"{b}_{s}"]
        Z0 = 3 * c0["Z"]  # CLASS has V = H0^2 (A + Z exp), and rho = V/3; casimir_fast has Z in units of the critical density
        print(ds, name, "start prod", c0["prod"], "Z", Z0, flush=True)
        try:
            r = F.fit(dict(st, b=b, prod=c0["prod"], Z=Z0), C.NAMES + ["prod", "Z"], iters=10)
            r["delta"] = r["chi2"] - base["LCDM"]["chi2"]
            r["eps"] = r["p"]["Z"] * math.exp(-4 * b * r["info"]["phi0"]) / 3
        except Exception as e:
            r = dict(failed=str(e)[-300:])
        out[name] = r
        print(name, r.get("delta"), r.get("eps"), r.get("p"), r.get("parts"), r.get("info"), r.get("failed"), flush=True)
        json.dump(out, open(path, "w"), indent=1, default=float)
print("casimirdone", flush=True)
