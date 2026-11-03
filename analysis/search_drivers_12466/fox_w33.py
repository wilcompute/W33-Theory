"""12533: two-qutrit Paulis are Fox tricolourings of 6 points.  V = {c in F_3^6 : sum (-1)^i c_i = 0} / <1>, dim 4; sigma_i acts by the Fox rule (a, b) -> (b, 2b - a).  Tests:
(1) the Fox action preserves V, is a B6 rep, and sigma_i - I has rank 1 with image a_i;
(2) there is a unique invariant alternating form up to scale, non-degenerate on V; sigma_i is a transvection for it; the map a_i -> +-p_{i-1} extends to a linear similitude V -> F_3^4 intertwining Fox with the W(3,3) transvections T_{p_i} of braid_codewords.py;
(3) caps: the colourings with c1 = c2, c3 = c4, c5 = c6 map exactly to the line L0 through p0, p2, p4;
(4) plat closures: the number of Fox colourings of the diagram, by independent linear algebra on the arcs, is 3^(1 + dim(L0 meet beta L0)), and matches the Jones state sum (Przytycki: colourings = 3 |V|^2);
(5) other strand numbers 2, 4, 8 from Fox and the state sum, with no W(3,3) input.  usage: py -3 fox_w33.py"""
import collections
import itertools
import json
import random
from sympy import GF, Matrix
from sympy.polys.matrices import DomainMatrix

p = 3


def _dm(rows, ncols):
    return DomainMatrix.from_Matrix(Matrix(len(rows), ncols, [x % p for r in rows for x in r])).convert_to(GF(p))


def rank_mod(rows, ncols):
    if not rows:
        return 0
    return _dm(rows, ncols).rank()


def nullspace_mod(rows, ncols):
    return [[int(x) % p for x in r] for r in _dm(rows, ncols).nullspace().to_Matrix().tolist()]


ks = open("knots_w33.py", encoding="utf-8").read().split("# plat\n")[0]
g = {}
exec(ks, g)
bracket, rep, L0pts, path, pts, lines, w_, rand_word, dim_from_abs = (g[k] for k in ("bracket", "rep", "L0", "path", "pts", "lines", "w", "rand_word", "dim_from_abs"))


def fox(c, s):
    c = list(c)
    i = abs(s) - 1
    a, b = c[i], c[i + 1]
    if s > 0:
        c[i], c[i + 1] = b, (2 * b - a) % p
    else:
        c[i], c[i + 1] = (2 * a - b) % p, a
    return tuple(c)


n = 6
out = {}
alt = lambda c: sum((-1) ** i * x for i, x in enumerate(c)) % p
ALL = [c for c in itertools.product(range(p), repeat=n) if alt(c) == 0]
assert len(ALL) == 3 ** 5
out["fox_preserves_alternating_sum"] = all(alt(fox(c, s)) == 0 for c in ALL for s in (1, 2, 3, 4, 5, -1, -3))
canon = lambda c: tuple((x - c[0]) % p for x in c)            # mod constants: first colour zero
V = sorted({canon(c) for c in ALL})
assert len(V) == 81
out["fox_is_a_braid_rep"] = all(fox(fox(fox(c, i), i + 1), i) == fox(fox(fox(c, i + 1), i), i + 1) for c in ALL for i in range(1, 5))


def to4(c):
    c = canon(c)
    return (c[1], c[2], c[3], c[4])


def from4(v):
    c = [0, v[0], v[1], v[2], v[3], 0]
    c[5] = (c[0] - c[1] + c[2] - c[3] + c[4]) % p            # makes the alternating sum zero
    assert alt(c) == 0
    return tuple(c)


basis = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
Ms = {s: [list(to4(fox(from4(b), s))) for b in basis] for s in (1, 2, 3, 4, 5)}     # rows = images of the basis
apply = lambda M, v: tuple(sum(v[i] * M[i][j] for i in range(4)) % p for j in range(4))
out["matrix_rep_matches_fox"] = all(apply(Ms[s], to4(c)) == to4(fox(c, s)) for s in Ms for c in ALL[:60])
a = {}
for s, M in Ms.items():
    D = [[(M[i][j] - int(i == j)) % p for j in range(4)] for i in range(4)]
    assert rank_mod(D, 4) == 1
    a[s] = next(tuple(r) for r in D if any(r))
idx = list(itertools.combinations(range(4), 2))
rows = []
for s, M in Ms.items():
    for u, v in idx:
        r = [0] * 6
        for k, (x, y) in enumerate(idx):
            r[k] = (M[u][x] * M[v][y] - M[u][y] * M[v][x] - int((x, y) == (u, v))) % p
        rows.append(r)
ns_ = nullspace_mod(rows, 6)
out["invariant_alternating_forms_dim"] = len(ns_)
f = ns_[0]
W = [[0] * 4 for _ in range(4)]
for k, (x, y) in enumerate(idx):
    W[x][y] = f[k]
    W[y][x] = -f[k] % p
