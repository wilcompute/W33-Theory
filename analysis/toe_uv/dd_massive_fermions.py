"""Can massive bulk fermions keep the negative Casimir energy today and also remove the AdS3 of Pass 12539?
Dark circle: a 5D field of mass M on a circle of length l gives, per real dof,
    V(l, M) = -(1/2) int ds/s (4 pi s)^(-5/2) l sum_{w != 0} exp(-w^2 l^2/(4 s) - s M^2)
            = -2 l (4 pi)^(-5/2) (2 M/l)^(5/2) sum_{w>=1} w^(-5/2) K_{5/2}(w l M)
which must tend to -3 zeta(5)/(4 pi^2 l^4) at M = 0: a control.  Fermions take the opposite sign, and are exponentially suppressed once M l >> 1.  l = 2 pi R.
Budget today: V_C = (-N_g C(0) + N_f 4 C(M l)) / (2 for an interval), N_g = 5 graviton dof; solve R so that V_C = eps rho_crit with eps from the fit.
No-AdS3: as in swampland_ext.py, 4D on a further circle L: v(L) = Lambda_4 + sum (fermion +, boson -) rho(m, L), Lambda_4 observed; SM: photon and graviton zero modes, Dirac neutrinos of mass spectrum m1.  Add the graviton tower m_n = n/R with 5 dof, and for each bulk Dirac fermion a tower sqrt(M^2 + n^2/R^2), n >= 0, with 4 dof.  Levels are summed to n L /R ~ 30, so the short-circle region is honest: no cut of 60 levels.
Controls: the graviton-only tower must return the AdS3 of Pass 12539; N_f = 0 and no tower must return m1 <= 7.65 meV.
Reported: on a grid of N_f and M R, net sign today, R, min_L v(L) at m1 = 0, and the m1 bound.  KK masses for the fermion use the free spectrum.
usage: py -3 dd_massive_fermions.py"""
import json
import math
import numpy as np
from scipy.special import kn, kv, zeta
from scipy.optimize import brentq

D21, D31 = 7.49e-5, 2.513e-3
RHO_DE = 2.6e-11  # eV^4, about (2.26 meV)^4
LAM4 = (2.24e-3) ** 4  # as swampland_ext.py
HC = 0.1973269804  # micron eV
out = {}


def C_ratio(x):
    """V(l, M)/V(l, 0) per real dof, x = M l"""
    if x < 1e-6:
        return 1.0
    s = 0.0
    for w in range(1, 60):
        t = w ** -2.5 * kv(2.5, w * x)
        s += t
        if w * x > 60:
            break
    val = 2 * (4 * math.pi) ** -2.5 * (2 * x) ** 2.5 * s  # times l^-4, with sign -
    return val / (3 * zeta(5) / (4 * math.pi ** 2))


out["control_C_small_x"] = {str(x): C_ratio(x) for x in (1e-4, 1e-3, 1e-2, 0.1, 1.0, 2 * math.pi, 4 * math.pi, 8 * math.pi)}
print(out["control_C_small_x"], flush=True)
assert abs(C_ratio(1e-4) - 1) < 1e-6


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


Ls = np.logspace(-1.5, 5.5, 400)


def spectrum(m1):
    return [m1, math.sqrt(m1 ** 2 + D21), math.sqrt(m1 ** 2 + D31)]


def v_of_L(m1, R, Nf, MR, tower=True, lam=LAM4):
    v = lam - 4 * rho_arr(0.0, Ls)
    for m in spectrum(m1):
        v = v + 4 * rho_arr(m, Ls)
    if tower and R is not None:
        mk = 1 / R
        nmax = int(30 * R / Ls[0]) + 2
        nmax = min(nmax, 6000)
        # geometric thinning of levels with weights, exact sum replaced by Euler-Maclaurin weights
        ns = np.unique(np.r_[np.arange(1, 400), np.geomspace(400, nmax, 400).astype(int)]) if nmax > 400 else np.arange(1, nmax + 1)
        wts = np.gradient(ns.astype(float))
        wts[ns < 400] = 1.0
        for n, wt in zip(ns, wts):
            mn = n * mk
            arg_min = mn * Ls[0]
            v = v - wt * 5 * rho_arr(mn, Ls)
            for j in range(1):
                v = v + wt * Nf * 4 * rho_arr(math.sqrt((MR * mk) ** 2 + mn ** 2), Ls)
        v = v + Nf * 4 * rho_arr(MR * mk, Ls)  # n = 0 level
    return v


def net_today(R, Nf, MR):
    """V_C in eV^4 on an interval: half the circle of length 2 pi R; returns sign and value"""
    l = 2 * math.pi * R
    base = 3 * zeta(5) / (4 * math.pi ** 2 * l ** 4)
    return 0.5 * base * (-5 + Nf * 4 * C_ratio(MR * l / R))


# control 1, no tower, m1 bound as in Pass 12537
f0 = lambda m: float(v_of_L(m, None, 0, 0.0, tower=False).min())
out["control_no_tower_min_at_m1_0"] = f0(0.0)
hi = 1e-4
while f0(hi) > 0 and hi < 0.2:
    hi *= 1.3
m1b = brentq(f0, hi / 1.3, hi, xtol=1e-6) if hi < 0.2 else None
out["control_no_tower_m1_bound"] = m1b
print("no tower", f0(0.0), "m1 bound", m1b, flush=True)
eps_t = 0.3
rows = []
for Nf in (0, 1, 2, 3, 4, 6, 8):
    for MR in (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0):
        if Nf == 0 and MR > 0:
            continue
        l_over_R = 2 * math.pi
        cr = C_ratio(MR * l_over_R)
        net = -5 + Nf * 4 * cr
        rowd = dict(Nf=Nf, MR=MR, C=cr, net_dof=net, sign="negative" if net < 0 else "positive")
        rho_crit = RHO_DE / 0.69
        R_eVinv = (0.5 * abs(net) * 3 * zeta(5) / (4 * math.pi ** 2 * l_over_R ** 4) / (eps_t * rho_crit)) ** 0.25 if net != 0 else None
        rowd["R_micron"] = None if R_eVinv is None else R_eVinv * HC
        if R_eVinv is not None:
            v0 = v_of_L(0.0, R_eVinv, Nf, MR)
            rowd["min_v_m1_0"] = float(v0.min())
            rowd["L_of_min_micron"] = float(Ls[int(np.argmin(v0))] * HC)
            rowd["ads3_at_m1_0"] = bool(v0.min() < 0)
            if not rowd["ads3_at_m1_0"]:
                g = lambda m: float(v_of_L(m, R_eVinv, Nf, MR).min())
                hi = 1e-4
                while g(hi) > 0 and hi < 0.2:
                    hi *= 1.5
                rowd["m1_bound_eV"] = brentq(g, hi / 1.5, hi, xtol=1e-5) if hi < 0.2 else None
        rows.append(rowd)
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rowd.items()}, flush=True)
        out["grid"] = rows
        json.dump(out, open("dd_massive_fermions.json", "w"), indent=1, default=float)
print("done", flush=True)
