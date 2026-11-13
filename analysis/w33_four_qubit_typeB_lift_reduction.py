"""Pass 12652 addendum: towards an exact 1/16 for the LIFTED four-qubit five-set (type B, Pass 12648; theta = 14.609 > 14, so the
Lovasz route cannot be tight; open item 'exact certificate at 1/16 for type B').
Reduction through a lift point p (uncovered, Pass 12648: 120 of them).  Write v = t u (+) s w with u, w unit vectors in the +1 / -1
eigenspaces of p.  Paulis commuting with p are block-diagonal, anticommuting ones are off-diagonal, so
    Sigma_U(v) = t^4 a(u) + s^4 b(w) + t^2 s^2 c(u, w)       (no odd powers of t, s),
with a(u) = Sigma_U(u (+) 0), b(w) = Sigma_U(0 (+) w), c = Sigma_U(u (+) w) - a(u) - b(w).
a, b <= 14 reduce to the THREE-qubit theorem of Pass 12652 (quotient p^perp/<p> = W(5,2), the five Lagrangians project to a maximal
three-qubit five-set).  Hence: max c <= 28  ==>  Sigma_U <= 14 (t^2 + s^2)^2 = 14  ==>  min F = 1/16 for type B.
This script (1) checks the decomposition identity at random points, (2) checks a, b <= 14 numerically, (3) maximises c.
Control: the same reduction for type A (genuine, no lift point; min F = 0.05236 < 1/16) at an arbitrary uncovered point must FAIL
(max Sigma_U > 14 there), so the script cannot pass vacuously.
usage: py -3 analysis/w33_four_qubit_typeB_lift_reduction.py"""
import json, os, time
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py")}
src = open(os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py"), encoding="utf-8").read()
exec(src[: src.index("def decide")], ex)
lags, NV = ex["lagrangians"](4); n = 4; lo = 15; d = 16
w_ = lambda x, y: (bin((x & lo) & (y >> n)).count("1") + bin((x >> n) & (y & lo)).count("1")) % 2
census = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_size5_census.json")))
X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)


def pauli(x):
    M = np.eye(1)
    for i in range(n):
        xi, zi = x >> i & 1, x >> (n + i) & 1
        M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
    return M


P = {x: pauli(x) for x in range(1, NV)}
# sanity: commutation of matrices matches w_
for x, y in ((3, 17), (5, 80), (129, 6), (33, 34)):
    assert np.allclose(P[x] @ P[y], (-1) ** w_(x, y) * P[y] @ P[x])


def lift_points(S, C):
    good = []
    for p in range(1, NV):
        if p in C: continue
        imgs = [frozenset(frozenset((x, x ^ p)) for x in lags[i] if w_(x, p) == 0) for i in S]
        if any(len(a & b) for k, a in enumerate(imgs) for b in imgs[k + 1:]): continue
        union = frozenset().union(*imgs)
        qlags = [frozenset(frozenset((x, x ^ p)) for x in M if x != p) for M in lags if p in M]
        if all(len(q & union) > 0 for q in qlags): good.append(p)
    return good


def analyse(S, p, starts=40, seed=0):
    C = frozenset().union(*[lags[i] for i in S]) - {0}
    U = [x for x in range(1, NV) if x not in C]
    PU = np.array([P[x] for x in U])
    ev, V = np.linalg.eigh(P[p]); Vm, Vp = V[:, ev < 0], V[:, ev > 0]
    SU = lambda v: float((np.einsum("i,kij,j->k", v.conj(), PU, v).real ** 2).sum())
    rng = np.random.default_rng(seed)
    rnd = lambda: (lambda z: z / np.linalg.norm(z))(rng.standard_normal(8) + 1j * rng.standard_normal(8))
    # (1) decomposition identity
    for _ in range(20):
        u, w = rnd(), rnd(); t, s = rng.random(2)
        lhs = SU(t * Vp @ u + s * Vm @ w)
        a, b = SU(Vp @ u), SU(Vm @ w); c = SU(Vp @ u + Vm @ w) - a - b
        assert abs(lhs - (t ** 4 * a + s ** 4 * b + t ** 2 * s ** 2 * c)) < 1e-9

    def maxf(f, dim_pairs):
        best = -1e9
        for _ in range(starts):
            z0 = rng.standard_normal(4 * 8 if dim_pairs == 2 else 2 * 8)
            r = minimize(lambda z: -f(z), z0, method="L-BFGS-B")
            best = max(best, -r.fun)
        return best
    cv = lambda z: z[:8] + 1j * z[8:16]
    nrm = lambda q: q / np.linalg.norm(q)
    amax = maxf(lambda z: SU(Vp @ nrm(cv(z))), 1)
    bmax = maxf(lambda z: SU(Vm @ nrm(cv(z))), 1)

    def cfun(z):
        u, w = nrm(cv(z[:16])), nrm(cv(z[16:]))
        return SU(Vp @ u + Vm @ w) - SU(Vp @ u) - SU(Vm @ w)
    cmax = maxf(cfun, 2)
    full = maxf(lambda z: SU(nrm(z[:16] + 1j * z[16:32])) if False else SU(nrm(np.concatenate([z[:8], z[8:16]]) + 1j * np.concatenate([z[16:24], z[24:32]]))), 2)
    return dict(p=p, n_U=len(U), a_max=amax, b_max=bmax, c_max=cmax, SigmaU_max=full, sufficient=bool(amax <= 14 + 1e-6 and bmax <= 14 + 1e-6 and cmax <= 28 + 1e-6))


t0 = time.time(); out = {}
for name, t in zip(("A_genuine", "B_lifted"), census["types"]):
    S = t["example"]; C = frozenset().union(*[lags[i] for i in S])
    lp = lift_points(S, C)
    p = lp[0] if lp else next(x for x in range(1, NV) if x not in C)
    r = analyse(S, p); r.update(n_lift_points=len(lp), used_lift_point=bool(lp))
    if lp:  # a second lift point for robustness
        r2 = analyse(S, lp[len(lp) // 2], seed=1); r["second_lift_point"] = r2
    out[name] = r; print(name, r, round(time.time() - t0), "s", flush=True)
out["seconds"] = round(time.time() - t0, 1)
json.dump(out, open(os.path.join(ROOT, "data", "w33_four_qubit_typeB_lift_reduction.json"), "w"), indent=1, default=float)
