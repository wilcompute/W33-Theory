"""Second round on Yukawa chains.
(a) Universality classes.  Hop A = expm(e G), G complex Ginibre, e = disorder per step.  e large: Ginibre, r = ln(m3/m2)/ln(m2/m1) -> 1/2.  e small: Brownian motion on GL(3,C)/U(3), the DMPK limit of quantum wires, exponents 1 : 3 : 5, r -> 1.  Control: reproduce both limits.
(b) Strong CP: SL(3,C) hops, A -> A / det(A)^(1/3), give arg det Y = 0 exactly.  Compare J with and without.  Control: without, arg det is uniform.
(c) Quarks with Brownian chains: Y_u = Q U, Y_d = Q D with disorder e.  Score as flavor_lyapunov.py; J not scored, as an out-of-sample number: ln|J| data = -10.39.
(d) Fair comparison: marginal likelihood over a stated grid with uniform weight, for chains and for FN over a stated grid of charges, so neither is scored at its best point only.  Also a goodness p value: fraction of simulated points with larger Mahalanobis distance.
(e) Leptons, out of sample: Y_e = L E, neutrinos Weinberg M = L^T S L with S symmetric anarchic, normal ordering assumed by sorting.  Using L short and E long: does large PMNS and the mass-squared ratio come out?  Data: th12 33.4, th23 45 +- 4, th13 8.6 deg, dm21/dm31 = 0.0298, r_lepton = 0.529, span ln(mtau/me) = 8.18.
(f) RG reading: chain "time" against ln(M_UV/M_Z).  Only a scale comparison.
usage: py -3 flavor_chain2.py"""
import json
import math
import numpy as np
from scipy.linalg import expm

rng = np.random.default_rng(20261106)
base = json.load(open("flavor_lyapunov.json"))
M = dict(u=1.24e-3, c=0.62, t=171.0, d=2.69e-3, s=0.0535, b=2.85, e=0.4866e-3, mu=0.1027, tau=1.746)
DATA = np.array([math.log(M["t"] / M["c"]), math.log(M["c"] / M["u"]), math.log(M["b"] / M["s"]), math.log(M["s"] / M["d"]), math.log(0.2265), math.log(0.0405), math.log(0.00365)])
LNJ = math.log(3.08e-5)


def G(n):
    return (rng.standard_normal((n, 3, 3)) + 1j * rng.standard_normal((n, 3, 3))) / math.sqrt(2)


def mexp(X):
    w, V = np.linalg.eig(X)
    return V @ (np.exp(w)[:, None] * np.eye(3, dtype=complex)[None]) @ np.linalg.inv(V)


def hop(n, e, sl3=False):
    A = G(n) if e is None else mexp(e * G(n))
    if sl3:
        d = np.linalg.det(A)
        A = A / (d ** (1 / 3))[:, None, None]
    return A


def chain(n, L, e, sl3=False):
    P = np.broadcast_to(np.eye(3, dtype=complex), (n, 3, 3)).copy()
    for _ in range(L):
        P = P @ hop(n, e, sl3)
        P = P / np.linalg.norm(P, axis=(1, 2))[:, None, None]
    return P


def obs(Yu, Yd):
    Uu, su, _ = np.linalg.svd(Yu)
    Ud, sd, _ = np.linalg.svd(Yd)
    V = (np.conj(np.swapaxes(Uu, 1, 2)) @ Ud)[:, ::-1, :][:, :, ::-1]  # light to heavy: numpy returns singular values heaviest first, and without this t12 and t23 are swapped
    Va = np.abs(V)
    t12 = np.arctan2(Va[:, 0, 1], Va[:, 0, 0])
    t23 = np.arctan2(Va[:, 1, 2], Va[:, 2, 2])
    J = np.imag(V[:, 0, 1] * V[:, 1, 2] * np.conj(V[:, 0, 2]) * np.conj(V[:, 1, 1]))
    x = np.c_[np.log(su[:, 0] / su[:, 1]), np.log(su[:, 1] / su[:, 2]), np.log(sd[:, 0] / sd[:, 1]), np.log(sd[:, 1] / sd[:, 2]), np.log(np.sin(t12) + 1e-300), np.log(np.sin(t23) + 1e-300), np.log(Va[:, 0, 2] + 1e-300)]
    return x, np.log(np.abs(J) + 1e-300)


