"""12523: a codeword against the spread of its double-six.  A spread = 10 disjoint lines; 36 of them; S6 stabiliser.  Match spreads to double-sixes by stabiliser (the same S6).  For a codeword: how many of its 10 lines lie in that spread, and in other spreads; line orbits of Stab(S)' = A5 (BT837's cores have [10,30]); is that A5 a core of the spread?  usage: py -3 codeword_vs_spread.py"""
import collections, itertools, json, runpy
import networkx as nx
ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T, lmap = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T", "lmap"))
e = tuple(range(40)); P = group([T(pts[i]) for i in range(40)]); Gl = {g: lmap(g) for g in P}; sets = [frozenset(L) for L in lines]
G = nx.Graph(); G.add_nodes_from(range(40)); G.add_edges_from((a, b) for a, b in itertools.combinations(range(40), 2) if not sets[a] & sets[b])
spreads = [frozenset(c) for c in nx.find_cliques(G) if len(c) == 10]; out = dict(spreads=len(spreads))
act = lambda g, S: frozenset(Gl[g][j] for j in S)
S0 = codewords[0]; St = [g for g in P if act(g, S0) == S0]; A5 = group([compose(compose(compose(a, b), tuple(sorted(range(40), key=lambda i: a[i]))), tuple(sorted(range(40), key=lambda i: b[i]))) for a, b in itertools.product(St[:25], repeat=2)][:40])
out["stab_derived"] = len(A5)
left = set(range(40)); o_ = []
while left:
    i = min(left); o = {Gl[g][i] for g in A5}; o_.append(sorted(o)); left -= o
out["A5_line_orbits"] = sorted(len(o) for o in o_)
tenorb = [o for o in o_ if len(o) == 10]
inv = [s for s in spreads if act(St[0], s) == s and all(act(g, s) == s for g in St)]; out["spreads_fixed_by_Stab"] = len(inv)
inva = [s for s in spreads if all(act(g, s) == s for g in A5)]; out["spreads_fixed_by_A5"] = len(inva)
out["intersections_with_all_spreads"] = dict(collections.Counter(len(S0 & s) for s in spreads))
if inv: out["intersection_with_fixed_spread"] = len(S0 & inv[0])
pc = collections.Counter()
for s in spreads: pc[len(S0 & s)] += 1
sp_stab = [g for g in P if act(g, spreads[0]) == spreads[0]]; out["spread_stabiliser"] = len(sp_stab)
print(json.dumps(out)); json.dump(out, open("codeword_vs_spread.json", "w"), indent=1)
