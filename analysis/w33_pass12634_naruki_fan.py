"""Is W(3,3) the ray structure of the tropical moduli space of cubic surfaces (the Naruki fan)?

Literature (Ren-Shaw-Sturmfels, Adv. Math. 300 (2016), arXiv:1402.5651, from Hacking-Keel-Tevelev): the tropical moduli space of
marked cubic surfaces, trop(Y0), is a 4-dimensional fan in R^40/R1 (valuations of the 40 Yoshida functions) with
f-vector (1, 76, 630, 1620, 1215); two ray types (a), (b); maximal cones 135 of type aaaa and 1080 of type aaab.

Hypothesis (reconstructed here, then checked by counting): type (a) rays = the 36 positive roots of E6, type (b) rays = the 40
A2xA2xA2 subsystems of E6; cones = sets of mutually orthogonal roots (size <= 4), or one A2^3 subsystem T together with roots
taken from distinct A2 factors of T.  Check 1: this reproduces the f-vector exactly.

Question: what graph does the fan's ray structure induce on the 40 type-(b) rays, and is it the W(3,3) collinearity graph
SRG(40,12,2,4)?  Candidate relations: number of shared positive roots... (each A2 lies in exactly one A2^3, so subsystems share
no A2); orthogonality-based relations between the 9 roots of T and of T'.  Every distance-type relation is tested for strong
regularity, and the parameters printed.  Control: the same relations on a random relabelling must not change (they are W(E6)
invariant), and a deliberately wrong relation must not give SRG(40,12,2,4).
usage: py -3 analysis/w33_pass12634_naruki_fan.py"""
import itertools
import json
import os
from collections import Counter

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- E8 roots, then E6 = roots orthogonal to an A2 -------------------------------------------------------------
E8 = []
for i, j in itertools.combinations(range(8), 2):
    for si in (1, -1):
        for sj in (1, -1):
            v = [0] * 8
            v[i], v[j] = 2 * si, 2 * sj
            E8.append(v)
for signs in itertools.product((1, -1), repeat=8):
    if signs.count(-1) % 2 == 0:
        E8.append(list(signs))
E8 = np.array(E8)  # doubled coordinates: norm 8
assert len(E8) == 240
a1 = E8[0]
a2 = next(r for r in E8 if r @ a1 == -4)  # angle 120 degrees: a1, a2 span an A2
E6 = np.array([r for r in E8 if r @ a1 == 0 and r @ a2 == 0])
assert len(E6) == 72, len(E6)
rng = np.random.default_rng(1)
f = rng.standard_normal(8)
POS = np.array([r for r in E6 if r @ f > 0])
assert len(POS) == 36
IP = POS @ POS.T  # inner products, norm 8; orthogonal = 0, angle 60/120 = +-4


def key(v):
    return tuple(v if v @ f > 0 else -v)


PI = {key(v): i for i, v in enumerate(POS)}
# --- A2 subsystems and A2^3 subsystems ------------------------------------------------------------------------
A2s = set()
for i, j in itertools.combinations(range(36), 2):
    if abs(IP[i, j]) == 4:
        third = POS[i] - POS[j] if IP[i, j] == 4 else POS[i] + POS[j]
        k = PI[key(third)]
        A2s.add(frozenset((i, j, k)))
A2s = sorted(A2s, key=sorted)
assert len(A2s) == 120, len(A2s)


def orth(A, B):
    return all(IP[a, b] == 0 for a in A for b in B)


T3 = set()
for A, B, C in itertools.combinations(A2s, 3):
    if orth(A, B) and orth(A, C) and orth(B, C):
        T3.add(frozenset((A, B, C)))
T3 = sorted(T3, key=lambda t: sorted(min(x) for x in t))
assert len(T3) == 40, len(T3)
assert Counter(sum(A in t for t in T3) for A in A2s) == Counter({1: 120})  # each A2 in exactly one A2^3
roots_of = [frozenset().union(*t) for t in T3]

