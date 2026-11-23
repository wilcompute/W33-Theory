"""Pass 12719 web-driven add-ons.
 (6) New top-mass input: Ball et al. (arXiv:2603.28865, March 2026) global fit with toponium corrections, M_t(pole) = 172.80 +- 0.26 GeV.
     mu_0, P(absolute stability) (M_t^c = 170.98 at alpha_s 0.1180, Pass 12709), y'_B' (flat R = 0.088 um, mediator gauge shift) and
     y'_hybrid (M_SS = 8.45e9, gauge mediation) at 172.57 vs 172.80.
 (7) DESI DR2 (w0 ~ -0.84) vs a rolling dark-dimension radius: if rho_DE ~ R^-4 (Lambda^(1/4) = lambda m_KK) and M5 is fixed in Standard-Model
     units (SM on a brane, m_p set by Lambda_QCD), then G m_p^2 ~ 1/R and |d ln G/dt| = (3/4)|1 + w0| H0.  Lunar laser ranging
     (Hofmann & Mueller 2018): dG/dt / G = (7.1 +- 7.6) x 1e-14 per year.
usage: py -3 analysis/explore_pass12719_web.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
K = 1 / (16 * math.pi ** 2)
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3, M5f = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3", "M5"))
dl_ = lambda y: (5 / 6) * 3 * K * y[5] ** 4 - 2 * y[4] * 3 * K * y[5] ** 2 / 3
res = {}


def mu0(Mt):
    Mt0 = Mt - OFF3
    s = solve_ivp(lambda t, y: beta_sm(*y), (0, math.log(2.4e18 / Mt0)), initial(Mt, 125.20, 0.1180), rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.5)
    ts = np.linspace(0, s.t[-1], 3000); lam = s.sol(ts)[4]; j = np.where(lam < 0)[0][0]
    return Mt0 * math.exp(brentq(lambda t: s.sol(t)[4], ts[j - 1], ts[j]))


def lam_end(yp, tgt, Mt, mvl=1740.0, withY=False):
    Mt0 = Mt - OFF3; kw = dict(rtol=1e-9, atol=1e-12, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(mvl / Mt0)), np.array(initial(Mt, 125.20, 0.1180) + [yp]), **kw).y[:, -1].copy()
    y[4] += dl_(y)
    def rhs(t, y):
        d = list(beta_vl(*y))
        if withY and Mt0 * math.exp(t) > 2000.0: d[2] += K * y[2] ** 3 / 6; d[0] += K * y[0] ** 3 / 9
        return d
    return solve_ivp(rhs, (math.log(mvl / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1][4]


rows = []
for Mt, s in ((172.57, math.hypot(0.29, 0.5)), (172.80, math.hypot(0.26, 0.5)), (172.80, 0.26)):
    m0 = mu0(Mt); z = (170.98 - Mt) / math.hypot(s, 0.20)
    yB = brentq(lambda p: lam_end(p, M5f(0.088e-6), Mt, withY=True), 0.2, 1.0, xtol=1e-6)
    yH = brentq(lambda p: lam_end(p, 8.45e9, Mt), 0.2, 1.0, xtol=1e-6)
    rows.append(dict(Mt=Mt, sigma=s, mu0=m0, P_stable=float(norm.cdf(z)), y_Bprime=yB, y_hybrid=yH))
    print(f"(6) M_t = {Mt} +- {s:.2f}: mu_0 = {m0:.2e} GeV, P(absolutely stable) = {norm.cdf(z):.1e}, y'_B'(0.088 um) = {yB:.4f}, y'_hybrid(c=1) = {yH:.4f}")
res["top_mass"] = dict(rows=rows, source="Ball et al. arXiv:2603.28865 (toponium-corrected global fit), M_t = 172.80 +- 0.26",
                       note="the hybrid's ceiling M_SS <= mu_0 still holds (8.45e9 < mu_0)")

H0 = 70 / 3.0857e19 * 3.156e7                       # per year
llr, llr_s = 7.1e-14, 7.6e-14
de = []
for w0 in (-0.84, -0.95, -0.99, -0.999):
    rate = 0.75 * abs(1 + w0) * H0
    de.append(dict(w0=w0, dlnG_dt=rate, ratio_to_LLR_2sigma=rate / (abs(llr) + 2 * llr_s)))
    print(f"(7) w0 = {w0}: radion-driven dark energy -> |d ln G/dt| = {rate:.1e} /yr = {rate / (abs(llr) + 2 * llr_s):.1f} x the LLR 2-sigma bound")
w_allowed = 1 - (abs(llr) + 2 * llr_s) / (0.75 * H0)
print(f"(7) LLR allows radion-driven dark energy only with 1 + w0 <~ {1 - w_allowed + 0:.1e} ... i.e. w0 >= -1 within {(abs(llr) + 2 * llr_s) / (0.75 * H0):.4f}")
res["desi_radion"] = dict(rows=de, H0_per_year=H0, LLR=(llr, llr_s), max_one_plus_w0=(abs(llr) + 2 * llr_s) / (0.75 * H0),
                          note="DESI-level evolution (1 + w0 ~ 0.16) cannot be carried by the dark-dimension radius if SM masses are fixed in 5D units; "
                               "it must come from another field (e.g. the string-coupling modulus of Anchordoqui et al. 2025) or R must be stabilised")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12719_web.json"), "w"), indent=1)
