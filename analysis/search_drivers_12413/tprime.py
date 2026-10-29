"""12413: the binary tetrahedral group SL(2,3) (= derived subgroup of Stab(J) = GU(2,3), 12403) acting on the 40 points and the 40
lines (contexts) of W(3,3): orbits, and decomposition of the permutation representations into SL(2,3) irreducibles (dims 1,1,1,2,2,2,3),
with the character table computed from the group itself (Burnside-Dixon: eigenvectors of class-sum multiplication matrices), checked by
the orthogonality relations.  Question (T' flavour models: three generations as 1+1'+1'' or 2+1 or 3): which irreducibles occur?"""
import itertools, json, collections
import numpy as np
from sympy import Matrix

p = 3
Om = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]], dtype=np.int64)


def tv(v):
    v = np.array(v, dtype=np.int64)
    return (np.eye(4, dtype=np.int64) + np.outer(v, np.array([int(e @ Om @ v) for e in np.eye(4, dtype=np.int64)]))) % p


gens = [tv(v) for v in ([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 1])]
seen = {np.eye(4, dtype=np.int64).tobytes(): np.eye(4, dtype=np.int64)}
fr = [np.eye(4, dtype=np.int64)]
while fr:
    nf = []
    for x in fr:
        for g in gens:
            y = (g @ x) % p
            if y.tobytes() not in seen:
                seen[y.tobytes()] = y
                nf.append(y)
    fr = nf
Sp = list(seen.values())
g0 = np.load('../search_drivers_12369/kahler_metrics.npy')[0]
J = np.array(Matrix(g0.tolist()).inv_mod(p), dtype=np.int64) @ Om % p
SJ = [h for h in Sp if ((h @ J - J @ h) % p == 0).all()]
inv = lambda a: np.array(Matrix(a.tolist()).inv_mod(p), dtype=np.int64)
D = {}
for a in SJ:
    for b in SJ:
        c = (a @ b @ inv(a) @ inv(b)) % p
        D[c.tobytes()] = c
fr = list(D.values())
while fr:
    nf = []
    for x in fr:
        for y in list(D.values()):
            z = (x @ y) % p
            if z.tobytes() not in D:
                D[z.tobytes()] = z
                nf.append(z)
    fr = nf
H = list(D.values())
assert len(H) == 24
key = lambda m: m.tobytes()
idx = {key(h): i for i, h in enumerate(H)}
mul = np.array([[idx[key((a @ b) % p)] for b in H] for a in H])
invi = [idx[key(inv(h))] for h in H]
# conjugacy classes
cls, seenc = [], set()
for i in range(24):
    if i in seenc: continue
    c = sorted({mul[mul[g, i], invi[g]] for g in range(24)})
    seenc |= set(c); cls.append(c)
cid = {}
for k, c in enumerate(cls):
    for i in c: cid[i] = k
r = len(cls)
# class multiplication coefficients: C_j C_k = sum_l c_jkl C_l
coef = np.zeros((r, r, r))
for j in range(r):
    for k in range(r):
        cnt = collections.Counter(cid[mul[a, b]] for a in cls[j] for b in cls[k])
        for l, n in cnt.items():
            coef[j, k, l] = n / len(cls[l])
# character table of SL(2,3) by element order (real parts suffice for real permutation characters: 1'/1'' and 2'/2'' are conjugate
# pairs with equal multiplicity).  order: 1, 2 (central -1), 4, 6, 3.  Re chi:
REAL = {'1': {1: 1, 2: 1, 4: 1, 6: 1, 3: 1}, "1'+1''": {1: 2, 2: 2, 4: 2, 6: -1, 3: -1},
        '2': {1: 2, 2: -2, 4: 0, 6: 1, 3: -1}, "2'+2''": {1: 4, 2: -4, 4: 0, 6: -1, 3: 1}, '3': {1: 3, 2: 3, 4: -1, 6: 0, 3: 0}}
