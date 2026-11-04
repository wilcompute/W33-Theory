"""Is there a natural origin for fermions at M ~ 1/R?  Scherk-Schwarz: 5D N = 1 supergravity on an interval with a twist omega gives gravitini masses |n + omega|/R, and arXiv:2301.07719 discusses this for the dark dimension.
Spectrum assumed, on an interval: bosons: 4 massless (graviton 2, radion 1, axion from the graviphoton 1), and 8 dof at n/R for n >= 1 (massive graviton 5, massive graviphoton 3); fermions: 4 dof at |n + omega|/R for all integers n.  At omega = 0 bosons and fermions match level by level: a control, since the 4D Casimir energy must vanish there.
4D Casimir energy on the dark circle: V = -(1/2) (3/(4 pi^2 l^4)) 8 sum_w (1 - cos(2 pi w omega))/w^5, l = 2 pi R: always negative, exactly R^-4, so no minimum, n = 4 and recollapse as in Pass 12562.  This is the sign the fit prefers, from one discrete or continuous twist, with no new bulk fields.
No-AdS3 on a further circle L: v(L) = Lambda_4 + Sum, as in dd_massive_fermions.py; SM photon 2 dof massless, Dirac neutrinos on the brane.  The two extra massless bosons (radion, axion) sit at the limit of Pass 12539; the radion's Hubble mass and any axion mass are ignored, which is conservative.
For eps = -0.33 of critical, R follows from omega.  Scan omega, report the AdS3 status at m1 = 0 and the m1 bound, for comparison with massive fermions.
usage: py -3 dd_ss_gravitino.py"""
import json
import math
import numpy as np
from scipy.optimize import brentq
from scipy.special import kn, zeta

D21, D31 = 7.49e-5, 2.513e-3
LAM4 = (2.24e-3) ** 4
HC = 0.1973269804
RHO_CRIT = 2.6e-11 / 0.69
Ls = np.logspace(-1.5, 5.5, 350)


def rho_arr(m, L):
    if m < 1e-12:
        return math.pi ** 2 / (90 * L ** 4)
    tot = np.zeros_like(L)
    for k in range(1, 12):
        arg = k * m * L
        if np.all(arg > 300):
            break
        tot += kn(2, np.minimum(arg, 690)) / k ** 2
    return m ** 2 / (2 * math.pi ** 2 * L ** 2) * tot


def spectrum(m1):
    return [m1, math.sqrt(m1 ** 2 + D21), math.sqrt(m1 ** 2 + D31)]


def Neff(om):
    return 8 * sum((1 - math.cos(2 * math.pi * w * om)) / w ** 5 for w in range(1, 400)) / float(zeta(5))


def v_of_L(m1, R, om, nmax=None):
    v = LAM4 - (2 + 4) * rho_arr(0.0, Ls)  # photon 2, graviton 2, radion 1, axion 1
    for m in spectrum(m1):
        v = v + 4 * rho_arr(m, Ls)
    mk = 1 / R
    nmax = min(int(30 * R / Ls[0]) + 2, 6000)
    ns = np.unique(np.r_[np.arange(1, 400), np.geomspace(400, nmax, 300).astype(int)]) if nmax > 400 else np.arange(1, nmax + 1)
    wts = np.gradient(ns.astype(float))
    wts[ns < 400] = 1.0
    for n, wt in zip(ns, wts):
        v = v - wt * 8 * rho_arr(n * mk, Ls)
        v = v + wt * 4 * (rho_arr((n + om) * mk, Ls) + rho_arr((n - om) * mk, Ls))
    v = v + 4 * rho_arr(abs(om) * mk, Ls)
    return v


out = dict(rows=[])
out["control_Neff_small_omega"] = Neff(1e-4)
assert Neff(1e-6) < 1e-6
# control: omega = 0 cancels level by level, so the tower adds nothing except the 4 fermions at n = 0 acting massless
for om in (0.5, 0.45, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.02):
    N = Neff(om)
    # interval: half of circle: V = 0.5 * N * 3 zeta(5)/(4 pi^2 (2 pi R)^4)
    R = (0.5 * N * 3 * float(zeta(5)) / (4 * math.pi ** 2 * (2 * math.pi) ** 4) / (0.33 * RHO_CRIT)) ** 0.25
    v = v_of_L(0.0, R, om)
    row = dict(omega=om, Neff=N, R_micron=R * HC, gravitino_eV=om / R, min_v=float(v.min()), L_of_min_micron=float(Ls[int(np.argmin(v))] * HC), ads3_at_m1_0=bool(v.min() < 0))
    if not row["ads3_at_m1_0"]:
        f = lambda m: float(v_of_L(m, R, om).min())
        hi = 1e-4
        while f(hi) > 0 and hi < 0.2:
            hi *= 1.5
        row["m1_bound_eV"] = brentq(f, hi / 1.5, hi, xtol=1e-5) if hi < 0.2 else None
    out["rows"].append(row)
    print({k: (round(x, 5) if isinstance(x, float) else x) for k, x in row.items()}, flush=True)
    json.dump(out, open("dd_ss_gravitino.json", "w"), indent=1, default=float)
print("done", flush=True)
