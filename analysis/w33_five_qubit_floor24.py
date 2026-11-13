"""Pass 12652 item 2: what is the robust floor of 24 in the five-qubit size-8 search (Pass 12650/12651)?  Collect annealed 6-matrix
states {S_1..S_6} (with L0, L1: 8 Lagrangians) whose set E of extendible nonsingular symmetric T (T + S_i nonsingular for all i) has
|E| = 24, and analyse E: its compatibility graph (T + T' nonsingular), clique number, whether adding a clique of E gives a maximal set
(size 9 = 6 + 1 + ...), the rank distribution of pairwise sums, the GL/orthogonal invariants, and whether E is an affine object
(e.g. closed under T, T' -> T + T' + T'').  usage: py -3 analysis/w33_five_qubit_floor24.py [n_states] [seconds]"""
import json, os, sys, time, math, itertools
from collections import Counter
import numpy as np
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_symmetric_rank_code_spreads.py")}
src = open(os.path.join(HERE, "w33_symmetric_rank_code_spreads.py"), encoding="utf-8").read()
exec(src[: src.index("def code_of")], g)
n = 5; pos, sing, alt, ns = g["setup"](n)
want = int(sys.argv[1]) if len(sys.argv) > 1 else 12
tl = float(sys.argv[2]) if len(sys.argv) > 2 else 900
def compat(S):
    m = np.ones(len(ns), bool)
    for s in S: m &= ~sing[ns ^ s]
    return m
def rank(c):
    rows = [0] * n
    for b, (i, j) in enumerate(pos):
        if c >> b & 1: rows[i] |= 1 << j; rows[j] |= 1 << i
    r = 0
    for col in range(n):
        piv = next((k for k in range(r, n) if rows[k] >> col & 1), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for k in range(n):
            if k != r and rows[k] >> col & 1: rows[k] ^= rows[r]
        r += 1
    return r
rng = np.random.default_rng(5); t0 = time.time(); states = []; k = 6; costs = Counter()
while len(states) < want and time.time() - t0 < tl:
    S = []; avail = np.ones(len(ns), bool)
    while len(S) < k and avail.any():
        i = int(rng.choice(np.flatnonzero(avail))); S.append(int(ns[i])); avail &= ~sing[ns ^ ns[i]]
    if len(S) < k: continue
    c = int(compat(S).sum()); T = 3.0
    for step in range(6000):
        drop = list(rng.choice(k, 2 if rng.random() < 0.3 else 1, replace=False)); keep = [S[i] for i in range(k) if i not in drop]
        new = list(keep)
        for _ in drop:
            cand = np.flatnonzero(compat(new))
            if len(cand) == 0: break
            new.append(int(ns[int(rng.choice(cand))]))
        if len(new) < k: continue
        c2 = int(compat(new).sum())
        if c2 <= c or rng.random() < math.exp(-(c2 - c) / max(T, 1e-3)): S, c = new, c2
        T = max(0.05, T * 0.9993)
        if c <= 24: break
    costs[c] += 1
    if c == 24 and sorted(S) not in [sorted(s) for s in states]: states.append(S)
print("final costs", dict(costs), "states with 24:", len(states), round(time.time() - t0), "s", flush=True)
out = dict(final_costs=dict(costs), n_states=len(states), states=[])
for S in states:
    E = ns[compat(S)].tolist()
    G = nx.Graph(); G.add_nodes_from(E)
    G.add_edges_from((a, b) for a, b in itertools.combinations(E, 2) if not sing[a ^ b])
    cliques = list(nx.find_cliques(G)); om = max(len(c) for c in cliques)
    # after adding a maximum clique of E, is the set maximal? (size = 2 + 6 + |clique|)
    maxed = []
    for c in cliques:
        rest = [t for t in E if all(not sing[t ^ x] for x in c) and t not in c]
        maxed.append((len(c), len(rest) == 0))
    sum_ranks = Counter(rank(a ^ b) for a, b in itertools.combinations(E, 2))
    rank_to_S = Counter(rank(t ^ s) for t in E for s in S)
    # affine closure test: is t1+t2+t3 in E for t's in E?
    Es = set(E); trip = sum(1 for a, b, c in itertools.combinations(E, 3) if (a ^ b ^ c) in Es)
    span = set([0])
    for t in E:
        span |= {x ^ t for x in span}
    deg = sorted(dict(G.degree()).values())
    rec = dict(S=S, E=E, compat_edges=G.number_of_edges(), degrees=dict(Counter(deg)), clique_number=om,
               clique_sizes=dict(Counter(len(c) for c in cliques)), maximal_after_clique=dict(Counter(maxed).items().__iter__()) if False else [list(x) for x in sorted(set(maxed))],
               pair_sum_ranks=dict(sum_ranks), rank_T_plus_S=dict(rank_to_S), affine_triples_in_E=trip, span_dim=int(round(math.log2(len(span)))),
               components=[len(c) for c in nx.connected_components(G)])
    print({k_: v for k_, v in rec.items() if k_ not in ("S", "E")}, flush=True); out["states"].append(rec)
json.dump(out, open(os.path.join(ROOT, "data", "w33_five_qubit_floor24.json"), "w"), indent=1)
