"""Pass 12649 item 3: a structural route to min F = 1/8 for three qubits.  F = (7 - sum_U <P>^2)/8; need sum_U <P>^2 <= 6.
Condition on the distinguished uncovered Pauli P0 (the 1-vertex class of the coherent closure, Pass 12643): f(t) = max sum_U <P>^2
over pure states with <P0> = t (penalty method, many starts).  Report f on a grid, where the maximum 6 is attained (t values), and the
split sum_U = t^2 + sum_A + sum_B (A: anticommute with P0, B: commute) at the optimum for each t.
usage: py -3 analysis/w33_threequbit_conditioning_profile.py"""
import json, os, contextlib, io, itertools
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_s = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_s[: _s.index(chr(10) + "res = {}")], cs)
pts, lag, w = cs["geometry"](2, 3); mps, _ = cs["maximal_partial_spreads"](lag)
S = next(sorted(S) for S in mps if len(S) == 5); C = frozenset().union(*[lag[L] for L in S]); U = [i for i in range(63) if i not in C]
idx = {tuple(p): i for i, p in enumerate(pts)}
add = lambda a, b: idx[tuple((x + y) % 2 for x, y in zip(pts[a], pts[b]))]
def inv(u):
    nb = [v for v in U if v != u and w(pts[u], pts[v]) == 1]
    return (sum(1 for a, b in itertools.combinations(nb, 2) if w(pts[a], pts[b]) == 1), sum(1 for v in nb if add(u, v) in C))
p0 = next(u for u in U if inv(u) == (36, 0))
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(a):
    M = np.eye(1)
    for i in range(3):
        x, z = a[i], a[3 + i]
        M = np.kron(M, (1j) ** (x * z) * np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z))
    return M
P0 = pauli(pts[p0]); A = [u for u in U if u != p0 and w(pts[u], pts[p0]) == 1]; Bc = [u for u in U if u != p0 and w(pts[u], pts[p0]) == 0]
PA = np.array([pauli(pts[u]) for u in A]); PB = np.array([pauli(pts[u]) for u in Bc])
def parts(v):
    e = lambda Ps: np.einsum("i,kij,j->k", v.conj(), Ps, v).real
    return float(np.vdot(v, P0 @ v).real), float(np.sum(e(PA) ** 2)), float(np.sum(e(PB) ** 2))
rng = np.random.default_rng(9); grid = np.linspace(0, 1, 11); rows = []
for t in grid:
    def obj(z):
        v = z[:8] + 1j * z[8:]; v = v / np.linalg.norm(v); a, sa, sb = parts(v)
        return -(a * a + sa + sb) + 200 * (a - t) ** 2
    best = min((minimize(obj, rng.standard_normal(16), method="BFGS") for _ in range(30)), key=lambda r: r.fun)
    v = best.x[:8] + 1j * best.x[8:]; v /= np.linalg.norm(v); a, sa, sb = parts(v)
    rows.append(dict(t=float(t), t_achieved=a, total=a * a + sa + sb, sum_A=sa, sum_B=sb)); print(rows[-1], flush=True)
res = dict(p0=list(pts[p0]), n_A=len(A), n_B=len(Bc), profile=rows)
json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_conditioning_profile.json"), "w"), indent=1)
