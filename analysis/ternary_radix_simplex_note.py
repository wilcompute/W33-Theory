"""Ternary + triangles note (Claude track, companion to Pass 12708).  Not physics claims; checks of the arithmetic behind them.
 (a) Radix economy E(r) = r / ln r (cost ~ r states per digit x number of digits): minimum at e; base 3 vs base 2.
 (b) Balanced ternary {-1, 0, +1}: representation, negation by digit flip, no sign bit; ternary weights carry log2(3) = 1.585 bits.
 (c) 'A circle is infinitely many thin triangles': inscribed n-gon fan -> perimeter and area converge to 2 pi, pi (rate 1/n^2);
     curvature of a triangulated surface lives at vertices as deficit angles; discrete Gauss-Bonnet: sum of deficits = 2 pi chi
     (icosahedron and its geodesic refinements -> 4 pi for every refinement).
 (d) Triangles alone build surfaces; volumes need tetrahedra, d dimensions need d-simplices.  The ternary-geometric object of
     this repository, W33 = the symplectic polar space W(3,3) over GF(3): its 40 points and 40 lines (4-cliques = tetrahedra) form a
     clique complex; homology over Q and GF(3) computed here.  (Owned elsewhere: first Betti 81 of the 80-vertex Levi graph and the
     Steinberg/apartment frame, Passes BT545-BT551, BT744.)
usage: py -3 analysis/ternary_radix_simplex_note.py"""
import itertools, json, math, os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = {}

# (a)
E = {r: r / math.log(r) for r in (2, 3, 4, 10)}
out["radix_economy"] = dict(E=E, e_min=math.e, gain_3_over_2=1 - E[3] / E[2])
print(f"(a) radix economy r/ln r: 2 -> {E[2]:.4f}, e -> {math.e:.4f}, 3 -> {E[3]:.4f}, 10 -> {E[10]:.4f}; base 3 cheaper than base 2 by {100 * (1 - E[3] / E[2]):.1f}%")


# (b)
def bt(n):
    d = []
    while n:
        r = n % 3; n //= 3
        if r == 2: r = -1; n += 1
        d.append(r)
    return d[::-1] or [0]


val = lambda d: sum(x * 3 ** i for i, x in enumerate(reversed(d)))
for n in (-13, 0, 7, 2026):
    assert val(bt(n)) == n and bt(-n) == [-x for x in bt(n)]
s = lambda d: "".join({1: "+", 0: "0", -1: "-"}[x] for x in d)
print(f"(b) balanced ternary: 2026 = {s(bt(2026))}, -2026 = {s(bt(-2026))} (negation = flip every trit); ternary weight = {math.log2(3):.3f} bits")
out["balanced_ternary"] = {n: s(bt(n)) for n in (-13, 7, 2026)}

# (c) polygon fan and discrete Gauss-Bonnet
fan = [(n, n * math.sin(math.pi / n) * 2, n / 2 * math.sin(2 * math.pi / n)) for n in (3, 6, 12, 96, 10000)]
for n, per, area in fan:
    print(f"(c) {n:5d} triangles: perimeter {per:.6f} (2pi = {2 * math.pi:.6f}), area {area:.6f} (pi = {math.pi:.6f})")
