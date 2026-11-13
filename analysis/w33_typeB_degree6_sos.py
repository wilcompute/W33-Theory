"""Pass 12658: degree-6 real SOS for the F_4 regulus set (type B, four qubits, d = 16), reduced by the four-qubit Pauli group,
porting w33_threequbit_pauli_reduced_sos.py (Pass 12647).  F(v)|v|^2 - delta |v|^6 = sum conj(v^alpha) K v^beta + sum conj(q) G q,
v^alpha degree-3 monomials (816), q = v_i v_j conj(v_k) (2176); X^a translation + Z-sector block structure reduce the Gram matrices to
one 51 x 51 and one 136 x 136 Hermitian block.  The 80 basis vectors are those of the CZ model: e_x and CZ_t (F (x) F) e_k, t in F_4
(entries +-1/4).  Maximise delta; 1/16 = 0.0625 would be the exact value (numerical minimum of F).
Control: with only the computational basis and the t = 0 basis (two MUBs, not maximal) the true minimum of F is 0 (a vector unbiased
to both exists), so delta must come out <= 0 there.   usage: py -3 analysis/w33_typeB_degree6_sos.py"""
import itertools, json, os, time
import numpy as np, cvxpy as cp
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_mub_sets.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_mub_sets.py")}
exec(src[: src.index("g = {")], g)
q, mul, trace = g["field"](2); d = 16
chi = lambda y: 1 - 2 * trace(y)
idx = lambda x1, x2: x1 + 4 * x2


def bases(ts):
    E = [np.eye(d)[x] for x in range(d)]
    for t in ts:
        for k1 in range(4):
            for k2 in range(4):
                E.append(np.array([chi(mul(t, mul(x % 4, x // 4)) ^ mul(k1, x % 4) ^ mul(k2, x // 4)) for x in range(d)]) / 4.0)
    return E


mons = list(itertools.combinations_with_replacement(range(d), 3)); mi = {m: i for i, m in enumerate(mons)}; nm = len(mons)
sect = lambda m: m[0] ^ m[1] ^ m[2]
qs = [((i, j), k) for i in range(d) for j in range(i, d) for k in range(d)]
s0K = [m for m in mons if sect(m) == 0]; s0G = [qq for qq in qs if qq[0][0] ^ qq[0][1] ^ qq[1] == 0]
nK, nG = len(s0K), len(s0G); print("sector-0 sizes:", nK, nG, flush=True)
shiftK = lambda m, a: tuple(sorted(x ^ a for x in m))
def shiftG(qq, a):
    (i, j), k = qq; i2, j2 = sorted((i ^ a, j ^ a)); return ((i2, j2), k ^ a)
# rows: only same-sector (alpha, beta) pairs
pairs = {}
for al in mons:
    for be in mons:
        if sect(al) == sect(be): pairs[(mi[al], mi[be])] = len(pairs)
nrow = len(pairs)
rK, cK = [], []
for a in range(d):
    for x, m1 in enumerate(s0K):
        for y, m2 in enumerate(s0K):
            rK.append(pairs[(mi[shiftK(m1, a)], mi[shiftK(m2, a)])]); cK.append(x * nK + y)
MK = sps.csr_matrix((np.ones(len(rK)), (rK, cK)), shape=(nrow, nK * nK))
rG, cG = [], []
for a in range(d):
    for x, q1 in enumerate(s0G):
        for y, q2 in enumerate(s0G):
            (i, j), k = shiftG(q1, a); (l, m_), n_ = shiftG(q2, a)
            rG.append(pairs[(mi[tuple(sorted((i, j, n_)))], mi[tuple(sorted((k, l, m_)))])]); cG.append(x * nG + y)
MG = sps.csr_matrix((np.ones(len(rG)), (rG, cG)), shape=(nrow, nG * nG))
cN = np.zeros(nrow)
for i, j, k in itertools.product(range(d), repeat=3):
    m = mi[tuple(sorted((i, j, k)))]; cN[pairs[(m, m)]] += 1


def coefF(E):
    T2 = np.zeros((d, d, d, d))
    for e in E:
        A = np.outer(e, e) - np.eye(d) / d
        T2 += np.einsum("ij,kl->ikjl", A, A)  # [i, i2, j, j2]
    c = np.zeros(nrow)
    nz = np.argwhere(np.abs(T2) > 1e-12)
    for i, i2, j, j2 in nz:
        val = T2[i, i2, j, j2]
        for k in range(d):
            key = (mi[tuple(sorted((i, i2, k)))], mi[tuple(sorted((j, j2, k)))])
            c[pairs[key]] += val
    return c


def solve(E, label, eps=1e-7):
    cF = coefF(E)
    K0r = cp.Variable((nK, nK), symmetric=True); K0i = cp.Variable((nK, nK))
    G0r = cp.Variable((nG, nG), symmetric=True); G0i = cp.Variable((nG, nG)); delta = cp.Variable()
    lhs_r = MK @ cp.vec(K0r, order="C") + MG @ cp.vec(G0r, order="C")
    lhs_i = MK @ cp.vec(K0i, order="C") + MG @ cp.vec(G0i, order="C")
    cons = [cp.bmat([[K0r, -K0i], [K0i, K0r]]) >> 0, cp.bmat([[G0r, -G0i], [G0i, G0r]]) >> 0, K0i == -K0i.T, G0i == -G0i.T,
            lhs_r == cF - delta * cN, lhs_i == 0]
    pr = cp.Problem(cp.Maximize(delta), cons); t = time.time()
    pr.solve(solver=cp.SCS, eps=eps, max_iters=100000)
    r = dict(label=label, delta=float(delta.value), status=pr.status, seconds=round(time.time() - t, 1))
    print(r, flush=True); return r


res = dict(sector0_K=nK, sector0_G=nG)
res["control_two_bases"] = solve(bases([0]), "control: two bases only (expect delta <= 0)", eps=1e-6)
res["typeB"] = solve(bases([0, 1, 2, 3]), "type B regulus, 5 bases (1/16 = 0.0625)")
json.dump(res, open(os.path.join(ROOT, "data", "w33_typeB_degree6_sos.json"), "w"), indent=1)
