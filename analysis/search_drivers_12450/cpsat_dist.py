"""12450: minimum weight of ker_2(A) for the W(3,q) collinearity graph by CP-SAT with native XOR constraints.
x_i in {0,1}; for every point y: XOR of x over the neighbours of y, together with a constant-true literal, holds (even parity);
1 <= sum x <= W.  Symmetry (Sp(4,q) is transitive on points and, in the point stabiliser, on neighbours and on non-neighbours -- rank 3):
x_0 = 1 and either (a) x_{n0} = 1 for one fixed neighbour n0, or (b) no neighbour of 0 in S and x_{f0} = 1 for one fixed non-neighbour f0
(every nonzero kernel word has even weight, so |S| >= 2).  Infeasible in both cases => no nonzero kernel word of weight <= W.
Usage: py -3 cpsat_dist.py q W [time_limit_seconds]"""
import sys, json, time
import numpy as np
from ortools.sat.python import cp_model
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q

q, W = int(sys.argv[1]), int(sys.argv[2])
tl = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
A = w3q(q); n = len(A)
nb0 = [j for j in range(n) if A[0, j]]; far0 = [j for j in range(1, n) if not A[0, j]]
res = {}
for case in ('a', 'b'):
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(n)]
    one = m.NewConstant(1)
    for y in range(n):
        m.AddBoolXOr([x[j] for j in range(n) if A[y, j]] + [one])
    m.Add(sum(x) <= W)
    m.Add(x[0] == 1)
    if case == 'a':
        m.Add(x[nb0[0]] == 1)
    else:
        for j in nb0: m.Add(x[j] == 0)
        m.Add(x[far0[0]] == 1)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 8
    t0 = time.time(); st = s.Solve(m)
    rec = dict(status=s.StatusName(st), seconds=round(time.time() - t0, 1))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = np.array([s.Value(v) for v in x]); rec['weight'] = int(sol.sum()); rec['kernel_ok'] = bool(not ((A @ sol) % 2).any())
    res[case] = rec
    print(q, W, case, rec, flush=True)
json.dump(dict(q=q, W=W, cases=res, no_word_of_weight_le_W=all(r['status'] == 'INFEASIBLE' for r in res.values())),
          open(f'cpsat_q{q}_W{W}.json', 'w'), indent=1)
