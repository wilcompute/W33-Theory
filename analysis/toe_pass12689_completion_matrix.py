"""Pass 12689: the two exclusive completions of the Higgs-quartic coincidence (Pass 12688), made concrete.
 (1) Completion B (dark dimension + vectorlike top partner): y'(R) needed for lambda(M_5) = 0 at the LHC-allowed M_VL = 1.65 TeV over
     R = 0.1-30 um, with the 3-loop-QCD-validated running of Pass 12685/12687 (offset form); and the KK-graviton DM initial temperature
     T_i(R) ~ 1 GeV (R / 1 um)^(-1/3) from Omega ~ T_i^3 R / M_Pl (Gonzalo-Montero-Obied-Vafa 2209.09249 scaling).
 (2) Completion A (SMASH-like + extra scalar): mass of the extra scalar s if its coupling kappa ~ 3e-5 to sigma comes with no tuning,
     m_s ~ sqrt(kappa) f_a; KSVZ domain-wall number N_DW = 1 (one heavy quark) and post-inflationary PQ breaking (no isocurvature).
 (3) Prediction matrix A vs B with the experiments that split them.
usage: py -3 analysis/toe_pass12689_completion_matrix.py"""
import json, math, os
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G = {"__name__": "x", "__file__": os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py")}
exec(open(os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py"), encoding="utf-8").read().split("res = {}")[0], G)
mu0, run, MPL = G["mu0"], G["run"], G["MPL"]
GEV_INV_M = 1.97327e-16
res = {}
MVL = 1650.0
yR = []
for R_um in (0.1, 0.3, 1.0, 3.0, 10.0, 30.0):
    R = R_um * 1e-6
    M5 = (MPL ** 2 / (2 * math.pi * R / GEV_INV_M)) ** (1 / 3)
    yp = brentq(lambda y: math.log(mu0(172.57, vl=(MVL, y))) - math.log(M5), 0.05, 1.5, xtol=1e-5)
    Ti = 1.0 * R_um ** (-1 / 3)
    yR.append(dict(R_um=R_um, M5=M5, y_prime=yp, T_i_GeV=Ti, m_KK_eV=GEV_INV_M / R * 1e9))
    print(f"(1) R = {R_um:5.1f} um: M5 = {M5:.2e} GeV, y'(1.65 TeV) = {yp:.3f}, graviton-DM T_i ~ {Ti:.2f} GeV, m_KK = {GEV_INV_M / R * 1e9:.3g} eV")
res["completion_B_yprime_of_R"] = dict(M_VL=MVL, rows=yR)
kappa, fa = 3e-5, 1e11
res["completion_A"] = dict(kappa=kappa, f_a=fa, m_s_natural_GeV=math.sqrt(kappa) * fa, N_DW="1 (single KSVZ quark)",
                           isocurvature="none: PQ broken after inflation (post-inflationary scenario)",
                           note="m_s ~ sqrt(kappa) f_a ~ 5e8 GeV unless tuned; s can decay to Higgs pairs via a small portal")
print(f"(2) completion A: extra scalar natural mass ~ sqrt(kappa) f_a = {math.sqrt(kappa) * fa:.1e} GeV; N_DW = 1; no isocurvature")
res["matrix"] = [
    dict(observable="dark matter", A="QCD axion, m_a 45-65 ueV (post-inflation lattice)", B="KK gravitons (dark dimension), keV-ish masses drifting", test="ADMX/MADMAX/ALPHA haloscopes; X-ray/galactic decays"),
    dict(observable="new coloured states", A="KSVZ quark at ~1e11 GeV (unobservable)", B="T, T', B triplet >= 1.65 TeV, y' ~ 0.5", test="LHC Run 3/HL-LHC, FCC-hh VLQ searches"),
    dict(observable="gravity at short range", A="Newtonian", B="deviation at R = 1-30 um", test="Eot-Wash type torsion balances"),
    dict(observable="reheating temperature", A=">~ 1e11 GeV (PQ restoration)", B="~ 1 GeV", test="indirect: DM identity, leptogenesis route"),
    dict(observable="baryogenesis", A="thermal leptogenesis (M_N 1e10-1e12)", B="non-thermal / low-scale", test="0nubb (Majorana), CP phase in nu oscillations"),
    dict(observable="tensor ratio r", A="0.005-0.007 (running-quartic inflation)", B="model-dependent", test="Simons Observatory / CMB-S4"),
    dict(observable="N_eff", A="3.044 (heavy states decouple)", B="~3.044 (non-thermal gravitons)", test="does not split A from B"),
    dict(observable="top mass", A="172.4-172.6 (lambda zero at f_a / sqrt(v M_Pl))", B="free (y' absorbs it)", test="FCC-ee threshold scan"),
]
for m in res["matrix"]: print(f"(3) {m['observable']:24s} | A: {m['A']:48s} | B: {m['B']:46s} | {m['test']}")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12689_completion_matrix.json"), "w"), indent=1)
