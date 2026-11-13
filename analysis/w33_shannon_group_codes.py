"""Pass 12658: codes in W(3,3) strong-square invariant under NON-cyclic diagonal groups <(g,g), (h,h)> (optionally with a twist
automorphism on the second coordinate: (g, c g c^-1)).  Random 2-generator subgroups of Aut(G) of order <= 240 are sampled; the orbit
CSP is solved to optimality.  Reports the best size per group order and the stabiliser-size data of the 60-code's symmetry class.
usage: py -3 analysis/w33_shannon_group_codes.py [n_groups] [sec]"""
import itertools, json, os, sys, time
from collections import defaultdict
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_shannon_symmetric_codes.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_shannon_symmetric_codes.py")}
argv = sys.argv; sys.argv = ["x", "30", "4"]; exec(src[: src.index("results = []; best")], g); sys.argv = argv
adj = g["adj"]; comp = lambda p, q: tuple(p[q[i]] for i in range(40)); inv = lambda p: tuple(int(i) for i in np.argsort(p))
ng = int(sys.argv[1]) if len(sys.argv) > 1 else 60; sec = float(sys.argv[2]) if len(sys.argv) > 2 else 20
rng = np.random.default_rng(5)
def group(gens, cap=241):
    idp = tuple(range(40)); seen = {idp}; fr = [idp]
    while fr:
        nx = []
        for x in fr:
            for s in gens:
                y = comp(s, x)
                if y not in seen:
                    seen.add(y); nx.append(y)
                    if len(seen) > cap: return None
        fr = nx
    return seen
best = defaultdict(int); runs = []; t0 = time.time(); top = (0, None)
tries = 0
while len(runs) < ng and tries < 4000:
    tries += 1
    a, b = g["random_element"](int(rng.integers(2, 9))), g["random_element"](int(rng.integers(2, 9)))
    k1, k2 = g["order"](a), g["order"](b)
    a = g["power"](a, k1 // int(rng.choice([p for p in (2, 3, 5) if k1 % p == 0]))) if k1 > 1 else a
    b = g["power"](b, k2 // int(rng.choice([p for p in (2, 3, 5) if k2 % p == 0]))) if k2 > 1 else b
    H = group([a, b])
    if H is None or len(H) < 6: continue
    for twist in (False, True):
        c = g["random_element"]() if twist else tuple(range(40))
        a2, b2 = comp(c, comp(a, inv(c))), comp(c, comp(b, inv(c)))
        orbs = g["orbits_of"](40, [lambda q, a=a, a2=a2: (a[q[0]], a2[q[1]]), lambda q, b=b, b2=b2: (b[q[0]], b2[q[1]])])
        size, bd, st, S, ngood = g["solve_orbits"](40, adj, orbs, sec, 4)
        runs.append(dict(group_order=len(H), twist=twist, size=size, bound=bd, status=st))
        best[len(H)] = max(best[len(H)], size)
        if size > top[0]: top = (size, S, runs[-1]); print("best so far", runs[-1], round(time.time() - t0), "s", flush=True)
out = dict(n_runs=len(runs), best_by_group_order={str(k): v for k, v in sorted(best.items())}, best_size=top[0], best_record=top[2], best_set=top[1], runs=runs)
print(out["best_by_group_order"], "BEST", top[0], flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_shannon_group_codes.json"), "w"), indent=1, default=int)
