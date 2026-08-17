#!/usr/bin/env python3
"""Pass5701: exact positivity certificates for the separate factor-pair tower.

This is the deterministic tower constructed independently in Pass5699, not the
frozen Pass5683/5693 tower.  The base edge list is globally sorted and the first
two-matching signing is selected already on the 80-vertex parent.  No
isomorphism between the two towers has been computed.

For each balanced signing used to form the next 2-lift, the signed adjacency A_s
is a symmetric integer matrix and the Ramanujan condition rho(A_s) < 2 sqrt(3)
is equivalent to

    B = 12 I - A_s^2   positive definite.

We certify B > 0 by exact rational LDL decomposition (all pivots strictly
positive as exact Fraction objects).  Floating eigensolvers choose among the six
deterministic matching-pair candidates; the positivity proof for each selected
integer matrix is exact.

Results (local levels in this separate tower):
  level 1 (parent n=80 ): B positive definite, min pivot ~= 4.817
  level 2 (parent n=160): B positive definite, min pivot ~= 4.489
  level 3 (parent n=320): B positive definite, min pivot ~= 4.522

Corollary: the signed-spectrum RH (all L-function poles on |u| = 1/sqrt(3)) is
an exact theorem for these three selected signings.  No 640-parent signing or
1280-vertex child is constructed here.
"""
from __future__ import annotations
import itertools, collections, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/PART_W33_PASS5701_EXACT_PSD_RAMANUJAN_CERTIFICATES.json'
RAM = 2*math.sqrt(3)

vecs = [v for v in itertools.product(range(3), repeat=4) if v != (0,0,0,0)]
def canon(v):
    for x in v:
        if x: return tuple((xi*(1 if x==1 else 2)) % 3 for xi in v)
pts = sorted(set(canon(v) for v in vecs))
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
E0 = sorted((p, 40+l) for l, L in enumerate(lines) for p in sorted(L))

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
    return sorted(i for i, c in enumerate(col) if c == 0), {i for i, c in enumerate(col) if c == 1}
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

def exact_ldl_psd(Bint):
    n = Bint.shape[0]
    A = [[Fraction(int(Bint[i, j])) for j in range(n)] for i in range(n)]
    ds = []
    for k in range(n):
        d = A[k][k]
        if d <= 0: return False, k, ds
        ds.append(d)
        inv = 1/d
        col = [A[i][k] for i in range(k+1, n)]
        for i in range(k+1, n):
            ci = col[i-k-1]
            if ci == 0: continue
            for j in range(k+1, n):
                A[i][j] -= ci*col[j-k-1]*inv
    return True, n, ds

def int_mat(E, n, neg=None):
    neg = set() if neg is None else set(neg)
    A = np.zeros((n, n), dtype=np.int64)
    for i, (u, v) in enumerate(E):
        s = -1 if i in neg else 1; A[u, v] = A[v, u] = s
    return A

def main():
    tower = [(E0, 80, None)]
    E, n = E0, 80
    for lvl in (1, 2, 3):
        mats = factor4(E, n); ei = {e: i for i, e in enumerate(E)}
        rows = []
        for a, b in itertools.combinations(range(4), 2):
            neg = {ei[e] for e in mats[a] | mats[b]}
            rho = float(np.max(np.abs(np.linalg.eigvalsh(signed_adj(E, n, neg)))))
            rows.append((rho, a, b, neg))
        rows.sort(key=lambda x: (x[0], x[1], x[2]))
        E = lift_edges(E, n, rows[0][3]); n = 2*n
        tower.append((E, n, rows[0][3]))

    certs = []
    for li in (1, 2, 3):
        Ep, np_ = tower[li-1][0], tower[li-1][1]; neg = tower[li][2]
        As = int_mat(Ep, np_, neg)
        B = 12*np.eye(np_, dtype=np.int64) - (As@As)
        ok, kk, ds = exact_ldl_psd(B)
        certs.append({'level': li, 'signed_parent_n': np_,
                      'B_eq_12I_minus_As2_positive_definite': ok, 'n_pivots': kk,
                      'min_pivot_exact': str(min(ds)) if ok else None,
                      'min_pivot_float': float(min(ds)) if ok else None})
        assert ok

    out = {
      'pass': 5701,
      'status': 'EXACT_POSITIVITY_FOR_THREE_SEPARATE_FACTOR_PAIR_LIFTS_THROUGH_640_VERTICES',
      'tower_provenance': ('Separate deterministic factor-pair tower, not the frozen Pass5683/5693 tower; '
                           'no isomorphism comparison has been computed.'),
      'method': 'exact rational LDL of B = 12 I - A_signed^2, all pivots strictly positive Fractions',
      'certificates': certs,
      'scope': 'Selected signings on parents 80, 160, and 320 only; no 640-parent signing is produced.',
      'physics_boundary': 'Exact integer/rational matrix algebra for a finite graph tower; not an all-level theorem or continuum Yang-Mills mass gap.'
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(out, indent=2, sort_keys=True))
if __name__ == '__main__': main()
