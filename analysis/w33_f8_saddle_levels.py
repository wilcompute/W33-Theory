"""Pass 12672: other critical levels of the F_8 regulus objective, found as minima on rank-3 Pauli code spaces <S, R> (Pass 12671
ladder: values 2.4985 (56 groups), 2.74109 (126), 3 (326), 7 (2)).  By symmetric criticality (the code space is the fixed space of a
group of Paulis, which preserve F) each code-space critical point is a critical point of F on all of C^64; this is checked directly
via the full 64-dim Riemannian gradient.  The 2.74109 level is refined by Newton in mpmath (8-dim code space) and identified
(findpoly, pslq over Q(2cos 2pi/9), and over Q(sqrt k)).   usage: py -3 analysis/w33_f8_saddle_levels.py"""
import collections, json, math, os
import numpy as np
import mpmath as mp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
lsrc = open(os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py")}
exec(lsrc[: lsrc.index("res = {}")], gl)
space, fg, comm, pauli, herm, gS, Sgrp, C8, trace, mul = (gl[k] for k in ("space", "fg", "comm", "pauli", "herm", "gS", "Sgrp", "C8", "trace", "mul"))
rng = np.random.default_rng(12672)


def cmin(B, n=8):
    m = B.shape[1]

    def f(w):
        A = B @ (w[:m] + 1j * w[m:]); val, gr = fg(np.concatenate([A.real, A.imag]))
        G = B.conj().T @ (gr[:64] + 1j * gr[64:]); return val, np.concatenate([G.real, G.imag])
    rs = [minimize(f, rng.standard_normal(2 * m), jac=True, method="L-BFGS-B", options=dict(maxiter=30000, gtol=1e-14, ftol=1e-18)) for _ in range(n)]
    r = min(rs, key=lambda r: r.fun); return r.fun * 64, B @ (r.x[:m] + 1j * r.x[m:])


cos = {}
for u in range(64):
    for v in range(64):
        if all(comm((u, v), s) for s in Sgrp[1:]): cos.setdefault(min((u ^ s[0], v ^ s[1]) for s in Sgrp), []).append((u, v))
found = {}
for k in sorted(cos):
    if k == (0, 0): continue
    for s in (1, -1):
        B = space(gS + [(k, s)]); val, psi = cmin(B, 6)
        lev = round(val, 5)
        if lev not in found: found[lev] = (k, s, B, psi)
    if len(found) >= 4: break
print("levels found:", sorted(found), flush=True)
out = {}
for lev, (k, s, B, psi) in sorted(found.items()):
    w = np.concatenate([psi.real, psi.imag]) / np.linalg.norm(psi)
    full_grad = np.linalg.norm(fg(w)[1])
    out[str(lev)] = dict(group=[list(k), s], full_gradient_norm=float(full_grad))
    print(lev, "group", k, s, "full 64-dim gradient", f"{full_grad:.1e}", flush=True)
# high-precision refinement of the 2.74109 level on its code space
lev = min(found, key=lambda L: abs(L - 2.74109)); k, s, B, psi = found[lev]
mp.mp.dps = 40
Xi = [[1 - 2 * trace(mul(a, b)) for b in range(8)] for a in range(8)]
Phi = [[[1 - 2 * trace(mul(t, mul(a, b))) for b in range(8)] for a in range(8)] for t in range(8)]
# exact code-space basis from the projector (entries in {0, +-1/8, +-i/8}), Gram-Schmidt in mpmath
Pr = np.eye(64, dtype=complex)
for kk, ss in gS + [(k, s)]: Pr = Pr @ (np.eye(64) + ss * herm(kk)) / 2
assert np.allclose(np.round(Pr * 8), Pr * 8)
cols = []
for j in range(64):
    if np.linalg.matrix_rank(Pr[:, cols + [j]], tol=1e-9) > len(cols): cols.append(j)
    if len(cols) == 8: break
Q = []
for j in cols:
    v = [mp.mpc(mp.mpf(int(round(Pr[i, j].real * 8))) / 8, mp.mpf(int(round(Pr[i, j].imag * 8))) / 8) for i in range(64)]
    for w_ in Q:
        ip = mp.fsum(mp.conj(w_[i]) * v[i] for i in range(64)); v = [v[i] - ip * w_[i] for i in range(64)]
    nr = mp.sqrt(mp.fsum(abs(z) ** 2 for z in v)); Q.append([z / nr for z in v])
Qn = np.array([[complex(Q[j][i]) for j in range(8)] for i in range(64)])
t0 = Qn.conj().T @ psi; t0 /= np.linalg.norm(t0)


def transform(A, t):
    Bq = [[A[a][b] * Phi[t][a][b] for b in range(8)] for a in range(8)]
    C = [[mp.fsum(Xi[kk][a] * Bq[a][b] for a in range(8)) for b in range(8)] for kk in range(8)]
    return [[mp.fsum(C[kk][b] * Xi[b][l] for b in range(8)) / 8 for l in range(8)] for kk in range(8)]


def back(W, t):
    C = [[mp.fsum(Xi[a][kk] * W[kk][l] for kk in range(8)) for l in range(8)] for a in range(8)]
    D = [[mp.fsum(C[a][l] * Xi[l][b] for l in range(8)) / 8 for b in range(8)] for a in range(8)]
    return [[D[a][b] * Phi[t][a][b] for b in range(8)] for a in range(8)]


def F_grad(x):
    t = [mp.mpc(x[2 * j], x[2 * j + 1]) for j in range(8)]
    A = [mp.fsum(Q[j][i] * t[j] for j in range(8)) for i in range(64)]
    nr = mp.sqrt(mp.fsum(abs(z) ** 2 for z in A)); A = [z / nr for z in A]
    A2 = [[A[8 * a + b] for b in range(8)] for a in range(8)]
    f = mp.fsum(abs(z) ** 4 for z in A); G = [[2 * abs(A2[a][b]) ** 2 * A2[a][b] for b in range(8)] for a in range(8)]
    for tt in range(8):
        K = transform(A2, tt); f += mp.fsum(abs(K[a][b]) ** 4 for a in range(8) for b in range(8))
        Bk = back([[2 * abs(K[a][b]) ** 2 * K[a][b] for b in range(8)] for a in range(8)], tt)
        for a in range(8):
            for b in range(8): G[a][b] += Bk[a][b]
    Gf = [G[i // 8][i % 8] for i in range(64)]
    ip = mp.fsum(mp.conj(u) * v for u, v in zip(A, Gf)); Gf = [v - ip * u for u, v in zip(A, Gf)]
    Gt = [mp.fsum(mp.conj(Q[j][i]) * Gf[i] for i in range(64)) for j in range(8)]
    gr = []
    for z in Gt: gr += [2 * mp.re(z) / nr, 2 * mp.im(z) / nr]
    return f - mp.mpf(9) / 64, gr


x = []
for z in t0: x += [mp.mpf(z.real), mp.mpf(z.imag)]
for it in range(7):
    f, gr = F_grad(x); gn = mp.sqrt(mp.fsum(v * v for v in gr))
    print(it, mp.nstr(64 * f, 38), "grad", mp.nstr(gn, 3), flush=True)
    if gn < mp.mpf(10) ** -32: break
    h = mp.mpf(10) ** -18; Hm = mp.matrix(16, 16)
    for i in range(16):
        xp = list(x); xm = list(x); xp[i] += h; xm[i] -= h
        gp = F_grad(xp)[1]; gm = F_grad(xm)[1]
        for j in range(16): Hm[j, i] = (gp[j] - gm[j]) / (2 * h)
    E, V = mp.eigsy((Hm + Hm.T) / 2); tol = mp.mpf(10) ** -10 * max(abs(e) for e in E)
    step = [mp.mpf(0)] * 16
    for kk in range(16):
        if abs(E[kk]) > tol:
            co = mp.fsum(V[j, kk] * gr[j] for j in range(16)) / E[kk]
            for j in range(16): step[j] += co * V[j, kk]
    x = [a - b for a, b in zip(x, step)]
c = 64 * f
g9 = 2 * mp.cos(2 * mp.pi / 9)
ident = dict(value=mp.nstr(c, 35), hessian_null=sum(1 for e in E if abs(e) <= tol),
             findpoly=str(mp.findpoly(c, 8, maxcoeff=10 ** 6)), Q_gamma=str(mp.pslq([c, 1, g9, g9 * g9], maxcoeff=10 ** 6, maxsteps=10 ** 6)),
             identify=str(mp.identify(c, ["sqrt(2)", "sqrt(3)", "sqrt(5)", "sqrt(6)", "sqrt(7)", "sqrt(17)", "sqrt(21)"])))
print(ident, flush=True)
out["refined"] = dict(level=lev, **ident)
json.dump(out, open(os.path.join(ROOT, "data", "w33_f8_saddle_levels.json"), "w"), indent=1)
