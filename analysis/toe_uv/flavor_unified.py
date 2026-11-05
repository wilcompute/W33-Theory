"""One chain structure for all flavour: 10-5bar split with random chains replacing U(1) charges.
   Y_u = T X_u T^T,   Y_d = T X_d R,   Y_e = T X_e R,   M_nu = R^T S R (Weinberg, Majorana) with X, S anarchic, X_u and S symmetric, T of length LT, R of length LR.
Two integers.  Thirteen scored observables: ln mt/mc, ln mc/mu, ln mb/ms, ln ms/md, ln mtau/mmu, ln mmu/me, ln s12, ln s23, ln s13 (CKM), then ln s12^2... PMNS as angles in logit form, ln(dm21/dm31).
Comparator: FN 10-5bar: Y_u = c eps^(q10_i + q10_j), Y_d, Y_e = c eps^(q10_i + q5_j), M_nu = c eps^(q5_i + q5_j), with q10 = (a, b, 0), q5 = (c, d, 0), eps grid.  Random order-one c.  This has four integers plus eps.
Second comparator: the two-sector scan, quarks only, from flavor_chain2.py is not comparable, so not used here.
Score: Gaussian in the observables per point, ln L at the data, and marginal over the stated grid.  p value from the Mahalanobis rank.  A leave-one-observable-out check on the best chain point: predict each observable from the conditional Gaussian given the other twelve and report the pull.
Conditional predictions at the best chain point, by keeping draws close to the data in the measured observables (ABC with stated tolerance): normal ordering probability, sum m_nu with the atmospheric scale fixed, m_bb, lightest mass, delta_CP; lnJ_CKM.
Both orderings are kept: the sort is by mass, and ordering is defined by whether the isolated state is heavy.
usage: py -3 flavor_unified.py"""
import json
import math
import numpy as np

import os
KIND = os.environ.get("KIND", "fwd")
OUT = f"flavor_unified_{KIND}.json"
rng = np.random.default_rng(20261107)
M = dict(u=1.24e-3, c=0.62, t=171.0, d=2.69e-3, s=0.0535, b=2.85, e=0.4866e-3, mu=0.1027, tau=1.746)
PMNS = dict(s12=math.sin(math.radians(33.4)), s23=math.sin(math.radians(45.0)), s13=math.sin(math.radians(8.6)))
DATA = np.array([math.log(M["t"] / M["c"]), math.log(M["c"] / M["u"]), math.log(M["b"] / M["s"]), math.log(M["s"] / M["d"]), math.log(M["tau"] / M["mu"]), math.log(M["mu"] / M["e"]), math.log(0.2265), math.log(0.0405), math.log(0.00365), math.log(PMNS["s12"]), math.log(PMNS["s23"]), math.log(PMNS["s13"]), math.log(0.0298)])
NAMES = ["mt/mc", "mc/mu", "mb/ms", "ms/md", "mtau/mmu", "mmu/me", "ckm12", "ckm23", "ckm13", "pmns12", "pmns23", "pmns13", "dm21/dm31"]


def G(n):
    return (rng.standard_normal((n, 3, 3)) + 1j * rng.standard_normal((n, 3, 3))) / math.sqrt(2)


def sym(n):
    A = G(n)
    return (A + np.swapaxes(A, 1, 2)) / math.sqrt(2)


def hop(n, kind):
    A = G(n)
    if kind == "inv":
        return np.linalg.inv(A)
    if kind == "sym":
        w, V = np.linalg.eig(A)
        return V @ (np.exp(w)[:, None] * np.eye(3)[None]) @ np.linalg.inv(V)
    return A


def chain(n, L, kind="fwd"):
    P = np.broadcast_to(np.eye(3, dtype=complex), (n, 3, 3)).copy()
    for _ in range(L):
        P = P @ hop(n, kind)
        P = P / np.linalg.norm(P, axis=(1, 2))[:, None, None]
    return P


def angles(V):
    a = np.abs(V)
    s13 = a[:, 0, 2]
    s12 = a[:, 0, 1] / np.sqrt(a[:, 0, 0] ** 2 + a[:, 0, 1] ** 2)
    s23 = a[:, 1, 2] / np.sqrt(a[:, 1, 2] ** 2 + a[:, 2, 2] ** 2)
    return s12, s23, s13


