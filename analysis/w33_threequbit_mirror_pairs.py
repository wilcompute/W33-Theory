"""Pass 12643 item 4: chirality one rung down.  Group the 24,192 three-qubit size-5 maximal partial spreads (W(5,2), 7-point Lagrangian
lines) by covered point set.  If two sets share their 35 covered points, their second moments agree (twirl identity) and any difference
is at higher order.  Report the fibre sizes, collinear-pair overlaps (pairs of points on a common chosen line) and, for a fibre with >= 2
sets, the optimal third-moment witness max_v sum_L p^3 - sum_R p^3 (with a stabiliser-state check).  Control: the two-qutrit codewords
(fibres of size 2, 0 shared collinear pairs, witness 16/27, Pass 12642).
usage: py -3 analysis/w33_threequbit_mirror_pairs.py"""
import itertools, json, os, contextlib, io
from collections import Counter
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("\nres = {}")], cs)
def analyse(p, n, size, witness=True):
    pts, lag, w = cs["geometry"](p, n); B = cs["bases_for"](p, n, pts, lag); mps, _ = cs["maximal_partial_spreads"](lag)
    sets = [tuple(sorted(S)) for S in mps if len(S) == size]
    fib = {}
    for S in sets:
        fib.setdefault(frozenset().union(*[lag[L] for L in S]), []).append(S)
    out = dict(n_sets=len(sets), n_covered_sets=len(fib), fibre_sizes=dict(Counter(len(v) for v in fib.values())))
    pairs = lambda S: {frozenset(pr) for L in S for pr in itertools.combinations(sorted(lag[L]), 2)}
    big = next((v for v in fib.values() if len(v) >= 2), None)
    if big is None:
        return out
    ov = Counter(len(pairs(a) & pairs(b)) for a, b in itertools.combinations(big, 2))
    out["collinear_pairs_per_set"] = len(pairs(big[0])); out["pair_overlaps_in_a_fibre"] = dict(ov)
    out["lines_shared_in_a_fibre"] = dict(Counter(len(set(a) & set(b)) for a, b in itertools.combinations(big, 2)))
    if witness:
        d = p ** n; L, R = big[0], big[1]
        EL = [e for x in L for e in B[x].T]; ER = [e for x in R for e in B[x].T]
        def D(z):
            v = z[:d] + 1j * z[d:]; v = v / np.linalg.norm(v)
            return sum(abs(np.vdot(e, v)) ** 6 for e in EL) - sum(abs(np.vdot(e, v)) ** 6 for e in ER)
        rng = np.random.default_rng(5)
        out["max_witness"] = float(max(-minimize(lambda z: -D(z), rng.standard_normal(2 * d), method="BFGS").fun for _ in range(30)))
        out["witness_on_left_stabiliser_states"] = sorted(set(np.round([D(np.concatenate([e.real, e.imag])) for e in EL], 9)))
        out["second_moment_diff"] = float(max(abs(sum(abs(np.vdot(e, v)) ** 4 for e in EL) - sum(abs(np.vdot(e, v)) ** 4 for e in ER))
                                              for v in [x / np.linalg.norm(x) for x in rng.standard_normal((5, d)) + 1j * rng.standard_normal((5, d))]))
    return out
res = {"control_two_qutrit_pentads": analyse(3, 2, 5)}
print("control:", res["control_two_qutrit_pentads"], flush=True)
res["three_qubit_size5"] = analyse(2, 3, 5)
print("three qubits:", res["three_qubit_size5"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_mirror_pairs.json"), "w"), indent=1, default=str)
