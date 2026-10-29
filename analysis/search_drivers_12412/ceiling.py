"""12412b: the entanglement ceiling.  p-ranks of the W(3,3) adjacency (p = 2, 3) and the maximum cut-rank over all bipartitions, by
hill-climbing (swap moves, many restarts), with the same search on random 12-regular graphs as control (must reach ~ min(|A|, |B|))."""
import json, random
import numpy as np
import networkx as nx
from arealaw import w33, rank_mod
G, _ = w33()
rng = random.Random(4)
def cutrank(H, A, p):
    A = sorted(A); B = [i for i in range(len(H)) if i not in A]
    return rank_mod(H[np.ix_(A, B)], p)
def climb(H, p, k, iters=400):
    A = set(rng.sample(range(len(H)), k)); best = cutrank(H, A, p)
    for _ in range(iters):
        a = rng.choice(sorted(A)); b = rng.choice([i for i in range(len(H)) if i not in A])
        B = (A - {a}) | {b}; s = cutrank(H, B, p)
        if s >= best: A, best = B, s
    return best
out = {}
for p in (3, 2):
    out[f'rank_A_mod{p}'] = rank_mod(G, p)
    out[f'max_cutrank_F{p}'] = {k: max(climb(G, p, k) for _ in range(6)) for k in (10, 15, 20)}
    H = nx.to_numpy_array(nx.random_regular_graph(12, 40, seed=7), dtype=np.int64)
    out[f'control_max_cutrank_F{p}'] = {k: max(climb(H, p, k) for _ in range(3)) for k in (10, 15, 20)}
    print(p, out)
json.dump(out, open('ceiling.json', 'w'), indent=1)
# the mechanism: (A + I)^2 = J mod 3 and rank_3(A + I) bounds every cut-rank
N = (G + np.eye(40, dtype=np.int64)) % 3
out['rank_A_plus_I_mod3'] = rank_mod(N, 3)
out['A_plus_I_squared_is_J_mod3'] = bool(((N @ N) % 3 == 1).all())
json.dump(out, open('ceiling.json', 'w'), indent=1)
