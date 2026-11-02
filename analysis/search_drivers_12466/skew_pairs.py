"""12523: the 216 codewords and the pairs of skew lines of the cubic surface.  45 sentinels with 'disjoint' = GQ(4,2) points (5 pts per line, 3 lines per point): its 27 lines = 5 mutually disjoint sentinels partitioning the 40 points ('frames', the 27 lines of the cubic).  Test: Stab(S) (S5, order 120) has a unique orbit of size 2 on the 27 frames, and it is a skew pair (no common sentinel); the map is a bijection onto all 216 skew pairs; how the codeword's five sentinels sit relative to the pair and to its 5 common transversal frames.  usage: py -3 skew_pairs.py"""
import collections, itertools, json, runpy
ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T, lmap = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T", "lmap"))
e = tuple(range(40)); P = group([T(pts[i]) for i in range(40)]); inv8 = [g for g in P if g != e and compose(g, g) == e and sum(g[i] == i for i in range(40)) == 8]
fix = sorted((frozenset(i for i in range(40) if g[i] == i) for g in inv8), key=sorted); sid = {f: i for i, f in enumerate(fix)}
disj = [[not (fix[a] & fix[b]) and a != b for b in range(45)] for a in range(45)]
frames = set()
for a in range(45):
    for C in itertools.combinations([b for b in range(45) if disj[a][b]], 4):
        if all(disj[x][y] for x, y in itertools.combinations(C, 2)): frames.add(frozenset((a,) + C))
frames = sorted(frames, key=sorted); out = dict(frames=len(frames), points_per_frame=sorted({len(f) for f in frames}), frames_per_sentinel=sorted(collections.Counter(s for f in frames for s in f).values())[::44])
fid = {f: i for i, f in enumerate(frames)}; sact = lambda g, i: sid[frozenset(g[p] for p in fix[i])]; fact = lambda g, i: fid[frozenset(sact(g, s) for s in frames[i])]
skew = [(a, b) for a, b in itertools.combinations(range(27), 2) if not (frames[a] & frames[b])]; out["skew_pairs"] = len(skew)
Gl = {g: lmap(g) for g in P}; act = lambda g, S: frozenset(Gl[g][j] for j in S)
S0 = codewords[0]; St = [g for g in P if act(g, S0) == S0]
left = set(range(27)); orbs = []
while left:
    i = min(left); o = {fact(g, i) for g in St}; orbs.append(sorted(o)); left -= o
out["stabiliser_orbits_on_27"] = sorted(len(o) for o in orbs)
print(out); pair = next(o for o in orbs if len(o) == 2); out["pair_is_skew"] = not (frames[pair[0]] & frames[pair[1]])
rel = {}
for g in P:
    k = act(g, S0); v = frozenset(fact(g, i) for i in pair); assert rel.setdefault(k, v) == v
out["bijection_codewords_to_skew_pairs"] = len(rel) == 216 and {frozenset(p) for p in skew} == set(rel.values())
comp = set(range(40)) - set().union(*(set(lines[j]) for j in S0)); circ = [i for i, f in enumerate(fix) if f <= comp]; assert len(circ) == 5
a, b = [frames[i] for i in pair]; A, B = set(a), set(b)
trans = [i for i, f in enumerate(frames) if f & a and f & b]; out["common_transversal_frames"] = len(trans)
out["circuit_in_pair_frames"] = [len(set(circ) & A), len(set(circ) & B)]
out["circuit_sentinel_on_how_many_transversals"] = sorted(sum(s in frames[t] for t in trans) for s in circ)
out["transversal_contains_how_many_circuit_sentinels"] = sorted(len(set(circ) & frames[t]) for t in trans)
out["third_line"] = None
print(json.dumps(out)); json.dump(out, open("skew_pairs.json", "w"), indent=1)
