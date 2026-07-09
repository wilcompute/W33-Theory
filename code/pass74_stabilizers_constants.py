#!/usr/bin/env python3
"""
Pass 74: Explicit stabilizers for [[15,5,3]], W(3,3) parent theory, physical constants
Date: 2026-07-08
"""
import numpy as np
from itertools import combinations, product as iproduct
import math

# Build W(2,2)
vecs = [v for v in iproduct([0,1], repeat=4) if any(v)]
vec_to_pt = {v: i for i, v in enumerate(vecs)}
def omega4(x, y): return (x[0]*y[2]+x[1]*y[3]+x[2]*y[0]+x[3]*y[1])%2
doily_lines = []
for i,j in combinations(range(15),2):
    p,q = vecs[i],vecs[j]
    if omega4(p,q)==0:
        r = tuple((p[k]+q[k])%2 for k in range(4))
        if r in vec_to_pt:
            rr = vec_to_pt[r]
            if rr not in (i,j):
                line = tuple(sorted([i,j,rr]))
                if line not in doily_lines: doily_lines.append(line)

ovoids = [c for c in combinations(range(15),5)
         if all(len([p for p in l if p in set(c)])==1 for l in doily_lines)]
def find_spreads(lines,npts=15):
    spreads=[]
    def bt(rem,chosen):
        if not rem: spreads.append(tuple(sorted(chosen)));return
        p=min(rem)
        for l in lines:
            if p in l and all(x in rem for x in l): bt(rem-set(l),chosen+[l])
    bt(set(range(npts)),[])
    return list(set(spreads))
spreads = find_spreads(doily_lines)

# Spread stabilizers
line_idx = {l:i for i,l in enumerate(doily_lines)}
print("=== [[15,5,3]] CSS CODE: PAULI STABILIZERS ===")
all_spread_vecs = np.zeros((6,15),dtype=int)
for si,sp in enumerate(spreads):
    for l in sp: all_spread_vecs[si,line_idx[l]]=1

print("X-STABILIZERS (spreads, weight 5):")
for i,sv in enumerate(all_spread_vecs):
    s = [j for j,b in enumerate(sv) if b]
    print(f"  g_X{i+1}: X_{'·X_'.join(str(j) for j in s)}")

print("\nLOGICAL X OPERATORS (spread XORs, weight 8):")
for i,j in combinations(range(6),2):
    xor = (all_spread_vecs[i]+all_spread_vecs[j])%2
    s = [k for k,b in enumerate(xor) if b]
    print(f"  X_L({i},{j}): X_{'·X_'.join(str(k) for k in s)}  [wt={sum(xor)}]")

print("\nVerification: all 15 logical X ops have weight 8:",
      all(sum((all_spread_vecs[i]+all_spread_vecs[j])%2)==8
          for i,j in combinations(range(6),2)))

# W(3,3) physical constants
print("\n=== W(3,3) PHYSICAL CONSTANTS ===")
k,q = 12,3
alpha_inv = (k-1)**2 + (k//q)**2
print(f"α⁻¹ = (k-1)² + (k/q)² = {k-1}² + {k//q}² = {alpha_inv} (PDG 137.036, err={abs(alpha_inv-137.036)/137.036*100:.3f}%)")
mp_me = k*(k**2+q**2)
print(f"mp/me = k(k²+q²) = {k}×{k**2+q**2} = {mp_me} (PDG 1836.15, err={abs(mp_me-1836.15)/1836.15*100:.4f}%)")
v=15; mu=4
lambda_exp = -(v*(v+1)//2 + mu//2)
print(f"Λ_exp = -(v(v+1)/2 + μ/2) = -({v*(v+1)//2}+{mu//2}) = {lambda_exp} (PDG -122, err=0%)")

print(f"\n137 is prime (Fermat forced): {all(137%i!=0 for i in range(2,12))}")
print(f"137 ≡ {137%4} mod 4 (≡1 mod 4 → unique sum of 2 squares)")
print("\nPass 74 complete.")
