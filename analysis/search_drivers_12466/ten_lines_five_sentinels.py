"""12523: the intersection graph of a codeword's 10 lines, its S5 action, and how the lines pair with the 5 sentinels.  Prediction: K_{5,5} minus a perfect matching, the 5 matching pairs = the 5 sentinels.  usage: py -3 ten_lines_five_sentinels.py"""
import collections, itertools, json, runpy
import networkx as nx
ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T, lmap = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T", "lmap"))
e = tuple(range(40)); P = group([T(pts[i]) for i in range(40)]); inv8 = [g for g in P if g != e and compose(g, g) == e and sum(g[i] == i for i in range(40)) == 8]
fix = {g: frozenset(i for i in range(40) if g[i] == i) for g in inv8}
out = {}; sets = [set(L) for L in lines]
S0 = sorted(codewords[0]); G = nx.Graph(); G.add_nodes_from(S0)
G.add_edges_from((a, b) for a, b in itertools.combinations(S0, 2) if sets[a] & sets[b])
out["degree"] = sorted(set(dict(G.degree()).values())); out["bipartite"] = nx.is_bipartite(G)
A, Bb = nx.bipartite.sets(G); out["parts"] = [len(A), len(Bb)]
Hc = nx.complement(G); match = [frozenset((a, b)) for a in A for b in Bb if not G.has_edge(a, b)]; out["matching_pairs"] = len(match)
comp = set(range(40)) - set().union(*(sets[j] for j in S0))
sent = [t for t in inv8 if fix[t] <= comp]; out["sentinels_in_complement"] = len(sent)
Gl = {t: lmap(t) for t in sent}
rel = []
for t in sent:
    fixed_lines = sorted(j for j in S0 if Gl[t][j] == j)
    swapped = sorted(frozenset((j, Gl[t][j])) and (min(j, Gl[t][j]), max(j, Gl[t][j])) for j in S0 if Gl[t][j] != j and Gl[t][j] in S0)
    rel.append(dict(fixes_S=all(Gl[t][j] in S0 for j in S0), fixed=fixed_lines, swapped=sorted(set(swapped))))
out["sentinel_action_on_ten"] = rel
mp = {m: [i for i, r in enumerate(rel) if sorted(m) == r["fixed"] or tuple(sorted(m)) in [tuple(x) for x in r["swapped"]]] for m in match}
out["each_matching_pair_singled_out_by_one_sentinel"] = sorted(len(v) for v in mp.values())
# perp of a disjoint pair: lines through it
transv = {}
for m in match:
    a, b = sorted(m); pp = [j for j in range(40) if sets[j] & sets[a] and sets[j] & sets[b]]
    pts_cov = set().union(*(sets[j] for j in pp)) if pp else set()
    transv[(a, b)] = dict(transversals=len(pp), union=len(pts_cov), meets_comp=len(pts_cov & comp))
out["pair_transversals"] = list({str(v) for v in transv.values()})
print(json.dumps(out)); json.dump(out, open("ten_lines_five_sentinels.json", "w"), indent=1, default=str)
