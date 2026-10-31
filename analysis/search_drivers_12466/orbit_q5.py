"""12484 addendum: stabiliser in PSp(4,5) of the Petersen-structured minimum even line set (orbit by BFS under transvections;
|PSp(4,5)| = 4,680,000).  usage: py -3 orbit_q5.py"""
import json
from even_line_sets_gf import build

q = 5
pts, lines, N = build(q)
pid = {p: i for i, p in enumerate(pts)}
w = lambda u, v: (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % q


def norm(v):
    f = next(x for x in v if x); s = pow(f, -1, q)
    return tuple(x * s % q for x in v)


lid = {frozenset(l): j for j, l in enumerate(lines)}
lgens = []
for a in pts:
    perm = [pid[norm(tuple((x[c] + w(x, a) * a[c]) % q for c in range(4)))] for x in pts]
    lgens.append([lid[frozenset(perm[x] for x in l)] for l in lines])
r = json.load(open("even_line_sets_gf_q5.json"))
start = frozenset(lid[frozenset(pid[tuple(p)] for p in l)] for l in r["chosen_lines"])
orbit = {start}; frontier = [start]
while frontier:
    nxt = []
    for S in frontier:
        for g in lgens:
            T = frozenset(g[j] for j in S)
            if T not in orbit:
                orbit.add(T); nxt.append(T)
    frontier = nxt
out = dict(orbit_size=len(orbit), stabiliser_order=4680000 // len(orbit), divides=4680000 % len(orbit) == 0)
print(json.dumps(out)); json.dump(out, open("orbit_q5.json", "w"))
