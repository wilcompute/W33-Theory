"""Pass 12649: kappa <= 3 via a degree-raised certificate (the decomposable one is infeasible).  With M_j the six 4x4 blocks (Gaussian
integer, scaled by nu), the target is p(x,y) = |y|^2 (3 nu^2 |x|^2 |y|^2 - sum_j |x^H M_j y|^2) >= 0.  Seek
  p = w^H G w + w'^H G' w',  w = x (x) Sym^2(y) (40),  w' = conj(x) (x) Sym^2(y) (40),  G, G' >= 0,
matching all coefficients of conj(x)_a x_a' conj(y)_b conj(y)_c y_d y_e.  Report the maximal interior margin; positive margin allows
exact rounding later.  usage: py -3 analysis/w33_kappa_symmetric_extension.py"""
import json, os, contextlib, io, itertools
import numpy as np, cvxpy as cp
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py")}
src = open(os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("# kappa numerically")], g)
Ms, nu = g["Ms"], g["nu"]
pairs = list(itertools.combinations_with_replacement(range(4), 2)); pi = {p: i for i, p in enumerate(pairs)}
# coefficient index: (a, a', (b,c) sorted-pair for conj(y), (d,e) sorted pair for y)  ;  a = conj(x) index, a' = x index
def cidx(a, a2, bc, de): return ((a * 4 + a2) * 10 + pi[bc]) * 10 + pi[de]
NC = 16 * 100
# target coefficients
def build_p(const):
  p = np.zeros(NC, complex)
# |y|^2 * 3 nu^2 |x|^2 |y|^2 :  sum_a conj(x_a) x_a * sum_{b,d} conj(y_b) y_b conj(y_d) y_d
  for a in range(4):
    for b in range(4):
        for dd in range(4):
            p[cidx(a, a, tuple(sorted((b, dd))), tuple(sorted((b, dd))))] += const * nu ** 2
# - |y|^2 sum_j |x^H M_j y|^2 = - sum_j sum conj(x_a) M_j[a,d] y_d * x_a' conj(M_j[a',e]) conj(y_e) * conj(y_f) y_f
  for M in Ms:
    for a, a2, dd, e, f in itertools.product(range(4), repeat=5):
        c = M[a, dd] * np.conj(M[a2, e])
        if c != 0: p[cidx(a, a2, tuple(sorted((e, f))), tuple(sorted((dd, f))))] -= c
  return p
# monomial map for w = x_a y_b y_c :  conj(w_(a,bc)) w_(a',de) -> conj(x_a) x_a' conj(y_b y_c) y_d y_e
idx40 = [(a, bc) for a in range(4) for bc in pairs]
rows, cols = [], []
for i, (a, bc) in enumerate(idx40):
    for j, (a2, de) in enumerate(idx40):
        rows.append(cidx(a, a2, bc, de)); cols.append(i * 40 + j)
Lw = sps.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(NC, 1600))
# w' = conj(x_a) y_b y_c : conj(w'_(a,bc)) w'_(a2,de) = x_a conj(x_a2) conj(y_b y_c) y_d y_e -> index (a2, a, bc, de)
rows2 = []
for i, (a, bc) in enumerate(idx40):
    for j, (a2, de) in enumerate(idx40):
        rows2.append(cidx(a2, a, bc, de))
Lw2 = sps.csr_matrix((np.ones(len(rows2)), (rows2, cols)), shape=(NC, 1600))
def herm(nm):
    R = cp.Variable((40, 40), symmetric=True, name=nm + "r"); I_ = cp.Variable((40, 40), name=nm + "i"); return R, I_
Gr, Gi = herm("G"); Hr, Hi = herm("H"); t = cp.Variable()
res = {}
for const, use_pt in ((4, False), (3, False), (3, True)):
    p = build_p(const)
    lhs_r = Lw @ cp.vec(Gr, order="C") + (Lw2 @ cp.vec(Hr, order="C") if use_pt else 0)
    lhs_i = Lw @ cp.vec(Gi, order="C") + (Lw2 @ cp.vec(Hi, order="C") if use_pt else 0)
    cons = [Gi == -Gi.T, cp.bmat([[Gr, -Gi], [Gi, Gr]]) >> t * np.eye(80), lhs_r == p.real, lhs_i == p.imag, t <= 1]
    if use_pt: cons += [Hi == -Hi.T, cp.bmat([[Hr, -Hi], [Hi, Hr]]) >> t * np.eye(80)]
    pr = cp.Problem(cp.Maximize(t), cons); pr.solve(solver=cp.SCS, eps=1e-9, max_iters=200000)
    res["const%d_%s" % (const, "pt" if use_pt else "plain")] = dict(margin=float(t.value) if t.value is not None else None, status=pr.status)
    print(res, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_kappa_symmetric_extension.json"), "w"), indent=1)
