"""Pass 12675: the three types of uncovered order-4 Pauli groups around the F_8 regulus minimum.
Type of an order-4 group S': covered-weight histogram of the cosets of S' in S'^perp (Pass 12674).
 (1) The seven order-4 subgroups of the rank-3 torus group T = <-iP(12,53), P(53,33), P(1,6)> (Pass 12671) and of the rank-3
     extension of a type-B stabiliser: their types.
 (2) Type-B ladder: the type-B stabiliser {(11,47), (35,8)} of a global minimiser (Pass 12674 census): minimum on its code space for
     every sign choice, and its rank-3 extensions attaining c8.
Effective-model minima and degree-6 SOS bounds of the type-B/C code spaces and of a type-B rank-3 space are computed with
w33_f8_codespace_effective_sos.py (GENS=...).   usage: py -3 analysis/w33_f8_stabiliser_types.py"""
import collections, itertools, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
lsrc = open(os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py")}
exec(lsrc[: lsrc.index("res = {}")], gl)
covered, comm, space, minval, C8 = (gl[k] for k in ("covered", "comm", "space", "minval", "C8"))
labels = [(u, v) for u in range(64) for v in range(64) if (u, v) != (0, 0)]
cov = {k: covered(k) for k in labels}
TYPE = {((0, 156), (1, 63), (2, 36)): "A", ((0, 138), (1, 99), (2, 18)): "B", ((0, 165), (1, 54), (2, 27), (3, 9)): "C"}
def wtype(g1, g2):
    Sg = [(0, 0), g1, g2, (g1[0] ^ g2[0], g1[1] ^ g2[1])]
    cos = {}
    for k in labels:
        if all(comm(k, t) for t in Sg[1:]): cos.setdefault(min((k[0] ^ t[0], k[1] ^ t[1]) for t in Sg), []).append(k)
    return tuple(sorted(collections.Counter(sum(cov.get(k, False) for k in c_) for kk, c_ in cos.items() if kk != (0, 0)).items()))
def subgroup_types(gens):
    T = [(0, 0)]
    for g in gens: T = T + [(e[0] ^ g[0], e[1] ^ g[1]) for e in T]
    subs = {frozenset([(0, 0), a, b, (a[0] ^ b[0], a[1] ^ b[1])]) for a, b in itertools.combinations(T[1:], 2)}
    out = collections.Counter(); reps = {}
    for S in subs:
        a, b = sorted(x for x in S if x != (0, 0))[:2]
        t = TYPE.get(wtype(a, b), str(wtype(a, b))); out[t] += 1; reps.setdefault(t, [list(a), list(b)])
    return dict(out), reps
res = {}
res["T_subgroups"], res["T_subgroup_reps"] = subgroup_types([(12, 53), (53, 33), (1, 6)])
print("T: order-4 subgroups by type", res["T_subgroups"], flush=True)
g1, g2 = (11, 47), (35, 8)
assert TYPE[wtype(g1, g2)] == "B"
signs = {}
for s1 in (1, -1):
    for s2 in (1, -1):
        signs[f"{s1},{s2}"] = minval(space([(g1, s1), (g2, s2)]), 8)[0]
res["typeB_code_space_minima"] = signs
print("type-B code space minima by sign:", signs, flush=True)
gS = [(g1, 1), (g2, 1)]; Sg = [(0, 0), g1, g2, (g1[0] ^ g2[0], g1[1] ^ g2[1])]
cos = {}
for (u, v) in labels:
    if all(comm((u, v), s) for s in Sg[1:]): cos.setdefault(min((u ^ s[0], v ^ s[1]) for s in Sg), []).append((u, v))
hits = []; hist = collections.Counter()
for k in cos:
    if k == (0, 0) or k in Sg: continue
    for s in (1, -1):
        v = minval(space(gS + [(k, s)]), 5)[0]; hist[round(v, 6)] += 1
        if abs(v - C8) < 1e-7: hits.append((k, s))
res["typeB_rank3_hits"] = len(hits); res["typeB_rank3_tested"] = sum(hist.values()); res["typeB_rank3_hist"] = {str(k): v for k, v in sorted(hist.items())}
print("type-B rank-3 extensions attaining c8:", len(hits), "of", res["typeB_rank3_tested"], flush=True)
if hits:
    k = hits[0][0]; res["typeB_rank3_example"] = [list(g1), list(g2), list(k)]
    res["typeB_rank3_subgroups"], _ = subgroup_types([g1, g2, k])
    print("subgroup types of that rank-3 group:", res["typeB_rank3_subgroups"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_stabiliser_types.json"), "w"), indent=1)
