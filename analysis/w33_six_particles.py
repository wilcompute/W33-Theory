"""Item 1: the six external particles of the double-six facet amplitude (Pass 12636 addendum 3: on each root facet r the pezzotope
amplitude restricts to the 6-point phi^3 tree; 6 neighbour roots = short diagonals = 2-particle channels, 3 cusps = long diagonals).
Hexagon reconstruction: a short diagonal (i-1, i+1) cuts off vertex i, and two short diagonals cross iff their vertices are adjacent;
so the 'crossing' graph (never together in a vertex) on the 6 neighbour roots must be a 6-cycle = the particles in cyclic order.
Candidate particles: the lines of a six of r's double-six (12 lines with r.l != 0, split by the sign of r.l).  For each neighbour
root s find the lines l of each six with a distinguished value of s.l, and test for a bijection neighbour roots <-> lines of one six
that turns the crossing 6-cycle into a 6-cycle of lines under some natural line relation (they are mutually skew, so test via the
other six / the 15 c_ij lines).  Also test the long diagonals: a long diagonal (i, i+3) splits the particles 3|3 - which 3|3 split of
the six does each cusp induce?  All 432 pezzotopes x 10 facets.
usage: py -3 analysis/w33_six_particles.py"""
import itertools, json, os
from collections import Counter
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
gz = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pezzotope_gosset.py")}
exec(open(os.path.join(HERE, "w33_pezzotope_gosset.py"), encoding="utf-8").read().split("# candidate canonical line sets")[0], gz)
pents, IP, T3, RL, roots_of = gz["pents"], gz["IP"], gz["T3"], gz["RL"], gz["roots_of"]
np = gz["np"]
stats = Counter()
example = None
for C, r in pents:
    ra = sorted(r.values())
    verts = []
    for S in itertools.combinations(ra, 4):
        if all(IP[x, y] == 0 for x, y in itertools.combinations(S, 2)):
            verts.append(frozenset(("a", x) for x in S))
    for t in C:
        for pick in itertools.product(*[sorted(A) for A in sorted(T3[t], key=min)]):
            if all(p in ra for p in pick):
                verts.append(frozenset([("b", t)] + [("a", p) for p in pick]))
    for root in ra:
        f = ("a", root)
        vf = [v - {f} for v in verts if f in v]
        nb_roots = sorted({g[1] for v in vf for g in v if g[0] == "a"})
        nb_cusps = sorted({g[1] for v in vf for g in v if g[0] == "b"})
        together = {frozenset(p) for v in vf for p in itertools.combinations(sorted(v, key=str), 2)}
        Gc = nx.Graph(); Gc.add_nodes_from(nb_roots)
        Gc.add_edges_from((a, b) for a, b in itertools.combinations(nb_roots, 2) if frozenset((("a", a), ("a", b))) not in together)
        is6cycle = nx.is_isomorphic(Gc, nx.cycle_graph(6))
        sixA = [l for l in range(27) if RL[root, l] > 1e-6]
        sixB = [l for l in range(27) if RL[root, l] < -1e-6]
        # each neighbour root s: which lines of each six does it pair with nonzero?
        pat = tuple(sorted((sum(abs(RL[s, l]) > 1e-6 for l in sixA), sum(abs(RL[s, l]) > 1e-6 for l in sixB)) for s in nb_roots))
        # candidate bijection: s -> the unique line of sixA with s.l == 0 (or != 0) if unique
        def uniq(six, zero):
            out = {}
            for s in nb_roots:
                L = [l for l in six if (abs(RL[s, l]) < 1e-6) == zero]
                out[s] = L[0] if len(L) == 1 else None
            return out
        cands = {}
        for name, six in (("A", sixA), ("B", sixB)):
            for zero in (True, False):
                m = uniq(six, zero)
                if all(v is not None for v in m.values()) and len(set(m.values())) == 6:
                    cands[(name, zero)] = m
        # long diagonals: each cusp T induces a 3|3 split of the 6 particles (= the neighbour roots in T vs not in T?)
        cusp_split = tuple(sorted(len(set(nb_roots) & roots_of[t]) for t in nb_cusps))
        key = (is6cycle, pat, tuple(sorted(cands)), cusp_split)
        stats[key] += 1
        if example is None and cands:
            example = dict(root=root, nb_roots=nb_roots, cands={str(k): v for k, v in cands.items()})
print("per root facet: (crossing graph = 6-cycle, (#lines of sixA, of sixB) each neighbour root meets, bijection types found, cusp 3|3 sizes): count")
for k, v in stats.items():
    print("  ", k, v)
res = dict(stats={str(k): v for k, v in stats.items()}, example=example)
json.dump(res, open(os.path.join(ROOT, "data", "w33_six_particles.json"), "w"), indent=1, default=str)

# --- the particles = the six lines of a six in a cyclic order: duads D_s of the neighbour roots form a Hamiltonian cycle on the six,
#     and two neighbour roots cross (hexagon-adjacent channels) iff their duads share a line; the duads in sixA and sixB carry the same
#     index pattern under the double-six pairing a_i <-> b_i (the unique line of B skew to a_i).
G_, v_skew = gz["G"], gz["v_skew"]
skew = lambda i, j: abs(G_[i, j] - v_skew) < 1e-6
ok = Counter()
for C, r in pents:
    ra = sorted(r.values())
    verts = []
    for S in itertools.combinations(ra, 4):
        if all(IP[x, y] == 0 for x, y in itertools.combinations(S, 2)):
            verts.append(frozenset(("a", x) for x in S))
    for t in C:
        for pick in itertools.product(*[sorted(A) for A in sorted(T3[t], key=min)]):
            if all(p in ra for p in pick):
                verts.append(frozenset([("b", t)] + [("a", p) for p in pick]))
    for root in ra:
        f = ("a", root)
        vf = [v - {f} for v in verts if f in v]
        nb = sorted({g[1] for v in vf for g in v if g[0] == "a"})
        together = {frozenset(p) for v in vf for p in itertools.combinations(sorted(v, key=str), 2)}
        cross = {frozenset((a, b)) for a, b in itertools.combinations(nb, 2) if frozenset((("a", a), ("a", b))) not in together}
        A = [l for l in range(27) if RL[root, l] > 1e-6]; B = [l for l in range(27) if RL[root, l] < -1e-6]
        partner = {a: next(b for b in B if skew(a, b)) for a in A}
        D = {s: frozenset(l for l in A if abs(RL[s, l]) > 1e-6) for s in nb}
        DB = {s: frozenset(l for l in B if abs(RL[s, l]) > 1e-6) for s in nb}
        H = nx.Graph(); H.add_edges_from(tuple(D[s]) for s in nb)
        ham = H.number_of_nodes() == 6 and nx.is_isomorphic(H, nx.cycle_graph(6))
        same = all({partner[a] for a in D[s]} == DB[s] for s in nb)
        cross_is_share = all((frozenset((a, b)) in cross) == bool(D[a] & D[b]) for a, b in itertools.combinations(nb, 2))
        ok[(ham, same, cross_is_share)] += 1
res["particles_test"] = {str(k): v for k, v in ok.items()}
print("(duads form a Hamiltonian 6-cycle on the six, same duads in both sixes, crossing <=> duads share a line): count", dict(ok))
json.dump(res, open(os.path.join(ROOT, "data", "w33_six_particles.json"), "w"), indent=1, default=str)
