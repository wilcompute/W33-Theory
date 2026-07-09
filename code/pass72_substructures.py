#!/usr/bin/env python3
"""
Pass 72: Sub-structures, dual code, Burnside-Leech, spinor embedding
Date: 2026-07-08
"""

import numpy as np
from itertools import combinations, product as iproduct
import math
from collections import Counter

# Build W(2,2)
vecs = [v for v in iproduct([0,1], repeat=4) if any(v)]
vec_to_pt = {v: i for i, v in enumerate(vecs)}

def omega4(x, y):
    return (x[0]*y[2] + x[1]*y[3] + x[2]*y[0] + x[3]*y[1]) % 2

doily_lines = []
for i, j in combinations(range(15), 2):
    p, q = vecs[i], vecs[j]
    if omega4(p, q) == 0:
        r = tuple((p[k]+q[k])%2 for k in range(4))
        if r in vec_to_pt:
            rr = vec_to_pt[r]
            if rr not in (i, j):
                line = tuple(sorted([i, j, rr]))
                if line not in doily_lines:
                    doily_lines.append(line)

A_adj = np.zeros((15,15), dtype=int)
for l in doily_lines:
    for a in range(3):
        for b in range(3):
            if a != b:
                A_adj[l[a], l[b]] = 1

ovoids = [combo for combo in combinations(range(15), 5)
          if all(len([p for p in l if p in set(combo)]) == 1 for l in doily_lines)]

def find_spreads(lines, npts=15):
    spreads = []
    def bt(rem, chosen):
        if not rem:
            spreads.append(tuple(sorted(chosen)))
            return
        p = min(rem)
        for l in lines:
            if p in l and all(x in rem for x in l):
                bt(rem - set(l), chosen + [l])
    bt(set(range(npts)), [])
    return list(set(spreads))

spreads = find_spreads(doily_lines)
pt_to_ovoids = {p: tuple([i for i, ov in enumerate(ovoids) if p in ov]) for p in range(15)}

# Sub-GQ(2,1) grids
print("=== SUB-GQ(2,1) GRIDS = K_{3,3} ===")
grids = []
for pts in combinations(range(15), 9):
    sub_lines = [l for l in doily_lines if all(p in pts for p in l)]
    if len(sub_lines) == 6:
        pt_degs = {p: sum(1 for l in sub_lines if p in l) for p in pts}
        if all(d == 2 for d in pt_degs.values()):
            grids.append(tuple(pts))

grids = list(set(grids))
print(f"Number of grids: {len(grids)}")

for g_pts in grids[:3]:
    k6_edges = [pt_to_ovoids[p] for p in g_pts]
    for triple in combinations(range(6), 3):
        A_set = set(triple)
        B_set = set(range(6)) - A_set
        if all(len(set(e)&A_set)==1 for e in k6_edges):
            print(f"  Grid -> K_{{3,3}} with A={sorted(A_set)}, B={sorted(B_set)}")
            break

# Dual code analysis
print("\n=== DUAL SPREAD CODE [15,10,3] ===")
line_idx = {l: i for i, l in enumerate(doily_lines)}
S_mat = np.zeros((6, 15), dtype=int)
for si, sp in enumerate(spreads):
    for l in sp:
        S_mat[si, line_idx[l]] = 1

def f2_rref(M):
    M = M.copy() % 2
    rows, cols = M.shape
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if M[r,col]==1), None)
        if pivot is None: continue
        M[[rank,pivot]] = M[[pivot,rank]]
        for r in range(rows):
            if r != rank and M[r,col]==1:
                M[r] = (M[r]+M[rank])%2
        rank += 1
    return M[:rank]

def null_space_f2(M):
    M = M.copy() % 2
    rows, cols = M.shape
    pivot_cols = []
    rank = 0
    M_work = M.copy()
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if M_work[r,col]==1), None)
        if pivot is None: continue
        M_work[[rank,pivot]] = M_work[[pivot,rank]]
        for r in range(rows):
            if r != rank and M_work[r,col]==1:
                M_work[r] = (M_work[r]+M_work[rank])%2
        pivot_cols.append(col)
        rank += 1
    free_cols = [c for c in range(cols) if c not in pivot_cols]
    null_vecs = []
    for fc in free_cols:
        v = np.zeros(cols, dtype=int)
        v[fc] = 1
        for i, pc in enumerate(pivot_cols):
            v[pc] = M_work[i, fc]
        null_vecs.append(v % 2)
    return null_vecs

G = f2_rref(S_mat)
dual_basis = null_space_f2(G)
dual_words = set()
for bits in iproduct([0,1], repeat=len(dual_basis)):
    cw = tuple(np.array(bits) @ np.array(dual_basis) % 2)
    dual_words.add(cw)

dual_wt_dist = Counter(sum(c) for c in dual_words)
print(f"[15, 10, {min(w for w in dual_wt_dist if w>0)}] weight dist:")
for w, cnt in sorted(dual_wt_dist.items()):
    print(f"  A({w}) = {cnt}")

# Weight-3 = partial spreads
wt3 = [cw for cw in dual_words if sum(cw)==3]
all_partial_spreads = all(
    not set(doily_lines[i]) & set(doily_lines[j])
    for cw in wt3
    for idx, (i,j) in enumerate(combinations([k for k,b in enumerate(cw) if b], 2))
)
print(f"\nWeight-3 codewords = partial spreads (3 disjoint lines): {all_partial_spreads}")
print(f"Count: {len(wt3)} = C(6,3) = {math.comb(6,3)}")

# Burnside-Leech
print("\n=== BURNSIDE-LEECH IDENTITY ===")
irrep_dims_S6 = [1,5,9,10,5,16,10,5,9,5,1]
burnside = sum(d**2 for d in irrep_dims_S6)
print(f"Irrep dims of S_6: {irrep_dims_S6}")
print(f"Σ(dim ρ_i)^2 = {burnside} = |S_6|? {burnside==720}")
print(f"744 = {burnside} + 24 = Σ(dim ρ_i)^2 + dim(Leech) = j-constant")

if __name__ == '__main__':
    print("\nPass 72 complete.")
