"""Pass 12644: (a) Lovasz theta for the saved four-qubit size-9 set (SCS); (b) Tabucol search for a 14-colouring of the commutation graph on
the 120 uncovered Paulis (each colour class pairwise anticommuting => sum over class of <P>^2 <= 1), giving the elementary bound
sum_U <P>^2 <= 14 and F >= 1/16 exactly.  A found colouring is re-verified independently and saved.
usage: py -3 analysis/w33_four_qubit_tabucol.py"""
import json, os, itertools, time
import numpy as np, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags, w = ex["lags"], ex["w"]
sol = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_theta_exact.json")))["lines"]
C = frozenset().union(*[lags[i] for i in sol]); U = [x for x in range(1, 256) if x not in C]; n = len(U)
ANTI = np.array([[w(U[a], U[b]) == 1 for b in range(n)] for a in range(n)])
COMM = (~ANTI) & ~np.eye(n, dtype=bool)
X = cp.Variable((n, n), symmetric=True)
E = [(a, b) for a, b in itertools.combinations(range(n), 2) if ANTI[a, b]]
pr = cp.Problem(cp.Maximize(cp.sum(X)), [X >> 0, cp.trace(X) == 1] + [X[a, b] == 0 for a, b in E]); pr.solve(solver=cp.SCS, eps=1e-8, max_iters=100000)
theta = float(pr.value); print("theta(saved set) =", theta, flush=True)
def tabucol(k, iters=400000, seed=0):
    rng = np.random.default_rng(seed); c = rng.integers(0, k, n)
    adj = COMM.astype(np.int64)
    M = np.zeros((n, k), np.int64)  # M[v, col] = number of commuting neighbours of v with colour col
    for v in range(n): M[v] = np.bincount(c[adj[v].astype(bool)], minlength=k)
    conf = int(sum(M[v, c[v]] for v in range(n)) // 2); best = conf; tabu = np.zeros((n, k), np.int64)
    for it in range(iters):
        if conf == 0: return c
        bad = np.where(M[np.arange(n), c] > 0)[0]
        delta = M[bad] - M[bad, c[bad]][:, None]
        delta[np.arange(len(bad)), c[bad]] = 10 ** 9
        allowed = (tabu[bad] <= it) | (conf + delta < best)
        delta = np.where(allowed, delta, 10 ** 9)
        i = np.unravel_index(np.argmin(delta + rng.random(delta.shape) * 0.5), delta.shape)
        v, col = bad[i[0]], i[1]
        if delta[i] >= 10 ** 9: continue
        old = c[v]; nb = np.where(adj[v])[0]
        M[nb, old] -= 1; M[nb, col] += 1
        conf += int(delta[i]); c[v] = col
        tabu[v, old] = it + 7 + int(0.6 * len(bad)) + rng.integers(0, 10)
        best = min(best, conf)
    return None
t = time.time(); found = None
for seed in range(40):
    found = tabucol(14, seed=seed)
    if found is not None: break
el = time.time() - t
res = dict(theta=theta, k=14, found=found is not None, seconds=el)
if found is not None:
    classes = [[U[v] for v in range(n) if found[v] == col] for col in range(14)]
    ok = sorted(x for cl in classes for x in cl) == sorted(U) and all(w(a, b) == 1 for cl in classes for a, b in itertools.combinations(cl, 2))
    res.update(verified=ok, class_sizes=sorted(len(cl) for cl in classes), classes=classes, seed=seed,
               conclusion="sum_U <P>^2 <= 14 (14 pairwise-anticommuting classes) => F >= |v|^4/16 for all v in C^16; attained (m* = 1) => min F = 1/16 exactly" if ok else "verification failed")
print({k_: v for k_, v in res.items() if k_ != "classes"}, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_four_qubit_tabucol.json"), "w"), indent=1)
