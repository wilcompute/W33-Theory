"""The future of Lambda + negative Casimir + sparse tower.  At the best fit chi_N < 0 today: the field has turned around and rolls back towards smaller radius, where V_C = Z exp(-4 b chi) is more negative without limit.  So V crosses zero and H reaches zero: recollapse, unlike the fading fit, where V = V0 exp(-c phi) stays positive.
Integrates N > 0 from the best fit of casimir_fits_*.json, in cosmic time t (H0 t), with matter, sparse tower, radiation neglected from N > 0 being small but kept.  Reports t when V = 0, when H = 0 (the turnaround), and the maximum N.  Control: Z = 0 with no drag must give de Sitter with no turnaround.  Also the no-drag fit: with f -> 0 the field has no kick and the term pulls it inward from the start.
Forward in time from the same state, so this depends on the potential staying exactly this form to radii much smaller than today's, which is an extrapolation.  usage: py -3 casimir_future.py dataset data_dir"""
import json
import math
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import dark_like as L
import casimir_fast as CF

ds, dd = sys.argv[1], sys.argv[2]
sn = L.load_sn(ds, dd)
fits = json.load(open(f"casimir_fits_{ds}.json"))


def future(b, prod, n, Z, wb, wbc, h):
    _, i = CF.solve(b, prod, n, Z, wb, wbc, h, want=True)
    f = prod / b
    lam = n * b
    ol = i["ol"]
    h2 = h * h
    # today's values
    chi0, x0 = i["chi0"], i["chiN0"]
    om_u = (wbc - wb) / h2 * (1 - f) + (wb + L.OMEGA_NU_H2) / h2
    # coupled density today from the budget
    kin0 = x0 * x0 / 6
    rc0 = 1 * (1 - kin0) - om_u - ol - Z * math.exp(-lam * chi0) - L.OMEGA_R_H2 / h2
    # integrate in t = H0 t: y = (ln a, chi, chidot, H), sign of H may change
    def rhs(t, y):
        la, chi, cd, H = y
        a3 = math.exp(-3 * la)
        rm = om_u * a3
        rc = rc0 * a3 * math.exp(-b * (chi - chi0))
        rr = L.OMEGA_R_H2 / h2 * a3 * math.exp(-la)
        # field: chi'' + 3 H chi' = -dV/dchi + b rho_c, with V and rho in units of 3 H0^2 M^2: factor 3
        dV = -lam * Z * math.exp(-lam * chi)
        cdd = -3 * H * cd + 3 * (-dV + b * rc)
        Hd = -0.5 * (cd * cd + 3 * (rm + rc + 4 / 3 * rr))
        return [H, cd, cdd, Hd]

    def turn(t, y):
        return y[3]

    turn.terminal = True
    turn.direction = -1

    def V0(t, y):
        return ol + Z * math.exp(-lam * y[1])

    V0.direction = -1
    s = solve_ivp(rhs, (0, 200.0), [0.0, chi0, x0, 1.0], rtol=1e-9, atol=1e-11, method="LSODA", events=[turn, V0])
    tV = float(s.t_events[1][0]) if len(s.t_events[1]) else None
    tH = float(s.t_events[0][0]) if len(s.t_events[0]) else None
    H0Gyr = 977.8 / (100 * h)
    return dict(chi0=chi0, chiN0=x0, rc0=rc0, t_V_zero_H0=tV, t_turnaround_H0=tH, t_V_zero_Gyr=None if tV is None else tV * H0Gyr, t_turnaround_Gyr=None if tH is None else tH * H0Gyr, N_max=float(s.y[0].max()), V_today=ol + Z * math.exp(-lam * chi0), end_t=float(s.t[-1]))


out = dict(dataset=ds)
for k in ("0.7071_-1", "1.0_-1", "0.7071_1"):
    v = fits["best"][k]
    b = float(k.split("_")[0])
    out[k] = future(b, v["prod"], 4.0, v["Z"], v["wb"], v["wbc"], v["h"])
    print(k, {a: (round(c, 3) if isinstance(c, float) else c) for a, c in out[k].items()}, flush=True)
# control: no Casimir and almost no coupling: no turnaround
v = fits["best"]["0.7071_-1"]
out["control_Z0"] = future(0.7071, 1e-7, 4.0, 0.0, v["wb"], v["wbc"], v["h"])
print("control", out["control_Z0"], flush=True)
assert out["control_Z0"]["t_turnaround_H0"] is None
# no-drag fit: grid in small Z, f -> 0
lc = minimize(lambda p: L.chi2(L.E_lcdm(p[1], p[2]), p[2], p[0], p[1], sn), [0.02223, 0.142, 0.675], method="Nelder-Mead", options=dict(xatol=3e-5, fatol=3e-3, maxiter=800))
rows = {}
for Z in (-0.001, -0.003, -0.01, -0.03, -0.1, -0.2, -0.3, -0.5):
    def fn_(p):
        try:
            return L.chi2(CF.solve(0.7071, 1e-7, 4.0, Z, p[0], p[1], p[2]), p[2], p[0], p[1], sn)
        except Exception:
            return 1e8
    r = minimize(fn_, lc.x, method="Nelder-Mead", options=dict(xatol=3e-5, fatol=3e-3, maxiter=300))
    rows[str(Z)] = r.fun - lc.fun
    print("no drag Z", Z, round(r.fun - lc.fun, 2), flush=True)
out["no_drag_grid"] = rows
json.dump(out, open(f"casimir_future_{ds}.json", "w"), indent=1, default=float)
print("done", flush=True)
