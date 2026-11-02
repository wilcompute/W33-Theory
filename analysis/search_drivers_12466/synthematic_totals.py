"""12523: codewords = (double-six, synthematic total).  Build the 27 frames and meet relation (share a sentinel) from the W(3,3) data.  For each codeword: Stab has orbits 12 + 15 on the 27; verify the 12 is a double-six (6 + 6 mutually skew, a_i skew to b_i, a_i meets b_j for i != j); the 15 are the c_ij; the planes inside the 15 are the 15 synthemes; the codeword's 5 sentinels are 5 synthemes covering all 15 c-lines.  Count: 36 double-sixes, 6 totals each, all hit once.  Duad labels c_ij are recovered from the double-six and the syntheme structure is checked combinatorially.  usage: py -3 synthematic_totals.py"""
import collections, itertools, json, runpy
import networkx as nx
ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T, lmap = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T", "lmap"))
e = tuple(range(40)); P = group([T(pts[i]) for i in range(40)]); inv8 = [g for g in P if g != e and compose(g, g) == e and sum(g[i] == i for i in range(40)) == 8]
fix = sorted((frozenset(i for i in range(40) if g[i] == i) for g in inv8), key=sorted)
disj = [[not (fix[a] & fix[b]) and a != b for b in range(45)] for a in range(45)]
frames = set()
for a in range(45):
    for C in itertools.combinations([b for b in range(45) if disj[a][b]], 4):
        if all(disj[x][y] for x, y in itertools.combinations(C, 2)): frames.add(frozenset((a,) + C))
frames = sorted(frames, key=sorted); assert len(frames) == 27
meet = [[a != b and bool(frames[a] & frames[b]) for b in range(27)] for a in range(27)]
planes = [frozenset(i for i, f in enumerate(frames) if s in f) for s in range(45)]; assert all(len(p) == 3 for p in planes)
# all double-sixes, intrinsically
sixes = [c for c in map(frozenset, nx.find_cliques(nx.Graph([(a, b) for a in range(27) for b in range(a) if not meet[a][b]]))) if len(c) == 6]
ds = set()
for A in sixes:
    for B in sixes:
        if A & B: continue
        if all(sum(not meet[a][b] for b in B) == 1 for a in A): ds.add(frozenset((A, B)))
out = dict(sixes=len(sixes), double_sixes=len(ds))
def totals_of(D):
    twelve = frozenset().union(*D); fifteen = frozenset(range(27)) - twelve
    syn = [i for i, p in enumerate(planes) if p <= fifteen]
    assert len(syn) == 15
    tots = []
    for C in itertools.combinations(syn, 5):
        if len(frozenset().union(*(planes[i] for i in C))) == 15: tots.append(frozenset(C))
    return twelve, fifteen, syn, tots
total_map = {}
for D in ds:
    _, _, syn, tots = totals_of(D); assert len(tots) == 6, len(tots)
    for t in tots: total_map[t] = D
out["totals_total"] = len(total_map); out["per_double_six"] = 6
hits = collections.Counter(); ok = True; inv = {}
for S in codewords:
    comp = set(range(40)) - set().union(*(set(lines[j]) for j in S))
    C = frozenset(i for i, f in enumerate(fix) if f <= comp); assert len(C) == 5
    if C not in total_map: ok = False; continue
    hits[total_map[C]] += 1; inv[C] = S
out["every_circuit_is_a_total"] = bool(ok); out["codewords_per_double_six"] = sorted(set(hits.values())); out["double_sixes_hit"] = len(hits); out["bijection_codewords_totals"] = len(inv) == 216 == len(total_map)
# Hexad side: two totals of a double-six share exactly one syntheme (the classical property), a discriminating check
D0 = next(iter(ds)); _, _, _, t0 = totals_of(D0); out["two_totals_share_one_syntheme"] = sorted({len(a & b) for a, b in itertools.combinations(t0, 2)})
# which sentinels: the 10 others of the stabiliser's orbit 10 and 30
S0 = codewords[0]; comp = set(range(40)) - set().union(*(set(lines[j]) for j in S0)); C0 = frozenset(i for i, f in enumerate(fix) if f <= comp); D = total_map[C0]; tw, fi, syn, _ = totals_of(D)
out["five_plus_ten_are_the_15_synthemes"] = C0 <= set(syn)
out["planes_with_2_in_12_and_1_in_15"] = sum(len(p & tw) == 2 and len(p & fi) == 1 for p in planes)
# control: a random 5-set of the 15 synthemes is not a total, and a zero-sum 5-set always is
out["5_subsets_of_15_synthemes_that_are_totals"] = sum(len(frozenset().union(*(planes[i] for i in C))) == 15 for C in itertools.combinations(syn, 5)); out["5_subsets_of_15"] = 3003
print(json.dumps(out)); json.dump(out, open("synthematic_totals.json", "w"), indent=1)
