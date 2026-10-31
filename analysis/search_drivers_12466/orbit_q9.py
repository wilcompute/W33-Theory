"""12496: size of the PSp(4,9)-orbit of the 48-line even set (BFS under random products of symplectic transvections, hashed, capped):
|stabiliser| = |PSp(4,9)| / |orbit| if the generators generate PSp(4,9) and the cap is not reached.  usage: py -3 orbit_q9.py cap"""
import sys, json, random
import numpy as np
from symmetric_fast import fast_build
from symmetric_even_sets_gf import setup

q = 9; cap = int(sys.argv[1]) if len(sys.argv) > 1 else 400000
pts, lines = fast_build(q); F, add, mul, inv, neg = setup(q)
pid = {p: i for i, p in enumerate(pts)}; lid = {L: j for j, L in enumerate(lines)}


def w(u, v):
    s = add[mul[u[0]][v[2]]][mul[u[1]][v[3]]]
    return add[s][neg[add[mul[u[2]][v[0]]][mul[u[3]][v[1]]]]]


def transvection(a, lam):
    def f(x):
        c = mul[lam][w(x, a)]
        v = tuple(add[x[i]][mul[c][a[i]]] for i in range(4))
        s = inv[next(t for t in v if t)]
        return pid[tuple(mul[s][t] for t in v)]
    return np.array([f(x) for x in pts])


rng = random.Random(3)
gens = []
for _ in range(4):                                   # products of 3 random transvections
    perm = np.arange(len(pts))
    for _ in range(3):
        t = transvection(rng.choice(pts), rng.randrange(1, q)); perm = t[perm]
    gens.append(np.array([lid[tuple(sorted(perm[x] for x in L))] for L in lines]))
rec = json.load(open("symmetric_fast_q9_r10.json"))[0]
start = np.array(sorted(rec["chosen"]))
seen = {hash(start.tobytes())}; frontier = [start]
while frontier and len(seen) < cap:
    nxt = []
    for S in frontier:
        for g in gens:
            T = np.sort(g[S]); h = hash(T.tobytes())
            if h not in seen:
                seen.add(h); nxt.append(T)
    frontier = nxt
order = q ** 4 * (q * q - 1) * (q ** 4 - 1) // 2
out = dict(orbit=len(seen), capped=len(seen) >= cap, PSp49=order, stabiliser=order // len(seen) if len(seen) < cap else None,
           divides=order % len(seen) == 0 if len(seen) < cap else None)
print(json.dumps(out)); json.dump(out, open("orbit_q9.json", "w"))
