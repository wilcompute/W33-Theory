"""12521: the B4 image is the stabiliser of the point c = <p0, p1, p2>^perp; the 108 + 108 split of the 216 codewords is "c covered / c not
covered"; B3 and B5 for contrast.  usage: py -3 braid_point_stabiliser.py"""
import json, runpy, collections
ns = runpy.run_path("braid_codewords.py")
pts, lines, gens, group, codewords, w, path, compose = (ns[k] for k in ("pts", "lines", "gens", "group", "codewords", "w", "path", "compose"))
out = {}
G = group(gens[:3]); assert len(G) == 648
fixed = [i for i in range(40) if all(g[i] == i for g in gens[:3])]
perp = [i for i in range(40) if all(w(pts[i], pts[p]) == 0 for p in path[:3])]
out["G_order"] = len(G); out["points_fixed_by_G"] = fixed; out["perp_of_p0_p1_p2"] = perp
c = fixed[0]; assert fixed == perp and len(fixed) == 1
stab = [g for g in group([g for g in [ns["T"](pts[i]) for i in range(40)]], cap=30000) if g[c] == c]
out["stabiliser_of_c_in_PSp43"] = len(stab); out["G_equals_stabiliser"] = set(stab) == set(G)
covered = lambda S: sum(c in lines[j] for j in S)
cov = collections.Counter(covered(S) for S in codewords); out["coverage_of_c"] = {str(k): v for k, v in cov.items()}
# orbits of G against the coverage classes
lid = ns["lid"]; lmap = ns["lmap"]; lms = [lmap(g) for g in gens[:3]]
seen, orbs = set(), []
for S in codewords:
    if S in seen: continue
    o = {S}; f = [S]
    while f:
        nf = []
        for T_ in f:
            for g in lms:
                U = frozenset(g[j] for j in T_)
                if U not in o: o.add(U); nf.append(U)
        f = nf
    seen |= o; orbs.append(o)
out["orbits_vs_coverage"] = [dict(size=len(o), coverages=sorted({covered(S) for S in o})) for o in orbs]
# stabiliser of a codeword in G, and of its involution: a Hesse point is the involution's fixed structure
inv = [g for g in G if g != tuple(range(40)) and compose(g, g) == tuple(range(40))]
out["involutions_in_G"] = len(inv)
fix = collections.Counter(sum(g[i] == i for i in range(40)) for g in inv); out["involution_fixed_points"] = {str(k): v for k, v in fix.items()}
fib = collections.defaultdict(list); shapes = collections.Counter()
for o_i, o in enumerate(orbs):
    for S in o:
        st = [g for g in G if frozenset(lmap(g)[j] for j in S) == S] if False else None
Gl = [(g, lmap(g)) for g in G]
for o_i, o in enumerate(orbs):
    S = next(iter(o))
    st = [g for g, l in Gl if frozenset(l[j] for j in S) == S]
    els = collections.Counter()
    for g in st:
        p = g; n = 1
        while p != tuple(range(40)): p = compose(g, p); n += 1
        els[n] += 1
    shapes[(o_i, len(st), tuple(sorted(els.items())))] += 1
out["codeword_stabilisers_in_G"] = [dict(orbit=k[0], order=k[1], element_orders=dict(k[2])) for k in shapes]
json.dump(out, open("braid_point_stabiliser.json", "w"), indent=1, default=str); print(json.dumps(out, default=str)[:1500])
