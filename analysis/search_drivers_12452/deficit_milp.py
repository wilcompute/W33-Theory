"""12452: smallest entanglement-deficient region of the binary W(3,q) graph state, exactly, by MILP.  A region R is deficient iff some
nonzero x supported in R has (A x mod 2) supported in R.  Minimise sum r subject to r >= x, A x = 2k + p (p binary parity), r >= p,
sum x >= 1, x_0 = 1 (transitivity).  Control q = 3: must give 6 (12427, exhaustive).  Question: is the minimum the code distance 2q?"""
import sys, json, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q

out = {}
for q in [int(a) for a in sys.argv[1:]] or [3, 5]:
    A = w3q(q); n = len(A)
    # variables: x (n), r (n), p (n), k (n)
    nv = 4 * n
    c = np.concatenate([np.zeros(n), np.ones(n), np.zeros(n), np.zeros(n)])
    rows, lo, hi = [], [], []
    I = np.eye(n)
    rows.append(np.hstack([A, np.zeros((n, n)), -I, -2 * I])); lo.append(np.zeros(n)); hi.append(np.zeros(n))      # A x - p - 2k = 0
    rows.append(np.hstack([-I, I, np.zeros((n, n)), np.zeros((n, n))])); lo.append(np.zeros(n)); hi.append(np.full(n, np.inf))  # r >= x
    rows.append(np.hstack([np.zeros((n, n)), I, -I, np.zeros((n, n))])); lo.append(np.zeros(n)); hi.append(np.full(n, np.inf))  # r >= p
    M = np.vstack(rows); L = np.concatenate(lo); H = np.concatenate(hi)
    lb = np.zeros(nv); ub = np.concatenate([np.ones(n), np.ones(n), np.ones(n), np.full(n, q * (q + 1))])
    lb[0] = 1
    t0 = time.time()
    res = milp(c, constraints=LinearConstraint(M, L, H), integrality=np.ones(nv), bounds=Bounds(lb, ub), options=dict(time_limit=3000))
    rec = dict(n=n, optimal=bool(res.status == 0), status=res.message, seconds=round(time.time() - t0, 1))
    if res.x is not None:
        x = np.round(res.x[:n]).astype(int); r = np.round(res.x[n:2 * n]).astype(int)
        rec.update(min_region=int(r.sum()), x_weight=int(x.sum()), x_in_kernel=bool(not ((A @ x) % 2).any()))
    out[q] = rec
    print(q, rec, flush=True)
json.dump(out, open('deficit_milp.json', 'w'), indent=1)
