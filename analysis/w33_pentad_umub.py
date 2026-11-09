"""Long shot 1: the E6 pezzotope pentads (= BT845 chiral pentads = maximal 5-line partial spreads of W(3,3)) as unextendible sets of
two-qutrit mutually unbiased bases.  Lines of W(3,3) = maximal commuting classes of 8 two-qutrit Paulis; disjoint lines = MUBs
(Bandyopadhyay et al.); a maximal partial spread = a 'weakly unextendible' set of Pauli-class MUBs (Mandayam-Bandyopadhyay-Grassl-
Wootters arXiv:1302.3709; Thas arXiv:1407.2778, who constructs sizes l^2-l+1, l^2-l+2 = 7, 8 for d = 9).
(1) Spectrum of sizes of maximal partial spreads of W(3,3) (exhaustive).  (2) Hilbert space: for one pentad, build the 5 common
eigenbases of the classes, verify |<a|b>|^2 = 1/9 across bases, and that every other Pauli-class basis has some overlap != 1/9 with
some basis of the pentad (no Pauli-class extension).
usage: py -3 analysis/w33_pentad_umub.py"""
import itertools
import json
import os
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sb = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12635_burkhardt_fan.py")}
exec(open(os.path.join(HERE, "w33_pass12635_burkhardt_fan.py"), encoding="utf-8").read().split("res = dict(")[0], sb)
P, iso, w = sb["P"], sb["iso"], sb["w"]
lines = [frozenset(L) for L in iso]
disj = [[not (lines[a] & lines[b]) for b in range(40)] for a in range(40)]

# (1) all maximal partial spreads (cliques of the disjointness graph that cannot be extended)
sizes = Counter()
maxsets = []
def bk(R, Pc, X):
    if not Pc and not X:
        sizes[len(R)] += 1
        if len(R) == 5:
            maxsets.append(frozenset(R))
        return
    for v in list(Pc):
        bk(R | {v}, {u for u in Pc if disj[v][u]}, {u for u in X if disj[v][u]})
        Pc = Pc - {v}
        X = X | {v}
bk(set(), set(range(40)), set())
print("maximal partial spreads of W(3,3) by size:", dict(sorted(sizes.items())))

# (2) Hilbert space check
om = np.exp(2j * np.pi / 3)
X1 = np.roll(np.eye(3), 1, axis=0)
Z1 = np.diag([1, om, om ** 2])
def pauli(v):  # v = (a1, a2, b1, b2): X^a1 Z^b1 (x) X^a2 Z^b2  (symplectic form w pairs coords 0<->2, 1<->3)
    A = np.linalg.matrix_power(X1, v[0]) @ np.linalg.matrix_power(Z1, v[2])
    B = np.linalg.matrix_power(X1, v[1]) @ np.linalg.matrix_power(Z1, v[3])
    return np.kron(A, B)
def basis_of_line(L):
    pts = [P[i] for i in sorted(lines[L])]
    rng = np.random.default_rng(L)
    H = sum(rng.standard_normal() * (pauli(p) + pauli(p).conj().T) + rng.standard_normal() * 1j * (pauli(p) - pauli(p).conj().T) for p in pts)
    vals, vecs = np.linalg.eigh(H)
    return vecs
bases = [basis_of_line(L) for L in range(40)]
def unbiased(a, b):
    O = np.abs(bases[a].conj().T @ bases[b]) ** 2
    return np.allclose(O, 1 / 9, atol=1e-8)
# sanity: unbiasedness <=> disjointness for all line pairs
agree = all(unbiased(a, b) == disj[a][b] for a, b in itertools.combinations(range(40), 2))
pent = sorted(maxsets[0])
pent_mub = all(unbiased(a, b) for a, b in itertools.combinations(pent, 2))
ext = [L for L in range(40) if L not in pent and all(unbiased(L, a) for a in pent)]
res = dict(maximal_partial_spread_sizes=dict(sizes), n_size5=sizes.get(5, 0), unbiased_iff_disjoint_all_pairs=agree,
           pentad_is_5_MUBs=pent_mub, pauli_class_extensions=len(ext), smallest_size=min(sizes))
print("unbiased <=> disjoint for all 780 line pairs:", agree, "| pentad = 5 MUBs:", pent_mub, "| Pauli-class bases unbiased to all 5:", len(ext))
json.dump(res, open(os.path.join(ROOT, "data", "w33_pentad_umub.json"), "w"), indent=1)

# --- (3) the 135 maximal partial spreads of size 8 vs the 135 aaaa cones (orthogonal root 4-frames) of the Naruki fan ---------------
eight = []
def bk8(R, Pc, X):
    if not Pc and not X:
        if len(R) == 8:
            eight.append(frozenset(R))
        return
    for v in list(Pc):
        bk8(R | {v}, {u for u in Pc if disj[v][u]}, {u for u in X if disj[v][u]})
        Pc = Pc - {v}; X = X | {v}
bk8(set(), set(range(40)), set())
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_split_bridge.py")}
exec(open(os.path.join(HERE, "w33_split_bridge.py"), encoding="utf-8").read().split("# (ii) roots -> spreads")[0], ns)
phi, roots_of, IP = ns["phi"], ns["roots_of"], ns["IP"]
inv = {v: k for k, v in phi.items()}
prof = Counter()
frames = Counter()
for S in eight:
    Ts = [inv[l] for l in S]
    cnt = Counter(r for t in Ts for r in roots_of[t])
    prof[tuple(sorted(Counter(cnt.get(r, 0) for r in range(36)).items()))] += 1
    # roots in no T of S: candidate frame
    missing = sorted(r for r in range(36) if cnt.get(r, 0) == 0)
    frames[(len(missing), all(IP[a, b] == 0 for a, b in itertools.combinations(missing, 2)))] += 1
res["size8_root_multiplicity_profile"] = {str(k): v for k, v in prof.items()}
res["size8_missing_roots"] = {str(k): v for k, v in frames.items()}
print("size-8 sets:", len(eight), "| root multiplicity profile:", dict(prof))
print("roots in none of the 8 A2^3 (count, pairwise orthogonal): sets", dict(frames))
json.dump(res, open(os.path.join(ROOT, "data", "w33_pentad_umub.json"), "w"), indent=1)
six_sets = []
for S in eight:
    cnt = Counter(r for l in S for r in roots_of[inv[l]])
    six_sets.append(frozenset(r for r in range(36) if cnt.get(r, 0) == 6))
orth = all(len(F) == 4 and all(IP[a, b] == 0 for a, b in itertools.combinations(sorted(F), 2)) for F in six_sets)
res["size8_multiplicity6_roots_form_orthogonal_frame"] = orth
res["size8_to_frames_bijective"] = orth and len(set(six_sets)) == 135
print("multiplicity-6 roots form an orthogonal 4-frame:", orth, "| distinct frames:", len(set(six_sets)), "(135 = all aaaa cones)")
json.dump(res, open(os.path.join(ROOT, "data", "w33_pentad_umub.json"), "w"), indent=1)
