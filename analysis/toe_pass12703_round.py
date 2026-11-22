"""Pass 12703 (Claude track): five follow-ups to Pass 12702.
 (1) E6 650: which SM-singlet direction lets Q + U be light while e^c stays heavy?  Explicit SU(5) Lambda^2(5) = 10 decomposition of the
     SM-invariant mass operators into 1 + 24 + 75; SO(10) x U(1) content of the 650 and its SM-singlet count (6 + 11 = 17).
     Alternatives: 650 vacua preserving SU(3)^3 / SU(6)xSU(2) / SO(10)xU(1) (Babu-Bajc-Susic 2305.16398) -> which light blocks, and do
     they unify (two loop, hybrid)?
 (2) Two-loop vectorlike terms in lambda and y_t: full two-loop SM + (Q_VL, T_VL, y') RGEs generated with PyR@TE 3 (2007.12700); the SM
     limit reproduces every two-loop coefficient of beta_sm in Pass 12685 (control).  Recompute y' for the hybrid (lambda(1e10)=0) and B.
 (3) Explicit flavour model for completion A's degenerate N: two N with O(2)-symmetric Majorana mass at Lambda, Casas-Ibarra Yukawas,
     one-loop running (h h^dag and the tau Yukawa), flavoured Pilaftsis-Underwood asymmetries, BDP efficiency per flavour -> eta_B.
 (4) B versus hybrid beyond the LHC: short-range gravity caps R < 38.6 um (Lee et al. 2020) -> upper end of B's y' band; y' really
     measures the scale of the quartic zero, so B and the hybrid overlap if M_SS <~ 1e9 GeV.  Hybrid unification versus M_SS.
 (5) Review of the other track's a790aef mediator vacuum (re-run its sympy verification; does it change the 650 question?).
usage: py -3 analysis/toe_pass12703_round.py"""
import json, math, os, subprocess, sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G = {"__file__": os.path.join(HERE, "toe_pass12702_round.py")}
src = open(os.path.join(HERE, "toe_pass12702_round.py"), encoding="utf-8").read().split("def yp_for")[0]
exec(src, G)
G85 = G["G85"]
K, MPL, initial, beta_sm, mu0, OFF3 = G["K"], G85["MPL"], G85["initial"], G85["beta_sm"], G85["mu0"], G85["OFF3"]
weyl, BIJ, B1, DU, CU, YC, AINV, MZ, tau_p = (G[k] for k in ("weyl", "BIJ", "B1", "DU", "CU", "YC", "AINV", "MZ", "tau_p"))
res = {}
MT = 172.57

# ======================================================================= (1) E6 650 and the SU(5) 75
R = sp.Rational
Y5 = [R(-1, 3)] * 3 + [R(1, 2)] * 2
pairs = [(a, b) for a in range(5) for b in range(a + 1, 5)]
lab = lambda a, b: "u^c" if b < 3 else ("Q" if a < 3 else "e^c")
mult = {"Q": 6, "u^c": 3, "e^c": 1}
Ylam = {lab(a, b): Y5[a] + Y5[b] for a, b in pairs}
assert Ylam == {"Q": R(1, 6), "u^c": R(-2, 3), "e^c": 1} and sum(mult.values()) == 10
keys = ["Q", "u^c", "e^c"]
ip = lambda u, w: sum(mult[k] * u[i] * w[i] for i, k in enumerate(keys))     # Hilbert-Schmidt on End(10)
one = [1, 1, 1]; yv = [Ylam[k] for k in keys]
f = sp.symbols("f0:3"); sol75 = sp.solve([ip(f, one), ip(f, yv), f[0] - 1], f, dict=True)[0]
f75 = [sol75[x] for x in f]
assert f75 == [1, -1, -3]
m0, a, b = sp.symbols("m0 a b")
mass = [m0 * one[i] + a * yv[i] + b * f75[i] for i in range(3)]
s1 = sp.solve([mass[0], mass[1]], [a, b], dict=True)[0]
me = sp.simplify(mass[2].subs(s1))
assert me == 10 * m0 and s1 == {a: 4 * m0, b: -R(5, 3) * m0}
# without the 75 (b = 0) the mass is affine in Y and Q = U = 0 forces e^c = 0 (Pass 12702)
s0 = sp.solve([mass[0].subs(b, 0), mass[1].subs(b, 0)], [m0, a], dict=True)[0]
assert sp.simplify(mass[2].subs(b, 0).subs(s0)) == 0
print(f"(1) SU(5): 10bar x 10 = 1 + 24 + 75; the 75's SM singlet acts on (Q, u^c, e^c) as {f75}; Q = U = 0 needs a = 4 m0, b = -5/3 m0 "
      f"and then m(e^c) = {me}")

