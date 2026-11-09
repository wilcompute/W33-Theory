"""Pass 12635 (claude track): the tropical Burkhardt quartic (= tropical A_2(3), the corpus's genus-2 level-3 flavour modulus) is
built from W(3,3) POINTS and the 45 tensor splits; the tropical cubic-surface moduli (Pass 12634) from W(3,3) LINES.

Literature (Ren, Sam, Schrader, Sturmfels, "Tropicalization of classical moduli spaces", arXiv:1303.1132, Thm 4.3):
trop(Burkhardt) is the fan over a 2-dim simplicial complex with 85 vertices, 600 edges, 880 triangles; rays 40 (a) indexed by the
lines through 0 in F_3^4, 45 (b) indexed by pairs {b, b-perp} of orthogonal non-isotropic planes; edges 240 aa + 360 ab; triangles
160 aaa + 720 aab.

Reconstruction tested here (F_3^4 with the symplectic form):
  (a) rays = the 40 points of W(3,3);  (b) rays = the 45 splits {b, b-perp} (nondegenerate plane + its perp = a tensor factorisation
  of two-qutrit space, corpus "45 factorisations");
  aa edges = collinear (orthogonal) point pairs;  aaa triangles = three points on an isotropic line;
  ab edges = point p with p in b or b-perp;  aab triangles = (p in b, q in b-perp, the split).
Checks: all counts equal the theorem's; the aa graph is the W(3,3) point graph (perp-perp size 4, not the dual Q(4,3)).
Duality with Pass 12634: there the cusp rays were W(3,3) LINES (Q(4,3)); here the (a) rays are W(3,3) POINTS; both fans meet the
same 45 splits (here the (b) rays; there the 45 D4 classes of the aaaa cones).
usage: py -3 analysis/w33_pass12635_burkhardt_fan.py"""
import itertools
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
q = 3
vecs = [v for v in itertools.product(range(q), repeat=4) if any(v)]
norm = lambda v: next(tuple((x * pow(c, -1, q)) % q for x in v) for c in v if c)
P = sorted({norm(v) for v in vecs})
assert len(P) == 40
w = lambda u, v: (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % q
idx = {p: i for i, p in enumerate(P)}


def span_pts(gens):
    out = set()
    for coeffs in itertools.product(range(q), repeat=len(gens)):
        v = tuple(sum(c * g[k] for c, g in zip(coeffs, gens)) % q for k in range(4))
        if any(v):
            out.add(idx[norm(v)])
    return frozenset(out)


planes = {span_pts([P[i], P[j]]) for i, j in itertools.combinations(range(40), 2)}
assert all(len(pl) == 4 for pl in planes) and len(planes) == 130
iso = [pl for pl in planes if all(w(P[a], P[b]) == 0 for a in pl for b in pl)]
non = [pl for pl in planes if pl not in iso]
perp = lambda pl: frozenset(i for i in range(40) if all(w(P[i], P[a]) == 0 for a in pl))
splits = {frozenset((pl, perp(pl))) for pl in non}
splits = [tuple(s) for s in splits]
res = dict(n_points=40, n_isotropic_lines=len(iso), n_nondeg_planes=len(non), n_splits=len(splits))
coll = lambda i, j: i != j and w(P[i], P[j]) == 0
aa = [(i, j) for i, j in itertools.combinations(range(40), 2) if coll(i, j)]
aaa = sum(1 for L in iso for _ in itertools.combinations(sorted(L), 3))
ab = sum(len(b | bp) for b, bp in splits)
aab = sum(len(b) * len(bp) for b, bp in splits)
# sanity: within a split, every point of b is orthogonal to every point of b-perp, and points within b are pairwise non-orthogonal
split_ok = all(all(coll(x, y) for x in b for y in bp) and all(not coll(x, y) for x, y in itertools.combinations(sorted(b), 2)) for b, bp in splits)
res.update(rays=40 + len(splits), edges_aa=len(aa), edges_ab=ab, triangles_aaa=aaa, triangles_aab=aab, edges=len(aa) + ab, triangles=aaa + aab,
           split_orthogonality_ok=split_ok)
# point graph type: perp-perp sizes of non-collinear pairs (4 for W(3,3), 2 for Q(4,3))
A = [[coll(i, j) for j in range(40)] for i in range(40)]
pp = Counter()
for x, y in itertools.combinations(range(40), 2):
    if A[x][y]:
        continue
    C = [z for z in range(40) if A[x][z] and A[y][z]]
    pp[sum(1 for v in range(40) if all(A[v][c] for c in C))] += 1
res["aa_graph_perp_perp"] = dict(pp)
lit = dict(rays=85, edges=600, triangles=880, edges_aa=240, edges_ab=360, triangles_aaa=160, triangles_aab=720)
checks = {f"{k}_matches": res[k] == v for k, v in lit.items()}
checks.update(splits_45=len(splits) == 45, split_orthogonality=split_ok, aa_is_W33_points=dict(pp) == {4: 540})
res["checks"] = checks
res["all_checks_pass"] = all(checks.values())
res["pass_number"] = 12635
json.dump(res, open(os.path.join(ROOT, "data", "w33_pass12635_burkhardt_fan.json"), "w"), indent=1)
print({k: res[k] for k in ("rays", "edges_aa", "edges_ab", "triangles_aaa", "triangles_aab", "n_splits")}, "| theorem: 85, 240, 360, 160, 720, 45")
print("aa graph perp-perp:", dict(pp), "-> W(3,3) points" if dict(pp) == {4: 540} else "")
print("all_checks_pass", res["all_checks_pass"])
