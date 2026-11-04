"""Lensing inside the fit, not post hoc.  ACT DR6 + Planck PR4 lensing bandpowers join plik-lite + tau prior + DESI + SN in the residual vector; all parameters refit.  This settles whether the post hoc gain of Pass 12558 survives, given aae4f41f5's follow-up f3593b2ae, which found A_s and n_s absorb 99.98 percent of the squared lensing response in an idealised test.
Models: LCDM, exponential (better sign), fading c < 0, Lambda + negative Casimir + sparse tower, b = 1/sqrt 2, sparse tower with free c.  Starts from the fits without lensing.
Each model run uses l_max_scalars = 4000 for the lensing corrections, so about twice the cost.  Local optima.
usage: python3 class_lensfit.py dataset"""
import json
import math
import os
import sys
import numpy as np
import act_dr6_lenslike as act
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
CBIN = C.HOME + "/class_casimir/class"
ds = sys.argv[1]
dd = act.load_data("actplanck_baseline", lens_only=False)
ULENS = np.linalg.cholesky(dd["cinv"]).T
C.STEP.update(prod=0.004, Z=0.06)
_run = C.run_class


def lens_resid(tag):
    fn = tag + "/o_cl_lensed.dat"
    d = np.loadtxt(fn)
    cols = C.titles(fn)
    ell = d[:, 0]
    fac = C.TCMB ** 2 * 2 * np.pi / (ell * (ell + 1))
    tt, ee, te, bb = (d[:, cols.index(k)] * fac for k in ("TT", "EE", "TE", "BB"))
    kk = (ell * (ell + 1)) ** 2 * (d[:, cols.index("phiphi")] * 2 * np.pi / (ell * (ell + 1))) / 4
    lo = int(ell[0])
    mk = lambda a: np.r_[np.zeros(lo), a]
    ls = np.arange(int(ell[-1]) + 1)
    _, th = act.generic_lnlike(dd, ls, mk(kk), ls, mk(tt), mk(ee), mk(te), mk(bb), return_theory=True)
    return ULENS @ (dd["data_binned_clkk"] - th)


class LF(C.Fitter):
    def resid(self, p, kind):
        extra = "l_max_scalars=4000"
        binp = C.CLASSBIN
        if "Z" in p:
            b = p["b"]
            f = p["prod"] / b
            extra += f"\nscf_parameters={4 * b},{b},2.0,{p['Z']},0.0,0.0"
            binp = CBIN
            if f < 1:
                extra += f"\nf_idm={1 - f}"
        elif "prod" in p:
            b = p["b"]
            f = p["prod"] / b
            extra += f"\nscf_parameters={p['c']},{b},2.0,0.0,0.0\nf_idm={1 - f}"
        kp = {}
        cl, z, H, dc, info = _run(p, kind, extra=extra, binp=binp, keep=kp)
        self.n += 1
        parts = dict(cmb=self.pl.resid(cl, p["A"]), pri=np.array([(p["A"] - 1) / 0.0025, (p["tau"] - 0.0544) / 0.0073]), bao=C.bao_resid(z, H, dc, info["rd"]))
        if self.sn is not None:
            parts["sn"] = self.sn.resid(z, dc)
        parts["lens"] = lens_resid(kp["tag"])
        import subprocess

        subprocess.run(["rm", "-rf", kp["tag"]])
        return np.concatenate(list(parts.values())), {k: float(v @ v) for k, v in parts.items()}, info


F = LF(ds)
base = json.load(open(os.path.join(BG, f"class_fit_{ds}.json")))
cas = json.load(open(os.path.join(BG, f"class_casimir_{ds}.json")))
frac = json.load(open(os.path.join(BG, f"class_fraction_{ds}.json")))
path = os.path.join(BG, f"class_lensfit_{ds}.json")
out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds)


def go(name, x0, free):
    if name in out:
        return
    print(name, flush=True)
    try:
        r = F.fit(x0, free, iters=8)
    except Exception as e:
        r = dict(failed=str(e)[-300:])
    out[name] = r
    if "chi2" in r:
        print(name, round(r["chi2"], 3), "vs LCDM", round(r["chi2"] - out["LCDM"]["chi2"], 3) if "LCDM" in out else "", {k: round(v, 4) for k, v in r["p"].items()}, r["parts"], r["info"], flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)


go("LCDM", dict(base["LCDM"]["p"]), C.NAMES)
ex = base["exp_neg"] if base["exp_neg"]["chi2"] < base["exp_pos"]["chi2"] else base["exp_pos"]
go("exp", dict(ex["p"]), C.NAMES + ["c"])
go("free_neg", dict(base["free_neg"]["p"]), C.NAMES + ["c", "cp"])
c0 = cas["b707_neg"]["p"]
go("casimir_neg", dict(c0), C.NAMES + ["prod", "Z"])
fr = frac["b707_product005"]
go("sparse_b707_free_c", dict(fr["p"], b=0.7071, prod=0.05), C.NAMES + ["c", "prod"])
print("lensfitdone", flush=True)
