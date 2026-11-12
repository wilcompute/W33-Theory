"""Pass 12647 item 3 (step 2): EXACT certificate min F = 1/8 for the three-qubit size-5 sets (Pauli-reduced degree-6 SOS + facial
reduction).  Minimisers: stabiliser states of Lagrangians meeting the covered set C in exactly one point (F = 1/8).  At a minimiser both
SOS terms vanish, so x(v) (degree-3 monomials) lies in ker K and q(v) in ker G; in the reduced form every sector-shift of these vectors
lies in ker K0 / ker G0.  Parametrise K0 = V Z V^H, G0 = W Y W^H with exact Gaussian-integer bases V, W of the orthogonal complements,
solve the SDP (delta = 1/8 fixed) maximising the smallest eigenvalue, round Z, Y to Gaussian rationals, restore the linear equations
exactly (pivot variables from an exact rref of an independent row subset), verify ALL coefficient equations in exact integer arithmetic
and check Z, Y PSD by exact rational LDL^T.  Success => F(v)|v|^2 - |v|^6/8 is an exact SOS => min F = 1/8 for all 24,192 sets.
usage: py -3 analysis/w33_threequbit_exact_one_eighth.py"""
import itertools, json, os, contextlib, io, time
from fractions import Fraction as Fr
import numpy as np, cvxpy as cp, sympy as sp
import scipy.sparse as sps
from sympy.polys.matrices import DomainMatrix
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
red = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_pauli_reduced_sos.py")}
src = open(os.path.join(HERE, "w33_threequbit_pauli_reduced_sos.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("# linear maps:")], red)
g = red
d, mons, mi, nm, qs, s0K, s0G, shiftK, shiftG, cF64, cN, pts, lag, B, S = (g[k] for k in "d mons mi nm qs s0K s0G shiftK shiftG cF64 cN pts lag B S".split())
C = frozenset().union(*[lag[L] for L in S])
# minimisers: stabiliser states (Gaussian-integer form) of Lagrangians meeting C once
mins = []
for L in range(len(lag)):
    if L in S or len(set(lag[L]) & C) != 1: continue
    for e in B[L].T:
        k = np.flatnonzero(np.abs(e) > 1e-9); s = len(k)
        u = e * np.sqrt(s); u = u / (u[k[0]] / abs(u[k[0]]))
        R = np.round(u.real) + 1j * np.round(u.imag); assert np.abs(u - R).max() < 1e-9
        mins.append(R)
print("minimiser states:", len(mins), flush=True)
def xvec(v): return np.array([np.prod([v[i] for i in m]) for m in mons])
def qvec(v): return np.array([v[i] * v[j] * np.conj(v[k]) for (i, j), k in qs])
qi = {q: n for n, q in enumerate(qs)}
kerK, kerG = [], []
for v in mins:
    x = xvec(v); q = qvec(v)
    for a in range(d):
        kerK.append([x[mi[shiftK(m, a)]] for m in s0K]); kerG.append([q[qi[shiftG(t, a)]] for t in s0G])
def exact_complement(vectors, n):
    """basis (Gaussian integers) of {z : <w, z> = 0 for all w} = nullspace of conj(W)."""
    K = sp.QQ.algebraic_field(sp.I)
    rows = [[K.from_sympy(sp.Integer(int(round(c.real))) - sp.I * sp.Integer(int(round(c.imag)))) for c in w] for w in vectors]
    M = DomainMatrix(rows, (len(rows), n), K)
    ns = M.nullspace().to_Matrix()  # rows are basis vectors
    basis = []
    for r in range(ns.shape[0]):
        vec = [sp.nsimplify(ns[r, c]) for c in range(n)]
        den = sp.ilcm(*[sp.fraction(sp.together(sp.re(z)))[1] for z in vec] + [sp.fraction(sp.together(sp.im(z)))[1] for z in vec])
        basis.append(np.array([complex(sp.re(z) * den) + 1j * complex(sp.im(z) * den) for z in vec]))
    return np.array(basis).T if basis else np.zeros((n, 0), complex)  # n x r
V = exact_complement(kerK, 15); W = exact_complement(kerG, 36)
rK, rG = V.shape[1], W.shape[1]
print("complement dims: K0", rK, "of 15 | G0", rG, "of 36", flush=True)
# Hermitian parametrisation: Z = sum z_t H_t
def herm_basis(r):
    out = []
    for p in range(r):
        M = np.zeros((r, r), complex); M[p, p] = 1; out.append(M)
    for p, q in itertools.combinations(range(r), 2):
        M = np.zeros((r, r), complex); M[p, q] = M[q, p] = 1; out.append(M)
        M = np.zeros((r, r), complex); M[p, q] = 1j; M[q, p] = -1j; out.append(M)
    return out
HK, HG = herm_basis(rK), herm_basis(rG)
def coef_K(K0):
    c = np.zeros((nm, nm), complex)
    for a in range(d):
        idx = [mi[shiftK(m, a)] for m in s0K]
        c[np.ix_(idx, idx)] += K0
    return c
def coef_G(G0):
    c = np.zeros((nm, nm), complex)
    for a in range(d):
        sh = [shiftG(t, a) for t in s0G]
        for x, ((i, j), k) in enumerate(sh):
            for y, ((l, m_), n_) in enumerate(sh):
                c[mi[tuple(sorted((i, j, n_)))], mi[tuple(sorted((k, l, m_)))]] += G0[x, y]
    return c
cols = [coef_K(V @ H @ V.conj().T).reshape(-1) for H in HK] + [coef_G(W @ H @ W.conj().T).reshape(-1) for H in HG]
A = np.array(cols).T  # complex (nm*nm) x nvar ; integer-valued (Gaussian integers)
assert np.abs(A - np.round(A.real) - 1j * np.round(A.imag)).max() < 1e-9
b = cF64 - 8 * cN  # 64 * (cF - cN/8)
Ar = np.vstack([A.real, A.imag]); br = np.concatenate([b.real.reshape(-1), b.imag.reshape(-1)])
keep = np.flatnonzero((np.abs(Ar).sum(1) > 0) | (np.abs(br) > 0))
Ar, br = np.round(Ar[keep]).astype(np.int64), np.round(br[keep]).astype(np.int64)
assert np.all(np.abs(Ar).sum(1) > 0), "an equation has no variables but nonzero rhs"
nvar = Ar.shape[1]
print("equations", Ar.shape[0], "variables", nvar, flush=True)
# numerical SDP: 64 * (K + L) coefficient equations, maximise t with Z >= tI, Y >= tI
z = cp.Variable(nvar); t = cp.Variable()
ZK = sum((z[k] * HK[k].real for k in range(len(HK))), np.zeros((rK, rK))); ZKi = sum((z[k] * HK[k].imag for k in range(len(HK))), np.zeros((rK, rK)))
ZG = sum(z[len(HK) + k] * HG[k].real for k in range(len(HG))); ZGi = sum(z[len(HK) + k] * HG[k].imag for k in range(len(HG)))
cons = [Ar.astype(float) @ z == br.astype(float), cp.bmat([[ZG, -ZGi], [ZGi, ZG]]) >> t * np.eye(2 * rG)]
if rK > 0: cons.append(cp.bmat([[ZK, -ZKi], [ZKi, ZK]]) >> t * np.eye(2 * rK))
# note: the equations above are 64*(coefK + coefG) = cF64 - 8 cN, so scale z by 1/64 implicitly: we solve A z = b (z absorbs the 64)
pr = cp.Problem(cp.Maximize(t), cons); pr.solve(solver=cp.SCS, eps=1e-10, max_iters=500000)
print("interior margin t =", t.value, pr.status, flush=True)
zs = z.value
# exact: select independent rows numerically, rref exactly, round free variables, solve pivots
Q, Rq, Pv = __import__("scipy.linalg", fromlist=["qr"]).qr(Ar.T.astype(float), pivoting=True, mode="economic")
rank = int(np.sum(np.abs(np.diag(Rq)) > 1e-8 * abs(Rq[0, 0])))
rows_sel = Pv[:rank]
Dm = DomainMatrix([[sp.QQ(int(x)) for x in Ar[r]] + [sp.QQ(int(br[r]))] for r in rows_sel], (rank, nvar + 1), sp.QQ)
Rr, piv = Dm.rref(); Rl = Rr.to_list(); piv = [p for p in piv if p < nvar]; pivset = set(piv)
print("rank", rank, "pivots", len(piv), flush=True)
def lde(M):
    M = [row[:] for row in M]; m = len(M)
    for i in range(m):
        if M[i][i] < 0: return False
        if M[i][i] == 0:
            if any(M[i][j] != 0 for j in range(i + 1, m)): return False
            continue
        for j in range(i + 1, m):
            if M[j][i] != 0:
                f = M[j][i] / M[i][i]
                for k in range(i, m): M[j][k] -= f * M[i][k]
    return True
res = dict(n_minimisers=len(mins), complement_K=rK, complement_G=rG, n_equations=int(Ar.shape[0]), n_variables=nvar, rank=rank, margin=float(t.value), attempts=[])
for D in (1, 2, 4, 8, 16, 32, 64, 128, 256, 1024, 4096):
    zr = [Fr(round(v * D), D) for v in zs]
    for ri, p in enumerate(piv):
        row = Rl[ri]; val = Fr(str(row[-1]))
        for c in range(nvar):
            if c != p and c not in pivset and row[c] != 0: val -= Fr(str(row[c])) * zr[c]
        zr[p] = val
    den = 1
    for q_ in zr: den = den * q_.denominator // np.gcd(den, q_.denominator)
    zi = [int(q_ * den) for q_ in zr]
    eq_ok = all(sum(int(Ar[r, c]) * zi[c] for c in np.flatnonzero(Ar[r])) == int(br[r]) * den for r in range(Ar.shape[0]))
    def realified(Hb, off, r):
        Zr = [[Fr(0)] * (2 * r) for _ in range(2 * r)]
        for k, H in enumerate(Hb):
            for p in range(r):
                for q in range(r):
                    if H[p, q] != 0:
                        re, im = int(round(H[p, q].real)), int(round(H[p, q].imag))
                        Zr[p][q] += re * zr[off + k]; Zr[p + r][q + r] += re * zr[off + k]
                        Zr[p + r][q] += im * zr[off + k]; Zr[p][q + r] -= im * zr[off + k]
        return Zr
    psdK = eq_ok and (rK == 0 or lde(realified(HK, 0, rK))); psdG = psdK and lde(realified(HG, len(HK), rG))
    res["attempts"].append(dict(D=D, equations_exact=eq_ok, psd_K=psdK, psd_G=psdG)); print("D", D, "eq", eq_ok, "K", psdK, "G", psdG, flush=True)
    if eq_ok and psdK and psdG:
        res.update(certified=True, denominator=D, conclusion="exact SOS: F|v|^2 - |v|^6/8 = sum of squares => min F = 1/8 exactly (all 24,192 sets, one orbit)")
        break
else:
    res["certified"] = False
json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_exact_one_eighth.json"), "w"), indent=1)
print({k: v for k, v in res.items() if k != "attempts"}, flush=True)
