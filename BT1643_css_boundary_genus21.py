#!/usr/bin/env python3
"""
BT1643 historical claim RETRACTED: CSS boundary is not a genus-21 surface

RETRACTED INTERPRETATION (TOE65, 2026-10-13):
This historical script correctly produces the f-vector (40,240,160,40)
and chi(two-skeleton)=-40, but it does NOT establish a genus-21 surface
or a genus-21 toric code. Actual vertex links have FOUR disconnected
3-cycles, whereas a surface requires one circle. The full tetrahedral
clique complex has homotopy type of the W33 point-line incidence graph
(wedge of 81 circles), and its 2-skeleton has F2 Betti [1,81,40].
See analysis/w33_20261013_toe65_surface_topology_correction.py and the
matching exact audit certificate. Historical matrix/code arithmetic below
is retained but its surface-distance and toric-code interpretation is
withdrawn pending a genuine surface cellulation and code-distance proof.

Perplexity session Aug 18 2026.
"""

import numpy as np
from math import factorial

q = 3; v = 40; k = 12; lam_par = 2; mu_par = 4; E = 240

# Build W(3,3)
def omega(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

F3 = [0, 1, 2]
all_vecs = [(a,b,c,d) for a in F3 for b in F3 for c in F3 for d in F3
            if not (a==0 and b==0 and c==0 and d==0)]

def canonical(v_in):
    v2 = list(v_in)
    for i in range(4):
        if v2[i] != 0:
            inv = v2[i]
            return tuple(int(v2[j] * inv) % 3 for j in range(4))

pts = sorted(set(canonical(vec) for vec in all_vecs))
n = len(pts)
assert n == 40
adj = [[omega(pts[i], pts[j]) == 0 and i != j for j in range(n)] for i in range(n)]

# Edge indexing
edges = []
edge_idx = {}
for i in range(n):
    for j in range(i+1, n):
        if adj[i][j]:
            edge_idx[(i,j)] = len(edges)
            edges.append((i,j))
assert len(edges) == 240

# Find all lines
def line_through(p, q_pt):
    result = set()
    for a in F3:
        for b in F3:
            if a == 0 and b == 0:
                continue
            v2 = tuple((a*p[i] + b*q_pt[i]) % 3 for i in range(4))
            c = canonical(v2)
            if c is not None:
                result.add(c)
    return frozenset(result)

lines_set = set()
for i in range(n):
    for j in range(i+1, n):
        if adj[i][j]:
            ln = line_through(pts[i], pts[j])
            if len(ln) == 4:
                lines_set.add(ln)
all_lines = [sorted([pts.index(p) for p in ln]) for ln in lines_set]
assert len(all_lines) == 40

# CSS parity check matrix H_X
H_X = np.zeros((len(all_lines), len(edges)), dtype=int)
for row, ln in enumerate(all_lines):
    for a in range(len(ln)):
        for b in range(a+1, len(ln)):
            i2, j2 = min(ln[a],ln[b]), max(ln[a],ln[b])
            col = edge_idx[(i2,j2)]
            H_X[row, col] = 1

rank_HX = np.linalg.matrix_rank(H_X)
logical_qutrits = len(edges) - 2 * rank_HX
print(f"H_X: {H_X.shape}, rank={rank_HX}, logical_qutrits={logical_qutrits}")

# Chain complex boundary maps
triangles = []
tri_idx = {}
for ln in all_lines:
    for a in range(len(ln)):
        for b in range(a+1, len(ln)):
            for c in range(b+1, len(ln)):
                t = (ln[a], ln[b], ln[c])
                tri_idx[t] = len(triangles)
                triangles.append(t)
assert len(triangles) == 160

# d2: triangles -> edges
d2 = np.zeros((len(edges), len(triangles)), dtype=int)
for col, (i2, j2, k2) in enumerate(triangles):
    for sign, (a, b) in [(+1,(j2,k2)), (-1,(i2,k2)), (+1,(i2,j2))]:
        aa, bb = min(a,b), max(a,b)
        row = edge_idx[(aa,bb)]
        d2[row, col] = (d2[row, col] + sign) % 3

# d3: lines -> triangles
d3 = np.zeros((len(triangles), len(all_lines)), dtype=int)
for col, ln in enumerate(all_lines):
    for a in range(4):
        for b in range(a+1, 4):
            for c in range(b+1, 4):
                t = (ln[a], ln[b], ln[c])
                row = tri_idx[t]
                missing = [x for x in range(4) if x not in [a,b,c]][0]
                sign = (-1)**missing
                d3[row, col] = (d3[row, col] + sign) % 3

# Verify d2 * d3 = 0
prod = (d2 @ d3) % 3
assert np.all(prod == 0), "d2 * d3 != 0!"
print("d2 composed with d3 = 0 (mod 3) [checked]")

# Euler count only: formal genus 21 would require a genuine surface.
chi_full = v - len(edges) + len(triangles) - len(all_lines)
chi_2skel = v - len(edges) + len(triangles)
assert chi_full == -80
assert chi_2skel == -40
formal_euler_genus_candidate = (2 - chi_2skel) // 2
assert formal_euler_genus_candidate == 21

print("\n=== BT1643 SURFACE INTERPRETATION RETRACTED (TOE65) ===")
print(f"The arithmetic Euler genus candidate is {formal_euler_genus_candidate},")
print("but the 2-skeleton is NOT a surface: each point has a disconnected")
print("vertex link consisting of four separate triangular cycles.")
print("The genus-21 toric-code and surface-distance interpretations are withdrawn.")
print("See analysis/w33_20261013_toe65_surface_topology_correction.py.")
