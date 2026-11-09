"""Item 2: hidden zeros.  Tr phi^3 amplitudes vanish on 'maximal rectangles' of mesh variables (Arkani-Hamed, Cao, Dong, Figueiredo,
He 2023): for n = 6, c_13 = c_14 = c_15 = 0 with c_ij = X_ij + X_{i+1,j+1} - X_{i,j+1} - X_{i+1,j}, X_{i,i+1} = 0.
(0) Control: the 6-point amplitude A6 = sum over the 14 triangulations of prod 1/X vanishes there (and not at random points).
(1) The pezzotope amplitude m = sum over its 45 vertices of prod 1/X_f (15 facet variables).  On each root facet r the hexagon labels
are fixed by the particle identification (w33_six_particles.py): short diagonal X_{i,i+2} = the root of duad (a_i, a_{i+1}); long
diagonal X_{i,i+3} = the cusp compatible with X_{i,i+2}, X_{i+1,i+3}, X_{i+3,i+5}, X_{i+4,i}.  Impose the facet's hexagon zero on its 9
neighbour variables (X_r and the other 5 facet variables random) and evaluate m.  Also the residue Res_{X_r} m (must vanish: = A6).
(2) Search: does m vanish if hexagon zeros are imposed on several root facets at once, up to all compatible choices?
usage: py -3 analysis/w33_pezzotope_hidden_zeros.py"""
import itertools, json, os
from collections import Counter
from fractions import Fraction as Fr
import random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
gz = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pezzotope_gosset.py")}
exec(open(os.path.join(HERE, "w33_pezzotope_gosset.py"), encoding="utf-8").read().split("# candidate canonical line sets")[0], gz)
pents, IP, T3, RL, roots_of, G_, v_skew = (gz[k] for k in ("pents", "IP", "T3", "RL", "roots_of", "G", "v_skew"))
rnd = random.Random(7)
# --- hexagon
diag = [(i, j) for i, j in itertools.combinations(range(6), 2) if (j - i) % 6 not in (1, 5)]
def crosses(a, b):
    (i, j), (k, l) = a, b
    if len({i, j, k, l}) < 4:
        return False
    return (i < k < j) != (i < l < j)
tri = [T for T in itertools.combinations(diag, 3) if not any(crosses(a, b) for a, b in itertools.combinations(T, 2))]
assert len(tri) == 14
def A6(X):
    return sum(Fr(1) / (X[T[0]] * X[T[1]] * X[T[2]]) for T in tri)
def Xget(X, i, j):
    i, j = i % 6, j % 6
    if i == j or (j - i) % 6 in (1, 5):
        return Fr(0)
    return X[(min(i, j), max(i, j))]
def zero_point():
    # random X on the hexagon with c_13 = c_14 = c_15 = 0 (0-based: c_02 = c_03 = c_04 = 0)
    while True:
        X = {d: Fr(rnd.randint(1, 50)) for d in diag}
        # c_{0,j} = X_{0j} + X_{1,j+1} - X_{0,j+1} - X_{1,j}: solve for X_{0,j+1} successively (j=2,3) and X_{1,5}... use X_{0,3}, X_{0,4}, X_{1,5}
        X[(0, 3)] = Xget(X, 0, 2) + Xget(X, 1, 3) - Xget(X, 1, 2)
        X[(0, 4)] = Xget(X, 0, 3) + Xget(X, 1, 4) - Xget(X, 1, 3)
        # c_{0,4} = X_04 + X_15 - X_05 - X_14 = 0, X_05 = 0 (adjacent): X_15 = X_14 - X_04
        X[(1, 5)] = Xget(X, 1, 4) - Xget(X, 0, 4)
        if all(v != 0 for v in X.values()):
            return X
cz = [A6(zero_point()) for _ in range(5)]
cr = [A6({d: Fr(rnd.randint(1, 50)) for d in diag}) for _ in range(5)]
print("control A6 at hidden-zero points:", [str(v) for v in cz], "| at random points nonzero:", all(v != 0 for v in cr))