def observables(Yu, Yd, Ye, Mn, full=False):
    Uu, su, _ = np.linalg.svd(Yu)
    Ud, sd, _ = np.linalg.svd(Yd)
    Ue, se, Ve = np.linalg.svd(Ye)
    # neutrino: the left-handed doublet L is the right index of Y_e = T X R
    Un, sn, _ = np.linalg.svd(Mn)
    Un = Un[:, :, ::-1]
    mn = sn[:, ::-1]  # ascending
    Vc = np.conj(np.swapaxes(Uu, 1, 2)) @ Ud
    Ve3 = np.conj(Ve)  # right singular vectors of Y_e act on L
    Ve_sorted = Ve3[:, :, :] if False else np.conj(np.swapaxes(Ve, 1, 2))
    # order charged leptons light to heavy
    Vp = np.conj(np.swapaxes(Ve_sorted[:, :, ::-1], 1, 2)) @ Un
    s12c, s23c, s13c = angles(Vc[:, ::-1, :][:, :, ::-1])
    # normal ordering labels: states sorted ascending; solar pair = the closest pair
    d21 = mn[:, 1] ** 2 - mn[:, 0] ** 2
    d32 = mn[:, 2] ** 2 - mn[:, 1] ** 2
    normal = d21 < d32
    W = Vp.copy()
    W[~normal] = np.roll(Vp[~normal], 1, axis=2)  # inverted: label 3 is lightest
    ratio = np.where(normal, d21 / (mn[:, 2] ** 2 - mn[:, 0] ** 2), d32 / (mn[:, 2] ** 2 - mn[:, 0] ** 2))
    s12p, s23p, s13p = angles(W)
    x = np.c_[np.log(su[:, 0] / su[:, 1]), np.log(su[:, 1] / su[:, 2]), np.log(sd[:, 0] / sd[:, 1]), np.log(sd[:, 1] / sd[:, 2]), np.log(se[:, 0] / se[:, 1]), np.log(se[:, 1] / se[:, 2]), np.log(s12c + 1e-300), np.log(s23c + 1e-300), np.log(s13c + 1e-300), np.log(s12p + 1e-300), np.log(s23p + 1e-300), np.log(s13p + 1e-300), np.log(ratio + 1e-300)]
    if not full:
        return x
    Vu = Vc[:, ::-1, :][:, :, ::-1]
    Jc = np.imag(Vu[:, 0, 1] * Vu[:, 1, 2] * np.conj(Vu[:, 0, 2]) * np.conj(Vu[:, 1, 1]))
    scale = np.sqrt(2.513e-3 / (mn[:, 2] ** 2 - mn[:, 0] ** 2))
    masses = mn * scale[:, None]
    Jp = np.imag(W[:, 0, 1] * W[:, 1, 2] * np.conj(W[:, 0, 2]) * np.conj(W[:, 1, 1]))
    mbb_order = np.where(normal, 0, 1)
    return x, dict(normal=normal, masses=masses, lnJ=np.log(np.abs(Jc) + 1e-300), Jp=Jp, s13p=s13p, Y_top=su[:, 0], Y_b=sd[:, 0], Y_tau=se[:, 0], W=W)


def score(x):
    x = x[np.all(np.isfinite(x), axis=1)]
    mu = x.mean(0)
    C = np.cov(x.T) + 1e-9 * np.eye(x.shape[1])
    Ci = np.linalg.inv(C)
    d = DATA - mu
    c2 = float(d @ Ci @ d)
    dd = x - mu
    sim = np.einsum("ij,jk,ik->i", dd, Ci, dd)
    return -0.5 * c2 - 0.5 * np.linalg.slogdet(C)[1] - 6.5 * math.log(2 * math.pi), c2, float(np.mean(sim > c2)), mu, C


N = 6000
rows = []
for LT in range(1, 13 if KIND != "sym" else 16):
    T = chain(N, LT, KIND)
    for LR in range(0, 6):
        R = chain(N, LR) if LR else np.broadcast_to(np.eye(3, dtype=complex), (N, 3, 3))
        x = observables(T @ sym(N) @ np.swapaxes(T, 1, 2), T @ G(N) @ R, T @ G(N) @ R, np.swapaxes(R, 1, 2) @ sym(N) @ R)
        l, c2, p, mu, C = score(x)
        rows.append(dict(LT=LT, LR=LR, lnL=l, chi2=c2, p=p, mean=mu.tolist(), sd=np.sqrt(np.diag(C)).tolist()))
rows.sort(key=lambda r: -r["lnL"])
ls = np.array([r["lnL"] for r in rows])
out = dict(names=NAMES, data=DATA.tolist(), chain=dict(n=len(rows), lnZ=float(np.logaddexp.reduce(ls) - math.log(len(ls))), best=rows[0], top=rows[:8]))
print("chain lnZ", round(out["chain"]["lnZ"], 2), "n", len(rows), flush=True)
print("data", np.round(DATA, 1), flush=True)
for r in rows[:5]:
    print(r["LT"], r["LR"], "lnL", round(r["lnL"], 2), "chi2", round(r["chi2"], 1), "p", round(r["p"], 3), "mean", np.round(r["mean"], 1), flush=True)
