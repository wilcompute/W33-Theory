"""Stress test of pq_unification.py: two-loop gauge running with top Yukawa, split masses, alpha_s error, and the other gates of the one-scale model.
Two-loop: dg_i/dt = g_i^3 b_i/(16 pi^2) + g_i^3/(16 pi^2)^2 (sum_j b_ij g_j^2 - c_i y_t^2).  SM b_ij = [[199/50, 27/10, 44/5], [9/10, 35/6, 12], [11/10, 9/2, -26]], c = (17/10, 3/2, 2).  Added Dirac fermion (two Weyl): db_ii = 2 S_i (10/3 C_G(i) + 2 C_F(i)), db_ij = 2 * 2 S_i C_F(j), with S_i the Dynkin index times the dimension of the other factors, GUT-normalised for U(1): S_1 = (3/5) Y^2 d, C_F(1) = (3/5) Y^2.  Control: the same formula applied to one SM generation must reproduce the known generation part of b_ij: 3 generations give [[19/15, 3/5, 44/15], [1/5, 49/3, 4], [11/30, 3/2, 76/3]] per Weyl sum formula, tested on the SM table itself.
y_t: 16 pi^2 dy/dt = y (9/2 y^2 - 8 g3^2 - 9/4 g2^2 - 17/20 g1^2) at one loop, with g1 GUT normalised; Q Yukawas to SM quarks neglected.
Solve for (M_X, M_U) by requiring all three couplings to meet: 2 equations, 2 unknowns.  Initial values at M_Z in MSbar: 1/alpha_em = 127.955, s2 = 0.23122, alpha_s = 0.1180, y_t(M_Z) = 0.96.
Variation: alpha_s +- 0.0009, and masses split: M_i = M_X r_i, r in {1/3, 1, 3}, all patterns for the three colored multiplets.  When split, one masses ratio is held by pattern and M_X and M_U solved.
Proton: tau = 1.6e36 yr x (M_U/1e16)^4 (35 alpha_U)^-2, an estimate for p -> e+ pi0 from X, Y exchange; lattice matrix elements not recomputed, read as a factor of about 3.  Super-K 2.4e34, Hyper-K sensitivity about 1e35 (memory).
Axion: f = M_X / y; f_a = f / N_DW; relic with theta_i = 1: Omega = 0.12 (f_a/9e11)^(7/6) theta^2 as in pq_unification.py; solve f_a for theta = 1 and 2, then y and m_a; g_agamma from E/N with the standard formula.
Neutrino: seesaw with M_N = y_N f: y_nu needed for 0.05 eV.  Bookkeeping, not a prediction.
usage: py -3 pq_twoloop.py"""
import itertools
import json
import math
from fractions import Fraction as Fr
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

MZ = 91.1876
K = 1 / (16 * math.pi ** 2)
B1 = np.array([41 / 10, -19 / 6, -7.0])
B2 = np.array([[199 / 50, 27 / 10, 44 / 5], [9 / 10, 35 / 6, 12], [11 / 10, 9 / 2, -26.0]])
CT = np.array([17 / 10, 3 / 2, 2.0])
CFc = {1: 0.0, 3: 4 / 3, 6: 10 / 3, 8: 3.0}
CFw = {1: 0.0, 2: 3 / 4, 3: 2.0}
Tc = {1: 0.0, 3: 0.5, 6: 2.5, 8: 3.0}
Tw = {1: 0.0, 2: 0.5, 3: 2.0}
CG = np.array([0.0, 2.0, 3.0])


def weyl(c, w, y):
    y = float(y)
    S = np.array([0.6 * y * y * c * w, Tw[w] * c, Tc[c] * w])
    CF = np.array([0.6 * y * y, CFw[w], CFc[c]])
    b1 = (2 / 3) * S
    b2 = np.zeros((3, 3))
    for i in range(3):
        b2[i, i] = S[i] * (10 / 3 * CG[i] + 2 * CF[i])
        for j in range(3):
            if j != i:
                b2[i, j] = 2 * S[i] * CF[j]
    return b1, b2


def gen_control():
    tot1, tot2 = np.zeros(3), np.zeros((3, 3))
    for c, w, y in ((3, 2, 1 / 6), (3, 1, -2 / 3), (3, 1, 1 / 3), (1, 2, -1 / 2), (1, 1, 1)):
        a, b = weyl(c, w, y)
        tot1 += a
        tot2 += b
    return tot1 * 3, tot2 * 3


def dirac(r):
    a, b = weyl(*r)
    return 2 * a, 2 * b


def rhs(t, y, B1a, B2a):
    g = y[:3]
    yt = y[3]
    dg = K * B1a * g ** 3 + K ** 2 * g ** 3 * (B2a @ g ** 2 - CT * yt ** 2)
    dy = K * yt * (4.5 * yt ** 2 - 8 * g[2] ** 2 - 2.25 * g[1] ** 2 - 0.85 * g[0] ** 2)
    return np.r_[dg, dy]


