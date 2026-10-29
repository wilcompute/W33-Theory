"""12404: the finite closure theorem beyond q = 3, by sampling plus a finite Urbantke reconstruction.

Bivectors L = Lambda^2 F^4 (basis 01 02 03 | 23 31 12), wedge pairing P = [[0, I], [I, 0]].  A closure solution kappa (P-symmetric,
kappa^2 = -1) is fixed by U = its i-eigenspace, a 3-space P-orthogonal to the (-i)-eigenspace:
  q = 1 mod 4: i lies in F_q; U is a rational nondegenerate 3-space (sampled uniformly); the (-i)-eigenspace is U^perp.
  q = 3 mod 4: i lies in F_{q^2}; U is a generator of the Hermitian polar space h(x, y) = P(x, sigma y) with P|_U nondegenerate
               (sampled by random isotropic extension); the (-i)-eigenspace is sigma(U).
Metricity: Urbantke's formula M_ij = eps_abc Sigma^a_ik Sigma^b_lm Sigma^c_nj eps^klmn from a basis Sigma^a of U; kappa is metric iff M
is nondegenerate and symmetric and U, Ubar are the two eigenspaces of the unnormalised Hodge map P^{-1} G2(M).
Controls: kappa_g for random metrics g; Urbantke must pass and return g up to scale.  The type (elliptic / hyperbolic) of every
reconstructed metric is recorded."""
import sys, json, random, itertools
import numpy as np

q = int(sys.argv[1])
NS = int(sys.argv[2]) if len(sys.argv) > 2 else 200
ext = (q % 4 == 3)
Q = q * q if ext else q


def enc(a, b=0):
    return (a % q) + q * (b % q)


A = np.zeros((Q, Q), dtype=np.int64)
M = np.zeros((Q, Q), dtype=np.int64)
for x in range(Q):
    for y in range(Q):
        a1, b1 = x % q, x // q
        a2, b2 = y % q, y // q
        A[x, y] = enc(a1 + a2, b1 + b2)
        M[x, y] = enc(a1 * a2 - b1 * b2, a1 * b2 + a2 * b1)
