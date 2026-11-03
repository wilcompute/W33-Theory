"""lambda on its true trajectory above M_Pl, with g2, g3, y_t all flowing (as_fixedpoint.py used an algebraic estimate with y_t frozen at M_Pl).  One loop above k = 1e19 GeV with gravity terms; start at the far-UV fixed point, integrate downward (stable for f_lam > 0), and read lambda(1e19); two-loop SM below; M_H from the Buttazzo matching.
Two fits only: f_g to g_Y, f_y to M_t (branch B).  Then f_lam: (a) scanned; (b) the value the Eichhorn-Held functions imply at the (G*, Lam*) reproducing those two fits.  If (b) gives M_H near 125.2 that would be a third number from two fits, so it is tested for dependence on the transition scale, the start T, and M_t.  usage: py -3 higgs_trajectory.py"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

src = open("as_fixedpoint.py", encoding="utf-8").read().split("out = {}\nmain = analyse(1e19)")[0]
exec(src)


def f_y_EH(L):
    return (96 + L * (-235 + L * (103 + 56 * L))) / (12 * math.pi * (3 + 2 * L * (-5 + 4 * L)) ** 2)


def f_l_EH(L):
    return (165 - 8 * L * (61 + L * (-49 + 4 * L))) / (6 * math.pi * (3 + 2 * L * (-5 + 4 * L)) ** 2)


def f_g_EH(L):
    return 5 * (1 - 4 * L) / (18 * math.pi * (1 - 2 * L) ** 2)


def fit_fy(mt, kt, T):
    y0 = low_to(mt, kt)
    G = y0[0] ** 2
    fg = K * 41 / 6 * G
    gs = [y0[1], y0[2]]
    fy = brentq(lambda f: float(yuk_at_mp(G, gs, f, fg, "B", T)[0] if yuk_at_mp(G, gs, f, fg, "B", T) is not None else 0) - y0[3], -1.5e-3, 8e-3, xtol=1e-10)
    return y0, G, fg, gs, fy


def lam_traj(flam, G, fg, gs, fy, T):
    sol = g_uv(gs, fg, T)
    def rhs(t, y):
        g2, g3 = sol(t)
        yt, l = y
        a, b, c, tt = G, g2 ** 2, g3 ** 2, yt ** 2
        return [K * yt * (9 / 2 * tt - 17 / 12 * a - 9 / 4 * b - 8 * c) - fy * yt,
                K * (24 * l ** 2 + l * (12 * tt - 9 * b - 3 * a) - 6 * tt ** 2 + 9 / 8 * b ** 2 + 3 / 4 * a * b + 3 / 8 * a ** 2) + flam * l]
    F = fy / K
    g2T, g3T = sol(T)
    tt = (F + 17 / 12 * G + 9 / 4 * g2T ** 2 + 8 * g3T ** 2) * 2 / 9
    a, b = G, g2T ** 2
    A_, B_, C_ = K * 24, K * (12 * tt - 9 * b - 3 * a) + flam, K * (-6 * tt ** 2 + 9 / 8 * b ** 2 + 3 / 4 * a * b + 3 / 8 * a ** 2)
    disc = B_ ** 2 - 4 * A_ * C_
    if disc < 0:
        return None
    l0 = (-B_ + math.sqrt(disc)) / (2 * A_)
    s = solve_ivp(rhs, (T, 0), [math.sqrt(tt), l0], rtol=1e-10, atol=1e-13, method="DOP853")
    if not s.success:
        return None
    return dict(lam=float(s.y[1, -1]), yt=float(s.y[0, -1]), lam_uv=l0, t_uv=tt)


def mh_from(lmp, mt, kt):
    return float(brentq(lambda mh: low_to(mt, kt, mh)[4] - lmp, 90, 200, xtol=1e-3))


out = {}
y0, G, fg, gs, fy = fit_fy(MT0, 1e19, 400)
out["fits"] = dict(f_g=fg, f_y=fy, yt_kt=y0[3], lam_kt_measured=y0[4])
# the target point of matter_scan
h = lambda L: -(fg / f_g_EH(L)) * f_y_EH(L) - fy
grid = np.linspace(-6, -0.5, 1200)
roots = [brentq(h, a, b) for a, b in zip(grid, grid[1:]) if h(a) * h(b) < 0]
Lt = roots[0]
Gt = fg / f_g_EH(Lt)
flam_t = Gt * f_l_EH(Lt)
out["target"] = dict(n_roots=len(roots), G=Gt, Lambda=Lt, f_lam=flam_t)
scan = []
for fl in (0.002, 0.005, 0.008, 0.01, 0.012, flam_t, 0.015, 0.02, 0.03, 0.05, 0.1, 0.3, 1.0):
    r = lam_traj(fl, G, fg, gs, fy, 400)
    if r is None:
        scan.append(dict(f_lam=fl, status="no real UV fixed point"))
        continue
    scan.append(dict(f_lam=fl, lam_MP=r["lam"], MH=mh_from(r["lam"], MT0, 1e19), yt_check=r["yt"], lam_uv=r["lam_uv"]))
out["scan"] = scan
print(json.dumps(out, default=float)[:1800], flush=True)
tests = []
for label, mt, kt, T in (("base", MT0, 1e19, 400), ("T=800", MT0, 1e19, 800), ("T=2000", MT0, 1e19, 2000), ("Mt=172.0", 172.0, 1e19, 400), ("Mt=173.1", 173.1, 1e19, 400), ("Mt=171.04", 171.04, 1e19, 400), ("k=1e18", MT0, 1e18, 400), ("k=2.4e18", MT0, 2.4e18, 400), ("k=1.22e19", MT0, 1.22e19, 400), ("k=1e20", MT0, 1e20, 400)):
    y_, G_, fg_, gs_, fy_ = fit_fy(mt, kt, T)
    h_ = lambda L: -(fg_ / f_g_EH(L)) * f_y_EH(L) - fy_
    rt = [brentq(h_, a, b) for a, b in zip(grid, grid[1:]) if h_(a) * h_(b) < 0]
    Lt_ = rt[0]
    Gt_ = fg_ / f_g_EH(Lt_)
    fl_ = Gt_ * f_l_EH(Lt_)
    r = lam_traj(fl_, G_, fg_, gs_, fy_, T)
    rec = dict(label=label, Mt=mt, k=kt, G=Gt_, Lam=Lt_, f_lam=fl_, lam_MP=None if r is None else r["lam"], MH=None if r is None else mh_from(r["lam"], mt, kt))
    tests.append(rec)
    print({a: (round(b, 4) if isinstance(b, float) else b) for a, b in rec.items()}, flush=True)
out["robustness"] = tests
json.dump(out, open("higgs_trajectory.json", "w"), indent=1, default=float)
