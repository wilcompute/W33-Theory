"""The swampland against the DESI DR2 distances.  Exponential quintessence V = V0 exp(-lam phi / M_Pl), flat universe, matter + radiation, thawing from rest.  chi2 from the 13 DESI DR2 BAO numbers (arXiv:2503.14738 Table 4) plus a compressed CMB: 100 theta* = 1.04110 +- 0.00053 and omega_m = 0.1430 +- 0.0011 (a Planck-like prior; the DESI paper's own covariance was not available to me).  r_d = 147.05 (omega_m / 0.1432)^-0.23 Mpc at fixed omega_b, N_eff; r_* = r_d / 1.0187.
Free: omega_m, h, and lam.  Control: the w0wa fit must come near the published DESI+CMB -0.42, -1.75 and improve on LCDM by about Delta chi2 = 12 (3.1 sigma).  Then Delta chi2(lam), against swampland values: sqrt(2/3) = 0.816 (Bedroya-Vafa TCC) and sqrt(2) = 1.414 (strong dS).  No supernovae here, so this is a BAO + CMB statement.  usage: py -3 quintessence_desi.py"""
import json
import math
import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.interpolate import interp1d
from scipy.optimize import brentq, minimize

C = 299792.458
DATA = [(0.295, "V", 7.942, 0.075)]
for z, dm, edm, dh, edh, r in [(0.510, 13.588, 0.167, 21.863, 0.425, -0.459), (0.706, 17.351, 0.177, 19.455, 0.330, -0.404), (0.934, 21.576, 0.152, 17.641, 0.193, -0.416), (1.321, 27.601, 0.318, 14.176, 0.221, -0.434), (1.484, 30.512, 0.760, 12.817, 0.516, -0.500), (2.330, 38.988, 0.531, 8.632, 0.101, -0.431)]:
    DATA.append((z, "MH", dm, edm, dh, edh, r))
ZSTAR = 1089.9
OMEGA_R_H2 = 4.15e-5


def E_lcdm(z, om, h):
    orr = OMEGA_R_H2 / h ** 2
    return np.sqrt(om * (1 + z) ** 3 + orr * (1 + z) ** 4 + 1 - om - orr)


def E_cpl(z, om, h, w0, wa):
    orr = OMEGA_R_H2 / h ** 2
    a = 1 / (1 + z)
    return np.sqrt(om * (1 + z) ** 3 + orr * (1 + z) ** 4 + (1 - om - orr) * a ** (-3 * (1 + w0 + wa)) * np.exp(-3 * wa * (1 - a)))


def E_quint(lam, om, h):
    """returns E(z) on a grid; shoot the initial potential so that Omega_de today = 1 - om - orr"""
    orr = OMEGA_R_H2 / h ** 2
    Ni = math.log(1 / 3000.0)

    def integrate(y0sq):
        def rhs(N, s):
            x, y, r_ = s
            m = max(1 - x * x - y * y - r_, 0)
            q = 3 * x * x + 1.5 * m + 2 * r_          # -dlnH/dN
            return [-3 * x + math.sqrt(1.5) * lam * y * y + q * x, -math.sqrt(1.5) * lam * x * y + q * y, r_ * (2 * q - 4)]
        rr0 = orr * math.exp(-4 * Ni) / (om * math.exp(-3 * Ni) + orr * math.exp(-4 * Ni))
        return solve_ivp(rhs, (Ni, 0), [1e-6 * math.sqrt(y0sq), math.sqrt(y0sq), rr0], rtol=1e-8, atol=1e-12, dense_output=True, method="LSODA")

    target = 1 - om - orr
    f = lambda ly: (lambda s: s.y[0, -1] ** 2 + s.y[1, -1] ** 2)(integrate(10 ** ly)) - target
    ly = brentq(f, -14, -5, xtol=1e-6)
    s = integrate(10 ** ly)
    Ns = np.linspace(Ni, 0, 1500)
    x, y, r_ = s.sol(Ns)
    m = np.maximum(1 - x * x - y * y - r_, 1e-300)
    # H^2 from matter: H^2 / H0^2 = om a^-3 / Omega_m(a)
    a = np.exp(Ns)
    E2 = om * a ** -3 / m
    w = (x * x - y * y) / (x * x + y * y)
    return a, np.sqrt(E2), w


def chi2_from_E(Efunc, h, om):
    zgrid = np.concatenate([np.linspace(0, 3, 601)[:-1], np.geomspace(3, 1200, 1500)])
    E = Efunc(zgrid)
    Dc = cumulative_trapezoid(1 / E, zgrid, initial=0) * C / (100 * h)
    Dm = interp1d(zgrid, Dc)
    Ei = interp1d(zgrid, E)
    om2 = om * h ** 2
    rd = 147.05 * (om2 / 0.1432) ** -0.23
    chi = 0.0
    for d in DATA:
        z = d[0]
        DM = float(Dm(z)) / rd
        DH = C / (100 * h * float(Ei(z))) / rd
        if d[1] == "V":
            V = (z * DM ** 2 * DH) ** (1 / 3)
            chi += ((V - d[2]) / d[3]) ** 2
        else:
            a_, b = (DM - d[2]) / d[3], (DH - d[4]) / d[5]
            r = d[6]
            chi += (a_ * a_ - 2 * r * a_ * b + b * b) / (1 - r * r)
    th = (rd / 1.0187) / float(Dm(ZSTAR))
    chi += ((100 * th - 1.04110) / 0.00053) ** 2 + ((om2 - 0.1430) / 0.0011) ** 2
    return chi


def fit(model, x0):
    best = minimize(model, x0, method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-3, maxiter=1500))
    return best


out = {}
lc = fit(lambda p: chi2_from_E(lambda z: E_lcdm(z, p[0], p[1]), p[1], p[0]), [0.30, 0.68])
out["LCDM"] = dict(chi2=lc.fun, om=lc.x[0], h=lc.x[1])
cp = fit(lambda p: chi2_from_E(lambda z: E_cpl(z, p[0], p[1], p[2], p[3]), p[1], p[0]) if p[2] + p[3] < 0 else 1e6, [0.34, 0.65, -0.5, -1.5])
out["CPL"] = dict(chi2=cp.fun, om=cp.x[0], h=cp.x[1], w0=cp.x[2], wa=cp.x[3], delta_chi2=cp.fun - lc.fun, published_w0=-0.42, published_wa=-1.75)
print(out, flush=True)
scan = []
for lam in (0.2, 0.4, 0.6, 0.7, 0.816, 1.0, 1.2, 1.414, 1.7):
    def mod(p):
        om, h = p
        try:
            a, E, w = E_quint(lam, om, h)
        except Exception:
            return 1e6
        z = 1 / a - 1
        fE = interp1d(z[::-1], E[::-1], bounds_error=False, fill_value="extrapolate")
        return chi2_from_E(lambda zz: fE(zz), h, om)
    b = fit(mod, [0.31, 0.67])
    a, E, w = E_quint(lam, b.x[0], b.x[1])
    wf = interp1d(np.log(a), w)
    w0 = float(w[-1])
    wa = float((w[np.argmin(abs(a - 0.5))] - w0) / 0.5)
    scan.append(dict(lam=lam, chi2=b.fun, delta_chi2_vs_LCDM=b.fun - lc.fun, om=b.x[0], h=b.x[1], w0=w0, wa_approx=wa))
    print(scan[-1], flush=True)
out["quintessence"] = scan
json.dump(out, open("quintessence_desi.json", "w"), indent=1, default=float)
