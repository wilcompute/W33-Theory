"""Pass 12647 item 3 (step 1): the degree-6 real SOS for three-qubit size-5 sets, reduced by the 3-qubit Pauli group.
Monomial basis (unnormalised): F(v)|v|^2 - delta|v|^6 = sum_{alpha,beta} conj(v^alpha) K_{alpha beta} v^beta + sum_{a,b} conj(q_a) G_ab q_b,
v^alpha (alpha = degree-3 multiset), q_{(ij),k} = v_i v_j conj(v_k).  F and |v|^2 are Pauli invariant; Pauli X^a Z^b maps monomials to
(+-1) x monomials with Z-sector s = i+j+k (mod 2, bitwise) shifted by a.  The centre acts as -1 on both spaces, so each is 8 copies of
the unique 8-dim irrep: an invariant Gram matrix is block diagonal over sectors, with sector-a block = X^a-translate of the sector-0
block.  Hence K = (+) K0 (15x15), G = (+) G0 (36x36).  All coefficients are Gaussian rationals (cF from stabiliser projectors).
Maximise delta; expect 1/8.  Control: unreduced value 0.1249999831 (Pass 12642).
usage: py -3 analysis/w33_threequbit_pauli_reduced_sos.py"""
import itertools, json, os, contextlib, io, time
from collections import Counter
import numpy as np, cvxpy as cp
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index(chr(10) + "res = {}")], cs)
d = 8
pts, lag, w = cs["geometry"](2, 3); B = cs["bases_for"](2, 3, pts, lag); mps, _ = cs["maximal_partial_spreads"](lag)
S = sorted(next(S for S in mps if len(S) == 5))
E = [b for L in S for b in B[L].T]
mons = list(itertools.combinations_with_replacement(range(d), 3)); mi = {m: i for i, m in enumerate(mons)}; nm = len(mons)
sect = lambda idx: idx[0] ^ idx[1] ^ idx[2]
# exact Gaussian-rational projectors: 8 |e><e| has Gaussian-integer entries
Pex = []
for e in E:
    M8 = 8 * np.outer(e, e.conj()); R = np.round(M8.real) + 1j * np.round(M8.imag)
    assert np.abs(M8 - R).max() < 1e-9
    Pex.append(R)
def coefF():
    # coefficient of conj(v)^alpha v^beta in F|v|^2 with A_e = P_e - I/8 ; scaled by 64*8 = 512 to stay integral: A8 = 8 A_e = R - I
    c = np.zeros((nm, nm), complex)
    for R in Pex:
        A8 = R - np.eye(d)
        for i, j, i2, j2, k in itertools.product(range(d), repeat=5):
            a = A8[i, j] * A8[i2, j2]
            if a != 0: c[mi[tuple(sorted((i, i2, k)))], mi[tuple(sorted((j, j2, k)))]] += a
    return c  # = 64 * true coefficients
cF64 = coefF()
cN = np.zeros((nm, nm))
for i, j, k in itertools.product(range(d), repeat=3): cN[mi[tuple(sorted((i, j, k)))], mi[tuple(sorted((i, j, k)))]] += 1
qs = [((i, j), k) for i in range(d) for j in range(i, d) for k in range(d)]; qi = {q: n for n, q in enumerate(qs)}; nq = len(qs)
s0K = [m for m in mons if sect(m) == 0]; s0G = [q for q in qs if q[0][0] ^ q[0][1] ^ q[1] == 0]
print("sector-0 sizes:", len(s0K), len(s0G), flush=True)
def shiftK(m, a): return tuple(sorted(x ^ a for x in m))
def shiftG(q, a):
    (i, j), k = q; i2, j2 = sorted((i ^ a, j ^ a)); return ((i2, j2), k ^ a)
# linear maps: K0 (15x15 complex) -> coefficient matrix contributions;  G0 (36x36) -> via q-pair map
K0r = cp.Variable((15, 15), symmetric=True); K0i = cp.Variable((15, 15))
G0r = cp.Variable((36, 36), symmetric=True); G0i = cp.Variable((36, 36))
delta = cp.Variable()
# build sparse maps from vec(K0) and vec(G0) to vec(coefficient matrix)
rK, cK = [], []
for a in range(d):
    for x, m1 in enumerate(s0K):
        for y, m2 in enumerate(s0K):
            rK.append(mi[shiftK(m1, a)] * nm + mi[shiftK(m2, a)]); cK.append(x * 15 + y)
MK = sps.csr_matrix((np.ones(len(rK)), (rK, cK)), shape=(nm * nm, 225))
rG, cG = [], []
for a in range(d):
    for x, q1 in enumerate(s0G):
        for y, q2 in enumerate(s0G):
            (i, j), k = shiftG(q1, a); (l, m_), n_ = shiftG(q2, a)
            # conj(q1) q2 = conj(v_i v_j) v_k * v_l v_m conj(v_n): alpha = {i,j,n}, beta = {k,l,m}
            rG.append(mi[tuple(sorted((i, j, n_)))] * nm + mi[tuple(sorted((k, l, m_)))]); cG.append(x * 36 + y)
MG = sps.csr_matrix((np.ones(len(rG)), (rG, cG)), shape=(nm * nm, 1296))
lhs_r = MK @ cp.vec(K0r, order="C") + MG @ cp.vec(G0r, order="C")
lhs_i = MK @ cp.vec(K0i, order="C") + MG @ cp.vec(G0i, order="C")
cons = [cp.bmat([[K0r, -K0i], [K0i, K0r]]) >> 0, cp.bmat([[G0r, -G0i], [G0i, G0r]]) >> 0, K0i == -K0i.T, G0i == -G0i.T,
        lhs_r == (cF64.real / 64).reshape(-1) - delta * cN.reshape(-1), lhs_i == (cF64.imag / 64).reshape(-1)]
pr = cp.Problem(cp.Maximize(delta), cons)
t = time.time(); pr.solve(solver=cp.SCS, eps=1e-9, max_iters=200000)
res = dict(sector0_K=len(s0K), sector0_G=len(s0G), delta=float(delta.value), status=pr.status, seconds=time.time() - t,
           eig_K0=[float(x) for x in np.linalg.eigvalsh(np.block([[K0r.value, -K0i.value], [K0i.value, K0r.value]]))[:6]],
           eig_G0=[float(x) for x in np.linalg.eigvalsh(np.block([[G0r.value, -G0i.value], [G0i.value, G0r.value]]))[:6]])
print(res, flush=True)
np.savez(os.path.join(ROOT, "data", "w33_threequbit_pauli_reduced_sos_solution.npz"), K0=K0r.value + 1j * K0i.value, G0=G0r.value + 1j * G0i.value)
json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_pauli_reduced_sos.json"), "w"), indent=1)
