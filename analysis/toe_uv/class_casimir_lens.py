"""ACT DR6 + Planck PR4 lensing, post hoc, at the Lambda + Casimir + sparse tower best fits of class_casimir_fits.py.  No refit, as in class_lens.py.
usage: python3 class_casimir_lens.py dataset [dataset...]"""
import json
import os
import subprocess
import sys
import numpy as np
import act_dr6_lenslike as act
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
CBIN = C.HOME + "/class_casimir/class"
dd = act.load_data("actplanck_baseline", lens_only=False)


def lens(p):
    b, f = p["b"], p["prod"] / p["b"]
    extra = f"l_max_scalars=4000\nscf_parameters={4 * b},{b},2.0,{p['Z']},0.0,0.0\nf_idm={1 - f}"
    kp = {}
    C.run_class(p, "fading", extra=extra, binp=CBIN, keep=kp)
    fn = kp["tag"] + "/o_cl_lensed.dat"
    d = np.loadtxt(fn)
    cols = C.titles(fn)
    subprocess.run(["rm", "-rf", kp["tag"]])
    ell = d[:, 0]
    fac = C.TCMB ** 2 * 2 * np.pi / (ell * (ell + 1))
    tt, ee, te, bb = (d[:, cols.index(k)] * fac for k in ("TT", "EE", "TE", "BB"))
    pp = d[:, cols.index("phiphi")] * 2 * np.pi / (ell * (ell + 1))
    kk = (ell * (ell + 1)) ** 2 * pp / 4
    lo = int(ell[0])
    mk = lambda a: np.r_[np.zeros(lo), a]
    ls = np.arange(int(ell[-1]) + 1)
    return float(-2 * act.generic_lnlike(dd, ls, mk(kk), ls, mk(tt), mk(ee), mk(te), mk(bb)))


for ds in sys.argv[1:]:
    path = os.path.join(BG, f"class_casimir_{ds}.json")
    o = json.load(open(path))
    for k, r in o.items():
        if isinstance(r, dict) and "p" in r and "lens" not in r:
            r["lens"] = lens(r["p"])
            print(ds, k, r["delta"], r["eps"], r["info"]["S8"], r["lens"], flush=True)
    json.dump(o, open(path, "w"), indent=1, default=float)
print("lensdone", flush=True)