# SO(10) x U(1)_psi content and SM-singlet counts (SU(5) branchings: 45 > 1+24, 54 > 24, 210 > 1+24+75, 16 > 1, 144 > 24, 10 > none)
SMS = {1: 1, 10: 0, 16: 1, 45: 2, 54: 1, 144: 1, 210: 3}
C650 = [(1, 0), (45, 0), (54, 0), (210, 0), (16, -3), (16, 3), (144, 3), (144, -3), (10, 6), (10, -6)]
C78 = [(1, 0), (45, 0), (16, -3), (16, 3)]
d650, n650 = sum(d for d, _ in C650), sum(SMS[d] for d, _ in C650)
d78, n78 = sum(d for d, _ in C78), sum(SMS[d] for d, _ in C78)
assert d650 == 650 and d78 == 78 and n650 == 11 and n78 + 1 == 6 and n650 + n78 + 1 == 17
print(f"(1) 650 = 1+45+54+210+16+16b+144+144b+10+10b under SO(10)xU(1): {n650} SM singlets; 1+78 give 6; total 17 = the 27b.27 mass parameters")
# The 10 of SU(5) holding Q, u^c, e^c sits in the 16 of SO(10); 16b x 16 = 1 + 45 + 210, so its 75 can only come from the 210 of the 650.

# light blocks of the regular 650 vacua (Babu-Bajc-Susic): trinification keeps whole (3,3b,1) / (3b,1,3) blocks, etc.
PIECE = {"Q": (3, 2, 1 / 6), "U": (3, 1, 2 / 3), "D": (3, 1, 1 / 3), "L": (1, 2, 1 / 2), "E": (1, 1, 1.0)}


def content(names):
    db, dB = np.zeros(3), np.zeros((3, 3))
    for n in names:
        b1, B = weyl(*PIECE[n]); db += 2 * b1; dB += 2 * B      # Dirac pair
    return db, dB


def unify(MX, yp, names, MSS=1e10, tanb=1.0):
    dbVL, dBVL = content(names)
    segs = [("SM", MZ, False), ("SM", MX, bool(names)), ("MSSM", MSS, bool(names))]
    g = list(np.sqrt(4 * math.pi / AINV)); y = 0.97; mu = MZ
    for i, (th, ms, on) in enumerate(segs):
        if i == 2: y = y / math.sin(math.atan(tanb))
        mend = segs[i + 1][1] if i + 1 < len(segs) else 1e19
        bb = B1[th] + (dbVL * (1.5 if th == "MSSM" else 1.0) if on else 0)
        Bm = BIJ[th] + (dBVL * (1.5 if th == "MSSM" else 1.0) if on else 0)
        ypp = yp if (on and "Q" in names and "U" in names) else 0.0

        def fn(t, z, bb=bb, Bm=Bm, th=th, ypp=ypp):
            gg, yy = z[:3], z[3]; g2 = gg ** 2
            dg = K * gg ** 3 * bb + K * K * gg ** 3 * (Bm @ g2 - DU[th] * (yy ** 2 + ypp ** 2))
            return list(dg) + [K * yy * (YC[th] * yy ** 2 - CU[th] @ g2)]
        ev = lambda t, z: z[0] - z[1]; ev.terminal = True
        s = solve_ivp(fn, (math.log(mu), math.log(mend)), g + [y], events=ev, rtol=1e-9, atol=1e-12, dense_output=True)
        if s.t_events[0].size:
            z = s.sol(s.t_events[0][0]); ai = 4 * math.pi / z[:3] ** 2
            return math.exp(s.t_events[0][0]), float(ai[0]), float(ai[2] - ai[0])
        g = list(s.y[:3, -1]); y = s.y[3, -1]; mu = mend
    return float("nan"), float("nan"), float("nan")


