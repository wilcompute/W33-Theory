"""Pass 12680: orbit classification of the uncovered order-4 isotropic Pauli groups of the F_8 regulus under its symmetry group
H = (SL(2,8) x SL(2,8)) x| Frobenius (m -> g m h^T, Frobenius; Paulis act trivially on subgroups).  Every such group {0, a, b, a+b}
(a, b commuting, a, b, a+b uncovered) is enumerated; orbits are found by union-find under generators of H acting on labels (precomputed
label permutations).  For each orbit: size, coset-weight type (A, B, C, ... as in Pass 12674-12678), and whether the global minimisers'
stabilisers (Pass 12674/12679 census) fall into it.   usage: py -3 analysis/w33_f8_order4_orbit_classification.py"""
import collections, contextlib, io, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_torus_global_origin.py")}
src = open(os.path.join(HERE, "w33_f8_torus_global_origin.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("norm=[]")], G)
mm, tp, tomat, tolabel, frob, multiply, covered, comm = (G[k] for k in ("mm", "tp", "tomat", "tolabel", "frob", "multiply", "covered", "comm"))
labels = [(u, v) for u in range(64) for v in range(64) if (u, v) != (0, 0)]
COV = {k for k in labels if covered(k)}
idx = {k: i for i, k in enumerate(labels)}
I2 = ((1, 0), (0, 1))
gensSL = [((1, a), (0, 1)) for a in (1, 2, 4)] + [((0, 1), (1, 0))]
def perm_left(g): return [idx[tolabel(mm(g, tomat(*k)))] for k in labels]
def perm_right(h): return [idx[tolabel(mm(tomat(*k), tp(h)))] for k in labels]
perms = [perm_left(g) for g in gensSL] + [perm_right(h) for h in gensSL] + [[idx[tolabel(frob(tomat(*k)))] for k in labels]]
for P in perms:     # each must preserve the covered set and commutation
    assert all((labels[P[i]] in COV) == (labels[i] in COV) for i in range(len(labels)))
# enumerate subgroups
unc = [i for i, k in enumerate(labels) if k not in COV]
uncset = set(unc)
xor = lambda i, j: idx[(labels[i][0] ^ labels[j][0], labels[i][1] ^ labels[j][1])]
subs = set()
for a in unc:
    for b in unc:
        if b <= a or not comm(labels[a], labels[b]): continue
        c = xor(a, b)
        if c in uncset: subs.add(frozenset((a, b, c)))
subs = list(subs); sid = {s: n for n, s in enumerate(subs)}
print("uncovered order-4 isotropic groups:", len(subs), flush=True)
par = list(range(len(subs)))
def find(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for P in perms:
    for n, s in enumerate(subs):
        t = sid[frozenset(P[i] for i in s)]
        ra, rb = find(n), find(t)
        if ra != rb: par[ra] = rb
orbits = collections.defaultdict(list)
for n in range(len(subs)): orbits[find(n)].append(n)
def wtype(s):
    a, b, c = (labels[i] for i in s); Sg = [(0, 0), a, b, c]
    cos = {}
    for k in labels:
        if all(comm(k, t) for t in Sg[1:]): cos.setdefault(min((k[0] ^ t[0], k[1] ^ t[1]) for t in Sg), []).append(k)
    return tuple(sorted(collections.Counter(sum(x in COV for x in c_) for kk, c_ in cos.items() if kk != (0, 0)).items()))
NAMES = {((0, 156), (1, 63), (2, 36)): "A", ((0, 138), (1, 99), (2, 18)): "B", ((0, 165), (1, 54), (2, 27), (3, 9)): "C"}
cen = json.load(open(os.path.join(ROOT, "data", "w33_f8_global_minimiser_stabilisers.json")))
min_subs = [frozenset(idx[tuple(x)] for x in r["stabiliser"]) for r in cen["records"]]
rows = []
for root, mem in sorted(orbits.items(), key=lambda kv: -len(kv[1])):
    t = wtype(subs[mem[0]]); mems = set(mem)
    hits = sum(1 for s in min_subs if sid.get(s) in mems)
    rows.append(dict(size=len(mem), type=NAMES.get(t, str(t)), minimiser_stabilisers_in_orbit=hits))
for r in rows: print(r, flush=True)
res = dict(n_groups=len(subs), n_orbits=len(rows), orbits=rows,
           types_per_orbit_unique=len({r["type"] for r in rows}) == len(rows))
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_order4_orbit_classification.json"), "w"), indent=1)