phi = (1 + 5 ** .5) / 2
V = [np.array(v, float) for v in ([0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi], [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
                                   [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1])]
V = [v / np.linalg.norm(v) for v in V]
Fc = [f for f in itertools.combinations(range(12), 3) if all(abs(np.linalg.norm(V[a] - V[b]) - np.linalg.norm(V[0] - V[4])) < 1e-6 for a, b in itertools.combinations(f, 2))]
assert len(Fc) == 20


def refine(V, F):
    V = list(V); mid = {}
    def m(a, b):
        k = tuple(sorted((a, b)))
        if k not in mid:
            w = V[a] + V[b]; V.append(w / np.linalg.norm(w)); mid[k] = len(V) - 1
        return mid[k]
    G = []
    for a, b, c in F:
        ab, bc, ca = m(a, b), m(b, c), m(c, a); G += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
    return V, G


def deficit_total(V, F):
    ang = np.zeros(len(V))
    for f in F:
        for i in range(3):
            a, b, c = f[i], f[(i + 1) % 3], f[(i + 2) % 3]
            u, w = V[b] - V[a], V[c] - V[a]; ang[a] += math.acos(np.clip(u @ w / np.linalg.norm(u) / np.linalg.norm(w), -1, 1))
    return float(np.sum(2 * math.pi - ang)), float(np.max(2 * math.pi - ang))


VV, FF = V, Fc; gb = []
for lev in range(4):
    tot, mx = deficit_total(VV, FF); Ecount = len(FF) * 3 // 2
    gb.append(dict(level=lev, V=len(VV), E=Ecount, F=len(FF), chi=len(VV) - Ecount + len(FF), total_deficit_over_pi=tot / math.pi, max_deficit=mx))
    print(f"(c) geodesic sphere level {lev}: V-E+F = {len(VV) - Ecount + len(FF)}, total deficit = {tot / math.pi:.10f} pi, largest single deficit {mx:.4f} rad")
    VV, FF = refine(VV, FF)
assert all(abs(g["total_deficit_over_pi"] - 4) < 1e-9 for g in gb)
out["gauss_bonnet"] = gb

# (d) W33 clique complex
pts = []
for v in itertools.product(range(3), repeat=4):
    if any(v):
        f = next(x for x in v if x); pts.append(tuple((x * (1 if f == 1 else 2)) % 3 for x in v))
pts = sorted(set(pts)); assert len(pts) == 40
J = lambda x, y: (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3
adj = {(i, j) for i in range(40) for j in range(40) if i != j and J(pts[i], pts[j]) == 0}
edges = [e for e in itertools.combinations(range(40), 2) if e in adj]
tri = [t for t in itertools.combinations(range(40), 3) if all(p in adj for p in itertools.combinations(t, 2))]
tet = [t for t in itertools.combinations(range(40), 4) if all(p in adj for p in itertools.combinations(t, 2))]

assert (len(edges), len(tri), len(tet)) == (240, 160, 40)


def bd(hi, lo):
    idx = {s: i for i, s in enumerate(lo)}; B = np.zeros((len(lo), len(hi)), int)
    for j, s in enumerate(hi):
        for k in range(len(s)):
            B[idx[s[:k] + s[k + 1:]], j] = (-1) ** k
    return B


def rank_mod(A, p):
    A = A.copy() % p; r = 0; rows, cols = A.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i, c]), None)
        if piv is None: continue
        A[[r, piv]] = A[[piv, r]]; A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        for i in range(rows):
            if i != r and A[i, c]: A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
    return r


verts = [(i,) for i in range(40)]
B1, B2, B3 = bd(edges, verts), bd(tri, edges), bd(tet, tri)
assert not (B1 @ B2).any() and not (B2 @ B3).any()
betti = {}
for field, rk in (("Q", lambda A: np.linalg.matrix_rank(A.astype(float))), ("GF(3)", lambda A: rank_mod(A, 3)), ("GF(2)", lambda A: rank_mod(A, 2))):
    r1, r2, r3 = rk(B1), rk(B2), rk(B3)
    betti[field] = [40 - r1, 240 - r1 - r2, 160 - r2 - r3, 40 - r3]
    print(f"(d) W33 clique complex (40 vertices, 240 edges, 160 triangles, 40 tetrahedra; chi = -80) Betti over {field}: {betti[field]}")
out["w33_clique_complex"] = dict(f_vector=[40, 240, 160, 40], chi=-80, betti=betti)
json.dump(out, open(os.path.join(ROOT, "data", "ternary_radix_simplex_note.json"), "w"), indent=1, default=int)
