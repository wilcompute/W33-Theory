"""Pass 12648: are the two size-5 types of W(7,2) lifts of three-qubit five-sets?  For an uncovered point p, the quotient p^perp/<p>
is W(5,2); each Lagrangian L (p not in L) gives the 3-space (L cap p^perp) whose image is a quotient Lagrangian.  Count points p for
which the five images are pairwise disjoint and form a MAXIMAL partial spread of the quotient (every quotient Lagrangian = M/<p> with
p in M meets their union).  Type B (count 56 through a fixed pair, same as the three-qubit count) is predicted to have such p.
usage: py -3 analysis/w33_four_qubit_type_lift.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py")}
src = open(os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py"), encoding="utf-8").read()
exec(src[: src.index("def decide")], ex)
lags, NV = ex["lagrangians"](4); n = 4; lo = 15
w = lambda x, y: (bin((x & lo) & (y >> n)).count("1") + bin((x >> n) & (y & lo)).count("1")) % 2
census = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_size5_census.json")))
out = []
for t in census["types"]:
    S = t["example"]; C = frozenset().union(*[lags[i] for i in S]); good = []
    for p in range(1, NV):
        if p in C: continue
        imgs = []
        for i in S:
            cos = frozenset(frozenset((x, x ^ p)) for x in lags[i] if w(x, p) == 0)
            imgs.append(cos)
        if any(len(a & b) for k, a in enumerate(imgs) for b in imgs[k + 1:]): continue
        union = frozenset().union(*imgs)
        qlags = [frozenset(frozenset((x, x ^ p)) for x in M if x != p) for M in lags if p in M]
        if all(len(q & union) > 0 for q in qlags): good.append(p)
    row = dict(n_inside=t["n_inside"], n_partitions=t["n_partitions"], theta=t["theta"], lift_points=len(good))
    out.append(row); print(row, flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_four_qubit_type_lift.json"), "w"), indent=1)
