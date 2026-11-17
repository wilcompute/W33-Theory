"""Pass 12683: the Weyl/incidence shadow of the other track's E6 -> SU(5) -> SM vacuum (6a4a37517, 6442db4d6) on two-qutrit frames.

Part A (their basis).  The 27 coordinates of A, B, C (I3 = det A + det B + det C - Tr(ABC)) are the 27 weights; two weights 'meet'
(intersecting lines of the cubic surface) iff they occur together in a cubic monomial.  Their two SU(5)-breaking VEVs are e7 = A[2,1]
and e8 = A[2,2].  We classify the other 25 weights by incidence with (e7, e8) and read off the integer hypercharge Y of their vacuum.

Part B (two qutrits).  Pauli classes of C^3 x C^3 = 40 points of W(3,3) (PG(3,3) with the symplectic form); a tensor factorisation
= octet L u L^perp for a non-isotropic line L (45); a complete factorisation frame = 5 factorisations whose octets partition the
40 classes (27 frames; dictionary 5419c27 / gq24_lives_inside_w33_as_its_octet_factors.py).  Frames meet iff they share a
factorisation.  An explicit isomorphism of incidence graphs sending (e7, e8) to a skew pair of frames transports Y to frames.

Part C.  Stabiliser of an ordered skew frame pair in PSp(4,3) (unitary Cliffords mod Paulis, acting on frames), and its action on
the five common transversal frames.   usage: py -3 analysis/w33_pass12683_su5_vacuum_skew_frames.py"""
import collections, itertools, json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
# ---------------- Part A
A = lambda i, j: 3 * i + j; B = lambda i, j: 9 + 3 * i + j; C = lambda i, j: 18 + 3 * i + j
mons = []
for M in (A, B, C):
    for p in itertools.permutations(range(3)): mons.append(frozenset(M(i, p[i]) for i in range(3)))
for i, j, k in itertools.product(range(3), repeat=3): mons.append(frozenset((A(i, j), B(j, k), C(k, i))))
assert len(set(mons)) == 45 and all(len(m) == 3 for m in mons)
adjA = {v: set() for v in range(27)}
for m in mons:
    for a, b in itertools.permutations(m, 2): adjA[a].add(b)
assert all(len(adjA[v]) == 10 for v in adjA)
YL, YR, YC = [1, 1, -2], [4, -2, -2], [0, 0, 0]
Y = {}
for i in range(3):
    for j in range(3):
        Y[A(i, j)] = YL[i] - YR[j]; Y[B(i, j)] = YR[i] - YC[j]; Y[C(i, j)] = YC[i] - YL[j]
assert Y[7] == 0 and Y[8] == 0 and 8 not in adjA[7], "VEVs must be a skew pair of zero-hypercharge weights"
def cls(adj, f1, f2, v):
    if v == f1: return "F1"
    if v == f2: return "F2"
    return {(True, True): "meets both (transversal)", (True, False): "meets F1 only", (False, True): "meets F2 only", (False, False): "skew to both"}[(v in adj[f1], v in adj[f2])]
classesA = collections.defaultdict(list)
for v in range(27): classesA[cls(adjA, 7, 8, v)].append(v)
SMNAME = {-6: "e^c (1,1)_1", -3: "H_u (1,2)_1/2", -2: "d^c (3b,1)_1/3", -1: "Q (3,2)_1/6", 0: "N (1,1)_0", 2: "D (3,1)_-1/3", 3: "L (1,2)_-1/2", 4: "u^c (3b,1)_-2/3"}
print("Part A: incidence classes relative to the VEV pair (e7, e8), with hypercharge content (Y_SM = -Y/6):")
reportA = {}
for k in ["F1", "F2", "meets both (transversal)", "meets F1 only", "meets F2 only", "skew to both"]:
    cnt = collections.Counter(SMNAME[Y[v]] for v in classesA[k]); reportA[k] = dict(size=len(classesA[k]), content=dict(cnt))
    print(f"  {k:26s} {len(classesA[k]):2d}  {dict(cnt)}")
