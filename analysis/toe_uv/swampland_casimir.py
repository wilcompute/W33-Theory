"""The Standard Model on a circle: the non-SUSY AdS conjecture against measured neutrino data.  Per real degree of freedom, on a circle of circumference L, the 4D Casimir density is
rho(m, L) = -/+ m^2 / (2 pi^2 L^2) sum_{k>=1} K_2(k m L) / k^2 (bosons -, periodic fermions +), which tends to -/+ pi^2 / (90 L^4) as m -> 0.
The 3D potential is proportional to (Lambda_4 + sum rho) / L^2, so an AdS3 vacuum exists iff Lambda_4 + sum rho(L) < 0 for some L.  Light spectrum: photon 2 and graviton 2 bosonic dof; each neutrino 2 (Majorana) or 4 (Dirac) periodic fermionic dof.
Heavier fermions matter only at L small compared with their Compton length, where the massless bosons are already outweighed; included: electron (4 dof) as a check.
Outputs: the bound on the lightest neutrino for NO and IO, Dirac and Majorana.  Controls: the published 7.7 meV (NO) and 2.5 meV (IO) with the old inputs.  Then the current data: DESI DR2 sum < 0.064 eV (95%).  usage: py -3 swampland_casimir.py"""
import json
import math
import numpy as np
from scipy.optimize import brentq
from scipy.special import kn


def rho_dof(m, L, nmax=40):
    """magnitude of the Casimir density per real dof, positive number"""
    if m * L < 1e-6:
        return math.pi ** 2 / (90 * L ** 4)
    tot = 0.0
    for k in range(1, nmax + 1):
        x = k * m * L
        if x > 700:
            break
        tot += kn(2, x) / k ** 2
    return m ** 2 / (2 * math.pi ** 2 * L ** 2) * tot


def min_density(masses, dof, Lambda4, nb=4):
    """the minimum over L of Lambda_4 + rho_total.  eV units, L in 1/eV"""
    Ls = np.logspace(0.0, 5.5, 900)
    best = (float("inf"), None)
    for L in Ls:
        v = Lambda4 - nb * rho_dof(0.0, L) + sum(d * rho_dof(m, L) for m, d in zip(masses, dof))
        if v < best[0]:
            best = (v, L)
    return best


def spectrum(m0, order, d21, d3l):
    if order == "NO":
        return [m0, math.sqrt(m0 ** 2 + d21), math.sqrt(m0 ** 2 + d3l)]
    # IO: m3 lightest; d3l = |Delta m^2_32| measured with m2 heaviest
    m2 = math.sqrt(m0 ** 2 + d3l)
    return [m0, math.sqrt(m2 ** 2 - d21), m2]


def bound(order, kind, Lambda4, d21, d3l):
    dof = [4, 4, 4] if kind == "Dirac" else [2, 2, 2]
    f = lambda m0: min_density(spectrum(m0, order, d21, d3l), dof, Lambda4)[0]
    v0 = f(0.0)
    if v0 < 0:
        vh = f(0.2)
        if vh < 0:
            return dict(kind=kind, order=order, status="AdS3 for every m0 tested (0 to 0.2 eV)", bound=None, m0_zero_value=v0)
    if v0 > 0:
        lo, hi = 0.0, 1e-5
        while f(hi) > 0 and hi < 0.2:
            lo, hi = hi, hi * 1.5
        if hi >= 0.2:
            return dict(kind=kind, order=order, status="no AdS3 up to 0.2 eV", bound=None)
        m = brentq(f, lo, hi, xtol=1e-7)
        return dict(kind=kind, order=order, status="no AdS3 only below the bound", bound=m, sum_at_bound=sum(spectrum(m, order, d21, d3l)))
    lo, hi = 1e-4, 0.2
    grid = np.logspace(-4, math.log10(0.2), 40)
    vals = [f(x) for x in grid]
    sign_change = [(grid[i], grid[i + 1]) for i in range(39) if vals[i] < 0 < vals[i + 1]]
    if sign_change:
        m = brentq(f, *sign_change[0], xtol=1e-7)
        return dict(kind=kind, order=order, status="no AdS3 only above a lower bound", lower_bound=m, sum_at_bound=sum(spectrum(m, order, d21, d3l)))
    return dict(kind=kind, order=order, status="AdS3 for every m0 on the grid", bound=None)


out = {}
L4_old = (2.26e-3) ** 4          # the published analyses used about this
inputs = dict(old=dict(Lambda4=3.25e-11, d21=7.5e-5, d3l=2.5e-3), current=dict(Lambda4=(2.24e-3) ** 4, d21=7.49e-5, d3l=2.513e-3))
for name, p in inputs.items():
    r = []
    for order in ("NO", "IO"):
        for kind in ("Dirac", "Majorana"):
            r.append(bound(order, kind, p["Lambda4"], p["d21"], p["d3l"] if order == "NO" else 2.484e-3 if name == "current" else p["d3l"]))
    out[name] = r
    print(name, flush=True)
    for x in r:
        print("  ", {k: (round(v * 1e3, 3) if isinstance(v, float) and k in ("bound", "lower_bound", "sum_at_bound") else v) for k, v in x.items() if k != "m0_zero_value"}, flush=True)
# the oscillation floor against the bound and DESI
d21, d31 = 7.49e-5, 2.513e-3
sum_no = lambda m: sum(spectrum(m, "NO", d21, d31))
out["sum_floor_NO_eV"] = sum_no(0.0)
out["sum_floor_IO_eV"] = sum(spectrum(0.0, "IO", d21, 2.484e-3))
out["desi_95_eV"] = 0.0642
m_desi = brentq(lambda m: sum_no(m) - 0.0642, 0, 0.05)
out["m1_max_from_DESI_NO_eV"] = m_desi
print({k: v for k, v in out.items() if k not in inputs})
json.dump(out, open("swampland_casimir.json", "w"), indent=1, default=float)