# --- pezzotope
skew = lambda i, j: abs(G_[i, j] - v_skew) < 1e-6
def pezzo(C, r):
    ra = sorted(r.values())
    verts = []
    for S in itertools.combinations(ra, 4):
        if all(IP[x, y] == 0 for x, y in itertools.combinations(S, 2)):
            verts.append(frozenset(("a", x) for x in S))
    for t in C:
        for pick in itertools.product(*[sorted(A) for A in sorted(T3[t], key=min)]):
            if all(p in ra for p in pick):
                verts.append(frozenset([("b", t)] + [("a", p) for p in pick]))
    return ra, verts
def hexagon_labels(root, verts):
    f = ("a", root)
    vf = [v - {f} for v in verts if f in v]
    nb = sorted({g[1] for v in vf for g in v if g[0] == "a"})
    cus = sorted({g[1] for v in vf for g in v if g[0] == "b"})
    together = {frozenset(p) for v in vf for p in itertools.combinations(sorted(v, key=str), 2)}
    A = [l for l in range(27) if RL[root, l] > 1e-6]
    D = {s: frozenset(l for l in A if abs(RL[s, l]) > 1e-6) for s in nb}
    # cyclic order of the six lines from the duad cycle
    adj = {l: [m for s in nb for m in D[s] if l in D[s] and m != l] for l in A}
    order = [A[0], adj[A[0]][0]]
    while len(order) < 6:
        order.append([m for m in adj[order[-1]] if m != order[-2]][0])
    pos = {l: i for i, l in enumerate(order)}
    lab = {}
    for s in nb:  # duad (a_i, a_{i+1}) -> X_{i,i+2}
        i, j = sorted(pos[l] for l in D[s])
        i = j if (j - i) == 5 else i
        lab[("a", s)] = (i % 6, (i + 2) % 6)
    for t in cus:  # long diagonal (i, i+3): compatible with X_{i,i+2}, X_{i+1,i+3}, X_{i+3,i+5}, X_{i+4,i}
        comp = {lab[("a", s)] for s in nb if frozenset((("a", s), ("b", t))) in together}
        for i in range(3):
            want = {(i, (i + 2) % 6), ((i + 1) % 6, (i + 3) % 6), ((i + 3) % 6, (i + 5) % 6), ((i + 4) % 6, i % 6)}
            if comp == want:
                lab[("b", t)] = (i, i + 3)
    norm = lambda d: (min(d), max(d))
    return {k: norm(v) for k, v in lab.items()}
def m_of(verts, X):
    return sum(Fr(1) / (X[a] * X[b] * X[c] * X[d]) for a, b, c, d in (tuple(v) for v in verts))
summary = Counter()
for C, r in pents[:40]:
    ra, verts = pezzo(C, r)
    facets = [("a", x) for x in ra] + [("b", t) for t in C]
    for root in ra:
        lab = hexagon_labels(root, verts)
        if len(lab) != 9:
            summary["label_fail"] += 1
            continue
        vals = []
        for _ in range(3):
            Xh = zero_point()
            X = {f: Fr(rnd.randint(1, 50)) for f in facets}
            for f, d in lab.items():
                X[f] = Xh[d]
            vals.append(m_of(verts, X))
            # residue at X_root: terms containing the root facet, with X_root factor removed
            res_ = sum(Fr(1) / (X[a] * X[b] * X[c]) for v in verts if ("a", root) in v for a, b, c in [tuple(sorted(v - {("a", root)}, key=str))])
            summary[("residue_zero", res_ == 0)] += 1
        summary[("full_m_zero", all(v == 0 for v in vals))] += 1
print("first 40 pezzotopes x 10 root facets:", dict(summary))
res = dict(control_zero=all(v == 0 for v in cz), control_random_nonzero=all(v != 0 for v in cr), summary={str(k): v for k, v in summary.items()})
json.dump(res, open(os.path.join(ROOT, "data", "w33_pezzotope_hidden_zeros.json"), "w"), indent=1)

