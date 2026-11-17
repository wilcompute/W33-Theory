"""Pass 12683 addendum: doublet-triplet splitting as a measurement context.  Builds on w33_pass12683_su5_vacuum_skew_frames.py (VEV pair
= skew frame pair (F1, F2); the 5 common transversal frames <-> the 5 tensor factorisations of F1, of F2; 3 carry the colour triplet D,
2 the weak doublet H_u).  Scans the 40 isotropic lines of W(3,3) (two-qutrit measurement contexts: 4 commuting Pauli classes / a joint
eigenbasis of 9 states), points and factorisations for those whose stabiliser inside the unitary pair-stabiliser (A5) splits the 5
transversals 2 + 3; then checks, for every such context and every factorisation of the VEV frame, whether the context is a product
basis (Tr rho_A^2 = 1 for all 9 eigenvectors) or maximally entangled (Tr rho_A^2 = 1/3).
usage: py -3 analysis/w33_pass12683_doublet_triplet_contexts.py"""
import collections, itertools, os
_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w33_pass12683_su5_vacuum_skew_frames.py")
src = open(_BASE, encoding="utf-8").read()
src = src.split("fperms = {perm_frames")[0]
G = {"__name__": "x", "__file__": _BASE}
exec(src, G)
seen, frames, facts, T, f2, act_pt, pts, iso = (G[k] for k in ("seen", "frames", "facts", "T", "f2", "act_pt", "pts", "iso"))
perm_frames = G["perm_frames"]
stabM = [M for M in seen.values() if (lambda p: p[0] == 0 and p[f2] == f2)(perm_frames(M))]
print("stabiliser matrices:", len(stabM))
data = []
for M in stabM:
    pm = [act_pt(M, i) for i in range(40)]; pf = perm_frames(M); data.append((pm, pf))
def orbit_split(fix_test):
    sub = [pf for pm, pf in data if fix_test(pm)]
    # orbits on transversals
    orb = []; left = set(T)
    while left:
        t = left.pop(); o = {pf[t] for pf in sub}; left -= o; orb.append(len(o))
    return len(sub), tuple(sorted(orb))
res = collections.Counter()
for i in range(40): res[("point",) + orbit_split(lambda pm, i=i: pm[i] == i)] += 1
for L in iso: res[("isotropic line",) + orbit_split(lambda pm, L=L: frozenset(pm[a] for a in L) == L)] += 1
for f in facts:
    oc = frozenset().union(*f)
    res[("factorisation",) + orbit_split(lambda pm, f=f: frozenset(frozenset(pm[a] for a in L) for L in f) == f)] += 1
for k, v in sorted(res.items()): print(k, "x", v)
octet = G["octet"]
special = []
for L in iso:
    sub = [pf for pm, pf in data if frozenset(pm[a] for a in L) == L]
    orb = []; left = set(T)
    while left:
        t = left.pop(); o = {pf[t] for pf in sub}; left -= o; orb.append(frozenset(o))
    if sorted(len(o) for o in orb) == [2, 3]:
        two = next(o for o in orb if len(o) == 2); special.append((L, two))
print("special lines:", len(special), "| distinct weak pairs:", len({two for _, two in special}))
F1f = [facts[i] for i in frames[0]]; F2f = [facts[i] for i in frames[f2]]
shared = {t: (next(iter(frames[t] & frames[0])), next(iter(frames[t] & frames[f2]))) for t in T}
for L, two in special[:3]:
    m1 = {t: len(L & octet[facts[shared[t][0]]]) for t in T}; m2 = {t: len(L & octet[facts[shared[t][1]]]) for t in T}
    print(" line meets F1-factorisation octets (by transversal):", m1, "| F2:", m2, "| weak pair:", sorted(two))
pattern = collections.Counter()
for L, two in special:
    m1 = tuple(sorted((len(L & octet[facts[shared[t][0]]]), t in two) for t in T)); pattern[m1] += 1
