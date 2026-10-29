"""12360: a minimal set of SM-singlet scalars whose monomials give mass to every vector-like and fractionally charged fermion of
SM_2913_v6 (structural full rank of each block: Q 6x3, U 3x6, D 3x6, L 7x4, E 3x6, X 4x4, Z 4x4 (pseudo-real doublets pair among
themselves), F 20x20 -- the 52 fractional fermions are X, Z, F).  Chiral SM fermions stay massless by chirality.  Greedy removal from
all 80 singlets (least-used first), re-testing only couplings whose witness monomial used the removed singlet.  This is a sufficient
structural set, NOT a vacuum: the potential, its minimisation and the singlet VEV sizes are not computed; structural rank is an upper
bound on the rank for coefficients that are not generic."""
import sys, json, collections
import numpy as np
import networkx as nx
sys.path.insert(0, '.')
from mono import FS, min_degree, typ, smsing, S, NS
F19 = [f for f in FS if f['m'] == 19 and smsing(f)]
G = {}
for f in F19:
    t, c = typ(f)
    if t: G.setdefault((t, c), []).append(f)
BLOCKS = [('Q', G[('Q', False)], G[('Q', True)]), ('U', G[('U', True)], G[('U', False)]), ('D', G[('D', True)], G[('D', False)]),
          ('L', G[('L', False)], G[('L', True)]), ('E', G[('E', True)], G[('E', False)]), ('X', G[('X', False)], G[('X', True)]),
          ('F', G[('F', False)], G[('F', True)]), ('Z', G[('Z', False)], G[('Z', False)])]
def need(name, R, C):
    return 4 if name == 'Z' else min(len(R), len(C))
def edges_for(name, R, C, allowed, cache=None, removed=None):
    E = {}
    for i, a in enumerate(R):
        for j, b in enumerate(C):
            if name == 'Z' and j <= i:
                continue
            key = (name, i, j)
            if cache is not None and key in cache and (cache[key] is None or removed not in [s for s, e in cache[key][1]]):
                E[key] = cache[key] if (cache[key] is None or all(allowed[s] for s, e in cache[key][1])) else min_degree([(a, 1), (b, 1)], allowed)
                if cache[key] is None:
                    E[key] = None
                continue
            E[key] = min_degree([(a, 1), (b, 1)], allowed)
    return E
def rank_ok(E):
    ok = {}
    for name, R, C in BLOCKS:
        g = nx.Graph()
        for (n, i, j), v in E.items():
            if n == name and v is not None:
                g.add_edge(('r', i), ('c', j)) if name != 'Z' else g.add_edge(i, j)
        mt = len(nx.max_weight_matching(g, maxcardinality=True)) if g.number_of_edges() else 0
        ok[name] = (2 * mt if name == 'Z' else mt, need(name, R, C))
    return ok
def all_edges(allowed, cache=None, removed=None):
    E = {}
    for name, R, C in BLOCKS:
        E.update(edges_for(name, R, C, allowed, cache, removed))
    return E
if __name__ == '__main__':
    allowed = [True] * NS
    E = all_edges(allowed); ok = rank_ok(E)
    print('all singlets:', ok, flush=True)
    assert all(a >= b for a, b in ok.values())
    use = collections.Counter(s for v in E.values() if v for s, e in v[1])
    order = sorted(range(NS), key=lambda s: (use[s], s))
    for s in order:
        trial = list(allowed); trial[s] = False
        E2 = all_edges(trial, E, s); ok2 = rank_ok(E2)
        if all(a >= b for a, b in ok2.values()):
            allowed, E = trial, E2
    vac = [s for s in range(NS) if allowed[s]]
    ok = rank_ok(E)
    degs = {name: collections.Counter(v[0] for (n, i, j), v in E.items() if n == name and v is not None) for name, _, _ in BLOCKS}
    print('minimal set size', len(vac), 'singlets', vac, ok)
    print('sectors of the vacuum singlets (n, Witten):', collections.Counter((S[s]['n'], S[s]['w']) for s in vac))
    json.dump(dict(vacuum=vac, vacuum_ids=[S[s]['id'] for s in vac], rank=ok, degree_hist={k: dict(v) for k, v in degs.items()}), open('vacuum.json', 'w'), indent=1)
