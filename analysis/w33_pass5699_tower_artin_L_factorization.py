#!/usr/bin/env python3
"""Pass5699: Artin factorization for a separate deterministic W33 2-lift tower.

This producer does *not* replay the frozen Pass5683/5693 tower.  It starts from
the same W(3,3) Levi graph, deterministically factors the edges into four perfect
matchings at every level (including the 80-vertex parent), selects the best of
the six two-matching signings, and constructs a separate tower through 640
vertices.  No isomorphism with the Pass5683/5693 tower is claimed.

For each 2-lift, the exact block decomposition theorem gives
spec(A_child) = spec(A_parent) union spec(A_signed).  Floating eigenvalues only
replay that exact identity numerically.  The Bass determinant formula then gives

    zeta_child(u)^{-1} = zeta_parent(u)^{-1} * L(u, chi)^{-1},
    L(u, chi)^{-1}     = (1-u^2)^{r-1} det(I - u A_signed + 3 u^2 I),

the standard Stark--Terras Artin factor of the Z/2 edge local system defined by
the signing.  This graph-edge local system is not identified with Pass5696's
AGL(2,3) determinant character; the two data live on different objects.

Pole analysis: through the three constructed lifts all determinant roots lie on
|u| = 1/sqrt(3) except the four trivial roots +/-1 and +/-1/3 inherited from the
eigenvalues +/-4; the signed spectra contribute roots on the circle.
The functional equation Delta(u) = (3 u^2)^n Delta(1/(3u)) follows exactly,
factor by factor, from
(3u^2)(1-lambda/(3u)+1/(3u^2)) = 1-lambda*u+3u^2.

Base closed form discovered and verified:
    Delta_levi(u) = (1-u^2)(1-9u^2)(1+9u^4)^24 (1+3u^2)^30 .
"""
from __future__ import annotations
import itertools, collections, json, math
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/PART_W33_PASS5699_TOWER_ARTIN_L_FACTORIZATION.json'
RAM = 2*math.sqrt(3)

vecs = [v for v in itertools.product(range(3), repeat=4) if v != (0,0,0,0)]
def canon(v):
    for x in v:
        if x: return tuple((xi*(1 if x==1 else 2)) % 3 for xi in v)
pts = sorted(set(canon(v) for v in vecs)); assert len(pts) == 40
P = {p: i for i, p in enumerate(pts)}
def omega(u, v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1]) % 3
lines = set()
for i, j in itertools.combinations(range(40), 2):
    if omega(pts[i], pts[j]) == 0:
        u, v = pts[i], pts[j]; mem = {i, j}
        for a in (1, 2):
            mem.add(P[canon(tuple((u[k]+a*v[k]) % 3 for k in range(4)))])
        lines.add(frozenset(mem))
lines = sorted(lines, key=lambda L: sorted(L))
assert len(lines) == 40 and all(len(L) == 4 for L in lines)
E0 = sorted((p, 40+l) for l, L in enumerate(lines) for p in sorted(L))
assert len(E0) == 160

def unsigned_adj(E, n):
    A = np.zeros((n, n))
    for u, v in E: A[u, v] = A[v, u] = 1.0
    return A
def signed_adj(E, n, neg):
    neg = set(neg); A = np.zeros((n, n))
    for i, (u, v) in enumerate(E):
        s = -1.0 if i in neg else 1.0; A[u, v] = A[v, u] = s
    return A
def bipartition(E, n):
    adj = [[] for _ in range(n)]
    for u, v in E: adj[u].append(v); adj[v].append(u)
    col = [None]*n
    for s in range(n):
        if col[s] is not None: continue
        col[s] = 0; q = collections.deque([s])
        while q:
            u = q.popleft()
            for v in sorted(adj[u]):
                if col[v] is None: col[v] = 1-col[u]; q.append(v)
                else: assert col[v] != col[u]
    X = sorted(i for i, c in enumerate(col) if c == 0)
    Y = {i for i, c in enumerate(col) if c == 1}
    assert len(X) == len(Y) == n//2
    return X, Y
def perfect_matching(E, n):
    X, Y = bipartition(E, n); adjl = {u: [] for u in X}
    for a, b in E:
        u, v = (b, a) if a in Y else (a, b); adjl[u].append(v)
    for u in X: adjl[u] = sorted(set(adjl[u]))
    mt = {}
    def dfs(u, seen):
        for v in adjl[u]:
            if v in seen: continue
            seen.add(v)
            if v not in mt or dfs(mt[v], seen): mt[v] = u; return True
        return False
    for u in X: assert dfs(u, set())
    return {tuple(sorted((u, v))) for v, u in mt.items()}
def factor4(E, n):
    rem = set(E); M = []
    for _ in range(4):
        m = perfect_matching(sorted(rem), n); M.append(m); rem -= m
    assert not rem
    return M
def lift_edges(E, n, neg_idx):
    neg = set(neg_idx); out = []
    for ei, (u, v) in enumerate(E):
        flip = 1 if ei in neg else 0
        for sh in (0, 1):
            a = u+sh*n; b = v+(sh ^ flip)*n
            if a > b: a, b = b, a
            out.append((a, b))
    return sorted(out)
def components(E, n):
    adj = [[] for _ in range(n)]
    for u, v in E: adj[u].append(v); adj[v].append(u)
    seen = set(); sizes = []
    for s in range(n):
        if s in seen: continue
        st = [s]; seen.add(s); m = 0
        while st:
            u = st.pop(); m += 1
            for v in adj[u]:
                if v not in seen: seen.add(v); st.append(v)
        sizes.append(m)
    return sorted(sizes, reverse=True)

