"""12462b: Embedding lemma.  For a graph G on N vertices and any prime q: put M_ij = 0 for edges ij, M_ij = 1 for non-edges (i > j), and
u_i = (e_i, g_i) in F_q^N + F_q^N with g_i[j] = M_ij for j < i, 0 otherwise.  With omega((x,y),(x',y')) = x.y' - y.x':
omega(u_i, u_j) = g_j[i] - g_i[j] = -M_ij (i > j), so u_i is orthogonal to u_j iff ij is an edge; the u_i are projectively distinct
(distinct e_i parts).  Hence G is an INDUCED subgraph of the collinearity graph of W(2N-1, q).  Verified here for grids, a random graph
and the W(3,3) graph itself, at q = 2, 3, 5."""
import json, random, itertools
import numpy as np
def embed(adj, q):
    N = len(adj); U = np.zeros((N, 2 * N), dtype=int)
    for i in range(N):
        U[i, i] = 1
        for j in range(i): U[i, N + j] = 0 if adj[i][j] else 1
    om = (U[:, :N] @ U[:, N:].T - U[:, N:] @ U[:, :N].T) % q
    return all((om[i, j] == 0) == bool(adj[i][j]) for i in range(N) for j in range(N) if i != j)
def grid(a, b):
    c = [(i, j) for i in range(a) for j in range(b)]
    return [[int(abs(x[0] - y[0]) + abs(x[1] - y[1]) == 1) for y in c] for x in c]
random.seed(12462)
R = [[0] * 20 for _ in range(20)]
for i, j in itertools.combinations(range(20), 2):
    R[i][j] = R[j][i] = random.randint(0, 1)
import sys; sys.path.insert(0, '../search_drivers_12419'); from two_codes import w3q
W = w3q(3).tolist()
res = {f'{name}_q{q}': embed(g, q) for name, g in (('grid3x3', grid(3, 3)), ('grid5x5', grid(5, 5)), ('random20', R), ('W33', W)) for q in (2, 3, 5)}
print(res); json.dump(res, open('embed_lemma.json', 'w'), indent=1)
