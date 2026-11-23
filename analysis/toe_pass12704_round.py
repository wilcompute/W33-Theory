"""Pass 12704 (Claude track): five follow-ups to Pass 12703.
 (1) SO(10) truncation of the 650 question: explicit Gamma-matrix construction of the 16, the SM-singlet directions of the 210 (p, a, omega)
     and 45 (B-L, T3R), the renormalizable invariants, and all F-flat vacua of (a) a 210 alone and (b) 45 + 210.  Can 16b (M + eta45 45 +
     eta210 210) 16 leave Q + U light with every other state of the 16 heavy?
 (2) Completion A with the tau on the PQ-charged doublet (b + tau, Pass 12696): how large must tan beta be for radiative-only leptogenesis
     (Pass 12703 needs y_tau >= 1.83 x SM)?  Two cases: N couples to the same doublet as tau (Y_e term -3/2) or to the other (+1/2).
 (3) Tree-level O(2)-breaking splitting delta = (M2 - M1)/M of random orientation: the window of delta that gives eta_B >= obs.
 (4) B's dark-graviton dark matter (Gonzalo-Montero-Obied-Vafa 2209.09249; Law-Smith-Obied-Prabhu-Vafa 2307.11048): its natural radius
     range 1-30 um maps to a narrower y' band.
 (5) Forecast: FCC-ee (M_t, alpha_s) + FCC-hh (y') -> inferred scale of the quartic zero; separation of B from the hybrid versus M_SS.
usage: py -3 analysis/toe_pass12704_round.py"""
import itertools, json, math, os
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)   # (1)-(2) of 12703: run2 etc.
for k in ("K", "MPL", "initial", "beta_sm", "beta_vl", "OFF3", "unify", "M5"): globals()[k] = G[k]
G3 = {"math": math, "np": np}
exec(src03.split("V, MSTAR, ETA_OBS")[1].split("def lepto")[0].join(["V, MSTAR, ETA_OBS", ""]), G3)
V, MSTAR, ETA_OBS, m2, m3, pmns, kappa = (G3[k] for k in ("V", "MSTAR", "ETA_OBS", "m2", "m3", "pmns", "kappa"))
res = {}

# ======================================================================= (1) SO(10): 45 + 210 and a light Q + U
s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -1j], [1j, 0]]); s3 = np.diag([1, -1]).astype(complex); I2m = np.eye(2)


def kron(*a):
    r = np.eye(1)
    for x in a: r = np.kron(r, x)
    return r


GM = []
for k in range(5):
    GM.append(kron(*([s3] * k + [s1] + [I2m] * (4 - k)))); GM.append(kron(*([s3] * k + [s2] + [I2m] * (4 - k))))
for i in range(10):
    for j in range(10): assert np.allclose(GM[i] @ GM[j] + GM[j] @ GM[i], 2 * (i == j) * np.eye(32))
G11 = (-1j) ** 5 * np.linalg.multi_dot(GM)
w = np.array([np.real(np.diag(-1j * (GM[2 * k] @ GM[2 * k + 1] - GM[2 * k + 1] @ GM[2 * k]) / 4)) for k in range(5)]).T
idx = [i for i in range(32) if abs(G11[i, i] - 1) < 1e-9]
BLq = 2 / 3 * w[idx, :3].sum(1); T3R = (w[idx, 3] + w[idx, 4]) / 2; Yq = T3R + BLq / 2
NAME = {1: "Q", -4: "u^c", 2: "d^c", -3: "L", 6: "e^c", 0: "nu^c"}
lab = [NAME[int(round(y * 6))] for y in Yq]
assert sorted(lab) == sorted(["Q"] * 6 + ["u^c"] * 3 + ["d^c"] * 3 + ["L"] * 2 + ["e^c", "nu^c"])
ST = ["Q", "u^c", "d^c", "L", "e^c", "nu^c"]


def form(terms, n):
    T = np.zeros((10,) * n)
    for ind, c in terms:
        for perm in itertools.permutations(range(n)):
            T[tuple(ind[q] for q in perm)] += c * round(np.linalg.det(np.eye(n)[list(perm)]))
    return T


def gam_on_16(T, n):
    M = np.zeros((32, 32), complex)
    for ind in itertools.combinations(range(10), n):
        if T[ind]: M += T[ind] * np.linalg.multi_dot([GM[x] for x in ind] + [np.eye(32)])
    return M[np.ix_(idx, idx)]