NEG = np.array([enc(-(x % q), -(x // q)) for x in range(Q)])
SIG = np.array([enc(x % q, -(x // q)) for x in range(Q)])
INV = np.zeros(Q, dtype=np.int64)
for x in range(1, Q):
    INV[x] = next(y for y in range(1, Q) if M[x, y] == 1)


def dot(u, v):
    s = 0
    for a, b in zip(u, v):
        s = A[s, M[a, b]]
    return s


def matvec(m, v):
    return np.array([dot(r, v) for r in m])


def matmul(a, b):
    return np.array([[dot(a[i], b[:, j]) for j in range(b.shape[1])] for i in range(a.shape[0])])


def rank_null(m):
    m = m.copy()
    rows, cols = m.shape
    piv, r = [], 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if m[i, c]), None)
        if pr is None:
            continue
        m[[r, pr]] = m[[pr, r]]
        iv = INV[m[r, c]]
        m[r] = [M[iv, x] for x in m[r]]
        for i in range(rows):
            if i != r and m[i, c]:
                f = NEG[m[i, c]]
                m[i] = [A[x, M[f, y]] for x, y in zip(m[i], m[r])]
        piv.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for fc in free:
        v = np.zeros(cols, dtype=np.int64)
        v[fc] = 1
        for i, pc in enumerate(piv):
            v[pc] = NEG[m[i, fc]]
        basis.append(v)
    return r, basis


Pm = np.zeros((6, 6), dtype=np.int64)
for i in range(3):
    Pm[i, 3 + i] = 1
    Pm[3 + i, i] = 1


def Pf(x, y):
    return dot(x, matvec(Pm, y))


pairs = [(0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2)]


def biv_to_mat(v):
    S = np.zeros((4, 4), dtype=np.int64)
    for (a, b), x in zip(pairs, v):
        S[a, b] = x
        S[b, a] = NEG[x]
    return S


def G2(g):
    return np.array([[A[M[g[a, c], g[b, d]], NEG[M[g[a, d], g[b, c]]]] for (c, d) in pairs] for (a, b) in pairs])


EPS = {}
for perm in itertools.permutations(range(4)):
    s = 1
    for i in range(4):
        for j in range(i + 1, 4):
            if perm[i] > perm[j]:
                s = -s
    EPS[perm] = s
EPS3 = {pp: EPS[pp + (3,)] for pp in itertools.permutations(range(3))}


def urbantke(U):
    S = [biv_to_mat(u) for u in U]
    Mt = np.zeros((4, 4), dtype=np.int64)
    for (a, b, c), e1 in EPS3.items():
        for (k, l, m_, n), e2 in EPS.items():
            for i in range(4):
                for j in range(4):
                    t = M[M[S[a][i, k], S[b][l, m_]], S[c][n, j]]
                    if t:
                        Mt[i, j] = A[Mt[i, j], t if e1 * e2 > 0 else NEG[t]]
    return Mt


def eig(Kh, U):
    mus = set()
    for u in U:
        w = matvec(Kh, u)
        idx = next(i for i in range(6) if u[i])
        mu = M[w[idx], INV[u[idx]]]
        if any(w[i] != M[mu, u[i]] for i in range(6)):
            return None
        mus.add(int(mu))
    return mus.pop() if len(mus) == 1 else None


def inverse(m):
    n = m.shape[0]
    aug = np.concatenate([m.copy(), np.eye(n, dtype=np.int64)], axis=1)
    for c in range(n):
        pr = next((i for i in range(c, n) if aug[i, c]), None)
        if pr is None:
            return None
        aug[[c, pr]] = aug[[pr, c]]
        iv = INV[aug[c, c]]
        aug[c] = [M[iv, x] for x in aug[c]]
        for i in range(n):
            if i != c and aug[i, c]:
                f = NEG[aug[i, c]]
                aug[i] = [A[x, M[f, y]] for x, y in zip(aug[i], aug[c])]
    return aug[:, n:]


def is_metric(U, Ub):
    # U consists of BIVECTORS (upper indices): Urbantke then returns the inverse metric density; invert it (a first version did not)
    Mu = urbantke(U)
    if rank_null(Mu.copy())[0] < 4:
        return False, None
    Mt = inverse(Mu)
    if any(Mt[i, j] != Mt[j, i] for i in range(4) for j in range(4)):
        return False, None
    Kh = matmul(Pm, G2(Mt))
    m1, m2 = eig(Kh, U), eig(Kh, Ub)
    return (m1 is not None and m2 is not None and m1 != m2 and m1 == NEG[m2]), Mt


rng = random.Random(12404)


def rvec(base):
    return np.array([rng.randrange(base) for _ in range(6)], dtype=np.int64)


def sample_U():
    while True:
        if not ext:
            U = [rvec(q) for _ in range(3)]
            if rank_null(np.array(U))[0] < 3:
                continue
            if rank_null(np.array([[Pf(a, b) for b in U] for a in U]))[0] < 3:
                continue
            perp = rank_null(np.array([matvec(Pm, u) for u in U]))[1]
            return U, perp
        U, tries = [], 0
        while len(U) < 3 and tries < 20000:
            tries += 1
            x = rvec(Q)
            if not x.any() or Pf(x, SIG[x]) != 0:
                continue
            if any(Pf(u, SIG[x]) != 0 for u in U):
                continue
            if rank_null(np.array(U + [x]))[0] < len(U) + 1:
                continue
            U.append(x)
        if len(U) < 3:
            continue
        if rank_null(np.array([[Pf(a, b) for b in U] for a in U]))[0] < 3:
            continue
        return U, [SIG[u] for u in U]


sq = {(x * x) % q for x in range(1, q)}


def typ_of(R):
    d = int(round(np.linalg.det(R))) % q
    return 'hyperbolic' if d in sq else 'elliptic'


out = dict(q=q, extension=ext)
ctrl = {}
for _ in range(80):
    g = np.zeros((4, 4), dtype=np.int64)
    for i in range(4):
        for j in range(i, 4):
            v = rng.randrange(q)
            g[i, j] = v
            g[j, i] = v
    if int(round(np.linalg.det(g))) % q == 0:
        continue
    t = typ_of(g)
    Kh = matmul(Pm, G2(g))
    lam = matmul(Kh, Kh)[0, 0]
    roots = [x for x in range(Q) if M[x, x] == lam]
    rec = False
    if roots:
        r = roots[0]
        U = rank_null(np.array([[A[Kh[i, j], NEG[r] if i == j else 0] for j in range(6)] for i in range(6)]))[1]
        Ub = rank_null(np.array([[A[Kh[i, j], r if i == j else 0] for j in range(6)] for i in range(6)]))[1]
        if len(U) == 3 and len(Ub) == 3:
            okm, Mt = is_metric(U, Ub)
            if okm:
                nz = next((i, j) for i in range(4) for j in range(4) if g[i, j])
                f = M[Mt[nz], INV[g[nz]]]
                rec = all(Mt[i, j] == M[f, g[i, j]] for i in range(4) for j in range(4))
    # closure needs s^2 * lam = -1 for a scalar s in F_q (i.e. a rational light cone)
    closes = any(M[M[s, s], lam] == NEG[1] for s in range(1, q))
    key = f'{t}, kappa^2 scalar has closure: {closes}'
    c = ctrl.setdefault(key, [0, 0])
    c[0] += 1
    c[1] += int(rec)
out['controls'] = ctrl
ok, types = 0, {}
for n in range(NS):
    U, Ub = sample_U()
    okm, Mt = is_metric(U, Ub)
    if okm:
        ok += 1
        nz = next((i, j) for i in range(4) for j in range(4) if Mt[i, j])
        f = INV[Mt[nz]]
        R = np.array([[M[f, Mt[i, j]] for j in range(4)] for i in range(4)])
        key = typ_of(R) if all(x < q for x in R.flatten()) else 'irrational'
        types[key] = types.get(key, 0) + 1
out.update(sampled=NS, metric=ok, reconstructed_types=types)
print(json.dumps(out))
json.dump(out, open(f'urbantke_q{q}.json', 'w'), indent=1)
