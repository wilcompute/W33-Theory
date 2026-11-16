"""Pass 12675: 45-digit value of the q = 32 torus-eigenspace level 12.4896207676 and its identification (second method).
The torus Clifford W (Pass 12672) has exact entries in Z[i]/sqrt(2)^k.  (1) The 16-dim eigenspace E of the minimising eigenvalue is
refined to high precision by iterative refinement: residual R = W V - lambda V in mpmath with the exact W, correction from the
double-precision spectral decomposition (pseudo-inverse of W - lambda on the complement), then mp Gram-Schmidt.  (2) Newton in mpmath
on F restricted to E (32 real parameters; Hessian by central differences of the mp gradient).  (3) findpoly / pslq over
Q(cos 2pi/33), Q(cos 2pi/11), Q(sqrt 33).   usage: py -3 analysis/w33_q32_torus_level_eigenspace_newton.py"""
import json, math, os, sys, time
import numpy as np
import mpmath as mp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
tsrc = open(os.path.join(HERE, "w33_regulus_torus_clifford_eigenspaces.py"), encoding="utf-8").read()
_argv = sys.argv; sys.argv = ["x", os.environ.get("REG_K", "5"), "1", "1", "1"]
gt = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_torus_clifford_eigenspaces.py")}
exec(tsrc[: tsrc.index("t0 = time.time(); tor")], gt); sys.argv = _argv
q, d, fg, trace, mul, clifford, torus_elements, rng = (gt[k] for k in ("q", "d", "fg", "trace", "mul", "clifford", "torus_elements", "rng"))
TARGET = float(os.environ.get("TARGET", "12.48962076778924"))
mp.mp.dps = 50
t00 = time.time(); log = lambda *a: print(*a, f"[{time.time() - t00:.0f}s]", flush=True)
tor = torus_elements(); W = clifford(tor[0], tor[0])
W = W * np.conj(W[0, 0]) / abs(W[0, 0])      # remove the arbitrary global phase (W is then +-1/sqrt(2)^k in every entry)
# exact entries: W * sqrt(2)^k is a Gaussian-integer matrix
amax = np.abs(W[np.abs(W) > 1e-9]); k2 = round(math.log2(1 / amax.min() ** 2))
Wi = np.round(W * math.sqrt(2) ** k2)
assert np.allclose(Wi, W * math.sqrt(2) ** k2, atol=1e-8)
log(f"W entries in Z[i]/sqrt2^{k2}")
ev, Ud = np.linalg.eig(W)
groups = []
for i in np.argsort(np.angle(ev)):
    if groups and abs(ev[groups[-1][0]] - ev[i]) < 1e-6: groups[-1].append(i)
    else: groups.append([i])
choice = None
for idx in groups:
    Q, _ = np.linalg.qr(Ud[:, idx]); m = Q.shape[1]
    def f(w):
        A = Q @ (w[:m] + 1j * w[m:]); val, gr = fg(np.concatenate([A.real, A.imag]))
        G = Q.conj().T @ (gr[:d] + 1j * gr[d:]); return val, np.concatenate([G.real, G.imag])
    for _ in range(3):
        r = minimize(f, rng.standard_normal(2 * m), jac=True, method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-12, ftol=1e-16))
        if abs(r.fun * d - TARGET) < 1e-6: choice = (idx, Q, r.x); break
    if choice: break
idx, Q, xbest = choice; lam_d = ev[idx[0]]; m = Q.shape[1]
log(f"eigenspace dim {m}, eigenvalue {lam_d:.6f}")
# ---- exact W in mp (sparse rows), eigenvalue in mp: lambda is a root of unity times a phase; refine as Rayleigh quotient
WiO = [[(j, mp.mpc(int(Wi[i, j].real), int(Wi[i, j].imag))) for j in np.nonzero(np.abs(Wi[i]) > 0.5)[0]] for i in range(d)]
sc = mp.sqrt(2) ** (-k2)
def Wmul(v):
    return [sc * mp.fsum(c * v[j] for j, c in row) for row in WiO]
Vm = [[mp.mpc(z.real, z.imag) for z in Q[:, c]] for c in range(m)]
others = [i for i in range(d) if i not in idx]
Uo = Ud[:, others]; Uinv = np.linalg.inv(Ud)
for it in range(4):
    WV = [Wmul(v) for v in Vm]
    lam = mp.fsum(mp.fsum(mp.conj(Vm[c][i]) * WV[c][i] for i in range(d)) for c in range(m)) / mp.fsum(mp.fsum(abs(z) ** 2 for z in v) for v in Vm)
    R = [[WV[c][i] - lam * Vm[c][i] for i in range(d)] for c in range(m)]
    rn = max(mp.sqrt(mp.fsum(abs(z) ** 2 for z in r_)) for r_ in R)
    log(f"refine {it}: residual {mp.nstr(rn, 3)}")
    if rn < mp.mpf(10) ** -45: break
    lamc = complex(lam)
    for c in range(m):
        rd = np.array([complex(z) for z in R[c]]) / max(float(rn), 1e-300)
        coef = Uinv[others] @ rd
        delta = Uo @ (coef / (ev[others] - lamc)) * float(rn)
        Vm[c] = [Vm[c][i] - mp.mpc(delta[i].real, delta[i].imag) for i in range(d)]
    # mp Gram-Schmidt
    for c in range(m):
        for c2 in range(c):
            ip = mp.fsum(mp.conj(Vm[c2][i]) * Vm[c][i] for i in range(d)); Vm[c] = [Vm[c][i] - ip * Vm[c2][i] for i in range(d)]
        nr = mp.sqrt(mp.fsum(abs(z) ** 2 for z in Vm[c])); Vm[c] = [z / nr for z in Vm[c]]
