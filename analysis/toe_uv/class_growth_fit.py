"""Weak lensing and RSD inside the fit: the test most able to kill the coupled dark sector, because c' raises S8 from about 0.81 to about 0.83.
Added to plik-lite + tau prior + DESI + SN + ACT/Planck lensing:
  S8 priors, one at a time, since they conflict: DES Y6 3x2pt 0.789 +- 0.012 (arXiv:2601.14559), KiDS-Legacy 0.81 +- 0.0185 (+0.016, -0.021 symmetrised, arXiv:2503.19442).
  f sigma8: z = 0.07 0.450 +- 0.055 (DESI DR1 PV, as cited by the parallel track), z = 0.38 0.497 +- 0.045, z = 0.51 0.459 +- 0.038 (BOSS DR12), z = 0.70 0.473 +- 0.044 (eBOSS LRG), z = 0.85 0.315 +- 0.095 (eBOSS ELG), z = 1.48 0.462 +- 0.045 (eBOSS QSO).  Diagonal: covariances neglected, and BOSS values quoted from memory except eBOSS LRG.
Caveats, all material: S8 from a survey is derived assuming LCDM, and its degeneracy direction need not be S8 exactly for these models, which also have dark matter species that do not trace each other; a summary prior is not a 3x2pt likelihood.  So this is a stress test of size, not a final verdict.
sigma8(z) comes from CLASS P(k, z) for matter, f sigma8 = -(1+z) d sigma8/dz by differences across +- 0.03.
Models: LCDM, exponential on the better sign, fading c < 0, relaxing radion (x_i = x_min, N_f = 2, b = 1/sqrt 2).
usage: python3 class_growth_fit.py dataset set(des|kids|none)"""
import json
import math
import os
import subprocess
import sys
import numpy as np
import act_dr6_lenslike as act
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
MBIN = C.HOME + "/class_massive/class"
ds, which = sys.argv[1], sys.argv[2]
dd = act.load_data("actplanck_baseline", lens_only=False)
ULENS = np.linalg.cholesky(dd["cinv"]).T
FS8 = [(0.07, 0.450, 0.055), (0.38, 0.497, 0.045), (0.51, 0.459, 0.038), (0.70, 0.473, 0.044), (0.85, 0.315, 0.095), (1.48, 0.462, 0.045)]
S8P = dict(des=(0.789, 0.012), kids=(0.81, 0.0185)).get(which)
ZS = sorted({round(z + d, 3) for z, _, _ in FS8 for d in (-0.03, 0.03)})
C.STEP.update(prod=0.004, Zn=0.002)
_run = C.run_class


def sigma8_from(fn, h):
    d = np.loadtxt(fn)
    k, P = d[:, 0], d[:, 1]
    x = k * 8.0
    W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return math.sqrt(np.trapezoid(k ** 3 * P * W ** 2 / (2 * np.pi ** 2), np.log(k)))


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


class GF(C.Fitter):
    def resid(self, p, kind):
        extra = "l_max_scalars=4000\nz_pk=" + ",".join(str(z) for z in ZS) + "\nz_max_pk=2.0"
        binp = C.CLASSBIN
        if "Zn" in p:
            b = p["b"]
            extra += f"\nscf_parameters={4 * b},{b},2.0,{p['Zn']},{p['lnxi']},2,0.0,0.0\nf_idm={1 - p['prod'] / b}"
            binp = MBIN
        kp = {}
        cl, z, H, dc, info = _run(p, kind, extra=extra, binp=binp, keep=kp)
        self.n += 1
        h = p["h"]
        s8 = {}
        for i, zz in enumerate(ZS):
            s8[zz] = sigma8_from(f"{kp['tag']}/o_z{i + 1}_pk.dat", h)
        fs = []
        out_fs = {}
        for zc, val, err in FS8:
            a, b_ = round(zc - 0.03, 3), round(zc + 0.03, 3)
            dsdz = (s8[b_] - s8[a]) / (b_ - a)
            v = -(1 + zc) * dsdz
            out_fs[str(zc)] = v
            fs.append((val - v) / err)
        parts = dict(cmb=self.pl.resid(cl, p["A"]), pri=np.array([(p["A"] - 1) / 0.0025, (p["tau"] - 0.0544) / 0.0073]), bao=C.bao_resid(z, H, dc, info["rd"]), lens=lens_resid(kp["tag"]), fs8=np.array(fs))
        if self.sn is not None:
            parts["sn"] = self.sn.resid(z, dc)
        if S8P is not None:
            parts["S8"] = np.array([(S8P[0] - info["S8"]) / S8P[1]])
        info["fs8"] = out_fs
        subprocess.run(["rm", "-rf", kp["tag"]])
        return np.concatenate(list(parts.values())), {k: float(v @ v) for k, v in parts.items()}, info


F = GF(ds)
base = json.load(open(os.path.join(BG, f"class_lensfit_{ds}.json")))
mas = json.load(open(os.path.join(BG, f"class_massive_{ds}.json")))
path = os.path.join(BG, f"class_growth_{ds}_{which}.json")
out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds, set=which, S8_prior=S8P)


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
        print(name, round(r["chi2"], 3), "vs LCDM", round(r["chi2"] - out["LCDM"]["chi2"], 3) if "LCDM" in out else "", r["parts"], {k: r["info"][k] for k in ("S8", "s8", "om")}, flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)


go("LCDM", dict(base["LCDM"]["p"]), C.NAMES)
go("exp", dict(base["exp"]["p"]), C.NAMES + ["c"])
go("free_neg", dict(base["free_neg"]["p"]), C.NAMES + ["c", "cp"])
go("relax", dict(mas["relax"]["p"]), C.NAMES + ["prod", "Zn"])
print("growthdone", flush=True)