def score(x):
    x = x[np.all(np.isfinite(x), axis=1)]
    mu = x.mean(0)
    C = np.cov(x.T) + 1e-9 * np.eye(7)
    Ci = np.linalg.inv(C)
    d = DATA - mu
    c2 = float(d @ Ci @ d)
    dd = x - mu
    sim = np.einsum("ij,jk,ik->i", dd, Ci, dd)
    return -0.5 * c2 - 0.5 * np.linalg.slogdet(C)[1] - 3.5 * math.log(2 * math.pi), c2, float(np.mean(sim > c2)), mu, np.sqrt(np.diag(C))


out = {}
# (a) control
ctl = {}
for e, L in ((None, 30), (1.0, 20), (0.5, 50), (0.25, 150), (0.125, 500)):
    n = 1500
    s = np.linalg.svd(chain(n, L, e), compute_uv=False)
    ok = s[:, 2] > 1e-280
    r = np.log(s[ok, 0] / s[ok, 1]) / np.log(s[ok, 1] / s[ok, 2])
    span = np.median(np.log(s[ok, 0] / s[ok, 2]))
    ctl[str(e)] = dict(L=L, median_r=float(np.median(r)), span_per_step=float(span / L), kept=int(ok.sum()))
out["universality"] = ctl
print("universality", {k: (round(v["median_r"], 3), round(v["span_per_step"], 4)) for k, v in ctl.items()}, flush=True)
# (b)
n = 6000
Pg = chain(n, 6, None)
Ps = chain(n, 6, None, sl3=True)
ag = np.angle(np.linalg.det(Pg))
as_ = np.angle(np.linalg.det(Ps))
out["sl3"] = dict(max_abs_argdet_sl3=float(np.max(np.abs(as_))), circ_abs_mean_generic=float(np.abs(np.mean(np.exp(1j * ag)))))
print("sl3", out["sl3"], flush=True)
# (c,d) grid
N = 5000
rows = []
for e in (None, 1.0, 0.5, 0.25):
    f = 1 if e is None else (1 if e == 1.0 else (3 if e == 0.5 else 12))
    for sl in (False, True):
        for LQ in (2, 4, 6, 8, 10):
            Q = chain(N, LQ * f, e, sl)
            for LU in (2, 4, 6, 8, 12):
                U = chain(N, LU * f, e, sl)
                for LD in (1, 2, 4, 6):
                    D = chain(N, LD * f, e, sl)
                    x, lj = obs(Q @ U, Q @ D)
                    l, c2, p, mu, sd = score(x)
                    rows.append(dict(e=str(e), sl3=sl, LQ=LQ, LU=LU, LD=LD, steps=f, lnL=l, chi2=c2, p=p, mean=mu.tolist(), sd=sd.tolist(), lnJ=float(np.median(lj)), lnJ_sd=float(np.std(lj))))
    print("done e", e, flush=True)
rows.sort(key=lambda r: -r["lnL"])
out["chain_best"] = rows[:12]
marg = {}
for e in ("None", "1.0", "0.5", "0.25"):
    for sl in (False, True):
        ls = np.array([r["lnL"] for r in rows if r["e"] == e and r["sl3"] == sl])
        marg[f"{e}_sl3{sl}"] = dict(n=len(ls), lnZ=float(np.logaddexp.reduce(ls) - math.log(len(ls))), best=float(ls.max()))
out["chain_marginal"] = marg
# FN over a stated charge grid, integer charges with the third family at 0: all (a>=b>=0)
fn = []
ch = [(a, b, 0) for a in range(0, 6) for b in range(0, a + 1)]
for eps in (0.15, 0.2, 0.225, 0.25, 0.3):
    for qQ in ch:
        for qu in ch[:]:
            for qd in [(a, b, c) for (a, b, c) in [(1, 1, 1), (2, 1, 1), (2, 2, 2), (1, 0, 0), (2, 1, 0), (3, 2, 2), (4, 3, 3), (3, 2, 1), (2, 2, 1), (0, 0, 0)]]:
                if rng.random() > 0.03:
                    continue  # stratified thin: 3 percent of the grid
                Eu = eps ** np.add.outer(qQ, qu).astype(float)
                Ed = eps ** np.add.outer(qQ, qd).astype(float)
                x, lj = obs(G(2500) * Eu, G(2500) * Ed)
                l, c2, p, mu, sd = score(x)
                fn.append(dict(eps=eps, qQ=qQ, qu=qu, qd=qd, lnL=l, chi2=c2, p=p, mean=mu.tolist(), lnJ=float(np.median(lj))))
