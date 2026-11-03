"""12526 follow-up: structured subsets of the 36 double-sixes.  For the stabiliser of a point, a line, a sentinel, a frame, a spread, a codeword: its orbits on the 36; every union of orbits is tested for rank 24, tightness on E_2, and exact detection of the 160 collinear triples by the cubic moment.  usage: py -3 tomography_orbits.py"""
import collections, itertools, json, runpy
import numpy as np
ns = runpy.run_path("simplex_frame.py")
Z_groups, pts, lines, w, group, T, compose, codewords = (ns[k] for k in ("Z_groups", "pts", "lines", "w", "group", "T", "compose", "codewords"))
P = list(group([T(pts[i]) for i in range(40)])); sets = [frozenset(L) for L in lines]
key = {}
for d, g in enumerate(Z_groups):
    for r in g: key[tuple(r.tolist())] = d
def act36(p):
    out = []
    for g in Z_groups:
        r = g[0]; n = np.zeros(40, dtype=np.int64); n[list(p)] = r; out.append(key[tuple(n.tolist())])
    return tuple(out)
acts = {p: act36(p) for p in P}
tri = list(itertools.combinations(range(40), 3)); col = np.array([any(set(t) <= L for L in sets) for t in tri]); ta, tb, tc = [np.array(x) for x in zip(*tri)]
E = np.linalg.svd(np.vstack(Z_groups).astype(float), full_matrices=False)[2][:24].T
def test(idx):
    Z = np.vstack([Z_groups[i] for i in idx]); t = (Z[:, ta] * Z[:, tb] * Z[:, tc]).sum(0)
    ev = np.linalg.eigvalsh(E.T @ (Z.T @ Z).astype(float) @ E)
    return dict(k=len(idx), rank=int(np.linalg.matrix_rank(Z)), tight=bool(ev.max() - ev.min() < 1e-8), detects=bool(np.all(t[col] == t[col][0]) and t[~col].max() < t[col][0]))
fixed = {
 "point": lambda p: p[0] == 0,
 "line": lambda p: frozenset(p[x] for x in sets[0]) == sets[0],
 "spread_of_double_six_0": lambda p: acts[p][0] == 0,
 "codeword": lambda p: frozenset(p[x] for x in set().union(*(sets[j] for j in codewords[0]))) == frozenset().union(*(sets[j] for j in codewords[0])),
}
out = {}
for name, f in fixed.items():
    H = [p for p in P if f(p)]; left = set(range(36)); orbs = []
    while left:
        i = min(left); o = {acts[p][i] for p in H}; orbs.append(sorted(o)); left -= o
    rec = dict(order=len(H), orbits=sorted(len(o) for o in orbs), unions=[])
    for r in range(1, len(orbs) + 1):
        for c in itertools.combinations(range(len(orbs)), r):
            idx = sorted(i for t in c for i in orbs[t])
            if len(idx) == 36: continue
            d = test(idx); d["orbit_sizes"] = sorted(len(orbs[t]) for t in c); rec["unions"].append(d)
    out[name] = rec; print(name, rec["order"], rec["orbits"], [ (u["k"], u["rank"], u["tight"], u["detects"]) for u in rec["unions"]][:16], flush=True)
json.dump(out, open("tomography_orbits.json", "w"), indent=1)
