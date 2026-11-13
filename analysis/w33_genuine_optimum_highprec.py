"""Pass 12650 item 4: the isolated genuine four-qubit optimum (type A, lines [129,190,287,444,530]) to high precision, then a STRICT
identification attempt.  f(v) = sum_{P in C} (v^H P v)^2 / (16 (v^H v)^2).  Gauge fixed by v_0 = 1 (real) -> 30 real unknowns; Newton on
the gradient in mpmath (dps 80) from the double-precision optimum; the Jacobian by central differences at step 1e-35.  Identification is
accepted only for degree <= 4, |coefficients| <= 10^4 and residual < 1e-45 (~3e21 candidate polynomials: chance match negligible).
usage: py -3 analysis/w33_genuine_optimum_highprec.py"""
import json, os
import numpy as np, mpmath as mp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex2 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
s2 = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(s2[: s2.index("rows, cols = []")], ex2)
C = sorted(frozenset().union(*[ex2["lags"][i] for i in [129, 190, 287, 444, 530]]))
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(v):
    M = np.eye(1)
    for i in range(4):
        x = (v >> i) & 1; z = (v >> (4 + i)) & 1
        M = np.kron(M, (1j) ** (x * z) * np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z))
    return M
Ps = [pauli(v) for v in C]
# sparse Pauli action: P v = phase_k * v[perm_k]
acts = []
for P in Ps:
    perm = [int(np.flatnonzero(np.abs(P[r]) > 0.5)[0]) for r in range(16)]
    ph = [complex(np.round(P[r, perm[r]].real) + 1j * np.round(P[r, perm[r]].imag)) for r in range(16)]
    acts.append((perm, ph))
def fnum(z):
    v = z[:16] + 1j * z[16:]; v = v / np.linalg.norm(v)
    return float(sum((np.vdot(v, P @ v).real) ** 2 for P in Ps)) / 16
rng = np.random.default_rng(7)
best = min((minimize(fnum, rng.standard_normal(32), method="BFGS", options=dict(gtol=1e-13)) for _ in range(40)), key=lambda r: r.fun)
v0 = best.x[:16] + 1j * best.x[16:]; v0 = v0 / v0[0]
mp.mp.dps = 80
PH = [(perm, [mp.mpc(c.real, c.imag) for c in ph]) for perm, ph in acts]
def f_mp(u):  # u: 30 reals -> v = (1, u)
    v = [mp.mpc(1, 0)] + [mp.mpc(u[2 * k], u[2 * k + 1]) for k in range(15)]
    nv = mp.fsum(abs(c) ** 2 for c in v)
    tot = mp.mpf(0)
    for perm, ph in PH:
        s = mp.fsum(mp.conj(v[r]) * ph[r] * v[perm[r]] for r in range(16))
        tot += mp.re(s) ** 2
    return tot / (16 * nv ** 2)
def grad(u, h=mp.mpf("1e-35")):
    gvec = []
    for k in range(30):
        up = list(u); um = list(u); up[k] += h; um[k] -= h
        gvec.append((f_mp(up) - f_mp(um)) / (2 * h))
    return gvec
u = [mp.mpf(repr(float(x))) for c in v0[1:] for x in (c.real, c.imag)]
for it in range(8):
    gv = grad(u)
    gn = mp.sqrt(mp.fsum(x ** 2 for x in gv)); print("iter", it, "f =", mp.nstr(f_mp(u), 30), "|grad| =", mp.nstr(gn, 5), flush=True)
    if gn < mp.mpf("1e-60"): break
    hh = mp.mpf("1e-25"); J = mp.matrix(30, 30)
    for k in range(30):
        up = list(u); um = list(u); up[k] += hh; um[k] -= hh
        gp, gm = grad(up), grad(um)
        for i in range(30): J[i, k] = (gp[i] - gm[i]) / (2 * hh)
    step = mp.lu_solve(J, mp.matrix(gv))
    u = [u[i] - step[i] for i in range(30)]
fstar = f_mp(u)
print("f* =", mp.nstr(fstar, 60), flush=True)
accepted = None
for deg in (1, 2, 3, 4):
    p = mp.findpoly(fstar, deg, maxcoeff=10000, tol=mp.mpf("1e-45"))
    if p:
        resid = abs(mp.polyval(p, fstar))
        if resid < mp.mpf("1e-45"): accepted = dict(degree=deg, coefficients=[int(c) for c in p], residual=mp.nstr(resid, 5)); break
res = dict(f_star=mp.nstr(fstar, 60), double_precision=best.fun, identification=accepted,
           rule="accept only degree <= 4, |coef| <= 1e4, residual < 1e-45")
print(res, flush=True); json.dump(res, open(os.path.join(ROOT, "data", "w33_genuine_optimum_highprec.json"), "w"), indent=1)