def run(reps, ratios, lnMX, lnMU, a3=0.1180, s2=0.23122):
    ae = 127.955
    a = np.array([(3 / 5) * ae * (1 - s2), ae * s2, 1 / a3])
    y0 = np.r_[np.sqrt(4 * math.pi / a), 0.96]
    # thresholds sorted
    th = sorted([(lnMX + math.log(r), rep) for rep, r in zip(reps, ratios)], key=lambda z: z[0])
    tnow = math.log(MZ)
    B1a, B2a = B1.copy(), B2.copy()
    y = y0
    for tt, rep in th:
        if tt > tnow:
            y = solve_ivp(rhs, (tnow, min(tt, lnMU)), y, args=(B1a, B2a), rtol=1e-9, atol=1e-10).y[:, -1]
            tnow = min(tt, lnMU)
        d1, d2 = dirac(rep)
        B1a = B1a + d1
        B2a = B2a + d2
    if lnMU > tnow:
        y = solve_ivp(rhs, (tnow, lnMU), y, args=(B1a, B2a), rtol=1e-9, atol=1e-10).y[:, -1]
    return 4 * math.pi / y[:3] ** 2


def solve2(reps, ratios=None, a3=0.1180, s2=0.23122, x0=None):
    ratios = ratios or [1.0] * len(reps)
    f = lambda x: [run(reps, ratios, x[0], x[1], a3, s2)[0] - run(reps, ratios, x[0], x[1], a3, s2)[1], run(reps, ratios, x[0], x[1], a3, s2)[1] - run(reps, ratios, x[0], x[1], a3, s2)[2]]
    s = root(f, x0 or [math.log(1e9), math.log(1e16)], tol=1e-7)
    if not s.success or s.x[0] >= s.x[1]:
        return None
    ai = run(reps, ratios, s.x[0], s.x[1], a3, s2)
    return dict(MX=math.exp(s.x[0]), MU=math.exp(s.x[1]), inv_alpha_U=float(ai.mean()), spread=float(ai.max() - ai.min()))


def tau(MU, ia):
    return 1.6e36 * (MU / 1e16) ** 4 * (35 / ia) ** 2


out = {}
g1, g2 = gen_control()
out["control_generation"] = dict(b1=g1.tolist(), b2=g2.tolist(), expected_b1=[4.0, 4.0, 4.0], expected_b2_diag=[19 / 15 * 3, 49 / 3, 76 / 3])
print("control gen b1", np.round(g1, 3), "b2", np.round(g2, 3), flush=True)
MODELS = {"A": [(3, 1, -1 / 3), (3, 2, 1 / 6), (3, 2, 1 / 6)], "B": [(3, 1, 2 / 3), (3, 2, 1 / 6), (3, 2, 1 / 6)], "C": [(3, 1, -1 / 3), (3, 2, 1 / 6), (3, 2, 1 / 6), (1, 1, 1)]}
EN = {"A": (22 / 15, 5), "B": (28 / 15, 5), "C": (28 / 15, 5)}
for name, reps in MODELS.items():
    base = solve2(reps)
    row = dict(two_loop=base)
    print(name, "2-loop", base, flush=True)
    if base is None:
        out[name] = row
        continue
    x0 = [math.log(base["MX"]), math.log(base["MU"])]
    v = {}
    for lab, a3 in (("as+", 0.1189), ("as-", 0.1171)):
        v[lab] = solve2(reps, a3=a3, x0=x0)
    row["alpha_s"] = v
    sp = []
    n3 = len(reps)
    for pat in itertools.product((1 / 3, 1.0, 3.0), repeat=n3):
        s = solve2(reps, list(pat), x0=x0)
        if s:
            sp.append(dict(pattern=list(pat), **s, tau=tau(s["MU"], s["inv_alpha_U"])))
    row["split"] = dict(n=len(sp), MX=[min(s["MX"] for s in sp), max(s["MX"] for s in sp)], MU=[min(s["MU"] for s in sp), max(s["MU"] for s in sp)], tau=[min(s["tau"] for s in sp), max(s["tau"] for s in sp)], frac_above_SK=float(np.mean([s["tau"] > 2.4e34 for s in sp])), frac_above_HK=float(np.mean([s["tau"] > 1e35 for s in sp])))
    row["tau_years"] = tau(base["MU"], base["inv_alpha_U"])
    en, ndw = EN[name]
    ax = {}
    for th in (1.0, 2.0):
        fa = 9e11 * (1 / th ** 2) ** (6 / 7)
        f = fa * ndw
        ax[str(th)] = dict(fa=fa, f=f, y_Q=base["MX"] / f, m_a_ueV=5.7e12 / fa)
    row["axion"] = ax
    row["E_over_N"] = en
    row["g_over_KSVZ"] = abs(en - 1.92) / 1.92
    row["g_over_DFSZ"] = abs(en - 1.92) / abs(8 / 3 - 1.92)
    row["y_nu_needed"] = math.sqrt(0.05e-9 * ax["1.0"]["f"] / 174.1 ** 2)
    out[name] = row
    print(" tau %.2g yr; as: %s; split MX %.2g-%.2g MU %.2g-%.2g tau %.2g-%.2g frac>SK %.2f frac>HK %.2f; g/KSVZ %.3f g/DFSZ %.3f; yQ(theta=1) %.2g, ma %.1f ueV, y_nu %.2g" % (row["tau_years"], {k: (None if a is None else ("%.2g" % a["MX"], "%.2g" % a["MU"])) for k, a in v.items()}, *row["split"]["MX"], *row["split"]["MU"], *row["split"]["tau"], row["split"]["frac_above_SK"], row["split"]["frac_above_HK"], row["g_over_KSVZ"], row["g_over_DFSZ"], ax["1.0"]["y_Q"], ax["1.0"]["m_a_ueV"], row["y_nu_needed"]), flush=True)
json.dump(out, open("pq_twoloop.json", "w"), indent=1, default=float)
print("done", flush=True)
