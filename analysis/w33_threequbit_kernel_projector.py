"""Pass 12647 item 3 (step 3): the exact kernel of the reduced degree-6 Gram block G0 (36x36) from the FULL minimiser variety.
The minimisers of F (three-qubit size-5 set, min 1/8) are not only the 160 stabiliser states: random-start minima fix exactly one of 15
uncovered Paulis (w33_threequbit_minimiser_variety.py), and their charge-1 monomial vectors span rank 25 (stabiliser states: 20).
Every minimiser's sector-shifted q(v) lies in ker G0.  Sample many minima, form the orthogonal projector P onto the span numerically,
round entries to Gaussian rationals, and verify EXACTLY: P^H = P, P^2 = P, rank 25, and P w = w for all 1280 exact stabiliser kernel
vectors.  Save an exact Gaussian-integer basis of the complement range(I - P) for the facially reduced certificate.
usage: py -3 analysis/w33_threequbit_kernel_projector.py"""
import os, contextlib, io, json
from fractions import Fraction as Fr
import numpy as np, sympy as sp
from scipy.optimize import minimize
from sympy.polys.matrices import DomainMatrix
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_exact_one_eighth.py")}
src = open(os.path.join(HERE, "w33_threequbit_exact_one_eighth.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("def exact_complement")], g)
E, qvec, qi, shiftG, s0G, kerG = g["red"]["E"], g["qvec"], g["qi"], g["shiftG"], g["s0G"], g["kerG"]; d = 8
def F(z):
    v = z[:d] + 1j * z[d:]; v = v / np.linalg.norm(v)
    return sum((abs(np.vdot(e, v)) ** 2 - 1 / d) ** 2 for e in E)
rng = np.random.default_rng(2026); vecs = [np.array(w_, complex) for w_ in kerG]; nmin = 0
while nmin < 600:
    r = minimize(F, rng.standard_normal(2 * d), method="BFGS", options=dict(gtol=1e-13))
    if r.fun < 0.125 + 1e-10:
        v = r.x[:d] + 1j * r.x[d:]; v /= np.linalg.norm(v); q = qvec(v); nmin += 1
        for a in range(d): vecs.append(np.array([q[qi[shiftG(t, a)]] for t in s0G]))
M = np.array(vecs).T
U_, s, _ = np.linalg.svd(M, full_matrices=False)
rk = int(np.sum(s > 1e-7 * s[0])); Q = U_[:, :rk]; P = Q @ Q.conj().T
print("numerical rank", rk, "| singular gap", s[rk - 1], s[rk] if rk < len(s) else 0, flush=True)
res = dict(n_minima=nmin, numerical_rank=rk)
for D in (2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256):
    Pr = [[Fr(round(P[i, j].real * D), D) + 0 for j in range(36)] for i in range(36)]
    Pi = [[Fr(round(P[i, j].imag * D), D) for j in range(36)] for i in range(36)]
    err = max(abs(float(Pr[i][j]) - P[i, j].real) + abs(float(Pi[i][j]) - P[i, j].imag) for i in range(36) for j in range(36))
    if err > 1e-8: continue
    K = sp.QQ.algebraic_field(sp.I)
    Pm = sp.Matrix(36, 36, lambda i, j: sp.Rational(Pr[i][j].numerator, Pr[i][j].denominator) + sp.I * sp.Rational(Pi[i][j].numerator, Pi[i][j].denominator))
    herm = (Pm - Pm.H).is_zero_matrix
    Pd = DomainMatrix.from_Matrix(Pm).convert_to(K)
    idem = (Pd * Pd - Pd).to_Matrix().is_zero_matrix
    rank_exact = Pd.rank()
    W = sp.Matrix([[sp.Integer(int(round(c.real))) + sp.I * sp.Integer(int(round(c.imag))) for c in w_] for w_ in kerG]).T
    contains = (DomainMatrix.from_Matrix(Pm * W - W).convert_to(K)).to_Matrix().is_zero_matrix
    print("D", D, "err", err, "hermitian", herm, "idempotent", idem, "rank", rank_exact, "contains stabiliser kernel", contains, flush=True)
    if herm and idem and rank_exact == rk and contains:
        comp = DomainMatrix.from_Matrix(sp.eye(36) - Pm).convert_to(K).columnspace().to_Matrix()
        basis = []
        for c in range(comp.shape[1]):
            col = [sp.nsimplify(comp[r, c]) for r in range(36)]
            den = sp.ilcm(*[sp.fraction(sp.together(sp.re(z)))[1] for z in col] + [sp.fraction(sp.together(sp.im(z)))[1] for z in col])
            basis.append([[int(sp.re(z) * den), int(sp.im(z) * den)] for z in col])
        res.update(exact=True, denominator=D, complement_dim=len(basis), complement_basis=basis)
        break
else:
    res["exact"] = False
print({k: v for k, v in res.items() if k != "complement_basis"}, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_kernel_projector.json"), "w"), indent=1)
