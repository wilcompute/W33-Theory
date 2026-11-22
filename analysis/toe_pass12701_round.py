"""Pass 12701 (Claude track): five follow-ups to Pass 12700.
 (1) Leptogenesis for completion A under the Vissani bound: hierarchical vs quasi-degenerate heavy neutrinos.
     Vissani delta mu^2 = m_nu M^3/(4 pi^2 v^2); Davidson-Ibarra eps_max = 3 M m_atm/(16 pi v^2); eta_B = 0.96e-2 eps kappa;
     kappa from the Buchmuller-Di Bari-Plumacher fit; required resonant enhancement R = eps_needed/eps_DI ~ M/Delta M (order of magnitude).
 (2) Split-SUSY version of the tan beta bridge (gauginos + higgsinos at 1 TeV, scalars at M_SS), with the one-loop
     Giudice-Romanino RGEs (hep-ph/0406088 appendix, eqs. 56-60, 68; lambda_ours = lambda_GR/2) added to the two-loop SM running.
 (3) Repair of high-scale-SUSY unification by incomplete E6 pieces (vectorlike fermion pairs from the 27, Weyl adjoint pieces
     from the 78) at a mass M_X; one-loop scan.  Check: the other track's light 16/10 states (fd9c87e47) are complete SU(5) multiplets.
 (4) Two-loop gauge unification (top Yukawa included; B_ij and d_u from hep-ph/0406088 eqs. 40-45) and the d=6 proton lifetime
     tau(p -> e+ pi0) ~ 4.7e34 yr (M_X/1e16)^4 (alpha_G^-1/25)^2 (alpha_H = 0.0144 GeV^3, A_R = 2.5; factor ~3).
usage: py -3 analysis/toe_pass12701_round.py"""
import itertools, json, math, os
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G85 = {"__name__": "x", "__file__": os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py")}
exec(open(os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py"), encoding="utf-8").read().split("res = {}")[0], G85)
run, beta_sm = G85["run"], G85["beta_sm"]
K = 1 / (16 * math.pi ** 2)
res = {}

# (1) ------------------------------------------------------------------------------------------------------------
vs, mu2, matm, etaB = 174.0, 125.2 ** 2 / 2, 0.05e-9, 6.1e-10


def kappa(Kw):
    zB = 2 + 4 * Kw ** 0.13 * math.exp(-2.5 / Kw)
    return 2 / (Kw * zB) * (1 - math.exp(-Kw * zB / 2))


lep = {}
for mt_eV, lab in ((0.0086, "m~ = m_sol"), (0.05, "m~ = m_atm")):
    Kw = mt_eV / 1.08e-3; kap = kappa(Kw); eps = etaB / (0.96e-2 * kap)
    for M in (1.24e7, 1e8, 5e8, 1e9):
        eDI = 3 * M * matm / (16 * math.pi * vs ** 2)
        D = matm * M ** 3 / (4 * math.pi ** 2 * vs ** 2) / mu2
        R = eps / eDI
        lep[f"{lab}, M={M:.3g}"] = dict(K=Kw, kappa=kap, eps_needed=eps, eps_DI=eDI, Delta=D, enhancement=R,
                                        degeneracy_dM_over_M=min(1.0, 1 / R))
        print(f"(1) {lab}: M = {M:.2e}: K = {Kw:.1f}, kappa = {kap:.1e}, eps needed {eps:.1e}, eps_DI {eDI:.1e} -> "
              f"enhancement {R:.1e} (dM/M ~ {min(1, 1 / R):.0e}); Vissani Delta {D:.1e}")
res["leptogenesis_A"] = dict(rows=lep, note="hierarchical thermal leptogenesis needs R <= 1 (M >~ 5e8-1e9, Delta >~ 7e5); at Delta = 10 "
                             "(M = 1.24e7) a quasi-degenerate pair with dM/M ~ 1e-4 suffices (order of magnitude; TeV-scale resonant "
                             "needs ~1e-10). Minimal axiogenesis is not available for KSVZ/DFSZ f_a (literature)")


# (2) ------------------------------------------------------------------------------------------------------------
def split_rhs(t, y, Mt0):
    gY, g2, g3, yt, lam, gu, gd, gpu, gpd = y
    d = beta_sm(gY, g2, g3, yt, lam)
    d[0] += K * 6 / 25 * gY ** 3; d[1] += K * 2 * g2 ** 3; d[2] += K * 2 * g3 ** 3
    Tg = 1.5 * (gu ** 2 + gd ** 2) + 0.5 * (gpu ** 2 + gpd ** 2)
    T = 3 * yt ** 2 + Tg
    d[3] += K * yt * Tg
    d[4] += K * (lam * (6 * (gu ** 2 + gd ** 2) + 2 * (gpu ** 2 + gpd ** 2))
                 + 0.5 * (-5 * (gu ** 4 + gd ** 4) - 2 * gu ** 2 * gd ** 2 - (gpu ** 2 + gpd ** 2) ** 2 - 2 * (gu * gpu + gd * gpd) ** 2))
    C = 0.25 * gY ** 2 + 11 / 4 * g2 ** 2; Cp = 0.25 * gY ** 2 + 0.75 * g2 ** 2
    dgu = -3 * gu * C + 1.25 * gu ** 3 - 0.5 * gu * gd ** 2 + 0.25 * gu * gpu ** 2 + gd * gpd * gpu + gu * T
    dgpu = -3 * gpu * Cp + 0.75 * gpu ** 3 + 1.5 * gpu * gpd ** 2 + 0.75 * gpu * gu ** 2 + 3 * gpd * gd * gu + gpu * T
    dgd = -3 * gd * C + 1.25 * gd ** 3 - 0.5 * gd * gu ** 2 + 0.25 * gd * gpd ** 2 + gu * gpu * gpd + gd * T
    dgpd = -3 * gpd * Cp + 0.75 * gpd ** 3 + 1.5 * gpd * gpu ** 2 + 0.75 * gpd * gd ** 2 + 3 * gpu * gu * gd + gpd * T
    return d + [K * dgu, K * dgd, K * dgpu, K * dgpd]


def split_bridge(Mt, lgSS, Mlight=1e3, iters=8):
    sol, Mt0 = run(Mt, mu_max=Mlight * 1.0001)
    y0 = list(sol.sol(math.log(Mlight / Mt0))[:5])
    t0, t1 = math.log(Mlight / Mt0), math.log(10 ** lgSS / Mt0)
    beta = math.pi / 4; scale = np.ones(4)
    for _ in range(iters):
        sb, cb = math.sin(beta), math.cos(beta)
        tgt0 = np.array([y0[1] * sb, y0[1] * cb, y0[0] * sb, y0[0] * cb])
        for _ in range(4):
            s = solve_ivp(split_rhs, (t0, t1), y0 + list(tgt0 * scale), args=(Mt0,), rtol=1e-8, atol=1e-11)
            gY, g2 = s.y[0, -1], s.y[1, -1]
            want = np.array([g2 * sb, g2 * cb, gY * sb, gY * cb]); got = s.y[5:, -1]
            scale *= want / got
        lam = s.y[4, -1]; rhs = (g2 ** 2 + gY ** 2) / 8; c2 = lam / rhs
        if c2 < 0: return dict(log10_MSS=lgSS, lambda_at_MSS=float(lam), cos2_2beta=float(c2), tan_beta=None)
        if c2 > 1: c2 = 1.0
        beta = math.pi / 4 + 0.5 * math.asin(math.sqrt(c2))
    return dict(log10_MSS=lgSS, lambda_at_MSS=float(lam), cos2_2beta=float(c2), tan_beta=math.tan(beta))


sp = []
for lg in (5.0, 6.0, 7.0, 8.0, 9.0, 10.0):
    r = split_bridge(172.57, lg); sp.append(r)
    print(f"(2) split, M_SS = 1e{lg:g}: lambda(M_SS) = {r['lambda_at_MSS']:+.4f}, tan beta = {r['tan_beta'] if r['tan_beta'] is None else round(r['tan_beta'], 2)}")
# ceiling by bisection on log10 M_SS (tan beta = 1 <=> lambda(M_SS) = 0 with g~u = g~d)
lo, hi = 5.0, 10.0
for _ in range(14):
    mid = 0.5 * (lo + hi)
    if split_bridge(172.57, mid, iters=3)["tan_beta"] is None: hi = mid
    else: lo = mid
print(f"(2) split-SUSY ceiling: M_SS < 1e{lo:.2f} GeV (high-scale SUSY: 1e10.73)")
res["split_bridge"] = dict(rows=sp, log10_ceiling=lo, Mlight=1e3,
                           note="one-loop Giudice-Romanino split terms on top of two-loop SM; no threshold corrections at 1 TeV or M_SS")

# (3) ------------------------------------------------------------------------------------------------------------
AINV = np.array([59.01, 29.59, 8.47]); MZ = 91.1876
B1 = dict(SM=np.array([41 / 10, -19 / 6, -7.0]), MSSM=np.array([33 / 5, 1.0, -3.0]))


def S(dim3, dim2, Y):  # Dynkin indices (GUT-normalised U(1)) for one Weyl fermion in (dim3, dim2, Y)
    T3 = {1: 0, 3: 0.5, 8: 3.0}[dim3]; T2 = {1: 0, 2: 0.5, 3: 2.0}[dim2]
    return np.array([0.6 * Y * Y * dim3 * dim2, T2 * dim3, T3 * dim2])


PIECES = {  # Delta b for a vectorlike Dirac pair (2 Weyl) or a real Weyl adjoint piece, below M_SS
    "Q+Qbar (3,2,1/6)": 4 / 3 * S(3, 2, 1 / 6), "U+Ubar (3,1,2/3)": 4 / 3 * S(3, 1, 2 / 3), "D+Dbar (3,1,-1/3)": 4 / 3 * S(3, 1, 1 / 3),
    "L+Lbar (1,2,-1/2)": 4 / 3 * S(1, 2, 1 / 2), "E+Ebar (1,1,1)": 4 / 3 * S(1, 1, 1), "X+Xbar (3,2,-5/6)": 4 / 3 * S(3, 2, 5 / 6),
    "octet (8,1,0)": 2 / 3 * S(8, 1, 0), "triplet (1,3,0)": 2 / 3 * S(1, 3, 0)}


def unify1(segs):
    a = AINV.copy(); mu = MZ
    for i, (b, ms) in enumerate(segs):
        mend = segs[i + 1][1] if i + 1 < len(segs) else 1e30
        t12 = 2 * math.pi * (a[0] - a[1]) / (b[0] - b[1]) if b[0] != b[1] else -1
        if t12 >= 0 and mu * math.exp(t12) <= mend:
            a12 = a - b * t12 / (2 * math.pi); return mu * math.exp(t12), float(a12[0]), float(a12[2] - a12[0])
        a = a - b * math.log(mend / mu) / (2 * math.pi); mu = mend
    return None


hits = []
names = list(PIECES)
for k in (1, 2):
    for combo in itertools.combinations(names, k):
        for mult in itertools.product((1, 2, 3), repeat=k):
            db = sum(m * PIECES[c] for m, c in zip(mult, combo))
            for lgX in range(3, 10):
                u = unify1([(B1["SM"], MZ), (B1["SM"] + db, 10 ** lgX), (B1["MSSM"] + 1.5 * db, 1e10)])
                if u and u[0] > 3e15 and u[1] > 10:
                    hits.append(dict(pieces={c: m for c, m in zip(combo, mult)}, log10_MX=lgX, M12=u[0], a_inv=u[1], delta=u[2]))
hits.sort(key=lambda h: abs(h["delta"]))
for h in hits[:8]:
    print(f"(3) repair: {h['pieces']} at 1e{h['log10_MX']}: M_GUT {h['M12']:.1e}, alpha^-1 {h['a_inv']:.1f}, delta {h['delta']:+.2f}")
print(f"(3) {sum(abs(h['delta']) < 0.3 for h in hits)} repairs with |delta| < 0.3 (of {len(hits)} with M_GUT > 3e15); complete SU(5) multiplets (16 = 10+5bar+1, "
      f"10 = 5+5bar) shift all b_i equally -> cannot repair")
res["e6_repair"] = dict(n_hits=sum(abs(h["delta"]) < 0.3 for h in hits), n_mgut_ok=len(hits), hits=hits[:40], other_track_states="16 and 10 of SO(10) are complete SU(5) multiplets: "
                        "no change to one-loop differences (fd9c87e47's 64 unlifted spinor directions cannot repair unification)")


# (4) ------------------------------------------------------------------------------------------------------------
BIJ = dict(SM=np.array([[199 / 50, 27 / 10, 44 / 5], [9 / 10, 35 / 6, 12], [11 / 10, 9 / 2, -26]]),
           SPLIT=np.array([[104 / 25, 18 / 5, 44 / 5], [6 / 5, 106 / 3, 12], [11 / 10, 9 / 2, 22]]),
           MSSM=np.array([[199 / 25, 27 / 5, 88 / 5], [9 / 5, 25, 24], [11 / 5, 9, 14]]))
B1["SPLIT"] = np.array([9 / 2, -7 / 6, -5.0])
DU = dict(SM=np.array([17 / 10, 3 / 2, 2]), SPLIT=np.array([17 / 10, 3 / 2, 2]), MSSM=np.array([26 / 5, 6, 4]))
CU = dict(SM=np.array([17 / 20, 9 / 4, 8]), SPLIT=np.array([17 / 20, 9 / 4, 8]), MSSM=np.array([13 / 15, 3, 16 / 3]))
YCOEF = dict(SM=4.5, SPLIT=4.5, MSSM=6.0)


def unify2(segs, tanb=2.0):
    g = list(np.sqrt(4 * math.pi / AINV)); y = 0.97; mu = MZ
    for i, (th, ms) in enumerate(segs):
        if th == "MSSM": y = y / math.sin(math.atan(tanb))
        mend = segs[i + 1][1] if i + 1 < len(segs) else 1e19

        def f(t, z, th=th):
            gg, yy = z[:3], z[3]; g2 = gg ** 2
            dg = K * gg ** 3 * B1[th] + K * K * gg ** 3 * (BIJ[th] @ g2 - DU[th] * yy ** 2)
            dy = K * yy * (YCOEF[th] * yy ** 2 - CU[th] @ g2)
            return list(dg) + [dy]

        ev = lambda t, z: z[0] - z[1]; ev.terminal = True
        s = solve_ivp(f, (math.log(mu), math.log(mend)), g + [y], events=ev, rtol=1e-9, atol=1e-12, dense_output=True)
        if s.t_events[0].size:
            te = s.t_events[0][0]; z = s.sol(te); ainv = 4 * math.pi / z[:3] ** 2
            return math.exp(te), float(ainv[0]), float(ainv[2] - ainv[0])
        g = list(s.y[:3, -1]); y = s.y[3, -1]; mu = mend
    return None


def tau_p(M, ainv): return 4.7e34 * (M / 1e16) ** 4 * (ainv / 25) ** 2


two = {}
for lab, segs, tb in (("SM", [("SM", MZ)], 2), ("MSSM at 1 TeV", [("SM", MZ), ("MSSM", 1e3)], 10),
                      ("high-scale SUSY 1e10", [("SM", MZ), ("MSSM", 1e10)], 1.26),
                      ("split: fermions 1 TeV, scalars 1e10", [("SM", MZ), ("SPLIT", 1e3), ("MSSM", 1e10)], 1.26)):
    M, ai, d3 = unify2(segs, tb)
    two[lab] = dict(M12=M, a_inv=ai, delta_a3_inv=d3, tau_p_years=tau_p(M, ai))
    print(f"(4) two-loop {lab:36s}: M12 {M:.2e}, alpha^-1 {ai:.1f}, delta {d3:+.2f}, tau_p ~ {tau_p(M, ai):.1e} yr")
if hits:
    h = hits[0]; M, ai = h["M12"], h["a_inv"]
    two["best repair (one loop)"] = dict(M12=M, a_inv=ai, delta_a3_inv=h["delta"], tau_p_years=tau_p(M, ai), pieces=h["pieces"])
    print(f"(4) best repair {h['pieces']}: tau_p ~ {tau_p(M, ai):.1e} yr (Super-K 2.4e34, Hyper-K 20 yr ~1e35)")
res["two_loop_unification"] = dict(rows=two, note="Super-K tau(p->e+pi0) > 2.4e34 yr; d=6 gauge exchange with M_X = M12; factor ~3")

json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12701_round.json"), "w"), indent=1, default=float)
print("wrote data/toe_pass12701_round.json")

# (3b) ------------------------------------------------------------------------------------------------------------
# The best repair (vectorlike Q+U at ~1 TeV) has B's top-partner content.  Its gauge contributions keep lambda > 0 to M_Pl
# unless the partner Yukawa y' is sizeable: find y' with the quartic zero at 1e10 (so that M_SS ~ mu_0 survives).
from scipy.optimize import brentq as _brentq
mu0 = G85["mu0"]
rep = {f"y'={yp}": mu0(172.57, vl=(1000.0, yp)) for yp in (0.0, 0.2, 0.3, 0.4, 0.51)}
for k_, v_ in rep.items(): print(f"(3b) VL Q+U at 1 TeV, {k_}: mu_0 = {v_:.2e}")
yp10 = _brentq(lambda yp: math.log10(min(mu0(172.57, vl=(1000.0, yp)), 1e30)) - 10.0, 0.2, 0.51, xtol=1e-3)
print(f"(3b) quartic zero at 1e10 needs y' = {yp10:.3f} at 1 TeV")
res["e6_repair"]["vl_quartic_zero"] = dict(rows=rep, yprime_for_mu0_1e10=yp10)
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12701_round.json"), "w"), indent=1, default=float)