om = lambda u, v: sum(u[i] * W[i][j] * v[j] for i in range(4) for j in range(4)) % p
out["form_nondegenerate"] = rank_mod(W, 4) == 4
allv = list(itertools.product(range(3), repeat=4))
out["sigma_is_a_transvection"] = all(any(all(apply(Ms[s], v) == tuple((v[i] + e * om(v, a[s]) * a[s][i]) % p for i in range(4)) for v in allv) for e in (1, 2)) for s in Ms)
out["a_vectors_as_colourings"] = {str(s): from4(a[s]) for s in a}
out["path_commutation_matches"] = all((om(a[s], a[t]) != 0) == (w_(pts[path[s - 1]], pts[path[t - 1]]) != 0) for s in a for t in a)
best = None
for sg in itertools.product((1, 2), repeat=4):
    src = [[sg[i] * x % p for x in a[i + 1]] for i in range(4)]
    tgt = [pts[path[i]] for i in range(4)]
    if rank_mod(src, 4) != 4:
        continue
    Si = Matrix(src).inv_mod(3)
    Ph = (Si * Matrix(tgt)).applyfunc(lambda x: x % 3)
    phi_ = lambda v, Ph=Ph: tuple(sum(v[i] * int(Ph[i, j]) for i in range(4)) % p for j in range(4))
    pairs_ = [(u, v) for u in basis for v in basis]
    if any((w_(phi_(u), phi_(v)) != 0) != (om(u, v) != 0) for u, v in pairs_):
        continue
    scales = {w_(phi_(u), phi_(v)) * pow(om(u, v), -1, 3) % 3 for u, v in pairs_ if om(u, v)}
    if len(scales) != 1:
        continue
    best = (sg, phi_, Ph)
    break
out["linear_similitude_exists"] = best is not None
assert best is not None
phi = best[1]
pid = {tuple(q_): i for i, q_ in enumerate(pts)}


def norm3(v):
    f_ = next(x for x in v if x)
    s_ = pow(f_, -1, 3)
    return tuple(x * s_ % 3 for x in v)


pt_of = lambda v: pid[norm3(phi(v))]
nz = [v for v in allv if any(v)]
Gs = {s: rep([s]) for s in Ms}
Gi = {s: rep([-s]) for s in Ms}
out["intertwines_each_generator_same_sign"] = {str(s): all(pt_of(apply(Ms[s], v)) == Gs[s][pt_of(v)] for v in nz) for s in Ms}
out["intertwines_each_generator_inverse_sign"] = {str(s): all(pt_of(apply(Ms[s], v)) == Gi[s][pt_of(v)] for v in nz) for s in Ms}
caps = {to4(c) for c in ALL if c[0] == c[1] and c[2] == c[3] and c[4] == c[5]}
capP = {pt_of(v) for v in caps if any(v)}
out["caps_map_to_L0"] = capP == set(L0pts)
out["cap_colourings_mod_const"] = len(caps)


def colourings(word, n, closure="plat"):
    """the Fox colouring space of the closed diagram: variables are arcs, one equation per crossing"""
    cur = list(range(n))
    nv = n
    top = cur[:]
    eqs = []
    for s in word:
        i = abs(s) - 1
        x, y = cur[i], cur[i + 1]
        z = nv
        nv += 1
        if s > 0:
            eqs.append(((x, -1), (z, -1), (y, 2)))           # y passes over: x + z = 2 y
            cur[i], cur[i + 1] = y, z
        else:
            eqs.append(((y, -1), (z, -1), (x, 2)))           # x passes over
            cur[i], cur[i + 1] = z, x
    rows = []
    for e in eqs:
        r = [0] * nv
        for k, c in e:
            r[k] = (r[k] + c) % p
        rows.append(r)
    if closure == "plat":
        pairs = [(top[a_], top[a_ + 1]) for a_ in range(0, n, 2)] + [(cur[a_], cur[a_ + 1]) for a_ in range(0, n, 2)]
    else:
        pairs = [(top[k], cur[k]) for k in range(n)]
    for u, v in pairs:
        r = [0] * nv
        r[u] = (r[u] + 1) % p
        r[v] = (r[v] - 1) % p
        rows.append(r)
    nul = nv - rank_mod(rows, nv)
    assert nul >= 1, 'constants are always colourings'
    return nul


rng = random.Random(21)
res = collections.Counter()
bad = []
for _ in range(150):
    wd = rand_word(6, rng.randint(2, 11))
    nul = colourings(wd, 6)
    gg = rep(wd)
    d = {4: 2, 1: 1, 0: 0}[len(L0pts & frozenset(gg[q_] for q_ in L0pts))]
    b = dim_from_abs(bracket(wd, 6, "plat"))
    res[(nul == d + 1, b == d)] += 1
    if nul != d + 1 or b != d:
        bad.append((wd, nul, d, b))
out["plat_fox_nullity_eq_1_plus_d__and_jones_eq_d"] = {str(k): v for k, v in res.items()}
out["bad"] = bad[:3]
gen = {}
for n_ in (2, 4, 8):
    ok = t_ = 0
    dims = collections.Counter()
    for _ in range(60):
        wd = rand_word(n_, rng.randint(1, 11))
        nul = colourings(wd, n_)
        b = dim_from_abs(bracket(wd, n_, "plat"))
        t_ += 1
        ok += nul == b + 1
        dims[b] += 1
    gen[n_] = dict(tests=t_, agree=ok, dims=dict(dims))
out["general_strands_fox_vs_jones"] = gen
print(json.dumps(out, default=str))
json.dump(out, open("fox_w33.json", "w"), indent=1, default=str)
