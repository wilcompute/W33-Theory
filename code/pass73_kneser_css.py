#!/usr/bin/env python3
"""
Pass 73: Kneser graph identity, CSS quantum code, McKay-Thompson
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
          if all(len([p for p in l if p in set(combo)])==1 for l in doily_lines)]

def find_spreads(lines, npts=15):
    spreads = []
    def bt(rem, chosen):
        if not rem:
            spreads.append(tuple(sorted(chosen))); return
        p = min(rem)
        for l in lines:
            if p in l and all(x in rem for x in l):
                bt(rem - set(l), chosen + [l])
    bt(set(range(npts)), [])
    return list(set(spreads))

spreads = find_spreads(doily_lines)
pt_to_ovoids = {p: tuple([i for i,ov in enumerate(ovoids) if p in ov]) for p in range(15)}

# KNESER K(6,2)
pair_list = list(combinations(range(6),2))
pair_to_idx = {p:i for i,p in enumerate(pair_list)}
kneser_adj = np.zeros((15,15), dtype=int)
for i, e1 in enumerate(pair_list):
    for j, e2 in enumerate(pair_list):
        if i != j and not set(e1) & set(e2):
            kneser_adj[i,j] = 1

doily_to_kneser = {p: pair_to_idx[tuple(pt_to_ovoids[p])] for p in range(15)}
A_relabeled = np.zeros((15,15), dtype=int)
for p in range(15):
    for q in range(15):
        if A_adj[p,q]==1:
            A_relabeled[doily_to_kneser[p], doily_to_kneser[q]] = 1

print(f"K(6,2) == W(2,2) collinearity: {np.array_equal(A_relabeled, kneser_adj)}")

# Cayley graph check: max order in S_6
from functools import reduce
partitions_6 = [(1,1,1,1,1,1),(2,1,1,1,1),(2,2,1,1),(2,2,2),(3,1,1,1),(3,2,1),(3,3),(4,1,1),(4,2),(5,1),(6,)]
max_ord = max(reduce(math.lcm, p) for p in partitions_6)
print(f"Max order in S_6 = {max_ord}, 15 > {max_ord} -> NOT a Cayley graph")

# CSS code
def f2_rref(M):
    M = M.copy() % 2
    rows, cols = M.shape
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank,rows) if M[r,col]==1), None)
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
    pivot_cols, rank = [], 0
    Mw = M.copy()
    for col in range(cols):
        pivot = next((r for r in range(rank,rows) if Mw[r,col]==1), None)
        if pivot is None: continue
        Mw[[rank,pivot]] = Mw[[pivot,rank]]
        for r in range(rows):
            if r != rank and Mw[r,col]==1:
                Mw[r] = (Mw[r]+Mw[rank])%2
        pivot_cols.append(col); rank += 1
    free_cols = [c for c in range(cols) if c not in pivot_cols]
    null_vecs = []
    for fc in free_cols:
        v = np.zeros(cols, dtype=int)
        v[fc] = 1
        for i,pc in enumerate(pivot_cols):
            v[pc] = Mw[i,fc]
        null_vecs.append(v%2)
    return null_vecs

line_idx = {l:i for i,l in enumerate(doily_lines)}
S_mat = np.zeros((6,15), dtype=int)
for si,sp in enumerate(spreads):
    for l in sp: S_mat[si,line_idx[l]] = 1

G = f2_rref(S_mat)
dual_basis = null_space_f2(G)

# CSS code: Hx=G, Hz=dual_basis
Hx = G  # 5x15
Hz = np.array(dual_basis)  # 10x15
print(f"Hx*Hz^T mod 2 = 0? {np.all(Hx @ Hz.T % 2 == 0)}")
print(f"CSS [[15, {15 - len(Hx) - len(Hz)}, ?]] = [[15, 5, d]]")

# Minimum distance
from itertools import product as iproduct
def min_dist(G):
    n = G.shape[1]
    min_w = n
    for bits in iproduct([0,1], repeat=len(G)):
        cw = np.array(bits) @ G % 2
        w = sum(cw)
        if w > 0 and w < min_w:
            min_w = w
    return min_w

print(f"Hx min distance: {min_dist(Hx)}")
print(f"Hz min distance: {min_dist(Hz)}")
print(f"CSS code: [[15, 5, {min(min_dist(Hx), min_dist(Hz))}]]")

print("\nPass 73 complete.")
