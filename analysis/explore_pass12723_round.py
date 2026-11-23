"""Pass 12723 (Claude track), items 1-4 (item 5: explore_pass12723_charlm96.py).
 (1) Flavour escape for the light-triplet hybrid: with 126-type Dirac contributions m_D1 = r m_u (r = 1 minimal), m_1 = m_D1^2 / M_R1 with
     M_R1 <= M_R1,max (Pass 12722).  DESI DR2 + CMB (sum < 0.064 eV, normal ordering) needs m_1 <~ 0.004 eV: the required suppression r.
 (2) Coupled quintessence in a static-radius B': V = V0 e^{-lambda phi}, dark-matter mass ~ e^{beta phi}; background integrated from z ~ 1100
     (8 pi G = 1, H0 = 1; Omega_b 0.049, Omega_m 0.31 today by shooting).  An observer assuming uncoupled cold DM infers
     rho_DE,app = 3H^2 - rho_b - rho_DM,0 a^-3 and w_app; CPL fit on 0.33 < a < 1; chi^2 vs DESI DR2 + CMB + Pantheon+ (Pass 12722 Gaussian).
 (3) Orbifold doublet-triplet splitting (Kawamura / Hall-Nomura S1/(Z2 x Z2')) vs the geometric protection of Pass 12717: window for M_* R.
 (4) Belle II exclusion of B': inclusive B -> baryon + missing energy, N_BB = 1.1e9 per ab^-1, hadronic tag 0.3%, signal efficiency
     0.2 sqrt(1 - (m_psi / m_max)^2) (m_max = 4.34 GeV for B -> psi + p), background 2 events per ab^-1; 90% CL reach 2.44 + 1.64 sqrt(B);
     fraction of B' (Pass 12713 Monte Carlo priors) excluded at 1, 10, 30, 50 ab^-1 vs m_psi.
usage: py -3 analysis/explore_pass12723_round.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = {}

# ======================================================================= (1)
P22 = json.load(open(os.path.join(ROOT, "data", "explore_pass12722_round.json")))
dm21, dm31 = 7.4e-5, 2.51e-3
s = lambda m1: m1 + math.sqrt(m1 ** 2 + dm21) + math.sqrt(m1 ** 2 + dm31)
m1max = float(np.interp(0.064, [s(x) for x in np.linspace(0, 0.03, 301)], np.linspace(0, 0.03, 301)))
fl = []
for r in P22["seesaw_triplets"]["rows"]:
    mD1max = math.sqrt(m1max * 1e-9 * r["MR1_max"])
    fl.append(dict(vHbar=r["vHbar"], m_u=r["m_u_GUT"], MR1_max=r["MR1_max"], mD1_max_MeV=mD1max * 1e3, r_required=mD1max / r["m_u_GUT"]))
    print(f"(1) <Hbar> = {r['vHbar']:.0e}, m_u = {r['m_u_GUT'] * 1e3:.1f} MeV: m_1 <= {m1max * 1e3:.1f} meV needs m_D1 <= {mD1max * 1e3:.3f} MeV, "
          f"i.e. m_D1 / m_u <= {mD1max / r['m_u_GUT']:.2f}")
res["flavour_escape"] = dict(m1_max_eV=m1max, rows=fl, note="126-type terms m_D = v (Y10 - 3 r126 Y126) can supply a factor-2-to-10 first-generation cancellation")

# ======================================================================= (2)
Ob, Om = 0.049, 0.31


def run(lam, beta, V0, A):
    def rhs(N, y):
        phi, dphi = y
        rho_b = 3 * Ob * math.exp(-3 * N); rho_c = A * math.exp(-3 * N) * math.exp(beta * phi); V = V0 * math.exp(-lam * phi)
        H2 = (rho_b + rho_c + V) / (3 - dphi ** 2 / 2)
        rho_tot = rho_b + rho_c + V + H2 * dphi ** 2 / 2; p_tot = H2 * dphi ** 2 / 2 - V
        dlnH = -0.5 * (rho_tot + p_tot) / H2
        ddphi = -(3 + dlnH) * dphi - (-lam * V + beta * rho_c) / H2
        return [dphi, ddphi]
    return solve_ivp(rhs, (-7.0, 0.0), [0.0, 0.0], rtol=1e-9, atol=1e-11, dense_output=True)


def state(sol, lam, beta, V0, A, N):
    phi, dphi = sol.sol(N)
    rho_b = 3 * Ob * math.exp(-3 * N); rho_c = A * math.exp(-3 * N) * math.exp(beta * phi); V = V0 * math.exp(-lam * phi)
    H2 = (rho_b + rho_c + V) / (3 - dphi ** 2 / 2)
    return H2, rho_b, rho_c


def fit(lam, beta):
    def eqs(p):
        V0, A = abs(p[0]), abs(p[1]); sol = run(lam, beta, V0, A); H2, rb, rc = state(sol, lam, beta, V0, A, 0.0)
        return [H2 - 1.0, (rb + rc) / (3 * H2) - Om]
    V0, A = fsolve(eqs, [3 * 0.69, 3 * (Om - Ob)], xtol=1e-12)
    V0, A = abs(V0), abs(A); sol = run(lam, beta, V0, A)
    rc0 = state(sol, lam, beta, V0, A, 0.0)[2]
    Ns = np.linspace(-1.1, 0, 200)
    rapp = np.array([3 * state(sol, lam, beta, V0, A, N)[0] - 3 * Ob * math.exp(-3 * N) - rc0 * math.exp(-3 * N) for N in Ns])
    w = -1 - np.gradient(np.log(rapp), Ns) / 3
    a = np.exp(Ns); X = np.vstack([np.ones_like(a), 1 - a]).T
    w0, wa = np.linalg.lstsq(X, w, rcond=None)[0]
    return w0, wa, float(w.min()), float(w[-1])


w0c, s0, wac, sa, rho = -0.857, 0.057, -0.55, 0.235, -0.9
Cinv = np.linalg.inv(np.array([[s0 ** 2, rho * s0 * sa], [rho * s0 * sa, sa ** 2]]))
chi2 = lambda w0, wa: float(np.array([w0 - w0c, wa - wac]) @ Cinv @ np.array([w0 - w0c, wa - wac]))
cq = []
for lam in (0.7, 1.0, 1.4):
    for beta in (-0.2, -0.1, 0.0, 0.1, 0.2):
        try:
            w0, wa, wmin, wnow = fit(lam, beta)
        except Exception as e:
            continue
        cq.append(dict(lam=lam, beta=beta, w0=w0, wa=wa, w_min=wmin, phantom=wmin < -1, chi2=chi2(w0, wa)))
        print(f"(2) lambda = {lam}, beta = {beta:+.1f}: apparent CPL w0 = {w0:.3f}, wa = {wa:.3f}, min w_app = {wmin:.3f}"
              f"{' (phantom crossing)' if wmin < -1 else ''}, chi2 = {chi2(w0, wa):.2f} (LambdaCDM {chi2(-1, 0):.2f})")
best = min(cq, key=lambda r: r["chi2"])
print(f"(2) best: lambda = {best['lam']}, beta = {best['beta']}: chi2 = {best['chi2']:.2f}")
res["coupled_quintessence"] = dict(rows=cq, best=best, chi2_LCDM=chi2(-1, 0),
                                   note="|beta| <= 0.2 respects the dark-sector fifth-force bound quoted by Bedroya et al. (c' <~ 0.2); no G variation")

# ======================================================================= (3)
res["orbifold"] = dict(protection="M_* L >= 30.8 with L = pi R -> M_* R >= 9.8", perturbativity="5D gauge coupling: M_* R <~ O(100) (strong coupling)",
                       window=[9.8, 100], note="Kawamura/Hall-Nomura S1/(Z2 x Z2') keeps doublets, removes triplets; Sigma on one brane, H on the other gives "
                                               "the brane separation of Pass 12717 for free")
print("(3) orbifold: protection needs M_* R >= 9.8 (M_* pi R >= 30.8); 5D perturbativity M_* R <~ 100 -> window 10 <~ M_* R <~ 100, the usual orbifold-GUT range")

# ======================================================================= (4)
rng = np.random.default_rng(12713); N = 200000
L4, Rmax = 87.7, 0.2
R_ = 10 ** rng.uniform(-4, math.log10(Rmax / L4), N) * L4
Tm = 5.96 * (R_ / Rmax) ** (-1 / 3); TR = np.exp(rng.uniform(np.log(5.96), np.log(np.maximum(Tm, 5.961)), N))
Br = 1.3e-8 * (60 / TR) * (10 ** rng.uniform(math.log10(11), 2, N) / 10.56) / 10 ** rng.uniform(-1, 0, N)
curve = []
for lumi in (1.0, 10.0, 30.0, 50.0):
    row = {"lumi_ab": lumi}
    for mpsi in (1.0, 2.0, 3.0, 4.0):
        eff = 0.2 * math.sqrt(max(0.0, 1 - (mpsi / 4.34) ** 2)); B = 2.0 * lumi
        reach = (2.44 + 1.64 * math.sqrt(B)) / (2 * 1.1e9 * lumi * 0.003 * eff)
        row[f"m{mpsi:.0f}"] = dict(reach=reach, frac=float(np.mean(Br >= reach)))
    curve.append(row)
    print(f"(4) Belle II {lumi:4.0f} ab^-1: reach (m_psi = 1/2/3/4 GeV) " + ", ".join(f"{row[f'm{m}']['reach']:.1e}" for m in (1, 2, 3, 4))
          + "; B' excluded " + ", ".join(f"{row[f'm{m}']['frac']:.0%}" for m in (1, 2, 3, 4)))
res["belle2"] = dict(curve=curve, plan="~1 ab^-1 now, ~10 ab^-1 in the 2030s, 50 ab^-1 by ~2042 with the IR upgrade (30 without)")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12723_round.json"), "w"), indent=1, default=float)
print("wrote data/explore_pass12723_round.json")
