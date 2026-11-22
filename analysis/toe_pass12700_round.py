"""Pass 12700 (Claude track): five follow-ups to Pass 12699.
 (1) tan beta bridge with the one-loop stop-mixing threshold
     Delta_lambda = 3 y_t^4/(8 pi^2) [Xt^2 - Xt^4/12]  (Xt = X_t/M_SS, SusyHD / Bagnaschi et al. convention)
     and the M_t band; upper bound on M_SS as a function of the mixing.
 (2) Completion A parameter space: random scan of the DFSZ-type potential (H1, H2, sigma) for boundedness below,
     plus the Higgs-mass tuning from the heavy doublet, Delta_H2 = lambda_eff m_H2^2/(16 pi^2 mu^2).
 (3) Gauge unification at one loop: SM, MSSM at 1 TeV, high-scale SUSY at 1e10 GeV, split SUSY (fermions at 1 TeV, scalars 1e10).
 (4) Fresh direction: naturalness ledger for A vs B.  The Vissani term from type-I seesaw,
     delta mu^2 = m_nu M_N^3/(4 pi^2 v^2) (v = 174 GeV; Vissani 1998, Clarke-Foot-Volkas 2015),
     against the Davidson-Ibarra floor of thermal leptogenesis; B's vectorlike top partner term 3 y'^2 M^2/(8 pi^2).
 (5) numbers for the summary page refresh.
SM running: toe_pass12685_intermediate_scale_suite.py (validated against three-loop lambda(M_Pl) to 1.6e-4).
usage: py -3 analysis/toe_pass12700_round.py"""
import json, math, os
import numpy as np
from scipy.optimize import minimize, brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G85 = {"__name__": "x", "__file__": os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py")}
exec(open(os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py"), encoding="utf-8").read().split("res = {}")[0], G85)
run, mu0 = G85["run"], G85["mu0"]
P2 = 8 * math.pi ** 2
res = {}


# (1) ------------------------------------------------------------------------------------------------------------
def dlam_stop(yt, x):
    return 3 * yt ** 4 / P2 * (x * x - x ** 4 / 12)


def bridge(Mt, x, lgs):
    sol, Mt0 = run(Mt)
    rows = []
    for lg in lgs:
        gY, g2, g3, yt, lam, _ = sol.sol(math.log(10 ** lg / Mt0))
        rhs = (g2 ** 2 + gY ** 2) / 8; d = dlam_stop(yt, x)
        c2 = (lam - d) / rhs
        tb = math.tan(math.pi / 4 + 0.5 * math.asin(math.sqrt(c2))) if 0 <= c2 <= 1 else None
        rows.append(dict(log10_MSS=lg, lambda_SM=float(lam), dlam_stop=float(d), cos2_2beta=float(c2), tan_beta=tb))
    # upper bound: lambda_SM(M_SS) = Delta_lambda (tan beta = 1)
    f = lambda lg: sol.sol(math.log(10 ** lg / Mt0))[4] - dlam_stop(sol.sol(math.log(10 ** lg / Mt0))[3], x)
    lgmax = brentq(f, 6, 18) if f(6) > 0 > f(18) else None
    return rows, lgmax


LGS = (8.0, 9.0, 10.0, 10.5)
b1 = {}
for x in (0.0, 1.0, 2.0, math.sqrt(6.0)):
    for Mt in (172.27, 172.57, 172.87):
        rows, lgmax = bridge(Mt, x, LGS)
        b1[f"Xt={x:.2f},Mt={Mt}"] = dict(rows=rows, log10_MSS_max=lgmax)
        if Mt == 172.57 or x == 0:
            tbs = ", ".join(f"1e{r['log10_MSS']:g}:{r['tan_beta']:.2f}" if r["tan_beta"] else f"1e{r['log10_MSS']:g}:none" for r in rows)
            print(f"(1) Xt={x:.2f} Mt={Mt}: M_SS max = 1e{lgmax:.2f} GeV; tan beta {tbs}")
res["tanbeta_threshold"] = dict(cases=b1, note="stop mixing only; other one-loop thresholds (heavy Higgs, gauginos/higgsinos, DR->MS) "
                                 "are O(1e-3) and enter as a band; Xt^2 <= 12 keeps Delta_lambda >= 0 so mixing LOWERS the M_SS ceiling")


# (2) ------------------------------------------------------------------------------------------------------------
def v4(p, z):
    # z: H1 (2 complex), H2 (2 complex), sigma (1 complex) -> 10 reals on the unit sphere
    z = z / np.linalg.norm(z)
    H1 = z[0:2] + 1j * z[2:4]; H2 = z[4:6] + 1j * z[6:8]; s = z[8] + 1j * z[9]
    n1, n2, ns = np.vdot(H1, H1).real, np.vdot(H2, H2).real, abs(s) ** 2
    h12 = np.vdot(H1, H2)
    return (p["l1"] * n1 ** 2 + p["l2"] * n2 ** 2 + p["l3"] * n1 * n2 + p["l4"] * abs(h12) ** 2 + p["ls"] * ns ** 2
            + p["l1s"] * n1 * ns + p["l2s"] * n2 * ns - 2 * p["k"] * (h12 * s * s).real)


def bfb(p, rng, starts=12):
    best = min(minimize(lambda z: v4(p, z), rng.normal(size=10), method="Nelder-Mead",
                        options=dict(maxiter=4000, xatol=1e-10, fatol=1e-16)).fun for _ in range(starts))
    return best


rng = np.random.default_rng(12700)
fa = 1e11; mu2 = 125.2 ** 2 / 2
scan = []
for _ in range(240):
    p = dict(l1=0.13, l2=10 ** rng.uniform(-2, 0), l3=rng.uniform(-1, 1), l4=rng.uniform(-1, 1),
             ls=10 ** rng.uniform(-12, -8), l1s=rng.choice([-1, 1]) * 10 ** rng.uniform(-14, -10),
             l2s=10 ** rng.uniform(-10, -4), k=10 ** rng.uniform(-16, -10))
    m = bfb(p, rng)
    # analytic necessary 2HDM conditions (no sigma)
    an = p["l3"] > -2 * math.sqrt(p["l1"] * p["l2"]) and p["l3"] + p["l4"] > -2 * math.sqrt(p["l1"] * p["l2"])
    mH2 = math.sqrt(max(p["l2s"], 0) * fa ** 2 / 2 + 2 * p["k"] * fa ** 2)
    scan.append(dict(bfb=bool(m > 0), analytic_2hdm=bool(an), m_H2=mH2, min_quartic=float(m)))
n_b = sum(s["bfb"] for s in scan); n_a = sum(s["analytic_2hdm"] for s in scan)
agree = sum(s["bfb"] == s["analytic_2hdm"] for s in scan)
print(f"(2) scan 240 points: bounded below {n_b}, analytic 2HDM conditions {n_a}, agreement {agree}/240 "
      f"(sigma portals/kappa never spoil BFB at these sizes: {all(s['bfb'] or not s['analytic_2hdm'] for s in scan)})")
tun = {}
for lam_eff in (0.1, 0.3, 1.0):
    for mh2 in (8e2, 2e3, 1e4, 1e6, 1e8):
        tun[f"leff={lam_eff},mH2={mh2:g}"] = lam_eff * mh2 ** 2 / (16 * math.pi ** 2 * mu2)
mH2_at10 = math.sqrt(10 * 16 * math.pi ** 2 * mu2 / 0.3)
print(f"(2) heavy-doublet tuning Delta = lambda_eff m_H2^2/(16 pi^2 mu^2): m_H2 = 1e8 -> {tun['leff=0.3,mH2=1e+08']:.1e}; "
      f"Delta = 10 at m_H2 = {mH2_at10:.0f} GeV (lambda_eff 0.3); b->s gamma type-II floor ~800 GeV")
res["A_scan"] = dict(n=240, bounded_below=n_b, analytic_2hdm=n_a, agreement=agree, tuning=tun, mH2_at_Delta10=mH2_at10,
                     note="kappa and sigma portals at DFSZ sizes never decide boundedness; the 2HDM quartics do. "
                          "A natural A puts H, A, H+- at 0.8-2 TeV")


# (3) ------------------------------------------------------------------------------------------------------------
AINV = np.array([59.01, 29.59, 8.47]); MZ = 91.1876
B = dict(SM=np.array([41 / 10, -19 / 6, -7.0]), MSSM=np.array([33 / 5, 1.0, -3.0]), SPLIT=np.array([9 / 2, -7 / 6, -5.0]))


def unify(segments):
    """segments: list of (b, mu_start); last runs to infinity. Return (M12, a^-1 at M12, a3^-1 - a12^-1)."""
    a = AINV.copy(); mu = MZ; out = None
    for i, (b, ms) in enumerate(segments):
        mend = segments[i + 1][1] if i + 1 < len(segments) else 1e30
        # a_i^-1(t) = a - b t/(2 pi); crossing of 1 and 2
        t12 = 2 * math.pi * (a[0] - a[1]) / (b[0] - b[1])
        if t12 >= 0 and MZ * 0 + mu * math.exp(t12) <= mend:
            a12 = a - b * t12 / (2 * math.pi)
            return mu * math.exp(t12), float(a12[0]), float(a12[2] - a12[0])
        t = math.log(mend / mu); a = a - b * t / (2 * math.pi); mu = mend
    return None


uni = {}
for lab, seg in (("SM", [(B["SM"], MZ)]), ("MSSM at 1 TeV", [(B["SM"], MZ), (B["MSSM"], 1e3)]),
                 ("high-scale SUSY 1e10", [(B["SM"], MZ), (B["MSSM"], 1e10)]),
                 ("split: fermions 1 TeV, scalars 1e10", [(B["SM"], MZ), (B["SPLIT"], 1e3), (B["MSSM"], 1e10)])):
    M, a12, d3 = unify(seg)
    uni[lab] = dict(M12=M, a12_inv=a12, delta_a3_inv=d3)
    print(f"(3) {lab:36s}: alpha1 = alpha2 at {M:.2e} GeV (alpha^-1 = {a12:.1f}); alpha3^-1 - alpha12^-1 = {d3:+.2f}")
res["unification"] = dict(rows=uni, note="one loop; two-loop shifts delta(alpha3^-1) by ~ +0.8 for MSSM (sign corrected in Pass 12701); complete E6 27s leave one-loop "
                                         "unification unchanged")


# (4) ------------------------------------------------------------------------------------------------------------
vs = 174.0; mnu = 0.05e-9
led = {}
for M in (1e7, 5e8, 1e9, 1e10):
    d = mnu * M ** 3 / (4 * math.pi ** 2 * vs ** 2)
    led[f"seesaw M_N={M:g}"] = d / mu2
    print(f"(4) Vissani: M_N = {M:.0e} GeV -> delta mu^2 = {d:.2e} GeV^2, Delta = {d / mu2:.1e}")
dB = 3 * 0.51 ** 2 * 1740 ** 2 / P2
led["B: VL top partner y'=0.51, M=1.74 TeV"] = dB / mu2
print(f"(4) B: vectorlike top partner -> Delta = {dB / mu2:.1f};  A with thermal leptogenesis (M_N >= 5e8): Delta >= {led['seesaw M_N=5e+08']:.0e}")
res["naturalness_ledger"] = dict(rows=led, note="thermal leptogenesis floor M_1 >~ 5e8 (flavoured) - 1e9 GeV (Davidson-Ibarra); "
                                 "A avoids the cost only with resonant/non-thermal leptogenesis; B's Dirac bulk neutrinos pay none; "
                                 "PQ quality (dim >= 12 at f_a = 1e11) is already in PASS12603_12608, not re-derived")

json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12700_round.json"), "w"), indent=1, default=float)
print("wrote data/toe_pass12700_round.json")
