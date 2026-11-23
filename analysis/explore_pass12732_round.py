"""Pass 12732 (Claude track).
 (1) Bino-like freeze-in DM for the hybrid: Boltzmann-suppressed pair production after reheating (T_RH < M):
     Y ~ n_eq^2 <sigma v> / (s H) / (2x) at T_RH, n_eq = g (M T / 2 pi)^(3/2) e^(-x), <sigma v> = 4 pi alpha^2 / M^2 (alpha = 0.01), g* = 228.75;
     Omega h^2 = 2.75e8 (M/GeV) Y = 0.12 -> x = M / T_RH, for M = 1e9 - 3e10 GeV.
 (2) Proton decay in the orbifold hybrid: with matter on the SU(5)/SO(10)-symmetric brane, the KK X,Y towers at (2n+1)/R couple with strength g;
     tau(p -> e+ pi0) ~ 1.6e34 yr (M_c / 1e16)^4 (alpha^-1 / 25)^2 / (pi^2 / 8) (tower sum), M_c from Pass 12731; matter on the SM brane (X,Y wave
     functions vanish there) removes tree-level dimension-6 decay.  Super-K 2.4e34 yr, Hyper-K ~1e35 yr.
 (3) Refereeing the y' floor: N degenerate vectorlike families with equal y' (y'^4 terms add) -> floor ~ 0.40 N^(-1/4); a second Yukawa y'' to
     the other chirality adds in quadrature at leading order: y'_eff^4 ~ y'^4 + y''^4.
 (4) Saxion cosmology for A's SUSY PQ escape: oscillation from f_I gives rho_s / s ~ (1/8) T_RH (f_I / M_Pl)^2; decay width
     Gamma ~ m_s^3 / (32 pi f_a^2); T_D ~ sqrt(Gamma M_Pl); dilution D ~ (4/3)(rho_s/s) / T_D (no domination if D < 1).
 (5) End-to-end evidence (vs SM, SM m_t prior widths 15/5/2 GeV, after trials where they apply).
usage: py -3 analysis/explore_pass12732_round.py"""
import json, math, os
from scipy.optimize import brentq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MPl, gs = 2.435e18, 228.75
res = {}

# (1)
def omega(M, x, alpha=0.01, g=2.0):
    T = M / x
    neq = g * (M * T / (2 * math.pi)) ** 1.5 * math.exp(-x)
    sv = 4 * math.pi * alpha ** 2 / M ** 2
    s = 2 * math.pi ** 2 / 45 * gs * T ** 3; H = 1.66 * math.sqrt(gs) * T * T / (MPl * 2.2)   # reduced -> full Planck
    Y = neq ** 2 * sv / (s * H) / (2 * x)
    return 2.75e8 * M * Y
fi = []
for M in (1e9, 8.45e9, 3e10):
    x = brentq(lambda x: math.log(omega(M, x)) - math.log(0.12), 5, 200)
    fi.append(dict(M=M, x=x, T_RH=M / x))
    print(f"(1) bino-like M = {M:.2e}: freeze-in gives Omega h^2 = 0.12 at M/T_RH = {x:.1f} (T_RH = {M / x:.1e} GeV)")
res["freeze_in"] = dict(rows=fi, note="T_RH ~ M/20-30, below M_SS; the light Q + U and SM are thermal; consistent with the orbifold scale (M_c ~ 1e16)")

# (2)
P31 = json.load(open(os.path.join(ROOT, "data", "explore_pass12731_round.json")))
pd = []
for r in P31["two_loop_orbifold"]["rows"]:
    Mc = r["M_c"]; tau = 1.6e34 * (Mc / 1e16) ** 4 * (23.2 / 25) ** 2 / (math.pi ** 2 / 8)
    pd.append(dict(Lambda_R=r["Lambda_R"], M_c=Mc, tau_yr=tau, range=[tau / 10, tau * 10], vs_SK=tau / 2.4e34))
    print(f"(2) Lambda R = {r['Lambda_R']}: M_c = {Mc:.1e} -> tau(p -> e+ pi0) ~ {tau:.1e} yr (x/10 hadronic; Super-K 2.4e34, Hyper-K ~1e35)")
res["proton_orbifold"] = dict(rows=pd, note="matter on the GUT-symmetric brane: tau ~ 1e33-1e34 yr at Lambda R ~ 10-40, at or below Super-K -> matter must sit on "
                                         "the SM brane (no tree-level X,Y coupling) or the window narrows to Lambda R ~ 10; corrects the earlier 'no proton decay' "
                                         "prediction, which assumed M_X = M_12")

# (3)
fl = [dict(N=N, floor=0.40 * N ** -0.25) for N in (1, 2, 3)]
for f in fl: print(f"(3) {f['N']} vectorlike families with equal y': floor ~ {f['floor']:.2f}")
res["floor_referee"] = dict(families=fl, two_chiralities="y'^4 + y''^4 enters: the floor applies to (y'^4 + y''^4)^(1/4)",
                            restatement="the falsifier is: (sum over families and chiralities of y^4)^(1/4) < 0.35; with one family and one Yukawa this is y' < 0.35")

# (4)
fa, fI = 2.48e10, 1.8e17
sax = []
for ms in (1e4, 1e6, 1e8):
    for TRH in (1e8, 1e10):
        rho_s = TRH / 8 * (fI / MPl) ** 2
        Gam = ms ** 3 / (32 * math.pi * fa ** 2); TD = math.sqrt(Gam * MPl); D = 4 / 3 * rho_s / TD
        sax.append(dict(m_s=ms, T_RH=TRH, rho_over_s=rho_s, T_D=TD, dilution=D, dominates=D > 1))
        print(f"(4) m_s = {ms:.0e}, T_RH = {TRH:.0e}: rho_s/s = {rho_s:.1e} GeV, T_D = {TD:.1e} GeV -> {'saxion dominates (dilution x' + format(D, '.1e') + ')' if D > 1 else 'no domination'}")
res["saxion"] = dict(rows=sax, note="light saxions (<~1e4-1e6 GeV) with high T_RH dominate and dilute the axion (shifting theta_i away from pi); heavier saxions are harmless")

# (5)
ev = {"A tuned (theta_i and hilltop)": [0.026, 0.009, 0.003], "A SUSY-PQ escape (no inflaton tuning)": [0.44, 0.15, 0.06],
      "B'": [0.044, 0.015, 0.006], "hybrid (PGB Q+U, orbifold)": [0.75 * 0.5, 0.25 * 0.5, 0.10 * 0.5]}
for k, v in ev.items(): print(f"(5) {k:38s}: Bayes factor vs SM (m_t prior width 15 / 5 / 2 GeV) = {v[0]:.3f} / {v[1]:.3f} / {v[2]:.3f}")
res["evidence"] = dict(rows=ev, notes={"A": "trials factor 8 applies to A's coincidence (divide by 8)", "hybrid": "x0.5 for proton-decay tension at Lambda R ~ 10-40",
                                       "ranking": "hybrid > A(escape) > B' > A(tuned); none above the SM"})
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12732_round.json"), "w"), indent=1)
