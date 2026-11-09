"""Do the 15 splits forming the S6 transpositions (w33_sentinel_identity.py) equal the 15 splits whose factors the codeword's Kramers reversal swaps?
theta ranges over the 36 fixed-point-free outer involutions of PGSp(4,3) on the 40 points (P12523: the Kramers reversals).
usage: py -3 analysis/w33_doily_s6_kramers.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sb = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12635_burkhardt_fan.py")}
exec(open(os.path.join(HERE, "w33_pass12635_burkhardt_fan.py"), encoding="utf-8").read().split("res = dict(")[0], sb)
P, splits, w = sb["P"], sb["splits"], sb["w"]
idx = {p: i for i, p in enumerate(P)}
norm = lambda v: next(tuple((x * pow(c, -1, 3)) % 3 for x in v) for c in v if c)
gens = [tuple(idx[norm(tuple((x + w(p, v) * vi) % 3 for x, vi in zip(p, v)))] for p in P) for v in P]
group = {tuple(range(40))}; frontier = [tuple(range(40))]
while frontier:
    new = []
    for g in frontier:
        for h in gens:
            k = tuple(h[g[i]] for i in range(40))
            if k not in group: group.add(k); new.append(k)
    frontier = new
g0 = tuple(idx[norm((p[0], p[1], (-p[2]) % 3, (-p[3]) % 3))] for p in P)
outer = {tuple(g0[g[i]] for i in range(40)) for g in group}
sid = json.load(open(os.path.join(ROOT, "data", "w33_sentinel_identity.json")))
fifteen = set(sid["fifteen_splits"])
thetas = [g for g in outer if all(g[g[i]] == i for i in range(40)) and all(g[i] != i for i in range(40))]
best = []
for th in thetas:
    swapped = {s for s, (b, bp) in enumerate(splits) if frozenset(th[p] for p in b) == bp}
    best.append((len(swapped & fifteen), len(swapped), swapped == fifteen))
hits = [b for b in best if b[2]]
res = dict(n_theta=len(thetas), exact_matches=len(hits), max_overlap=max(b[0] for b in best), swapped_sizes=sorted({b[1] for b in best}))
print("fixed-point-free outer involutions:", len(thetas), "| thetas whose swapped splits = the S6 fifteen:", len(hits), "| max overlap", res["max_overlap"], "| swapped sizes", res["swapped_sizes"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_doily_s6_kramers.json"), "w"), indent=1)
