"""12462: largest induced grid (2D cluster-state graph P_a x P_b) in the collinearity graph of W(2n-1,q).  A Z-basis measurement of a
qudit graph state removes the vertex (up to local Z-type corrections on its neighbours, any prime dimension), so an induced a x b grid
is a cluster state reachable by Pauli measurements alone -- the standard universal MBQC resource once a, b grow.  CP-SAT: one integer
variable per grid cell, AllDifferent, and for every pair of cells a table of vertex pairs whose adjacency matches the grid (adjacent iff
grid neighbours).  usage: py -3 induced_grid.py n q a b [time]"""
import sys, json, time, itertools
import numpy as np
from ortools.sat.python import cp_model


def polar(n2, q):
    # points of PG(2n-1, q) (q prime), adjacency = symplectic orthogonality
    pts = []
    for v in itertools.product(range(q), repeat=n2):
        if any(v):
            f = next(x for x in v if x)
            inv = pow(f, -1, q)
            w = tuple(x * inv % q for x in v)
            if w == v: pts.append(v)
    P = np.array(pts); h = n2 // 2
    om = (P[:, :h] @ P[:, h:].T - P[:, h:] @ P[:, :h].T) % q
    A = (om == 0).astype(int); np.fill_diagonal(A, 0)
    return A


n2, q, a, b = (int(x) for x in sys.argv[1:5]); tl = float(sys.argv[5]) if len(sys.argv) > 5 else 600
A = polar(n2, q); N = len(A)
cells = [(i, j) for i in range(a) for j in range(b)]
adjc = lambda c, d: abs(c[0] - d[0]) + abs(c[1] - d[1]) == 1
E = [(u, v) for u in range(N) for v in range(N) if u != v and A[u, v]]
NE = [(u, v) for u in range(N) for v in range(N) if u != v and not A[u, v]]
m = cp_model.CpModel()
X = [m.NewIntVar(0, N - 1, f'c{k}') for k in range(len(cells))]
m.AddAllDifferent(X)
for (k, c), (l, d) in itertools.combinations(enumerate(cells), 2):
    m.AddAllowedAssignments([X[k], X[l]], E if adjc(c, d) else NE)
m.Add(X[0] == 0)                                               # vertex transitivity
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 8
t0 = time.time(); st = s.Solve(m)
rec = dict(polar=f'W({n2 - 1},{q})', points=N, grid=f'{a}x{b}', status=s.StatusName(st), seconds=round(time.time() - t0, 1))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    emb = [s.Value(v) for v in X]
    rec['verified_induced'] = all(A[emb[k], emb[l]] == adjc(c, d) for (k, c), (l, d) in itertools.combinations(enumerate(cells), 2))
    rec['embedding'] = emb
print(json.dumps({k: v for k, v in rec.items() if k != 'embedding'}), flush=True)
json.dump(rec, open(f'grid_W{n2 - 1}_{q}_{a}x{b}.json', 'w'), indent=1)
