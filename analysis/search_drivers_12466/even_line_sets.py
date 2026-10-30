"""12467: minimum size of a nonempty EVEN line set of W(3,q) (every point on an even number of chosen lines) = minimum weight of
ker_2 N (N = point-line incidence), by exact MILP.  Why: in the remaining case of d = 2q (12466) the line set Y of a minimal
representation covers every point outside S evenly, |S| < 2q, so Y is within |S| odd points of an even line set; small even line sets
are what such a Y must resemble.  Natural candidates: a pencil pair is not even; a (q,1) grid sub-quadrangle would be (2(q+1) lines, each
point on 2) but W(q) has no (q,1) sub-GQ for q odd (its lines are not regular).  Control: q = 2 (lines regular) has even line sets from
grids, so the minimum there must be <= 2(q+1) = 6.  usage: py -3 even_line_sets.py q [time]"""
import sys, json, time, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


def polar(q):
    pts = []
    for v in itertools.product(range(q), repeat=4):
        if any(v):
            f = next(x for x in v if x); inv = pow(f, -1, q); w = tuple(x * inv % q for x in v)
            if w == v: pts.append(v)
    P = np.array(pts)
    om = (P[:, :2] @ P[:, 2:].T - P[:, 2:] @ P[:, :2].T) % q
    A = (om == 0).astype(int); np.fill_diagonal(A, 0)
    return A


q = int(sys.argv[1]); tl = float(sys.argv[2]) if len(sys.argv) > 2 else 1800
A = polar(q); n = len(A)
lines = set()
for a in range(n):
    for b in range(a + 1, n):
        if A[a, b]:
            L = tuple(sorted([x for x in range(n) if x in (a, b) or (A[a, x] and A[b, x])]))
            if len(L) == q + 1: lines.add(L)
lines = sorted(lines); m = len(lines); assert m == (q + 1) * (q * q + 1)
N = np.zeros((n, m), dtype=int)
for j, L in enumerate(lines): N[list(L), j] = 1
# variables: y (m binary), z (n integer); N y - 2 z = 0; sum y >= 1; y_0 = 1 (line transitivity)
c = np.concatenate([np.ones(m), np.zeros(n)])
M = np.vstack([np.hstack([N, -2 * np.eye(n)]), np.concatenate([np.ones(m), np.zeros(n)])[None, :]])
lo = np.concatenate([np.zeros(n), [1]]); hi = np.concatenate([np.zeros(n), [np.inf]])
lb = np.zeros(m + n); ub = np.concatenate([np.ones(m), np.full(n, (q + 1) // 2)]); lb[0] = 1
t0 = time.time()
r = milp(c, constraints=LinearConstraint(M, lo, hi), integrality=np.ones(m + n), bounds=Bounds(lb, ub), options=dict(time_limit=tl))
rec = dict(q=q, lines=m, optimal=bool(r.status == 0), seconds=round(time.time() - t0, 1), status=r.message)
if r.x is not None:
    y = np.round(r.x[:m]).astype(int); cov = N @ y
    rec.update(min_even_line_set=int(y.sum()), verified_even=bool(not (cov % 2).any()), coverage_profile=sorted(set(int(v) for v in cov)))
print(json.dumps(rec), flush=True)
json.dump(rec, open(f'even_line_sets_q{q}.json', 'w'), indent=1)