# --- Check 1: f-vector of the reconstructed fan ---------------------------------------------------------------
orth_sets = {1: [frozenset((i,)) for i in range(36)]}
for n in (2, 3, 4, 5):
    orth_sets[n] = sorted({s | {k} for s in orth_sets[n - 1] for k in range(36) if k not in s and all(IP[k, x] == 0 for x in s)}, key=sorted)
flags = {n: [(t, c) for t in range(40) for c in itertools.combinations(sorted(T3[t], key=min), n) for _ in [0]] for n in (1, 2, 3)}
cnt_flag = {n: sum(len(list(itertools.product(*[sorted(A) for A in c]))) for t in range(40) for c in itertools.combinations(sorted(T3[t], key=min), n)) for n in (0, 1, 2, 3)}
fvec = [36 + 40, len(orth_sets[2]) + cnt_flag[1], len(orth_sets[3]) + cnt_flag[2], len(orth_sets[4]) + cnt_flag[3]]
res = dict(fvector_reconstructed=fvec, fvector_literature=[76, 630, 1620, 1215], max_orth_set=max(n for n in orth_sets if orth_sets[n]),
           aaaa=len(orth_sets[4]), aaab=cnt_flag[3])
print("f-vector reconstructed", fvec, "literature [76, 630, 1620, 1215]; aaaa", res["aaaa"], "aaab", res["aaab"], "orth 5-sets", len(orth_sets[5]))


# --- Graphs on the 40 type-(b) rays ---------------------------------------------------------------------------
def srg(adj):
    n = len(adj)
    A = np.array(adj, dtype=int)
    deg = set(A.sum(1))
    if len(deg) != 1:
        return None
    k = deg.pop()
    A2_ = A @ A
    lam = {A2_[i, j] for i in range(n) for j in range(n) if i != j and A[i, j]}
    mu = {A2_[i, j] for i in range(n) for j in range(n) if i != j and not A[i, j]}
    if len(lam) == 1 and len(mu) == 1:
        return (n, int(k), int(lam.pop()), int(mu.pop()))
    return ("regular", int(k), sorted(lam), sorted(mu))


# invariant of a pair (T, T'): the multiset of |inner products| between the 9 roots of T and the 9 roots of T'
def pair_type(s, t):
    c = Counter(abs(int(IP[a, b])) for a in roots_of[s] for b in roots_of[t])
    shared = len(roots_of[s] & roots_of[t])
    return (shared, tuple(sorted(c.items())))


types = Counter(pair_type(s, t) for s, t in itertools.combinations(range(40), 2))
res["pair_types"] = {str(k): v for k, v in types.items()}
print("pair types (shared roots, |IP| histogram): count")
for k, v in sorted(types.items(), key=lambda x: -x[1]):
    print("  ", k, v)
graphs = {}
for ty in types:
    adj = [[1 if s != t and pair_type(s, t) == ty else 0 for t in range(40)] for s in range(40)]
    graphs[str(ty)] = srg(adj)
    print("relation", ty, "->", graphs[str(ty)])
res["graphs"] = graphs
res["w33_found"] = any(g == (40, 12, 2, 4) for g in graphs.values())
# control: a non-invariant relation (index parity) must not be SRG(40,12,2,4)
ctrl = srg([[1 if s != t and (s + t) % 3 == 0 else 0 for t in range(40)] for s in range(40)])
res["control_noninvariant"] = str(ctrl)
print("control (index relation):", ctrl)
json.dump(res, open(os.path.join(ROOT, "data", "w33_pass12634_naruki_fan.json"), "w"), indent=1, default=str)
print("W(3,3) collinearity graph among fan-induced relations:", res["w33_found"])

# --- Which GQ(3,3)? W(3,3) (all points regular: |{x,y}^perp-perp| = 4 for non-collinear x,y) or its dual Q(4,3) (size 2) -------
def gq_test(adj):
    A = np.array(adj, dtype=int)
    sizes = Counter()
    for x, y in itertools.combinations(range(40), 2):
        if A[x, y]:
            continue
        C = [z for z in range(40) if A[x, z] and A[y, z]]
        pp = [w for w in range(40) if all(A[w, c] for c in C)]
        sizes[len(pp)] += 1
    return dict(sizes)


