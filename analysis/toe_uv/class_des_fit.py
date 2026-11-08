"""A real cosmic-shear likelihood: DES Y3 xi+/xi- with the published covariance and source n(z), replacing the stand-in survey of class_shear_equiv.py.
Model: Limber with CLASS Halofit P(k, z), the true comoving matter density in the lensing kernel, and nuisances:
  shear calibration m_i, priors (-0.0063, -0.0198, -0.0241, -0.0369) +- (0.0091, 0.0078, 0.0076, 0.0076);
  photo-z shifts dz_i, priors 0 +- (0.018, 0.015, 0.011, 0.017), mean shift only, not the n(z) realisations;
  intrinsic alignments, NLA only (A, eta), wide Gaussian priors 0 +- 3 and 0 +- 4, F(z) = -A 0.0134 Om_com(z) / D(z) ((1+z)/1.62)^eta.
These prior values are from memory of Amon et al / Secco et al 2022 and are not re-read here; the control below tests the result.
Scale cuts are mine, not the DES Lambda-CDM optimised table: xi+ theta > THP arcmin, xi- theta > THM arcmin, defaults 10 and 60, to be insensitive to baryons, which are not modelled.  Mean bin angle, not bin average.
Set "shearonly": LCDM on shear with Gaussian priors h = 0.68 +- 0.03, wb = 0.0224 +- 0.0005, ns = 0.965 +- 0.02; must return DES Y3's S8 near 0.77.  Published: 0.759 to 0.776 by analysis choice.  This is the control.
Set "joint": plik-lite + tau prior + DESI + SN + ACT/Planck lensing + f sigma8 + DES Y3 shear, for LCDM, exp, fading, relaxing radion.
usage: python3 class_des_fit.py dataset set [models]; env THP, THM, MNU"""
import json
import math
import os
import subprocess
import sys
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.special import jv

BG = os.path.dirname(os.path.abspath(__file__))
os.chdir(BG)
ds_, SET = sys.argv[1], sys.argv[2]
models = sys.argv[3].split(",") if len(sys.argv) > 3 else ["LCDM", "exp", "free_neg", "relax"]
THP, THM = float(os.environ.get("THP", 10)), float(os.environ.get("THM", 60))
MNU = float(os.environ.get("MNU", 0.06))
TAG = os.environ.get("TAG", "")
sys.argv = ["x", ds_, "none"]
src = open("class_growth_fit.py", encoding="utf-8").read().split("F = GF(ds)")[0]
g = dict(__name__="x", __file__=os.path.join(BG, "class_growth_fit.py"))
exec(src, g)
C, FS8, MBIN, lens_resid, sigma8_from = (g[k] for k in ("C", "FS8", "MBIN", "lens_resid", "sigma8_from"))

SURVEY = os.environ.get("SURVEY", "des")  # des (default, unchanged) or kids (KiDS-Legacy via kids_convert.py)
D = np.load(os.environ.get("DESNPZ", "/mnt/c/tmp/dl/kids/kids_legacy.npz" if SURVEY == "kids" else "/mnt/c/tmp/dl/des_y3.npz"))
keep = np.r_[D["xip_ang"] > THP, D["xim_ang"] > THM]
ANG = np.r_[D["xip_ang"], D["xim_ang"]] * math.pi / 180 / 60
BI = np.r_[D["xip_i"], D["xim_i"]]
BJ = np.r_[D["xip_j"], D["xim_j"]]
ISM = np.r_[np.zeros(len(D["xip"]), bool), np.ones(len(D["xim"]), bool)]
DATA = np.r_[D["xip"], D["xim"]]
COV = D["cov"][np.ix_(keep, keep)]
UCOV = np.linalg.cholesky(np.linalg.inv(COV)).T
NDATA = int(keep.sum())
ZN, NZ = D["z"], D["nz"]
NB = NZ.shape[0]
ZSH = [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.3, 2.6, 3.0]
ZS = sorted(set(ZSH) | {round(z + d, 3) for z, _, _ in FS8 for d in (-0.03, 0.03)})
ZG = ZN[ZN <= 3.0]
NZG = NZ[:, ZN <= 3.0]
# Hankel kernels: spline basis on ln l, fine l grid
LN = np.linspace(math.log(5), math.log(3e5), 70)
LF = np.linspace(LN[0], LN[-1], 24000)
ELLF = np.exp(LF)
dl = LF[1] - LF[0]
taper = np.where(ELLF > 1e5, np.cos(0.5 * math.pi * (ELLF - 1e5) / 2e5) ** 2, 1.0)
basis = CubicSpline(LN, np.eye(len(LN)), bc_type="natural")(LF)  # fine x nodes
UA, IA_ = np.unique(np.c_[ANG[keep], ISM[keep]], axis=0, return_inverse=True)
HK = np.zeros((len(UA), len(LN)))
for n, (th, im) in enumerate(UA):
    J = jv(4 if im else 0, ELLF * th)
    HK[n] = (ELLF ** 2 * J * taper / (2 * math.pi) * dl) @ basis
