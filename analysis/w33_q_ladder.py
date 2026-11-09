"""Item 5: the q-ladder.  For each q, build W(3,q) (points = isotropic points of PG(3,q), lines = Lagrangian planes) and its dual
Q(4,q); test self-duality by the perp-perp size of non-collinear point pairs (W(3,q): q+1 always; Q(4,q): 2 for odd q, q+1 for even q).
Genus-2 level-q moduli A_2(q): Satake boundary = 1-cusps <-> isotropic points, 0-cusps <-> Lagrangian planes, incidence = W(3,q), for every
q (standard).  Level 2: W(3,2) self-dual -> the Segre and Igusa fans coincide (RSSS Thm 2.4).  Level 3: not self-dual -> Burkhardt sees
points, cubic surfaces see lines (Passes 12634-12635) - the second moduli space exists because W(E6) = PGSp(4,3) (exceptional).
Level 5: not self-dual (computed here); PGSp(4,5) is not a Weyl group, so no del Pezzo-type partner is expected.
usage: py -3 analysis/w33_q_ladder.py"""
import itertools, json, os
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def ladder(q):
    pts = []
    for v in itertools.product(range(q), repeat=4):
        if any(v):
            c = next(x for x in v if x)
            inv = pow(c, -1, q)
            n = tuple((x * inv) % q for x in v)
            if n not in pts:
                pts.append(n)
    w = lambda u, v: (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % q
    N = len(pts)
    A = [[i != j and w(pts[i], pts[j]) == 0 for j in range(N)] for i in range(N)]
    # lines: Lagrangian planes as point sets
    idx = {p: i for i, p in enumerate(pts)}
    def norm(v):
        c = next(x for x in v if x); inv = pow(c, -1, q); return tuple((x * inv) % q for x in v)
    lines = set()
    for i in range(N):
        for j in range(i + 1, N):
            if A[i][j]:
                S = frozenset(idx[norm(tuple((a * pts[i][k] + b * pts[j][k]) % q for k in range(4)))] for a in range(q) for b in range(q) if (a, b) != (0, 0))
                lines.add(S)
    lines = list(lines)
    LA = [[a != b and bool(lines[a] & lines[b]) for b in range(len(lines))] for a in range(len(lines))]
    def pp(Adj):
        n = len(Adj); out = Counter()
        sample = [(x, y) for x in range(n) for y in range(x + 1, n) if not Adj[x][y]][:400]
        for x, y in sample:
            C = [z for z in range(n) if Adj[x][z] and Adj[y][z]]
            out[sum(1 for v in range(n) if all(Adj[v][c] for c in C))] += 1
        return dict(out)
    return dict(q=q, points=N, lines=len(lines), point_graph_perp_perp=pp(A), line_graph_perp_perp=pp(LA))
res = [ladder(q) for q in (2, 3, 5)]
for r in res:
    sd = set(r["point_graph_perp_perp"]) == set(r["line_graph_perp_perp"])
    r["self_dual_by_perp_perp"] = sd
    print(r)
json.dump(res, open(os.path.join(ROOT, "data", "w33_q_ladder.json"), "w"), indent=1)