# --- (2) simultaneous hexagon zeros on k root facets (k = 2, 3), every rotation of the skinny rectangle per facet (6 rotations),
#     linear system on the 15 facet variables; random rational point of the solution space with all X != 0; test m == 0.
import sympy as sp
C, r = pents[0]
ra, verts = pezzo(C, r)
facets = [("a", x) for x in ra] + [("b", t) for t in C]
fidx = {f: i for i, f in enumerate(facets)}
labs = {root: hexagon_labels(root, verts) for root in ra}
def rect_eqs(root, k):
    inv = {d: f for f, d in labs[root].items()}
    def var(i, j):
        i, j = i % 6, j % 6
        if i == j or (j - i) % 6 in (1, 5):
            return None
        return inv[(min(i, j), max(i, j))]
    eqs = []
    for j in (k + 2, k + 3, k + 4):  # c_{k,j}, j = k+2..k+4
        row = [0] * 15
        for (a, b), sgn in (((k, j), 1), ((k + 1, j + 1), 1), ((k, j + 1), -1), ((k + 1, j), -1)):
            f = var(a, b)
            if f is not None:
                row[fidx[f]] += sgn
        eqs.append(row)
    return eqs
found = Counter()
examples = []
for kk in (2, 3):
    for roots in itertools.combinations(ra, kk):
        for rots in itertools.product(range(6), repeat=kk):
            M = sp.Matrix([row for rt, k in zip(roots, rots) for row in rect_eqs(rt, k)])
            ns = M.nullspace()
            if not ns:
                found[(kk, "no_solution")] += 1
                continue
            hit = None
            for _ in range(3):
                vec = sum((sp.Rational(rnd.randint(-40, 40)) * v for v in ns), sp.zeros(15, 1))
                if any(x == 0 for x in vec):
                    continue
                X = {f: Fr(int(sp.fraction(vec[fidx[f]])[0]), int(sp.fraction(vec[fidx[f]])[1])) for f in facets}
                hit = (m_of(verts, X) == 0)
                break
            found[(kk, "m_zero" if hit else ("m_nonzero" if hit is False else "degenerate"))] += 1
            if hit:
                examples.append((kk, [str(x) for x in roots], rots))
print("simultaneous zeros (k facets, outcome): count", dict(found))
res["simultaneous"] = {str(k): v for k, v in found.items()}
res["simultaneous_examples"] = examples[:10]
json.dump(res, open(os.path.join(ROOT, "data", "w33_pezzotope_hidden_zeros.json"), "w"), indent=1)

# --- verify the hits on 6 fresh random points of the solution space each, and characterise them
ver = Counter(); shapes = Counter()
all_hits = []
for kk in (2, 3):
    for roots in itertools.combinations(ra, kk):
        for rots in itertools.product(range(6), repeat=kk):
            M = sp.Matrix([row for rt, k in zip(roots, rots) for row in rect_eqs(rt, k)])
            ns = M.nullspace()
            if not ns:
                continue
            vals = []
            for _ in range(12):
                vec = sum((sp.Rational(rnd.randint(-60, 60)) * v for v in ns), sp.zeros(15, 1))
                if any(x == 0 for x in vec):
                    continue
                X = {f: Fr(int(sp.fraction(vec[fidx[f]])[0]), int(sp.fraction(vec[fidx[f]])[1])) for f in facets}
                vals.append(m_of(verts, X) == 0)
                if len(vals) == 6:
                    break
            if vals and any(vals):
                ver[(kk, all(vals), len(vals))] += 1
                if all(vals):
                    keys = [k_ for k_, v in r.items() if v in roots]
                    orth = sum(1 for a, b in itertools.combinations(roots, 2) if IP[a, b] == 0)
                    shapes[(kk, tuple(sorted(keys)), orth, len(ns))] += 1
                    all_hits.append((kk, [list(k) for k in keys], list(rots), len(ns)))
print("hits re-tested (k, zero at all fresh points, #points): count", dict(ver))
print("genuine zero configurations (k, K5 edge labels of the facets, # orthogonal pairs, solution dim):")
for k_, v in sorted(shapes.items(), key=str):
    print("  ", k_, v)
res["verified_hits"] = {str(k): v for k, v in ver.items()}
res["genuine_zero_shapes"] = {str(k): v for k, v in shapes.items()}
res["genuine_zero_list"] = all_hits
json.dump(res, open(os.path.join(ROOT, "data", "w33_pezzotope_hidden_zeros.json"), "w"), indent=1)