def blockvals(M):
    out = {}
    for b in ST:
        ii = [i for i in range(16) if lab[i] == b]; sub = M[np.ix_(ii, ii)]
        assert np.allclose(sub, sub[0, 0] * np.eye(len(ii))); out[b] = sub[0, 0]
    return out


def singlet_dim(n):
    mats = [gam_on_16(form([(f, 1)], n), n) for f in itertools.combinations(range(10), n)]
    rows = [[m[i, j] for m in mats] for i in range(16) for j in range(16) if i != j]
    for b in ST:
        ii = [i for i in range(16) if lab[i] == b]
        rows += [[m[i, i] - m[ii[0], ii[0]] for m in mats] for i in ii[1:]]
    A = np.array(rows); s = np.linalg.svd(np.vstack([A.real, A.imag]), compute_uv=False)
    return len(mats) - int(np.sum(s > 1e-9))


n210, n45 = singlet_dim(4), singlet_dim(2)
assert (n210, n45) == (3, 2)
J = [(0, 1), (2, 3), (4, 5)]; S4 = [(6, 7), (8, 9)]
F = dict(p=form([((6, 7, 8, 9), 1)], 4), a=form([((0, 1, 2, 3), 1), ((0, 1, 4, 5), 1), ((2, 3, 4, 5), 1)], 4),
         w=form([(c + s, 1) for c in J for s in S4], 4), A=form([(c, 1) for c in J], 2), B=form([(s, 1) for s in S4], 2))
CL = {k: blockvals(gam_on_16(T, 4 if k in "paw" else 2)) for k, T in F.items()}
CL = {k: {X: (v.real if k in "paw" else v.imag) for X, v in d.items()} for k, d in CL.items()}   # 45 coupling: Hermitian generator
p, a, wv, Av, Bv = sp.symbols("p a w A B")
I2 = sum(sp.Rational(round(np.einsum("abcd,abcd", F[x], F[y]))) * X * Y for x, X in zip("paw", (p, a, wv)) for y, Y in zip("paw", (p, a, wv)))
I3 = sum(sp.Rational(round(np.einsum("abcd,cdef,efab", F[x], F[y], F[z]))) * X * Y * Z
         for x, X in zip("paw", (p, a, wv)) for y, Y in zip("paw", (p, a, wv)) for z, Z in zip("paw", (p, a, wv)))
Q2 = sum(sp.Rational(round(np.einsum("ab,ab", F[x], F[y]))) * X * Y for x, X in zip("AB", (Av, Bv)) for y, Y in zip("AB", (Av, Bv)))
MX = sum(sp.Rational(round(np.einsum("ab,cd,abcd", F[x], F[y], F[z]))) * X * Y * Z
         for x, X in zip("AB", (Av, Bv)) for y, Y in zip("AB", (Av, Bv)) for z, Z in zip("paw", (p, a, wv)))
I2, I3, Q2, MX = map(sp.expand, (I2, I3, Q2, MX))
assert sp.expand(I2 - 24 * (p ** 2 + 3 * a ** 2 + 6 * wv ** 2)) == 0 and sp.expand(I3 - 48 * (a ** 3 + 6 * a * wv ** 2 + 3 * p * wv ** 2)) == 0
print(f"(1) SO(10): SM singlets 210 -> {n210}, 45 -> {n45}; I2 = 24(p^2+3a^2+6w^2), I3 = 48(a^3+6aw^2+3pw^2) (minimal-SO(10) form); 45.45.210 = {MX}")
print("(1) Clebsches on (Q,u^c,d^c,L,e^c,nu^c): " + "; ".join(f"{k}: {[round(CL[k][X], 3) for X in ST]}" for k in CL))
c210 = lambda X: sp.nsimplify(CL["p"][X]) * p + sp.nsimplify(CL["a"][X]) * a + sp.nsimplify(CL["w"][X]) * wv
c45 = lambda X: sp.nsimplify(CL["A"][X]) * Av + sp.nsimplify(CL["B"][X]) * Bv

v210 = []
for s in sp.solve([sp.diff(I2 + I3, v) for v in (p, a, wv)], [p, a, wv], dict=True):
    m = {X: sp.simplify(c210(X).subs(s)) for X in ST}
    light = sorted(X for X in ST if sp.simplify(m[X] - m["Q"]) == 0)
    v210.append(dict(vev={str(k): str(v) for k, v in s.items()}, degenerate_with_Q=light))
    print(f"(1) 210 alone, vacuum {s}: states degenerate with Q (light together when Q is): {light}")
