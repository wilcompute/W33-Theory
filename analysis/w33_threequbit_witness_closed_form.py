"""Pass 12643: closed form of the three-qubit mirror witness 9/16.  For a left line L and a right line L', |L cap L'| in points is
0, 1 or 3 (vector dim 0, 1, 2); a stabiliser state of L scores sum p^3 = (2^k/8)^2 on the basis of L'.  Check the meeting pattern
for every left line of every fibre (all 12,096 pairs) and the resulting value 1 + 4*8/8^3 - sum_R.
usage: py -3 analysis/w33_threequbit_witness_closed_form.py"""
import json, os, contextlib, io
from collections import Counter
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("\nres = {}")], cs)
pts, lag, w = cs["geometry"](2, 3); mps, _ = cs["maximal_partial_spreads"](lag)
fib = {}
for S in mps:
    if len(S) == 5: fib.setdefault(frozenset().union(*[lag[L] for L in S]), []).append(sorted(S))
pat = Counter(); vals = Counter()
val = {0: Fr(1, 64), 1: Fr(1, 16), 3: Fr(1, 4)}
for v in fib.values():
    for A, Bs in ((v[0], v[1]), (v[1], v[0])):
        for L in A:
            m = tuple(sorted(len(set(lag[L]) & set(lag[R])) for R in Bs)); pat[m] += 1
            vals[str(1 + Fr(4 * 8, 512) - sum(val[k] for k in m))] += 1
res = dict(meeting_patterns={str(k): c for k, c in pat.items()}, witness_values=dict(vals))
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_witness_closed_form.json"), "w"), indent=1)