# ---------------- Part B: two-qutrit frames
F3 = range(3)
pts = []
for v in itertools.product(F3, repeat=4):
    if any(v):
        f = next(x for x in v if x); inv = 1 if f == 1 else 2
        w = tuple(x * inv % 3 for x in v)
        if w not in pts: pts.append(w)
assert len(pts) == 40
idx = {p: i for i, p in enumerate(pts)}
def norm(v):
    f = next(x for x in v if x); inv = 1 if f == 1 else 2
    return tuple(x * inv % 3 for x in v)
om = lambda u, v: (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % 3
lines = set()
for a, b in itertools.combinations(range(40), 2):
    u, v = pts[a], pts[b]
    L = frozenset(idx[norm(tuple((s * x + t * y) % 3 for x, y in zip(u, v)))] for s in F3 for t in F3 if (s, t) != (0, 0))
    lines.add(L)
assert len(lines) == 130
iso = [L for L in lines if all(om(pts[a], pts[b]) == 0 for a in L for b in L)]
noniso = [L for L in lines if L not in iso]
assert len(iso) == 40 and len(noniso) == 90
perp = lambda L: frozenset(i for i in range(40) if all(om(pts[i], pts[a]) == 0 for a in L))
facts = list({frozenset((L, perp(L))) for L in noniso})
octet = {f: frozenset().union(*f) for f in facts}
assert len(facts) == 45 and all(len(o) == 8 for o in octet.values())
frames = []
for combo in itertools.combinations(range(45), 5):
    pass
# smarter: build frames by backtracking over disjoint octets
def extend(chosen, used):
    if len(chosen) == 5:
        frames.append(frozenset(chosen)); return
    start = max(chosen) + 1 if chosen else 0
    for i in range(start, 45):
        if not (octet[facts[i]] & used): extend(chosen + [i], used | octet[facts[i]])
extend([], frozenset())
assert len(frames) == 27, len(frames)
adjB = {a: {b for b in range(27) if b != a and len(frames[a] & frames[b]) == 1} for a in range(27)}
assert all(len(adjB[a]) == 10 for a in adjB) and all(len(frames[a] & frames[b]) in (0, 1) for a in range(27) for b in range(27) if a != b)
# isomorphism adjA -> adjB with 7 -> 0 and 8 -> first frame skew to frame 0 (backtracking)
f2 = next(b for b in range(27) if b != 0 and b not in adjB[0])
def iso_search(mp):
    if len(mp) == 27: return dict(mp)
    v = next(u for u in range(27) if u not in mp)
    used = set(mp.values())
    for t in range(27):
        if t in used: continue
        if all((u in adjA[v]) == (mp[u] in adjB[t]) for u in mp):
            mp[v] = t; r = iso_search(mp)
            if r: return r
            del mp[v]
    return None
phi = iso_search({7: 0, 8: f2})
assert phi is not None
Yframe = {phi[v]: Y[v] for v in range(27)}
print("Part B: 45 factorisations, 27 complete frames, frames meet iff they share one factorisation (Schlaefli graph, degree 10).")
print("  isomorphism sends the VEV pair to the skew frame pair (0, %d); hypercharge transported to frames." % f2)
# the five transversal frames and how Y splits them
T = sorted(b for b in range(27) if b in adjB[0] and b in adjB[f2])
assert len(T) == 5 and all(b not in adjB[a] for a in T for b in T if a != b), "the 5 transversals must be mutually skew"
print("  transversal frames (share one factorisation with each VEV frame, mutually skew):", T, "| their hypercharge:", [SMNAME[Yframe[t]] for t in T])
# the factorisation each transversal shares with F1 and with F2
shared = {t: (next(iter(frames[t] & frames[0])), next(iter(frames[t] & frames[f2]))) for t in T}
# ---------------- Part C: PSp(4,3) on frames
def mat_mul(X, Yy): return tuple(tuple(sum(X[i][k] * Yy[k][j] for k in range(4)) % 3 for j in range(4)) for i in range(4))
def transvection(u):
    return tuple(tuple(((1 if i == j else 0) + u[i] * om(u, e)) % 3 for j, e in enumerate(np.eye(4, dtype=int).tolist())) for i in range(4))
# x -> x + om(x,u) u  as a matrix acting on row vectors: x M
def tv(u):
    M = [[0] * 4 for _ in range(4)]
    for j in range(4):
        e = [0] * 4; e[j] = 1
        img = [(e[k] + om(e, u) * u[k]) % 3 for k in range(4)]
        M[j] = img
    return tuple(tuple(r) for r in M)
gens = [tv(p) for p in pts]
act_pt = lambda M, i: idx[norm(tuple(sum(pts[i][k] * M[k][j] for k in range(4)) % 3 for j in range(4)))]
def perm_frames(M):
    pm = [act_pt(M, i) for i in range(40)]
    fac_img = {}
    for fi, f in enumerate(facts):
        img = frozenset(frozenset(pm[a] for a in L) for L in f); fac_img[fi] = facts.index(img)
    return tuple(frames.index(frozenset(fac_img[i] for i in fr)) for fr in frames)
seen = {}
frontier = [tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))]
perms = set()
while frontier:
    M = frontier.pop()
    key = tuple(act_pt(M, i) for i in range(40))
    if key in seen: continue
    seen[key] = M
    for g in gens: frontier.append(mat_mul(M, g))
