"""Pass 12644: an ELEMENTARY exact certificate for strong unextendibility of qubit Pauli MUB sets: partition the uncovered Paulis U into k
pairwise-anticommuting sets.  For pairwise anticommuting Hermitian Paulis, sum <P>^2 <= 1 (standard: (sum c_i P_i)^2 = |c|^2 I), so
sum_U <P>^2 <= k and F >= (d - 1 - k)/d.  If k = alpha(anticommutation graph) the bound is tight (stabiliser state).
ILP: colour the COMMUTATION graph on U with k colours (each colour class anticommuting).  Controls: two qubits (k = 2 must exist), three
qubits (k = 6 must NOT exist since theta = 4 + sqrt5 > 6; k = 7 exists -> gives only F >= 0).  Target: the four-qubit size-9 set, k = 14.
Each found cover is re-verified directly (all pairs in a class anticommute, classes partition U).
usage: py -3 analysis/w33_anticommuting_clique_cover.py"""
import itertools, json, os, contextlib, io, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def cover(U, anti, k, tl=1200):
    n = len(U); N = n * k; idx = lambda v, c: v * k + c
    A, lo, hi = [], [], []
    for v in range(n):
        r = np.zeros(N); r[[idx(v, c) for c in range(k)]] = 1; A.append(r); lo.append(1); hi.append(1)
    for a, b in itertools.combinations(range(n), 2):
        if not anti(U[a], U[b]):
            for c in range(k):
                r = np.zeros(N); r[idx(a, c)] = r[idx(b, c)] = 1; A.append(r); lo.append(0); hi.append(1)
    # symmetry breaking: vertex 0 in colour 0
    r = np.zeros(N); r[idx(0, 0)] = 1; A.append(r); lo.append(1); hi.append(1)
    t = time.time()
    res = milp(np.zeros(N), constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.ones(N), bounds=Bounds(0, 1), options=dict(time_limit=tl))
    el = time.time() - t
    if res.x is None:
        return dict(k=k, found=False, status=int(res.status), message=res.message, seconds=el)
    classes = [[U[v] for v in range(n) if res.x[idx(v, c)] > 0.5] for c in range(k)]
    ok = sorted(x for c in classes for x in c) == sorted(U) and all(anti(a, b) for c in classes for a, b in itertools.combinations(c, 2))
    return dict(k=k, found=True, verified=ok, class_sizes=sorted(len(c) for c in classes), seconds=el, classes=classes)
out = {}
# two and three qubits via the census helpers
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("\nres = {}")], cs)
for nq, size, ks in [(2, 3, [2]), (3, 5, [6, 7])]:
    pts, lag, w = cs["geometry"](2, nq); mps, _ = cs["maximal_partial_spreads"](lag)
    S = next(sorted(S) for S in mps if len(S) == size); C = frozenset().union(*[lag[L] for L in S])
    U = [i for i in range(len(pts)) if i not in C]
    for k in ks:
        r = cover(U, lambda a, b: w(pts[a], pts[b]) == 1, k, tl=600); r.pop("classes", None)
        out["n%d_size%d_k%d" % (nq, size, k)] = r; print(nq, size, r, flush=True)
# four qubits: the saved size-9 set
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags, w4 = ex["lags"], ex["w"]
sol = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_theta_exact.json")))["lines"]
C = frozenset().union(*[lags[i] for i in sol]); U = [x for x in range(1, 256) if x not in C]
r = cover(U, lambda a, b: w4(a, b) == 1, 14, tl=2400)
out["n4_size9_k14"] = r
print(4, 9, {k: v for k, v in r.items() if k != "classes"}, flush=True)
if r.get("verified"):
    out["n4_conclusion"] = "sum_U <P>^2 <= 14 exactly (14 anticommuting classes) => F >= 1/16 |v|^4 for all v in C^16; attained (alpha = 14): min F = 1/16 exactly"
json.dump(out, open(os.path.join(ROOT, "data", "w33_anticommuting_clique_cover.json"), "w"), indent=1)