assert not any(r["degenerate_with_Q"] == ["Q", "u^c"] for r in v210)
Msym, e45 = sp.symbols("M e45")
hits, rows45 = 0, []
for m1, m2_, lam, kap in ((sp.Rational(1), sp.Rational(1), sp.Rational(1), sp.Rational(1, 2)), (sp.Rational(2), sp.Rational(1), sp.Rational(3, 2), sp.Rational(1)),
                          (sp.Rational(1, 3), sp.Rational(2), sp.Rational(1), sp.Rational(5, 4))):
    W2 = m1 * Q2 + m2_ * I2 + lam * I3 + kap * MX
    for s in sp.solve([sp.diff(W2, v) for v in (p, a, wv, Av, Bv)], [p, a, wv, Av, Bv], dict=True):
        if all(sp.simplify(s[v]) == 0 for v in (Av, Bv)) or any(abs(complex(sp.N(s[v])).imag) > 1e-12 for v in s): continue
        mass = {X: Msym + e45 * c45(X).subs(s) + c210(X).subs(s) for X in ST}           # eta210 = 1
        sol = sp.solve([mass["Q"], mass["u^c"]], [Msym, e45], dict=True)
        if not sol or set(sol[0]) != {Msym, e45}: continue
        rest = {X: float(sp.N(mass[X].subs(sol[0]))) for X in ("d^c", "L", "e^c", "nu^c")}
        ok = all(abs(v) > 1e-9 for v in rest.values()); hits += ok
        rows45.append(dict(params=[str(m1), str(m2_), str(lam), str(kap)], vev={str(k): float(sp.N(v)) for k, v in s.items()}, others=rest, QU_only=ok))
        if ok: print(f"(1) 45+210 vacuum {({str(k): round(float(sp.N(v)), 3) for k, v in s.items()})}: Q = U = 0 at M, eta45 tuned; others {({k: round(v, 3) for k, v in rest.items()})}")
assert hits > 0
res["so10_light_QU"] = dict(singlets={"210": n210, "45": n45}, invariants={"I2": str(I2), "I3": str(I3), "Q2": str(Q2), "45.45.210": str(MX)},
                            clebsch={k: {X: float(v) for X, v in d.items()} for k, d in CL.items()}, vacua_210_only=v210,
                            vacua_45_210=rows45, n_QU_only=hits,
                            note="210 alone: no F-flat vacuum makes Q and u^c degenerate without d^c or e^c (all-quark, SU(5) or flipped multiplets). "
                                 "45+210: real vacua with p, a and <45> along T3R (unbroken SU(3)xSU(2)xU(1)_RxU(1)_B-L) give Q = U = 0 with d^c, L, e^c, "
                                 "nu^c heavy, at two tuned couplings (M, eta45). E6 reading: the 650's 45 and 210 parts share one coupling, so an "
                                 "independent 45 coupling needs a 78 with a non-psi VEV (or a second 650).")

# ======================================================================= (2)+(3) leptogenesis: tau on the PQ doublet, tree-level splitting


def lepto(M0, Lam, z, delta, alpha, xi, ytau, cY=1.5, dtree=0.0, th=0.0):
    U = pmns(delta, alpha)
    Rm = np.array([[0, 0], [np.cos(z), -xi * np.sin(z)], [np.sin(z), xi * np.cos(z)]])
    h0 = (1 / V) * np.conj(U) @ np.diag([0, math.sqrt(m2), math.sqrt(m3)]) @ Rm * math.sqrt(M0)
    L = math.log(Lam / M0); c = cY * K * ytau ** 2
    wv_ = np.array([L, L, (1 - math.exp(-2 * c * L)) / (2 * c) if c > 0 else L])
    S = -K * 2 * np.real(h0.conj().T @ np.diag(wv_) @ h0)
    Rt = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    S = S + dtree / 2 * Rt @ np.diag([-1, 1]) @ Rt.T
    sv, O = np.linalg.eigh(S); h = h0 @ O; Mi = M0 * (1 + sv); dM = M0 * (sv - sv[::-1])
    hh = h.conj().T @ h; Gam = np.real(np.diag(hh)) * Mi / (8 * math.pi); eps = np.zeros((2, 3))
    for i in range(2):
        j = 1 - i; d2 = dM[i] * (Mi[i] + Mi[j]); fr = d2 * Mi[i] * Gam[j] / (d2 ** 2 + (Mi[i] * Gam[j]) ** 2)
        for al in range(3):
            num = np.imag(np.conj(h[al, i]) * h[al, j] * hh[i, j]) + Mi[i] / Mi[j] * np.imag(np.conj(h[al, i]) * h[al, j] * hh[j, i])
            eps[i, al] = num / np.real(hh[i, i] * hh[j, j]) * fr
    Ka = (np.abs(h) ** 2 * V ** 2 / (Mi[None, :] * MSTAR)).sum(axis=1)
    return 0.96e-2 * abs(sum(kappa(Ka[al]) * eps[:, al].sum() for al in range(3))), abs(dM[0]) / Gam.mean()


