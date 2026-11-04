"""What could measure the Casimir exponent, given that CMB + BAO + SN do not?  Best fits at n = 1, 4, 12 (b = 1/sqrt 2, s = -1), each refit, then the observables that differ: H(z), D_M(z), w_phi(z), the growth of each fluid, f sigma8 proxy, and the future.
Forecast yardsticks are declared, not measured: 0.3 percent on D_M and D_H per z bin (a stage-V BAO target), 1 percent on f sigma8 per bin, 0.005 mag on SN at z < 0.1.
Growth: subhorizon two-fluid ODE from a = 0.02, G_eff from 2 b^2 on the coupled fluid, friction -b chi_N; same equations controlled in class_controls.py and resolved by CLASS in class_fraction.py.
usage: py -3 casimir_nobs.py dataset data_dir"""
import json
import math
import sys
import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.optimize import minimize
import dark_like as L
import casimir_fast as CF

ds, dd = sys.argv[1], sys.argv[2]
sn = L.load_sn(ds, dd)
fits = json.load(open(f"casimir_fits_{ds}.json"))
b = 0.7071
base = fits["best"]["0.7071_-1"]


def X(n, p):
    if not (0 < p[3] <= b) or p[4] >= 0:
        return 1e8
    try:
        return L.chi2(CF.solve(b, p[3], n, p[4], p[0], p[1], p[2]), p[2], p[0], p[1], sn)
    except Exception:
        return 1e8


def nm(fn, x0, steps, maxiter):
    x0 = np.asarray(x0, float)
    return minimize(fn, x0, method="Nelder-Mead", options=dict(xatol=3e-5, fatol=3e-3, maxiter=maxiter, maxfev=maxiter, initial_simplex=np.vstack([x0] + [x0 + np.eye(len(x0))[i] * steps[i] for i in range(len(x0))])))


def growth(n, x):
    wb, wbc, h, prod, Z = x
    E, inf = CF.solve(b, prod, n, Z, wb, wbc, h, want=True)
    f = prod / b
    zg = L.ZGRID
    Ng = -np.log1p(zg)[::-1]
    Eg = E[::-1]
    # chi(N) by the same integration as casimir_fast: re-derive from the solver output via a second call on the grid
    chi = _chi(n, x)
    chiN = np.gradient(chi, Ng)
    h2 = h * h
    ob = (wb + L.OMEGA_NU_H2) / h2
    oc_rec = (wbc - wb) / h2
    i_rec = int(np.argmin(abs(Ng + math.log(1090))))
    oci = oc_rec / ((1 - f) + f * np.exp(-b * chi[i_rec]))
    a3 = np.exp(-3 * Ng)
    Oc = f * oci * a3 * np.exp(-b * chi) / Eg ** 2
    Ou = (1 - f) * oci * a3 / Eg ** 2
    Ob = wb / h2 * a3 / Eg ** 2
    dlnH = np.gradient(np.log(Eg), Ng)

    def rhs(N, y):
        oc, ou, obb, cn, dh = (np.interp(N, Ng, q) for q in (Oc, Ou, Ob, chiN, dlnH))
        src = 1.5 * (oc * y[0] + ou * y[2] + obb * y[4])
        return [y[1], -(2 + dh - b * cn) * y[1] + src + 1.5 * 2 * b * b * oc * y[0], y[3], -(2 + dh) * y[3] + src, y[5], -(2 + dh) * y[5] + src]

    Ni = math.log(0.02)
    s = solve_ivp(rhs, (Ni, 0), [1, 1, 1, 1, 1, 1], rtol=1e-7, atol=1e-10, dense_output=True)
    res = {}
    for z in (0.0, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0):
        N = -math.log(1 + z)
        y = s.sol(N)
        oc, ou, obb = (float(np.interp(N, Ng, q)) for q in (Oc, Ou, Ob))
        tot = oc + ou + obb
        dm = (oc * y[0] + ou * y[2] + obb * y[4]) / tot
        dmN = (oc * y[1] + ou * y[3] + obb * y[5]) / tot
        res[str(z)] = dict(D=float(dm), f=float(dmN / dm))
    D0 = res["0.0"]["D"]
    for z, v in res.items():
        v["fs8_rel"] = v["f"] * v["D"] / D0
    res["coupled_over_uncoupled_today"] = float(s.y[0, -1] / s.y[2, -1])
    return res


