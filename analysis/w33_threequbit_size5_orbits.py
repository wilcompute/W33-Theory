"""Item 2 support: all size-5 maximal partial spreads of the three-qubit dual polar geometry (Sp(6,2) Lagrangians, 135 lines);
count them, split by an invariant (covered-point count multiset of pairwise intersections + numeric min F), so the degree-6 SOS can be run
on one representative of each type.  usage: py -3 analysis/w33_threequbit_size5_orbits.py"""
import itertools, json, os
from collections import Counter
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
exec(_src[: _src.index("\nres = {}")], cs)
pts, lag, w = cs["geometry"](2, 3); B = cs["bases_for"](2, 3, pts, lag); mps, _ = cs["maximal_partial_spreads"](lag)
sizes = Counter(len(S) for S in mps)
five = [sorted(S) for S in mps if len(S) == 5]
def inv(S):
    # for each non-covered Lagrangian: number of chosen Lagrangians it meets in a 2-dim / 1-dim subspace -> histogram
    lagsets = [frozenset(L) if not isinstance(L, frozenset) else L for L in lag]
    cov = frozenset().union(*[frozenset(lag[i]) for i in S])
    return (len(cov), tuple(sorted(Counter(len(frozenset(lag[j]) & cov) for j in range(len(lag)) if j not in S).items())))
types = Counter(inv(S) for S in five)
rng = np.random.default_rng(3); d = 8
def Fmin(S):
    E = [b for L in S for b in B[L].T]
    def Fn(z):
        v = z[:d] + 1j * z[d:]; v = v / np.linalg.norm(v)
        return sum((np.vdot(v, (np.outer(e, e.conj()) - np.eye(d) / d) @ v).real) ** 2 for e in E)
    return min(minimize(Fn, rng.standard_normal(2 * d), method="BFGS").fun for _ in range(30))
reps = {}
for S in five:
    k = inv(S)
    if k not in reps: reps[k] = S
res = dict(maximal_sizes=dict(sorted(sizes.items())), n_size5=len(five), n_types=len(types),
           types=[dict(invariant=str(k), count=types[k], rep=reps[k], numeric_min_F=float(Fmin(reps[k]))) for k in types])
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_size5_orbits.json"), "w"), indent=1)