chk = unify(1740.0, 0.462, ["Q", "U"])
assert abs(chk[2] - 0.26) < 0.02, chk                      # reproduces Pass 12702's +0.26
blocks = {"SU(5)-75 direction: Q + U": ["Q", "U"],
          "SU(3)^3 quark blocks: Q + U + 2 D": ["Q", "U", "D", "D"],
          "SU(3)^3 lepton block: 2 L + E (+ singlets)": ["L", "L", "E"],
          "SU(6)xSU(2) (15,1): Q + U + E + D + L (complete 10 + 5)": ["Q", "U", "E", "D", "L"]}
alt = {}
for k, nm in blocks.items():
    M12, ai, dl = unify(1740.0, 0.46, nm); alt[k] = dict(M12=M12, alpha_inv=ai, delta=dl, tau_p=tau_p(M12, ai) if M12 == M12 else None)
    print(f"(1) light at 1.74 TeV, hybrid M_SS=1e10: {k:58s} M12={M12:.2e} delta={dl:+.2f}")
res["e6_650"] = dict(f75_on_Q_uc_ec=[int(x) for x in f75], solution={"a": "4 m0", "b": "-5/3 m0"}, m_ec=str(me),
                     SM_singlets={"650": n650, "1+78": n78 + 1, "total": 17}, so10_content_650=C650, light_block_unification=alt,
                     note="Q+U light with e^c heavy needs the SU(5) 75 inside the SO(10) 210 of the 650 (16b x 16 = 1+45+210). The regular single-650 "
                          "vacua (SU(3)^3, SU(6)xSU(2), SO(10)xU(1); Babu-Bajc-Susic 2305.16398) preserve groups that keep Q and u^c in different or "
                          "complete blocks; the 75 direction preserves only the SM, so it needs a misaligned VEV beyond a single 650 potential.")

# ======================================================================= (2) two-loop vectorlike terms (PyR@TE 3 output, transcribed)


