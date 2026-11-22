"""Pass 12702 (Claude track): five follow-ups to Pass 12701 on the E6-SUSY + vectorlike-top-partner hybrid and completion A.
 (1) Two-loop gauge running with the vectorlike pair: two-loop coefficients for Weyl fermions from the general formula
     B_ij += kappa [4 S_i(F) C2_j(F) + (20/3) C2(G_i) S_i(F) delta_ij], kappa = 1/2 per Weyl fermion (validated against the SM
     fermion part of B_ij); y' -> mu_0 map with M_t and alpha_s variations.
 (2) E6 obstruction: with renormalizable 27bar.27.(1 + 78) masses, the SM-unique components Q, u^c, e^c of the 27 get masses affine
     in hypercharge, so a light Q + U forces a light e^c (complete 10 + 10bar, no unification repair).  Count of SM-invariant mass
     parameters: 17 for a 27 + 27bar pair, at most 1 + 5 from 1 + 78.  Applied to the other track's F/D-flat branch (7af60ca6b).
 (3) Leptogenesis for A: radiative resonant leptogenesis (exact degeneracy at a high scale, splitting from Yukawa running) lands at
     Delta M / Gamma ~ ln(Lambda/M)/pi automatically; pseudo-Dirac (approximate lepton number) degeneracy raises the Vissani term by M/Delta M.
 (4) Top-partner masses above the LHC limit (1.74 TeV prompt): unification quality, y' needed for mu_0 = 1e10, proton lifetime.
 (5) Proton decay channels: d=6 e+ pi0 vs Hyper-K; d=5 K+ nubar suppressed by (M_SS / 1 TeV)^2 in high-scale SUSY.
usage: py -3 analysis/toe_pass12702_round.py"""
import json, math, os
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G85 = {"__name__": "x", "__file__": os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py")}
exec(open(os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py"), encoding="utf-8").read().split("res = {}")[0], G85)
mu0 = G85["mu0"]
K = 1 / (16 * math.pi ** 2)
res = {}

# (1) two-loop coefficients ---------------------------------------------------------------------------------------
T3 = {1: 0, 3: 0.5, 8: 3.0}; T2 = {1: 0, 2: 0.5, 3: 2.0}; C3 = {1: 0, 3: 4 / 3, 8: 3.0}; C2d = {1: 0, 2: 0.75, 3: 2.0}
CG = np.array([0.0, 2.0, 3.0])


def weyl(d3, d2, Y):
    S = np.array([0.6 * Y * Y * d3 * d2, T2[d2] * d3, T3[d3] * d2])
    C = np.array([0.6 * Y * Y, C2d[d2], C3[d3]])
    b1 = 2 / 3 * S
    B = 0.5 * (4 * np.outer(S, C) + 20 / 3 * np.diag(CG * S))
    return b1, B


GEN = [(3, 2, 1 / 6), (3, 1, 2 / 3), (3, 1, 1 / 3), (1, 2, 1 / 2), (1, 1, 1)]
Bf = 3 * sum(weyl(*f)[1] for f in GEN)
BSM = np.array([[199 / 50, 27 / 10, 44 / 5], [9 / 10, 35 / 6, 12], [11 / 10, 9 / 2, -26]])
BH = np.array([[9 / 50, 9 / 10, 0], [3 / 10, 13 / 6, 0], [0, 0, 0]]); Bgauge = np.diag([0, -136 / 3, -102])
assert np.allclose(Bf + BH + Bgauge, BSM), Bf + BH + Bgauge
print("(1) two-loop Weyl formula reproduces the SM B_ij (fermions + Higgs + gauge)")
bQ, BQ = weyl(3, 2, 1 / 6); bU, BU = weyl(3, 1, 2 / 3)
dbVL, dBVL = 2 * (bQ + bU), 2 * (BQ + BU)            # Dirac pairs Q + Qbar, U + Ubar
AINV = np.array([59.01, 29.59, 8.47]); MZ = 91.1876
B1 = dict(SM=np.array([41 / 10, -19 / 6, -7.0]), MSSM=np.array([33 / 5, 1.0, -3.0]))
BIJ = dict(SM=BSM, MSSM=np.array([[199 / 25, 27 / 5, 88 / 5], [9 / 5, 25, 24], [11 / 5, 9, 14]]))
DU = dict(SM=np.array([17 / 10, 3 / 2, 2]), MSSM=np.array([26 / 5, 6, 4]))
CU = dict(SM=np.array([17 / 20, 9 / 4, 8]), MSSM=np.array([13 / 15, 3, 16 / 3])); YC = dict(SM=4.5, MSSM=6.0)


def unify2(MX, yp, MSS=1e10, tanb=1.0, vl=True):
    segs = [("SM", MZ, False), ("SM", MX, vl), ("MSSM", MSS, vl)]
    g = list(np.sqrt(4 * math.pi / AINV)); y = 0.97; mu = MZ
    for i, (th, ms, on) in enumerate(segs):
        if i == 2: y = y / math.sin(math.atan(tanb))
        mend = segs[i + 1][1] if i + 1 < len(segs) else 1e19
        b = B1[th] + (dbVL * (1.5 if th == "MSSM" else 1.0) if on else 0)
        Bm = BIJ[th] + (dBVL * (1.5 if th == "MSSM" else 1.0) if on else 0)

        def f(t, z, b=b, Bm=Bm, th=th, on=on):
            gg, yy = z[:3], z[3]; g2 = gg ** 2
            dg = K * gg ** 3 * b + K * K * gg ** 3 * (Bm @ g2 - DU[th] * (yy ** 2 + (yp ** 2 if on else 0)))
            return list(dg) + [K * yy * (YC[th] * yy ** 2 - CU[th] @ g2)]

        ev = lambda t, z: z[0] - z[1]; ev.terminal = True
        s = solve_ivp(f, (math.log(mu), math.log(mend)), g + [y], events=ev, rtol=1e-9, atol=1e-12, dense_output=True)
        if s.t_events[0].size:
            z = s.sol(s.t_events[0][0]); ai = 4 * math.pi / z[:3] ** 2
            return math.exp(s.t_events[0][0]), float(ai[0]), float(ai[2] - ai[0])
        g = list(s.y[:3, -1]); y = s.y[3, -1]; mu = mend


def tau_p(M, ai): return 4.7e34 * (M / 1e16) ** 4 * (ai / 25) ** 2


def yp_for(MX, target=10.0, Mt=172.57, a3=0.1180):
    f = lambda yp: math.log10(min(mu0(Mt, a3=a3, vl=(MX, yp)), 1e30)) - target
    lo, hi = 0.25, 0.8
    return brentq(f, lo, hi, xtol=2e-4) if f(lo) > 0 > f(hi) else None


hyb = {}
for MX in (1.0e3, 1.74e3, 2.5e3, 4.0e3, 1e4):
    yp = yp_for(MX)
    M, ai, d = unify2(MX, yp or 0.5)
    hyb[f"{MX:g}"] = dict(M_VL=MX, yprime_mu0_1e10=yp, M12=M, a_inv=ai, delta_two_loop=d, tau_p=tau_p(M, ai))
    print(f"(1/4) VL Q+U at {MX / 1e3:.2f} TeV: y' = {yp:.3f} for mu_0 = 1e10; two-loop M12 {M:.2e}, alpha^-1 {ai:.1f}, "
          f"delta {d:+.2f}, tau_p ~ {tau_p(M, ai):.1e} yr")
ref = unify2(1e3, 0.0, vl=False)
print(f"(1) reference: high-scale SUSY 1e10 without VL, two-loop delta {ref[2]:+.2f}")
# y' map width at 1.74 TeV
band = {}
for lab, kw, tgt in (("mu0=1e9", {}, 9.0), ("mu0=1e11", {}, 11.0), ("Mt-0.3", dict(Mt=172.27), 10.0), ("Mt+0.3", dict(Mt=172.87), 10.0),
                     ("as-0.0009", dict(a3=0.1171), 10.0), ("as+0.0009", dict(a3=0.1189), 10.0)):
    band[lab] = yp_for(1.74e3, target=tgt, **kw)
    print(f"(1) y' at 1.74 TeV, {lab}: {band[lab]:.3f}")
res["hybrid"] = dict(rows=hyb, no_VL_delta=ref[2], yprime_band_174=band,
                     note="two-loop gauge with VL Weyl formula; lambda running two-loop SM + one-loop VL; above M_SS VL superfields scaled 1.5x")

# (2) E6 obstruction -----------------------------------------------------------------------------------------------
comp = {  # (Y, chi, psi) for the 27 under SM x U(1)_chi x U(1)_psi; 27 = 16_1 + 10_-2 + 1_4, 16 = 10_-1 + 5bar_3 + 1_-5, 10 = 5_2 + 5bar_-2
    "Q": (sp.Rational(1, 6), -1, 1), "u^c": (sp.Rational(-2, 3), -1, 1), "e^c": (1, -1, 1),
    "d^c": (sp.Rational(1, 3), 3, 1), "L": (sp.Rational(-1, 2), 3, 1), "nu^c": (0, -5, 1),
    "D": (sp.Rational(-1, 3), 2, -2), "H_u": (sp.Rational(1, 2), 2, -2), "Dbar": (sp.Rational(1, 3), -2, -2), "H_d": (sp.Rational(-1, 2), -2, -2),
    "S": (0, 0, 4)}
Mrow = sp.Matrix([[1, *comp[k]] for k in ("Q", "u^c", "e^c")])
rank = Mrow.rank()
m, cY, cX, cP = sp.symbols("m cY cX cP")
sol = sp.solve([m + cY * comp[k][0] + cX * comp[k][1] + cP * comp[k][2] for k in ("Q", "u^c")], [m, cY], dict=True)[0]
me = sp.simplify((m + cY * comp["e^c"][0] + cX * comp["e^c"][1] + cP * comp["e^c"][2]).subs(sol))
print(f"(2) rows (1, Y, chi, psi) of Q, u^c, e^c have rank {rank}; Q = u^c = 0 forces m(e^c) = {me}")
# SM-invariant mass parameters of a 27 + 27bar pair: same-SM-rep blocks
blocks = {"Q": 1, "u^c": 1, "e^c": 1, "D": 1, "H_u": 1, "(d^c, Dbar)": 4, "(L, H_d)": 4, "(nu^c, S)": 4}
nmass = sum(blocks.values())
print(f"(2) SM-invariant 27bar.27 mass parameters: {nmass}; singlet + 78 supply at most 1 + 5 (Y, chi, psi, 16/16bar singlets) -> "
      f"a 650 (27bar x 27 = 1 + 78 + 650) or non-renormalizable operators are needed for a light Q + U alone")
other = {"adjoint direction": "U(1)_psi (a = -m/(4 lambda))", "16": "3m/4", "10": "3m/2", "1": "0"}
res["e6_obstruction"] = dict(rank_QUE_rows=int(rank), m_ec_when_Q_U_massless=str(me), n_SM_mass_parameters=nmass, max_from_1_plus_78=6,
                             other_track_branch=other, conclusion="renormalizable 27bar.27.(1+78) masses cannot leave Q+U light without e^c; "
                             "the F/D-flat branch of 7af60ca6b keeps complete SO(10) multiplets (16: 3m/4, 10: 3m/2, singlet massless)")

# (3) radiative resonant leptogenesis -------------------------------------------------------------------------------
lep = {}
for lab, Lam in (("Lambda = f_a = 1e11", 1e11), ("Lambda = M_GUT = 2e16", 2e16), ("Lambda = M_Pl", 2.4e18)):
    M = 1.24e7; L = math.log(Lam / M); r = L / math.pi
    eps_max = 0.5 * r / (r * r + 0.25)
    lep[lab] = dict(log=L, dM_over_Gamma=r, eps_over_sinphi=eps_max, sinphi_needed=(1.5e-6 / eps_max, 1.2e-5 / eps_max))
    print(f"(3) radiative splitting, {lab}: Delta M/Gamma ~ {r:.1f}, eps ~ {eps_max:.2f} sin(phi); needed sin(phi) ~ "
          f"{1.5e-6 / eps_max:.0e}-{1.2e-5 / eps_max:.0e}")
y2 = 0.05e-9 * 1.24e7 / 174.0 ** 2
print(f"(3) seesaw Yukawa y^2 ~ {y2:.1e}: Gamma/M = {y2 / (8 * math.pi):.1e}, Delta M/M ~ {y2 / (8 * math.pi) * lep['Lambda = f_a = 1e11']['dM_over_Gamma']:.0e}; "
      f"pseudo-Dirac (approximate L) instead multiplies the Vissani Delta by M/Delta M ~ 1e4 -> Delta ~ 1e5")
res["leptogenesis_radiative"] = dict(rows=lep, y2=y2, pseudo_dirac_penalty="Delta x M/DeltaM",
                                     note="Delta M/Gamma = ln(Lambda/M)/pi x O(1) Yukawa-structure factor; order of magnitude")

# (5) proton channels ------------------------------------------------------------------------------------------------
best = hyb["1740"]
res["proton"] = dict(e_pi0_years=best["tau_p"], hyperK_10yr_90CL=7.8e34, superK=2.4e34, d5_suppression=(1e10 / 1e3) ** 2,
                     note="high-scale SUSY: d=5 K+ nubar amplitude ~ 1/M_SS -> rate x (1 TeV/M_SS)^2 ~ 1e-14 vs TeV SUSY; e+ pi0 is the channel")
print(f"(5) hybrid at 1.74 TeV: tau(e+ pi0) ~ {best['tau_p']:.1e} yr vs Hyper-K 10-yr 7.8e34; d=5 K+ nubar suppressed by ~1e14")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12702_round.json"), "w"), indent=1, default=float)
print("wrote data/toe_pass12702_round.json")
