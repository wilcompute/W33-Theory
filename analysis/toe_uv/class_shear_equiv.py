"""What S8 would a LCDM shear analysis infer for these models?  An S8 prior assumes LCDM, and these models have a different growth history and a fading matter density, so the true S8 need not be what the survey reports.  Build DES-like tomographic shear C_l by Limber, for each model, and fit the LCDM family (sigma8, Omega_m) to them with a Gaussian mock covariance.  The S8 of that fit is the LCDM-equivalent S8 to compare with the survey.
n(z): four Gaussians at z = 0.33, 0.52, 0.75, 0.95, sigma 0.15: a stand-in for DES Y6, not its n(z).  5000 deg^2, 8 per arcmin^2 per 4 bins total shape noise sigma_e = 0.26.  l from 30 to 2000.  No intrinsic alignments, no baryons, no photo-z or shear nuisances.  Halofit P_nl from CLASS, times the N-body P ratio for coupled models, from nbody_L25_b707.json at z = 0 and scaled with growth is not attempted: applied at all z as an upper bound on the effect.
W(chi) uses the true comoving matter density at each z, since the coupled species fades.  The scalar force does not bend light.
Control: a LCDM model with known S8 must return it within 0.002.
usage: python3 class_shear_equiv.py dataset"""
import json
import math
import os
import subprocess
import sys
import numpy as np
from scipy.integrate import cumulative_trapezoid
import class_cmb as C

BG = os.path.dirname(os.path.abspath(__file__))
ds = sys.argv[1]
ZS = [0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.3, 2.6, 3.0]
ELL = np.geomspace(30, 2000, 18)
MEANS = (0.33, 0.52, 0.75, 0.95)
SIG = 0.15
MBIN = os.environ.get("MASSBIN", C.HOME + "/class_massive/class")
FSKY = 5000 / 41253.0
NEFF = 8.0 / 4 * (180 * 60 / math.pi) ** 2
SIGE = 0.26
nb = json.load(open(os.path.join(BG, "nbody_L25_b707.json")))
NBK = np.array(nb["k_common"])
NBR = np.array(nb["P_ratio"])


def shear(p, kind="fading", extra="", binp=C.CLASSBIN, boost=False):
    kp = {}
    ex = "z_pk=" + ",".join(map(str, ZS)) + "\nz_max_pk=3.1\nP_k_max_1/Mpc=30\n" + extra
    cl, z, H, dc, info = C.run_class(p, kind, extra=ex.strip(), binp=binp, keep=kp)
    h = p["h"]
    t = kp["tag"]
    Pz = []
    for i in range(len(ZS)):
        d = np.loadtxt(f"{t}/o_z{i + 1}_pk_nl.dat")
        Pz.append((d[:, 0] * h, d[:, 1] / h ** 3))
    bc = kp["cols"]
    raw = kp["raw"][::-1]
    zb = raw[:, bc.index("z")]
    rho = raw[:, bc.index("(.)rho_cdm")] + raw[:, bc.index("(.)rho_b")] + (raw[:, bc.index("(.)rho_idm")] if "(.)rho_idm" in bc else 0.0)
    H0 = raw[0, bc.index("H [1/Mpc]")]
    om_com = rho / H0 ** 2 / (1 + zb) ** 3  # comoving matter density in units of the critical density today
    subprocess.run(["rm", "-rf", t])
    zg = np.linspace(0.005, 3.0, 300)
    chi = np.interp(zg, z, dc)
    Hg = np.interp(zg, z, H)
    omg = np.interp(zg, zb, om_com)
    nz = [np.exp(-0.5 * ((zg - m) / SIG) ** 2) for m in MEANS]
    nz = [n / np.trapezoid(n, zg) for n in nz]
    W = []
    for n in nz:
        q = np.array([np.trapezoid((n * (chi - c) / chi)[j:], zg[j:]) for j, c in enumerate(chi)])
        W.append(1.5 * H0 ** 2 * omg * (1 + zg) * chi * q)
    lnZ = np.log1p(np.array(ZS))
    res = []
    for l in ELL:
        kk = (l + 0.5) / chi
        P = np.zeros_like(zg)
        for j, zz in enumerate(zg):
            i = int(np.clip(np.searchsorted(ZS, zz) - 1, 0, len(ZS) - 2))
            tt = (math.log1p(zz) - lnZ[i]) / (lnZ[i + 1] - lnZ[i])
            k1, p1 = Pz[i]
            k2, p2 = Pz[i + 1]
            a = np.interp(np.log(kk[j]), np.log(k1), np.log(p1), left=-50, right=-50)
            b = np.interp(np.log(kk[j]), np.log(k2), np.log(p2), left=-50, right=-50)
            P[j] = math.exp(a + tt * (b - a))
            if boost:
                P[j] *= float(np.interp(np.log(kk[j] / h), np.log(NBK), NBR))
        row = []
        for i in range(4):
            for m in range(i, 4):
                row.append(np.trapezoid(W[i] * W[m] / chi ** 2 * P / Hg, zg))
        res.append(row)
    return np.array(res), info