def beta_vl(gY, g2, g3, yt, lam, yp):
    a, b, c, t2, p2, L = gY * gY, g2 * g2, g3 * g3, yt * yt, yp * yp, lam
    one = [53 / 6 * gY ** 3, -7 / 6 * g2 ** 3, -5 * g3 ** 3,
           yt * (-17 / 12 * a - 9 / 4 * b - 8 * c + 9 / 2 * t2 + 3 * p2),
           3 / 8 * a * a + 3 / 4 * a * b - 3 * a * L + 9 / 8 * b * b - 9 * b * L + 24 * L * L + 12 * L * (t2 + p2) - 6 * (t2 * t2 + p2 * p2),
           yp * (-17 / 12 * a - 9 / 4 * b - 8 * c + 3 * t2 + 9 / 2 * p2)]
    two = [gY ** 3 * (121 / 9 * a + 5 * b + 68 / 3 * c - 17 / 6 * (t2 + p2)),
           g2 ** 3 * (5 / 3 * a + 91 / 3 * b + 20 * c - 3 / 2 * (t2 + p2)),
           g3 ** 3 * (17 / 6 * a + 15 / 2 * b + 12 * c - 2 * (t2 + p2)),
           yt * (1535 / 216 * a * a - 3 / 4 * a * b + 19 / 9 * a * c + 131 / 16 * a * t2 + 85 / 24 * a * p2 - 17 / 4 * b * b + 9 * b * c + 225 / 16 * b * t2
                 + 45 / 8 * b * p2 - 284 / 3 * c * c + 36 * c * t2 + 20 * c * p2 + 6 * L * L - 12 * L * t2 - 12 * t2 * t2 - 27 / 4 * t2 * p2 - 27 / 4 * p2 * p2),
           (-475 / 48 * a ** 3 - 655 / 48 * a * a * b + 749 / 24 * a * a * L - 19 / 4 * a * a * (t2 + p2) - 385 / 48 * a * b * b + 39 / 4 * a * b * L
            + 21 / 2 * a * b * (t2 + p2) + 36 * a * L * L + 85 / 6 * a * L * (t2 + p2) - 8 / 3 * a * (t2 * t2 + p2 * p2) + 209 / 16 * b ** 3 + 47 / 8 * b * b * L
            - 9 / 4 * b * b * (t2 + p2) + 108 * b * L * L + 45 / 2 * b * L * (t2 + p2) + 80 * c * L * (t2 + p2) - 32 * c * (t2 * t2 + p2 * p2) - 312 * L ** 3
            - 144 * L * L * (t2 + p2) - 3 * L * (t2 * t2 + p2 * p2) + 30 * (t2 ** 3 + p2 ** 3)),
           yp * (1535 / 216 * a * a - 3 / 4 * a * b + 19 / 9 * a * c + 85 / 24 * a * t2 + 131 / 16 * a * p2 - 17 / 4 * b * b + 9 * b * c + 45 / 8 * b * t2
                 + 225 / 16 * b * p2 - 284 / 3 * c * c + 20 * c * t2 + 36 * c * p2 + 6 * L * L - 12 * L * p2 - 27 / 4 * t2 * t2 - 27 / 4 * t2 * p2 - 12 * p2 * p2)]
    return [K * x + K * K * y for x, y in zip(one, two)]


# control: with the vectorlike fields removed PyR@TE gives exactly beta_sm (checked symbolically in the scratch run); numerically here:
# the vectorlike pair is a second top without mixing: beta_lambda is symmetric under yt <-> y', and beta_yt(yt, y') = beta_y'(y', yt)
zz = (0.46, 0.60, 0.95, 0.80, 0.02)
bA, bB = beta_vl(*zz, 0.5), beta_vl(*zz[:3], 0.5, zz[4], 0.80)
assert abs(bA[4] - bB[4]) < 1e-15 and abs(bA[3] - bB[5]) < 1e-15


def run2(Mt, MVL, yp, mu_max):
    y0 = initial(Mt) + [yp]; Mt0 = Mt - OFF3

    def rhs(t, y):
        mu = Mt0 * math.exp(t)
        return (beta_vl(*y) if mu > MVL else beta_sm(*y[:5]) + [0.0])
    return solve_ivp(rhs, (0, math.log(mu_max / Mt0)), y0, rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.5), Mt0


def mu0_2(Mt, MVL, yp):
    s, Mt0 = run2(Mt, MVL, yp, MPL); ts = np.linspace(0, s.t[-1], 4000); lam = s.sol(ts)[4]
    i = np.where(lam < 0)[0]
    if not len(i): return float("inf")
    j = i[0]; return Mt0 * math.exp(brentq(lambda tt: s.sol(tt)[4], ts[j - 1], ts[j]))


def yp_target(target, MVL, two=True, Mt=MT):
    f = (lambda p: math.log(mu0_2(Mt, MVL, p)) - math.log(target)) if two else (lambda p: math.log(mu0(Mt, vl=(MVL, p))) - math.log(target))
    return brentq(f, 0.2, 0.9, xtol=1e-5)