DIMSUM = {'1': 1, "1'+1''": 2, '2': 2, "2'+2''": 4, '3': 3}
def eorder(i):
    k, x = 1, i
    while x != idx[key(np.eye(4, dtype=np.int64))]:
        x = mul[x, i]; k += 1
    return k
orders = [eorder(i) for i in range(24)]
assert sorted(collections.Counter(orders).items()) == [(1, 1), (2, 1), (3, 8), (4, 6), (6, 8)]
# check: the regular representation decomposes as sum dim * chi (sanity of the table)
reg = [24 if o == 1 else 0 for o in orders]
regm = {n: sum(reg[i] * t[orders[i]] for i in range(24)) / 24 for n, t in REAL.items()}
assert regm == {'1': 1, "1'+1''": 2, '2': 2, "2'+2''": 4, '3': 3}, regm
pts = [np.array(v, dtype=np.int64) for v in itertools.product(range(3), repeat=4) if any(v) and next(x for x in v if x) == 1]
def norm(v):
    v = v % 3
    f = next(x for x in v if x)
    return tuple((v * (1 if f == 1 else 2)) % 3)
pid = {tuple(v): i for i, v in enumerate(pts)}
om = lambda u, v: int(u @ Om @ v) % 3
lines = set()
for i in range(40):
    for j in range(i + 1, 40):
        if om(pts[i], pts[j]) == 0:
            lines.add(frozenset(pid[norm(a * pts[i] + b * pts[j])] for a in range(3) for b in range(3) if (a, b) != (0, 0)))
lines = sorted(lines, key=sorted)
lid = {l: i for i, l in enumerate(lines)}
def perm_pts(h): return [pid[norm(h @ v)] for v in pts]
def perm_lines(h):
    pp = perm_pts(h)
    return [lid[frozenset(pp[x] for x in l)] for l in lines]
DIM1 = {'1': 1, "1'+1''": 1, '2': 2, "2'+2''": 2, '3': 3}
out = dict(order=len(H), element_orders={str(k): v for k, v in collections.Counter(orders).items()}, regular_check=regm)
for name, act in (('points', perm_pts), ('lines', perm_lines)):
    fix = [sum(1 for i, j in enumerate(act(h)) if i == j) for h in H]
    mult = {n: sum(fix[i] * t[orders[i]] for i in range(24)) / 24 for n, t in REAL.items()}
    orb, seeno = [], set()
    for i in range(40):
        if i in seeno: continue
        o = {act(h)[i] for h in H}
        seeno |= o; orb.append(len(o))
    out[name] = dict(orbits=sorted(orb), multiplicities=mult, dimension_check=sum(mult[n] * DIM1[n] for n in mult))
print(json.dumps(out, indent=1))
json.dump(out, open('tprime.json', 'w'), indent=1)
# spinorial check: the 80 nonzero vectors (-1 acts freely), where the 2-dimensional (T'-only) irreducibles can appear
vecs = [np.array(v, dtype=np.int64) for v in itertools.product(range(3), repeat=4) if any(v)]
vid = {tuple(v): i for i, v in enumerate(vecs)}
def perm_vecs(h): return [vid[tuple((h @ v) % 3)] for v in vecs]
fix = [sum(1 for i, j in enumerate(perm_vecs(h)) if i == j) for h in H]
mult = {n: sum(fix[i] * t[orders[i]] for i in range(24)) / 24 for n, t in REAL.items()}
orb, seeno = [], set()
for i in range(80):
    if i in seeno: continue
    o = {perm_vecs(h)[i] for h in H}; seeno |= o; orb.append(len(o))
out['vectors'] = dict(orbits=sorted(orb), multiplicities=mult, dimension_check=sum(mult[n] * DIM1[n] for n in mult))
print(json.dumps(out['vectors'])); json.dump(out, open('tprime.json', 'w'), indent=1)
