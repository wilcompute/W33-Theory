"""Pass 12643: stabiliser value (p-1) m*/d versus numerical min F for the d = 25 uniform covers (m* = min over lines M of |M cap C|).
Regenerates the same ILP covers as w33_minF_covered_points.py (same exclusion order).  usage: py -3 analysis/w33_ququint_stabiliser_value.py"""
import json, os, contextlib, io
from collections import Counter
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
qs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_ququint_sentinel_search.py")}
_src = open(os.path.join(HERE, "w33_ququint_sentinel_search.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("res = {}")], qs)
p = 5; pts, lag, w = qs["geometry"](p, 2); mf = json.load(open(os.path.join(ROOT, "data", "w33_minF_covered_points.json")))
res = {}
for m in (2, 1):
    ex = []
    for k in range(2):
        with contextlib.redirect_stdout(io.StringIO()):
            r = qs["search"](p, m, exclude=tuple(ex))
        lines = r["lines"]; ex.append(lines)
        C = frozenset().union(*[lag[L] for L in lines])
        meet = Counter(len(set(lag[M]) & C) for M in range(len(lag)) if M not in lines)
        ms = min(meet); sv = Fr((p - 1) * ms, 25); key = "d25_m%d_cover%d" % (m, k)
        res[key] = dict(meeting_histogram=dict(sorted(meet.items())), m_star=ms, stabiliser_value=str(sv), min_F=mf[key]["min_F"], min_F_equals_stabiliser=abs(mf[key]["min_F"] - float(sv)) < 1e-6)
        print(key, res[key], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_ququint_stabiliser_value.json"), "w"), indent=1)