M0, YT = 1.24e7, 0.0095
rng = np.random.default_rng(12704)
rnd = lambda: (complex(rng.uniform(0, math.pi), rng.uniform(-1.5, 1.5)), rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi), rng.choice([-1, 1]))
e_chk = max(lepto(M0, 2e16, *rnd(), YT)[0] for _ in range(1500))
assert 1.4e-10 < e_chk < 2.0e-10, e_chk                                  # Pass 12703: max 1.8e-10
need = math.sqrt(ETA_OBS / 1.80e-10)
tb = {}
for case, cY in (("N and tau on the same (PQ) doublet: -3/2", 1.5), ("N on the other doublet: +1/2", 0.5)):
    fac = need * math.sqrt(1.5 / cY); tanb = math.sqrt(fac ** 2 - 1)
    etas = np.array([lepto(M0, 2e16, *rnd(), YT * fac * 1.15, cY)[0] for _ in range(1500)])
    tb[case] = dict(ytau_factor_needed=fac, tan_beta_min=tanb, frac_ge_obs_at_1p15x=float(np.mean(etas >= ETA_OBS)))
    print(f"(2) {case}: y_tau >= {fac:.2f} x SM -> 1/cos(beta) >= {fac:.2f}, tan beta >= {tanb:.2f}; at 1.15x that: fraction >= obs {np.mean(etas >= ETA_OBS):.3f}")
res["tau_on_PQ_doublet"] = dict(cases=tb, axion="b + tau same sign (Pass 12696): E/N = 8/3, N_DW = 1, g_agg = 0.39 g_KSVZ, haloscope time x44",
                                note="Y_e term in dh/dt: -3/2 = +1/2 (lepton-doublet wave function) - 2 (vertex, needs the same doublet).")
win = []
for lg in np.arange(-15.0, -1.9, 1.0):
    vals = [lepto(M0, 2e16, *rnd(), YT, 1.5, 10 ** lg, rng.uniform(0, math.pi)) for _ in range(600)]
    etas = np.array([v[0] for v in vals]); rat = np.median([v[1] for v in vals])
    win.append(dict(log10_delta=float(lg), frac_ge_obs=float(np.mean(etas >= ETA_OBS)), eta_max=float(etas.max()), dM_over_Gamma=float(rat)))
    print(f"(3) tree splitting delta = 1e{lg:+.1f}: median dM/Gamma {rat:9.2e}, eta_B max {etas.max():.2e}, fraction >= obs {np.mean(etas >= ETA_OBS):.3f}")
okw = [r["log10_delta"] for r in win if r["frac_ge_obs"] > 0.05]
res["tree_splitting_window"] = dict(scan=win, window_log10_delta_frac_gt_5pct=[min(okw), max(okw)] if okw else None,
                                    spurion="delta = eps^n: with eps = y_tau ~ 0.01 the window needs n ~ 4.5")
print(f"(3) window (fraction > 5%): log10 delta in {res['tree_splitting_window']['window_log10_delta_frac_gt_5pct']}")

# ======================================================================= (4) B's dark-graviton DM band and (5) forecast


def run2a(Mt, a3, MVL, yp, mu_max):
    y0 = initial(Mt, 125.20, a3) + [yp]; Mt0 = Mt - OFF3
    rhs = lambda t, y: beta_vl(*y) if Mt0 * math.exp(t) > MVL else beta_sm(*y[:5]) + [0.0]
    return solve_ivp(rhs, (0, math.log(mu_max / Mt0)), y0, rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.5), Mt0


