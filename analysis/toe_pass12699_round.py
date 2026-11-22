"""Pass 12699.
 (1) Anomaly scout against completions A and B: Belle II B+ -> K+ nu nubar (2.3(7)e-5 vs SM 0.50e-5, 2023) via B -> K a, and the
     ~95 GeV scalar hints (CMS gamma gamma, LEP bb); values entered from the experiments' publications (approximate).
 (2) Completion A's DFSZ-type scalar potential (H1, H2, sigma; PQ term -kappa H1 H2 sigma^2): copositivity of the quartic form on the
     radial directions, a numerical vacuum with f_a = 1e11 GeV and v = 246 GeV, and the mass spectrum (heavy doublet, tuning).
 (3) Toy Monte Carlo for completion B's soft leptons: pair kinematics from the CT18NNLO-weighted threshold distribution (Pass 12692),
     B -> T l nu with a Michel spectrum (endpoint dM/2 = 22 GeV) in the B frame, boosted to the lab: acceptance for pT > 7/10 GeV, |eta| < 2.5.
 (4) Haloscope forecast for A's axion (b-only E/N = 2/3) relative to KSVZ and DFSZ (E/N = 8/3) benchmarks: scan time ~ g^-4.
 (5) Bridge to the other track's SUSY E6 construction: if SUSY is broken at M_SS with the MSSM boundary condition
     lambda(M_SS) = (g^2 + g'^2)/8 cos^2 2beta, which tan beta is required for M_SS = 1e9-1e12 GeV at the measured M_t?
usage: py -3 analysis/toe_pass12699_round.py"""
import json, math, os
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
rng = np.random.default_rng(12699)
# (1)
mB, mK, GB = 5.279, 0.493677, 6.582e-25 / 1.638e-12
def brBKa(fa, C, f0=0.33): return mB ** 3 * C ** 2 * f0 ** 2 * (1 - mK ** 2 / mB ** 2) ** 3 / (16 * math.pi * fa ** 2 * GB)
excess = 2.3e-5 - 0.50e-5
fa_over_C = math.sqrt(brBKa(1.0, 1.0) / excess)
res["anomaly_scout"] = dict(belle2_excess=excess, fa_over_Cbs_needed_GeV=fa_over_C, A_prediction=brBKa(1e11, 0.041),
                            reading_K="needs f_a/C_bs ~ %.1e GeV: excluded for a QCD axion (SN1987A f_a >~ 1e8); A predicts 1e-13: A does not explain it" % fa_over_C,
                            reading_95="A's second doublet decouples at >= 1e5 GeV and B adds no light scalar: neither completion supplies a 95 GeV state")
print(f"(1) Belle II K nu nu excess {excess:.1e}: needs f_a/C_bs ~ {fa_over_C:.1e} GeV (A gives BR {brBKa(1e11, 0.041):.0e}); 95 GeV: no state in A or B")
# (2) DFSZ-type potential on radial fields (h1, h2, s): V = sum m_i^2 phi_i^2/2 + quartics - kappa h1 h2 s^2
lam1, lam2, lams, l12, l1s, l2s, kap = 0.13, 0.5, 1e-10 * 4, 0.1, 1e-12, 1e-6, 2e-13
Q = np.array([[lam1 / 4, l12 / 4, l1s / 4], [l12 / 4, lam2 / 4, l2s / 4], [l1s / 4, l2s / 4, lams / 4]])
# copositivity with the kappa term: minimise quartic part on the unit sphere over the positive octant (h1, h2 > 0 maximises -kappa term)
def quart(x):
    x = np.abs(x) / np.linalg.norm(x)
    h1, h2, s = x
    return lam1 * h1 ** 4 / 4 + lam2 * h2 ** 4 / 4 + lams * s ** 4 / 4 + l12 * h1 ** 2 * h2 ** 2 / 2 + l1s * h1 ** 2 * s ** 2 / 2 + l2s * h2 ** 2 * s ** 2 / 2 - kap * h1 * h2 * s ** 2
