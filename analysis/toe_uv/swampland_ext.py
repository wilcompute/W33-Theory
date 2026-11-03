"""Extensions of swampland_casimir.py.
(a) How many extra massless bosonic dof does the no-AdS3 conjecture allow, with measured neutrinos (Dirac, NO)?  This bounds massless dark photons (2 dof) and massless scalars (1 dof).
(b) The bound on Lambda: for a given lightest neutrino mass, the minimal Lambda_4 with no AdS3, i.e. Lambda_4^{1/4} >= c m_1; c is computed.
(c) Dark dimension: m_KK = 1/R, gravitons in the bulk (a massive KK level has 5 dof) and right-handed neutrinos in the bulk with KK masses approximately sqrt(m_i^2 + n^2 m_KK^2), 4 dof per flavour per level.  How the bound on m_1 changes with m_KK.  The tower offset is noted by Anchordoqui, Antoniadis, Cunat; this gives the numbers.
usage: py -3 swampland_ext.py"""
import json
import math
import numpy as np
from scipy.optimize import brentq
from scipy.special import kn

D21, D31 = 7.49e-5, 2.513e-3
L4 = (2.24e-3) ** 4
Ls = np.logspace(0.0, 5.5, 700)


def rho_arr(m, L):
    """magnitude per real dof on the array L; sums over windings"""
    if m < 1e-12:
        return math.pi ** 2 / (90 * L ** 4)
    tot = np.zeros_like(L)
    for k in range(1, 30):
        tot += kn(2, np.minimum(k * m * L, 690)) / k ** 2
    return m ** 2 / (2 * math.pi ** 2 * L ** 2) * tot


def spectrum(m1):
    return [m1, math.sqrt(m1 ** 2 + D21), math.sqrt(m1 ** 2 + D31)]


def min_rho(m1, nb, lam=L4, extra=None):
    v = lam - nb * rho_arr(0.0, Ls)
    for m in spectrum(m1):
        v = v + 4 * rho_arr(m, Ls)
    if extra is not None:
        v = v + extra(m1)
    return float(v.min())


out = {}
rows = []
for nb in (4, 5, 6, 7, 8):
    f = lambda m: min_rho(m, nb)
    v0 = f(0.0)
    if v0 < 0:
        rows.append(dict(nb=nb, extra_massless_bosons=nb - 4, massless_lightest="AdS3 even at m1 = 0", m1_bound=None))
        continue
    hi = 1e-5
    while f(hi) > 0 and hi < 0.2:
        hi *= 1.4
    rows.append(dict(nb=nb, extra_massless_bosons=nb - 4, m1_bound=brentq(f, hi / 1.4, hi, xtol=1e-7) if hi < 0.2 else None))
out["extra_massless_bosons"] = rows
print(rows, flush=True)
# (b) minimal Lambda for given m1, in units of m1: Lambda^{1/4} / m1
cs = []
for m1 in (1e-3, 2e-3, 4e-3, 7.65e-3):
    g = lambda lam: min_rho(m1, 4, lam)
    lo, hi = 1e-16, 1e-6
    lam = brentq(g, lo, hi, xtol=1e-19) if g(hi) > 0 and g(lo) < 0 else None
    cs.append(dict(m1=m1, Lambda14_min=None if lam is None else lam ** 0.25, ratio=None if lam is None else lam ** 0.25 / m1))
out["minimal_Lambda_for_m1"] = cs
print(cs, flush=True)
# (c) dark dimension
def tower(mk, nlev=60):
    def extra(m1):
        v = np.zeros_like(Ls)
        for n in range(1, nlev + 1):
            mn = n * mk
            if mn * Ls[0] > 200:
                break
            v = v - 5 * rho_arr(mn, Ls)                       # massive graviton level: bosonic
            for m in spectrum(m1):
                v = v + 4 * rho_arr(math.sqrt(m ** 2 + mn ** 2), Ls)      # bulk right-handed tower
        return v
    return extra


dd = []
for mk in (1e-1, 3e-2, 1e-2, 6e-3, 3e-3, 1e-3, 3e-4):
    ex = tower(mk)
    f = lambda m: min_rho(m, 4, L4, ex)
    v0 = f(0.0)
    if v0 < 0:
        dd.append(dict(m_KK_eV=mk, R_um=0.1973 / mk, status="AdS3 at m1 = 0"))
        continue
    hi = 1e-5
    while f(hi) > 0 and hi < 0.2:
        hi *= 1.4
    if hi >= 0.2:
        dd.append(dict(m_KK_eV=mk, R_um=0.1973 / mk, status="no AdS3 up to 0.2 eV"))
    else:
        b = brentq(f, hi / 1.4, hi, xtol=1e-7)
        dd.append(dict(m_KK_eV=mk, R_um=0.1973 / mk, m1_bound_meV=b * 1e3, sum_meV=sum(spectrum(b)) * 1e3))
    print(dd[-1], flush=True)
ex0 = None
# graviton-only tower: right-handed neutrinos on the brane
dg = []
for mk in (1e-2, 6e-3, 3e-3, 1e-3, 3e-4):
    def ex(m1, mk=mk):
        v = np.zeros_like(Ls)
        for n in range(1, 61):
            if n * mk * Ls[0] > 200:
                break
            v = v - 5 * rho_arr(n * mk, Ls)
        return v
    f = lambda m: min_rho(m, 4, L4, ex)
    dg.append(dict(m_KK_eV=mk, R_um=0.1973 / mk, min_density_at_m1_0=f(0.0), AdS3_at_m1_0=f(0.0) < 0))
out["dark_dimension_bulk_nuR"] = dd
out["dark_dimension_graviton_only"] = dg
print(dg, flush=True)
json.dump(out, open("swampland_ext.json", "w"), indent=1, default=float)