# ---- mp objective on the eigenspace
Xi = np.array([[mp.mpf(1 - 2 * trace(mul(a, b))) for b in range(q)] for a in range(q)], dtype=object)
PhiO = [np.array([[mp.mpf(1 - 2 * trace(mul(t, mul(a, b)))) for b in range(q)] for a in range(q)], dtype=object) for t in range(q)]
absq = np.vectorize(lambda z: abs(z) ** 2, otypes=[object])
VmA = np.array(Vm, dtype=object)            # m x d
def val_grad(x):
    t = np.array([mp.mpc(x[c], x[m + c]) for c in range(m)], dtype=object)
    A = t.dot(VmA); nrm = mp.sqrt(mp.fsum(abs(z) ** 2 for z in A)); A = A / nrm
    A2 = A.reshape(q, q); aA = absq(A2)
    f = mp.fsum(v * v for v in aA.ravel()); G = 2 * aA * A2
    for tt in range(q):
        K = Xi.dot(A2 * PhiO[tt]).dot(Xi) / q; aK = absq(K); f += mp.fsum(v * v for v in aK.ravel())
        G = G + PhiO[tt] * (Xi.dot(2 * aK * K).dot(Xi) / q)
    Gf = G.ravel(); ip = mp.fsum(mp.conj(a) * g for a, g in zip(A, Gf)); Gp = (Gf - mp.re(ip) * A) / nrm
    Gt = [mp.fsum(mp.conj(VmA[c][i]) * Gp[i] for i in range(d)) for c in range(m)]
    return (f - mp.mpf(q + 1) / q ** 2) * d, [2 * mp.re(z) for z in Gt] + [2 * mp.im(z) for z in Gt]
x0 = (Q.conj().T @ (Q @ (xbest[:m] + 1j * xbest[m:])))
x = [mp.mpf(z.real) for z in x0] + [mp.mpf(z.imag) for z in x0]
hist = []
for it in range(6):
    c, g = val_grad(x); gn = mp.sqrt(mp.fsum(v * v for v in g))
    hist.append((it, mp.nstr(c, 45), mp.nstr(gn, 3))); log(f"newton {it}: c = {mp.nstr(c, 45)}  |grad| = {mp.nstr(gn, 3)}")
    if gn < mp.mpf(10) ** -42: break
    h = mp.mpf(10) ** -22; n = 2 * m; H = mp.matrix(n, n)
    for i in range(n):
        xp = list(x); xm = list(x); xp[i] += h; xm[i] -= h
        gp = val_grad(xp)[1]; gm = val_grad(xm)[1]
        for j in range(n): H[j, i] = (gp[j] - gm[j]) / (2 * h)
    E, V = mp.eigsy((H + H.T) / 2); tol = mp.mpf(10) ** -10 * max(abs(e) for e in E)
    step = [mp.mpf(0)] * n
    for kk in range(n):
        if abs(E[kk]) > tol:
            co = mp.fsum(V[j, kk] * g[j] for j in range(n)) / E[kk]
            for j in range(n): step[j] += co * V[j, kk]
    x = [a - b for a, b in zip(x, step)]
c = val_grad(x)[0]
from math import gcd
Nf = q + 1; degf = sum(1 for j in range(1, Nf) if gcd(j, Nf) == 1) // 2
gN = 2 * mp.cos(2 * mp.pi / Nf)
rel = mp.pslq([c] + [gN ** kk for kk in range(degf)], maxcoeff=10 ** 7, maxsteps=10 ** 7)
res = dict(q=q, value=mp.nstr(c, 45), history=hist, field=f"Q(cos 2pi/{Nf})", degree=degf, pslq=str(rel))
if rel and rel[0]:
    coeffs = [mp.mpf(-v) / rel[0] for v in rel[1:]]
    def conj_val(k):
        g = 2 * mp.cos(2 * mp.pi * k / Nf); return mp.fsum(cf * g ** i for i, cf in enumerate(coeffs))
    ks = [k for k in range(1, Nf // 2 + 1) if gcd(k, Nf) == 1]
    conj = sorted(conj_val(k) for k in ks)
    poly = [mp.mpf(1)]
    for r_ in conj:
        y = Nf * r_; nw = [mp.mpf(0)] * (len(poly) + 1)
        for i, a in enumerate(poly): nw[i] += a; nw[i + 1] -= a * y
        poly = nw
    res.update(conjugates=[mp.nstr(v, 20) for v in conj], smallest_conjugate=bool(abs(conj[0] - c) < mp.mpf(10) ** -30),
               minimal_polynomial_of_Ntau=[str(int(mp.nint(a))) for a in poly], max_dist_to_int=mp.nstr(max(abs(a - mp.nint(a)) for a in poly), 3))
log(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_q32_torus_level_eigenspace_newton.json" if q == 32 else f"w33_q{q}_torus_level_eigenspace_newton.json"), "w"), indent=1)