ELLN = np.exp(LN)
PAIRS = [(i, j) for i in range(NB) for j in range(i, NB)]
PIDX = {p: n for n, p in enumerate(PAIRS)}
KB = BI[keep]
KJ = BJ[keep]
IM = np.array([PIDX[(int(min(a, b)), int(max(a, b)))] for a, b in zip(KB, KJ)])
if SURVEY == "kids":
    # KiDS-Legacy: shear calibration is inside the covariance, so m_i are pinned (prior sd 1e-5); correlated dz prior from Nz_covariance (kids_convert.py)
    PRIM = (np.zeros(NB), np.full(NB, 1e-5))
    DZM = np.array(D["dz_mean"])
    DZU = np.linalg.cholesky(np.linalg.inv(np.array(D["dz_cov"]))).T
else:
    PRIM = (np.array([-0.0063, -0.0198, -0.0241, -0.0369]), np.array([0.0091, 0.0078, 0.0076, 0.0076]))
    DZM = np.zeros(NB)
    DZU = np.diag(1 / np.array([0.018, 0.015, 0.011, 0.017]))
PRIZ = 1 / np.diag(DZU)
NUIS = [f"m{i}" for i in range(NB)] + [f"dz{i}" for i in range(NB)] + ["Aia", "eta"]
C.STEP.update({f"m{i}": (1e-5 if SURVEY == "kids" else 0.004) for i in range(NB)})
C.STEP.update({f"dz{i}": 0.005 for i in range(NB)})
C.STEP.update(Aia=0.1, eta=0.3)
C.STEP.update(prod=0.004, Zn=0.002)


class Tab:
    """everything the shear projection needs from one CLASS run"""

    def __init__(self, kp, p, z, H, dc):
        h = p["h"]
        t = kp["tag"]
        self.lnk, self.lnP = [], []
        self.zsh = np.array(ZSH)
        s8 = []
        for zz in ZSH:
            i = ZS.index(zz) + 1
            d = np.loadtxt(f"{t}/o_z{i}_pk_nl.dat")
            self.lnk.append(np.log(d[:, 0] * h))
            self.lnP.append(np.log(d[:, 1] / h ** 3))
            s8.append(sigma8_from(f"{t}/o_z{i}_pk.dat", h))
        s8 = np.array(s8)
        bc = kp["cols"]
        raw = kp["raw"][::-1]
        zb = raw[:, bc.index("z")]
        rho = raw[:, bc.index("(.)rho_cdm")] + raw[:, bc.index("(.)rho_b")] + (raw[:, bc.index("(.)rho_idm")] if "(.)rho_idm" in bc else 0.0)
        H0 = raw[0, bc.index("H [1/Mpc]")]
        self.H0 = H0
        self.om = np.interp(ZG, zb, rho / H0 ** 2 / (1 + zb) ** 3)
        self.chi = np.interp(ZG, z, dc)
        self.H = np.interp(ZG, z, H)
        self.D = np.interp(ZG, self.zsh, s8 / s8[0])
        lz = np.log1p(self.zsh)
        kk = (ELLN[None, :] + 0.5) / self.chi[:, None]
        Pm = np.zeros(kk.shape)
        for j, zz in enumerate(ZG):
            a = int(np.clip(np.searchsorted(self.zsh, zz) - 1, 0, len(ZSH) - 2))
            tt = (math.log1p(zz) - lz[a]) / (lz[a + 1] - lz[a])
            lk = np.log(kk[j])
            y = []
            for b in (a, a + 1):
                v = np.interp(lk, self.lnk[b], self.lnP[b])
                s = (self.lnP[b][-1] - self.lnP[b][-8]) / (self.lnk[b][-1] - self.lnk[b][-8])
                v = np.where(lk > self.lnk[b][-1], self.lnP[b][-1] + s * (lk - self.lnk[b][-1]), v)
                s0 = (self.lnP[b][7] - self.lnP[b][0]) / (self.lnk[b][7] - self.lnk[b][0])
                v = np.where(lk < self.lnk[b][0], self.lnP[b][0] + s0 * (lk - self.lnk[b][0]), v)
                y.append(v)
            Pm[j] = np.exp(y[0] + tt * (y[1] - y[0]))
        self.P = Pm


def xi_model(T, p):
    W = []
    dzg = np.gradient(ZG)
    F = -p["Aia"] * 0.0134 * T.om / T.D * ((1 + ZG) / 1.62) ** p["eta"]
    for i in range(NB):
        n = np.interp(ZG - p[f"dz{i}"], ZG, NZG[i], left=0.0, right=0.0)
        n = n / np.sum(n * dzg)
        cum = np.cumsum((n * dzg)[::-1])[::-1]
        cumc = np.cumsum((n * dzg / np.maximum(T.chi, 1e-6))[::-1])[::-1]
        q = cum - T.chi * cumc
        W.append(1.5 * T.H0 ** 2 * T.om * (1 + ZG) * T.chi * q + F * T.H * n)
    W = np.array(W)
    res = np.zeros(len(PAIRS) * len(UA))
    fac = dzg / T.H / T.chi ** 2
    pm = [(1 + p[f"m{i}"]) for i in range(NB)]
    cl = np.zeros((len(PAIRS), len(LN)))
    for n, (i, j) in enumerate(PAIRS):
        cl[n] = np.sum((W[i] * W[j] * fac)[:, None] * T.P, axis=0) * pm[i] * pm[j]
    xiU = cl @ HK.T  # pairs x unique angles
    return xiU[IM, IA_]


