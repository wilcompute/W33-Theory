"""Cluster gas fractions: a direct clock on the dark matter mass.  Baryons do not fade and dark matter does, so the cosmic baryon fraction rises toward today in these models, with no reference to growth or to the CMB.  A cluster measurement also carries the distance factor f_gas proportional to D_A^(3/2), relative to the reference cosmology used to analyse it.
Apparent signal, relative to the same model's value at z = 0.1:
    A(z) = [f_b(z) / f_b(0.1)] x [D_ref(z)/D(z)]^(3/2) / [D_ref(0.1)/D(0.1)]^(3/2)
with the LCDM best fit as reference, so LCDM returns exactly 1, the control.  f_b is rho_b / (rho_b + all clustering dark matter).  For the relaxing radion only the fraction prod/b of dark matter fades, and CLASS holds the two fluids separately.  Assumes clusters trace the cosmic ratio with an unchanged depletion factor, and ignores the extra concentration of the coupled species, measured at 1.2 to 1.4 in peaks by nbody_pm.py, which works in the same direction only in the cores.
usage: python3 class_fgas.py dataset"""
import json
import os
import sys
import numpy as np
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
ds = sys.argv[1]
MBIN = C.HOME + "/class_massive/class"
gf = json.load(open(os.path.join(BG, f"class_growth_{ds}_none.json")))
ZG = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 1.1])


def table(p, extra="", binp=C.CLASSBIN):
    kp = {}
    cl, z, H, dc, info = C.run_class(p, "fading", extra=extra, binp=binp, keep=kp)
    raw = kp["raw"][::-1]
    bc = kp["cols"]
    zb = raw[:, bc.index("z")]
    rb = raw[:, bc.index("(.)rho_b")]
    rc = raw[:, bc.index("(.)rho_cdm")] + (raw[:, bc.index("(.)rho_idm")] if "(.)rho_idm" in bc else 0.0)
    f = rb / (rb + rc)
    os.system(f"rm -rf {kp['tag']}")
    da = np.interp(ZG, z, dc) / (1 + ZG)
    return np.interp(ZG, zb, f), da


fL, dL = table(gf["LCDM"]["p"])
out = dict(dataset=ds, z=ZG.tolist(), fb_LCDM=fL.tolist(), rows={})
ctrl = (fL / fL[0]) * ((dL / dL) / (dL[0] / dL[0])) ** 1.5
out["control_LCDM_A"] = ctrl.tolist()
print("control", ctrl, flush=True)
pr = gf["relax"]["p"]
b = pr["b"]
models = [("exp", gf["exp"]["p"], "", C.CLASSBIN), ("free_neg", gf["free_neg"]["p"], "", C.CLASSBIN), ("relax", dict(pr, c=0.0, cp=b), f"scf_parameters={4 * b},{b},2.0,{pr['Zn']},{pr['lnxi']},2,0.0,0.0\nf_idm={1 - pr['prod'] / b}", MBIN)]
for n, p, ex, bp in models:
    f, d = table(p, ex, bp)
    A_fb = f / f[0]
    A_d = ((dL / d) / (dL[0] / d[0])) ** 1.5
    out["rows"][n] = dict(fb=f.tolist(), A_fb=A_fb.tolist(), A_dist=A_d.tolist(), A=(A_fb * A_d).tolist())
    print(n, "fb", np.round(A_fb, 4), "dist", np.round(A_d, 4), "A", np.round(A_fb * A_d, 4), flush=True)
    json.dump(out, open(os.path.join(BG, f"class_fgas_{ds}.json"), "w"), indent=1, default=float)
print("fgasdone", flush=True)
