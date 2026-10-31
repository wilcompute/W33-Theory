"""12501: the q = 9 48-line even set inside the 288 W-lines that miss the hyperbolic quadric swept by its 12 free lines
(free lines = {X, Y} u {X, Y}^perp, K_{2,10}).  Orbits of H = Stab_{PSp(4,9)}({X, Y}) = GL(2,9) (x on X, M^{-T} on Y) . 2 on those 288
passant lines; is the 48-set a union of H-orbits?  usage: py -3 passant_orbits.py"""
import json, itertools, collections, random
import networkx as nx
from symmetric_fast import fast_build
from symmetric_even_sets_gf import setup

q = 9
pts, lines = fast_build(q); F, add, mul, inv, neg = setup(q)
pid = {p: i for i, p in enumerate(pts)}; sets = [frozenset(l) for l in lines]; lid = {L: j for j, L in enumerate(lines)}
S = set(json.load(open("symmetric_fast_q9_r10.json"))[0]["chosen"])
cov = set().union(*(sets[j] for j in S))
free = [j for j in range(len(lines)) if not (sets[j] & cov)]
Fg = nx.Graph(); Fg.add_nodes_from(free); Fg.add_edges_from((a, b) for a, b in itertools.combinations(free, 2) if sets[a] & sets[b])
X, Y = [v for v, d in Fg.degree() if d == 10]
Q = set().union(*(sets[r] for r in free if r not in (X, Y)))
pas = [j for j in range(len(lines)) if not (sets[j] & Q)]


def w(u, v):
    s = add[mul[u[0]][v[2]]][mul[u[1]][v[3]]]
    return add[s][neg[add[mul[u[2]][v[0]]][mul[u[3]][v[1]]]]]


def scal(c, v): return tuple(mul[c][x] for x in v)
def vadd(u, v): return tuple(add[a][b] for a, b in zip(u, v))
xs = [pts[p] for p in lines[X]]; ys = [pts[p] for p in lines[Y]]
x1 = xs[0]; x2 = next(v for v in xs[1:])
# dual basis y1, y2 in span(Y): w(x_i, y_j) = delta_ij
Yvecs = [scal(c, v) for v in ys for c in F if c]
y1 = next(v for v in Yvecs if w(x1, v) == 1 and w(x2, v) == 0)
y2 = next(v for v in Yvecs if w(x1, v) == 0 and w(x2, v) == 1)


def coords(v):            # v = a1 x1 + a2 x2 + b1 y1 + b2 y2:  a_j = w(v, y_j), b_i = w(x_i, v)
    return (w(v, y1), w(v, y2), w(x1, v), w(x2, v))


def from_coords(a1, a2, b1, b2):
    return vadd(vadd(scal(a1, x1), scal(a2, x2)), vadd(scal(b1, y1), scal(b2, y2)))


def norm(v):
    s = inv[next(t for t in v if t)]; return tuple(mul[s][t] for t in v)


def mat2(M, a, b): return (add[mul[M[0][0]][a]][mul[M[0][1]][b]], add[mul[M[1][0]][a]][mul[M[1][1]][b]])


def inv_T(M):              # (M^{-1})^T
    det = add[mul[M[0][0]][M[1][1]]][neg[mul[M[0][1]][M[1][0]]]]; d = inv[det]
    Mi = ((mul[d][M[1][1]], mul[d][neg[M[0][1]]]), (mul[d][neg[M[1][0]]], mul[d][M[0][0]]))
    return ((Mi[0][0], Mi[1][0]), (Mi[0][1], Mi[1][1]))


def elem(M):
    MT = inv_T(M)
    def g(p):
        a1, a2, b1, b2 = coords(pts[p]); na = mat2(M, a1, a2); nb = mat2(MT, b1, b2)
        return pid[norm(from_coords(na[0], na[1], nb[0], nb[1]))]
    return g


def swap(p):
    a1, a2, b1, b2 = coords(pts[p])          # x_i -> y_i, y_i -> -x_i preserves w
    return pid[norm(from_coords(neg[b1], neg[b2], a1, a2))]


rng = random.Random(2); gens = []
while len(gens) < 4:
    M = tuple(tuple(rng.choice(F) for _ in range(2)) for _ in range(2))
    if add[mul[M[0][0]][M[1][1]]][neg[mul[M[0][1]][M[1][0]]]] != 0: gens.append(elem(M))
gens.append(swap)
lperms = []
for g in gens:
    pm = [g(p) for p in range(len(pts))]
    lperms.append({j: lid[tuple(sorted(pm[x] for x in lines[j]))] for j in pas})
assert all(set(lp.values()) == set(pas) for lp in lperms), "H must preserve the passant lines"
seen, orbits = set(), []
for j in pas:
    if j in seen: continue
    orb = {j}; fr = [j]
    while fr:
        nx_ = []
        for t in fr:
            for lp in lperms:
                u = lp[t]
                if u not in orb: orb.add(u); nx_.append(u)
        fr = nx_
    seen |= orb; orbits.append(orb)
sizes = sorted(len(o) for o in orbits)
in_S = sorted((len(o), len(o & S)) for o in orbits)
out = dict(passants=len(pas), orbit_sizes=sizes, orbit_hits_by_S=in_S, S_union_of_orbits=all(len(o & S) in (0, len(o)) for o in orbits))
print(json.dumps(out)); json.dump(out, open("passant_orbits_q9.json", "w"))
