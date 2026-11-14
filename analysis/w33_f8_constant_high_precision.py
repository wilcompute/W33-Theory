"""Pass 12669: high-precision value of c_8 = 64 min F for the F_8 regulus (nine MUBs, six qubits) and a search for a closed form.
Start: the saved minimiser (data/w33_f8_minimiser.npy, c = 2.498508646688).  F in the CZ model (w33_regulus_constants_q16_q32.py):
F(A) = sum_p |A_p|^4 + sum_t sum_k |K_t(A)_k|^4 - 9/64 for unit A in C^64, K_t = Xi (A o Phi_t) Xi / 8.
Newton's method in mpmath (dps 60) on the Riemannian gradient (tangent to the sphere, orthogonal to the phase direction), with a
pseudo-inverse Hessian built by central differences of the analytic gradient (the minimum is degenerate along symmetry orbits).
Then mpmath.findpoly / pslq for integer relations among powers of c (degree <= 12, coefficients <= 1e7), and identify() over
common surds.  usage: py -3 analysis/w33_f8_constant_high_precision.py"""
import json, os, time
import numpy as np
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], g)
q, mul, trace = g["field"](3)
Xi = [[1 - 2 * trace(mul(a, b)) for b in range(8)] for a in range(8)]
Phi = [[[1 - 2 * trace(mul(t, mul(a, b))) for b in range(8)] for a in range(8)] for t in range(8)]
mp.mp.dps = 60


def transform(A, t):  # K = Xi (A o Phi_t) Xi / 8, A as 8x8 list of mpc
    B = [[A[a][b] * Phi[t][a][b] for b in range(8)] for a in range(8)]
    C = [[mp.fsum(Xi[k][a] * B[a][b] for a in range(8)) for b in range(8)] for k in range(8)]
    return [[mp.fsum(C[k][b] * Xi[b][l] for b in range(8)) / 8 for l in range(8)] for k in range(8)]


def back(W, t):  # adjoint: Phi_t o (Xi W Xi) / 8   (Xi symmetric, real)
    C = [[mp.fsum(Xi[a][k] * W[k][l] for k in range(8)) for l in range(8)] for a in range(8)]
    D = [[mp.fsum(C[a][l] * Xi[l][b] for l in range(8)) / 8 for b in range(8)] for a in range(8)]
    return [[D[a][b] * Phi[t][a][b] for b in range(8)] for a in range(8)]


def F_and_grad(x):
    A = [[mp.mpc(x[2 * (8 * a + b)], x[2 * (8 * a + b) + 1]) for b in range(8)] for a in range(8)]
    nrm = mp.sqrt(mp.fsum(abs(A[a][b]) ** 2 for a in range(8) for b in range(8)))
    A = [[A[a][b] / nrm for b in range(8)] for a in range(8)]
    f = mp.fsum(abs(A[a][b]) ** 4 for a in range(8) for b in range(8))
    G = [[2 * abs(A[a][b]) ** 2 * A[a][b] for b in range(8)] for a in range(8)]
    for t in range(8):
        K = transform(A, t)
        f += mp.fsum(abs(K[k][l]) ** 4 for k in range(8) for l in range(8))
        W = [[2 * abs(K[k][l]) ** 2 * K[k][l] for l in range(8)] for k in range(8)]
        Bk = back(W, t)
        for a in range(8):
            for b in range(8): G[a][b] += Bk[a][b]
    # Riemannian gradient on the sphere (and remove phase direction)
    flatA = [A[a][b] for a in range(8) for b in range(8)]; flatG = [G[a][b] for a in range(8) for b in range(8)]
    ip = mp.fsum((mp.conj(u) * v) for u, v in zip(flatA, flatG))
    flatG = [v - mp.re(ip) * u - 1j * mp.im(ip) * u for u, v in zip(flatA, flatG)]
    grad = []
    for v in flatG: grad += [2 * mp.re(v) / nrm, 2 * mp.im(v) / nrm]
    xs = []
    for u in flatA: xs += [mp.re(u), mp.im(u)]
    return f - mp.mpf(9) / 64, grad, xs


A0 = np.load(os.path.join(ROOT, "data", "w33_f8_minimiser.npy"))
x = []
for a in range(8):
    for b in range(8): x += [mp.mpf(float(A0[a, b].real)), mp.mpf(float(A0[a, b].imag))]
t0 = time.time(); hist = []
for it in range(8):
    f, gr, x = F_and_grad(x)
    gnorm = mp.sqrt(mp.fsum(v * v for v in gr)); hist.append((it, mp.nstr(f * 64, 30), mp.nstr(gnorm, 5)))
    print(it, mp.nstr(f * 64, 35), "grad", mp.nstr(gnorm, 5), round(time.time() - t0), "s", flush=True)
    if gnorm < mp.mpf(10) ** -45: break
    h = mp.mpf(10) ** -25; n = len(x); H = mp.matrix(n, n)
    for i in range(n):
        xp = list(x); xm = list(x); xp[i] += h; xm[i] -= h
        gp = F_and_grad(xp)[1]; gm = F_and_grad(xm)[1]
        for j in range(n): H[j, i] = (gp[j] - gm[j]) / (2 * h)
    Hs = (H + H.T) / 2
    E, Q = mp.eigsy(Hs)
    step = [mp.mpf(0)] * n
    tol = mp.mpf(10) ** -12 * max(abs(e) for e in E)
    for k in range(n):
        if abs(E[k]) > tol:
            coef = mp.fsum(Q[j, k] * gr[j] for j in range(n)) / E[k]
            for j in range(n): step[j] += coef * Q[j, k]
    x = [xi - si for xi, si in zip(x, step)]
c8 = f * 64
res = dict(c8=mp.nstr(c8, 45), history=hist, seconds=round(time.time() - t0))
cands = {}
for deg in range(2, 13):
    p = mp.findpoly(c8, deg, maxcoeff=10 ** 7)
    if p: cands[deg] = [int(v) for v in p]; break
res["findpoly"] = cands
res["identify"] = str(mp.identify(c8, ["sqrt(2)", "sqrt(3)", "sqrt(5)", "sqrt(7)", "sqrt(13)", "sqrt(17)"]))
print(res, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_constant_high_precision.json"), "w"), indent=1)
