"""Item 2: three-qubit size-5 sets, degree-6 real SOS (Hermitian charge-3 block + charge-1 block).
F(v)|v|^2 - delta |v|^6 = (v^(x)3)^dag H3 v^(x)3 + sum_{a,b} G_ab conj(q_a) q_b,  q_{(ij),k}(v) = v_i v_j conj(v_k) (i <= j),  H3, G Hermitian PSD.
Work in monomial-coefficient space: c[alpha, beta] = coefficient of conj(v)^alpha v^beta (alpha, beta degree-3 multisets).
(v^(x)3)^dag H v^(x)3 has c = sqrt(m_alpha m_beta) H[alpha, beta] (m = multinomial counts) in the orthonormal Sym^3 basis.
conj(q_a) q_b = conj(v_i v_j) v_k * v_l v_m conj(v_n)  ->  alpha = sorted(i, j, n), beta = sorted(k, l, m).
Maximise delta (SCS).  Control: the two-qutrit pentad would be too large (d = 9: 405-dim charge-1 block); instead control on the two-qubit
size-3 set (d = 4; degree-4 already certifies 1/4, so delta must come out > 0).
usage: py -3 analysis/w33_threequbit_degree6.py"""
import itertools, json, os, time
from collections import Counter
import numpy as np, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
exec(_src[: _src.index("\nres = {}")], cs)
geometry, bases_for, maximal_partial_spreads = cs["geometry"], cs["bases_for"], cs["maximal_partial_spreads"]
from math import factorial
def solve(E, d):
    mons = list(itertools.combinations_with_replacement(range(d), 3)); mi = {m: i for i, m in enumerate(mons)}; nm = len(mons)
    mult = np.array([factorial(3) / np.prod([factorial(c) for c in Counter(m).values()]) for m in mons])
    sq = np.sqrt(np.outer(mult, mult))
    # coefficients of F |v|^2: F = sum_e (v^dag A_e v)^2, A_e = |e><e| - I/d ; F|v|^2 = sum_e (v^dag A v)^2 (v^dag v)
    cF = np.zeros((nm, nm), complex)
    for e in E:
        A = np.outer(e, e.conj()) - np.eye(d) / d
        # (sum_ij conj(v_i) A_ij v_j)^2 (sum_k conj(v_k) v_k): conj indices (i, i2, k), plain indices (j, j2, k)
        for i, j, i2, j2, k in itertools.product(range(d), repeat=5):
            a = A[i, j] * A[i2, j2]
            if a != 0:
                cF[mi[tuple(sorted((i, i2, k)))], mi[tuple(sorted((j, j2, k)))]] += a
    cN = np.zeros((nm, nm))
    for i, j, k in itertools.product(range(d), repeat=3):
        cN[mi[tuple(sorted((i, j, k)))], mi[tuple(sorted((i, j, k)))]] += 1
    qs = [((i, j), k) for i in range(d) for j in range(i, d) for k in range(d)]; nq = len(qs)
    # linear map G -> c_L: c_L[alpha, beta] += G[a, b], a = ((i,j),k), b = ((l,m),n): alpha = sorted(i,j,n), beta = sorted(k,l,m)
    rows, cols = [], []
    for a, ((i, j), k) in enumerate(qs):
        for b, ((l, m), n) in enumerate(qs):
            rows.append(mi[tuple(sorted((i, j, n)))] * nm + mi[tuple(sorted((k, l, m)))]); cols.append(a * nq + b)
    import scipy.sparse as sp
    Lmap = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(nm * nm, nq * nq))
    Gr = cp.Variable((nq, nq), symmetric=True); Gi = cp.Variable((nq, nq))
    Hr = cp.Variable((nm, nm), symmetric=True); Hi = cp.Variable((nm, nm))
    delta = cp.Variable()
    cons = [cp.bmat([[Gr, -Gi], [Gi, Gr]]) >> 0, cp.bmat([[Hr, -Hi], [Hi, Hr]]) >> 0, Gi == -Gi.T, Hi == -Hi.T]
    cLr = cp.reshape(Lmap @ cp.vec(Gr, order="C"), (nm, nm), order="C"); cLi = cp.reshape(Lmap @ cp.vec(Gi, order="C"), (nm, nm), order="C")
    cons += [cF.real - delta * cN == cp.multiply(sq, Hr) + cLr, cF.imag == cp.multiply(sq, Hi) + cLi]
    prob = cp.Problem(cp.Maximize(delta), cons)
    t = time.time()
    prob.solve(solver=cp.SCS, eps=1e-6, max_iters=20000)
    el = time.time() - t
    G = Gr.value + 1j * Gi.value; H = Hr.value + 1j * Hi.value; dl = float(delta.value)
    # independent check: evaluate the identity at random points directly from the polynomial definitions
    rng = np.random.default_rng(11); resid = 0.0
    for _ in range(50):
        v = rng.standard_normal(d) + 1j * rng.standard_normal(d)
        Fv = sum((np.vdot(v, (np.outer(e, e.conj()) - np.eye(d) / d) @ v).real) ** 2 for e in E)
        x = np.array([np.prod([v[i] for i in m]) * np.sqrt(mt) for m, mt in zip(mons, mult)])
        q = np.array([v[i] * v[j] * np.conj(v[k]) for (i, j), k in qs])
        lhs = Fv * np.vdot(v, v).real - dl * np.vdot(v, v).real ** 3
        rhs = np.vdot(x, H @ x).real + np.vdot(q, G @ q).real
        resid = max(resid, abs(lhs - rhs) / np.vdot(v, v).real ** 3)
    from scipy.optimize import minimize
    def Fn(z):
        v = z[:d] + 1j * z[d:]; v = v / np.linalg.norm(v)
        return sum((np.vdot(v, (np.outer(e, e.conj()) - np.eye(d) / d) @ v).real) ** 2 for e in E)
    fmin = min(minimize(Fn, rng.standard_normal(2 * d), method="BFGS").fun for _ in range(60))
    return dict(delta=dl, status=prob.status, seconds=el, identity_max_rel_residual=float(resid),
                eig_min_G=float(np.linalg.eigvalsh((G + G.conj().T) / 2)[0]), eig_min_H=float(np.linalg.eigvalsh((H + H.conj().T) / 2)[0]),
                numeric_min_F=float(fmin))
res = {}
pts, lag, w = geometry(2, 2); B = bases_for(2, 2, pts, lag); mps, _ = maximal_partial_spreads(lag)
three = sorted(next(S for S in mps if len(S) == 3))
res["control_d4_size3"] = solve([b for L in three for b in B[L].T], 4)
print("control two-qubit size-3 (degree-6):", res["control_d4_size3"], flush=True)
pts, lag, w = geometry(2, 3); B = bases_for(2, 3, pts, lag); mps, _ = maximal_partial_spreads(lag)
five = sorted(next(S for S in mps if len(S) == 5))
res["d8_size5"] = solve([b for L in five for b in B[L].T], 8)
print("three-qubit size-5 (degree-6 real SOS):", res["d8_size5"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_degree6.json"), "w"), indent=1, default=str)
