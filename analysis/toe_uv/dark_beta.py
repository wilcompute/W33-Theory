"""Joint fit of (c, c', beta): baryons and every brane scale carry mass ~ exp(-beta phi) in Planck units, so the fit sees the coupling directly rather than only through a solar-system bound.
Background: rho_b ~ a^-3 exp(-beta phi), force beta rho_b.  Observed redshift: 1 + z = (1/a) exp(beta (phi - phi_0)), conformal distances unchanged; BAO and CMB angles are frame invariant, D_H = d chi / dz_obs.
SNe: M_Ch ~ G^(-3/2) gives Delta M = s (15/4) log10(G/G0), with G m^2 ~ exp(-2 beta phi), s = 1 (Gaztanaga et al 2002), or s = 0 (no G dependence of the standard candle): both reported, the G scaling of SNe being model dependent.
Priors when switched on: Cassini gamma - 1 = (2.1 +- 2.3)e-5 with gamma - 1 = -4 beta^2/(1 + 2 beta^2); LLR Gdot/G = (7.1 +- 7.6)e-14 per year (Hofmann and Mueller 2018) with Gdot/G = -2 beta phi_N H0.
xi = dlnVol/dlnL = 2 r/(1 - r), r = beta/c'.  Control: beta = 0 returns fading_ds.py.  usage: py -3 dark_beta.py dataset data_dir"""
import json
import math
import sys
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import minimize
import dark_like as L

ds, ddir = sys.argv[1], sys.argv[2]
sn = L.load_sn(ds, ddir)
NI = -12.0
NG = np.log(1 / (1 + L.ZGRID))[::-1]
NREC = -math.log(1090.0)


def solve(c, cp, be, wb, wbc, h):
    h2 = h * h
    orr, ob0, onu = L.OMEGA_R_H2 / h2, wb / h2, L.OMEGA_NU_H2 / h2
    oc_rec = (wbc - wb) / h2
    oci, obi = oc_rec, ob0

    def run(lV, oci, obi):
        V0 = math.exp(lV)

        def rhs(N, s):
            phi, p = s
            ea = math.exp(-3 * N)
            rc = oci * ea * math.exp(-cp * phi)
            rb = obi * ea * math.exp(-be * phi)
            rn = onu * ea
            rr = orr * ea * math.exp(-N)
            V = V0 * math.exp(-c * phi)
            E2 = (rc + rb + rn + rr + V) / (1 - p * p / 6)
            dlnH = -0.5 * (p * p + 3 * (rc + rb + rn + 4 / 3 * rr) / E2)
            return [p, -(3 + dlnH) * p + 3 * (c * V + cp * rc + be * rb) / E2]

        return solve_ivp(rhs, (NI, 0), [0.0, 0.0], rtol=1e-8, atol=1e-11, method="LSODA", dense_output=True)

    def e1(lV, oci, obi):
        s = run(lV, oci, obi)
        if not s.success:
            raise RuntimeError
        phi, p = s.y[:, -1]
        return (oci * math.exp(-cp * phi) + obi * math.exp(-be * phi) + onu + orr + math.exp(lV - c * phi)) / (1 - p * p / 6) - 1, s

    lV = math.log(max(1 - (wbc + L.OMEGA_NU_H2) / h2, 0.05))
    for _ in range(3):
        for __ in range(14):
            d, s = e1(lV, oci, obi)
            if abs(d) < 1e-7:
                break
            dd, _s = e1(lV + 1e-4, oci, obi)
            lV -= d / ((dd - d) / 1e-4)
        pr = float(s.sol(NREC)[0])
        nc, nb = oc_rec * math.exp(cp * pr), ob0 * math.exp(be * pr)
        done = abs(nc / oci - 1) < 1e-8 and abs(nb / obi - 1) < 1e-8
        oci, obi = nc, nb
        if done:
            break
    d, s = e1(lV, oci, obi)
    phi, p = s.sol(NG)
    a3 = np.exp(-3 * NG)
    E2 = (oci * a3 * np.exp(-cp * phi) + obi * a3 * np.exp(-be * phi) + onu * a3 + orr * a3 * np.exp(-NG) + math.exp(lV) * np.exp(-c * phi)) / (1 - p * p / 6)
    E = np.sqrt(E2)
    return E[::-1], phi[::-1], p[::-1]


