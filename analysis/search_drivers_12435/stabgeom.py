"""12435-12436: stabilizer-state geometry.  n qutrits: stabilizer states = joint eigenvectors of the Weyl operators of a Lagrangian
(maximal isotropic) L in F_3^{2n} -- 360 states / 40 Lagrangians at n = 2 (the 40 lines of W(3,3)), 30240 / 1120 at n = 3.  Dual polar
graph: L ~ L' iff dim(L cap L') = n - 1; distance d(L, L') = n - dim(L cap L'), diameter n.
Checks:  (1) |<psi|phi>|^2 in {0} u {3^-d} with d = n - dim(L cap L') for every nonzero overlap (n = 2: all pairs; n = 3: one reference
state against all 30240);  (2) sphere sizes of the dual polar graph = q^{r(r+1)/2} [n choose r]_q (q = 3): the 'light cone' grows with n.
Reading [I]: graph distance = -log_q fidelity -- a metric made of information, with a light cone of radius n (one Clifford step moves a
Lagrangian by at most 1)."""
import itertools, json, collections
import numpy as np

q = 3
w = np.exp(2j * np.pi / q)
X = np.roll(np.eye(q), 1, axis=0); Z = np.diag([w ** j for j in range(q)])


def weyl(v, n):
    a, b = v[:n], v[n:]
    M = np.array([[1.0]])
    for i in range(n):
        M = np.kron(M, np.linalg.matrix_power(X, int(a[i])) @ np.linalg.matrix_power(Z, int(b[i])))
    return M


def symp(u, v, n):
    return int(np.dot(u[:n], v[n:]) - np.dot(u[n:], v[:n])) % q


def rref(B):
    B = [list(map(int, r)) for r in B]; m = len(B); ncol = len(B[0]); r = 0; out = []
    B = np.array(B) % q
    for c in range(ncol):
        piv = next((i for i in range(r, m) if B[i, c]), None)
        if piv is None: continue
        B[[r, piv]] = B[[piv, r]]; B[r] = (B[r] * pow(int(B[r, c]), q - 2, q)) % q
        for i in range(m):
            if i != r and B[i, c]: B[i] = (B[i] - B[i, c] * B[r]) % q
        r += 1
        if r == m: break
    return tuple(map(tuple, B[:r]))


def span(B):
    B = np.array(B)
    return {tuple((np.array(c) @ B) % q) for c in itertools.product(range(q), repeat=len(B))}


def lagrangians(n):
    # BFS orbit of the standard Lagrangian <e_1..e_n> under symplectic transvections
    std = rref(np.eye(2 * n, dtype=int)[:n])
    vecs = [np.array(v) for v in itertools.product(range(q), repeat=2 * n) if any(v)]
    gens = [v for v in vecs if np.count_nonzero(v) <= 2]      # transvections by weight <= 2 vectors generate Sp(2n, 3)
    def tv(v, u):
        return (u + symp(u, v, n) * v) % q
    seen = {std}; fr = [std]
    while fr:
        nf = []
        for L in fr:
            for g in gens:
                M = rref([tv(g, np.array(r)) for r in L])
                if M not in seen: seen.add(M); nf.append(M)
        fr = nf
    return sorted(seen)


def states(L, n, rng):
    Ws = [weyl(np.array(r), n) for r in L]
    H = sum(rng.normal() * (Wm + Wm.conj().T) + 1j * rng.normal() * (Wm - Wm.conj().T) for Wm in Ws)
    _, V = np.linalg.eig(H)
    V = V / np.linalg.norm(V, axis=0)
    # verify joint eigenvectors
    for Wm in Ws:
        R = Wm @ V
        lam = np.sum(V.conj() * R, axis=0)
        assert np.allclose(R, V * lam, atol=1e-8)
    return V


out = {}
rng = np.random.default_rng(12435)
for n in (2, 3):
    Ls = lagrangians(n)
    Lsets = [span(L) for L in Ls]
    expected = {2: 40, 3: 1120}[n]
    rec = dict(lagrangians=len(Ls), expected=expected)
    S = [states(L, n, rng) for L in Ls]
    # distance distribution from Lagrangian 0 and sphere sizes
    def dist(i, j):
        inter = len(Lsets[i] & Lsets[j])
        return n - int(round(np.log(inter) / np.log(q)))
    sph = collections.Counter(dist(0, j) for j in range(len(Ls)))
    def gauss(n_, r):
        num = den = 1
        for i in range(r):
            num *= q ** (n_ - i) - 1; den *= q ** (i + 1) - 1
        return num // den
    rec['spheres'] = {str(k): v for k, v in sorted(sph.items())}
    rec['spheres_formula'] = {str(r): q ** (r * (r + 1) // 2) * gauss(n, r) for r in range(n + 1)}
    # overlaps
    bad = 0; tab = collections.Counter()
    refs = range(len(Ls)) if n == 2 else [0]
    for i in refs:
        for j in range(len(Ls)):
            O = np.abs(S[i].conj().T @ S[j]) ** 2
            d = dist(i, j)
            for val in O.flatten():
                if val < 1e-9:
                    tab[(d, 'zero')] += 1
                elif abs(val - q ** (-d)) < 1e-8:
                    tab[(d, f'3^-{d}')] += 1
                else:
                    bad += 1
    rec['overlap_table'] = {f'{a}|{b}': c for (a, b), c in sorted(tab.items())}
    rec['overlaps_violating_3^-d'] = bad
    out[n] = rec
    print(n, rec, flush=True)
json.dump(out, open('stabgeom.json', 'w'), indent=1)
