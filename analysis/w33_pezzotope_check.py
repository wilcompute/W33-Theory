"""The E6 pezzotope (Early-Geiger-Panizzut-Sturmfels-Yun, arXiv:2306.13604): each of the 432 W(E6)-equivalent regions of the real
moduli space of marked cubic surfaces is a simple 4-polytope with f-vector (45, 90, 60, 15); 15 facets = 10 of type A1 (roots)
+ 5 of type A2^3 (cusps); a positive geometry.  Pass 12634: A2^3 cusps = W(3,3) lines (Q(4,3) points).

Derived constraints (fan: no cone has two (b) rays): the 5 cube facets are pairwise disjoint; each cube meets 6 root facets, each
root facet meets 3 cubes and 6 roots.  S5 ansatz: cubes T_1..T_5, roots r_ab (a<b in 1..5), r_ab in T_i iff i not in {a,b}.
Search: all 5-sets of A2^3 subsystems in which every 3 of them share exactly one positive root, and those 10 roots are distinct;
then check (i) root orthogonality pattern, (ii) the face numbers of the induced subcomplex of the reconstructed Naruki fan equal
the pezzotope's dual counts (15 rays, 60 2-cones, 90 3-cones, 45 4-cones), (iii) the number of configurations (expect 432),
(iv) in W(3,3) language: the 5 lines are pairwise disjoint (share 3 roots) and whether they extend to a spread (10 pairwise
disjoint lines = ovoid of Q(4,3)), and how many extensions.
usage: py -3 analysis/w33_pezzotope_check.py"""
import itertools
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_pass12634_naruki_fan.py"), encoding="utf-8").read().split("# --- Check 1")[0]
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12634_naruki_fan.py")}
exec(src, g)
IP, T3, roots_of = g["IP"], g["T3"], g["roots_of"]
n = 40
share = [[len(roots_of[s] & roots_of[t]) for t in range(n)] for s in range(n)]
disjoint_lines = [[s != t and share[s][t] == 3 for t in range(n)] for s in range(n)]  # W(3,3)-disjoint lines = non-collinear in Q(4,3)

# 5-cliques of pairwise disjoint lines
cliques = []
def extend(cl, cand):
    if len(cl) == 5:
        cliques.append(tuple(cl)); return
    for i, v in enumerate(cand):
        extend(cl + [v], [w for w in cand[i + 1:] if disjoint_lines[v][w]])
extend([], list(range(n)))
configs = []
for C in cliques:
    ok = True
    r = {}
    for trip in itertools.combinations(range(5), 3):
        common = roots_of[C[trip[0]]] & roots_of[C[trip[1]]] & roots_of[C[trip[2]]]
        if len(common) != 1:
            ok = False; break
        a, b = sorted(set(range(5)) - set(trip))
        r[(a, b)] = next(iter(common))
    if ok and len(set(r.values())) == 10:
        configs.append((C, r))
print("5-sets of pairwise disjoint W(3,3) lines:", len(cliques), "| satisfying the S5 triple condition:", len(configs))


def fan_faces(rays_a, rays_b):
    """faces of the reconstructed Naruki fan whose rays all lie in the given sets"""
    A = sorted(rays_a)
    orth = lambda S: all(IP[x, y] == 0 for x, y in itertools.combinations(S, 2))
    cnt = Counter()
    for k in range(1, 5):
        for S in itertools.combinations(A, k):
            if orth(S):
                cnt[k] += 1
    for t in rays_b:
        A2f = sorted(T3[t], key=min)
        for k in range(0, 4):
            for fac in itertools.combinations(A2f, k):
                for pick in itertools.product(*[sorted(x) for x in fac]):
                    if all(p in rays_a for p in pick):
                        cnt[k + 1] += 1
    return [cnt[1], cnt[2], cnt[3], cnt[4]]


rows = []
for C, r in configs:
    ra = set(r.values())
    fv = fan_faces(ra, C)
    orth_pat = Counter((len(set(p) & set(q)) > 0, IP[r[p], r[q]] == 0) for p, q in itertools.combinations(r, 2))
    rows.append(dict(fan_faces=fv, orth_pattern={str(k): v for k, v in orth_pat.items()}))
    if len(rows) <= 3: print("config", C, "induced fan faces", fv, "(pezzotope dual: [15, 60, 90, 45]) | (pairs intersect, roots orthogonal):", dict(orth_pat))

# spreads: maximal sets of pairwise disjoint lines (size 10 expected)
spreads = []
def ext10(cl, cand):
    if len(cl) == 10:
        spreads.append(frozenset(cl)); return
    for i, v in enumerate(cand):
        ext10(cl + [v], [w for w in cand[i + 1:] if disjoint_lines[v][w]])
ext10([], list(range(n)))
ext_counts = Counter(sum(set(C) <= S for S in spreads) for C, _ in configs)
print("spreads (10 pairwise disjoint lines):", len(spreads), "| extensions of each pezzotope 5-set to a spread:", dict(ext_counts))
res = dict(n_disjoint_5sets=len(cliques), n_pezzotope_configs=len(configs), sample=rows, n_spreads=len(spreads), spread_extensions=dict(ext_counts),
           expect_432=len(configs) == 432, faces_match=all(x["fan_faces"] == [15, 60, 90, 45] for x in rows))
json.dump(res, open(os.path.join(ROOT, "data", "w33_pezzotope_check.json"), "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in res.items() if k != "sample"}))
