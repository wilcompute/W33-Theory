"""Shared likelihood: DESI DR2 BAO + the DESI compressed CMB (theta*, omega_b, omega_bc; DESI DR2 Appendix A, covariance as printed in arXiv:2608.01215) + one supernova sample with M marginalised.
Replaces the theta* + omega_m prior I chose in sn_quint.py.  r_d from the DESI fit; r_* from the Eisenstein-Hu analytic form with z* from Hu-Sugiyama, calibrated so that LCDM at the prior mean with h = 0.6737 returns theta* exactly.
A model supplies E(z), its late omega_m, and omega_b and omega_bc at recombination.  Perturbations (ISW, lensing) are not seen, so this tests geometry only."""
import csv
import math
import os
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d

C = 299792.458
DATA = [(0.295, "V", 7.942, 0.075)]
for z, dm, edm, dh, edh, r in [(0.510, 13.588, 0.167, 21.863, 0.425, -0.459), (0.706, 17.351, 0.177, 19.455, 0.330, -0.404), (0.934, 21.576, 0.152, 17.641, 0.193, -0.416), (1.321, 27.601, 0.318, 14.176, 0.221, -0.434), (1.484, 30.512, 0.760, 12.817, 0.516, -0.500), (2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]:
    DATA.append((z, "MH", dm, edm, dh, edh, r))
OMEGA_R_H2 = 4.15e-5
OMEGA_NU_H2 = 0.000642
X_CMB = np.array([0.0104110, 0.02223, 0.14208])
C_CMB = 1e-9 * np.array([[0.006621, 0.12444, -1.1929], [0.12444, 21.344, -94.001], [-1.1929, -94.001, 1488.4]])
IC_CMB = np.linalg.inv(C_CMB)
ZGRID = np.concatenate([np.linspace(0, 3, 1501)[:-1], np.geomspace(3, 1300, 1500)])


def load_sn(ds, ddir):
    if ds == "none":
        return None
    if ds == "pantheon":
        rows = open(os.path.join(ddir, "Pantheon_SH0ES.dat")).read().splitlines()
        h_ = rows[0].split()
        tab = [r.split() for r in rows[1:]]
        ZC = np.array([float(r[h_.index("zHD")]) for r in tab])
        ZH = np.array([float(r[h_.index("zHEL")]) for r in tab])
        MU = np.array([float(r[h_.index("m_b_corr")]) for r in tab])
        vals = np.fromfile(os.path.join(ddir, "Pantheon_SH0ES_STAT_SYS.cov"), sep=" ")
        n = int(vals[0])
        CM = vals[1:].reshape(n, n)
        keep = ZC > 0.01
        ZC, ZH, MU = ZC[keep], ZH[keep], MU[keep]
        IC = np.linalg.inv(CM[keep][:, keep])
    elif ds == "dovekie":
        lines_ = [l for l in open(os.path.join(ddir, "dov_hd.csv")) if not l.startswith("#") and l.strip()]
        keys = lines_[0].split()
        r = [dict(zip(keys, l.split())) for l in lines_[1:]]
        ZC = np.array([float(x["zHD"]) for x in r])
        ZH = np.array([float(x["zHEL"]) for x in r])
        MU = np.array([float(x["MU"]) for x in r])
        d = np.load(os.path.join(ddir, "dov_cov.npz"))
        n = int(d[d.files[0]][0])
        IC = np.zeros((n, n))
        IC[np.triu_indices(n)] = d[d.files[1]]
        il = np.tril_indices(n, -1)
        IC[il] = IC.T[il]
    elif ds == "desy5":
        r = list(csv.DictReader(open(os.path.join(ddir, "desy5_hd.csv"))))
        ZC = np.array([float(x["zHD"]) for x in r])
        ZH = np.array([float(x["zHEL"]) for x in r])
        MU = np.array([float(x["MU"]) for x in r])
        err = np.array([float(x["MUERR_FINAL"]) for x in r])
        vals = np.loadtxt(os.path.join(ddir, "desy5_cov.txt"))
        n = int(vals[0])
        CM = vals[1:].reshape(n, n) + np.diag(err ** 2)
        IC = np.linalg.inv(CM)
    assert IC.shape[0] == len(ZC)
    return dict(ZC=ZC, ZH=ZH, MU=MU, IC=IC, sum=IC.sum(), ones=IC.sum(1), n=len(ZC))


def zstar(wb, wm):
    g1 = 0.0783 * wb ** -0.238 / (1 + 39.5 * wb ** 0.763)
    g2 = 0.560 / (1 + 21.1 * wb ** 1.81)
    return 1048 * (1 + 0.00124 * wb ** -0.738) * (1 + g1 * wm ** g2)


def rs_analytic(wb, wm, zs):
    t = 2.7255 / 2.7
    Req = 31.5 * wb * t ** -4 * (1000 / (2.5e4 * wm * t ** -4))
    Rs = 31.5 * wb * t ** -4 * (1000 / zs)
    keq = 0.0746 * wm * t ** -2
    return 2 / (3 * keq) * math.sqrt(6 / Req) * math.log((math.sqrt(1 + Rs) + math.sqrt(Rs + Req)) / (1 + math.sqrt(Req)))


def _dm_star(E, h, zs):
    chi = cumulative_trapezoid(1 / E, ZGRID, initial=0)
    return np.interp(zs, ZGRID, chi) * C / (100 * h), chi


def _lcdm_E(om, h):
    orr = OMEGA_R_H2 / h ** 2
    return np.sqrt(om * (1 + ZGRID) ** 3 + orr * (1 + ZGRID) ** 4 + 1 - om - orr)


_w0, _wbc = X_CMB[1], X_CMB[2]
_wm = _wbc + OMEGA_NU_H2
_zs = zstar(_w0, _wm)
_dm, _ = _dm_star(_lcdm_E(_wm / 0.6737 ** 2, 0.6737), 0.6737, _zs)
CAL = X_CMB[0] * _dm / rs_analytic(_w0, _wm, _zs)


def chi2(E, h, wb, wbc, sn, ok=0.0, parts=False):
    """E on ZGRID.  wb, wbc are the physical densities at recombination."""
    if np.any(~np.isfinite(E)) or np.any(E <= 0):
        return 1e8
    chi_ = cumulative_trapezoid(1 / E, ZGRID, initial=0)
    S = chi_ if abs(ok) < 1e-8 else (np.sinh(math.sqrt(ok) * chi_) / math.sqrt(ok) if ok > 0 else np.sin(math.sqrt(-ok) * chi_) / math.sqrt(-ok))
    Dc = S * C / (100 * h)
    wm = wbc + OMEGA_NU_H2
    rd = 147.05 * (wb / 0.02236) ** -0.13 * (wbc / 0.1432) ** -0.23
    bao = 0.0
    for d_ in DATA:
        z = d_[0]
        DM = float(np.interp(z, ZGRID, Dc)) / rd
        DH = C / (100 * h * float(np.interp(z, ZGRID, E))) / rd
        if d_[1] == "V":
            bao += (((z * DM ** 2 * DH) ** (1 / 3) - d_[2]) / d_[3]) ** 2
        else:
            a_, b = (DM - d_[2]) / d_[3], (DH - d_[4]) / d_[5]
            r_ = d_[6]
            bao += (a_ * a_ - 2 * r_ * a_ * b + b * b) / (1 - r_ * r_)
    zs = zstar(wb, wm)
    th = CAL * rs_analytic(wb, wm, zs) / float(np.interp(zs, ZGRID, Dc))
    dx = np.array([th, wb, wbc]) - X_CMB
    cmb = float(dx @ IC_CMB @ dx)
    snc = 0.0
    if sn is not None:
        Dmz = np.interp(sn["ZC"], ZGRID, Dc)
        res = sn["MU"] - 5 * np.log10((1 + sn["ZH"]) * Dmz)
        snc = float(res @ sn["IC"] @ res - (sn["ones"] @ res) ** 2 / sn["sum"])
    if parts:
        return dict(bao=bao, cmb=cmb, sn=snc)
    return bao + cmb + snc


def E_lcdm(wbc, h):
    return _lcdm_E((wbc + OMEGA_NU_H2) / h ** 2, h)


def E_cpl(wbc, h, w0, wa):
    om = (wbc + OMEGA_NU_H2) / h ** 2
    orr = OMEGA_R_H2 / h ** 2
    a = 1 / (1 + ZGRID)
    return np.sqrt(om * (1 + ZGRID) ** 3 + orr * (1 + ZGRID) ** 4 + (1 - om - orr) * a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a)))


def E_binned(wbc, h, edges, ws):
    """piecewise constant w on z bins; w = -1 above the last edge."""
    om = (wbc + OMEGA_NU_H2) / h ** 2
    orr = OMEGA_R_H2 / h ** 2
    lnrho = np.zeros_like(ZGRID)
    ln1z = np.log1p(ZGRID)
    edges = np.asarray(edges)
    le = np.log1p(edges)
    acc = 0.0
    for i, w in enumerate(ws):
        m = (ln1z >= le[i]) & (ln1z < le[i + 1])
        lnrho[m] = acc + 3 * (1 + w) * (ln1z[m] - le[i])
        acc += 3 * (1 + w) * (le[i + 1] - le[i])
    lnrho[ln1z >= le[-1]] = acc
    return np.sqrt(om * (1 + ZGRID) ** 3 + orr * (1 + ZGRID) ** 4 + (1 - om - orr) * np.exp(lnrho))