def chi2_model(c, cp, be, s_, wb, wbc, h, priors):
    E, phi, p = solve(c, cp, be, wb, wbc, h)
    z_true = L.ZGRID
    if be != 0.0:
        z_obs = (1 + z_true) * np.exp(be * (phi - phi[0])) - 1
        chi = cumulative_trapezoid(1 / E, z_true, initial=0)
        chi_o = np.interp(L.ZGRID, z_obs, chi)
        tail = L.ZGRID > z_obs[-1]  # z_obs can end below the grid top when beta > 0: continue linearly rather than clamp
        chi_o[tail] = chi[-1] + (L.ZGRID[tail] - z_obs[-1]) * (chi[-1] - chi[-2]) / (z_obs[-1] - z_obs[-2])
        E_eff = 1 / np.gradient(chi_o, L.ZGRID)
        phi_o = np.interp(L.ZGRID, z_obs, phi)
    else:
        E_eff, phi_o = E, phi
    s2 = dict(sn)
    if s_ != 0.0 and be != 0.0:
        dM = s_ * (15 / 4) * (-2 * be * (np.interp(sn["ZC"], L.ZGRID, phi_o) - phi[0])) / math.log(10)
        s2["MU"] = sn["MU"] - dM
    x = L.chi2(E_eff, h, wb, wbc, s2)
    extra = 0.0
    gd = -2 * be * p[0] * H0YR(h)
    if priors:
        gm = -4 * be * be / (1 + 2 * be * be)
        extra = ((gm - 2.1e-5) / 2.3e-5) ** 2 + ((gd - 7.1e-14) / 7.6e-14) ** 2
    return x + extra, gd


def H0YR(h):
    return 100 * h / 3.0857e19 * 3.156e7


def nm(fn, x0, steps, maxiter):
    x0 = np.asarray(x0, float)
    return minimize(fn, x0, method="Nelder-Mead", options=dict(xatol=3e-5, fatol=3e-3, maxiter=maxiter, maxfev=maxiter, initial_simplex=np.vstack([x0] + [x0 + np.eye(len(x0))[i] * steps[i] for i in range(len(x0))])))


prev = json.load(open(f"fading_ds_{ds}.json"))
fn = prev["free_c_neg"]
lcdm = prev["LCDM"]["chi2"]
PRIOR0 = (2.1 / 2.3) ** 2 + (7.1 / 7.6) ** 2  # the priors' cost at beta = 0, also paid by LCDM
out = dict(dataset=ds, lcdm=lcdm, prior_cost_at_beta0=PRIOR0, single=dict(delta=fn["delta"], c=fn["c"], cp=fn["cp"]))
fname = f"dark_beta_{ds}.json"
x0 = [fn["wb"], fn["wbc"], fn["h"], fn["c"], fn["cp"]]
S = [1e-4, 1e-3, 3e-3, 0.15, 0.01]
out["control_beta0"] = chi2_model(fn["c"], fn["cp"], 0.0, 1.0, fn["wb"], fn["wbc"], fn["h"], False)[0] - lcdm
print("control", out["control_beta0"], fn["delta"], flush=True)


def f_at(be, s_, priors, key, start, sgn):
    def f(p):
        if p[3] * sgn < 0 or p[4] < 0:
            return 1e8
        try:
            return chi2_model(p[3], p[4], be, s_, p[0], p[1], p[2], priors)[0]
        except Exception:
            return 1e8
    r = nm(f, start, S, 420)
    return dict(beta=be, delta=r.fun - lcdm, wb=r.x[0], wbc=r.x[1], h=r.x[2], c=r.x[3], cp=r.x[4], gdot=chi2_model(r.x[3], r.x[4], be, s_, *r.x[:3], False)[1])


BE = (-0.3, -0.1, -0.03, -0.01, -0.004, 0.004, 0.01, 0.03, 0.1, 0.3)
for s_ in (1.0, 0.0):
    rows = []
    for be in BE:
        r = f_at(be, s_, False, "", x0, -1)
        rows.append(r)
        print("s", s_, "beta", be, round(r["delta"], 2), "c", round(r["c"], 3), "cp", round(r["cp"], 3), "gdot", r["gdot"], flush=True)
        out[f"profile_s{int(s_)}"] = rows
        json.dump(out, open(fname, "w"), indent=1, default=float)


# free beta, with and without the Cassini + LLR priors; both signs of the start
def free(s_, priors):
    best = None
    for b0 in (-0.01, 0.01):
        def f(p):
            if p[3] > 0 or p[4] < 0:
                return 1e8
            try:
                return chi2_model(p[3], p[4], p[5], s_, p[0], p[1], p[2], priors)[0]
            except Exception:
                return 1e8
        r = nm(f, x0 + [b0], S + [0.005], 700)
        if best is None or r.fun < best.fun:
            best = r
    x = best.x
    ratio = x[5] / x[4] if x[4] else 0.0
    return dict(delta=best.fun - lcdm - (PRIOR0 if priors else 0.0), wb=x[0], wbc=x[1], h=x[2], c=x[3], cp=x[4], beta=x[5], xi=2 * ratio / (1 - ratio) if abs(1 - ratio) > 1e-9 else None)


for s_ in (1.0, 0.0):
    for pri in (False, True):
        k = f"free_s{int(s_)}_{'priors' if pri else 'nopriors'}"
        out[k] = free(s_, pri)
        print(k, {a: round(b, 5) for a, b in out[k].items() if b is not None}, flush=True)
        json.dump(out, open(fname, "w"), indent=1, default=float)
print("done", flush=True)