qmin = min(minimize(quart, rng.random(3) + 0.01, method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-20, maxiter=20000)).fun for _ in range(40))
fa = 1e11
# masses: choose m_s^2 = -lams fa^2, m_1^2 tuned for v1 ~ 246, m_2^2 positive large
m2sq = 1e14 ** 1 * 1.0       # (1e7 GeV)^2
v2_induced = kap * fa ** 2 * 246.0 / (m2sq + l2s * fa ** 2)
mH2 = math.sqrt(m2sq + l2s * fa ** 2)
res["dfsz_potential"] = dict(couplings=dict(lam1=lam1, lam2=lam2, lams=lams, l12=l12, l1s=l1s, l2s=l2s, kappa=kap), quartic_min_on_sphere=qmin,
                             bounded_below=qmin > 0, m_H2_GeV=mH2, v2_induced_GeV=v2_induced, tan_beta_eff=246.0 / max(v2_induced, 1e-30),
                             tuning=(125.0 / mH2) ** 2 + (l1s * fa ** 2) / (2 * 125.0 ** 2) * 0 , note="tiny portals (l1s ~ 1e-12) keep the Higgs light; m_H2 ~ 1e8 GeV")
print(f"(2) quartic minimum on the sphere {qmin:.2e} (bounded below: {qmin > 0}); m_H2 ~ {mH2:.1e} GeV, induced v2 ~ {v2_induced:.1e} GeV")
# (3) toy MC
src = open(os.path.join(HERE, "toe_pass12692_five_checks.py"), encoding="utf-8").read()
start = src.index("from parton import mkPDF"); stop = src.index("stt = sigma_pair(172.5, 13000.0)")
G = {"__name__": "x", "__file__": os.path.join(HERE, "toe_pass12692_five_checks.py"), "np": np, "math": math, "os": os}
exec(src[start:stop], G)
pdf, alphas, sig_hat, xf = G["pdf"], G["alphas"], G["sig_hat"], G["xf"]
M, rs, dM = 1650.0, 14000.0, 44.4
s = rs * rs; mu = M; a = alphas(mu); tau0 = 4 * M * M / s
taus = np.exp(np.linspace(math.log(tau0) + 1e-6, math.log(0.5), 300))
wts = []
gx, wx = np.polynomial.legendre.leggauss(80)
for tau in taus:
    lt = math.log(tau); lx = lt / 2 * (1 - gx); x = np.exp(lx); x2 = tau / x; jx = -lt / 2
    Lgg = float(np.sum(wx * xf(21, x, mu) * xf(21, x2, mu))) * jx / tau
    qq = sum(xf(q, x, mu) * xf(-q, x2, mu) + xf(-q, x, mu) * xf(q, x2, mu) for q in (1, 2, 3, 4, 5))
    Lqq = float(np.sum(wx * qq)) * jx / tau
    sq, sg = sig_hat(tau * s, M, a)
    wts.append(tau * tau * (Lqq * sq + Lgg * sg))        # d sigma / d ln tau