def bass_det(A, u):
    n = A.shape[0]
    return float(np.linalg.det(np.eye(n)-u*A+3*u*u*np.eye(n)))
def pole_moduli(ev):
    out = []
    for lam in ev:
        d = lam*lam-12
        if d >= 0:
            out += [abs((lam+math.sqrt(d))/6), abs((lam-math.sqrt(d))/6)]
        else:
            out += [1/math.sqrt(3)]*2
    return out

def main():
    tower = [(E0, 80, None, None)]
    E, n = E0, 80
    for lvl in (1, 2, 3):
        mats = factor4(E, n); ei = {e: i for i, e in enumerate(E)}
        rows = []
        for a, b in itertools.combinations(range(4), 2):
            neg = {ei[e] for e in mats[a] | mats[b]}
            rho = float(np.max(np.abs(np.linalg.eigvalsh(signed_adj(E, n, neg)))))
            rows.append((rho, a, b, neg))
        rows.sort(key=lambda x: (x[0], x[1], x[2]))
        rho, a, b, neg = rows[0]; assert rho < RAM
        E = lift_edges(E, n, neg); n = 2*n
        assert components(E, n) == [n]
        tower.append((E, n, neg, rho))

    split_checks = []
    for li in (1, 2, 3):
        neg = tower[li][2]; Ep, np_ = tower[li-1][0], tower[li-1][1]
        both = np.sort(np.concatenate([np.linalg.eigvalsh(unsigned_adj(Ep, np_)),
                                       np.linalg.eigvalsh(signed_adj(Ep, np_, neg))]))
        err = float(np.max(np.abs(both - np.linalg.eigvalsh(unsigned_adj(tower[li][0], np_*2)))))
        split_checks.append(err < 1e-10)
    assert all(split_checks)

    def closed_levi(u):
        return (1-u*u)*(1-9*u*u)*(1+9*u**4)**24*(1+3*u*u)**30
    base = unsigned_adj(E0, 80)
    closed_ok = all(abs(bass_det(base, u)/closed_levi(u)-1) < 1e-9
                    for u in (0.01, 0.013, 0.0077, 0.02))

    pole_rows = []
    for li, (E, n, neg, rho) in enumerate(tower):
        rr = pole_moduli(np.linalg.eigvalsh(unsigned_adj(E, n)))
        off = sorted(set(round(m, 6) for m in rr if abs(m-1/math.sqrt(3)) >= 1e-9))
        pole_rows.append({'level': li, 'vertices': n, 'n_poles': len(rr),
                          'on_critical_circle': sum(1 for m in rr if abs(m-1/math.sqrt(3)) < 1e-9),
                          'off_circle_moduli': off})
        assert off == [0.333333, 1.0]
    signed_rows = []
    for li in (1, 2, 3):
        neg = tower[li][2]; Ep, np_ = tower[li-1][0], tower[li-1][1]
        rr = pole_moduli(np.linalg.eigvalsh(signed_adj(Ep, np_, neg)))
        off = [m for m in rr if abs(m-1/math.sqrt(3)) >= 1e-9]
        signed_rows.append({'level': li, 'parent': np_, 'n_Lpoles': len(rr), 'off_circle': len(off)})
        assert not off

    out = {
      'pass': 5699,
      'status': 'SEPARATE_DETERMINISTIC_FACTOR_PAIR_TOWER_ARTIN_FACTORIZATION_THROUGH_640',
      'tower_provenance': ('Separate deterministic factor-pair tower: the base edge list is globally sorted and the '
                           'best two-matching signing is selected already at parent size 80. This is not the frozen '
                           'Pass5683/5693 tower, and no isomorphism between the towers has been computed.'),
      'factorization': 'zeta_child^-1 = zeta_parent^-1 * L(u,chi)^-1 with L(u,chi)^-1 = (1-u^2)^(r-1) det(I - u A_signed + 3u^2 I)',
      'spectrum_split_exact_by_2lift_block_conjugation': True,
      'numeric_spectrum_split_error_below_1e_10_each_level': split_checks,
      'base_closed_form': 'Delta_levi(u) = (1-u^2)(1-9u^2)(1+9u^4)^24 (1+3u^2)^30',
      'base_closed_form_verified': closed_ok,
      'unsigned_poles': pole_rows,
      'signed_L_function_poles': signed_rows,
      'functional_equation_exact_factor_identity': '(3u^2)(1-lambda/(3u)+1/(3u^2)) = 1-lambda*u+3u^2',
      'stark_terras_reference': 'Factorization of zeta functions of coverings into Artin L-functions (Stark--Terras); here the Z/2 covering is the balanced 2-lift.',
      'prior_corpus_owners': ('BT545 and Pass75 already own the Levi spectrum, girth-eight cycle count, and Ihara-prime '
                              'surface; this pass only applies the standard covering factorization to this separate finite tower.'),
      'non_identification': ('The graph-edge Z/2 signing is not Pass5696\'s AGL(2,3) determinant character. No map between '
                             'those local systems or partition-function interpretation is constructed.'),
      'physics_boundary': ('Finite-graph determinant identities through 640 vertices only; no all-level recursion, continuum '
                           'zeta regularization, partition function, or physical energy spectrum is claimed.')
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(out, indent=2, sort_keys=True))
if __name__ == '__main__': main()