def ypt(target, MVL, Mt=172.57, a3=0.1180):
    def f(pp):
        s, Mt0 = run2a(Mt, a3, MVL, pp, target * 1.0001); return s.y[4, -1]
    return brentq(f, 0.2, 0.9, xtol=1e-6)


GEV_INV_M = 1.97327e-16
band = []
for Rum in (0.1, 1.0, 10.0, 20.0, 30.0):
    m5 = M5(Rum * 1e-6); yp = ypt(m5, 1650.0)
    band.append(dict(R_um=Rum, M5=m5, yprime=yp, m_KK_eV=GEV_INV_M / (Rum * 1e-6) * 1e9, mDM_rel_1um=(1.0 / Rum) ** (1 / 7)))
    print(f"(4) B: R = {Rum:5.1f} um, M5 = {m5:.2e}, m_KK = {GEV_INV_M / (Rum * 1e-6) * 1e9:.3f} eV: y' = {yp:.3f}; m_DM(today) relative to 1 um: x{(1 / Rum) ** (1 / 7):.2f}")
assert abs(band[0]["yprime"] - 0.495) < 0.004
res["B_dark_graviton_band"] = dict(rows=band, natural_range_um=[1, 30],
                                   note="2307.11048: natural l5_eff ~ 1-30 um; its eqs. (42)-(43) (read from a summary of the paper, to verify) need "
                                        "l5 >~ 20 um (delta/0.5)(lambda/0.1)^(2/3); m_DM today ~ m_KK^(1/7), only x0.6 over 1-30 um.")

h = 1e-3
mu_h, mu_B = 1e10, M5(1e-6)
der = {}
for nm, mu in (("hybrid@1e10", mu_h), ("B@1um", mu_B)):
    y = ypt(mu, 1740.0)
    dMt = (ypt(mu, 1740.0, Mt=172.57 + 0.1) - ypt(mu, 1740.0, Mt=172.57 - 0.1)) / 0.2
    das = (ypt(mu, 1740.0, a3=0.1180 + 0.0005) - ypt(mu, 1740.0, a3=0.1180 - 0.0005)) / 0.001
    dl = (ypt(mu * 10 ** 0.1, 1740.0) - ypt(mu * 10 ** -0.1, 1740.0)) / 0.2
    der[nm] = dict(yprime=y, dy_dMt=dMt, dy_dalphas=das, dy_dlog10mu=dl)
    print(f"(5) {nm}: y' = {y:.4f}, dy'/dM_t = {dMt:+.4f}/GeV, dy'/dalpha_s = {das:+.2f}, dy'/dlog10 mu0 = {dl:+.4f}")
SC = dict(today=dict(Mt=0.29, as_=0.0009, ym=0.002, th=0.002), fcc=dict(Mt=0.04, as_=0.0002, ym=0.002, th=0.002))
fore = {}
for scen, s in SC.items():
    d = der["hybrid@1e10"]
    sig_y = math.sqrt((d["dy_dMt"] * s["Mt"]) ** 2 + (d["dy_dalphas"] * s["as_"]) ** 2 + s["ym"] ** 2 + s["th"] ** 2)
    sig_log = sig_y / abs(d["dy_dlog10mu"])
    rows = []
    for MSS in (3e9, 1e10, 3e10):
        for RB, mB in (("R>=0.1um", M5(1e-7)), ("R>=1um", M5(1e-6)), ("R>=20um", M5(2e-5))):
            rows.append(dict(MSS=MSS, B=RB, decades=math.log10(MSS / mB), sigma=math.log10(MSS / mB) / sig_log))
    fore[scen] = dict(sigma_yprime=sig_y, sigma_log10_mu0=sig_log, separation=rows)
    print(f"(5) {scen}: sigma(y') = {sig_y:.4f}, sigma(log10 mu0) = {sig_log:.2f}; " + ", ".join(
        f"M_SS={r['MSS']:.0e}/{r['B']}: {r['sigma']:.1f}s" for r in rows if r["B"] != "R>=20um"))
res["forecast"] = dict(derivatives=der, scenarios=fore, inputs=SC,
                       note="y' measured at FCC-hh (+-0.002, Pass 12696); FCC-ee M_t +-0.04 GeV incl. theory, alpha_s +-0.0002; +-0.002 matching theory.")

json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12704_round.json"), "w"), indent=1, default=float)
print("wrote data/toe_pass12704_round.json")
