"""Outside-the-box 3: is the unique 60480-orbit of Lagrangian triples (pairwise intersection dims 0,1,2; Sp(6,2)-stabiliser 24)
structurally the E7 pezzotope?  E7 pezzotope facets (Early-Geiger-Panizzut-Sturmfels-Yun): 10 A1 + 12 A2 + 9 A3^2 + 3 A7 = 34.
Roots (A1) <-> points of W(5,2) (63).  For one scalene triple, classify the 63 points by (planes containing it, planes it is orthogonal
to) and look for natural classes of sizes 10 / 12 / 9 / 3.
usage: py -3 analysis/w33_e7_scalene.py"""
import itertools, json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_e7_rung_mubs.py")}
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_e7_rung_mubs.py"), encoding="utf-8").read().split("G = nx.Graph()")[0], ns)
P, lag, w = ns["P"], ns["lag"], ns["w"]
dimI = lambda a, b: {0: 0, 1: 1, 3: 2, 7: 3}[len(lag[a] & lag[b])]
tri = next(t for t in itertools.combinations(range(len(lag)), 3) if sorted(dimI(a, b) for a, b in itertools.combinations(t, 2)) == [0, 1, 2])
def perp_to_plane(p, L):
    return all(w(P[p], P[x]) == 0 for x in lag[L])
cls = Counter()
members = {}
for p in range(63):
    key = (tuple(int(p in lag[L]) for L in tri), tuple(int(perp_to_plane(p, L)) for L in tri))
    cls[key] += 1
    members.setdefault(key, []).append(p)
print("triple pairwise dims:", [dimI(a, b) for a, b in itertools.combinations(tri, 2)])
print("63 points by (on plane i?, orthogonal to plane i?) for the 3 planes:")
for k, v in sorted(cls.items(), key=lambda x: -x[1]):
    print("  ", k, v)
sizes = sorted(cls.values())
res = dict(classes={str(k): v for k, v in cls.items()}, sizes=sizes, has_10=10 in sizes, has_12=12 in sizes, has_9=9 in sizes)
json.dump(res, open(os.path.join(ROOT, "data", "w33_e7_scalene.json"), "w"), indent=1)

# --- exact stabiliser: choose complementary Lagrangians L2 = <e1,e2,e3>, L3 = <f1,f2,f3> (w pairs coords 0-3, 1-4, 2-5); the
#     stabiliser of (L2, L3) in Sp(6,2) is GL(3,2) acting as (A, A^-T).  Pick L1 with dim(L1 cap L2) = 2, dim(L1 cap L3) = 1; keep the
#     A with g(L1) = L1.  Then orbits on the 63 points (roots) and on the 135 planes.
import numpy as np
idx = {p: i for i, p in enumerate(P)}
L2 = frozenset(idx[p] for p in P if p[3] == p[4] == p[5] == 0)
L3 = frozenset(idx[p] for p in P if p[0] == p[1] == p[2] == 0)
li = {L: i for i, L in enumerate(lag)}
i2, i3 = li[L2], li[L3]
L1i = next(i for i in range(len(lag)) if dimI(i, i2) == 2 and dimI(i, i3) == 1)
mats = []
for bits in itertools.product(range(2), repeat=9):
    A = np.array(bits).reshape(3, 3)
    if round(np.linalg.det(A)) % 2 == 1:
        mats.append(A)
assert len(mats) == 168
def inv2(A):
    for B in mats:
        if ((A @ B) % 2 == np.eye(3, dtype=int)).all():
            return B
def act(A, Ainvt, p):
    x = (A @ np.array(p[:3])) % 2; y = (Ainvt @ np.array(p[3:])) % 2
    return idx[tuple(int(t) for t in np.concatenate([x, y]))]
stab = []
for A in mats:
    Ait = inv2(A).T
    perm = [act(A, Ait, p) for p in P]
    if frozenset(perm[x] for x in lag[L1i]) == lag[L1i]:
        stab.append(perm)
print("stabiliser of the scalene triple (L1, L2, L3) inside GL(3,2):", len(stab))
# group structure: element orders
def order(perm):
    k, cur = 1, perm[:]
    while cur != list(range(63)):
        cur = [perm[c] for c in cur]; k += 1
    return k
oc = Counter(order(g) for g in stab)
print("element orders:", dict(sorted(oc.items())), "(S4: 1:1, 2:9, 3:8, 4:6)")
def orbits(n, apply):
    seen, out = set(), []
    for x in range(n):
        if x in seen: continue
        O = {x}; todo = [x]
        while todo:
            y = todo.pop()
            for g in stab:
                z = apply(g, y)
                if z not in O: O.add(z); todo.append(z)
        seen |= O; out.append(len(O))
    return sorted(out)
pt_orb = orbits(63, lambda g, y: g[y])
pl_orb = orbits(len(lag), lambda g, y: li[frozenset(g[x] for x in lag[y])])
print("stabiliser orbits on the 63 points:", pt_orb)
print("stabiliser orbits on the 135 planes:", pl_orb)
res.update(stab_order=len(stab), element_orders=dict(oc), point_orbits=pt_orb, plane_orbits=pl_orb)
json.dump(res, open(os.path.join(ROOT, "data", "w33_e7_scalene.json"), "w"), indent=1)
