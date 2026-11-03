"""Does anything here single out three generations?  A toy: keep the measured couplings at M_t, keep the third-generation Yukawa and the Higgs, and change the number of light chiral generations from M_t upward (Delta b_Y = 20/9, Delta b_2 = Delta b_3 = 4/3 per generation at one loop).  Extra generations are massless, which is excluded by Higgs data, so this tests the UV constraints only and not viability.  For N_g = 0..8: QCD and SU(2) asymptotic freedom; whether g_Y hits a Landau pole below M_Pl; lambda(M_Pl); and the Dona-Eichhorn-Percacci positivity bound N_D < 23 + 2 N_V - N_S/2 (scheme II), N_D < 11 + 2 N_V - N_S/2 (scheme Ia), with and without nu_R.  Lower bound from CP violation: N_g >= 3 (Kobayashi-Maskawa).  usage: py -3 ngen_scan.py"""
import json
import math
from scipy.integrate import solve_ivp
from sm_rge import K, beta_sm, matching

m = matching(172.57, 125.20, 0.1180, 80.369)
y0 = [m["gY"], m["g2"], m["g3"], m["yt"], m["lam"], 0.0155, 0.0100]


def run_ng(ng, top=1e19):
    d = ng - 3
    def rhs(t, y):
        b = beta_sm(y, 2)
        b[0] += K * y[0] ** 3 * (20 / 9) * d
        b[1] += K * y[1] ** 3 * (4 / 3) * d
        b[2] += K * y[2] ** 3 * (4 / 3) * d
        return b
    ev = lambda t, y: max(abs(v) for v in y[:5]) - 6.0
    ev.terminal = True
    s = solve_ivp(rhs, (math.log(172.57), math.log(top)), y0, rtol=1e-9, atol=1e-12, events=ev, method="LSODA")
    pole = None if s.status != 1 else math.exp(s.t[-1])
    return s.y[:, -1], pole


rows = []
for ng in range(0, 9):
    y, pole = run_ng(ng)
    b3, b2 = -11 + 4 / 3 * ng, -22 / 3 + 1 / 6 + 4 / 3 * ng
    Nd, Nd_nu = 7.5 * ng, 8 * ng
    rows.append(dict(N_g=ng, b3=b3, b2=b2, QCD_AF=b3 < 0, SU2_AF=b2 < 0, nonperturbative_below_1e19_at=pole, gY=float(y[0]), g2=float(y[1]), g3=float(y[2]), lam_at_top=float(y[4]) if pole is None else None,
                     dona_II=Nd < 23 + 24 - 2, dona_II_nuR=Nd_nu < 23 + 24 - 2, dona_Ia=Nd < 11 + 24 - 2, dona_Ia_nuR=Nd_nu < 11 + 24 - 2, CP_violation_allowed=ng >= 3))
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rows[-1].items() if k not in ("b2", "b3")}, flush=True)
allowed = [r["N_g"] for r in rows if r["QCD_AF"] and r["SU2_AF"] and r["CP_violation_allowed"] and r["dona_II"] and r["nonperturbative_below_1e19_at"] is None]
out = dict(rows=rows, allowed_by_all=allowed)
print(allowed)
json.dump(out, open("ngen_scan.json", "w"), indent=1, default=float)
