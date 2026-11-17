"""Pass 12688: round 4 on the intermediate-scale picture.
 (1) PQ (SMASH-like) inflation with a running quartic: U = lambda(phi) phi^4/4/(1 + xi phi^2)^2 with lambda(phi) = lambda_0 [1 + b ln(phi/phi_0)]
     (phi_0 = 1 M_Pl).  Which b gives n_s = 0.9743 (P-ACT-LB) or 0.9709 (P-ACT) with r < 0.036?  b = beta_lambda/lambda per e-fold of field;
     translate into the KSVZ Yukawa y_Q (beta_lambda_sigma ⊃ -6 y_Q^4/(16 pi^2) ... for one Dirac colour triplet: -6 N_c? we use -N_c y^4 * 2/(16pi^2))
     and the portal (+2 lambda_Hsigma^2/(16pi^2)).
 (2) Dark-dimension cosmology: KK-graviton dark matter needs T_i ~ 1 GeV and overproduces as ~T_i^3 (Gonzalo-Montero-Obied-Vafa 2209.09249);
     consequences for post-inflationary PQ restoration (T > f_a ~ 1e11), thermal leptogenesis (T > ~1e9), the vectorlike plasma dilution
     and Delta N_eff (non-thermal gravitons -> negligible).
 (3) FCC-era separation of the sqrt(v M_Pl) variants with the running offset closed (Pass 12687), theory floor from NNLO matching.
 (4) Vectorlike-quark decay patterns (literature, no fit).
 (5) Re-rating with ACT without DESI (P-ACT n_s = 0.9709 +- 0.0038; Delta N_eff < 0.14 at 95%).
 (6) Updated combined ranking with the dark dimension at T_i ~ 1 GeV.
usage: py -3 analysis/toe_pass12688_intermediate_scale_round4.py"""
import json, math, os
from scipy.integrate import quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}

# ---------------- (1) running-quartic nonminimal inflation
def infl(xi, b, N=55.6):
    try:
        return _infl(xi, b, N)
    except (ZeroDivisionError, ValueError, OverflowError):
        return None
def _infl(xi, b, N=55.6):
    lam = lambda p: 1 + b * math.log(p)
    U = lambda p: lam(p) * p ** 4 / 4 / (1 + xi * p * p) ** 2
    dchi = lambda p: math.sqrt((1 + xi * p * p + 6 * xi * xi * p * p) / (1 + xi * p * p) ** 2)
    def dU(p):
        h = 1e-6 * p
        return (U(p + h) - U(p - h)) / (2 * h)
    eps = lambda p: 0.5 * (dU(p) / U(p) / dchi(p)) ** 2
    def eta(p):
        h = 1e-4 * p; f = lambda q: dU(q) / dchi(q)
        return (f(p + h) - f(p - h)) / (2 * h) / dchi(p) / U(p)
    grid = [10 ** (k / 20) for k in range(-40, 81)]
    pend = None
    for a, c in zip(grid, grid[1:]):
        if (eps(a) - 1) * (eps(c) - 1) < 0 and eps(a) > 1: pend = brentq(lambda p: eps(p) - 1, a, c); break
    if pend is None: return None
    Nof = lambda p: quad(lambda q: U(q) / dU(q) * dchi(q) ** 2, pend, p, limit=400)[0]
    try:
        ps = brentq(lambda p: Nof(p) - N, pend * 1.0001, 1e4)
    except ValueError:
        return None
    if dU(ps) <= 0: return None
    return dict(ns=1 - 6 * eps(ps) + 2 * eta(ps), r=16 * eps(ps), phi_star=ps)
rows = []
for xi in (0.1, 1.0, 10.0):
    for b in (-0.06, -0.04, -0.02, 0.0, 0.02, 0.04, 0.06, 0.1):
        o = infl(xi, b)
        if o: rows.append(dict(xi=xi, b=b, **o)); print(f"(1) xi={xi:g} b={b:+.2f}: n_s={o['ns']:.4f} r={o['r']:.4f} phi*={o['phi_star']:.2f}")
def b_for(target, xi):
    f = lambda b: infl(xi, b)["ns"] - target
    try: return brentq(f, 0.0, 0.1, xtol=1e-5)
    except (ValueError, TypeError): return None
need = {}
for xi in (0.1, 1.0, 10.0):
    for lab, tgt in (("P-ACT-LB 0.9743", 0.9743), ("P-ACT 0.9709", 0.9709)):
        b = b_for(tgt, xi)
        o = infl(xi, b) if b is not None else None
        need[f"xi={xi:g} {lab}"] = dict(b=b, r=o["r"] if o else None)
        print(f"    xi={xi:g}: n_s = {lab} needs b = {b} (r = {o['r'] if o else None})")
# translate b into couplings: lambda_sigma ~ 4.4e-10 xi^2-ish (A_s normalisation, Pass 12686: 4.4e-10 at xi=1, N=60)
lam_s = {0.1: 1.04e-11, 1.0: 4.42e-10, 10.0: 3.84e-08}
trans = {}
for key, v in need.items():
    if v["b"] is None: continue
    xi = float(key.split()[0].split("=")[1]); ls = lam_s[xi]
    beta = v["b"] * ls                         # positive b needs a positive beta: portal-dominated
    portal = math.sqrt(beta * 16 * math.pi ** 2 / 2)      # beta ⊃ 2 lambda_Hsigma^2/(16 pi^2)
    trans[key] = dict(beta_needed=beta, portal_needed=portal, portal_over_sqrt_lambda_sigma=portal / math.sqrt(ls))
    print(f"    {key}: beta_lambda_sigma = {beta:.2e} -> portal lambda_Hsigma ~ {portal:.2e} = {portal / math.sqrt(ls):.3f} sqrt(lambda_sigma)")
