"""Pass 12675: high-precision value of the q = 32 torus-eigenspace level 12.4896207678 (Pass 12672 addendum 2) and its identification.
The level is the minimum of F on an eigenspace of the two-sided torus Clifford (g, g), ord g = 33.  By symmetric criticality the
eigenspace minimiser is a critical point of F on all of C^1024.  Mixed-precision Newton in the full space: gradient in mpmath (dps 45),
Hessian in double by central differences of the analytic double gradient (2048 x 2048), pseudo-inverse step (null directions:
radial, phase, and any degenerate family).  Each step gains roughly the double-Hessian accuracy (~8 digits).  Then findpoly / pslq
over Q(cos 2pi/33) (degree 10), Q(cos 2pi/11) (5) and Q(sqrt33).
usage: py -3 analysis/w33_q32_torus_level_mixed_newton.py"""
import json, math, os, sys, time
import numpy as np
import mpmath as mp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
tsrc = open(os.path.join(HERE, "w33_regulus_torus_clifford_eigenspaces.py"), encoding="utf-8").read()
_argv = sys.argv; sys.argv = ["x", "5", "1", "1", "1"]
gt = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_torus_clifford_eigenspaces.py")}
exec(tsrc[: tsrc.index("t0 = time.time(); tor")], gt); sys.argv = _argv
q, d, fg, trace, mul, clifford, torus_elements, rng = (gt[k] for k in ("q", "d", "fg", "trace", "mul", "clifford", "torus_elements", "rng"))
TARGET = 12.48962076778924
t00 = time.time(); log = lambda *a: print(*a, f"[{time.time() - t00:.0f}s]", flush=True)
tor = torus_elements(); W = clifford(tor[0], tor[0]); ev, U = np.linalg.eig(W)
groups = []
for i in np.argsort(np.angle(ev)):
    if groups and abs(ev[groups[-1][0]] - ev[i]) < 1e-6: groups[-1].append(i)
    else: groups.append([i])
A0 = None
for idx in groups:
    Q, _ = np.linalg.qr(U[:, idx]); m = Q.shape[1]
    def f(w):
        A = Q @ (w[:m] + 1j * w[m:]); val, gr = fg(np.concatenate([A.real, A.imag]))
        G = Q.conj().T @ (gr[:d] + 1j * gr[d:]); return val, np.concatenate([G.real, G.imag])
    for _ in range(3):
        r = minimize(f, rng.standard_normal(2 * m), jac=True, method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-12, ftol=1e-16))
        if abs(r.fun * d - TARGET) < 1e-6: A0 = Q @ (r.x[:m] + 1j * r.x[m:]); break
    if A0 is not None: break
assert A0 is not None, "level not found"
A0 /= np.linalg.norm(A0)
w0 = np.concatenate([A0.real, A0.imag])
log(f"start: c = {fg(w0)[0] * d:.14f}, full-space gradient {np.linalg.norm(fg(w0)[1]):.2e}")
# ---------- mp gradient
mp.mp.dps = 45
Xi = [[1 - 2 * trace(mul(a, b)) for b in range(q)] for a in range(q)]
Phi = [[[1 - 2 * trace(mul(t, mul(a, b))) for b in range(q)] for a in range(q)] for t in range(q)]
XiO = np.array([[mp.mpf(v) for v in row] for row in Xi], dtype=object)
PhiO = [np.array([[mp.mpf(v) for v in row] for row in Phi[t]], dtype=object) for t in range(q)]
def mp_val_grad(x):
    A = np.array([mp.mpc(x[i], x[d + i]) for i in range(d)], dtype=object)
    nrm = mp.sqrt(mp.fsum(abs(z) ** 2 for z in A)); A = A / nrm
    A2 = A.reshape(q, q)
    absA2 = np.vectorize(lambda z: abs(z) ** 2, otypes=[object])
    f = mp.fsum(v * v for v in absA2(A).ravel()); G = 2 * absA2(A2) * A2
    for t in range(q):
        K = XiO.dot(A2 * PhiO[t]).dot(XiO) / q
        aK = absA2(K); f += mp.fsum(v * v for v in aK.ravel())
        Wm = 2 * aK * K
        G = G + PhiO[t] * (XiO.dot(Wm).dot(XiO) / q)
    Gf = G.ravel()
    ip = mp.fsum(mp.conj(a) * g for a, g in zip(A, Gf))
    Gp = (Gf - mp.re(ip) * A) / nrm
    grad = [2 * mp.re(z) for z in Gp] + [2 * mp.im(z) for z in Gp]
    return (f - mp.mpf(q + 1) / q ** 2) * d, grad
def dbl_hessian(w, h=1e-5):
    n = len(w); H = np.zeros((n, n))
    for i in range(n):
        wp = w.copy(); wm = w.copy(); wp[i] += h; wm[i] -= h
        H[:, i] = (fg(wp)[1] - fg(wm)[1]) / (2 * h)
    return (H + H.T) / 2
x = [mp.mpf(v) for v in w0]; hist = []
for it in range(7):
    c, g = mp_val_grad(x); gn = mp.sqrt(mp.fsum(v * v for v in g))
    hist.append((it, mp.nstr(c, 40), mp.nstr(gn, 4))); log(f"iter {it}: c = {mp.nstr(c, 40)}  |grad| = {mp.nstr(gn, 4)}")
    if gn < mp.mpf(10) ** -38: break
    wd = np.array([float(v) for v in x]); wd /= np.linalg.norm(wd)
    H = dbl_hessian(wd)
    E, V = np.linalg.eigh(H); tol = 1e-7 * np.abs(E).max()
    gd = np.array([float(v) for v in g])
    keep = np.abs(E) > tol
    step = V[:, keep] @ ((V[:, keep].T @ gd) / E[keep])
    if it == 0: log(f"Hessian: {int((~keep).sum())} null directions, {int((E[keep] < 0).sum())} negative eigenvalues (saddle index in C^1024)")
    nx = mp.sqrt(mp.fsum(v * v for v in x))
    x = [xi - mp.mpf(si) * nx for xi, si in zip(x, step)]
c = mp_val_grad(x)[0]
res = dict(value=mp.nstr(c, 42), history=hist)
g33 = 2 * mp.cos(2 * mp.pi / 33); g11 = 2 * mp.cos(2 * mp.pi / 11)
res["findpoly"] = {str(n_): str(mp.findpoly(c, n_, maxcoeff=10 ** 8)) for n_ in (2, 3, 4, 5, 6, 8, 10)}
res["pslq_Q_cos2pi_33"] = str(mp.pslq([c] + [g33 ** k for k in range(10)], maxcoeff=10 ** 6, maxsteps=10 ** 7))
res["pslq_Q_cos2pi_11"] = str(mp.pslq([c] + [g11 ** k for k in range(5)], maxcoeff=10 ** 6, maxsteps=10 ** 7))
res["pslq_Q_cos2pi_11_sqrt33"] = str(mp.pslq([c] + [g11 ** k for k in range(5)] + [mp.sqrt(33) * g11 ** k for k in range(5)], maxcoeff=10 ** 6, maxsteps=10 ** 7))
log(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_q32_torus_level_mixed_newton.json"), "w"), indent=1)
