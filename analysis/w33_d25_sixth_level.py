"""Pass 12646 item 4: geometry of the level |<W_u>| = 1/6 in the d = 25 single-cover optimiser.  Are the 144 vectors unions of whole
points (all 4 nonzero multiples)?  How many points, how they meet the 14 covered lines, whether they are pairwise commuting / form lines,
and whether the level value 1/6 is exact to the optimiser's precision.
usage: py -3 analysis/w33_d25_sixth_level.py"""
import json, os, contextlib, io, itertools
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
st = {"__name__": "x", "__file__": os.path.join(HERE, "w33_d25_optimiser_structure.py")}
src = open(os.path.join(HERE, "w33_d25_optimiser_structure.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index(chr(10) + "res = {}")], st)
weyl, polish = st["weyl"], st["polish"]
qs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_ququint_sentinel_search.py")}
s2 = open(os.path.join(HERE, "w33_ququint_sentinel_search.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(s2[: s2.index("res = {}")], qs)
p = 5; pts, lag, w = qs["geometry"](p, 2)
with contextlib.redirect_stdout(io.StringIO()):
    r = qs["search"](p, 1)
lines = r["lines"]; cov = sorted(frozenset().union(*[lag[L] for L in lines]))
f, v = polish(p, 2, pts, cov, 30, 2)
norm = lambda u: (lambda c: tuple((x * pow(c, -1, p)) % p for x in u))(next(x for x in u if x))
idx = {q: i for i, q in enumerate(pts)}
vals = {u: abs(np.vdot(v, weyl(p, 2, u) @ v)) for u in itertools.product(range(p), repeat=4) if any(u)}
lvl = [u for u, a in vals.items() if abs(a - 1 / 6) < 1e-5]
err = max(abs(vals[u] - 1 / 6) for u in lvl)
P6 = Counter(idx[norm(u)] for u in lvl)
whole = all(c == 4 for c in P6.values())
pts6 = sorted(P6); covset = set(cov)
on_cov = sum(1 for q in pts6 if q in covset)
per_line_cov = Counter(len(set(lag[L]) & set(pts6)) for L in lines)
comm = Counter(w(pts[a], pts[b]) == 0 for a, b in itertools.combinations(pts6, 2))
lines_in = sum(1 for L in range(len(lag)) if set(lag[L]) <= set(pts6))
res = dict(min_F=f, n_vectors=len(lvl), max_dev_from_one_sixth=float(err), n_points=len(pts6), whole_points=whole, points_on_covered=on_cov,
           per_covered_line_intersections=dict(sorted(per_line_cov.items())), commuting_pairs=comm[True], anticommuting_pairs=comm[False], full_lines_inside=lines_in)
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_d25_sixth_level.json"), "w"), indent=1)