print("Part C: PSp(4,3) on the 40 points has order", len(seen))
fperms = {perm_frames(M) for M in seen.values()}
stab = [p for p in fperms if p[0] == 0 and p[f2] == f2]
on_T = collections.Counter(tuple(p[t] for t in T) for p in stab)
from itertools import permutations
sign = lambda s: (-1) ** sum(1 for i in range(len(s)) for j in range(i + 1, len(s)) if s[i] > s[j])
perm_T = {tuple(T.index(x) for x in im) for im in on_T}
print("  frame action order", len(fperms), "| stabiliser of the ordered skew pair:", len(stab), "| acts on the 5 transversals as a group of order", len(perm_T),
      "all even:", all(sign(s) == 1 for s in perm_T))
res = dict(partA_classes=reportA, transversal_frames=T, transversal_hypercharges=[SMNAME[Yframe[t]] for t in T],
           psp43_order=len(seen), frame_action_order=len(fperms), ordered_skew_pair_stabiliser=len(stab), action_on_transversals=len(perm_T),
           action_on_transversals_even=all(sign(s) == 1 for s in perm_T),
           frame_hypercharge=[SMNAME[Yframe[b]] for b in range(27)])
json.dump(res, open(os.path.join(ROOT, "data", "w33_pass12683_su5_vacuum_skew_frames.json"), "w"), indent=1)
# the 5 transversals <-> the 5 factorisations of F1 (and of F2)
sh1 = [shared[t][0] for t in T]; sh2 = [shared[t][1] for t in T]
bij = sorted(sh1) == sorted(frames[0]) and sorted(sh2) == sorted(frames[f2])
print("Part D: transversal -> shared factorisation is a bijection onto F1's five factorisations and onto F2's:", bij)
colour = [t for t in T if Yframe[t] == 2]; weak = [t for t in T if Yframe[t] == -3]
print("  colour triplet D = transversals", colour, "| weak doublet H_u = transversals", weak)
# ordered-pair stabiliser on unordered 2-subsets of transversals (doublet-triplet choices)
orb2 = {frozenset(T.index(x) for x in (p[weak[0]], p[weak[1]])) for p in stab}
stab2 = [p for p in stab if {p[weak[0]], p[weak[1]]} == set(weak)]
print("  doublet choices in one orbit of", len(orb2), "under the unitary stabiliser; stabiliser of the choice has order", len(stab2))
res.update(transversal_factorisation_bijection=bij, colour_transversals=colour, weak_transversals=weak, doublet_choice_orbit=len(orb2), doublet_choice_stabiliser=len(stab2))
json.dump(res, open(os.path.join(ROOT, "data", "w33_pass12683_su5_vacuum_skew_frames.json"), "w"), indent=1)
