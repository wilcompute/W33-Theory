"""Pass 12654: the 40 trinification frames of E6 and the generalized quadrangle W(3,3).
A trinification frame = an A2+A2+A2 root subsystem of E6 (the root system of SU(3)^3 in E6 containing a fixed Cartan; 27 =
(3,3b,1)+(1,3,3b)+(3b,1,3); the cubic becomes det A + det B + det C - tr ABC on such a frame -- the frame used by the parallel
assistant's clock T(A,B,C) = (RA, B, CR^-1)).  Count: |W(E6)| / |W(A2)^3 : S3| = 51840 / 1296 = 40, the number of points (and of
lines) of W(3,3).  Which?  The frame stabiliser contains the ABELIAN normal 3^3 of W(A2)^3, while the W(3,3) point stabiliser
contains the NON-abelian Heisenberg 3^(1+2) (Pass 12059), so the prediction is: frames <-> LINES of W(3,3) (points of the dual Q(4,3)).
Test: enumerate the 40 frames from explicit E6 roots; for every candidate relation 'frames F, F' share exactly m orthogonal-pair /
intersection pattern' build the graph; find relations giving an SRG(40,12,2,4) and test isomorphism (VF2) against BOTH the W(3,3)
point-collinearity graph and its line graph (lines meeting).  Control: the two W(3,3) graphs must be non-isomorphic (W(q) is not
self-dual for odd q).  usage: py -3 analysis/w33_trinification_frames.py"""
import itertools, json, os
import numpy as np, networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
# E6 roots inside E8 (standard coordinates): E8 roots orthogonal to the A2 spanned by alpha=(0,..,0,1,-1,0)? use the usual model:
# E8 roots: +-e_i +- e_j (i<j) and (1/2)(+-1,...,+-1) with even number of minus signs.  E6 = roots orthogonal to v1=(0,0,0,0,0,1,1,0)... choose
# E6 = {r in E8 : r.u = r.w = 0} with u = (0,0,0,0,0,0,1,1), w = (0,0,0,0,0,1,-1,0)?  -- verify count 72 below.
E8 = []
for i, j in itertools.combinations(range(8), 2):
    for si, sj in itertools.product((1, -1), repeat=2):
        v = np.zeros(8); v[i] = si; v[j] = sj; E8.append(v)
for signs in itertools.product((1, -1), repeat=8):
    if signs.count(-1) % 2 == 0: E8.append(np.array(signs) / 2)
E8 = np.array(E8); assert len(E8) == 240
# the E6 sublattice orthogonal to an A2 (E8 -> E6 x A2): pick an A2 with simple roots a, b
a = np.array([0, 0, 0, 0, 0, 1, -1, 0.]); b = np.array([0, 0, 0, 0, 0, 0, 1, -1.])
E6 = np.array([r for r in E8 if abs(r @ a) < 1e-9 and abs(r @ b) < 1e-9]); assert len(E6) == 72, len(E6)
key = lambda r: tuple(np.round(2 * r).astype(int))
idx = {key(r): i for i, r in enumerate(E6)}
G = E6 @ E6.T
# A2 subsystems: {r, s, -(r+s)} with r.s = -1, closed with negatives -> 6 roots
a2s = set()
for i, j in itertools.combinations(range(72), 2):
    if abs(G[i, j] + 1) < 1e-9:
        t = -(E6[i] + E6[j]); k = idx[key(t)]
        a2s.add(frozenset({i, j, k, idx[key(-E6[i])], idx[key(-E6[j])], idx[key(-t)]}))
a2s = list(a2s); assert len(a2s) == 120, len(a2s)
orth = lambda A, B: all(abs(G[x, y]) < 1e-9 for x in A for y in B)
frames = set()
for A, B, C in itertools.combinations(a2s, 3):
    if orth(A, B) and orth(A, C) and orth(B, C): frames.add(frozenset([A, B, C]))
frames = list(frames); print("A2^3 frames:", len(frames), flush=True); assert len(frames) == 40
roots_of = [frozenset().union(*F) for F in frames]
# W(3,3) point graph and line graph
pts = sorted({min(tuple((c * x) % 3 for x in v) for c in (1, 2)) for v in itertools.product(range(3), repeat=4) if any(v)})
om = lambda u, v: (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3
Pg = nx.Graph(); Pg.add_nodes_from(range(40))
Pg.add_edges_from((i, j) for i, j in itertools.combinations(range(40), 2) if om(pts[i], pts[j]) == 0)
lines = [frozenset(c) for c in nx.find_cliques(Pg) if len(c) == 4]; assert len(lines) == 40
Lg = nx.Graph(); Lg.add_nodes_from(range(40))
Lg.add_edges_from((i, j) for i, j in itertools.combinations(range(40), 2) if lines[i] & lines[j])
ctrl_noniso = not nx.is_isomorphic(Pg, Lg)
print("control: W(3,3) point graph and line graph non-isomorphic:", ctrl_noniso, flush=True)
# candidate relations between frames: (number of shared roots, number of mutually orthogonal root pairs between frames, ...)
def inv(i, j):
    shared = len(roots_of[i] & roots_of[j])
    # number of A2 components of frame j contained in the centraliser... simple invariant: shared A2 count
    sharedA2 = len(set(frames[i]) & set(frames[j]))
    return (shared, sharedA2)
from collections import Counter
dist = Counter(inv(0, j) for j in range(1, 40))
print("invariants from frame 0:", dict(dist), flush=True)
res = dict(n_frames=40, n_A2=120, control_point_vs_line_noniso=ctrl_noniso, invariant_distribution_from_frame0={str(k): v for k, v in dist.items()}, relations=[])
for val in set(inv(i, j) for i, j in itertools.combinations(range(40), 2)):
    H = nx.Graph(); H.add_nodes_from(range(40)); H.add_edges_from((i, j) for i, j in itertools.combinations(range(40), 2) if inv(i, j) == val)
    degs = set(dict(H.degree()).values())
    rec = dict(relation=str(val), degrees=sorted(degs))
    if degs == {12}:
        ev = np.round(np.linalg.eigvalsh(nx.to_numpy_array(H)), 6); rec["spectrum"] = sorted(Counter(ev.tolist()).items())
        rec["iso_W33_points"] = nx.is_isomorphic(H, Pg); rec["iso_W33_lines"] = nx.is_isomorphic(H, Lg)
    res["relations"].append(rec); print(rec, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_trinification_frames.json"), "w"), indent=1, default=str)
