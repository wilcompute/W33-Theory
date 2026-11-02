"""12521: the codeword <-> Hesse dictionary at a fixed point c.
Part A (exact, on W(3,3)): T_c acts freely on the 216 codewords; each uncovered codeword has a unique involution in its stabiliser, each
covered one has 3 collinear involutions; the 9 involutions = the 9 hyperbolic lines through c (the factorisations with P_c in a factor).
Part B (quantum, from the TL6 braid matrices): the isolated eigenvector of each involution on a 3-dim block gives a 9-state SIC (|<a|b>|^2 = 1/4);
P_c eigenspaces, the direction test and the MUB control are in hesse_dictionary2.py.  usage: py -3 hesse_dictionary.py"""
import collections, itertools, json, runpy
import numpy as np
ns = runpy.run_path("braid_codewords.py")
pts, lines, gens, group, codewords, w, path, compose, lmap, T = (ns[k] for k in ("pts", "lines", "gens", "group", "codewords", "w", "path", "compose", "lmap", "T"))
c = path[4]; G = group(gens[:3]); e = tuple(range(40)); out = dict(c=c)
Gl = {g: lmap(g) for g in G}
Tc = T(pts[c]); assert all(compose(Tc, g) == compose(g, Tc) for g in G) and Tc in G
out["Tc_fixes_no_codeword"] = all(frozenset(Gl[Tc][j] for j in S) != S for S in codewords)
inv = [g for g in G if g != e and compose(g, g) == e]
# each involution: fixed points = two hyperbolic lines of 4, one through c
hyp = {}
for t in inv:
    F = [i for i in range(40) if t[i] == i]
    nb = {i: {j for j in F if j != i and w(pts[i], pts[j]) != 0} for i in F}
    comp = []
    left = set(F)
    while left:
        a = left.pop(); C = {a}; 
        for b in F:
            if b != a and w(pts[a], pts[b]) != 0: C.add(b)
        comp.append(frozenset(C)); left -= C
    assert sorted(map(len, comp)) == [4, 4], comp
    hyp[t] = next(C for C in comp if c in C)
out["involutions"] = len(inv); out["distinct_hyperbolic_lines_through_c"] = len(set(hyp.values()))
# the affine structure: t1 t2 t1 is the third point of the line through t1, t2
aff_lines = set()
for a, b in itertools.combinations(inv, 2):
    aff_lines.add(frozenset({a, b, compose(compose(a, b), a)}))
out["affine_lines"] = len(aff_lines); out["each_line_has_3"] = all(len(L) == 3 for L in aff_lines)
direction = {}
covered = {S for S in codewords if any(c in lines[j] for j in S)}; uncovered = set(codewords) - covered
through_c = [j for j, L in enumerate(lines) if c in L]
fib_u, fib_c = collections.Counter(), collections.Counter(); pair_vs_line = collections.defaultdict(set); stab_orders = collections.Counter()
for S in codewords:
    st = [g for g, l in Gl.items() if frozenset(l[j] for j in S) == S]
    stab_orders[len(st)] += 1
    I = frozenset(g for g in st if g != e and compose(g, g) == e)
    if S in uncovered:
        assert len(I) == 1; fib_u[next(iter(I))] += 1
    else:
        assert len(I) == 3 and I in aff_lines; fib_c[I] += 1
        pair_vs_line[I].add(frozenset(j for j in S if j in through_c))
out["uncovered_fibres_over_9_involutions"] = sorted(fib_u.values()); out["covered_fibres_over_12_lines"] = sorted(fib_c.values()); out["stabiliser_orders"] = dict(stab_orders)
out["pairs_per_line"] = sorted(len(v) for v in pair_vs_line.values())
# Part B
tl = runpy.run_path("tl_braid_iso_exact.py")
seen, blocks, R, vecs, PM, gen_act, vid = (tl[k] for k in ("seen", "blocks", "R", "vecs", "PM", "gen_act", "vid"))
fixedP = [v for v in vecs if any(v) and all(a[vid[v]][0] == vid[v] for a in gen_act)]
out["pauli_vectors_fixed_by_braid"] = len(fixedP)
# involutions on the 3-dim blocks
acts = list(seen.keys())
def comp_act(a, b): return tl["compose_act"](a, b)
I_act = tl["I_act"]
def proj_pts(a): return tuple(a[i][0] for i in range(81))
ids = {proj_pts(I_act)}
invs = [a for a in acts if proj_pts(a) not in ids and proj_pts(comp_act(a, a)) in ids]
out["involutions_in_block_group"] = len(invs)
for bi, B in enumerate(blocks):
    if B.shape[1] != 3: continue
    vs = []
    for a in invs:
        m = seen[a][bi]; ev, V = np.linalg.eig(m)
        # the eigenvalue of multiplicity one
        cl = [i for i in range(3) if sum(abs(ev[i] - ev[j]) < 1e-7 for j in range(3)) == 1]
        assert len(cl) == 1; vs.append(V[:, cl[0]] / np.linalg.norm(V[:, cl[0]]))
    ov = collections.Counter(round(float(abs(np.vdot(vs[i], vs[j])) ** 2), 6) for i in range(len(vs)) for j in range(len(vs)) if i < j)
    out.setdefault("SIC_overlaps_per_3_block", []).append({str(k): v for k, v in ov.items()})
json.dump(out, open("hesse_dictionary.json", "w"), indent=1, default=str); print(json.dumps(out, default=str))
