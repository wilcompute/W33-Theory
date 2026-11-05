"""GUT thresholds for the PQ-assisted models: how robust is "one of 85 above Super-K"?
Embedding: non-SUSY SU(5) with 24_H and 5_H.  Model A's light quarks are fragments of vectorlike 5 + 10 + 10 of SU(5); their partners are heavy near M_V = mass of X, Y.  Heavy states, with one-loop coefficients Db (same normalisation as pq_twoloop: Dirac 4/3 S, complex scalar 1/3 S, real scalar 1/6 S):
  24_H: (8,1,0) real, (1,3,0) real.  5_H: (3,1,-1/3) complex scalar triplet.
  partners: from 5: (1,2,-1/2) Dirac.  From each 10: (3,1,2/3) [the conjugate fragment] and (1,1,1) Dirac.
X, Y vectors at M_V are the matching scale.  At mu = M_V: alpha_i^-1(M_V-) + sum_h Db_i^h ln(M_h/M_V)/(2 pi) = alpha_U^-1, where the sum is the heavy spectrum's threshold: states heavier than M_V add with ln > 0.
Draw each heavy mass ratio r_h = M_h/M_V log-uniformly in [1/10, 10] (and [1/3, 3]), linearise the two crossing conditions in (ln M_X, ln M_V) around the two-loop solution, solve, and get tau.  Proton: tau = 1.6e36 (M_V/1e16)^4 (35 alpha_U)^-2 yr, the X, Y estimate; triplet-scalar mediated decay suppressed by light Yukawas is not included.
Same for B, C and the single-Q set, whose partners are from one 10.
Control: all r = 1 returns the two-loop numbers.
usage: py -3 pq_gut_thresholds.py"""
import json
import math
import numpy as np

src = open("pq_twoloop.py", encoding="utf-8").read().split("out = {}")[0]
g = {}
exec(src, g)
run, solve2, tau, weyl = g["run"], g["solve2"], g["tau"], g["weyl"]


def db_rep(c, w, y, kind):
    S = np.array([0.6 * y * y * c * w, g["Tw"][w] * c, g["Tc"][c] * w])
    f = dict(dirac=4 / 3, complex=1 / 3, real=1 / 6)[kind]
    return f * S


HEAVY_COMMON = [((8, 1, 0.0), "real"), ((1, 3, 0.0), "real"), ((3, 1, -1 / 3), "complex")]
PARTNERS = {"A": [((1, 2, -0.5), "dirac"), ((3, 1, 2 / 3), "dirac"), ((1, 1, 1.0), "dirac"), ((3, 1, 2 / 3), "dirac"), ((1, 1, 1.0), "dirac")],
            "B": [((1, 2, 0.5), "dirac"), ((3, 1, 2 / 3), "dirac"), ((1, 1, 1.0), "dirac"), ((3, 1, 2 / 3), "dirac"), ((1, 1, 1.0), "dirac")],
            "Q": [((3, 1, 2 / 3), "dirac"), ((1, 1, 1.0), "dirac")]}
LIGHT = {"A": [(3, 1, -1 / 3), (3, 2, 1 / 6), (3, 2, 1 / 6)], "B": [(3, 1, 2 / 3), (3, 2, 1 / 6), (3, 2, 1 / 6)], "Q": [(3, 2, 1 / 6)]}
X0 = {"A": [math.log(2.73e10), math.log(3.96e15)], "B": [math.log(1.68e9), math.log(2.69e15)], "Q": [math.log(2.12e7), math.log(1.32e15)]}
rng = np.random.default_rng(20261105)
out = {}
for name in ("A", "B", "Q"):
    light = LIGHT[name]
    base = solve2(light, x0=X0[name])
    x0 = np.array([math.log(base["MX"]), math.log(base["MU"])])

    def F(x):
        a = run(light, [1.0] * len(light), x[0], x[1])
        return np.array([a[0] - a[1], a[1] - a[2]]), a

    f0, a0 = F(x0)
    J = np.zeros((2, 2))
    for k in range(2):
        dx = np.zeros(2)
        dx[k] = 1e-3
        J[:, k] = (F(x0 + dx)[0] - F(x0 - dx)[0]) / 2e-3
    heavy = HEAVY_COMMON + PARTNERS[name]
    dbs = np.array([db_rep(*h[0], h[1]) for h in heavy])
    res = {}
    for span in (3.0, 10.0):
        taus, mvs = [], []
        for _ in range(20000):
            lr = rng.uniform(-math.log(span), math.log(span), len(heavy))
            th = (dbs * lr[:, None]).sum(0) / (2 * math.pi)  # added to alpha_i^-1 at M_V
            dth = np.array([th[0] - th[1], th[1] - th[2]])
            dx = -np.linalg.solve(J, dth)
            x = x0 + dx
            ia = float(np.mean(a0 + th))
            if x[0] >= x[1]:
                continue
            taus.append(tau(math.exp(x[1]), ia))
            mvs.append(math.exp(x[1]))
        t = np.array(taus)
        res[f"span{span:g}"] = dict(n=len(t), frac_above_SK=float(np.mean(t > 2.4e34)), frac_above_HK=float(np.mean(t > 1e35)), tau_q=[float(q) for q in np.quantile(t, [0.05, 0.16, 0.5, 0.84, 0.95])], MV_q=[float(q) for q in np.quantile(mvs, [0.16, 0.5, 0.84])])
    res["base"] = dict(MX=base["MX"], MU=base["MU"], tau=tau(base["MU"], base["inv_alpha_U"]))
    res["control_zero_threshold"] = float(np.max(np.abs(f0)))
    out[name] = res
    print(name, "base tau %.2g" % res["base"]["tau"], {k: (round(v["frac_above_SK"], 3), round(v["frac_above_HK"], 3), ["%.2g" % q for q in v["tau_q"]]) for k, v in res.items() if k.startswith("span")}, flush=True)
json.dump(out, open("pq_gut_thresholds.json", "w"), indent=1, default=float)
