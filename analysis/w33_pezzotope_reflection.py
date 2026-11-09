"""Item 1: which W(E6) element maps a pezzotope to its opposite-chirality partner over the same codeword (Pass 12634 addendum 4)?
Candidate: the reflection s_alpha in the root alpha of the pezzotope's double-six (alpha = the unique positive root pairing
non-trivially with exactly the 12 double-six lines); s_alpha has det -1 (outer coset of PSp(4,3) = W(E6)+) and swaps the two sixes.
Test on all 216 codeword pairs: s_alpha(left pentad) == right pentad?  Control: a reflection in a root orthogonal to alpha must not.
usage: py -3 analysis/w33_pezzotope_reflection.py"""
import itertools
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
gz = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pezzotope_gosset.py")}
exec(open(os.path.join(HERE, "w33_pezzotope_gosset.py"), encoding="utf-8").read().split("# candidate canonical line sets")[0], gz)
pents, POS, IP, T3, roots_of, RL, np = (gz[k] for k in ("pents", "POS", "IP", "T3", "roots_of", "RL", "np"))
key = gz["g"]["key"]
PI = gz["g"]["PI"]
Tindex = {roots_of[t]: t for t in range(40)}

def reflect_perm(a):
    al = POS[a]
    return [PI[key(POS[i] - (2 * (POS[i] @ al) // (al @ al)) * al)] for i in range(36)]

def image_pentad(C, perm):
    return frozenset(Tindex[frozenset(perm[x] for x in roots_of[t])] for t in C)

info = []
for C, r in pents:
    keys = sorted(r); R = [r[k] for k in keys]
    twelve = frozenset(l for l in range(27) if sum(abs(RL[R[x], l]) > 1e-6 for x in range(10)) == 5)
    alphas = [a for a in range(36) if frozenset(l for l in range(27) if abs(RL[a, l]) > 1e-6) == twelve]
    fifteen = [l for l in range(27) if sum(abs(RL[R[x], l]) > 1e-6 for x in range(10)) == 4]
    nz = {l: [keys[x] for x in range(10) if abs(RL[R[x], l]) > 1e-6] for l in fifteen}
    tot = frozenset(frozenset(l for l in fifteen if (set(range(5)) - {x for e in nz[l] for x in e}).pop() == m) for m in range(5))
    info.append(dict(C=frozenset(C), alphas=alphas, key=(twelve, tot)))
assert all(len(x["alphas"]) == 1 for x in info)
by_key = {}
for x in info:
    by_key.setdefault(x["key"], []).append(x)
hit, ctrl_hit = Counter(), Counter()
for k, (p, q) in ((k, v) for k, v in by_key.items()):
    a = p["alphas"][0]
    img = image_pentad(p["C"], reflect_perm(a))
    hit[img == q["C"]] += 1
    b = next(b for b in range(36) if IP[a, b] == 0)
    ctrl_hit[image_pentad(p["C"], reflect_perm(b)) == q["C"]] += 1
res = dict(reflection_in_double_six_root_maps_left_to_right=dict(hit), control_orthogonal_root=dict(ctrl_hit),
           all_216=hit.get(True, 0) == 216 and ctrl_hit.get(True, 0) == 0)
print("s_alpha(left) == right partner:", dict(hit), "| control (orthogonal root):", dict(ctrl_hit))
json.dump(res, open(os.path.join(ROOT, "data", "w33_pezzotope_reflection.json"), "w"), indent=1)

# --- Item 4: is the corpus codeword (Pass 173 / P12523: minimal even line set, 10 lines, 216 of them) = left pentad U right pentad? --
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_split_bridge.py")}
exec(open(os.path.join(HERE, "w33_split_bridge.py"), encoding="utf-8").read().split("# (ii) roots -> spreads")[0], ns)
phi, lines = ns["phi"], ns["lines"]
unions = []
for k, (p, q) in by_key.items():
    U = frozenset(phi[t] for t in p["C"]) | frozenset(phi[t] for t in q["C"])
    unions.append(U)
def point_degrees(U):
    return Counter(sum(1 for L in U if pt in lines[L]) for pt in range(40))
even = [all(d % 2 == 0 for d in point_degrees(U).values()) for U in unions]
deg_profile = Counter(tuple(sorted(point_degrees(U).items())) for U in unions)
found = None  # total count of 10-line even sets is certified in the corpus (Pass 173: 216); not recomputed here
res.update(unions_size=sorted({len(U) for U in unions}), unions_even=all(even), union_point_degree_profile={str(k): v for k, v in deg_profile.items()},
           n_distinct_unions=len(set(unions)), corpus_count_pass173=216)
print("unions: sizes", res["unions_size"], "even:", res["unions_even"], "| point degree profile:", res["union_point_degree_profile"])
print("distinct unions:", len(set(unions)), "(corpus Pass 173: 216 minimal even 10-line sets)")
json.dump(res, open(os.path.join(ROOT, "data", "w33_pezzotope_reflection.json"), "w"), indent=1)
