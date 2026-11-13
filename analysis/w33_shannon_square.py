"""Pass 12653 audit, lower bound: alpha(G strong-product G) for the W(3,3) collinearity graph G (alpha(G) = 7, theta = 10).
Theta(G) >= sqrt(alpha(G x G)); alpha(G x G) >= 49 trivially.  CP-SAT model: x_(u,v) Boolean, one clique constraint per pair of
lines (L x L' is a 16-clique; these cover every edge of G x G since adjacent-or-equal points lie on a common line).  Reports the
best set and the solver bound; a set of size >= 50 would give Theta > 7.  Control: C5 x C5 must give 5 (Shannon/Lovasz).
usage: py -3 analysis/w33_shannon_square.py [seconds] [workers]"""
import itertools, json, os, sys, time
import numpy as np
from ortools.sat.python import cp_model
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_shannon_capacity_audit.py")}
exec(open(os.path.join(HERE, "w33_shannon_capacity_audit.py"), encoding="utf-8").read().split("t0 = time.time(); res = {}")[0], g)
tl = float(sys.argv[1]) if len(sys.argv) > 1 else 600; wk = int(sys.argv[2]) if len(sys.argv) > 2 else 2
def solve(cliques, n, tl, wk, hint=None):
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{i}") for i in range(n * n)]
    for L in cliques:
        for M in cliques:
            m.Add(sum(x[u * n + v] for u in L for v in M) <= 1)
    m.Maximize(sum(x))
    if hint:
        for i in range(n * n): m.AddHint(x[i], int(i in hint))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = wk
    st = s.Solve(m)
    sol = [i for i in range(n * n) if s.Value(x[i])]
    return int(s.ObjectiveValue()), int(s.BestObjectiveBound()), s.StatusName(st), sol
# control: C5, cliques = edges (closed: each edge is a maximal clique)
c5 = [[i, (i + 1) % 5] for i in range(5)]
ctrl = solve(c5, 5, 60, wk)
print("control C5xC5", ctrl[:3], flush=True); assert ctrl[0] == 5
A = g["w33"](); n = 40
lines = set()
for i, j in zip(*np.nonzero(np.triu(A, 1))):
    L = frozenset([i, j] + [k for k in range(n) if A[i, k] and A[j, k]])
    lines.add(L)
lines = [sorted(L) for L in lines]; assert len(lines) == 40 and all(len(L) == 4 for L in lines)
# hint: product of a maximum independent set with itself (49)
a7 = g["alpha_exact"](A, 60)
t0 = time.time()
hint = None
if len(sys.argv) > 3 and sys.argv[3] == "hint" and os.path.exists(os.path.join(ROOT, "data", "w33_shannon_square.json")):
    prev = json.load(open(os.path.join(ROOT, "data", "w33_shannon_square.json")))["set"]; hint = {u * n + v for u, v in prev}
best, bound, status, sol = solve(lines, n, tl, wk, hint)
# verify independence
S = [(i // n, i % n) for i in sol]
ok = all(not ((u == u2 or A[u, u2]) and (v == v2 or A[v, v2])) for (u, v), (u2, v2) in itertools.combinations(S, 2))
res = dict(control_C5=ctrl[:3], alpha_G=a7, alpha_G2_best=best, solver_bound=bound, status=status, verified_independent=ok,
           Theta_lower=best ** 0.5, seconds=round(time.time() - t0, 1), set=S)
print({k: v for k, v in res.items() if k != "set"}, flush=True)
out_name = "w33_shannon_square_long.json" if hint else "w33_shannon_square.json"
json.dump(res, open(os.path.join(ROOT, "data", out_name), "w"), indent=1, default=int)
