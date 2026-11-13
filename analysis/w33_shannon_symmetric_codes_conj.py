"""Pass 12655 addendum: (1) independent verification of the best symmetric code of w33_shannon_symmetric_codes.py on a separately
built W(3) (different form/enumeration, GQ axiom, VF2 isomorphism); (2) wider search: codes invariant under <(g, c g^a c^-1)> for
random conjugators c (order-5 and order-3 elements), which includes non-diagonal embeddings.  usage: py -3 analysis/w33_shannon_symmetric_codes_conj.py [n_conj] [sec]"""
import itertools, json, os, sys, time
import numpy as np, networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_shannon_symmetric_codes.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_shannon_symmetric_codes.py")}
sys_argv = sys.argv; sys.argv = ["x", "60", "4"]
exec(src[: src.index("results = []; best")], g)
sys.argv = sys_argv
adj, pts = g["adj"], g["pts"]
G1 = nx.from_numpy_array(np.array(adj))
# independent W(3)
pts2 = sorted({min(tuple((c * x) % 3 for x in v) for c in (1, 2)) for v in itertools.product(range(3), repeat=4) if any(v)}, reverse=True)
om2 = lambda a, b: (a[0] * b[1] - a[1] * b[0] + a[2] * b[3] - a[3] * b[2]) % 3
G2 = nx.Graph(); G2.add_nodes_from(range(40)); G2.add_edges_from((i, j) for i, j in itertools.combinations(range(40), 2) if om2(pts2[i], pts2[j]) == 0)
cl = list(nx.find_cliques(G2)); assert len(cl) == 40 and all(len(c) == 4 for c in cl)
for p in range(40):
    for L in cl:
        if p not in L: assert sum(1 for x in L if G2.has_edge(p, x)) == 1
iso = nx.vf2pp_isomorphism(G1, G2); assert iso is not None
def verify(S):
    T = [(iso[u], iso[v]) for u, v in S]; close = lambda a, b: a == b or G2.has_edge(a, b)
    return len(set(T)) == len(T) and not any(close(x[0], y[0]) and close(x[1], y[1]) for x, y in itertools.combinations(T, 2))
d = json.load(open(os.path.join(ROOT, "data", "w33_shannon_symmetric_codes.json")))
S0 = [tuple(x) for x in d["best_set"]]
out = dict(base_size=len(S0), base_verified_independently=verify(S0), runs=[])
print("base code", len(S0), "independently verified:", out["base_verified_independently"], flush=True)
nconj = int(sys.argv[1]) if len(sys.argv) > 1 else 30; sec = float(sys.argv[2]) if len(sys.argv) > 2 else 40
best = (len(S0), S0); t0 = time.time(); rng = np.random.default_rng(11)
elems = g["elems"]; power = g["power"]
inv = lambda p: tuple(int(i) for i in np.argsort(p))
comp = lambda p, q: tuple(p[q[i]] for i in range(40))
for key in [k for k in elems if k[0] in (5, 3, 9, 6)]:
    gp = elems[key]
    for trial in range(nconj):
        c = g["random_element"](); a = int(rng.integers(1, key[0])) if key[0] in (5, 3) else 1
        h = comp(c, comp(power(gp, a), inv(c)))
        orbs = g["orbits_of"](40, [lambda q, gp=gp, h=h: (gp[q[0]], h[q[1]])])
        size, bd, st, S, ngood = g["solve_orbits"](40, adj, orbs, sec, 4)
        out["runs"].append(dict(order=key[0], fixed=key[1], size=size, bound=bd, status=st))
        if size > best[0]:
            assert verify(S); best = (size, S); print("NEW BEST", size, key, st, round(time.time() - t0), "s", flush=True)
    print(key, "max so far", best[0], Counter_ := max(r["size"] for r in out["runs"] if r["order"] == key[0]), round(time.time() - t0), "s", flush=True)
out.update(best_size=best[0], best_set=best[1], best_verified_independently=verify(best[1]), Theta_lower=best[0] ** 0.5)
json.dump(out, open(os.path.join(ROOT, "data", "w33_shannon_symmetric_codes_conj.json"), "w"), indent=1, default=int)
print("FINAL", best[0], out["best_verified_independently"], flush=True)
