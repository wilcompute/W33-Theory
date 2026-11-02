"""12523: for an uncovered codeword, c lies in exactly 2 sentinels of its circuit, i.e. a pair of the 9 involutions through c (Hesse SIC points).  Test: T_c-classes <-> the 36 pairs, and the codeword's
unique stabiliser involution is the third point of the affine line through the pair.  For a covered codeword: how do the 9 Hesse points sit against the circuit?  usage: py -3 pair_of_sic.py"""
import collections, itertools, json, runpy
ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T, lmap, gens, path = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T", "lmap", "gens", "path"))
e = tuple(range(40)); c = path[4]; G = group(gens[:3]); Gl = {g: lmap(g) for g in G}; Tc = T(pts[c])
act = lambda g, S: frozenset(Gl[g][j] for j in S)
inv = [g for g in G if g != e and compose(g, g) == e]; assert len(inv) == 9
fix = {t: frozenset(i for i in range(40) if t[i] == i) for t in inv}
third = lambda a, b: compose(compose(a, b), a)
out = {}; pairs = collections.defaultdict(set); ok_third = True; cov_pattern = collections.Counter(); cov_line = True
for S in codewords:
    covered = set().union(*(set(lines[j]) for j in S)); comp = set(range(40)) - covered
    inside = [t for t in inv if fix[t] <= comp]     # sentinels of S's circuit through c, among the 9
    cls = frozenset({S, act(Tc, S), act(Tc, act(Tc, S))})
    st = [g for g in G if act(g, S) == S]; I = [g for g in st if g != e and compose(g, g) == e]
    if c in covered:
        cov_pattern[len(inside)] += 1
    else:
        assert len(inside) == 2 and len(I) == 1
        ok_third &= third(inside[0], inside[1]) == I[0]
        pairs[frozenset(inside)].add(cls)
out["uncovered_pair_labels"] = len(pairs); out["classes_per_pair"] = sorted({len(v) for v in pairs.values()}); out["stabiliser_involution_is_third_point"] = bool(ok_third)
out["covered_codewords_by_number_of_Hesse_sentinels_in_complement"] = dict(cov_pattern)
print(json.dumps(out)); json.dump(out, open("pair_of_sic.json", "w"), indent=1)
