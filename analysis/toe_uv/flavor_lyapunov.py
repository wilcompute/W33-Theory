"""Fermion masses as Lyapunov exponents.  Y = product of N random 3x3 hopping matrices.  No flavour symmetry and no charges: only chain lengths.
Exact: for complex Ginibre factors ln s_k / N -> psi(k)/2, so ln(m3/m2)/ln(m2/m1) -> 1/2 for the forward product and 2 for the inverse product (zero-mode transfer form).
Sharing the doublet chain Q between up and down: Y_u = Q U, Y_d = Q D aligns the left singular frames (Oseledets), so CKM is near 1 and its angles are set by the same gaps.
Models, scanned over integer lengths:
  fwd:   Y_u = Q U, Y_d = Q D, forward products
  inv:   same with inverse factors
  su5f:  Y_u = T X T^T, Y_d = T X', with T forward (10 chain) and anarchic X
  su5i:  same with T inverse
Nulls, same scoring:
  anarchy: Y single Ginibre (length 1 each): no structure.
  FN: Y_ij = c_ij eps^(q_i + q_j') with order-one random c, fitted charges, the standard comparator.  It has more freedom, by construction.
Score: Gaussian in log observables per model point, ln L at the data: x = ln(mt/mc), ln(mc/mu), ln(mb/ms), ln(ms/md), ln th12, ln th23, ln th13.  Masses at M_Z (Xing et al 2008 values from memory; ratios run little).  Log J reported, not scored.
The scale of ln L is meaningful only relative to the nulls under the same scoring, and integer lengths are scanned, so a look-elsewhere count is reported.
Control: the Monte Carlo must return r -> 1/2 and 2 at large N, and CKM -> 1 as N_Q grows.
usage: py -3 flavor_lyapunov.py"""
import json
import math
import numpy as np

rng = np.random.default_rng(20261105)
M = dict(u=1.24e-3, c=0.62, t=171.0, d=2.69e-3, s=0.0535, b=2.85, e=0.4866e-3, mu=0.1027, tau=1.746)
TH = dict(t12=0.2265, t23=0.0405, t13=0.00365)
DATA = np.array([math.log(M["t"] / M["c"]), math.log(M["c"] / M["u"]), math.log(M["b"] / M["s"]), math.log(M["s"] / M["d"]), math.log(TH["t12"]), math.log(TH["t23"]), math.log(TH["t13"])])
NAMES = ["ln mt/mc", "ln mc/mu", "ln mb/ms", "ln ms/md", "ln th12", "ln th23", "ln th13"]
r_obs = dict(up=DATA[0] / DATA[1], down=DATA[2] / DATA[3], lepton=math.log(M["tau"] / M["mu"]) / math.log(M["mu"] / M["e"]), ckm=DATA[5] / DATA[4])


def ginibre(n):
    return (rng.standard_normal((n, 3, 3)) + 1j * rng.standard_normal((n, 3, 3))) / math.sqrt(2)


def chain(n, L, inverse=False):
    """stabilised product is not needed for L up to ~30 in double precision on singular values with care: use QR accumulation."""
    Q = np.broadcast_to(np.eye(3, dtype=complex), (n, 3, 3)).copy()
    logs = np.zeros((n, 3))
    # keep as Q R with R accumulated via diagonal logs; we need the full matrix, so hold it as Q * diag(exp logs) * W
    P = Q
    scale = np.zeros(n)
    for _ in range(L):
        A = ginibre(n)
        if inverse:
            A = np.linalg.inv(A)
        P = P @ A
        s = np.linalg.norm(P, axis=(1, 2))
        P = P / s[:, None, None]
        scale += np.log(s)
    return P


def obs_quark(Yu, Yd):
    Uu, su, _ = np.linalg.svd(Yu)
    Ud, sd, _ = np.linalg.svd(Yd)
    V = (np.conj(np.swapaxes(Uu, 1, 2)) @ Ud)[:, ::-1, :][:, :, ::-1]  # light to heavy: numpy returns singular values heaviest first, and without this t12 and t23 are swapped
    Va = np.abs(V)
    t13 = Va[:, 0, 2]
    t12 = np.arctan2(Va[:, 0, 1], Va[:, 0, 0])
    t23 = np.arctan2(Va[:, 1, 2], Va[:, 2, 2])
    J = np.imag(V[:, 0, 1] * V[:, 1, 2] * np.conj(V[:, 0, 2]) * np.conj(V[:, 1, 1]))
    x = np.c_[np.log(su[:, 0] / su[:, 1]), np.log(su[:, 1] / su[:, 2]), np.log(sd[:, 0] / sd[:, 1]), np.log(sd[:, 1] / sd[:, 2]), np.log(np.maximum(np.sin(t12), 1e-300)), np.log(np.maximum(np.sin(t23), 1e-300)), np.log(np.maximum(t13, 1e-300))]
    return x, np.log(np.abs(J) + 1e-300)