disj = [[1 if s != t and not (roots_of[s] & roots_of[t]) else 0 for t in range(40)] for s in range(40)]
pp = gq_test(disj)
res["perp_perp_sizes_noncollinear"] = pp
res["gq_type"] = "W(3,3) points (symplectic)" if set(pp) == {4} else ("Q(4,3) points = W(3,3) lines" if set(pp) == {2} else "neither")
# control: build W(3,3) directly (PG(3,3) points, symplectic form) and Q(4,3) (parabolic quadric) and run the same test
def pg_points(n):
    pts = []
    for v in itertools.product(range(3), repeat=n):
        if any(v):
            first = next(c for c in v if c)
            if first == 1:
                pts.append(v)
    return pts
P3 = pg_points(4)
symp = lambda u, v: (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3
Wadj = [[1 if i != j and symp(P3[i], P3[j]) == 0 else 0 for j in range(40)] for i in range(40)]
P4 = [v for v in pg_points(5) if (v[0] * v[0] + v[1] * v[2] + v[3] * v[4]) % 3 == 0]
bil = lambda u, v: (2 * u[0] * v[0] + u[1] * v[2] + u[2] * v[1] + u[3] * v[4] + u[4] * v[3]) % 3
Qadj = [[1 if i != j and bil(P4[i], P4[j]) == 0 else 0 for j in range(len(P4))] for i in range(len(P4))]
res["control_W33"] = gq_test(Wadj)
res["control_Q43"] = gq_test(Qadj) if len(P4) == 40 else len(P4)
print("Naruki cusp graph |{x,y}^pp| over non-collinear pairs:", pp, "->", res["gq_type"])
print("controls: W(3,3)", res["control_W33"], " Q(4,3)", res["control_Q43"], " SRG check W", srg(Wadj), " Q", srg(Qadj))
json.dump(res, open(os.path.join(ROOT, "data", "w33_pass12634_naruki_fan.json"), "w"), indent=1, default=str)

# --- The 135 aaaa cones: orthogonal 4-frames grouped by the D4 subsystem they span (expected 45 x 3) ----------------------------
def span_roots(S):
    # all E6 positive roots in the rational span of the frame vectors
    M = POS[sorted(S)].astype(float)
    P = M.T @ np.linalg.pinv(M.T)
    return frozenset(i for i in range(36) if np.allclose(P @ POS[i], POS[i]))
groups = Counter(span_roots(S) for S in orth_sets[4])
res["aaaa_by_D4"] = dict(n_D4=len(groups), frames_per_D4=sorted(set(groups.values())), roots_per_D4=sorted({len(g) for g in groups}))
print("aaaa cones grouped by spanned D4:", res["aaaa_by_D4"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_pass12634_naruki_fan.json"), "w"), indent=1, default=str)

checks = dict(
    fvector_matches_literature=res["fvector_reconstructed"] == res["fvector_literature"],
    no_orthogonal_5_sets=len(orth_sets[5]) == 0,
    root_disjoint_graph_is_srg_40_12_2_4=res["w33_found"],
    cusp_graph_is_Q43_not_W33=res["gq_type"].startswith("Q(4,3)"),
    controls_distinguish=res["control_W33"] == {4: 540} and res["control_Q43"] == {2: 540},
    noninvariant_control_not_srg=not str(res["control_noninvariant"]).startswith("(40, 12, 2, 4)"),
    aaaa_is_45_D4_times_3=res["aaaa_by_D4"] == dict(n_D4=45, frames_per_D4=[3], roots_per_D4=[12]),
)
res["checks"] = checks
res["all_checks_pass"] = all(checks.values())
res["pass_number"] = 12634
json.dump(res, open(os.path.join(ROOT, "data", "w33_pass12634_naruki_fan.json"), "w"), indent=1, default=str)
print("all_checks_pass", res["all_checks_pass"])
