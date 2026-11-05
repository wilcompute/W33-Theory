"""The axion-mass ceiling for Model A from the measured top mass, replacing my one-loop crossing (about 1e8, too low).
Buttazzo et al, arXiv:1307.3536, eq. (67): log10 Lambda_V/GeV = 9.5 + 0.7 (M_h - 125.15) - 1.0 (M_t - 173.34) + 0.3 (alpha_s - 0.1184)/0.0007, gauge and scheme independent, NNLO.  The same paper: the MSbar scale where lambda vanishes is about 2 Lambda_V.  Threshold stabilisation needs m_rho below that scale, so mu_I = 2 Lambda_V is used, and Lambda_V itself as a conservative variant.
Inputs (PDG-type values from memory, not re-read): M_h = 125.20 +- 0.11, M_t = 172.57 +- 0.29 (direct average), alpha_s = 0.1180 +- 0.0009.  A further +- 0.5 GeV on M_t for the pole-mass interpretation of direct measurements is included as a separate case.
Fine grid in f of the sigma stability bound from pq_gates.py (common y_Q = M_X / f, M_X = 2.73e10), giving m_rho(f); the ceiling is the largest m_a with m_rho < mu_I and y_Q <= 1.
Monte Carlo over inputs gives the distribution of the ceiling, compared with post-inflation simulation windows: 40-180 ueV (talk abstract quoted in Pass 12607), 95-450 ueV (Kaltschmidt et al 2502.02398), 160-270 and 480-520 ueV (Hoof et al, as quoted by the search tool, not read).
usage: py -3 pq_mass_ceiling.py"""
import json
import math
import numpy as np

src = open("pq_gates.py", encoding="utf-8").read().split("rows = []")[0]
g = {}
exec(src, g)
mls = g["min_ls_for_stability"]
fs = np.geomspace(2.73e10, 1e12, 28)
tab = []
for f in fs:
    y = 2.73e10 / f
    ls = mls(y, f)
    tab.append((f, y, 5.7e12 / f, math.sqrt(2 * ls) * f))
tab = np.array(tab)
print("grid m_a vs m_rho", [(round(r[2], 1), "%.2g" % r[3]) for r in tab[::3]], flush=True)
lnmr = np.log(tab[:, 3])
ma = tab[:, 2]


def ceiling(mu):
    """largest m_a with m_rho < mu; m_rho decreases with f, so m_a ceiling is where m_rho crosses mu"""
    if mu >= tab[0, 3]:
        return float(ma[0])  # y = 1 limit
    if mu <= tab[-1, 3]:
        return float(ma[-1])
    return float(np.exp(np.interp(math.log(mu), lnmr[::-1], np.log(ma[::-1]))))


def lamV(mh, mt, a3):
    return 10 ** (9.5 + 0.7 * (mh - 125.15) - 1.0 * (mt - 173.34) + 0.3 * (a3 - 0.1184) / 0.0007)


out = dict(grid=[dict(f=r[0], y=r[1], m_a=r[2], m_rho=r[3]) for r in tab])
c = lamV(125.20, 172.57, 0.1180)
out["central"] = dict(Lambda_V=c, mu_I=2 * c, ceiling_2LV=ceiling(2 * c), ceiling_LV=ceiling(c))
print("central Lambda_V %.3g mu_I %.3g ceiling %.1f ueV (conservative %.1f)" % (c, 2 * c, ceiling(2 * c), ceiling(c)), flush=True)
rng = np.random.default_rng(7)
for lab, smt in (("Mt_0.29", 0.29), ("Mt_0.58", math.hypot(0.29, 0.5))):
    mh = rng.normal(125.20, 0.11, 40000)
    mt = rng.normal(172.57, smt, 40000)
    a3 = rng.normal(0.1180, 0.0009, 40000)
    lv = lamV(mh, mt, a3)
    ce = np.array([ceiling(2 * x) for x in lv[:6000]])
    q = np.quantile(ce, [0.05, 0.16, 0.5, 0.84, 0.95])
    wins = dict(w40_180=float(np.mean(ce >= 40)), w95_450=float(np.mean(ce >= 95)), w160=float(np.mean(ce >= 160)), w480=float(np.mean(ce >= 480)))
    out[lab] = dict(log10_LambdaV_q=[float(x) for x in np.quantile(np.log10(lv), [0.16, 0.5, 0.84])], ceiling_q=[float(x) for x in q], P_ceiling_reaches=wins)
    print(lab, "log10 Lambda_V", np.round(np.quantile(np.log10(lv), [0.16, 0.5, 0.84]), 2), "ceiling ueV", np.round(q, 0), "P(ceiling >= window low end)", {k: round(v, 3) for k, v in wins.items()}, flush=True)
json.dump(out, open("pq_mass_ceiling.json", "w"), indent=1, default=float)
