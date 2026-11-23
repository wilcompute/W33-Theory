"""Pass 12714 add-on: if the hybrid's vectorlike Q + U are pseudo-Goldstone fermions with M_VL ~ c M_SS^2 / M_GUT, the TeV floor fixes M_SS;
y' of the hybrid then follows from lambda(M_SS) = 0 (tan beta ~ 1 matching), with the Pass 12707 one-loop threshold at M_VL.
usage: py -3 analysis/explore_pass12714_mss.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3 = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3"))
K = 1 / (16 * math.pi ** 2); MT, A3, MGUT = 172.57, 0.1180, 4.1e16
dl = lambda y: (5 / 6) * 3 * K * y[5] ** 4 - 2 * y[4] * 3 * K * y[5] ** 2 / 3


def lam_end(yp, tgt, MVL):
    Mt0 = MT - OFF3; kw = dict(rtol=1e-9, atol=1e-12, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(MVL / Mt0)), np.array(initial(MT, 125.20, A3) + [yp]), **kw).y[:, -1].copy()
    y[4] += dl(y)
    return solve_ivp(lambda t, y: beta_vl(*y), (math.log(MVL / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1][4]


rows = []
for c in (0.3, 1.0, 3.0):
    for MVL in (1740.0, 3000.0):
        MSS = math.sqrt(MVL * MGUT / c)
        yp = brentq(lambda p: lam_end(p, MSS, MVL), 0.2, 1.0, xtol=1e-6)
        rows.append(dict(c=c, M_VL=MVL, M_SS=MSS, y_hybrid=yp))
        print(f"c = {c}: M_VL = {MVL / 1e3:.2f} TeV -> M_SS = {MSS:.2e} GeV -> hybrid y' = {yp:.4f}")
json.dump(rows, open(os.path.join(ROOT, "data", "explore_pass12714_mss.json"), "w"), indent=1)
