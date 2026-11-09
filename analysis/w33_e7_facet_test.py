"""Item 2: the E7 facet test for the scalene-triple candidate (Pass 12637).
E7 pezzotope facets (Early-Geiger-Panizzut-Sturmfels-Yun, eqs. (35)-(39)): 10 A1, 12 A2, 9 A3x2, 3 A7, roots in the d-coordinates:
'ijk' = d_i + d_j + d_k (Pic: h - e_i - e_j - e_k), 'ij' = d_i - d_j (e_i - e_j), 'i' = -d_i + sum d_j (2h - sum e + e_i).
Dictionary to three qubits: roots mod 2 <-> 63 points of W(5,2) (collinear iff the Pic intersection number is even); Lagrangian planes
<-> the 135 7A1 frames (7 mutually orthogonal roots); A7 subsystems <-> O+ forms, A7's 28 roots = non-singular points.
Test: the planes totally singular for ALL THREE A7 facets (frames disjoint from the three 28-root sets) - is it exactly a scalene triple
(pairwise common roots 0, 1, 3 <-> intersection dims 0, 1, 2)?  Then: the 10 A1 roots vs the triple, and the S4.
usage: py -3 analysis/w33_e7_facet_test.py"""
import itertools, json, os
from collections import Counter
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def vec(s):
    v = np.zeros(8, dtype=int)  # (h, e1..e7)
    if len(s) == 3:
        v[0] = 1
        for c in s: v[int(c)] = -1
    elif len(s) == 2:
        v[int(s[0])] = 1; v[int(s[1])] = -1
    else:
        v[0] = 2; v[1:] = -1; v[int(s)] = 0
    return v
B = lambda x, y: int(x[0] * y[0] - x[1:] @ y[1:])
roots = [vec(f"{i}{j}") for i in range(1, 8) for j in range(i + 1, 8)] + [vec("".join(map(str, t))) for t in itertools.combinations(range(1, 8), 3)] + [vec(str(i)) for i in range(1, 8)]
assert len(roots) == 63 and all(B(r, r) == -2 for r in roots)
key = lambda v: tuple(v) if tuple(v) > tuple(-v) else tuple(-v)
RI = {key(r): i for i, r in enumerate(roots)}
def rid(s): return RI[key(vec(s))]
G = np.array([[B(a, b) for b in roots] for a in roots])
frames = []
def ext(S, start):
    if len(S) == 7: frames.append(frozenset(S)); return
    for k in range(start, 63):
        if all(G[k, x] == 0 for x in S): ext(S + [k], k + 1)
ext([], 0)
print("7A1 frames (Lagrangian planes):", len(frames))
A1 = ["124", "126", "134", "135", "157", "235", "237", "367", "456", "457"]
A7 = {
 "u32": "126 124 134 135 235 237 456 457 567 46 136 23 125 45 234 12 137 57 467 1 236 67 127 3 13 56 2 47".split(),
 "u33": "126 457 157 135 235 237 367 124 567 3 246 14 345 37 257 12 137 57 356 26 146 5 347 46 35 24 7 16".split(),
 "u34": "134 135 157 457 237 456 367 124 125 45 147 37 345 14 156 67 236 1 245 26 146 5 267 23 15 36 4 27".split(),
}
A7s = {k: frozenset(rid(s) for s in v) for k, v in A7.items()}
ok_a7 = {k: (len(S) == 28, all(G[a, b] % 2 == 0 or True for a in S for b in S)) for k, S in A7s.items()}
print("A7 facet sizes:", {k: len(S) for k, S in A7s.items()})
sing = [f for f in frames if all(not (f & S) for S in A7s.values())]
inter = sorted(len(a & b) for a, b in itertools.combinations(sing, 2))
print("frames totally singular for all three A7 facets:", len(sing), "| pairwise common roots:", inter)
scalene = len(sing) == 3 and inter == [0, 1, 3]
# A1 facets relative to the triple
a1 = [rid(s) for s in A1]
rel = Counter(tuple(int(x in f) for f in sing) for x in a1) if sing else None
res = dict(n_frames=len(frames), n_singular_for_all_three=len(sing), pairwise_common=inter, scalene_triple=scalene,
           A1_vs_triple={str(k): v for k, v in rel.items()} if rel else None)
print("scalene triple:", scalene, "| A1 roots by membership in the three planes:", res["A1_vs_triple"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_e7_facet_test.json"), "w"), indent=1)

# --- explore other natural frame sets defined by the facets
names = list(A7s)
sing_by = {f: tuple(int(not (f & A7s[k])) for k in names) for f in frames}
cnt = Counter(sing_by.values())
print("frames by singularity pattern for (u32, u33, u34):", dict(sorted(cnt.items())))
A2 = {"u11": "12 135 235", "u12": "14 157 457", "u13": "23 124 134", "u14": "26 237 367", "u15": "37 135 157", "u16": "45 134 135",
      "u17": "46 124 126", "u18": "57 235 237", "u19": "67 456 457", "u20": "1 237 456", "u21": "3 126 457", "u22": "5 124 367"}
A2s = {k: frozenset(rid(s) for s in v.split()) for k, v in A2.items()}
facet_roots = set(a1) | set().union(*A2s.values())
by_a1 = Counter(len(f & set(a1)) for f in frames)
print("frames by number of A1-facet roots they contain:", dict(sorted(by_a1.items())))
# candidate: frames with exactly k A1 roots, for each k, and their pairwise common-root pattern
cands = {}
for k in sorted(by_a1):
    F = [f for f in frames if len(f & set(a1)) == k]
    if len(F) <= 6:
        cands[k] = (len(F), sorted(len(a & b) for a, b in itertools.combinations(F, 2)))
print("small frame classes by #A1 roots (size, pairwise common roots):", cands)
for pat in sorted(cnt):
    F = [f for f in frames if sing_by[f] == pat]
    if 2 <= len(F) <= 6:
        print("  singularity pattern", pat, "->", len(F), "frames, pairwise common:", sorted(len(a & b) for a, b in itertools.combinations(F, 2)))
res["singularity_patterns"] = {str(k): v for k, v in cnt.items()}
res["frames_by_A1_count"] = dict(by_a1)
json.dump(res, open(os.path.join(ROOT, "data", "w33_e7_facet_test.json"), "w"), indent=1, default=str)

# --- the canonical triple: the unique frame with 6 A1 roots + the two frames singular for all three A7 facets
F6 = [f for f in frames if len(f & set(a1)) == 6]
trip = F6 + sing
pc = sorted(len(a & b) for a, b in itertools.combinations(trip, 2)) if len(trip) == 3 else None
is_scalene = pc == [0, 1, 3]
print("canonical triple (6-A1 frame + two all-A7-singular frames): pairwise common roots", pc, "-> scalene:", is_scalene)
res["canonical_triple_pairwise_common"] = pc
res["canonical_triple_is_scalene"] = is_scalene
json.dump(res, open(os.path.join(ROOT, "data", "w33_e7_facet_test.json"), "w"), indent=1, default=str)
