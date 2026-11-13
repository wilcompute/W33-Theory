"""Pass 12650 item 2: upper bounds on the smallest maximal partial spread of W(2n-1,2) for n = 4, 5 by randomised greedy rank codes.
Through the X/Z Lagrangian pair, add random nonsingular symmetric S compatible (S + S_i nonsingular) with those chosen, until none is
compatible; the spread then has size k + 2 and is maximal automatically.  Size distribution over many runs; the smallest size found is
an upper bound (lower bounds: n = 4 exactly 5, Pass 12648; n = 5 >= 8, Pass 12649).  Also a biased variant that prefers matrices
covering many uncovered T (greedy set cover), which tends to find small maximal spreads.
usage: py -3 analysis/w33_rank_code_greedy_sizes.py"""
import json, os, time
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_symmetric_rank_code_spreads.py")}
src = open(os.path.join(HERE, "w33_symmetric_rank_code_spreads.py"), encoding="utf-8").read()
exec(src[: src.index("def code_of")], g)
setup = g["setup"]
def greedy(n, runs, biased, seed, tlimit):
    pos, sing, alt, ns = setup(n); rng = np.random.default_rng(seed); sizes = Counter(); best = None; t0 = time.time()
    for r in range(runs):
        if time.time() - t0 > tlimit: break
        chosen = []; avail = np.ones(len(ns), bool); covered = np.zeros(len(ns), bool)
        while avail.any():
            idx = np.flatnonzero(avail)
            if biased and len(idx) > 1:
                sub = idx if len(idx) <= 400 else rng.choice(idx, 400, replace=False)
                gains = np.array([(sing[ns ^ ns[i]] & ~covered).sum() for i in sub])
                top = sub[gains >= gains.max() - (1 if rng.random() < 0.5 else 0)]
                i = int(rng.choice(top))
            else:
                i = int(rng.choice(idx))
            c = ns[i]; chosen.append(int(c)); covered |= sing[ns ^ c]; avail &= ~sing[ns ^ c]
        k = len(chosen) + 2; sizes[k] += 1
        if best is None or k < len(best) + 2: best = chosen
    return dict(n=n, biased=biased, runs=sum(sizes.values()), sizes=dict(sorted(sizes.items())), smallest=min(sizes), example=best)
res = {}
for n, runs, tl in [(4, 2000, 300), (5, 3000, 1500)]:
    for biased in (False, True):
        r = greedy(n, runs, biased, 50 + n, tl); res["n%d_%s" % (n, "biased" if biased else "random")] = r
        print({k: v for k, v in r.items() if k != "example"}, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_rank_code_greedy_sizes.json"), "w"), indent=1)
