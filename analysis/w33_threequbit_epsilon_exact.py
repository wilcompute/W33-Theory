"""Pass 12647 item 3 (step 5): exact three-qubit bound F >= (1/8 - eps)|v|^4 from a strictly interior Pauli-reduced degree-6 SOS.
At delta = 1/8 the facially reduced SDP has zero margin and the second facial-reduction dual returns a full-rank Omega (both solver
statuses 'inaccurate'), consistent with the degree-6 bound 1/8 being approached but not attained.  So certify delta = 1/8 - eps:
solve for K0 (15x15), G0 (36x36) Hermitian maximising the smallest eigenvalue t, round to Gaussian rationals (denominator D), restore the
coefficient equations exactly (pivot variables from an exact rref of an independent row subset), verify every equation in exact integer
arithmetic and check K0, G0 PSD by exact rational LDL^T.  Stabiliser states attain F = 1/8, so min F lies in [1/8 - eps, 1/8] exactly.
usage: py -3 analysis/w33_threequbit_epsilon_exact.py"""
import itertools, json, os, contextlib, io, time
from fractions import Fraction as Fr
import numpy as np, cvxpy as cp, sympy as sp
from sympy.polys.matrices import DomainMatrix
import scipy.linalg as sla
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
red = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_pauli_reduced_sos.py")}
src = open(os.path.join(HERE, "w33_threequbit_pauli_reduced_sos.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("# linear maps:")], red)
d, mons, mi, nm, qs, s0K, s0G, shiftK, shiftG, cF64, cN = (red[k] for k in "d mons mi nm qs s0K s0G shiftK shiftG cF64 cN".split())
def herm_basis(r):
    out = []
    for p in range(r):
        M = np.zeros((r, r), complex); M[p, p] = 1; out.append(M)
    for p, q in itertools.combinations(range(r), 2):
        M = np.zeros((r, r), complex); M[p, q] = M[q, p] = 1; out.append(M)
        M = np.zeros((r, r), complex); M[p, q] = 1j; M[q, p] = -1j; out.append(M)
    return out
HK, HG = herm_basis(15), herm_basis(36)
def coef_K(K0):
    c = np.zeros((nm, nm), complex)
    for a in range(d):
        idx = [mi[shiftK(m, a)] for m in s0K]; c[np.ix_(idx, idx)] += K0
    return c
def coef_G(G0):
    c = np.zeros((nm, nm), complex)
    for a in range(d):
        sh = [shiftG(t, a) for t in s0G]
        for x, ((i, j), k) in enumerate(sh):
            for y, ((l, m_), n_) in enumerate(sh):
                c[mi[tuple(sorted((i, j, n_)))], mi[tuple(sorted((k, l, m_)))]] += G0[x, y]
    return c
A = np.array([coef_K(H).reshape(-1) for H in HK] + [coef_G(H).reshape(-1) for H in HG]).T
Ar = np.vstack([A.real, A.imag]); nvar = Ar.shape[1]
res = dict(n_variables=nvar, runs=[])
for eps in (Fr(1, 1000), Fr(1, 10000), Fr(1, 100000), Fr(1, 1000000)):
    delta = Fr(1, 8) - eps
    # equations: coefK + coefG = cF - delta cN ; multiply by 64 * den(eps) to make integral
    S_ = 64 * delta.denominator
    b = cF64 * (S_ // 64) - (delta.numerator * (S_ // delta.denominator)) * cN
    br = np.concatenate([b.real.reshape(-1), b.imag.reshape(-1)])
    keep = np.flatnonzero((np.abs(Ar).sum(1) > 0) | (np.abs(br) > 0))
    Ak, bk = np.round(Ar[keep]).astype(np.int64), np.round(br[keep]).astype(np.int64)
    assert np.all(np.abs(Ak).sum(1) > 0)
    z = cp.Variable(nvar); t = cp.Variable()
    ZK = sum(z[k] * HK[k].real for k in range(len(HK))); ZKi = sum(z[k] * HK[k].imag for k in range(len(HK)))
    ZG = sum(z[len(HK) + k] * HG[k].real for k in range(len(HG))); ZGi = sum(z[len(HK) + k] * HG[k].imag for k in range(len(HG)))
    scale = S_ // 64
    cons = [Ak.astype(float) @ z == bk.astype(float) / scale, cp.bmat([[ZK, -ZKi], [ZKi, ZK]]) >> t * np.eye(30), cp.bmat([[ZG, -ZGi], [ZG * 0 + ZGi, ZG]]) >> t * np.eye(72), t <= 1]
    pr = cp.Problem(cp.Maximize(t), cons); tt = time.time(); pr.solve(solver=cp.SCS, eps=1e-10, max_iters=500000)
    if z.value is None:
        res['runs'].append(dict(eps=str(eps), status=pr.status)); print('eps', eps, pr.status, flush=True); break
    zs = z.value * scale; print("eps", eps, "margin", t.value, pr.status, "%.0fs" % (time.time() - tt), flush=True)
    Q, Rq, Pv = sla.qr(Ak.T.astype(float), pivoting=True, mode="economic")
    rank = int(np.sum(np.abs(np.diag(Rq)) > 1e-8 * abs(Rq[0, 0]))); rows_sel = Pv[:rank]
    Dm = DomainMatrix([[sp.QQ(int(x)) for x in Ak[r]] + [sp.QQ(int(bk[r]))] for r in rows_sel], (rank, nvar + 1), sp.QQ)
    Rr, piv = Dm.rref(); Rl = Rr.to_list(); piv = [p for p in piv if p < nvar]; pivset = set(piv)
    def lde(M):
        M = [row[:] for row in M]; m = len(M)
        for i in range(m):
            if M[i][i] <= 0:
                if M[i][i] < 0 or any(M[i][j] != 0 for j in range(i + 1, m)): return False
                continue
            for j in range(i + 1, m):
                if M[j][i] != 0:
                    f = M[j][i] / M[i][i]
                    for k in range(i, m): M[j][k] -= f * M[i][k]
        return True
    def realified(Hb, off, r, zr):
        Zr = [[Fr(0)] * (2 * r) for _ in range(2 * r)]
        for k, H in enumerate(Hb):
            for p, q in zip(*np.nonzero(H)):
                re, im = int(round(H[p, q].real)), int(round(H[p, q].imag)); val = zr[off + k]
                Zr[p][q] += re * val; Zr[p + r][q + r] += re * val; Zr[p + r][q] += im * val; Zr[p][q + r] -= im * val
        return Zr
    run = dict(eps=str(eps), margin=float(t.value), rank=rank, attempts=[])
    for D in (16, 64, 256, 1024, 4096, 16384, 65536):
        zr = [Fr(round(v * D), D) for v in zs]
        for ri, p in enumerate(piv):
            row = Rl[ri]; val = Fr(str(row[-1]))
            for c in range(nvar):
                if c != p and c not in pivset and row[c] != 0: val -= Fr(str(row[c])) * zr[c]
            zr[p] = val
        den = 1
        for q_ in zr: den = den * q_.denominator // int(np.gcd(den, q_.denominator))
        zi = [int(q_ * den) for q_ in zr]
        eq_ok = all(sum(int(Ak[r, c]) * zi[c] for c in np.flatnonzero(Ak[r])) == int(bk[r]) * den for r in range(Ak.shape[0]))
        okK = eq_ok and lde(realified(HK, 0, 15, zr)); okG = okK and lde(realified(HG, len(HK), 36, zr))
        run["attempts"].append(dict(D=D, equations_exact=eq_ok, psd_K=okK, psd_G=okG)); print("  D", D, eq_ok, okK, okG, flush=True)
        if okG:
            run.update(certified=True, denominator=D, conclusion="exact: F(v) >= (1/8 - %s)|v|^4 for every v in C^8, every size-5 three-qubit set (one orbit); min F in [1/8 - %s, 1/8]" % (eps, eps))
            break
    else:
        run["certified"] = False
    res["runs"].append(run)
    json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_epsilon_exact.json"), "w"), indent=1)
    if not run.get("certified"): break
print(json.dumps(res, indent=1)[:1500], flush=True)
