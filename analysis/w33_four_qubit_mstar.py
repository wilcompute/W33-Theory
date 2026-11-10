"""Pass 12644: for the saved four-qubit size-9 set, the meeting histogram of the other Lagrangians with the covered set C (m* = 1 means a
stabiliser state attains F = 1/16), plus maximality re-check (every Lagrangian meets C) and disjointness of the 9 classes.
usage: py -3 analysis/w33_four_qubit_mstar.py"""
import json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags = ex["lags"]; sol = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_theta_exact.json")))["lines"]
C = frozenset().union(*[lags[i] for i in sol])
hist = Counter(len(lags[i] & C) for i in range(len(lags)) if i not in sol)
res = dict(disjoint=len(C) == 15 * len(sol), maximal=min(hist) >= 1, meeting_histogram=dict(sorted(hist.items())), m_star=min(hist), stabiliser_value="%d/16" % min(hist))
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_four_qubit_mstar.json"), "w"), indent=1)
