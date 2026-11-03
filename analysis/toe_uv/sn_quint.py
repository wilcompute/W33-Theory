"""quintessence_desi.py with real supernovae and with curvature.  Datasets: Pantheon+ (z > 0.01, full STAT+SYS covariance) or DES-Dovekie (the recalibrated DES-SN5YR; inverse covariance as supplied).  M is marginalised analytically.  Controls: DESI+CMB+SNe w0wa against published values: Pantheon+ -0.838, -0.62; DES-Dovekie -0.803, -0.72.
Models: LCDM, LCDM + Omega_k, flat CPL, exponential quintessence flat and with free Omega_k (thawing).  The data files are not in the repo: they are read from the path given, and their URLs are in the report.  usage: py -3 sn_quint.py pantheon|dovekie data_dir"""
import json
import math
import os
import sys
import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.interpolate import interp1d
from scipy.optimize import brentq, minimize

src = open("quintessence_desi.py", encoding="utf-8").read().split("def E_lcdm")[0]
exec(src)
ds, ddir = sys.argv[1], sys.argv[2]
if ds == "pantheon":
    rows = open(os.path.join(ddir, "Pantheon_SH0ES.dat")).read().splitlines()
    h_ = rows[0].split()
    i_z, i_h, i_m, i_cal = h_.index("zHD"), h_.index("zHEL"), h_.index("m_b_corr"), h_.index("IS_CALIBRATOR")
    tab = [r.split() for r in rows[1:]]
    ZC = np.array([float(r[i_z]) for r in tab])
    ZH = np.array([float(r[i_h]) for r in tab])
    MU = np.array([float(r[i_m]) for r in tab])
    Cal = np.array([int(r[i_cal]) for r in tab])
    vals = np.fromfile(os.path.join(ddir, "Pantheon_SH0ES_STAT_SYS.cov"), sep=" ")
    n = int(vals[0])
    CM = vals[1:].reshape(n, n)
    keep = ZC > 0.01
    ZC, ZH, MU = ZC[keep], ZH[keep], MU[keep]
    IC = np.linalg.inv(CM[keep][:, keep])
elif ds == "dovekie":
    import csv
    lines_ = [l for l in open(os.path.join(ddir, "dov_hd.csv")) if not l.startswith("#") and l.strip()]
    delim = "," if "," in lines_[0] else None
    if delim:
        r = list(csv.DictReader(lines_))
    else:
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
    assert n == len(ZC), (n, len(ZC))
print(ds, len(ZC), flush=True)
ICsum = IC.sum()
ones_IC = IC.sum(1)
ZGRID = np.concatenate([np.linspace(0, 3, 1501)[:-1], np.geomspace(3, 1200, 1500)])


def sn_chi2(Dm_fn, h):
    dl = (1 + ZH) * Dm_fn(ZC)
    res = MU - 5 * np.log10(dl)
    return float(res @ IC @ res - (ones_IC @ res) ** 2 / ICsum)


def total(Efunc, om, h, ok=0.0):
    E = Efunc(ZGRID)
    if np.any(~np.isfinite(E)) or np.any(E <= 0):
        return 1e8
    chi_ = cumulative_trapezoid(1 / E, ZGRID, initial=0)
    if abs(ok) < 1e-8:
        S = chi_
    elif ok > 0:
        S = np.sinh(math.sqrt(ok) * chi_) / math.sqrt(ok)
    else:
        S = np.sin(math.sqrt(-ok) * chi_) / math.sqrt(-ok)
    Dc = S * C / (100 * h)
    Dm = interp1d(ZGRID, Dc)
    Ei = interp1d(ZGRID, E)
    om2 = om * h ** 2
    rd = 147.05 * (om2 / 0.1432) ** -0.23
    chi = 0.0
    for d_ in DATA:
        z = d_[0]
        DM = float(Dm(z)) / rd
        DH = C / (100 * h * float(Ei(z))) / rd
        if d_[1] == "V":
            chi += (((z * DM ** 2 * DH) ** (1 / 3) - d_[2]) / d_[3]) ** 2
        else:
            a_, b = (DM - d_[2]) / d_[3], (DH - d_[4]) / d_[5]
            r_ = d_[6]
            chi += (a_ * a_ - 2 * r_ * a_ * b + b * b) / (1 - r_ * r_)
    th = (rd / 1.0187) / float(Dm(ZSTAR))
    chi += ((100 * th - 1.04110) / 0.00053) ** 2 + ((om2 - 0.1430) / 0.0011) ** 2
    return chi + sn_chi2(Dm, h)


