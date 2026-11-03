"""Matter content and no-fit predictions, using only PUBLISHED fixed points.  Dona-Eichhorn-Percacci (arXiv:1311.2898) Tables 3 and 4 give G*, Lambda* for matter contents; Eichhorn-Held (arXiv:1707.01107) give f_g, f_y, f_lambda as functions of Lambda and their own point (3.29, -4.51).  Notation of as_fixedpoint.py: f_g = G f_g^EH, f_y = -G f_y^EH, f_lam = G f_lam^EH.
Two treatments of hypercharge: interacting (g_Y(M_Pl) = sqrt(f_g / (K 41/6)), a prediction) and Gaussian (g_Y free, taken from data, as in 1707.01107, so only M_t and M_H are predictions).
The target: the (G*, Lambda*) that would give the observed f_g and f_y.  A first version scanned N_S, N_D, N_V using the perturbative eqs. 37-38, but those give G* = 0.84, Lambda* = -1.5 for the SM against Table 3's 1.76, -2.40, so that scan is not used and the failure is recorded in the report.
usage: py -3 matter_scan.py"""
import json
import math
import numpy as np
from scipy.optimize import brentq

src = open("as_fixedpoint.py", encoding="utf-8").read().split("out = {}\nmain = analyse(1e19)")[0]
exec(src)


def f_y_EH(L):
    return (96 + L * (-235 + L * (103 + 56 * L))) / (12 * math.pi * (3 + 2 * L * (-5 + 4 * L)) ** 2)


def f_l_EH(L):
    return (165 - 8 * L * (61 + L * (-49 + 4 * L))) / (6 * math.pi * (3 + 2 * L * (-5 + 4 * L)) ** 2)


def f_g_EH(L):
    return 5 * (1 - 4 * L) / (18 * math.pi * (1 - 2 * L) ** 2)


y_ref = low_to(MT0, 1e19)
gs_ref = [y_ref[1], y_ref[2]]
G_data = y_ref[0] ** 2


def predict(G_, L, hypercharge):
    fg, fy, fl = G_ * f_g_EH(L), -G_ * f_y_EH(L), G_ * f_l_EH(L)
    r = dict(f_g=fg, f_y=fy, f_lam=fl)
    if hypercharge == "interacting":
        Gp = fg / (K * 41 / 6)
    else:
        Gp = G_data
    r["gY_MP"] = math.sqrt(Gp)
    v = yuk_at_mp(Gp, gs_ref, fy, fg, "B")
    if v is None:
        r["status"] = "no top fixed point (f_y has the wrong sign or size)"
        return r
    yt = float(v[0])
    r["yt_MP"] = yt
    l_mp = lam_at_mp(fl, yt, Gp, gs_ref, fy, fg)
    if l_mp is None:
        r["status"] = "no real lambda fixed point"
        return r
    r["lam_MP"] = l_mp
    try:
        lo = run([r["gY_MP"], y_ref[1], y_ref[2], yt, l_mp, 0.005, 0.005], 1e19, 173.0)
    except (AssertionError, ValueError):
        r["status"] = "running failed"
        return r
    r.update(status="ok", gY_low=lo[0], Mt=173.34 + (lo[3] - 0.93690 + 0.00042 * (A3 - 0.1184) / 0.0007) / 0.00556, MH=125.15 + (lo[4] - 0.12604) / 0.00206)
    return r


models = dict(SM=(1.762, -2.399), SM_3nuR=(2.15, -3.20), SM_dm_scalar=(1.87, -2.50), SM_3nuR_axion_dm=(2.50, -3.62), no_matter=(0.77, 0.01), EH_1707=(3.29, -4.51))
out = {}
out["published_models"] = {k: {h: predict(G_, L, h) for h in ("interacting", "gaussian")} for k, (G_, L) in models.items()}
L0 = brentq(f_y_EH, -4.5, -2.4)
out["Lambda_where_f_y_changes_sign"] = L0
# the target: f_g = 0.0098 and f_y = -4.5e-4
fg_req, fy_req = 0.0098, -4.5e-4
Lt = brentq(lambda L: (fg_req / f_g_EH(L)) * f_y_EH(L) + fy_req, -3.5, L0 + 1e-6) if False else None
# G from f_g, then solve for f_y
h = lambda L: -(fg_req / f_g_EH(L)) * f_y_EH(L) - fy_req
grid = np.linspace(-6, -0.5, 1200)
roots = [brentq(h, a, b) for a, b in zip(grid, grid[1:]) if h(a) * h(b) < 0]
out["target_roots"] = [dict(Lambda=r, G=fg_req / f_g_EH(r)) for r in roots]
out["ratio_G_table_to_target"] = {k: v[0] / (fg_req / f_g_EH(roots[0])) for k, v in models.items()} if roots else None
out["f_lam_at_target"] = [(fg_req / f_g_EH(r)) * f_l_EH(r) for r in roots]
print(json.dumps(out, default=float)[:3400])
json.dump(out, open("matter_scan.json", "w"), indent=1, default=float)
