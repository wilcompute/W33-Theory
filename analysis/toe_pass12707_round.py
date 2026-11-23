"""Pass 12707 (Claude track): fresh inputs and a revised Completion B.
 (1) Shared input card analysis/toe_inputs_card.json; drift scan of the hard-coded inputs in passes 12684-12706.
 (2) Input sensitivity of mu_0 and y' with the top-mass scheme ambiguity (MC vs pole) added to the experimental errors.
 (3) Finite one-loop threshold at M_VL: integrating out the vectorlike Q + T with Yukawa y' H Q T gives
     lambda_SM(M) = lambda_VL(M) - (5/6) N_c y'^4 / 16pi^2 (MS-bar, mu = M, degenerate Dirac masses; exact series of the CW potential),
     plus a field-renormalisation term -2 lambda dZ with |dZ| <= N_c y'^2/16pi^2 (bounded, not computed).
 (4) Revised B: Langhoff arXiv:2610.01825 (same suppression: Lee-Randall-Riojas) excludes KK-graviton DM in a flat dark dimension and
     needs R <~ 0.2 um.  y'_B over the surviving window R = lambda Lambda^(-1/4), lambda = 1e-4 .. 2.3e-3; gap to the hybrid; FCC.
 (5) Single-T production vs B's mixing bound (theta_t <~ 0.18), using the ATLAS combination arXiv:2408.08789.
 (6) Reheating window of the surviving dark dimension and its overlap with B-mesogenesis (5-140 MeV).
usage: py -3 analysis/toe_pass12707_round.py"""
import glob, json, math, os, re
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
CARD = json.load(open(os.path.join(HERE, "toe_inputs_card.json"), encoding="utf-8"))
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3, M5 = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3", "M5"))
K = 1 / (16 * math.pi ** 2); NC = 3
MT, SMT, SSCH = CARD["Mt"]["value"], CARD["Mt"]["sigma_exp"], CARD["Mt"]["sigma_scheme"]
A3, SA3, MVL = CARD["alpha_s"]["value"], CARD["alpha_s"]["sigma"], CARD["M_VL_floor_GeV"]["value"]
res = {"card": CARD}

# ======================================================================= (1) drift scan
pat = {"Mt": r"\b17[23]\.\d{1,2}\b", "alpha_s": r"\b0\.11[78]\d\b", "M_VL": r"\b1[67][45]0(?:\.0)?\b"}
drift = {}
for f in sorted(glob.glob(os.path.join(HERE, "toe_pass126[89]*_round.py")) + glob.glob(os.path.join(HERE, "toe_pass1270[0-6]_round.py"))):
    s = open(f, encoding="utf-8").read()
    drift[os.path.basename(f)] = {k: sorted(set(re.findall(p, s))) for k, p in pat.items()}
mvl_used = sorted(set(v for dd in drift.values() for v in dd["M_VL"]))
res["drift"] = dict(files=drift, M_VL_values_seen=mvl_used)
print(f"(1) drift scan over {len(drift)} scripts: M_VL values hard-coded {mvl_used}")

# ======================================================================= helpers


def run2a(Mt, a3, MVL_, yp, mu_max, dlam=0.0):
    """two-loop SM below M_VL, two-loop SM+VL above; dlam = lambda_VL - lambda_SM applied at M_VL (threshold)."""
    Mt0 = Mt - OFF3; y0 = np.array(initial(Mt, 125.20, a3) + [yp]); tM = math.log(MVL_ / Mt0); tE = math.log(mu_max / Mt0)
    kw = dict(rtol=1e-9, atol=1e-12, max_step=0.5)
    y1 = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, tM), y0, **kw).y[:, -1].copy()
    y1[4] += dlam(y1) if callable(dlam) else dlam
    return solve_ivp(lambda t, y: beta_vl(*y), (tM, tE), y1, **kw).y[:, -1]


def ypt(target, Mt=MT, a3=A3, MVL_=MVL, dlam=0.0):
    return brentq(lambda p: run2a(Mt, a3, MVL_, p, target, dlam)[4], 0.2, 0.9, xtol=1e-6)


def mu0(Mt, a3):
    Mt0 = Mt - OFF3
    s = solve_ivp(lambda t, y: beta_sm(*y), (0, math.log(2.4e18 / Mt0)), initial(Mt, 125.20, a3), rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.5)
    ts = np.linspace(0, s.t[-1], 3000); lam = s.sol(ts)[4]; j = np.where(lam < 0)[0][0]
    return Mt0 * math.exp(brentq(lambda t: s.sol(t)[4], ts[j - 1], ts[j]))