res["running_quartic_inflation"] = dict(rows=rows, needed=need, couplings=trans,
                                        note="b>0 (quartic growing with field) raises n_s; a portal lambda_Hsigma ~ few x sqrt(lambda_sigma) supplies it, the same size the Higgs-stability threshold needs (>= 0.10 sqrt(lambda_sigma), Pass 12685)")

# ---------------- (2) dark-dimension cosmology vs the intermediate scale
over = {lab: (T / 1.0) ** 3 for lab, T in (("T = f_a ~ 1e11 GeV (post-inflation PQ)", 1e11), ("T = 1e9 GeV (thermal leptogenesis)", 1e9),
                                            ("T = 1.65 TeV (VL quarks in plasma)", 1650.0), ("T = 1 GeV (graviton DM)", 1.0))}
for k, v in over.items(): print(f"(2) KK-graviton overproduction factor Omega/Omega_DM ~ (T/1 GeV)^3 at {k}: {v:.1e}")
res["dark_dimension_cosmology"] = dict(overproduction_T3=over, note="Gonzalo-Montero-Obied-Vafa 2209.09249: T_i ~ 1 GeV gives all DM; scaling Omega ~ T_i^3 "
                                       "(m ~ T_i times Y ~ T_i^2 M_Pl/M_5^3). Brane T <~ few GeV: no post-inflationary axion, no thermal leptogenesis, VL quarks never in "
                                       "plasma, non-thermal gravitons -> Delta N_eff negligible (the +3.1 sigma of Pass 12687 is removed)")

# ---------------- (3) FCC-era separation (sensitivities from Pass 12685)
f85 = json.load(open(os.path.join(ROOT, "data", "toe_pass12685_intermediate_scale_suite.json")))["forecast"]
dl_dmt, dl_da, dl_dmh = f85["dlog10mu0_dMt"], f85["dlog10mu0_dalpha_s"], f85["dlog10mu0_dMh"]
dl_dlam = dl_dmh / 0.00206
sep = {}
for lab, (dmt, da, dmh, thy, thl) in {"FCC-ee, current NNLO matching": (0.05, 0.0003, 0.02, 0.0005, 0.0003),
                                       "FCC-ee, matching errors halved": (0.05, 0.0003, 0.02, 0.00025, 0.00015),
                                       "FCC-ee, matching N3LO (errors /4)": (0.05, 0.0002, 0.01, 0.000125, 0.000075)}.items():
    s = math.sqrt((dl_dmt * dmt) ** 2 + (dl_da * da) ** 2 + (dl_dmh * dmh) ** 2 + (dl_dmt * thy / 0.00556) ** 2 + (dl_dlam * thl) ** 2)
    sep[lab] = dict(sigma_log10mu0=s, sqrtvMPl_vs_sqrtvMbar_sigma=math.log10(math.sqrt(1.2209e19 / 2.435e18)) / s)
    print(f"(3) {lab}: sigma(log10 mu0) = {s:.3f}; sqrt(v M_Pl) vs sqrt(v Mbar_Pl) separated at {sep[lab]['sqrtvMPl_vs_sqrtvMbar_sigma']:.1f} sigma")
res["fcc_separation"] = sep

# ---------------- (4) VLQ decay patterns (literature)
res["vlq_patterns"] = {"singlet-like T (mixing with t_R-less SM doublet)": "BR(Wb:Zt:ht) ~ 2:1:1",
                       "doublet (T,B) mixing via t_R": "T -> Zt, ht ~ 50:50; B -> Wt ~ 100%",
                       "this rescue": "near-degenerate T, T', B triplet at M_VL >= 1.65 TeV; pattern set by the (small) SM mixing, not by y'",
                       "limits": "pair production 1.49 TeV (singlet) - 1.6 TeV (doublet), 2412.01761 / ATLAS PRD 111 012012"}

# ---------------- (5) ACT without DESI
smash_ns = 0.9653
r5 = dict(SMASH_pull_PACT_LB=(smash_ns - 0.9743) / 0.0034, SMASH_pull_PACT=(smash_ns - 0.9709) / 0.0038)
print(f"(5) SMASH n_s 0.9653: pull {r5['SMASH_pull_PACT_LB']:+.2f} (P-ACT-LB) -> {r5['SMASH_pull_PACT']:+.2f} (P-ACT, no DESI)")
res["act_without_desi"] = r5

# ---------------- (6) updated ranking
p87 = json.load(open(os.path.join(ROOT, "data", "toe_pass12687_intermediate_scale_round3.json")))["combined_likelihood"]["models"]
neff_sm = (3.044 - 2.86) / 0.13
rank = {k: dict(chi2=v["chi2"], k=v["k"]) for k, v in p87.items()}
rank["dark dimension + VL quark, T_i ~ 1 GeV (non-thermal gravitons)"] = dict(chi2=0.0 + neff_sm ** 2, k=1)
rank["full SMASH with running quartic (b fitted)"] = dict(chi2=p87["boundary at axion f_a (lattice)"]["chi2"], k=1)
rank["full SMASH, P-ACT (no DESI) n_s"] = dict(chi2=p87["boundary at axion f_a (lattice)"]["chi2"] + r5["SMASH_pull_PACT"] ** 2, k=0)
base = rank["SM + LCDM (free M_t, free n_s)"]["chi2"]
for k, v in rank.items():
    v["dAIC"] = v["chi2"] + 2 * v["k"] - base
    print(f"(6) {k:62s}: chi2 = {v['chi2']:.2f}, k = {v['k']}, dAIC = {v['dAIC']:+.2f}")
res["ranking"] = rank
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12688_intermediate_scale_round4.json"), "w"), indent=1, default=float)
