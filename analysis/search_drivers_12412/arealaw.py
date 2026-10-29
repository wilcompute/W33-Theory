"""12412: a finite area law?  Qutrit (and qubit) graph state on the collinearity graph of W(3,3) (40 points, degree 12).  Entanglement of
a region A (in units of log q) = rank over F_q of the cut matrix Gamma[A, complement] (standard graph-state formula); the 'area' = number
of edges cut.  Families: the 40 lines (4 points), the 40 point-perps (point + 12 neighbours = 13), the perp of a line (4 + ...), random
sets of each size; control: random 12-regular graphs on 40 vertices (same sizes).  Reports S(A), max possible min(|A|, |A^c|), the
deficit |A| - S(A) (= stabilizers of the graph state supported in A), and S / cut ('bits per area')."""
import itertools, json, random, collections
import numpy as np
import networkx as nx


def w33():
    pts = []
    for v in itertools.product(range(3), repeat=4):
        if any(v) and next(x for x in v if x) == 1:
            pts.append(v)
    om = lambda u, v: (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % 3
    G = np.array([[1 if i != j and om(a, b) == 0 else 0 for j, b in enumerate(pts)] for i, a in enumerate(pts)], dtype=np.int64)
    lines = set()
    for i in range(40):
        for j in range(i + 1, 40):
            if G[i, j]:
                L = frozenset(k for k in range(40) if k in (i, j) or (G[i, k] and G[j, k]))
                if len(L) == 4: lines.add(L)
    return G, sorted(map(sorted, lines))


def rank_mod(m, p):
    m = m.copy() % p
    r = 0
    rows, cols = m.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if m[i, c]), None)
        if piv is None: continue
        m[[r, piv]] = m[[piv, r]]
        inv = pow(int(m[r, c]), p - 2, p)
        m[r] = (m[r] * inv) % p
        for i in range(rows):
            if i != r and m[i, c]:
                m[i] = (m[i] - m[i, c] * m[r]) % p
        r += 1
        if r == rows: break
    return r


def stats(G, A, p):
    A = sorted(A); B = [i for i in range(len(G)) if i not in A]
    S = rank_mod(G[np.ix_(A, B)], p)
    cut = int(G[np.ix_(A, B)].sum())
    return S, cut, min(len(A), len(B))


G, lines = w33()
assert G.sum(axis=1).tolist() == [12] * 40 and len(lines) == 40
rng = random.Random(12412)
out = {}
for p in (3, 2):
    fam = {}
    fam['line'] = [stats(G, L, p) for L in lines]
    fam['perp'] = [stats(G, [i] + [j for j in range(40) if G[i, j]], p) for i in range(40)]
    fam['neighbours'] = [stats(G, [j for j in range(40) if G[i, j]], p) for i in range(40)]
    for k in (4, 8, 13, 20):
        fam[f'random_{k}'] = [stats(G, rng.sample(range(40), k), p) for _ in range(200)]
    res = {}
    for name, rows in fam.items():
        S = [r[0] for r in rows]; cut = [r[1] for r in rows]; mx = [r[2] for r in rows]
        res[name] = dict(S=dict(collections.Counter(S)), max=mx[0], cut=dict(collections.Counter(cut)),
                         deficit_mean=float(np.mean([m - s for s, m in zip(S, mx)])), S_per_cut=float(np.mean([s / c for s, c in zip(S, cut) if c])))
    # control: random 12-regular graphs
    ctrl = {}
    for k in (4, 13, 20):
        vals = []
        for t in range(20):
            H = nx.to_numpy_array(nx.random_regular_graph(12, 40, seed=1000 + t), dtype=np.int64)
            vals += [stats(H, rng.sample(range(40), k), p)[0] for _ in range(20)]
        ctrl[f'random_{k}'] = dict(collections.Counter(vals))
    out[f'F{p}'] = dict(w33=res, control_random_regular=ctrl)
    print(f'F{p}', json.dumps(res, indent=0)[:1500]); print('control', ctrl)
json.dump(out, open('arealaw.json', 'w'), indent=1)