def score(x):
    x = x[np.all(np.isfinite(x), axis=1)]
    mu = x.mean(0)
    C = np.cov(x.T) + 1e-9 * np.eye(x.shape[1])
    d = DATA - mu
    return float(-0.5 * d @ np.linalg.solve(C, d) - 0.5 * np.linalg.slogdet(C)[1] - 0.5 * x.shape[1] * math.log(2 * math.pi)), mu, np.sqrt(np.diag(C)), float(d @ np.linalg.solve(C, d))


out = {"observed_r": r_obs}
# controls
ctrl = {}
for L in (10, 40, 120):
    for inv in (False, True):
        n = 4000
        P = chain(n, L, inv)
        s = np.linalg.svd(P, compute_uv=False)
        ok = np.all(s > 1e-290, axis=1)
        r = np.log(s[ok, 0] / s[ok, 1]) / np.log(s[ok, 1] / s[ok, 2])
        ctrl[f"L{L}_{'inv' if inv else 'fwd'}"] = dict(median_r=float(np.median(r)), iqr=[float(np.quantile(r, .25)), float(np.quantile(r, .75))], kept=int(ok.sum()))
out["control_r"] = ctrl
print("control", {k: round(v["median_r"], 3) for k, v in ctrl.items()}, flush=True)
print("observed", {k: round(v, 3) for k, v in r_obs.items()}, flush=True)

N = 6000
rows = []
for model in ("fwd", "inv"):
    inv = model == "inv"
    for LQ in (0, 2, 4, 6, 8, 10, 14):
        Q = chain(N, LQ, inv) if LQ else np.broadcast_to(np.eye(3, dtype=complex), (N, 3, 3))
        for LU in (1, 2, 4, 6, 8, 12):
            U = chain(N, LU, inv)
            for LD in (1, 2, 4, 6, 8, 12):
                D = chain(N, LD, inv)
                x, lj = obs_quark(Q @ U, Q @ D)
                l, mu, sd, c2 = score(x)
                rows.append(dict(model=model, LQ=LQ, LU=LU, LD=LD, lnL=l, chi2=c2, mean=mu.tolist(), sd=sd.tolist(), lnJ=float(np.median(lj))))
for model in ("su5f", "su5i"):
    inv = model == "su5i"
    for LT in (2, 4, 6, 8, 10, 14):
        T = chain(N, LT, inv)
        for LX in (1, 2, 4):
            Xd = chain(N, LX, inv)
            Xu = ginibre(N)
            Xu = Xu + np.swapaxes(Xu, 1, 2)
            x, lj = obs_quark(T @ Xu @ np.swapaxes(T, 1, 2), T @ Xd)
            l, mu, sd, c2 = score(x)
            rows.append(dict(model=model, LQ=LT, LU=0, LD=LX, lnL=l, chi2=c2, mean=mu.tolist(), sd=sd.tolist(), lnJ=float(np.median(lj))))
# nulls
A, B = ginibre(N), ginibre(N)
x, lj = obs_quark(A, B)
l, mu, sd, c2 = score(x)
rows.append(dict(model="anarchy", LQ=0, LU=0, LD=0, lnL=l, chi2=c2, mean=mu.tolist(), sd=sd.tolist(), lnJ=float(np.median(lj))))
# FN comparator with standard textbook charges: Q (3,2,0), u (3,2,0), d (1,0,0), eps scanned
for eps in (0.15, 0.2, 0.225, 0.25, 0.3):
    for qQ, qu, qd in (((3, 2, 0), (3, 2, 0), (1, 0, 0)), ((3, 2, 0), (4, 2, 0), (2, 1, 1)), ((4, 2, 0), (4, 2, 0), (2, 1, 0))):
        cu, cd = ginibre(N), ginibre(N)
        Eu = eps ** (np.add.outer(qQ, qu).astype(float))
        Ed = eps ** (np.add.outer(qQ, qd).astype(float))
        x, lj = obs_quark(cu * Eu, cd * Ed)
        l, mu, sd, c2 = score(x)
        rows.append(dict(model="FN", LQ=eps, LU=str(qQ) + str(qu), LD=str(qd), lnL=l, chi2=c2, mean=mu.tolist(), sd=sd.tolist(), lnJ=float(np.median(lj))))
rows.sort(key=lambda r: -r["lnL"])
out["rows"] = rows
best = {}
for r in rows:
    best.setdefault(r["model"], r)
out["best"] = best
out["n_points"] = {m: sum(1 for r in rows if r["model"] == m) for m in best}
json.dump(out, open("flavor_lyapunov.json", "w"), indent=1, default=float)
print("data", np.round(DATA, 2), flush=True)
for m, r in best.items():
    print(m, "pts", out["n_points"][m], "LQ,LU,LD", r["LQ"], r["LU"], r["LD"], "lnL", round(r["lnL"], 2), "chi2", round(r["chi2"], 1), "mean", np.round(r["mean"], 2), "sd", np.round(r["sd"], 2), "lnJ", round(r["lnJ"], 1), flush=True)
