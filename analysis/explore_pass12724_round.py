"""Pass 12724 (Claude track), items 1-4 (item 5: explore_pass12724_charlm*_fixed.py).
 (1) B' two-component dark matter: one dark baryon psi per baryon; with Omega_DM / Omega_b = 5.36 the psi fraction is f = (m_psi/m_p)/5.36;
     the kinematic bound m_psi(early) < 4.34 GeV and the drift m_psi(today)/m_psi(early) = 0.93 (best coupled fit, Pass 12723) give
     m_psi(today) <= 4.04 GeV -> f <= 0.80; the rest (>= 20%) is the second component (the dark scalar of mesogenesis or an axion).
 (2) Monte Carlo y' floor: M_t = 172.80 +- 0.26 (+) scheme 0.5 GeV, alpha_s 0.1180 +- 0.0009, threshold Z-term +-50%: min over
     mu_match in {1e10, ..., 1e13} of the needed y' (M_VL = 1.74 TeV); 2.5th percentile of the floor.
 (3) Orbifold KK thresholds, Hall-Nomura-type SU(5) on S1/(Z2 x Z2') (SUSY, 5D): massive levels 2n/R carry the SM adjoint (b = (0,-4,-6)) and
     the Higgs doublets (b = (0.6, 2, 0)); levels (2n+1)/R carry X,Y (b = (-10,-6,-4)) and the triplets (b = (0.27, 0, 2)); delta_i =
     sum b_i ln(M_s R / level) / 2pi; shift of the predicted alpha_3^-1: Delta = delta3 - delta1 + (12/7)(delta1 - delta2), for M_s R = 10-100.
 (4) Linear growth with DM-coupled quintessence (m_DM ~ e^{beta phi}, 8 pi G = 1): delta_c'' + (2 + H'/H - beta phi') delta_c' =
     1.5 (Omega_c (1 + 2 beta^2) delta_c + Omega_b delta_b); delta_b'' + (2 + H'/H) delta_b' = 1.5 (Omega_c delta_c + Omega_b delta_b);
     growth from z = 1100 normalised to the same early amplitude; sigma8 and f sigma8(z = 0.5) relative to LambdaCDM with the same Omega_m.
usage: py -3 analysis/explore_pass12724_round.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, fsolve

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}

# ======================================================================= (1)
ratio = 0.931
mmax_now = 4.34 * ratio
f_max = (mmax_now / 0.938) / 5.36
res["two_component"] = dict(m_psi_today_max=mmax_now, f_psi_max=f_max, f_other_min=1 - f_max)
print(f"(1) m_psi(today) <= {mmax_now:.2f} GeV -> psi carries <= {f_max:.0%} of the dark matter; >= {1 - f_max:.0%} must be a second component")

# ======================================================================= (2)
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3 = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3"))
K = 1 / (16 * math.pi ** 2)


def lam_end(yp, tgt, Mt, a3, zf, mvl=1740.0):
    Mt0 = Mt - OFF3; kw = dict(rtol=1e-8, atol=1e-11, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(mvl / Mt0)), np.array(initial(Mt, 125.20, a3) + [yp]), **kw).y[:, -1].copy()
    y[4] += (5 / 6) * 3 * K * y[5] ** 4 - zf * 2 * y[4] * 3 * K * y[5] ** 2 / 3
    return solve_ivp(lambda t, y: beta_vl(*y), (math.log(mvl / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1][4]


rng = np.random.default_rng(124); floors = []
for _ in range(40):
    Mt = 172.80 + rng.normal() * math.hypot(0.26, 0.5); a3 = 0.1180 + rng.normal() * 0.0009; zf = 1 + 0.5 * rng.uniform(-1, 1)
    ys = []
    for lg in (10, 11, 12, 13):
        try: ys.append(brentq(lambda p: lam_end(p, 10 ** lg, Mt, a3, zf), 0.05, 1.2, xtol=1e-5))
        except ValueError: pass
    if ys: floors.append(min(ys))
floors = np.array(floors)
res["y_floor_mc"] = dict(n=len(floors), median=float(np.median(floors)), p2_5=float(np.percentile(floors, 2.5)), p97_5=float(np.percentile(floors, 97.5)))
print(f"(2) y' floor over mu in 1e10-1e13 ({len(floors)} samples): median {np.median(floors):.3f}, 95% range {np.percentile(floors, 2.5):.3f}-{np.percentile(floors, 97.5):.3f}")

# ======================================================================= (3)
b_even = np.array([0, -4, -6]) + np.array([0.6, 2, 0]); b_odd = np.array([-10, -6, -4]) + np.array([0.267, 0, 2])
orb = []
for MsR in (10, 30, 100):
    se = sum(math.log(MsR / (2 * n)) for n in range(1, int(MsR // 2) + 1) if 2 * n < MsR)
    so = sum(math.log(MsR / (2 * n + 1)) for n in range(0, int(MsR)) if 2 * n + 1 < MsR)
    dlt = (b_even * se + b_odd * so) / (2 * math.pi)
    D = dlt[2] - dlt[0] + 12 / 7 * (dlt[0] - dlt[1])
    orb.append(dict(MsR=MsR, delta=dlt.tolist(), shift_alpha3_inv=D))
    print(f"(3) M_s R = {MsR}: thresholds delta_(1,2,3) = {np.round(dlt, 2)}; predicted alpha_3^-1 shift {D:+.2f} (hybrid mismatch today +0.26)")
res["orbifold_thresholds"] = dict(rows=orb, note="SU(5)-orbifold estimate; brane-localised kinetic terms add O(1/(2pi)) uncertainties")

# ======================================================================= (4)
Ob, Om = 0.049, 0.31


def background(lam, beta):
    def run(V0, A):
        def rhs(N, y):
            phi, dphi = y[:2]
            rb = 3 * Ob * math.exp(-3 * N); rc = A * math.exp(-3 * N) * math.exp(beta * phi); V = V0 * math.exp(-lam * phi)
            H2 = (rb + rc + V) / (3 - dphi ** 2 / 2)
            dlnH = -0.5 * (rb + rc + V + H2 * dphi ** 2 / 2 + H2 * dphi ** 2 / 2 - V) / H2
            return [dphi, -(3 + dlnH) * dphi - (-lam * V + beta * rc) / H2]
        return solve_ivp(rhs, (-7.0, 0.0), [0.0, 0.0], rtol=1e-9, atol=1e-11, dense_output=True)
    def quantities(sol, V0, A, N):
        phi, dphi = sol.sol(N)
        rb = 3 * Ob * math.exp(-3 * N); rc = A * math.exp(-3 * N) * math.exp(beta * phi); V = V0 * math.exp(-lam * phi)
        H2 = (rb + rc + V) / (3 - dphi ** 2 / 2)
        dlnH = -0.5 * (rb + rc + V + H2 * dphi ** 2 - V) / H2
        return H2, rb / (3 * H2), rc / (3 * H2), dlnH, dphi
    def eqs(p):
        V0, A = abs(p[0]), abs(p[1]); sol = run(V0, A); H2, ob, oc, _, _ = quantities(sol, V0, A, 0.0)
        return [H2 - 1, ob + oc - Om]
    V0, A = fsolve(eqs, [3 * 0.69, 3 * (Om - Ob)], xtol=1e-12); V0, A = abs(V0), abs(A)
    sol = run(V0, A)
    return lambda N: quantities(sol, V0, A, N)


def growth(lam, beta):
    q = background(lam, beta)
    def rhs(N, y):
        dc, ddc, db, ddb = y; H2, ob, oc, dlnH, dphi = q(N)
        return [ddc, -(2 + dlnH - beta * dphi) * ddc + 1.5 * (oc * (1 + 2 * beta ** 2) * dc + ob * db),
                ddb, -(2 + dlnH) * ddb + 1.5 * (oc * dc + ob * db)]
    N0 = -7.0; a0 = math.exp(N0)
    s = solve_ivp(rhs, (N0, 0.0), [a0, a0, a0, a0], rtol=1e-9, atol=1e-14, dense_output=True)
    def dm(N):
        dc, ddc, db, ddb = s.sol(N); H2, ob, oc, _, _ = q(N); om = ob + oc
        d = (oc * dc + ob * db) / om; dd = (oc * ddc + ob * ddb) / om
        return d, dd / d
    return dm


ref = growth(1e-6, 0.0)                  # effectively LambdaCDM (lambda -> 0)
gr = []
for lam, beta in ((1.0, 0.0), (1.0, 0.1), (0.7, 0.1), (1.4, 0.2)):
    g = growth(lam, beta)
    s8 = g(0.0)[0] / ref(0.0)[0]
    Nz = -math.log(1.5); fs8 = (g(Nz)[0] * g(Nz)[1]) / (ref(Nz)[0] * ref(Nz)[1])
    gr.append(dict(lam=lam, beta=beta, sigma8_ratio=s8, fsigma8_z05_ratio=fs8))
    print(f"(4) lambda {lam}, beta {beta}: sigma8 / sigma8(LCDM) = {s8:.3f}, f sigma8(z=0.5) ratio = {fs8:.3f}")
res["growth"] = dict(rows=gr, note="same early amplitude and Omega_m(today); S8 tension: weak lensing ~0.77-0.79 vs Planck ~0.83 (about -5 to -7%)")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12724_round.json"), "w"), indent=1, default=float)
print("wrote data/explore_pass12724_round.json")
