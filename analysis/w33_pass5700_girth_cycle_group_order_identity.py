#!/usr/bin/env python3
"""Pass5700: trace-excess identity and the two root-grade cycle orbits.

Exact integer trace arithmetic (no floats): with M8 = 2092 the 8th moment of the
4-regular infinite tree (Kesten--McKay), the Levi graph of W(3,3) satisfies

    Tr(A^8) = 193280 = 80*2092 + 25920 = n*M8 + |PSp(4,3)|,

so the number of girth-8 cycles is 25920/16 = 1620.  BT545 and Pass75 already
own that 1620-cycle result and the Levi spectrum.  For the separate deterministic
factor-pair tower used here, the observed excess sequence is
25920 -> 25600 -> 25216 -> 24928 while girth remains 8 at the four computed
levels.  No all-level convergence theorem is inferred.

The 25920 ordered cycle encodings split into two PSp(4,3) orbits of 12960,
each with stabilizer C2.  The separator is exactly the root grade: one orbit is
point-rooted and the other is line-rooted.  It is not a chirality invariant.
W(3,3) is not self-dual, so no point-line merger under W(E6), no grading-reversing
Levi automorphism, and no regular-action claim is made.
"""
from __future__ import annotations
import itertools, collections, json, math
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/PART_W33_PASS5700_GIRTH_CYCLE_GROUP_ORDER_IDENTITY.json'

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

def int_mat(E, n, neg=None):
    neg = set() if neg is None else set(neg)
    A = np.zeros((n, n), dtype=np.int64)
    for i, (u, v) in enumerate(E):
        s = -1 if i in neg else 1; A[u, v] = A[v, u] = s
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
def signed_adj(E, n, neg):
    neg = set(neg); A = np.zeros((n, n))
    for i, (u, v) in enumerate(E):
        s = -1.0 if i in neg else 1.0; A[u, v] = A[v, u] = s
    return A
def girth(E, n):
    adj = [[] for _ in range(n)]
    for u, v in E: adj[u].append(v); adj[v].append(u)
    best = 10**9
    for s in range(n):
        dist = {s: 0}; par = {s: -1}; q = collections.deque([s]); g = 10**9
        while q:
            u = q.popleft()
            if 2*dist[u]+1 >= g: continue
            for v in adj[u]:
                if v not in dist: dist[v] = dist[u]+1; par[v] = u; q.append(v)
                elif par[u] != v and par.get(v) != u: g = min(g, dist[u]+dist[v]+1)
        best = min(best, g)
    return best

