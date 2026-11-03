"""Control for the fast HiGHS q = 9 run: (1) class 24380 must be feasible at W = 48 and infeasible at W = 46; (2) the LP relaxation (no integrality) of each sampled case at W = 46: if LP-infeasible, a Farkas certificate exists; report its bound.  usage: py -3 highs_control_q9.py"""
import json, time
import numpy as np
from scipy.optimize import milp, linprog, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from star_cubes import build, orbits
q = 9; B = build(q); digits, reps, counts = orbits(B); lines, through, X = B["lines"], B["through"], B["X"]; m, n = len(lines), len(B["pts"])
A = lil_matrix((n, m + n))
for p in range(n):
    for j in through[p]: A[p, j] = 1
    A[p, m + p] = -2
A = A.tocsr(); out = {}
def case(r):
    star = digits[r]; fixed = {X} | {B["choices"][i][int(star[i])] for i in range(q + 1)}; ban = {j for p in B["Xpts"] for j in through[p]} - fixed
    lb = np.zeros(m + n); ub = np.ones(m + n)
    for j in fixed: lb[j] = 1
    for j in ban: ub[j] = 0
    return lb, ub
c = np.concatenate([np.ones(m), np.zeros(n)])
lb, ub = case(24380)
t0 = time.time(); o = milp(c, constraints=LinearConstraint(A, np.zeros(n), np.zeros(n)), integrality=np.ones(m + n), bounds=Bounds(lb, ub), options=dict(time_limit=900))
out["class_24380_min_weight"] = None if o.x is None else int(round(o.x[:m].sum())); out["class_24380_status"] = int(o.status); out["seconds"] = round(time.time() - t0, 1)
import random
rng = random.Random(1); lps = []
for r in rng.sample(reps.tolist(), 12) + [24380]:
    lb, ub = case(r); l = linprog(c, A_eq=A, b_eq=np.zeros(n), bounds=list(zip(lb, ub)), method="highs")
    lps.append(dict(rep=r, status=int(l.status), lp_min=None if l.status else round(float(l.fun), 3)))
out["lp_relaxation_min_weight"] = lps; print(json.dumps(out)); json.dump(out, open("highs_control_q9.json", "w"), indent=1)
