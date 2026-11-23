"""Pass 12723 add-on (exploration): is y' ~ 1/2 an attractor?
 For a TeV vectorlike Q + T(U) (M_VL = 1.74 TeV, one-loop threshold of Pass 12707), the y' that makes lambda(mu_match) = 0, scanned over
 mu_match = 1e7 - 1e13 GeV, with and without a light vectorlike 5 + 5bar, at M_t = 172.57 and 172.80.  Sensitivity dy'/dlog10(mu).
 Also: the old coincidence lambda = 0 at sqrt(v M_Pl) (Pass 12684, needs M_t = 172.57) against M_t = 172.80 +- 0.26.
usage: py -3 analysis/explore_pass12723_attractor.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3 = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3"))
K = 1 / (16 * math.pi ** 2)
dl_ = lambda y: (5 / 6) * 3 * K * y[5] ** 4 - 2 * y[4] * 3 * K * y[5] ** 2 / 3


def lam_end(yp, tgt, Mt, extra, mvl=1740.0):
    Mt0 = Mt - OFF3; kw = dict(rtol=1e-9, atol=1e-12, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(mvl / Mt0)), np.array(initial(Mt, 125.20, 0.1180) + [yp]), **kw).y[:, -1].copy()
    y[4] += dl_(y)
    def rhs(t, y):
        d = list(beta_vl(*y))
        if extra: d[0] += K * y[0] ** 3 * 10 / 9; d[1] += K * y[1] ** 3 * 2 / 3; d[2] += K * y[2] ** 3 * 2 / 3
        return d
    return solve_ivp(rhs, (math.log(mvl / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1][4]


rows = []
for Mt in (172.57, 172.80):
    for extra in (False, True):
        ys = []
        for lg in np.arange(7, 13.5, 1.0):
            try:
                ys.append((lg, brentq(lambda p: lam_end(p, 10 ** lg, Mt, extra), 0.05, 1.2, xtol=1e-6)))
            except ValueError:
                ys.append((lg, float("nan")))
        good = [(a, b) for a, b in ys if b == b]
        slope = np.polyfit([a for a, _ in good], [b for _, b in good], 1)[0]
        rows.append(dict(Mt=Mt, extra_5=extra, scan=ys, slope_per_decade=float(slope)))
        print(f"M_t {Mt}, light 5+5bar {extra}: y'(log10 mu = 7..13) = {[round(b, 3) for _, b in ys]}; slope {slope:+.4f} per decade")
v, MPf = 246.22, 1.2209e19
P19 = json.load(open(os.path.join(ROOT, "data", "explore_pass12719_web.json")))["top_mass"]["rows"]
mu_new = P19[1]["mu0"]; target = math.sqrt(v * MPf)
z = (172.80 - 172.57) / 0.26
print(f"sqrt(v M_Pl) = {target:.2e} GeV vs mu_0(172.80) = {mu_new:.2e}: the 'lambda = 0 at sqrt(v M_Pl)' coincidence now sits {z:.1f} sigma from the measured M_t "
      f"(it needs 172.57)")
json.dump(dict(rows=rows, coincidence=dict(target=target, mu0_new=mu_new, sigma_off=z)), open(os.path.join(ROOT, "data", "explore_pass12723_attractor.json"), "w"), indent=1)