def cov_weights(C0):
    """diagonal Gaussian weights per l bin and pair"""
    dl = np.gradient(ELL)
    idx = [(i, m) for i in range(4) for m in range(i, 4)]
    w = np.zeros_like(C0)
    for b in range(len(ELL)):
        A = {}
        for n, (i, m) in enumerate(idx):
            A[(i, m)] = A[(m, i)] = C0[b, n] + (SIGE ** 2 / NEFF if i == m else 0.0)
        for n, (i, m) in enumerate(idx):
            var = (A[(i, i)] * A[(m, m)] + A[(i, m)] ** 2) / ((2 * ELL[b] + 1) * dl[b] * FSKY)
            w[b, n] = 1 / var
    return w


fit = json.load(open(os.path.join(BG, f"class_fit_{ds}.json")))
mas = json.load(open(os.path.join(BG, f"class_massive_{ds}.json")))
p0 = dict(fit["LCDM"]["p"])
C0, i0 = shear(p0)
wt = cov_weights(C0)
th = [("lnA", 0.04), ("wc", 0.004)]
J, dS = [], []
for n, st in th:
    C1, i1 = shear(dict(p0, **{n: p0[n] + st}))
    J.append(((C1 - C0) / st).ravel())
    dS.append((i1["S8"] - i0["S8"]) / st)
J = np.array(J).T
W = wt.ravel()
JW = J.T @ (W[:, None] * J)


def equiv(Cm):
    d = (Cm - C0).ravel()
    x = np.linalg.solve(JW, J.T @ (W * d))
    res = d - J @ x
    return i0["S8"] + dS[0] * x[0] + dS[1] * x[1], float(res @ (W * res)), float(d @ (W * d)), x.tolist()


out = dict(dataset=ds, LCDM_S8=i0["S8"], rows={})
Ct, it = shear(dict(p0, lnA=p0["lnA"] - 0.03, wc=p0["wc"] + 0.0015))
se, r, d, x = equiv(Ct)
out["control_LCDM"] = dict(S8_true=it["S8"], S8_equiv=se, resid_chi2=r)
print("control", out["control_LCDM"], flush=True)
models = [("free_neg", fit["free_neg"]["p"], "fading", "", C.CLASSBIN), ("free_pos", fit["free_pos"]["p"], "fading", "", C.CLASSBIN), ("exp_neg", fit["exp_neg"]["p"], "fading", "", C.CLASSBIN)]
pr = mas["relax"]["p"]
b = pr["b"]
models.append(("relax", dict(pr, c=0.0, cp=b), "fading", f"scf_parameters={4 * b},{b},2.0,{pr['Zn']},{pr['lnxi']},2,0.0,0.0\nf_idm={1 - pr['prod'] / b}", MBIN))
for name, p, kind, ex, binp in models:
    for boost in (False, True):
        if boost and name not in ("relax",):
            continue
        Cm, im = shear(p, kind, ex, binp, boost)
        se, r, d, x = equiv(Cm)
        key = name + ("_nbody" if boost else "")
        out["rows"][key] = dict(S8_true=im["S8"], S8_equiv=se, resid_chi2=r, total_chi2_from_LCDM=d, om=im["om"], s8=im["s8"])
        print(key, out["rows"][key], flush=True)
        json.dump(out, open(os.path.join(BG, f"class_shear_{ds}{os.environ.get('OUTTAG', '')}.json"), "w"), indent=1, default=float)
print("sheardone", flush=True)
