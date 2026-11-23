"""Pass 12725 (Claude track), items 1, 2, 4 (item 3: explore_pass12725_codelm*.py; item 5: the summary page).
 (1) SO(10) on S1/(Z2 x Z2') with Pati-Salam on one brane and SU(5) x U(1) on the other (Dermisek-Mafi-type): the 45 splits into parity
     classes (++) = PS cap SU(5)xU(1) (13, levels 2n/R), (+-) = PS only (8) and (-+) = SU(5)xU(1) only (12) (levels (2n+1)/R), (--) = rest (12,
     levels (2n+2)/R).  SM content from the so(10) machinery; N = 2 vector multiplets b_i = -2 sum(index); a 10_H hypermultiplet with doublets
     (++) and triplets at (2n+1)/R.  Shift of the predicted alpha_3^-1 vs M_s R.
 (2) Partially coupled dark sector for B': only a fraction f of the dark matter couples (m ~ e^{beta phi}); background + apparent CPL vs DESI
     DR2 + CMB + Pantheon+, and linear growth (coupled and uncoupled DM components) -> sigma8 ratio vs LambdaCDM.  Is there a point with
     chi2 < 4 and sigma8 ratio <= 1?
 (4) FCC-era y' floor: sigma(M_t) = 0.04 GeV (short-distance, no scheme), sigma(alpha_s) = 0.0002, threshold Z-term +-10%.
usage: py -3 analysis/explore_pass12725_round.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, fsolve

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}

# ======================================================================= (1)
src16 = open(os.path.join(HERE, "explore_pass12716_round.py"), encoding="utf-8").read()
blk = src16.split("# ======================================================================= (0) GIFT count")[1].split("bS, bH, eaten = ")[0]
G = {"np": np, "math": math}
exec(blk, G)
so10, comm, sm_content, commutant = G["so10"], G["comm"], G["sm_content"], G["commutant"]
u5 = commutant(G["J"])                                                       # u(5) = SU(5) x U(1), 25
P = np.diag([1.0] * 3 + [-1.0] * 2 + [1.0] * 3 + [-1.0] * 2)                # SO(6) x SO(4) on colour / weak coordinates
ps = [g for g in [sum(c * so10[i] for i, c in enumerate(v)) for v in np.linalg.svd(np.array([(P @ g - g @ P).ravel() for g in so10]).T)[2][-15:]]]
ps = commutant(P, ) if False else None
Cm = np.array([(P @ g - g @ P).ravel() for g in so10]).T
u_, s_, vh_ = np.linalg.svd(Cm); kps = int(np.sum(s_ < 1e-9))
ps = [sum(c * so10[i] for i, c in enumerate(v)) for v in vh_[-kps:]]
assert len(u5) == 25 and len(ps) == 21, (len(u5), len(ps))


def span(gs):
    A = np.array([g.ravel() for g in gs]).T; u, s, vh = np.linalg.svd(A, full_matrices=False)
    return u[:, :int(np.sum(s > 1e-9))]


Up, Uf = span(ps), span(u5); Uall = span(so10)
Pp, Pf = Up @ Up.T, Uf @ Uf.T
w, V = np.linalg.eigh((Pp + Pf) / 2)
both = V[:, w > 1 - 1e-6]                                                    # intersection
def proj_complement(B, *subs):
    M = B.copy()
    for S in subs: M = M - S @ (S.T @ M)
    u, s, vh = np.linalg.svd(M, full_matrices=False); return u[:, s > 1e-6]
psonly = proj_complement(Up, both); fonly = proj_complement(Uf, both); rest = proj_complement(Uall, Up, Uf)
cls = {"++": both, "+-": psonly, "-+": fonly, "--": rest}
print("(1) SO(10) parity classes: " + ", ".join(f"{k}: {v.shape[1]}" for k, v in cls.items()))
assert [v.shape[1] for v in cls.values()] == [13, 8, 12, 12]


def bvec(content):
    b = np.zeros(3)
    for key, cnt in content.items():
        r3, r2 = key.split(")")[0][1:].split(","); y = float(key.split(")")[1])
        i3 = {"1": 0, "3": 1 / 6, "8": 3 / 8}.get(r3, 0); i2 = {"1": 0, "2": 1 / 4, "3": 2 / 3}.get(r2, 0)
        b += cnt * np.array([0.6 * y * y, i2, i3])
    return -2 * b


bcls = {}
for k, Bm in cls.items():
    gens = [Bm[:, j].reshape(10, 10) for j in range(Bm.shape[1])]
    c = sm_content(gens); bcls[k] = bvec(c)
    print(f"(1) class {k}: SM content {dict(sorted(c.items()))} -> b = {np.round(bcls[k], 3)}")
bH_doublet = np.array([0.6, 2.0, 0.0]); bH_triplet = np.array([0.267, 0.0, 2.0])
orb = []
for MsR in (10, 15, 30, 100):
    lv = lambda start, step: [start + step * n for n in range(0, 400) if start + step * n < MsR and start + step * n > 0]
    S = lambda levels: sum(math.log(MsR / m) for m in levels)
    d = (bcls["++"] * S(lv(2, 2)) + (bcls["+-"] + bcls["-+"]) * S(lv(1, 2)) + bcls["--"] * S(lv(2, 2)) + bH_doublet * S(lv(2, 2)) + bH_triplet * S(lv(1, 2))) / (2 * math.pi)
    D = d[2] - d[0] + 12 / 7 * (d[0] - d[1])
    orb.append(dict(MsR=MsR, shift=D))
    print(f"(1) SO(10) orbifold, M_s R = {MsR}: predicted alpha_3^-1 shift {D:+.2f}")
res["so10_orbifold"] = dict(b=dict((k, v.tolist()) for k, v in bcls.items()), rows=orb)

# ======================================================================= (2)
Ob, Om = 0.049, 0.31
w0c, s0, wac, sa, rho = -0.857, 0.057, -0.55, 0.235, -0.9
Cinv = np.linalg.inv(np.array([[s0 ** 2, rho * s0 * sa], [rho * s0 * sa, sa ** 2]]))
chi2 = lambda w0, wa: float(np.array([w0 - w0c, wa - wac]) @ Cinv @ np.array([w0 - w0c, wa - wac]))


def model(lam, beta, f):
    def run(V0, A):
        def rhs(N, y):
            phi, dphi = y
            rb = 3 * Ob * math.exp(-3 * N); r1 = f * A * math.exp(-3 * N) * math.exp(beta * phi); r2 = (1 - f) * A * math.exp(-3 * N)
            V = V0 * math.exp(-lam * phi); H2 = (rb + r1 + r2 + V) / (3 - dphi ** 2 / 2)
            dlnH = -0.5 * (rb + r1 + r2 + H2 * dphi ** 2) / H2
            return [dphi, -(3 + dlnH) * dphi - (-lam * V + beta * r1) / H2]
        return solve_ivp(rhs, (-7.0, 0.0), [0.0, 0.0], rtol=1e-9, atol=1e-11, dense_output=True)
    def q(sol, V0, A, N):
        phi, dphi = sol.sol(N)
        rb = 3 * Ob * math.exp(-3 * N); r1 = f * A * math.exp(-3 * N) * math.exp(beta * phi); r2 = (1 - f) * A * math.exp(-3 * N)
        V = V0 * math.exp(-lam * phi); H2 = (rb + r1 + r2 + V) / (3 - dphi ** 2 / 2)
        return H2, rb, r1, r2, -0.5 * (rb + r1 + r2 + H2 * dphi ** 2) / H2, dphi
    def eqs(p):
        V0, A = abs(p[0]), abs(p[1]); sol = run(V0, A); H2, rb, r1, r2, _, _ = q(sol, V0, A, 0.0)
        return [H2 - 1, (rb + r1 + r2) / (3 * H2) - Om]
    V0, A = fsolve(eqs, [3 * 0.69, 3 * (Om - Ob)], xtol=1e-12); V0, A = abs(V0), abs(A); sol = run(V0, A)
    Q = lambda N: q(sol, V0, A, N)
    H0q = Q(0.0); r10, r20 = H0q[2], H0q[3]
    Ns = np.linspace(-1.1, 0, 160)
    rapp = np.array([3 * Q(N)[0] - Q(N)[1] - (r10 + r20) * math.exp(-3 * N) for N in Ns])
    wv = -1 - np.gradient(np.log(rapp), Ns) / 3; a = np.exp(Ns)
    w0, wa = np.linalg.lstsq(np.vstack([np.ones_like(a), 1 - a]).T, wv, rcond=None)[0]
    def grhs(N, y):
        d1, dd1, d2, dd2, db, ddb = y; H2, rb, r1, r2, dlnH, dphi = Q(N); o1, o2, ob = r1 / (3 * H2), r2 / (3 * H2), rb / (3 * H2)
        src = o1 * d1 + o2 * d2 + ob * db
        return [dd1, -(2 + dlnH - beta * dphi) * dd1 + 1.5 * (src + 2 * beta ** 2 * o1 * d1), dd2, -(2 + dlnH) * dd2 + 1.5 * src, ddb, -(2 + dlnH) * ddb + 1.5 * src]
    a0 = math.exp(-7.0)
    sg = solve_ivp(grhs, (-7.0, 0.0), [a0] * 6, rtol=1e-9, atol=1e-14)
    d1, _, d2, _, db, _ = sg.y[:, -1]; H2, rb, r1, r2, _, _ = Q(0.0)
    dm = (r1 * d1 + r2 * d2 + rb * db) / (r1 + r2 + rb)
    return w0, wa, float(wv.min()), dm


ref = model(1e-6, 0.0, 0.0)[3]
pts = []
for f in (0.2, 0.5, 1.0):
    for beta in (0.1, 0.2, 0.3, 0.45):
        for lam in (0.9, 1.1, 1.3):
            try:
                w0, wa, wmin, dm = model(lam, beta, f)
            except Exception:
                continue
            pts.append(dict(f=f, beta=beta, lam=lam, w0=w0, wa=wa, w_min=wmin, chi2=chi2(w0, wa), sigma8_ratio=dm / ref))
good = [p for p in pts if p["chi2"] < 4 and p["sigma8_ratio"] <= 1.0]
for p in sorted(pts, key=lambda r: r["chi2"])[:8]:
    print(f"(2) f = {p['f']}, beta = {p['beta']}, lambda = {p['lam']}: w0 {p['w0']:.3f}, wa {p['wa']:.3f}, min w {p['w_min']:.3f}, chi2 {p['chi2']:.2f}, sigma8 ratio {p['sigma8_ratio']:.3f}")
print(f"(2) points with chi2 < 4 and sigma8 ratio <= 1: {[(p['f'], p['beta'], p['lam'], round(p['chi2'], 2), round(p['sigma8_ratio'], 3)) for p in good] or 'none'}")
res["partial_coupling"] = dict(points=pts, good=good)

# ======================================================================= (4)
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G3 = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G3)
initial, beta_sm, beta_vl, OFF3 = (G3[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3"))
K = 1 / (16 * math.pi ** 2)


def lam_end(yp, tgt, Mt, a3, zf, mvl=1740.0):
    Mt0 = Mt - OFF3; kw = dict(rtol=1e-8, atol=1e-11, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(mvl / Mt0)), np.array(initial(Mt, 125.20, a3) + [yp]), **kw).y[:, -1].copy()
    y[4] += (5 / 6) * 3 * K * y[5] ** 4 - zf * 2 * y[4] * 3 * K * y[5] ** 2 / 3
    return solve_ivp(lambda t, y: beta_vl(*y), (math.log(mvl / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1][4]


rng = np.random.default_rng(1250); fl = []
for _ in range(30):
    Mt = 172.80 + rng.normal() * 0.04; a3 = 0.1180 + rng.normal() * 0.0002; zf = 1 + 0.1 * rng.uniform(-1, 1)
    ys = []
    for lg in (11, 12, 13):
        try: ys.append(brentq(lambda p: lam_end(p, 10 ** lg, Mt, a3, zf), 0.05, 1.2, xtol=1e-5))
        except ValueError: pass
    if ys: fl.append(min(ys))
fl = np.array(fl)
res["fcc_floor"] = dict(median=float(np.median(fl)), p2_5=float(np.percentile(fl, 2.5)), p97_5=float(np.percentile(fl, 97.5)))
print(f"(4) FCC-era y' floor: median {np.median(fl):.3f}, 95% range {np.percentile(fl, 2.5):.3f}-{np.percentile(fl, 97.5):.3f} (today: 0.351-0.469)")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12725_round.json"), "w"), indent=1, default=float)
print("wrote data/explore_pass12725_round.json")