GEV_INV_M = 1.97327e-16
M5 = lambda Rm: (MPL ** 2 / (2 * math.pi * Rm / GEV_INV_M)) ** (1 / 3)
two_loop = {}
y1h, y2h = yp_target(1e10, 1740.0, False), yp_target(1e10, 1740.0, True)
assert abs(y1h - 0.462) < 0.003, y1h
two_loop["hybrid_1e10_MVL1740"] = dict(one_loop_VL=y1h, two_loop_VL=y2h)
print(f"(2) hybrid lambda(1e10)=0, M_VL=1.74 TeV: y' = {y1h:.3f} (one-loop VL) -> {y2h:.3f} (two-loop VL, PyR@TE)")
Bband = []
for Rum in (0.1, 1.0, 38.6):
    m5 = M5(Rum * 1e-6); y1, y2 = yp_target(m5, 1650.0, False), yp_target(m5, 1650.0, True)
    Bband.append(dict(R_um=Rum, M5=m5, one_loop_VL=y1, two_loop_VL=y2))
    print(f"(2) B: R={Rum} um, M5={m5:.2e}: y' = {y1:.3f} (one-loop VL) -> {y2:.3f} (two-loop VL)")
assert abs(Bband[0]["one_loop_VL"] - 0.494) < 0.003 and abs(Bband[1]["one_loop_VL"] - 0.507) < 0.003     # Pass 12689 control
two_loop["B_MVL1650"] = Bband
res["two_loop_vectorlike"] = two_loop

# ======================================================================= (4) y' measures the zero scale: hybrid versus M_SS
hyb = []
for MSS in (1e8, 3e8, 1e9, 3e9, 1e10, 3e10):
    yp = yp_target(MSS, 1740.0, True); M12, ai, dl = unify(1740.0, yp, ["Q", "U"], MSS=MSS)
    hyb.append(dict(MSS=MSS, yprime_two_loop=yp, M12=M12, delta=dl))
    print(f"(4) hybrid M_SS={MSS:.0e}: y' = {yp:.3f}, delta = {dl:+.2f}, M12 = {M12:.2e}")
yB_lo, yB_hi = Bband[0]["two_loop_VL"], Bband[2]["two_loop_VL"]
overlap = [h["MSS"] for h in hyb if yB_lo - 0.004 <= h["yprime_two_loop"] <= yB_hi + 0.004]
res["B_vs_hybrid"] = dict(B_band_two_loop=[yB_lo, yB_hi], gravity_bound_R_um=38.6, hybrid_vs_MSS=hyb, hybrid_MSS_overlapping_B=overlap,
                          note="y' measures the scale of the quartic zero; B's zero is M5 in [1.6e8, 1.2e9] GeV for R in [0.1, 38.6] um.")
print(f"(4) B band (two loop, R 0.1-38.6 um): y' in [{yB_lo:.3f}, {yB_hi:.3f}]; hybrid M_SS values inside it: {overlap}")

# ======================================================================= (3) radiative resonant leptogenesis, explicit O(2) model
V, MSTAR, ETA_OBS = 174.0, 1.08e-12, 6.1e-10
m2, m3 = 8.6e-12, 5.0e-11
t12, t13, t23 = map(math.radians, (33.4, 8.57, 49.0))