# ======================================================================= (3) threshold, exact CW series
a, M = sp.symbols("a M", positive=True)
mp2 = M ** 2 + a ** 2 / 2 + a * sp.sqrt(M ** 2 + a ** 2 / 4); mm2 = M ** 2 + a ** 2 / 2 - a * sp.sqrt(M ** 2 + a ** 2 / 4)
F = lambda m2: m2 ** 2 * (sp.log(m2 / M ** 2) - sp.Rational(3, 2))
ser = sp.Poly(sp.expand(sp.series(F(mp2) + F(mm2), a, 0, 6).removeO()), a)
assert ser.coeff_monomial(a ** 4) == sp.Rational(5, 6) and ser.coeff_monomial(a ** 2) == -2 * M ** 2
# V_CW = -Nc/16pi^2 * sum m^4(ln m^2/M^2 - 3/2), a = y' h/sqrt2, V = lambda h^4/4  ->  lambda_SM = lambda_VL - (5/6) Nc K y'^4
dl_CW = lambda y: +(5 / 6) * NC * K * y[5] ** 4                        # lambda_VL - lambda_SM at M_VL (CW h^4 part)
dl_V = dl_CW
dl_Zp = lambda y: dl_CW(y) + 2 * y[4] * NC * K * y[5] ** 2             # crude bound |dZ| <= Nc K y'^2, both signs
dl_Zm = lambda y: dl_CW(y) - 2 * y[4] * NC * K * y[5] ** 2
# Field renormalisation computed here: fermion bubble with chiral vertex (trace 2k.(k+p)), equal masses, MS-bar at mu = M:
#   dPi/dp^2 ~ int x(1-x) (1 - 3 L)  ->  Z_kin = 1 + Nc K y'^2 [ln(mu^2/M^2) - 1/3]  ->  Z_kin(M) = 1 - eps, eps = Nc K y'^2 / 3
#   canonical H_EFT = sqrt(1-eps) H  ->  lambda_EFT = lambda_VL (1 + 2 eps) - (5/6) Nc K y'^4.   (Cross-check with Matchmakereft: open.)
dl_full = lambda y: dl_CW(y) - 2 * y[4] * NC * K * y[5] ** 2 / 3
thr = {}
for name, tgt in (("B@R=0.088um", M5(0.088e-6)), ("B@R=10um(old)", M5(10e-6)), ("hybrid@1e10", 1e10)):
    y0_, yV, yF, yp_, ym_ = ypt(tgt), ypt(tgt, dlam=dl_V), ypt(tgt, dlam=dl_full), ypt(tgt, dlam=dl_Zp), ypt(tgt, dlam=dl_Zm)
    thr[name] = dict(no_threshold=y0_, with_V=yV, with_V_and_Z=yF, crude_Z_band=[min(yp_, ym_), max(yp_, ym_)], shift=yF - y0_)
    print(f"(3) {name}: y' = {y0_:.4f} -> {yV:.4f} (CW h^4) -> {yF:.4f} (+ field renormalisation); total shift {yF - y0_:+.4f}")
res["threshold"] = dict(formula="lambda_SM(M_VL) = lambda_VL(M_VL)(1 + 2 Nc y'^2/(48 pi^2)) - (5/6) N_c y'^4/(16 pi^2)", rows=thr)
dl_V = dl_full                                                          # use the full one-loop threshold below

# ======================================================================= (2) sensitivity incl. scheme
mu_rows = {}
for nm, (mt, a3) in {"PDG": (MT, A3), "ATLAS+CMS": (172.52, A3), "CMS": (172.44, A3), "ATLAS": (172.69, A3), "PDG+FLAG": (MT, 0.1183),
                      "Mt-0.5 (scheme)": (MT - SSCH, A3), "Mt+0.5 (scheme)": (MT + SSCH, A3)}.items():
    mu_rows[nm] = mu0(mt, a3)
    print(f"(2) mu_0 [{nm:16s}] = {mu_rows[nm]:.2e} GeV")
tB = M5(0.088e-6)
dmt = (ypt(tB, MT + .1, dlam=dl_V) - ypt(tB, MT - .1, dlam=dl_V)) / .2
das = (ypt(tB, MT, A3 + .0005, dlam=dl_V) - ypt(tB, MT, A3 - .0005, dlam=dl_V)) / .001
dlog_mt = (math.log10(mu0(MT + .1, A3)) - math.log10(mu0(MT - .1, A3))) / .2
dlog_as = (math.log10(mu0(MT, A3 + .0005)) - math.log10(mu0(MT, A3 - .0005))) / .001
err = {}
for lab, smt, sas in (("today exp", SMT, SA3), ("today exp+scheme", math.hypot(SMT, SSCH), SA3),
                      ("FCC era", CARD["FCC_era"]["sigma_Mt"], CARD["FCC_era"]["sigma_alpha_s"])):
    err[lab] = dict(sigma_yprime=math.hypot(dmt * smt, das * sas), sigma_log10_mu0=math.hypot(dlog_mt * smt, dlog_as * sas))
    print(f"(2) {lab:17s}: sigma(y'_B) = {err[lab]['sigma_yprime']:.4f}, sigma(log10 mu_0) = {err[lab]['sigma_log10_mu0']:.3f}")
