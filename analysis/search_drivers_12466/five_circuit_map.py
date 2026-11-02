"""12523: explicit equivariant bijection between the 216 minimal even line sets (Pass 173) and the 216 sentinel five-circuits of 2026-08-29.  A sentinel = the 8 fixed points of an
involution of PSp(4,3) with 8 fixed points (H u H^perp, a factorisation); a five-circuit = 5 sentinels with zero F2-sum, as in w33_20260829_216_clifford_torsor_nogo.py (count asserted 216).
Find the Stab(S)-invariant five-circuits of a codeword S; transport by the whole group; check the relation is a well-defined bijection.  Then read the geometry: how each of S's 10 lines sits
against the 5 sentinels (10 = C(5,2)?).  usage: py -3 five_circuit_map.py"""
import collections, itertools, json, runpy
import numpy as np
ns = runpy.run_path("braid_codewords.py")
pts, lines, codewords, w, compose, group, T, lmap = (ns[k] for k in ("pts", "lines", "codewords", "w", "compose", "group", "T", "lmap"))
e = tuple(range(40)); P = group([T(pts[i]) for i in range(40)]); assert len(P) == 25920
inv8 = [g for g in P if g != e and compose(g, g) == e and sum(g[i] == i for i in range(40)) == 8]
assert len(inv8) == 45
sup = {g: frozenset(i for i in range(40) if g[i] == i) for g in inv8}; supports = sorted(sup.values(), key=sorted); assert len(set(supports)) == 45
sid = {s: i for i, s in enumerate(supports)}; masks = [sum(1 << i for i in s) for s in supports]
circuits = set()
for C in itertools.combinations(range(45), 5):
    x = 0
    for i in C: x ^= masks[i]
    if x == 0: circuits.add(frozenset(C))
assert len(circuits) == 216
sact = lambda g, i: sid[frozenset(g[p] for p in supports[i])]
S0 = codewords[0]; Gl = {g: lmap(g) for g in P}
act = lambda g, S: frozenset(Gl[g][j] for j in S)
St = [g for g in P if act(g, S0) == S0]; assert len(St) == 120
inv_C = [C for C in circuits if all(frozenset(sact(g, i) for i in C) == C for g in St)]
out = dict(stabiliser=len(St), invariant_circuits=len(inv_C))
orbs = []; left = set(range(45))
while left:
    i = min(left); o = {sact(g, i) for g in St}; orbs.append(len(o)); left -= o
out["stabiliser_orbits_on_45_sentinels"] = sorted(orbs)
assert len(inv_C) == 1, inv_C
C0 = inv_C[0]; rel = {}
for g in P:
    k = act(g, S0); v = frozenset(sact(g, i) for i in C0)
    assert rel.setdefault(k, v) == v
out["bijection"] = len(rel) == 216 and len(set(rel.values())) == 216 and set(rel.values()) == circuits
# geometry of one codeword against its circuit
Cs = [supports[i] for i in C0]
lab = collections.Counter(); pairs = {}
for j in S0:
    L = set(lines[j]); ints = tuple(sorted(len(L & s) for s in Cs)); lab[ints] += 1; pairs[j] = frozenset(i for i, s in enumerate(Cs) if len(L & s) == 0)
out["line_vs_5_sentinels_intersections"] = {str(k): v for k, v in lab.items()}
out["lines_to_subsets_of_sentinels"] = sorted(sorted(v) for v in pairs.values())
cov = collections.Counter(); covered = set().union(*(set(lines[j]) for j in S0))
for p in range(40): cov[(p in covered, sum(p in s for s in Cs))] += 1
out["point_(covered,in_how_many_sentinels)"] = {str(k): v for k, v in cov.items()}
out["sentinel_pairwise_intersections"] = sorted({len(a & b) for a, b in itertools.combinations(Cs, 2)})
out["union_of_circuit_points"] = len(set().union(*Cs))
print(json.dumps(out)); json.dump(out, open("five_circuit_map.json", "w"), indent=1)