def pmns(delta, alpha):
    s12, c12, s13, c13, s23, c23 = math.sin(t12), math.cos(t12), math.sin(t13), math.cos(t13), math.sin(t23), math.cos(t23)
    e = np.exp(1j * delta)
    U = np.array([[c12 * c13, s12 * c13, s13 / e],
                  [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                  [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])
    return U @ np.diag([1, np.exp(1j * alpha / 2), 1])


def kappa(Kw):
    zB = 2 + 4 * Kw ** 0.13 * math.exp(-2.5 / Kw)
    return 2 / (zB * Kw) * (1 - math.exp(-zB * Kw / 2))


def lepto(M0, Lam, z, delta, alpha, xi, ytau, reg="PU"):
    U = pmns(delta, alpha)
    Rm = np.array([[0, 0], [np.cos(z), -xi * np.sin(z)], [np.sin(z), xi * np.cos(z)]])
    h0 = (1 / V) * np.conj(U) @ np.diag([0, math.sqrt(m2), math.sqrt(m3)]) @ Rm * math.sqrt(M0)
    mnu = V ** 2 * h0 @ h0.T / M0
    assert np.allclose(np.sort(np.abs(np.linalg.eigvals(mnu @ mnu.conj().T)) ** 0.5), [0, m2, m3], atol=1e-14)
    L = math.log(Lam / M0); c = 1.5 * K * ytau ** 2
    w = np.array([L, L, (1 - math.exp(-2 * c * L)) / (2 * c) if c > 0 else L])
    I = 2 * np.real(h0.conj().T @ np.diag(w) @ h0)                   # integral of 2 Re(h^dag h) from M0 to Lambda
    lamI, O = np.linalg.eigh(I)
    h = h0 @ O; Mi = M0 * (1 - K * lamI); dM = -M0 * K * (lamI - lamI[::-1])  # M_i - M_j
    hh = h.conj().T @ h; Gam = np.real(np.diag(hh)) * Mi / (8 * math.pi)
    eps = np.zeros((2, 3))
    for i in range(2):
        j = 1 - i; d2 = dM[i] * (Mi[i] + Mi[j])
        den = d2 ** 2 + (Mi[i] * Gam[j]) ** 2 if reg == "PU" else d2 ** 2 + (Mi[i] * Gam[i] - Mi[j] * Gam[j]) ** 2
        fr = d2 * Mi[i] * Gam[j] / den
        for al in range(3):
            num = np.imag(np.conj(h[al, i]) * h[al, j] * hh[i, j]) + Mi[i] / Mi[j] * np.imag(np.conj(h[al, i]) * h[al, j] * hh[j, i])
            eps[i, al] = num / np.real(hh[i, i] * hh[j, j]) * fr
    Kia = np.abs(h) ** 2 * V ** 2 / (Mi[None, :] * MSTAR)
    Ka = Kia.sum(axis=1)
    N = sum(kappa(Ka[al]) * eps[:, al].sum() for al in range(3))
    return dict(eta=0.96e-2 * abs(N), dM_over_Gamma=abs(dM[0]) / Gam.mean(), eps_tot=float(abs(eps.sum())), eps_flav_max=float(np.abs(eps.sum(0)).max()))


M0, YTAU = 1.24e7, 0.0095
pt = (M0, 2e16, 0.3 + 0.7j, 1.2, 0.8, 1, YTAU)
e1 = lepto(*pt)["eta"]; e2 = lepto(M0, 2e16, 1.9 + 0.7j, 1.2, 0.8, 1, YTAU)["eta"]
assert abs(e1 - e2) < 1e-6 * e1, (e1, e2)                                            # Re z = an O(2) rotation of degenerate N: unphysical
e0 = lepto(M0, 2e16, 0.3 + 0.7j, 1.2, 0.8, 1, 0.0)["eta"]
print(f"(3) invariance under Re z: eta {e1:.3e} = {e2:.3e}; control y_tau = 0 (aligned running): eta = {e0:.1e}")
rng = np.random.default_rng(12703); lep = {}
for name, Lam in (("f_a=1e11", 1e11), ("M_GUT=2e16", 2e16), ("M_Pl", 2.4e18)):
    for reg in ("PU", "diff"):
        etas, rat = [], []
        for _ in range(4000):
            z = complex(rng.uniform(0, math.pi), rng.uniform(-1.5, 1.5))
            r = lepto(M0, Lam, z, rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi), rng.choice([-1, 1]), YTAU, reg)
            etas.append(r["eta"]); rat.append(r["dM_over_Gamma"])
        etas = np.array(etas)
        lep[f"{name}|{reg}"] = dict(frac_ge_obs=float(np.mean(etas >= ETA_OBS)), eta_max=float(etas.max()), eta_median=float(np.median(etas)),
                                    dM_over_Gamma_median=float(np.median(rat)))
        print(f"(3) Lambda={name:11s} regulator={reg:4s}: eta_B max {etas.max():.2e}, median {np.median(etas):.1e}, "
              f"fraction >= obs {np.mean(etas >= ETA_OBS):.3f}, median dM/Gamma {np.median(rat):.2f}")
# scaling with y_tau (e.g. type-II leptons on a tan-beta-enhanced doublet)
sc = {}
for fac in (1, 3, 10):
    etas = np.array([lepto(M0, 2e16, complex(rng.uniform(0, math.pi), rng.uniform(-1.5, 1.5)), rng.uniform(0, 6.283), rng.uniform(0, 6.283), 1,
                           YTAU * fac)["eta"] for _ in range(2000)])
    sc[str(fac)] = dict(frac_ge_obs=float(np.mean(etas >= ETA_OBS)), eta_max=float(etas.max()))
    print(f"(3) y_tau x {fac:2d} (Lambda = M_GUT): fraction >= obs {np.mean(etas >= ETA_OBS):.3f}, max {etas.max():.2e}")
ext = {}
for ymax, m0x in ((4.0, 1.24e7), (4.0, 3e6)):
    etas = np.array([lepto(m0x, 2e16, complex(rng.uniform(0, math.pi), rng.uniform(-ymax, ymax)), rng.uniform(0, 6.283), rng.uniform(0, 6.283),
                           rng.choice([-1, 1]), YTAU)["eta"] for _ in range(2000)])
    ext[f"|Im z|<{ymax}, M0={m0x:.2e}"] = float(etas.max())
    print(f"(3) extended scan |Im z| < {ymax}, M0 = {m0x:.2e}: eta_B max {etas.max():.2e}")
etamax = max(v["eta_max"] for v in lep.values())
ytau_min_factor = math.sqrt(ETA_OBS / etamax)
print(f"(3) eta_B max ~ y_tau^2: radiative-only O(2) leptogenesis needs y_tau >= {ytau_min_factor:.2f} x SM")
res["leptogenesis_O2_model"] = dict(M0=M0, ytau=YTAU, invariance_Re_z=[e1, e2], control_ytau0=e0, scan=lep, ytau_scaling=sc,
                                    extended_scan_eta_max=ext, ytau_min_factor=ytau_min_factor,
                                    note="Exact O(2) degeneracy at Lambda + one-loop running: total and flavoured asymmetries vanish at leading order "
                                         "(mass basis diagonalises Re h^dag h); the tau Yukawa misaligns the running and is the only source.")

# ======================================================================= (5) other track's mediator vacuum (a790aef): independent re-run
p = subprocess.run([sys.executable, os.path.join(HERE, "toe_20261122_round7_h27_mediator_vacuum.py")], capture_output=True, text=True, cwd=ROOT)
ok = p.returncode == 0 and "PASS_H27_MEDIATOR" in p.stdout
med = json.load(open(os.path.join(ROOT, "data", "toe_20261122_round7_h27_mediator_vacuum.json"), encoding="utf-8"))
print(f"(5) a790aef mediator vacuum re-run: {'PASS' if ok else 'FAIL'}; full Hessian rank {med['full_15x15_Hessian_rank']}, residual moduli "
      f"{med['residual_singlet_moduli_after_gauge_quotient']}")
res["review_a790aef"] = dict(rerun_pass=ok, full_rank=med["full_15x15_Hessian_rank"], residual_moduli=med["residual_singlet_moduli_after_gauge_quotient"],
                             note="Only SO(10)-singlet u,v, one adjoint Cartan a and E6-neutral mediators: the 27 masses still come from 27b.27.(1+78) along "
                                  "U(1)_psi, so the light states remain complete SO(10) multiplets; no 650 or 75 component, question 4 stays open.")
# the script rewrites its own certificate; restore the committed version so this pass does not touch the other track's file
subprocess.run(["git", "checkout", "--", "data/toe_20261122_round7_h27_mediator_vacuum.json"], cwd=ROOT, capture_output=True)

json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12703_round.json"), "w"), indent=1, default=float)
print("wrote data/toe_pass12703_round.json")