def Elcdm(om, h, ok=0.0):
    orr = OMEGA_R_H2 / h ** 2
    return lambda z: np.sqrt(om * (1 + z) ** 3 + orr * (1 + z) ** 4 + ok * (1 + z) ** 2 + 1 - om - orr - ok)


def Ecpl(om, h, w0, wa):
    orr = OMEGA_R_H2 / h ** 2
    def f(z):
        a = 1 / (1 + z)
        return np.sqrt(om * (1 + z) ** 3 + orr * (1 + z) ** 4 + (1 - om - orr) * a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a)))
    return f


def Equint(lam, om, h, ok=0.0):
    orr = OMEGA_R_H2 / h ** 2
    Ni = math.log(1 / 3000.0)
    den = om * math.exp(-3 * Ni) + orr * math.exp(-4 * Ni) + ok * math.exp(-2 * Ni)
    r0 = orr * math.exp(-4 * Ni) / den
    k0 = ok * math.exp(-2 * Ni) / den

    def integrate(y0sq):
        def rhs(N, s):
            x, y, r_, k = s
            m = max(1 - x * x - y * y - r_ - k, 0)
            q = 3 * x * x + 1.5 * m + 2 * r_ + k
            return [-3 * x + math.sqrt(1.5) * lam * y * y + q * x, -math.sqrt(1.5) * lam * x * y + q * y, r_ * (2 * q - 4), k * (2 * q - 2)]
        return solve_ivp(rhs, (Ni, 0), [1e-6 * math.sqrt(y0sq), math.sqrt(y0sq), r0, k0], rtol=1e-8, atol=1e-12, dense_output=True, method="LSODA")

    target = 1 - om - orr - ok
    f = lambda ly: (lambda s: s.y[0, -1] ** 2 + s.y[1, -1] ** 2)(integrate(10 ** ly)) - target
    ly = brentq(f, -14, -5, xtol=1e-6)
    s = integrate(10 ** ly)
    Ns = np.linspace(Ni, 0, 1500)
    x, y, r_, k = s.sol(Ns)
    m = np.maximum(1 - x * x - y * y - r_ - k, 1e-300)
    a = np.exp(Ns)
    E = np.sqrt(om * a ** -3 / m)
    z = 1 / a - 1
    w = (x * x - y * y) / (x * x + y * y)
    fE = interp1d(z[::-1], E[::-1], bounds_error=False, fill_value="extrapolate")
    return fE, float(w[-1]), float(w[np.argmin(abs(a - 0.5))])


def fit(fn, x0):
    return minimize(fn, x0, method="Nelder-Mead", options=dict(xatol=2e-4, fatol=2e-3, maxiter=900))


out = dict(dataset=ds, n=len(ZC))
lc = fit(lambda p: total(Elcdm(p[0], p[1]), p[0], p[1]), [0.31, 0.68])
out["LCDM"] = dict(chi2=lc.fun, om=lc.x[0], h=lc.x[1])
lk = fit(lambda p: total(Elcdm(p[0], p[1], p[2]), p[0], p[1], p[2]), [0.31, 0.68, 0.0])
out["LCDM_k"] = dict(chi2=lk.fun, om=lk.x[0], h=lk.x[1], ok=lk.x[2], delta=lk.fun - lc.fun)
cp = fit(lambda p: total(Ecpl(p[0], p[1], p[2], p[3]), p[0], p[1]) if p[2] + p[3] < 0 else 1e8, [0.31, 0.68, -0.85, -0.5])
out["CPL"] = dict(chi2=cp.fun, om=cp.x[0], h=cp.x[1], w0=cp.x[2], wa=cp.x[3], delta=cp.fun - lc.fun)
print(out, flush=True)
scan = []
for lam in (0.3, 0.6, 0.816, 1.0, 1.2, 1.414):
    def flat(p):
        try:
            return total(Equint(lam, p[0], p[1])[0], p[0], p[1])
        except Exception:
            return 1e8
    def curved(p):
        try:
            return total(Equint(lam, p[0], p[1], p[2])[0], p[0], p[1], p[2])
        except Exception:
            return 1e8
    a = fit(flat, [0.31, 0.67])
    b = fit(curved, [a.x[0], a.x[1], 0.005])
    fE, w0, w5 = Equint(lam, a.x[0], a.x[1])
    rec = dict(lam=lam, flat_delta=a.fun - lc.fun, flat_om=a.x[0], flat_h=a.x[1], w0=w0, w_at_half=w5, curved_delta=b.fun - lc.fun, curved_ok=b.x[2], curved_om=b.x[0], curved_h=b.x[1])
    scan.append(rec)
    print({k: round(v, 4) for k, v in rec.items()}, flush=True)
out["quintessence"] = scan
json.dump(out, open(f"sn_quint_{ds}.json", "w"), indent=1, default=float)
