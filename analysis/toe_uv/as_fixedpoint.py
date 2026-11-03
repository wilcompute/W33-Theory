"""Asymptotic-safety fixed points of the Standard Model with gravity, in the parametrisation of Eichhorn-Held (arXiv:1707.01107, 1803.04027): for k > M_Pl = 1e19 GeV, beta_gi = SM - f_g g_i, beta_y = SM - f_y y, beta_lam = SM + f_lam lam, with f_i = 0 below (sharp transition), one-loop above, two-loop SM below.
Three scenarios.
A (1803.04027): t, b both nonzero at the fixed point, y_t^2 - y_b^2 = g_Y^2 / 3.  Fit f_g to g_Y and f_y to y_b; PREDICT M_t.  Control: the paper's 178-182 GeV.
B (1707.01107-like): y_b = 0 at the fixed point, t nonzero.  Fit f_g to g_Y, f_y to the measured M_t.  Nothing predicted for M_t; it gives the relevance table.
Higgs: lambda on its fixed-point trajectory for a range of f_lam; PREDICT M_H.
Relevance table (the conflict test): at the far-UV fixed point the coefficient theta = beta_y / y at y -> 0, per Yukawa type, with theta < 0 relevant (free, may be nonzero and small) and theta > 0 irrelevant (y is forced to 0 exactly).  For the Dirac neutrino, theta > 0 would contradict the Dirac requirement of the no-AdS conjecture.
usage: py -3 as_fixedpoint.py"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from sm_rge import K, beta_sm, matching, run

MP = 1e19
TUV = 400
MT0, MH0, A3, MW = 172.57, 125.20, 0.1180, 80.369


def low_to_planck(mt, mh=MH0):
    m = matching(mt, mh, A3, MW)
    return run([m["gY"], m["g2"], m["g3"], m["yt"], m["lam"], 0.0155, 0.0100], mt, MP)


def planck_to_low(y, mt):
    return run(y, MP, mt)


def g_uv(gs_at_mp, fg, T):
    """g2, g3 flow above M_Pl: integrate upward, stable"""
    def rhs(t, g):
        return [K * g[0] ** 3 * (-19 / 6) - fg * g[0], K * g[1] ** 3 * (-7) - fg * g[1]]
    s = solve_ivp(rhs, (0, T), gs_at_mp, rtol=1e-10, atol=1e-14, dense_output=True, method="DOP853")
    return s.sol


def yuk_rhs(t, y, G, sol, fy):
    g2, g3 = sol(t)
    a, b, c = G, g2 ** 2, g3 ** 2
    yt, yb = y
    tt, bb = yt ** 2, yb ** 2
    return [K * yt * (9 / 2 * tt + 3 / 2 * bb - 17 / 12 * a - 9 / 4 * b - 8 * c) - fy * yt,
            K * yb * (9 / 2 * bb + 3 / 2 * tt - 5 / 12 * a - 9 / 4 * b - 8 * c) - fy * yb]


def yuk_at_mp(G, gs, fy, fg, branch, T=400):
    sol = g_uv(gs, fg, T)
    F = fy / K
    g2T, g3T = sol(T)
    b_, c_ = g2T ** 2, g3T ** 2
    if branch == "A":
        # 9/2 t + 3/2 b = F + 17/12 G + X; 3/2 t + 9/2 b = F + 5/12 G + X
        X = 9 / 4 * b_ + 8 * c_
        tt = ((F + 17 / 12 * G + X) * 9 / 2 - (F + 5 / 12 * G + X) * 3 / 2) / 18
        bb = tt - G / 3
        if bb <= 0 or tt <= 0:
            return None
        y0 = [math.sqrt(tt), math.sqrt(bb)]
    else:
        tt = (F + 17 / 12 * G + 9 / 4 * b_ + 8 * c_) * 2 / 9
        if tt <= 0:
            return None
        y0 = [math.sqrt(tt), 0.0]
    s = solve_ivp(yuk_rhs, (T, 0), y0, args=(G, sol, fy), rtol=1e-10, atol=1e-14, method="DOP853")
    if not s.success:
        return None
    return s.y[:, -1]


def lam_at_mp(flam, y_mp_t, G, gs, fy, fg, T=400):
    """lambda on the trajectory that stays bounded above M_Pl: irrelevant for flam > 0, solved by a fine downward sweep from the fixed point"""
    sol = g_uv(gs, fg, T)
    def rhs(t, l):
        g2, g3 = sol(t)
        a, b = G, g2 ** 2
        tt = y_mp_t ** 2                 # t ~ constant on the trajectory near the fixed point: adequate for this scan
        return K * (24 * l ** 2 + l * (12 * tt - 9 * b - 3 * a) - 6 * tt ** 2 + 9 / 8 * b ** 2 + 3 / 4 * a * b + 3 / 8 * a ** 2) + flam * l
    # for flam > 0 lambda relaxes quickly to its quasi-fixed value when integrated upward is unstable, so take the algebraic root at t = 0
    g2, g3 = sol(0)
    a, b, tt = G, g2 ** 2, y_mp_t ** 2
    A_ = K * 24
    B_ = K * (12 * tt - 9 * b - 3 * a) + flam
    C_ = K * (-6 * tt ** 2 + 9 / 8 * b ** 2 + 3 / 4 * a * b + 3 / 8 * a ** 2)
    disc = B_ ** 2 - 4 * A_ * C_
    return None if disc < 0 else (-B_ + math.sqrt(disc)) / (2 * A_)



def low_to(mt, scale, mh=MH0):
    m = matching(mt, mh, A3, MW)
    return run([m["gY"], m["g2"], m["g3"], m["yt"], m["lam"], 0.0155, 0.0100], mt, scale)


def analyse(kt, verbose=False):
    """all of it at transition scale kt"""
    y0 = low_to(MT0, kt)
    G = y0[0] ** 2
    gs = [y0[1], y0[2]]
    fg = K * 41 / 6 * G

    def predict_A(fy):
        v = yuk_at_mp(G, gs, fy, fg, "A")
        if v is None:
            return None
        mt = MT0
        for _ in range(6):
            y = low_to(mt, kt)
            lo = run([y[0], y[1], y[2], v[0], y[4], v[1], y[6]], kt, mt)
            mt = 173.34 + (lo[3] - 0.93690 + 0.00042 * (A3 - 0.1184) / 0.0007) / 0.00556
        return dict(mt=float(mt), yb_low=float(lo[5]), yt_low=float(lo[3]), yt_kt=float(v[0]), yb_kt=float(v[1]))

    f0 = K * G / 12
    grid = [f0 + d for d in np.concatenate([-np.logspace(-3, -8, 70), np.logspace(-8, -3, 70)])]
    vals = [(f, predict_A(float(f))) for f in grid]
    vals = [(f, r) for f, r in vals if r]
    A = None
    for (f1, r1), (f2, r2) in zip(vals, vals[1:]):
        if (r1["yb_low"] - 0.0155) * (r2["yb_low"] - 0.0155) < 0:
            fA = brentq(lambda f: predict_A(f)["yb_low"] - 0.0155, f1, f2, xtol=1e-11)
            A = dict(f_y=float(fA), **predict_A(fA))
            break
    if A is None and vals:
        best = min(vals, key=lambda x: x[1]["yb_low"])
        A = dict(no_solution_smallest_yb=best[1], f_y=float(best[0]))
    fB = brentq(lambda f: float(yuk_at_mp(G, gs, f, fg, "B")[0] if yuk_at_mp(G, gs, f, fg, "B") is not None else 0) - y0[3], -1.5e-3, 8e-3, xtol=1e-9)
    F = fB / K
    tB = (F + 17 / 12 * G) * 2 / 9
    tabB = dict(t=tB, G=G, F=F, third_gen_b=-3 * tB + G, up_light=-3 / 2 * tB, down_light=-3 / 2 * tB + G, charged_lepton=-3 / 2 * tB - 7 / 3 * G, dirac_neutrino=-3 / 2 * tB + 2 / 3 * G)
    return dict(k_tr=kt, gY_kt=float(y0[0]), g2_kt=float(y0[1]), g3_kt=float(y0[2]), yt_kt_measured=float(y0[3]), lam_kt_measured=float(y0[4]), f_g=float(fg), f0=float(f0), A=A, fB=float(fB), table_B=tabB)


out = {}
main = analyse(1e19)
out["k_1e19"] = main
G = main["gY_kt"] ** 2
out["analytic_branch_A"] = dict(dirac_neutrino="+G/6", down_light="+G/2", up_light="-G/2", charged_lepton="-G/2 - 7G/3", tau_fixed_point="y_tau^2 = 17/9 G", values=dict(dirac=G / 6, down_light=G / 2, up_light=-G / 2, lepton=-G / 2 - 7 * G / 3))
scan = []
for kt in (1e15, 1e16, 1e17, 3e17, 1e18, 3e18, 1e19, 3e19, 1e20, 1e21):
    r = analyse(kt)
    a = r["A"]
    scan.append(dict(k_tr=kt, Mt_A=a.get("mt"), yb_low=a.get("yb_low"), f_y=a.get("f_y"), no_solution=("no_solution_smallest_yb" in a), t_B=r["table_B"]["t"], third_gen_b_B=r["table_B"]["third_gen_b"], dirac_B=r["table_B"]["dirac_neutrino"], down_light_B=r["table_B"]["down_light"]))
    print(kt, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in scan[-1].items() if k != "k_tr"}, flush=True)
out["k_tr_scan"] = scan
y0 = low_to(MT0, 1e19)
G, gs = y0[0] ** 2, [y0[1], y0[2]]
fg = K * 41 / 6 * G
hi = []
for flam in [0.005, 0.01, 0.02, 0.052, 0.1, 0.2, 1.0, 100.0]:
    l_mp = lam_at_mp(flam, y0[3], G, gs, main["fB"], fg)
    if l_mp is None:
        hi.append(dict(f_lam=flam, lam_MP=None, MH=None, note="no real fixed point"))
        continue
    mh = brentq(lambda mh_: low_to(MT0, 1e19, mh_)[4] - l_mp, 110, 170, xtol=1e-3)
    hi.append(dict(f_lam=flam, lam_MP=float(l_mp), MH=float(mh)))
out["higgs_at_measured_Mt"] = hi
out["Mt_for_lambda_MP_zero_at_measured_MH"] = float(brentq(lambda mt: low_to(mt, 1e19)[4], 165, 180, xtol=1e-3))
print(json.dumps({k: out[k] for k in ("analytic_branch_A", "higgs_at_measured_Mt", "Mt_for_lambda_MP_zero_at_measured_MH")}, default=float))
print(json.dumps(main, default=float))
json.dump(out, open("as_fixedpoint.json", "w"), indent=1, default=float)