class SF(C.Fitter):
    def __init__(self, ds):
        super().__init__(ds)
        self.cache = {}

    def cosmo(self, p, kind):
        key = tuple(sorted((k, round(float(v), 12)) for k, v in p.items() if k not in NUIS and isinstance(v, (int, float))))
        if key in self.cache:
            return self.cache[key]
        extra = "l_max_scalars=4000\nz_pk=" + ",".join(str(z) for z in ZS) + "\nz_max_pk=3.1\nP_k_max_1/Mpc=30"
        binp = C.CLASSBIN
        if "Zn" in p:
            b = p["b"]
            extra += f"\nscf_parameters={4 * b},{b},2.0,{p['Zn']},{p['lnxi']},2,0.0,0.0\nf_idm={1 - p['prod'] / b}"
            binp = MBIN
        kp = {}
        cl, z, H, dc, info = C.run_class(p, kind, extra=extra, binp=binp, keep=kp)
        self.n += 1
        h = p["h"]
        parts = {}
        if SET == "joint":
            s8 = {zz: sigma8_from(f"{kp['tag']}/o_z{i + 1}_pk.dat", h) for i, zz in enumerate(ZS)}
            fs = []
            out_fs = {}
            for zc, val, err in FS8:
                a, b_ = round(zc - 0.03, 3), round(zc + 0.03, 3)
                v = -(1 + zc) * (s8[b_] - s8[a]) / (b_ - a)
                out_fs[str(zc)] = v
                fs.append((val - v) / err)
            parts = dict(cmb=self.pl.resid(cl, p["A"]), pri=np.array([(p["A"] - 1) / 0.0025, (p["tau"] - 0.0544) / 0.0073]), bao=C.bao_resid(z, H, dc, info["rd"]), lens=lens_resid(kp["tag"]), fs8=np.array(fs))
            if self.sn is not None:
                parts["sn"] = self.sn.resid(z, dc)
            info["fs8"] = out_fs
        else:
            parts = dict(pri=np.array([(h - 0.68) / 0.03, (p["wb"] - 0.0224) / 0.0005, (p["ns"] - 0.965) / 0.02]))
        T = Tab(kp, p, z, H, dc)
        subprocess.run(["rm", "-rf", kp["tag"]])
        if len(self.cache) > 40:
            self.cache.clear()
        self.cache[key] = (parts, T, info)
        return self.cache[key]

    def resid(self, p, kind):
        parts, T, info = self.cosmo(p, kind)
        parts = dict(parts)
        parts["des"] = UCOV @ (xi_model(T, p) - DATA[keep])
        parts["desp"] = np.r_[[(p[f"m{i}"] - PRIM[0][i]) / PRIM[1][i] for i in range(NB)], DZU @ (np.array([p[f"dz{i}"] for i in range(NB)]) - DZM), [p["Aia"] / 3.0, p["eta"] / 4.0]]
        return np.concatenate(list(parts.values())), {k: float(v @ v) for k, v in parts.items()}, info


F = SF(ds_)
base = json.load(open(f"class_growth_{ds_}_none.json"))
start_nuis = {f"m{i}": float(PRIM[0][i]) for i in range(NB)}
start_nuis.update({f"dz{i}": float(DZM[i]) for i in range(NB)}, Aia=0.3, eta=0.0)
suffix = f"_{TAG}" if TAG else ""
path = f"class_des_{ds_}_{SET}{suffix}.json"
out = json.load(open(path)) if os.path.exists(path) else dict(dataset=ds_, set=SET, ndata=NDATA, cuts=[THP, THM], mnu=MNU, rows={})
print("ndata", NDATA, flush=True)
for m in models:
    if m in out["rows"]:
        continue
    fr = dict(LCDM=[], exp=["c"], free_neg=["c", "cp"], relax=["prod", "Zn"])[m]
    if SET == "shearonly":
        free = ["lnA", "wc", "h", "wb", "ns"] + NUIS
    else:
        free = C.NAMES + fr + NUIS
    x0 = dict(base[m]["p"], mnu=MNU, **start_nuis)
    r = F.fit(x0, free, iters=int(os.environ.get("ITERS", 8)))
    out["rows"][m] = r
    print(m, round(r["chi2"], 3), {k: round(v, 2) for k, v in r["parts"].items()}, "S8", round(r["info"]["S8"], 4), {k: round(r["p"][k], 4) for k in NUIS + ["c", "cp", "prod"] if k in r["p"]}, flush=True)
    json.dump(out, open(path, "w"), indent=1, default=float)
print("desdone", flush=True)
