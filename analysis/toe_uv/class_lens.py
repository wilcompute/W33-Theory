"""CMB lensing at the Planck + DESI + SN best fits of class_fits.py: ACT DR6 + Planck PR4 lensing bandpowers (act_dr6_lenslike, variant actplanck_baseline).  plik-lite does not include the lensing reconstruction, and lensing is what the fifth force on CDM changes most directly.
Post hoc: no refit, so a lensing penalty is an upper limit on what a joint fit would show, and a lensing gain a lower limit.  Control: the LCDM chi2 at the Planck best fit should be near the number of bandpowers.
usage: python3 class_lens.py dataset [dataset...]"""
import json
import os
import re
import subprocess
import sys
import numpy as np
import act_dr6_lenslike as act
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
dd = act.load_data("actplanck_baseline", lens_only=False)


def lens_chi2(p, kind):
    kp = {}
    C.run_class(p, kind, extra="l_max_scalars=4000", keep=kp)
    f = kp["tag"] + "/o_cl_lensed.dat"
    d = np.loadtxt(f)
    cols = C.titles(f)
    subprocess.run(["rm", "-rf", kp["tag"]])
    ell = d[:, 0]
    fac = C.TCMB ** 2 * 2 * np.pi / (ell * (ell + 1))
    tt, ee, te, bb = (d[:, cols.index(k)] * fac for k in ("TT", "EE", "TE", "BB"))
    pp = d[:, cols.index("phiphi")] * 2 * np.pi / (ell * (ell + 1))  # CLASS column is l(l+1) C_l^pp / 2 pi
    kk = (ell * (ell + 1)) ** 2 * pp / 4
    ell_ = ell.astype(int)
    # the likelihood expects arrays starting at l = 0
    mk = lambda a: np.r_[np.zeros(ell_[0]), a]
    ls = np.arange(ell_[-1] + 1)
    return float(-2 * act.generic_lnlike(dd, ls, mk(kk), ls, mk(tt), mk(ee), mk(te), mk(bb)))


for ds in sys.argv[1:]:
    fits = json.load(open(os.path.join(BG, f"class_fit_{ds}.json")))
    path = os.path.join(BG, f"class_lens_{ds}.json")
    out = json.load(open(path)) if os.path.exists(path) else {}
    for k, r in fits.items():
        if k == "dataset" or "p" not in r or k in out:
            continue
        kind = "lcdm" if k == "LCDM_native" else ("cpl" if k == "CPL" else "fading")
        try:
            out[k] = dict(chi2_lens=lens_chi2(r["p"], kind), S8=r["info"]["S8"], s8=r["info"]["s8"])
        except Exception as e:
            out[k] = dict(failed=str(e)[-200:])
        print(ds, k, out[k], flush=True)
        json.dump(out, open(path, "w"), indent=1)
print("lensdone", flush=True)