MAXM = 12; f = {0: 1}; KM = {}
for tt in range(1, 2*MAXM+1):
    nf = collections.Counter()
    for r, c in f.items():
        if r == 0: nf[1] += 4*c
        else: nf[r-1] += c; nf[r+1] += 3*c
    f = nf
    if tt % 2 == 0: KM[tt] = f.get(0, 0)

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

    rows_out = []
    for li, (E, n, neg) in enumerate(tower):
        A = int_mat(E, n); A2 = A@A; A4 = A2@A2; A8 = A4@A4
        t8 = int(np.trace(A8)); exc = t8-n*KM[8]
        assert exc % 16 == 0
        rows_out.append({'level': li, 'n': n, 'Tr_A8_exact': t8,
                         'tree_part': n*KM[8], 'excess': exc,
                         'cycles8': exc//16, 'girth': girth(E, n)})
    assert rows_out[0]['excess'] == 25920
    assert rows_out[0]['cycles8'] == 1620

    def transvection_perm(v):
        perm = []
        for i in range(40):
            u = pts[i]; c = omega(u, v)
            perm.append(P[canon(tuple((u[k]+c*v[k]) % 3 for k in range(4)))])
        return tuple(perm)
    gens = sorted(set(transvection_perm(pts[i]) for i in range(40)))
    def mul(p, q): return tuple(p[q[i]] for i in range(40))
    G = {tuple(range(40))}; frontier = [tuple(range(40))]
    while frontier:
        nf = []
        for g in frontier:
            for h in gens:
                x = mul(g, h)
                if x not in G: G.add(x); nf.append(x)
        frontier = nf
    assert len(G) == 25920

    line_idx = {L: 40+i for i, L in enumerate(lines)}
    def gen80(gp):
        perm = list(gp)
        for i, L in enumerate(lines):
            perm.append(line_idx[frozenset(gp[p] for p in L)])
        return tuple(perm)
    gens80 = [gen80(g) for g in gens]
    adj80 = [[] for _ in range(80)]
    for u, v in E0: adj80[u].append(v); adj80[v].append(u)
    adj80 = [sorted(a) for a in adj80]
    cycles = []
    for s in range(80):
        stack = [(s, [s], {s})]
        while stack:
            u, path, seen = stack.pop()
            if len(path) == 8:
                if s in adj80[u]: cycles.append(tuple(path))
                continue
            for v in adj80[u]:
                if v not in seen: stack.append((v, path+[v], seen | {v}))
    assert len(cycles) == 25920
    def cycle_orbit(seed):
        orbit = {seed}; frontier = [seed]
        while frontier:
            nf = []
            for c in frontier:
                for g in gens80:
                    x = tuple(g[v] for v in c)
                    if x not in orbit: orbit.add(x); nf.append(x)
            frontier = nf
        return orbit
    cycle_set = set(cycles)
    point_seed = next(c for c in cycles if c[0] < 40)
    line_seed = next(c for c in cycles if c[0] >= 40)
    point_orbit = cycle_orbit(point_seed)
    line_orbit = cycle_orbit(line_seed)
    assert len(point_orbit) == len(line_orbit) == 12960
    assert point_orbit.isdisjoint(line_orbit)
    assert point_orbit | line_orbit == cycle_set
    assert all(c[0] < 40 for c in point_orbit)
    assert all(c[0] >= 40 for c in line_orbit)
    p4 = [point_seed[0], point_seed[2], point_seed[4], point_seed[6]]
    stab = [g for g in G if all(g[p] == p for p in p4)]
    assert len(stab) == 2
    g_inv = [g for g in stab if g != tuple(range(40))][0]
    assert mul(g_inv, g_inv) == tuple(range(40))
    fixed = [i for i in range(40) if g_inv[i] == i]

    out = {
      'pass': 5700,
      'status': 'TRACE_EXCESS_IDENTITY_AND_POINT_ROOTED_VERSUS_LINE_ROOTED_CYCLE_ORBITS',
      'tower_provenance': ('Separate deterministic factor-pair tower, not the frozen Pass5683/5693 tower; '
                           'no isomorphism comparison has been computed.'),
      'master_identity': 'Tr(A_levi^8) = 193280 = 80*2092 + 25920 = n*M8_tree + |PSp(4,3)|',
      'tower_excess': [r['excess'] for r in rows_out],
      'tower_cycles8': [r['cycles8'] for r in rows_out],
      'tower_girth': [r['girth'] for r in rows_out],
      'observed_excess_strictly_decreases_in_four_levels': all(
          rows_out[i]['excess'] > rows_out[i+1]['excess'] for i in range(3)),
      'cycle_space': {
          'prior_corpus_owners': 'BT545 and Pass75 already own the 1620 unrooted Levi 8-cycles',
          'unrooted_8cycles': 1620,
          'ordered_cycle_encodings': 25920,
          'root_grade_orbits': {'point_rooted': len(point_orbit),
                                'line_rooted': len(line_orbit),
                                'stabilizer_order_each': 2},
          'separator': 'initial vertex belongs to the point grade or the line grade; this is not chirality',
          'point_orbit_stabilizer_involution': {'fixed_points_on_W33_points': len(fixed),
                                                'transpositions_on_W33_points': (40-len(fixed))//2,
                                                'cycle_structure_on_W33_points': '1^8 2^16'},
          'duality_firewall': ('W(3,3) is not self-dual. No W(E6) point-line merger, grading-reversing '
                               'Levi automorphism, or regular action on the 1620 cycles is claimed.')},
      'physics_boundary': ('Exact finite trace and group-action statements plus a four-level observed excess trend. '
                           'No chirality, physical parity, all-level convergence, or continuum claim.')
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(out, indent=2, sort_keys=True))
if __name__ == '__main__': main()
