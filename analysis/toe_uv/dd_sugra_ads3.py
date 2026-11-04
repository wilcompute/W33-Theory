"""No-AdS3 for 5D N = 1 supergravity with Scherk-Schwarz twist omega and N_H massive hypermultiplets, at the fitted (R, M) of casimir_sugra_*.json.  Towers, interval convention: gravity as in dd_ss_gravitino.py.  Each hyper: fermions 2 dof at sqrt(M^2 + n^2/R^2), scalars 2 dof at sqrt(M^2 + (n + omega)^2/R^2), for all integers n.  At omega = 0 they match level by level, which is the control.
Also the twist: V_C(omega) is a potential for the graviphoton Wilson line, with a minimum at omega = 1/2 for gravity alone.  Its curvature in omega is reported, and the mass in H0 units for a declared normalisation a = sqrt(3/2) M_Pl kappa omega with kappa = 1, a stand-in for the no-scale Kahler potential that I did not derive.  If the mass is of order H0 the twist can still be rolling, so omega = 1/2 is not guaranteed.
usage: py -3 dd_sugra_ads3.py"""
import json
import math
import os
import numpy as np
from scipy.optimize import brentq
from scipy.special import zeta

src = open("dd_ss_gravitino.py", encoding="utf-8").read().split("out = dict(rows=[])")[0]
g = {"__name__": "x"}
exec(src, g)
rho_arr, spectrum, Ls, LAM4, HC = (g[k] for k in ("rho_arr", "spectrum", "Ls", "LAM4", "HC"))
OM = 0.5


def v_of_L(m1, R, MR, NH):
    v = LAM4 - 6 * rho_arr(0.0, Ls)
    for m in spectrum(m1):
        v = v + 4 * rho_arr(m, Ls)
    mk = 1 / R
    nmax = min(int(30 * R / Ls[0]) + 2, 6000)
    ns = np.unique(np.r_[np.arange(1, 300), np.geomspace(300, nmax, 240).astype(int)]) if nmax > 300 else np.arange(1, nmax + 1)
    wts = np.gradient(ns.astype(float))
    wts[ns < 300] = 1.0
    M = MR * mk
    for n, wt in zip(ns, wts):
        v = v - wt * 8 * rho_arr(n * mk, Ls) + wt * 4 * (rho_arr((n + OM) * mk, Ls) + rho_arr((n - OM) * mk, Ls))
        fm = math.sqrt(M ** 2 + (n * mk) ** 2)
        v = v + wt * NH * 4 * rho_arr(fm, Ls)
        v = v - wt * NH * 2 * (rho_arr(math.sqrt(M ** 2 + ((n + OM) * mk) ** 2), Ls) + rho_arr(math.sqrt(M ** 2 + ((n - OM) * mk) ** 2), Ls))
    v = v + 4 * rho_arr(OM * mk, Ls)
    v = v + NH * 2 * rho_arr(M, Ls) - NH * 2 * rho_arr(math.sqrt(M ** 2 + (OM * mk) ** 2), Ls)
    return v


# Each row costs about 25 minutes, so only these: N_H = 3 and 8 at the minimum, the x_0 near V_min = 0, the second supernova sample.
TARGETS = [("dovekie", "3", "1.0"), ("dovekie", "8", "1.0"), ("dovekie", "3", "1.35"), ("desy5", "3", "1.0")]
out = json.load(open("dd_sugra_ads3.json")) if os.path.exists("dd_sugra_ads3.json") else dict(rows=[])
done = {(r["dataset"], str(r["N_H"]), r["xi_over_xmin"]) for r in out["rows"]}
for ds, nh, k in TARGETS:
    if (ds, nh, k) in done:
        continue
    d = json.load(open(f"casimir_sugra_{ds}.json"))
    for block, r in [(d[nh], d[nh]["rows"][k])]:
        if True:
            if "R_micron" not in r:
                continue
            R = r["R_micron"] / HC
            v = v_of_L(0.0, R, r["x0"], int(nh))
            row = dict(dataset=ds, N_H=int(nh), xi_over_xmin=k, R_micron=r["R_micron"], M_eV=r["M_eV"], x0=r["x0"], delta=r["delta"], V_min=r["V_min"], ads3=bool(v.min() < 0), L_min=float(Ls[int(np.argmin(v))] * HC))
            if not row["ads3"]:
                f = lambda m: float(v_of_L(m, R, r["x0"], int(nh)).min())
                hi = 1e-4
                while f(hi) > 0 and hi < 0.2:
                    hi *= 1.5
                row["m1_bound_eV"] = brentq(f, hi / 1.5, hi, xtol=1e-4) if hi < 0.2 else None
            out["rows"].append(row)
            print({a: (round(float(c), 4) if isinstance(c, float) else c) for a, c in row.items()}, flush=True)
            json.dump(out, open("dd_sugra_ads3.json", "w"), indent=1, default=float)
# the twist
oms = np.linspace(0, 1, 401)
S = np.array([sum((1 - math.cos(2 * math.pi * w * o)) / w ** 5 for w in range(1, 300)) for o in oms]) / float(zeta(5))
i = int(np.argmax(S))
d2S = (S[i + 1] - 2 * S[i] + S[i - 1]) / (oms[1] - oms[0]) ** 2
# V(omega) = -|V_C(1/2)| S(omega)/S(1/2), in units of rho_crit
eps = 0.33
mu2_H0 = abs(d2S) / S[i] * eps * 3 / (1.5)  # V in units 3 H0^2 M^2 / f^2 with f^2 = (3/2) M^2 kappa^2
out["twist"] = dict(omega_at_min=float(oms[i]), S_at_min=float(S[i]), d2S=float(d2S), mu_over_H0_kappa1=math.sqrt(mu2_H0))
print(out["twist"], flush=True)
json.dump(out, open("dd_sugra_ads3.json", "w"), indent=1, default=float)
print("done", flush=True)