def _chi(n, x):
    wb, wbc, h, prod, Z = x
    _, inf = CF.solve(b, prod, n, Z, wb, wbc, h, want=True)
    f = prod / b
    h2 = h * h
    orr, obn = L.OMEGA_R_H2 / h2, (wb + L.OMEGA_NU_H2) / h2
    oc_rec = (wbc - wb) / h2
    lam = n * b
    ol = inf["ol"]
    oci = oc_rec / ((1 - f) + f * math.exp(-b * inf["chi_rec"]))
    fo, uo = f * oci, (1 - f) * oci + obn

    def rhs(N, y):
        c, xx = y
        ea = math.exp(-3 * N)
        rcc = fo * ea * math.exp(-b * c)
        rr = orr * ea * math.exp(-N)
        Vc = Z * math.exp(-lam * c)
        E2 = (rcc + uo * ea + rr + ol + Vc) / (1 - xx * xx / 6)
        dl = -0.5 * (xx * xx + 3 * (rcc + uo * ea + 4 / 3 * rr) / E2)
        return [xx, -(3 + dl) * xx + 3 * (b * rcc + lam * Vc) / E2]

    Ng = -np.log1p(L.ZGRID)[::-1]
    m = Ng >= CF.NI
    s = solve_ivp(rhs, (CF.NI, 0), [0.0, 0.0], rtol=1e-8, atol=1e-11, method="LSODA", t_eval=Ng[m])
    chi = np.zeros_like(Ng)
    chi[m] = s.y[0]
    return chi


out = dict(dataset=ds, rows={})
S = [1e-4, 1e-3, 3e-3]
x0 = [base["wb"], base["wbc"], base["h"], base["prod"], base["Z"]]
zs = np.array([0.05, 0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.33, 3.0])
for n in (1.0, 4.0, 12.0):
    z0 = fits["n_scan"][str(n)]["Z"]
    r = nm(lambda p: X(n, p), x0[:3] + [fits["n_scan"][str(n)]["prod"], z0], S + [0.005, 0.05 * z0], 500)
    wb, wbc, h, prod, Z = r.x
    E, inf = CF.solve(b, prod, n, Z, wb, wbc, h, want=True)
    chi = cumulative_trapezoid(1 / E, L.ZGRID, initial=0) * L.C / (100 * h)
    rd = 147.05 * (wb / 0.02236) ** -0.13 * (wbc / 0.1432) ** -0.23
    out["rows"][str(n)] = dict(delta=r.fun - L.chi2(L.E_lcdm(*_lcdm(sn) if False else (wbc, h)), h, wb, wbc, sn) if False else r.fun, x=list(r.x), H0=100 * h, eps=inf["eps"], w=inf["w_phi"], V_rel=inf["V_over_V0"], DM=(np.interp(zs, L.ZGRID, chi) / rd).tolist(), DH=(L.C / (100 * h * np.interp(zs, L.ZGRID, E)) / rd).tolist(), growth=growth(n, r.x))
    print(n, round(r.fun, 2), "eps", round(inf["eps"], 3), "h", round(h, 4), "w", {k: round(v, 3) for k, v in inf["w_phi"].items()}, flush=True)
a, c, e = (out["rows"][k] for k in ("1.0", "4.0", "12.0"))
out["zs"] = zs.tolist()
out["dDM_percent_1_vs_12"] = (100 * (np.array(a["DM"]) / np.array(e["DM"]) - 1)).tolist()
out["dDH_percent_1_vs_12"] = (100 * (np.array(a["DH"]) / np.array(e["DH"]) - 1)).tolist()
out["dfs8_percent_1_vs_12"] = {z: 100 * (a["growth"][z]["fs8_rel"] / e["growth"][z]["fs8_rel"] - 1) for z in ("0.0", "0.3", "0.5", "1.0", "2.0")}
# SN: distance modulus difference with a free offset, mag
mu = lambda g: 5 * np.log10(np.array(g["DM"]) * (1 + zs))
out["dmu_mag_1_vs_12"] = (mu(a) - mu(e) - (mu(a) - mu(e))[0]).tolist()
# yardstick chi2
sD = 0.3
ch = float(np.sum((np.array(out["dDM_percent_1_vs_12"][2:]) / sD) ** 2) + np.sum((np.array(out["dDH_percent_1_vs_12"][2:]) / sD) ** 2))
out["yardstick_chi2_BAO_0p3pc_8bins"] = ch
out["yardstick_chi2_fs8_1pc"] = float(sum((v / 1.0) ** 2 for v in out["dfs8_percent_1_vs_12"].values()))
print({k: out[k] for k in ("dDM_percent_1_vs_12", "dDH_percent_1_vs_12", "dfs8_percent_1_vs_12", "dmu_mag_1_vs_12", "yardstick_chi2_BAO_0p3pc_8bins", "yardstick_chi2_fs8_1pc")}, flush=True)
print("growth coupled/uncoupled", a["growth"]["coupled_over_uncoupled_today"], c["growth"]["coupled_over_uncoupled_today"], e["growth"]["coupled_over_uncoupled_today"], flush=True)
json.dump(out, open(f"casimir_nobs_{ds}.json", "w"), indent=1, default=float)
print("done", flush=True)