fn.sort(key=lambda r: -r["lnL"])
ls = np.array([r["lnL"] for r in fn])
out["FN_marginal"] = dict(n=len(fn), lnZ=float(np.logaddexp.reduce(ls) - math.log(len(ls))), best=float(ls.max()), best_row=fn[0])
print("marg", {k: (v["n"], round(v["lnZ"], 2), round(v["best"], 2)) for k, v in marg.items()}, flush=True)
print("FN", out["FN_marginal"]["n"], round(out["FN_marginal"]["lnZ"], 2), round(out["FN_marginal"]["best"], 2), fn[0]["eps"], fn[0]["qQ"], fn[0]["qu"], fn[0]["qd"], flush=True)
for r in rows[:6]:
    print({k: r[k] for k in ("e", "sl3", "LQ", "LU", "LD")}, "lnL", round(r["lnL"], 2), "chi2", round(r["chi2"], 1), "p", round(r["p"], 3), "mean", np.round(r["mean"], 1), "lnJ", round(r["lnJ"], 1), "+-", round(r["lnJ_sd"], 1), flush=True)
print("data", np.round(DATA, 1), "lnJ", round(LNJ, 1), flush=True)
# (e) leptons
PMNS = dict(t12=33.4, t23=45.0, t13=8.6, ratio=0.0298, r=0.529, span=8.18)
lep = []
for e, f in ((None, 1), (1.0, 1)):
    for LL in (0, 1, 2, 3):
        Lc = chain(N, LL * f, e) if LL else np.broadcast_to(np.eye(3, dtype=complex), (N, 3, 3))
        for LE in (6, 8, 10, 12):
            E = chain(N, LE * f, e)
            Ye = Lc @ E
            S = G(N)
            S = S + np.swapaxes(S, 1, 2)
            Mn = np.swapaxes(Lc, 1, 2) @ S @ Lc
            Ue, se, _ = np.linalg.svd(Ye)
            Un, sn, _ = np.linalg.svd(Mn)
            Un = Un[:, :, ::-1]
            mn = sn[:, ::-1]
            V = np.abs(np.conj(np.swapaxes(Ue[:, :, ::-1], 1, 2)) @ Un)
            t13 = np.degrees(np.arcsin(np.minimum(V[:, 0, 2], 1)))
            t12 = np.degrees(np.arctan2(V[:, 0, 1], V[:, 0, 0]))
            t23 = np.degrees(np.arctan2(V[:, 1, 2], V[:, 2, 2]))
            rat = (mn[:, 1] ** 2 - mn[:, 0] ** 2) / (mn[:, 2] ** 2 - mn[:, 0] ** 2)
            r = np.log(se[:, 0] / se[:, 1]) / np.log(se[:, 1] / se[:, 2])
            sp = np.log(se[:, 0] / se[:, 2])
            lep.append(dict(e=str(e), LL=LL, LE=LE, med=dict(t12=float(np.median(t12)), t23=float(np.median(t23)), t13=float(np.median(t13)), ratio=float(np.median(rat)), r=float(np.median(r)), span=float(np.median(sp))), q=dict(t13=float(np.mean(t13 < 8.6)), ratio=float(np.mean(rat < 0.0298)), t23=float(np.mean(t23 < 45)), t12=float(np.mean(t12 < 33.4)))))
out["leptons"] = lep
for r in lep:
    if r["e"] == "None" and r["LE"] in (8, 10, 12):
        print("lep", r["LL"], r["LE"], {k: round(v, 2) for k, v in r["med"].items()}, "quantiles", {k: round(v, 2) for k, v in r["q"].items()}, flush=True)
# (f)
span_up = DATA[0] + DATA[1]
out["rg_reading"] = dict(lnMP_over_MZ=math.log(2.4e18 / 91.19), ln_GUT=math.log(2e16 / 91.19), span_up=span_up, per_efold=span_up / math.log(2.4e18 / 91.19))
json.dump(out, open("flavor_chain2.json", "w"), indent=1, default=float)
print("rg", out["rg_reading"], flush=True)
