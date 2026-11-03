"""12532: the heavy cases of heavy_split.py (same reductions, same case list) solved by HiGHS instead of CP-SAT.  Every point has even coverage <= 2*floor(W/(2(q+1))), the case's lines are fixed, weight <= W.  usage: py -3 heavy_highs.py q W [secs] [first] [last]"""
import json, sys, time
args = sys.argv[1:]; q_, W_ = args[0], args[1]; secs = args[2] if len(args) > 2 else "1800"; first = int(args[3]) if len(args) > 3 else 0; last = int(args[4]) if len(args) > 4 else None
sys.argv = ["heavy_split.py", q_, W_, secs]
exec(open("heavy_split.py", encoding="utf-8").read().split("maxz = W //")[0])
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
maxz = W // (2 * (q + 1)); assert maxz >= 2
m, n = len(lines), len(B["pts"])
A = lil_matrix((n + 1, m + n))
for p_ in range(n):
    for j in through[p_]: A[p_, j] = 1
    A[p_, m + p_] = -2
for j in range(m): A[n, j] = 1
A = A.tocsr(); lo = np.zeros(n + 1); hi = np.zeros(n + 1); hi[n] = W
last = len(cases) if last is None else last
res = dict(q=q, W=W, cases=len(cases), range=[first, last], maxz=maxz, infeasible=0, feasible=[], unknown=[]); t0 = time.time()
for k, fixed in enumerate(cases[first:last]):
    lb = np.zeros(m + n); ub = np.concatenate([np.ones(m), np.full(n, maxz)])
    for j in fixed: lb[j] = 1
    o = milp(np.zeros(m + n), constraints=LinearConstraint(A, lo, hi), integrality=np.ones(m + n), bounds=Bounds(lb, ub), options=dict(time_limit=tl))
    if o.status == 2: res["infeasible"] += 1
    elif o.status == 0: res["feasible"].append(dict(case=first + k, weight=int(round(o.x[:m].sum())), chosen=[int(j) for j in range(m) if o.x[j] > 0.5]))
    else: res["unknown"].append(first + k)
    print(f"  {first + k}: status {o.status} inf {res['infeasible']} feas {len(res['feasible'])} unk {len(res['unknown'])} {time.time() - t0:.0f}s", flush=True)
res["seconds"] = round(time.time() - t0, 1); print({k: (v if k != "feasible" else [f["weight"] for f in v]) for k, v in res.items()}, flush=True)
json.dump(res, open(f"heavy_highs_q{q}_W{W}.json", "w"), indent=1)