print("patterns (octet hits, is-weak):", dict(pattern))
# do the weak factorisations' octets each contain 2 points of the line, i.e. the line lies in the union of the two weak octets?
print("line inside union of the two weak F1-octets:", all(L <= (octet[facts[shared[a][0]]] | octet[facts[shared[b][0]]]) for L, two in special for a, b in [sorted(two)]))
print("line inside union of the two weak F2-octets:", all(L <= (octet[facts[shared[a][1]]] | octet[facts[shared[b][1]]]) for L, two in special for a, b in [sorted(two)]))
import numpy as np
L_of = lambda f: list(f)    # the two non-isotropic lines L, L^perp of a factorisation
ok_product = True; ok_bell = True
w = np.exp(2j * np.pi / 3); X = np.roll(np.eye(3), 1, axis=0); Z = np.diag([1, w, w * w])
def P(p):   # two-qutrit Weyl operator for point p = (x1, x2, z1, z2)
    x1, x2, z1, z2 = p
    return np.kron(np.linalg.matrix_power(X, x1) @ np.linalg.matrix_power(Z, z1), np.linalg.matrix_power(X, x2) @ np.linalg.matrix_power(Z, z2))
def joint_basis(Lpts):
    A = P(pts[Lpts[0]]) + (0.37 + 0.11j) * P(pts[Lpts[1]])
    return np.linalg.eig(A)[1]
def entanglement_in(f, vec):
    # Schmidt spectrum of vec in the tensor split defined by factorisation f: build local operator algebras from L and L^perp
    La, Lb = list(f)
    pa = [P(pts[i]) for i in list(La)[:2]]; pb = [P(pts[i]) for i in list(Lb)[:2]]
    # purity of reduced state on side A: average over the 9 Weyl ops of side A of |<P>|^2 equals 3 Tr rho_A^2
    opsA = [np.linalg.matrix_power(pa[0], i) @ np.linalg.matrix_power(pa[1], j) for i in range(3) for j in range(3)]
    return sum(abs(np.vdot(vec, Op @ vec)) ** 2 for Op in opsA) / 3     # Tr rho_A^2
for Lc, two in special:
    Lpts = sorted(Lc); V = joint_basis(Lpts)
    for t in T:
        f = facts[shared[t][0]]; Lf, Lfp = list(f)
        hits = (len(Lc & Lf), len(Lc & Lfp))
        pur = [round(entanglement_in(f, V[:, k] / np.linalg.norm(V[:, k])), 6) for k in range(9)]
        if t in two: ok_product &= hits == (1, 1) and all(abs(p - 1) < 1e-6 for p in pur)
        else: ok_bell &= hits == (0, 0) and all(abs(p - 1 / 3) < 1e-6 for p in pur)
print("weak factorisations: context = one local Pauli per qutrit and eigenbasis is a PRODUCT basis (purity 1):", ok_product)
print("colour factorisations: context has no local Pauli and eigenbasis is MAXIMALLY ENTANGLED (purity 1/3):", ok_bell)
Lc, two = special[0]; Lpts = sorted(Lc); V = joint_basis(Lpts)
print("context points:", [pts[i] for i in Lpts], "commute:", all(om(pts[a], pts[b]) == 0 for a in Lpts for b in Lpts) if (om := G["om"]) else None)
print("ops commute numerically:", all(np.allclose(P(pts[a]) @ P(pts[b]), P(pts[b]) @ P(pts[a])) for a in Lpts for b in Lpts))
for t in T:
    f = facts[shared[t][0]]; Lf, Lfp = list(f)
    print(t, "weak" if t in two else "colour", "hits", (len(Lc & Lf), len(Lc & Lfp)), "purities", sorted({round(entanglement_in(f, V[:, k] / np.linalg.norm(V[:, k])), 4) for k in range(9)}))
import json, os
json.dump(dict(scan={" ".join(map(str, k)): v for k, v in sorted(res.items())}, special_contexts=len(special), distinct_weak_pairs=len({two for _, two in special}),
               weak_factorisations_product_basis=bool(ok_product), colour_factorisations_maximally_entangled=bool(ok_bell),
               octet_hit_pattern={str(k): v for k, v in pattern.items()}),
          open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "w33_pass12683_doublet_triplet_contexts.json"), "w"), indent=1)
