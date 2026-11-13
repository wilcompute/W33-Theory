"""Pass 12650 item 1: kappa <= 3 at higher certificate levels.  Target: q(x,y) = 3 nu^2 |x|^2|y|^2 - sum_j |x^H M_j y|^2 >= 0 for all x, y
(M_j the six 4x4 Gaussian-integer blocks of Lemma B).  Level (a,b): p = |x|^{2(a-1)} |y|^{2(b-1)} q is written as
  p = sum over blocks of  w^H G w,   w in { Sym^a(x) (x) Sym^b(y),  Sym^a(x) (x) Sym^b(conj y) [PT_y],  Sym^a(conj x) (x) Sym^b(y) [PT_x] },
G >= 0, coefficient matching on monomials conj(x)^A x^B conj(y)^C y^D.  Maximise the interior margin.  Controls: constant 4 feasible;
level (1,2) reproduces Pass 12649 (infeasible).  usage: py -3 analysis/w33_kappa_hierarchy.py"""
import json, os, contextlib, io, itertools
from collections import defaultdict
import numpy as np, cvxpy as cp
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py")}
src = open(os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("# kappa numerically")], g)
Ms, nu = g["Ms"], g["nu"]
Z4 = (0, 0, 0, 0)
def e(i):
    v = [0, 0, 0, 0]; v[i] = 1; return tuple(v)
def addv(a, b): return tuple(x + y for x, y in zip(a, b))
def pmul(P, Q):
    R = defaultdict(complex)
    for (a1, b1, c1, d1), u in P.items():
        for (a2, b2, c2, d2), v in Q.items():
            R[(addv(a1, a2), addv(b1, b2), addv(c1, c2), addv(d1, d2))] += u * v
    return R
nx2 = {(e(i), e(i), Z4, Z4): 1 for i in range(4)}   # |x|^2 : conj(x)_i x_i
ny2 = {(Z4, Z4, e(i), e(i)): 1 for i in range(4)}
def q_poly(const):
    P = defaultdict(complex)
    for i in range(4):
        for k in range(4): P[(e(i), e(i), e(k), e(k))] += const * nu ** 2
    for M in Ms:
        # |x^H M y|^2 = sum conj(x_a) M[a,d] y_d * x_a2 conj(M[a2,e]) conj(y_e)
        for a, dd, a2, ee in itertools.product(range(4), repeat=4):
            c = M[a, dd] * np.conj(M[a2, ee])
            if c != 0: P[(e(a), e(a2), e(ee), e(dd))] -= c
    return P
def multisets(deg):
    return [tuple(sum(1 for t in comb if t == i) for i in range(4)) for comb in itertools.combinations_with_replacement(range(4), deg)]
def solve(a, b, const, blocks):
    p = q_poly(const)
    for _ in range(a - 1): p = pmul(p, nx2)
    for _ in range(b - 1): p = pmul(p, ny2)
    X, Y = multisets(a), multisets(b); basis = [(u, v) for u in X for v in Y]; nB = len(basis)
    keys = {}; terms = []
    def key(k):
        if k not in keys: keys[k] = len(keys)
        return keys[k]
    Gs = []
    for blk in blocks:
        rows, cols = [], []
        for i, (u1, v1) in enumerate(basis):
            for j, (u2, v2) in enumerate(basis):
                if blk == "plain":   # conj(x^u1 y^v1) x^u2 y^v2
                    k = (u1, u2, v1, v2)
                elif blk == "pt_y":  # w = x^u (conj y)^v : conj(w1) w2 = conj(x)^u1 y^v1 x^u2 conj(y)^v2
                    k = (u1, u2, v2, v1)
                else:                # pt_x: w = (conj x)^u y^v
                    k = (u2, u1, v1, v2)
                rows.append(key(k)); cols.append(i * nB + j)
        Gs.append((rows, cols))
    for k in p: key(k)
    NC = len(keys); target = np.zeros(NC, complex)
    for k, v in p.items(): target[keys[k]] += v
    t = cp.Variable(); lhs_r = 0; lhs_i = 0; cons = []
    for rows, cols in Gs:
        L = sps.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(NC, nB * nB))
        Gr = cp.Variable((nB, nB), symmetric=True); Gi = cp.Variable((nB, nB))
        cons += [Gi == -Gi.T, cp.bmat([[Gr, -Gi], [Gi, Gr]]) >> t * np.eye(2 * nB)]
        lhs_r = lhs_r + L @ cp.vec(Gr, order="C"); lhs_i = lhs_i + L @ cp.vec(Gi, order="C")
    cons += [lhs_r == target.real, lhs_i == target.imag, t <= 1]
    pr = cp.Problem(cp.Maximize(t), cons); pr.solve(solver=cp.SCS, eps=1e-8, max_iters=100000)
    return dict(level=[a, b], const=const, blocks=blocks, basis_size=nB, margin=float(t.value) if t.value is not None else None, status=pr.status)
res = []
for a, b, const, blocks in [(1, 2, 4, ["plain"]), (1, 2, 3, ["plain", "pt_y"]), (2, 1, 3, ["plain", "pt_x"]), (2, 2, 3, ["plain"]),
                            (2, 2, 3, ["plain", "pt_y"]), (2, 2, 3, ["plain", "pt_x", "pt_y"])]:
    r = solve(a, b, const, blocks); res.append(r); print(r, flush=True)
    json.dump(res, open(os.path.join(ROOT, "data", "w33_kappa_hierarchy.json"), "w"), indent=1)