res["sensitivity"] = dict(mu0=mu_rows, dy_dMt=dmt, dy_das=das, dlog10mu0_dMt=dlog_mt, dlog10mu0_das=dlog_as, errors=err)

# ======================================================================= (4) revised B window
L4 = CARD["dark_dimension"]["Lambda_inv_quarter_um"]; Rmax = CARD["dark_dimension"]["R_max_um"]
yH = ypt(1e10, dlam=dl_V)
rows = []
for lam_ in (1e-4, 3e-4, 1e-3, Rmax / L4):
    R = lam_ * L4; t = M5(R * 1e-6)
    rows.append(dict(lambda_=lam_, R_um=R, M5=t, yB=ypt(t, dlam=dl_V)))
for R in (1.0, 10.0, 30.0):
    t = M5(R * 1e-6); rows.append(dict(lambda_=R / L4, R_um=R, M5=t, yB=ypt(t, dlam=dl_V), excluded_by_2610_01825=True))
SG_GAP_FCC = 0.0012
for r in rows:
    r["gap"] = r["yB"] - yH
    r["FCC_sigma_sep"] = {str(sm): r["gap"] / math.hypot(sm, SG_GAP_FCC) for sm in CARD["FCC_era"]["sigma_yprime_meas"]}
    print(f"(4) lambda={r['lambda_']:.1e} R={r['R_um']:8.4f} um M5={r['M5']:.2e}: y'_B={r['yB']:.4f}, gap to hybrid ({yH:.4f}) = {r['gap']:.4f}; "
          f"FCC sep {r['FCC_sigma_sep']['0.005']:.0f}-{r['FCC_sigma_sep']['0.002']:.0f} sigma{'  [EXCLUDED window]' if r.get('excluded_by_2610_01825') else ''}")
surv = [r for r in rows if not r.get("excluded_by_2610_01825")]
res["B_revised"] = dict(rows=rows, y_hybrid=yH, surviving_yB=[min(r["yB"] for r in surv), max(r["yB"] for r in surv)],
                        note="separation = gap / (sigma_meas (+) sigma_param,gap,FCC): a measured y' compared with the two predictions")
print(f"(4) surviving B: y' = {res['B_revised']['surviving_yB'][0]:.3f}-{res['B_revised']['surviving_yB'][1]:.3f} "
      f"(+/- {err['today exp+scheme']['sigma_yprime']:.3f} param today)")

# ======================================================================= (5) single production
theta_max = 0.18
kappa_max = math.sqrt(2) * theta_max   # ASSUMPTION: singlet T, universal kappa ~ sqrt2 sin(theta_L); verify against Roy et al. PRD 101 115027
hl_kappa = 0.5 * (140 / 3000) ** 0.25   # sigma ~ kappa^2, background-dominated limit ~ 1/sqrt(L)
res["single_T"] = dict(theta_max=theta_max, kappa_max_assumed=kappa_max, hl_lhc_kappa_reach_at_2p1TeV=hl_kappa,
                       atlas_2408_08789=dict(excluded_all_masses_kappa_gt=0.57, kappa05_excluded_below_TeV=2.1,
                                             low_coupling="singlet excluded for m_T < 1.5 TeV at kappa ~ 0.25 (Gamma/m < 5%)"))
print(f"(5) theta_t <= {theta_max} -> kappa <= {kappa_max:.2f} (assumed map); ATLAS excludes kappa ~0.25 only below ~1.5 TeV -> no gain over 1.74 TeV; "
      f"HL-LHC (1/sqrt L) reaches kappa ~ {hl_kappa:.2f} at 2.1 TeV, i.e. the EW-precision mixing bound itself")

# ======================================================================= (6) reheating window vs B-mesogenesis
trh = []
for r in surv:
    tmax = 5.96 * (r["R_um"] / Rmax) ** (-1 / 3)   # Langhoff eq. (28): rho_h ~ T_RH^3 / m_KK at fixed allowed fraction (mass dependence of photon limits ignored)
    trh.append(dict(R_um=r["R_um"], T_RH_min=5.96, T_RH_max_est=tmax, overlaps_B_mesogenesis=tmax > 5.0))
    print(f"(6) R={r['R_um']:.4f} um: T_RH in [5.96, ~{tmax:.1f}] MeV (scaling estimate); B-mesogenesis optimum 5 (B_d) - 10 (B_s) MeV")
res["reheating"] = dict(rows=trh, B_mesogenesis="T_R ~ 5 MeV (B_d), ~10 MeV (B_s), allowed up to ~140 MeV (arXiv:2101.02706, 2610.03455)")

json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12707_round.json"), "w", encoding="utf-8"), indent=1, default=float)
print("wrote data/toe_pass12707_round.json")
