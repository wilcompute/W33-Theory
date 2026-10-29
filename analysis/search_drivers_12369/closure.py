"""12369: finite premetric electrodynamics.  V = F_3^4, bivector space L = Lambda^2 V (dim 6), basis e01 e02 e03 | e23 e31 e12, wedge pairing
P(alpha, beta) = coefficient of e0123 in alpha ^ beta = [[0, I], [I, 0]].  A constitutive map kappa: L -> L that is P-symmetric
(P kappa symmetric) and satisfies the closure relation kappa^2 = -1 is the finite analogue of the Obukhov-Hehl / Gross-Rubilar closure
condition, whose real solutions are exactly (+-) Hodge stars of Lorentzian metrics.
(A) ALL solutions, exactly: kappa = [[a, b], [c, a^T]] with b, c symmetric; the equations are a a + b c = -1, a b + b a^T = 0,
    c a + a^T c = 0, c b + a^T a^T = -1.  For each symmetric b (729) the second is linear in a (nullspace, enumerated); the rest is checked
    for all 729 symmetric c at once.
(B) METRIC solutions: for every nondegenerate symmetric g on V, kappa_g = P^{-1} G2 (G2 = induced Gram matrix on L, 2x2 minors);
    kappa_g^2 is a scalar lambda_g; if lambda_g = -1 then +-kappa_g are closure solutions.  Type of g: hyperbolic (det square) or
    elliptic (det nonsquare).
Compare the two sets."""
import itertools, json, collections
import numpy as np
from sympy import Matrix
from sympy.polys.matrices import DomainMatrix
from sympy.polys.domains import GF
p = 3
I3 = np.eye(3, dtype=np.int64)
P = np.block([[np.zeros((3, 3), dtype=np.int64), I3], [I3, np.zeros((3, 3), dtype=np.int64)]])
def symmats(n):
    idx = [(i, j) for i in range(n) for j in range(i, n)]
    out = []
    for vals in itertools.product(range(p), repeat=len(idx)):
        m = np.zeros((n, n), dtype=np.int64)
        for (i, j), v in zip(idx, vals): m[i, j] = v; m[j, i] = v
        out.append(m)
    return np.array(out)
S3 = symmats(3)                                    # 729 symmetric 3x3
def nullspace_mod3(A):
    dm = DomainMatrix([[GF(p)(int(x)) for x in row] for row in A.tolist()], A.shape, GF(p))
    ns = dm.nullspace().to_Matrix()
    return np.array([[int(x) % p for x in ns.row(r)] for r in range(ns.rows)], dtype=np.int64) if ns.rows else np.zeros((0, A.shape[1]), dtype=np.int64)
sols = set()
for b in S3:
    # linear map a (9 entries, row-major) -> a b + b a^T (9 entries)
    M = np.zeros((9, 9), dtype=np.int64)
    for k in range(9):
        a = np.zeros(9, dtype=np.int64); a[k] = 1; a = a.reshape(3, 3)
        M[:, k] = ((a @ b + b @ a.T) % p).reshape(9)
    N = nullspace_mod3(M)
    for coeffs in itertools.product(range(p), repeat=len(N)):
        a = (np.array(coeffs, dtype=np.int64) @ N % p).reshape(3, 3) if len(N) else np.zeros((3, 3), dtype=np.int64)
        e1 = (a @ a + np.einsum('ij,cjk->cik', b, S3) + I3) % p            # a a + b c + 1
        e3 = (np.einsum('cij,jk->cik', S3, a) + np.einsum('ij,cjk->cik', a.T, S3)) % p
        e4 = (np.einsum('cij,jk->cik', S3, b) + a.T @ a.T + I3) % p
        ok = ~(e1.any(axis=(1, 2)) | e3.any(axis=(1, 2)) | e4.any(axis=(1, 2)))
        for c in S3[ok]:
            k = np.block([[a, b], [c, a.T]]) % p
            sols.add(k.tobytes())
print('all closure solutions:', len(sols))
pairs = [(0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2)]
def G2(g):
    return np.array([[(g[a, c] * g[b, d] - g[a, d] * g[b, c]) % p for (c, d) in pairs] for (a, b) in pairs], dtype=np.int64)
Pinv = P  # P^2 = 1
met = collections.defaultdict(set); lam_hist = collections.Counter(); kap_of = {}
for g in symmats(4):
    det = int(round(np.linalg.det(g))) % p
    if det == 0: continue
    typ = 'hyperbolic' if det == 1 else 'elliptic'
    k0 = Pinv @ G2(g) % p
    sq = k0 @ k0 % p
    lam = sq[0, 0]
    assert (sq == lam * np.eye(6, dtype=np.int64) % p).all(), 'kappa_g^2 not scalar'
    lam_hist[(typ, int(lam))] += 1
    if lam == p - 1:
        for s in (1, p - 1):
            kb = (s * k0 % p).astype(np.int64).tobytes(); met[typ].add(kb); kap_of.setdefault(kb, []).append(g.tobytes())
metric_all = set().union(*met.values())
print('lambda_g histogram (type, kappa_g^2):', dict(lam_hist))
print('metric closure solutions:', {k: len(v) for k, v in met.items()}, 'total', len(metric_all), ' subset of all:', metric_all <= sols)
exotic = sols - metric_all
print('non-metric closure solutions:', len(exotic))
# metrics per metric-kappa (conformal class size)
fib = collections.Counter(len(v) for v in kap_of.values())
out = dict(all_solutions=len(sols), metric_solutions=len(metric_all), metric_by_type={k: len(v) for k, v in met.items()},
           lambda_hist={str(k): v for k, v in lam_hist.items()}, nonmetric=len(exotic), metrics_per_kappa=dict(fib))
json.dump(out, open('closure.json', 'w'), indent=1)
np.save('exotic.npy', np.array([np.frombuffer(x, dtype=np.int64).reshape(6, 6) for x in sorted(exotic)]) if exotic else np.zeros((0, 6, 6)))
np.save('allsols.npy', np.array([np.frombuffer(x, dtype=np.int64).reshape(6, 6) for x in sorted(sols)]))
