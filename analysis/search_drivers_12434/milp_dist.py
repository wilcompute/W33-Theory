"""12434: exact minimum weight of ker_2(A) for the W(3,q) collinearity graph (every nonzero word, stabilisers included), by MILP:
minimise sum x, x binary, A x = 2 k (k integer), x_0 = 1 (point-transitivity of Sp(4,q) lets one point be fixed).  Since stabilisers
(rowspace) have weight >= 2q + 2 (no-triangle argument, even case) and weight-2q logicals exist (12421), min weight = 2q proves d = 2q.
Control q = 3: must return 6 (cross-track exhaustive).  Also records whether the optimum word has an odd line intersection."""
import sys, json, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, '../search_drivers_12419')
from two_codes import w3q

out = {}
for q in [int(a) for a in sys.argv[1:]] or [3, 5]:
    A = w3q(q); n = len(A)
    nv = 2 * n
    c = np.concatenate([np.ones(n), np.zeros(n)])
    M = np.hstack([A, -2 * np.eye(n)])
    cons = [LinearConstraint(M, 0, 0)]
    lb = np.concatenate([np.zeros(n), np.zeros(n)]); ub = np.concatenate([np.ones(n), np.full(n, q * (q + 1))])
    lb[0] = 1
    t0 = time.time()
    res = milp(c, constraints=cons, integrality=np.ones(nv), bounds=Bounds(lb, ub), options=dict(time_limit=3000))
    x = np.round(res.x[:n]).astype(int) if res.x is not None else None
    rec = dict(n=n, status=res.message, optimal=bool(res.status == 0), min_weight=int(x.sum()) if x is not None else None, seconds=round(time.time() - t0, 1),
               mip_gap=getattr(res, 'mip_gap', None))
    if x is not None:
        assert not ((A @ x) % 2).any()
        S = set(np.nonzero(x)[0].tolist())
        # lines through the optimum: odd intersections?
        odd = 0
        for i in range(n):
            for j in range(i + 1, n):
                if A[i, j] and i in S:
                    L = {i, j} | {k for k in range(n) if A[i, k] and A[j, k]}
                    if len(S & L) % 2: odd += 1
        rec['optimum_has_odd_line'] = odd > 0
    out[q] = rec
    print(q, rec, flush=True)
json.dump(out, open('milp_dist_' + '_'.join(str(k) for k in out) + '.json', 'w'), indent=1)