# FN comparator
fn = [dict(eps=0, q10=[0,0,0], q5=[0,0,0], lnL=-1e9, chi2=0, p=0, mean=[])] if KIND != "fwd" else []
for eps in ((0.15, 0.2, 0.225, 0.25, 0.3) if KIND == "fwd" else ()):
    for a in range(1, 7):
        for b in range(0, a + 1):
            for c in range(0, 4):
                for d in range(0, c + 1):
                    q10, q5 = np.array([a, b, 0.0]), np.array([c, d, 0.0])
                    n = 3000
                    E1 = eps ** np.add.outer(q10, q10)
                    E2 = eps ** np.add.outer(q10, q5)
                    E3 = eps ** np.add.outer(q5, q5)
                    x = observables(sym(n) * E1, G(n) * E2, G(n) * E2, sym(n) * E3)
                    l, c2, p, mu, C = score(x)
                    fn.append(dict(eps=eps, q10=[a, b, 0], q5=[c, d, 0], lnL=l, chi2=c2, p=p, mean=mu.tolist()))
fn.sort(key=lambda r: -r["lnL"])
ls = np.array([r["lnL"] for r in fn])
out["FN"] = dict(n=len(fn), lnZ=float(np.logaddexp.reduce(ls) - math.log(len(ls))), best=fn[0], top=fn[:5])
print("FN lnZ", round(out["FN"]["lnZ"], 2), "n", len(fn), flush=True)
for r in fn[:3]:
    print(r["eps"], r["q10"], r["q5"], "lnL", round(r["lnL"], 2), "chi2", round(r["chi2"], 1), "p", round(r["p"], 3), "mean", np.round(r["mean"], 1), flush=True)
# seed scatter of the best points
sc = []
b = rows[0]
for k in range(4):
    n = 6000
    T, R = chain(n, b["LT"], KIND), chain(n, b["LR"]) if b["LR"] else np.broadcast_to(np.eye(3, dtype=complex), (n, 3, 3))
    x = observables(T @ sym(n) @ np.swapaxes(T, 1, 2), T @ G(n) @ R, T @ G(n) @ R, np.swapaxes(R, 1, 2) @ sym(n) @ R)
    sc.append(score(x)[0])
out["best_seed_scatter"] = sc
# leave-one-out and conditional predictions at the best point
n = 80000
T, R = chain(n, b["LT"], KIND), chain(n, b["LR"]) if b["LR"] else np.broadcast_to(np.eye(3, dtype=complex), (n, 3, 3))
x, ex = observables(T @ sym(n) @ np.swapaxes(T, 1, 2), T @ G(n) @ R, T @ G(n) @ R, np.swapaxes(R, 1, 2) @ sym(n) @ R, full=True)
ok = np.all(np.isfinite(x), axis=1)
x = x[ok]
mu, C = x.mean(0), np.cov(x.T)
loo = {}
for i, name in enumerate(NAMES):
    o = [j for j in range(13) if j != i]
    Coo = C[np.ix_(o, o)]
    w = np.linalg.solve(Coo, C[o, i])
    m = mu[i] + w @ (DATA[o] - mu[o])
    s = math.sqrt(C[i, i] - w @ C[o, i])
    loo[name] = dict(pred=float(m), sd=float(s), data=float(DATA[i]), pull=float((DATA[i] - m) / s), prior_sd=float(math.sqrt(C[i, i])))
out["leave_one_out"] = loo
print("LOO", {k: (round(v["pred"], 2), round(v["sd"], 2), round(v["pull"], 2)) for k, v in loo.items()}, flush=True)
d = (x - DATA) / np.sqrt(np.diag(C))
dist = np.sqrt(np.sum(d ** 2, axis=1))
for tol in (2.5, 3.0):
    k = dist < tol
    ms = ex["masses"][ok][k]
    nor = ex["normal"][ok][k]
    out[f"conditional_tol{tol}"] = dict(n=int(k.sum()), P_normal=float(nor.mean()), sum_mnu_NO_q=[float(q) for q in np.quantile(ms[nor].sum(1), [.16, .5, .84])] if nor.sum() else None, m1_NO_q=[float(q) for q in np.quantile(ms[nor][:, 0], [.16, .5, .84])] if nor.sum() else None, lnJ_q=[float(q) for q in np.quantile(ex["lnJ"][ok][k], [.16, .5, .84])])
    print("cond", tol, out[f"conditional_tol{tol}"], flush=True)
out["unconditional"] = dict(P_normal=float(ex["normal"][ok].mean()), lnJ_q=[float(q) for q in np.quantile(ex["lnJ"][ok], [.16, .5, .84])], mb_over_mt=[float(q) for q in np.quantile(np.log((ex["Y_b"] / ex["Y_top"])[ok]), [.16, .5, .84])])
print("uncond", out["unconditional"], flush=True)
json.dump(out, open(OUT, "w"), indent=1, default=float)
print("done", flush=True)
