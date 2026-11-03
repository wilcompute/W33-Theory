"""Second solver family: HiGHS MILP on the star cases (no shared code with CP-SAT).  usage: py -3 recheck_highs.py q W secs [first] [last]"""
import json, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from star_cubes import build, orbits
q, W, tl = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]); first = int(sys.argv[4]) if len(sys.argv) > 4 else 0
B = build(q); digits, reps, counts = orbits(B); last = int(sys.argv[5]) if len(sys.argv) > 5 else len(reps); lines, through, X = B["lines"], B["through"], B["X"]; m, n = len(lines), len(B["pts"])
A = lil_matrix((n + 1, m + n))
for p in range(n):
    for j in through[p]: A[p, j] = 1
    A[p, m + p] = -2
for j in range(m): A[n, j] = 1
A = A.tocsr(); lo = np.zeros(n + 1); hi = np.zeros(n + 1); hi[n] = W; lo[n] = 1
res = dict(q=q, W=W, classes=len(reps), range=[first, last], infeasible=0, feasible=[], unknown=[]); t0 = time.time()
for k, r in enumerate(reps.tolist()[first:last]):
    star = digits[r]; fixed = {X} | {B["choices"][i][int(star[i])] for i in range(q + 1)}; ban = {j for p in B["Xpts"] for j in through[p]} - fixed
    lb = np.zeros(m + n); ub = np.ones(m + n)
    for j in fixed: lb[j] = 1
    for j in ban: ub[j] = 0
    o = milp(np.zeros(m + n), constraints=LinearConstraint(A, lo, hi), integrality=np.ones(m + n), bounds=Bounds(lb, ub), options=dict(time_limit=tl))
    # status 2 = infeasible, 0 = optimal, 1 = limit
    if o.status == 2: res["infeasible"] += 1
    elif o.status == 0: res["feasible"].append(dict(rep=r, weight=int(round(o.x[:m].sum()))))
    else: res["unknown"].append(r)
    print(f"  {k + 1}: rep {r} status {o.status} {time.time() - t0:.0f}s", flush=True)
res["seconds"] = round(time.time() - t0, 1); print(res, flush=True); json.dump(res, open(f"recheck_highs_q{q}_W{W}_{first}_{last}.json", "w"), indent=1)
