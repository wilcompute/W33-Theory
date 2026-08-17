#!/usr/bin/env python3
"""Pass5702: sampled Kesten--McKay CDF discrepancies for three finite signings.

This uses the separate deterministic factor-pair tower of Pass5699, not the
frozen Pass5683/5693 tower.  At each 2-lift the signed adjacency eigenvalues are
the new spectral parameters in the exact child block decomposition; they are not
themselves Artin L-function zeros.

We compare the three finite signed spectra with the Kesten--McKay measure of the
4-regular tree,

    rho_KM(lambda) = (4 sqrt(12 - lambda^2)) / (2 pi (16 - lambda^2)),
    |lambda| <= 2 sqrt(3),

two ways:

(1) Moment matching.  Tree moments and signed matrix traces are computed with
    exact integer arithmetic.  The moments match exactly through M6; the finite
    per-vertex M8 discrepancies are -4, -12/5, and -9/10.

(2) A sampled CDF discrepancy on a fixed 241-point grid.  The Kesten--McKay CDF
    is evaluated by double-precision trapezoidal quadrature with 4000 panels per
    grid point.  The observed values 0.02102, 0.01079, and 0.00540 decrease across
    these three levels.  This is not the exact Kolmogorov--Smirnov statistic, no
    quadrature error bound is supplied, and no convergence-rate theorem follows.
"""
from __future__ import annotations
import itertools, collections, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/PART_W33_PASS5702_KESTEN_MCKAY_EQUIDISTRIBUTION.json'
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

MAXM = 12; f = {0: 1}; KM = {}
for tt in range(1, 2*MAXM+1):
    nf = collections.Counter()
    for r, c in f.items():
        if r == 0: nf[1] += 4*c
        else: nf[r-1] += c; nf[r+1] += 3*c
    f = nf
    if tt % 2 == 0: KM[tt] = f.get(0, 0)

def km_cdf(x):
    if x <= -RAM: return 0.0
    if x >= RAM: return 1.0
    xs = np.linspace(-RAM, x, 4001)
    fv = 4*np.sqrt(np.clip(12-xs*xs, 0, None))/(2*np.pi*(16-xs*xs))
    return float(np.trapezoid(fv, xs))

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

    grid = np.linspace(-RAM, RAM, 241)
    km_vals = np.array([km_cdf(x) for x in grid]); km_vals /= km_vals[-1]

    moment_rows = []; discrepancy_rows = []
    for li in (1, 2, 3):
        neg = tower[li][2]; Ep, np_ = tower[li-1][0], tower[li-1][1]
        As = signed_adj(Ep, np_, neg).astype(np.int64)
        evs = np.linalg.eigvalsh(As.astype(float))
        Ap2 = np.eye(np_, dtype=np.int64); mrow = {'level': li, 'parent_n': np_}
        for m in range(1, 7):
            Ap2 = Ap2@As@As
            numerator = int(np.trace(Ap2))
            moment = Fraction(numerator, np_)
            diff = moment - KM[2*m]
            if m <= 3:
                assert diff == 0
            mrow[f'M{2*m}_trace_exact'] = numerator
            mrow[f'M{2*m}_per_vertex_exact'] = str(moment)
            mrow[f'KM{2*m}'] = KM[2*m]
            mrow[f'diff{2*m}_exact'] = str(diff)
            mrow[f'diff{2*m}_float'] = round(float(diff), 6)
        moment_rows.append(mrow)
        emp = np.array([np.mean(evs <= x) for x in grid])
        discrepancy_rows.append({'level': li, 'n': np_,
                                 'sampled_cdf_discrepancy': round(float(np.max(np.abs(emp-km_vals))), 5)})

    out = {
      'pass': 5702,
      'status': 'THREE_LEVEL_SAMPLED_KM_CDF_DISCREPANCY_WITH_EXACT_LOW_MOMENTS',
      'tower_provenance': ('Separate deterministic factor-pair tower, not the frozen Pass5683/5693 tower; '
                           'no isomorphism comparison has been computed.'),
      'km_density': 'rho(lambda) = 4 sqrt(12-lambda^2) / (2 pi (16-lambda^2)) on [-2 sqrt(3), 2 sqrt(3)]',
      'tree_moments_exact': {str(2*m): KM[2*m] for m in range(1, 7)},
      'moment_matching': moment_rows,
      'sampled_cdf_discrepancies': discrepancy_rows,
      'sampling_contract': {'lambda_grid_points': 241,
                            'quadrature_panels_per_cdf_value': 4000,
                            'quadrature': 'double-precision trapezoidal',
                            'rigorous_quadrature_error_bound': None,
                            'is_exact_KS_statistic': False},
      'finite_observation': 'The sampled discrepancies decrease across these three levels; no rate or all-level limit is proved.',
      'physics_boundary': 'Finite spectral diagnostics only; no GOE, chaos, continuum, or physical-spectrum interpretation is claimed.'
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(out, indent=2, sort_keys=True))
if __name__ == '__main__': main()
