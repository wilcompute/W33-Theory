"""Item 4: the orbifold Model A with two-loop running below 1/R and the brane kinetic terms that orbifold_gut.py neglected.
Below 1/R: the two-loop machinery of pq_twoloop.py (SM + Model A fragments above M_X).  Above 1/R: KK towers at one loop as in orbifold_gut.py up to Lambda.  At Lambda: alpha_i^-1(Lambda) + delta_i = alpha_U^-1, where delta_i are the brane kinetic terms (non-universal part matters).  Unknowns: M_X and 1/R for given Lambda R and delta.
Report: Lambda R = 3 and 10 with delta = 0; then the sensitivity d ln M_X / d delta_i and d ln(1/R) / d delta_i, and the size of non-universal brane terms that keeps M_X in the PQ window 1e9 to 2e11 and 1/R high enough for the proton (tau > 2.4e34 with matter on the SU(5) brane).
usage: py -3 orbifold_twoloop.py"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

src = open("pq_twoloop.py", encoding="utf-8").read().split("out = {}")[0]
g = {}
exec(src, g)
run2, tau = g["run"], g["tau"]
src2 = open("orbifold_gut.py", encoding="utf-8").read().split("def ainv_at")[0]
g2 = {}
exec(src2, g2)
towers, DQ, B_SM = g2["towers"], g2["DQ"], g2["B_SM"]
LIGHT = [(3, 1, -1 / 3), (3, 2, 1 / 6), (3, 2, 1 / 6)]


def ainv(lnMX, invR, LR, delta):
    a = run2(LIGHT, [1.0] * 3, lnMX, math.log(invR))  # two loops to 1/R
    mu = LR * invR
    a = a - (B_SM + DQ) * math.log(mu / invR) / (2 * math.pi)  # zero modes above 1/R, one loop
    for b, typ in towers:
        m = (2 if typ == "pp" else 1) * invR
        while m < mu:
            a = a - b * math.log(mu / m) / (2 * math.pi)
            m += 2 * invR
    return a + np.array(delta)


def solve(LR, delta, x0):
    f = lambda x: [ainv(x[0], math.exp(x[1]), LR, delta)[0] - ainv(x[0], math.exp(x[1]), LR, delta)[1], ainv(x[0], math.exp(x[1]), LR, delta)[1] - ainv(x[0], math.exp(x[1]), LR, delta)[2]]
    s = root(f, x0, tol=1e-9)
    if not s.success:
        return None
    a = ainv(s.x[0], math.exp(s.x[1]), LR, delta)
    return dict(MX=math.exp(s.x[0]), invR=math.exp(s.x[1]), inv_alpha=float(a.mean()), tau=tau(math.exp(s.x[1]), float(a.mean())))


out = {}
x0 = [math.log(2.7e10), math.log(5e15)]
for LR in (1.0, 3.0, 10.0):
    r = solve(LR, [0, 0, 0], x0)
    out[f"LR{LR:g}"] = r
    print("Lambda R", LR, r, flush=True)
    if r:
        x0 = [math.log(r["MX"]), math.log(r["invR"])]
# sensitivity at Lambda R = 3
base = out["LR3"]
x0 = [math.log(base["MX"]), math.log(base["invR"])]
sens = {}
for i, name in enumerate(("delta1", "delta2", "delta3")):
    d = [0.0, 0.0, 0.0]
    d[i] = 0.5
    r = solve(3.0, d, x0)
    sens[name] = dict(dlnMX=math.log(r["MX"] / base["MX"]) / 0.5, dlninvR=math.log(r["invR"] / base["invR"]) / 0.5)
out["sensitivity_per_unit_delta"] = sens
print("sensitivity", sens, flush=True)
# random non-universal brane terms of size s
rng = np.random.default_rng(3)
band = {}
for s in (0.5, 1.0, 2.0, 4.0):
    mx, tv = [], []
    for _ in range(400):
        d = rng.uniform(-s, s, 3)
        dlnMX = sum(sens[f"delta{i + 1}"]["dlnMX"] * d[i] for i in range(3))
        dlnR = sum(sens[f"delta{i + 1}"]["dlninvR"] * d[i] for i in range(3))
        MXv = base["MX"] * math.exp(dlnMX)
        R = base["invR"] * math.exp(dlnR)
        mx.append(MXv)
        tv.append(tau(R, base["inv_alpha"]))
    mx, tv = np.array(mx), np.array(tv)
    band[str(s)] = dict(MX_q=[float(q) for q in np.quantile(mx, [0.16, 0.5, 0.84])], frac_MX_window=float(np.mean((mx > 1e9) & (mx < 2e11))), frac_tau_SK=float(np.mean(tv > 2.4e34)))
    print("brane terms +-", s, band[str(s)], flush=True)
out["brane_band"] = band
json.dump(out, open("orbifold_twoloop.json", "w"), indent=1, default=float)
