"""12452b: is there an entanglement-deficient region of size <= R of the binary W(3,q) graph state?  x != 0, p_y = (A x)_y mod 2 via native
XOR, region r_i = x_i OR p_i, sum r <= R.  Symmetry as in cpsat_dist.py: x_0 = 1 and (a) a fixed neighbour of 0 in supp x, or (b) no neighbour
of 0 in supp x and a fixed non-neighbour in supp x, or (c) x = {0} alone (only possible when R >= 1 + q(q+1)).  Infeasible in (a), (b) and
R < 1 + q(q+1) => smallest deficient region > R.  Usage: py -3 deficit_cpsat.py q R [time_limit]"""
import sys, json, time
from ortools.sat.python import cp_model
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q

q, R = int(sys.argv[1]), int(sys.argv[2])
tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600
A = w3q(q); n = len(A)
nb0 = [j for j in range(n) if A[0, j]]; far0 = [j for j in range(1, n) if not A[0, j]]
res = {}
for case in ('a', 'b'):
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(n)]; p = [m.NewBoolVar(f'p{i}') for i in range(n)]; r = [m.NewBoolVar(f'r{i}') for i in range(n)]
    one = m.NewConstant(1)
    for y in range(n):
        m.AddBoolXOr([x[j] for j in range(n) if A[y, j]] + [p[y], one])
        m.AddMaxEquality(r[y], [x[y], p[y]])
    m.Add(sum(r) <= R)
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
        rec['region'] = sum(s.Value(v) for v in r); rec['x_weight'] = sum(s.Value(v) for v in x)
    res[case] = rec
    print(q, R, case, rec, flush=True)
json.dump(dict(q=q, R=R, cases=res, no_region_le_R=all(c['status'] == 'INFEASIBLE' for c in res.values()) and R < 1 + q * (q + 1)),
          open(f'deficit_cpsat_q{q}_R{R}.json', 'w'), indent=1)
