"""Pass 12672: degree-6 real SOS with the U(1)-phase block structure, for the F_8 regulus objective on the 8-dim code space of the
rank-3 Pauli group T (Pass 12671).  g(t) = 64 F(Bt) for |t| = 1 is the bihomogeneous quartic sum_j 64|u_j.t|^4 - 9|t|^4.
Certificate sought:  |t|^2 (g - c |t|^4) = sum over charge blocks q in {3, 1} of m_q^dagger G_q m_q,  G_q Hermitian PSD,
m_3 = (t^alpha, |alpha| = 3) (120), m_1 = (t^alpha conj(t_i), |alpha| = 2) (288).  conj(t^a1 tbar^b1) t^a2 tbar^b2 has coefficient key
(tbar-exponent a1 + b2, t-exponent b1 + a2).  Since real polynomials in (Re t, Im t) invariant under the phase are exactly
charge-0 Hermitian combinations, and an invariant SOS can be averaged to a charge-block-diagonal one, this is the full degree-6
SOS bound with multiplier |t|^2.  c_SOS6 <= min of g on the code space.   usage: py -3 analysis/w33_f8_codespace_sos6.py"""
import itertools, json, math, os, sys, time
from math import factorial
import numpy as np
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
qsrc = open(os.path.join(HERE, "w33_f8_codespace_quillen.py"), encoding="utf-8").read()
gq = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_codespace_quillen.py")}
sys_argv = sys.argv; import sys as _s; _s.argv = ["x", "3", "0"]
exec(qsrc[: qsrc.index("res = dict(")], gq); _s.argv = sys_argv
S, G2, n, multis_fast, mf, C8 = gq["S"], gq["G2"], gq["n"], gq["multis_fast"], gq["mf"], gq["C8"]
idx2 = {g: i for i, g in enumerate(G2)}
G3 = multis_fast(3); idx3 = {g: i for i, g in enumerate(G3)}
E = [tuple(int(k == i) for k in range(n)) for i in range(n)]
addm = lambda a, b: tuple(x + y for x, y in zip(a, b))
# target: coefficient matrix (unique) of |t|^2 g on (3,3) monomials: C[A,B] = sum_i S[A - e_i, B - e_i]
Ct = np.zeros((len(G3), len(G3)), complex)
for i in range(n):
    for a, ga in enumerate(G2):
        for b, gb in enumerate(G2):
            if S[a, b] != 0: Ct[idx3[addm(ga, E[i])], idx3[addm(gb, E[i])]] += S[a, b]
D6 = np.diag([factorial(3) / mf(a) for a in G3])  # |t|^6
keys = {}
def key(A, Bk):
    k_ = (A, Bk)
    if k_ not in keys: keys[k_] = len(keys)
    return keys[k_]
for A in G3:
    for Bk in G3: key(A, Bk)
# block 3: m = t^alpha (a=alpha, b=0): conj(m1) m2 -> (alpha1, alpha2)
m3 = [(a, (0,) * n) for a in G3]
m1 = [(a, E[i]) for a in G2 for i in range(n)]
def amap(ms):
    r, c_, L = [], [], len(ms)
    for p, (a1, b1) in enumerate(ms):
        for qq, (a2, b2) in enumerate(ms):
            r.append(key(addm(a1, b2), addm(b1, a2))); c_.append(p * L + qq)
    return sps.csr_matrix((np.ones(len(r)), (r, c_)), shape=(len(keys), L * L))
A3, A1 = amap(m3), amap(m1)
K = len(keys)
tvec = np.zeros(K, complex); dvec = np.zeros(K, complex)
for ia, A in enumerate(G3):
    for ib, Bk in enumerate(G3):
        tvec[keys[(A, Bk)]] = Ct[ia, ib]; dvec[keys[(A, Bk)]] = D6[ia, ib]
# Direct Clarabel formulation (cvxpy canonicalisation needs > 200 GB here).  A Hermitian PSD X is represented by a symmetric
# PSD Y of twice the size through X = (Y11 + Y22)/2 + i (Y21 - Y21^T)/2 (any PSD Y gives a Hermitian PSD X, and conversely).
import scs
L3, L1 = len(m3), len(m1)
nv3, nv1 = (2 * L3) * (2 * L3 + 1) // 2, (2 * L1) * (2 * L1 + 1) // 2
off3, off1 = 1, 1 + nv3; NV = 1 + nv3 + nv1
SIZE = {}
def sidx(i, j, n_):  # SCS svec: lower triangle, column-major, off-diagonals scaled by sqrt2; Y[i,j] = y[idx] * scale
    if i < j: i, j = j, i
    return j * n_ - j * (j - 1) // 2 + (i - j), (1.0 if i == j else 1 / math.sqrt(2))
rows, cols, vals = [], [], []
def add(r, off, i, j, w):
    k, sc = sidx(i, j, SIZE[off]); rows.append(r); cols.append(off + k); vals.append(w * sc)
SIZE[off3] = 2 * L3; SIZE[off1] = 2 * L1
for Am, L, off in ((A3, L3, off3), (A1, L1, off1)):
    Am = Am.tocoo()
    for r, col in zip(Am.row, Am.col):
        p_, q_ = divmod(int(col), L)
        add(int(r), off, p_, q_, 0.5); add(int(r), off, L + p_, L + q_, 0.5)                  # Re: Xr[p,q]
        add(K + int(r), off, L + p_, q_, 0.5); add(K + int(r), off, L + q_, p_, -0.5)          # Im: Xi[p,q]
for r in range(K): rows.append(r); cols.append(0); vals.append(dvec.real[r])                 # + c * d  (Re rows)
Aeq = sps.csr_matrix((vals, (rows, cols)), shape=(2 * K, NV))
beq = np.concatenate([tvec.real, tvec.imag])
Apsd = -sps.eye(NV, format="csr")[1:]
A = sps.vstack([Aeq, Apsd]).tocsc(); b = np.concatenate([beq, np.zeros(NV - 1)])
qv = np.zeros(NV); qv[0] = -1.0
t0 = time.time()
solver = scs.SCS(dict(A=A, b=b, c=qv), dict(z=2 * K, s=[2 * L3, 2 * L1]), eps_abs=1e-7, eps_rel=1e-7, max_iters=200000, verbose=False)
sol = solver.solve()
class _S: pass
sol_ = _S(); sol_.x = sol["x"]; sol_.status = sol["info"]["status"]; sol = sol_
val = float(sol.x[0]); status = str(sol.status)
print(f"degree-6 phase-block SOS on the rank-3 code space: c_SOS6 = {val:.10f}  (c8 = {C8:.10f}, gap {val - C8:.2e}); status {status}; "
      f"blocks {L3} + {L1}; {time.time() - t0:.0f}s", flush=True)
json.dump(dict(c_sos6=val, c8=C8, gap=val - C8, status=status, blocks=[L3, L1], n_constraints=2 * K),
          open(os.path.join(ROOT, "data", "w33_f8_codespace_sos6.json"), "w"), indent=1)
