"""12523: Kramers, doily, codeword.  The 36 anti-symplectic involutions (coset of PSp(4,3) in PGSp(4,3)) with theta^2 = -1 (Pass 11210) act on the 45 sentinels; for each, the sentinels it fixes while swapping the two hyperbolic lines (15 expected).  Test: those 15 are the syntheme slice S_D of one double-six; lines of the doily = those 15 sentinels, points = the 15 c frames (GQ(2,2) checked: 3 points per line, 3 lines per point, 15+15, no triangles); doily spreads = the 6 totals; each codeword's five sentinels are a spread of the doily of a unique theta.  Also write generators and one spread for GAP.  usage: py -3 kramers_doily.py"""
import collections, itertools, json, runpy
import numpy as np, networkx as nx
ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T, lmap, pid, norm = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T", "lmap", "pid", "norm"))
e = tuple(range(40)); P = group([T(pts[i]) for i in range(40)]); inv8 = [g for g in P if g != e and compose(g, g) == e and sum(g[i] == i for i in range(40)) == 8]
fix = sorted((frozenset(i for i in range(40) if g[i] == i) for g in inv8), key=sorted); sid = {f: i for i, f in enumerate(fix)}
s = tuple(pid[norm((v[0], v[1], (-v[2]) % 3, (-v[3]) % 3))] for v in pts)
assert all((w(pts[s[a]], pts[s[b]]) == 0) == (w(pts[a], pts[b]) == 0) for a in range(40) for b in range(40))  # commutation preserved
coset = [compose(g, s) for g in P]; assert len(set(coset)) == 25920 and not (set(coset) & P)
invo = [g for g in coset if compose(g, g) == e]; out = dict(involutions_in_outer_coset=len(invo), fixed_point_counts=dict(collections.Counter(sum(g[i] == i for i in range(40)) for g in invo)))
sact = lambda g, i: sid[frozenset(g[p] for p in fix[i])]
def hyp_parts(f):
    G = nx.Graph(); G.add_nodes_from(f); G.add_edges_from((a, b) for a, b in itertools.combinations(sorted(f), 2) if w(pts[a], pts[b]) != 0)
    return [frozenset(c) for c in nx.connected_components(G)]
kr = {}
for g in invo:
    F = [i for i in range(45) if sact(g, i) == i]
    if len(F) != 15: continue
    swaps = [i for i in F if frozenset(g[p] for p in hyp_parts(fix[i])[0]) == hyp_parts(fix[i])[1]]
    kr[g] = (frozenset(F), len(swaps))
out["outer_involutions_fixing_15_sentinels"] = len(kr); out["all_15_swap_the_factors"] = sorted({v[1] for v in kr.values()})
disj = [[not (fix[a] & fix[b]) and a != b for b in range(45)] for a in range(45)]
frames = set()
for a in range(45):
    for C in itertools.combinations([b for b in range(45) if disj[a][b]], 4):
        if all(disj[x][y] for x, y in itertools.combinations(C, 2)): frames.add(frozenset((a,) + C))
frames = sorted(frames, key=sorted)
planes = [frozenset(i for i, f in enumerate(frames) if t in f) for t in range(45)]
codes = {}
for S in codewords:
    comp = set(range(40)) - set().union(*(set(lines[j]) for j in S)); codes[frozenset(i for i, f in enumerate(fix) if f <= comp)] = S
assert len(codes) == 216
out["slices"] = len({v[0] for v in kr.values()})
hits = collections.Counter(); gq = True; sp_count = collections.Counter()
for g, (F, _) in kr.items():
    pts15 = frozenset().union(*(planes[i] for i in F))
    if len(pts15) != 15: gq = False; continue
    deg = collections.Counter(x for i in F for x in planes[i]); gq &= set(deg.values()) == {3}
    col = nx.Graph(); [col.add_edge(a, b) for i in F for a, b in itertools.combinations(planes[i], 2)]
    gq &= sum(nx.triangles(col).values()) // 3 == 15     # exactly the 15 lines are triangles: no others
    spreads = [frozenset(C) for C in itertools.combinations(sorted(F), 5) if len(frozenset().union(*(planes[i] for i in C))) == 15]
    sp_count[len(spreads)] += 1
    for C in spreads:
        if C in codes: hits[C] += 1
out["doily_is_GQ22"] = bool(gq); out["spreads_per_doily"] = dict(sp_count); out["codewords_hit"] = len(hits); out["each_codeword_from_unique_theta"] = sorted(set(hits.values()))
print(json.dumps(out)); json.dump(out, open("kramers_doily.json", "w"), indent=1)
Gl = [lmap(T(pts[i])) for i in range(6)]
sp = nx.Graph(); sets = [frozenset(L) for L in lines]; sp.add_nodes_from(range(40)); sp.add_edges_from((a, b) for a, b in itertools.combinations(range(40), 2) if not sets[a] & sets[b])
spread = next(c for c in nx.find_cliques(sp) if len(c) == 10)
allg = [lmap(T(pts[i])) for i in range(40)]
with open("gap_q3.g", "w") as f:
    f.write("gens := [" + ",\n".join("PermList([" + ",".join(str(x + 1) for x in g) + "])" for g in allg) + "];;\nspread := Set([" + ",".join(str(j + 1) for j in spread) + "]);;\n")
    f.write("codewords := [" + ",".join("Set([" + ",".join(str(j + 1) for j in S) + "])" for S in codewords) + "];;\n")
