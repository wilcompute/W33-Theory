"""Can a Euclid-depth BAO survey fix the sign of c?  Asimov Delta chi2 between the frozen fading c<0 and c>0 predictions (dr3_prereg.json, sha 6d76b63b) for D_M/r_d and D_H/r_d at z = 0.934, 1.321, 1.484, 2.33 (the high-z bins where w_eff differs most), uncorrelated fractional errors sigma_f = 0.5, 0.3, 0.2 percent per quantity (assumed Euclid-like and better; my assumption).
Upper bound: models not refitted.  usage: py -3 euclid_sign.py"""
import json
import numpy as np

pr = json.load(open("dr3_prereg.json"))
ZA = pr["z_aniso"]
zs = [0.934, 1.321, 1.484, 2.33]
out = {}
for ds in ("dovekie", "desy5"):
    a, b = pr["fits"][f"{ds}_free_neg"], pr["fits"][f"{ds}_free_pos"]
    for sf in (0.005, 0.003, 0.002):
        chi = 0.0
        for z in zs:
            i = ZA.index(z)
            for k in ("DM_rd", "DH_rd"):
                m = 0.5 * (a[k][i] + b[k][i])
                chi += ((a[k][i] - b[k][i]) / (sf * m)) ** 2
        out[f"{ds}_{sf}"] = chi
        print(ds, "sigma %.1f%%" % (sf * 100), "Delta chi2 %.2f" % chi)
    print(ds, "fractional DM/DH differences:", [round((a["DM_rd"][ZA.index(z)] / b["DM_rd"][ZA.index(z)] - 1) * 100, 3) for z in zs], [round((a["DH_rd"][ZA.index(z)] / b["DH_rd"][ZA.index(z)] - 1) * 100, 3) for z in zs])
json.dump(out, open("euclid_sign.json", "w"), indent=1)