wts = np.array(wts); cdf = np.cumsum(wts); cdf /= cdf[-1]
n = 200000
tau_s = np.interp(rng.random(n), cdf, taus)
shat = tau_s * s
beta = np.sqrt(1 - 4 * M * M / shat)
pstar = 0.5 * np.sqrt(shat) * beta
cth = rng.uniform(-1, 1, n); sth = np.sqrt(1 - cth ** 2); ph = rng.uniform(0, 2 * math.pi, n)
ypair = np.clip(rng.normal(0, 0.7, n), -2.5, 2.5)
# heavy quark momentum in lab: transverse = pstar sin, longitudinal boosted by pair rapidity
EB_cm = 0.5 * np.sqrt(shat)
pz_cm = pstar * cth
E_lab = EB_cm * np.cosh(ypair) + pz_cm * np.sinh(ypair)
pz_lab = EB_cm * np.sinh(ypair) + pz_cm * np.cosh(ypair)
px, py = pstar * sth * np.cos(ph), pstar * sth * np.sin(ph)
# lepton in B frame: Michel spectrum x^2(3-2x) on [0,1], E = x dM/2, isotropic
u = rng.random(n); xs = np.empty(n)
grid = np.linspace(0, 1, 2001); c = grid ** 3 - grid ** 4 / 2; c /= c[-1]
xs = np.interp(u, c, grid)
El = xs * dM / 2
cl = rng.uniform(-1, 1, n); sl = np.sqrt(1 - cl ** 2); pl = rng.uniform(0, 2 * math.pi, n)
lx, ly, lz = El * sl * np.cos(pl), El * sl * np.sin(pl), El * cl
# boost lepton by the B velocity vector
bx, by, bz = px / E_lab, py / E_lab, pz_lab / E_lab
b2 = bx ** 2 + by ** 2 + bz ** 2; gam = 1 / np.sqrt(1 - b2)
bp = bx * lx + by * ly + bz * lz
k = (gam - 1) * bp / b2 + gam * El
Lx, Ly, Lz = lx + k * bx, ly + k * by, lz + k * bz
pT = np.hypot(Lx, Ly); pabs = np.sqrt(pT ** 2 + Lz ** 2); eta = 0.5 * np.log((pabs + Lz) / (pabs - Lz + 1e-12) + 1e-12)
acc = {f"pT>{c_}": float(np.mean((pT > c_) & (np.abs(eta) < 2.5))) for c_ in (5.0, 7.0, 10.0, 15.0)}
res["toy_mc_soft_lepton"] = dict(n=n, median_pT=float(np.median(pT)), acceptance=acc, mean_beta=float(beta.mean()))
print(f"(3) toy MC: median soft-lepton pT {np.median(pT):.1f} GeV; acceptance " + ", ".join(f"{k} {v:.2f}" for k, v in acc.items()) + f"; <beta*> = {beta.mean():.2f}")
# (4)
hal = {}
for lab, EN in (("KSVZ", 0.0), ("b only (A)", 2 / 3), ("b + tau opposite (A)", -4 / 3), ("DFSZ benchmark", 8 / 3)):
    g = abs(EN - 1.92) / 1.92
    hal[lab] = dict(E_over_N=EN, g_rel_KSVZ=g, time_rel_KSVZ=g ** -4, time_rel_DFSZ=(g / (abs(8 / 3 - 1.92) / 1.92)) ** -4)
    print(f"(4) {lab:22s}: g/g_KSVZ = {g:.2f}; scan time vs KSVZ x{g ** -4:.2f}, vs DFSZ x{hal[lab]['time_rel_DFSZ']:.2f}")
res["haloscope"] = dict(rows=hal, note="experiments designed to reach DFSZ (MADMAX/ALPHA goals) cover A's b-only axion ~7.7x faster than DFSZ")
# (5)
G85 = {"__name__": "x", "__file__": os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py")}
exec(open(os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py"), encoding="utf-8").read().split("res = {}")[0], G85)
sol, Mt0 = G85["run"](172.57)
tb = []
for lg in (9.0, 10.0, 10.5, 11.0, 11.5, 12.0):
    t = math.log(10 ** lg / Mt0); gY, g2, g3, yt, lam, _ = sol.sol(t)
    rhs = (g2 ** 2 + gY ** 2) / 8
    c2 = lam / rhs
    if c2 < 0: tb.append(dict(log10_MSS=lg, lambda_SM=float(lam), cos2_2beta=float(c2), tan_beta=None)); continue
    c = math.sqrt(min(c2, 1.0)); beta = 0.5 * math.acos(c) if c <= 1 else 0
    tanb = 1 / math.tan(0.5 * math.acos(-c)) if False else math.tan(math.pi / 4 + 0.5 * math.asin(c))
    tb.append(dict(log10_MSS=lg, lambda_SM=float(lam), cos2_2beta=float(c2), tan_beta=tanb))
    print(f"(5) M_SS = 1e{lg} GeV: lambda_SM = {lam:+.4f}, (g^2+g'^2)/8 = {rhs:.4f} -> cos^2 2beta = {c2:.3f}, tan beta = {tanb:.2f}")
for r in tb:
    if r["tan_beta"] is None: print(f"(5) M_SS = 1e{r['log10_MSS']} GeV: lambda_SM < 0 -> no tan beta (SUSY threshold cannot match)")
res["high_scale_susy_tanbeta"] = dict(rows=tb, note="tree-level matching, no threshold corrections; SUSY broken above mu_0 ~ 5e10 GeV is impossible")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12699_round.json"), "w"), indent=1, default=float)
