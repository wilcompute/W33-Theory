#!/usr/bin/env sage
"""
W33 - APARTMENTS AND THE 81 CYCLES

We found 33 apartments. Let's understand:
1. Why 33?
2. How do apartments relate to the 81 cycles?
3. What is the structure of the apartment system?
"""

from sage.all import *
import numpy as np
from itertools import product, combinations, permutations

print("=" * 70)
print("W33 APARTMENTS DEEP DIVE")
print("=" * 70)

# Build the symplectic polar space W(3,3)
def symplectic_form(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

def normalize(v):
    for i in range(4):
        if v[i] != 0:
            inv = pow(v[i], -1, 3)
            return tuple((inv * x) % 3 for x in v)
    return None

proj_points = set()
for v in product(range(3), repeat=4):
    if v != (0, 0, 0, 0):
        nv = normalize(v)
        if nv:
            proj_points.add(nv)

proj_points = sorted(proj_points)
point_to_idx = {p: i for i, p in enumerate(proj_points)}
n = len(proj_points)

# Adjacency
adj = [[False] * n for _ in range(n)]
for i, p1 in enumerate(proj_points):
    for j, p2 in enumerate(proj_points):
        if i < j and symplectic_form(p1, p2) == 0:
            adj[i][j] = adj[j][i] = True

# Find lines
lines_set = set()
for i in range(n):
    for j in range(i+1, n):
        if adj[i][j]:
            common = [k for k in range(n) if k != i and k != j and adj[i][k] and adj[j][k]]
            for k, l in combinations(common, 2):
                if adj[k][l]:
                    lines_set.add(tuple(sorted([i, j, k, l])))

lines = sorted(lines_set)
line_to_idx = {line: i for i, line in enumerate(lines)}

print(f"W33: {n} points, {len(lines)} lines")

# =============================================================================
# COUNT APARTMENTS PROPERLY
# =============================================================================
print("\n" + "=" * 70)
print("COUNTING APARTMENTS")
print("=" * 70)

# An apartment is determined by a symplectic frame (symplectic basis)
# A symplectic basis of GF(3)⁴ is {e₁, e₂, f₁, f₂} where:
#   ⟨eᵢ, fⱼ⟩ = δᵢⱼ (Kronecker delta)
#   ⟨eᵢ, eⱼ⟩ = ⟨fᵢ, fⱼ⟩ = 0

# The number of symplectic bases of GF(q)^{2n} is:
# |Sp(2n, q)| = product over i=1 to n of (q^{2i} - 1) × q^{i-1}

# For Sp(4, 3):
# |Sp(4, 3)| = (3² - 1)(3⁴ - 1) × 3^{0+1} = 8 × 80 × 3 = 51840 / 2 = 25920
# Wait, let me compute this properly

# |Sp(4,3)| = 3^4 × (3^2-1)(3^4-1)/2 = ... let me just compute

# Actually, the number of apartments equals |G|/|N_G(A)| where A is an apartment
# and N_G(A) is the stabilizer

# For Sp(4,q), the number of apartments is:
# (q+1)^2 × (q^2+1) / ... complicated

# Let me just enumerate them directly

def find_all_apartments():
    """Find all apartments by looking for 8-cycles in incidence graph."""
    apartments = set()
    
    for p0 in range(n):
        # Lines through p0
        lines_p0 = [j for j, line in enumerate(lines) if p0 in line]
        
        for L0 in lines_p0:
            pts_L0 = list(lines[L0])
            for p1 in pts_L0:
                if p1 == p0:
                    continue
                    
                lines_p1 = [j for j, line in enumerate(lines) if p1 in line and j != L0]
                for L1 in lines_p1:
                    pts_L1 = list(lines[L1])
                    for p2 in pts_L1:
                        if p2 == p1 or adj[p0][p2]:  # p0 and p2 must be opposite
                            continue
                            
                        lines_p2 = [j for j, line in enumerate(lines) if p2 in line and j != L1]
                        for L2 in lines_p2:
                            pts_L2 = list(lines[L2])
                            for p3 in pts_L2:
                                if p3 == p2 or adj[p1][p3]:  # p1 and p3 must be opposite
                                    continue
                                    
                                # Check if L3 exists connecting p3 back to p0
                                for L3 in [j for j, line in enumerate(lines) 
                                          if p3 in line and p0 in line and j != L2 and j != L0]:
                                    # Found apartment!
                                    pts = tuple(sorted([p0, p1, p2, p3]))
                                    lns = tuple(sorted([L0, L1, L2, L3]))
                                    apartments.add((pts, lns))
    
    return apartments

apartments = find_all_apartments()
print(f"Total apartments: {len(apartments)}")

# =============================================================================
# ANALYZE APARTMENT STRUCTURE
# =============================================================================
print("\n" + "=" * 70)
print("APARTMENT ANALYSIS")
print("=" * 70)

# The apartments should correspond to decompositions of GF(3)⁴ into
# two hyperbolic planes

# Let's look at the first few apartments
apt_list = list(apartments)[:5]
for i, (pts, lns) in enumerate(apt_list):
    print(f"\nApartment {i+1}:")
    print(f"  Points: {pts}")
    print(f"  Coordinates: {[proj_points[p] for p in pts]}")
    print(f"  Lines: {lns}")

# =============================================================================
# THE 81 CYCLES AND APARTMENTS
# =============================================================================
print("\n" + "=" * 70)
print("RELATIONSHIP: APARTMENTS ↔ 81 CYCLES")
print("=" * 70)

# Each apartment (8-cycle in incidence graph) corresponds to a 4-cycle
# in the point graph (connecting p0-p1-p2-p3-p0)

# Let's count how many induced 4-cycles come from apartments
apartment_4cycles = set()
for pts, lns in apartments:
    p0, p1, p2, p3 = sorted(pts)
    # The 4-cycle connects adjacent pairs
    # In an apartment: p0~p1, p1~p2, p2~p3, p3~p0, with p0≁p2, p1≁p3
    # But we need to figure out the actual adjacencies
    
    # Actually, in the octagon, the adjacencies are:
    # p0 ~ p1 via L0, p1 ~ p2 via L1, p2 ~ p3 via L2, p3 ~ p0 via L3
    pass

# Let's verify by examining one apartment
pts, lns = apt_list[0]
p0, p1, p2, p3 = pts
print(f"\nApartment 1 adjacencies:")
print(f"  {p0} ~ {p1}? {adj[p0][p1]}")
print(f"  {p1} ~ {p2}? {adj[p1][p2]}")
print(f"  {p2} ~ {p3}? {adj[p2][p3]}")
print(f"  {p3} ~ {p0}? {adj[p3][p0]}")
print(f"  {p0} ~ {p2}? {adj[p0][p2]} (opposite)")
print(f"  {p1} ~ {p3}? {adj[p1][p3]} (opposite)")

# =============================================================================
# THE WEYL GROUP ACTION
# =============================================================================
print("\n" + "=" * 70)
print("WEYL GROUP AND APARTMENTS")
print("=" * 70)

print("""
For Sp(4), the Weyl group is W(C₂) = dihedral group of order 8.

The Weyl group acts on each apartment as the symmetry group of the octagon:
  - 4 rotations (by 0°, 90°, 180°, 270°)
  - 4 reflections

The 8 chambers in an apartment are permuted by W(C₂).

Key formula:
  # apartments = |G| / (|B| × |W|)
  
where B is a Borel subgroup and W is the Weyl group.
""")

# For PSp(4,3): |G| = 25920, |W| = 8
# |B| = |T| × |U| where T = torus, U = unipotent radical
# For Sp(4,3): |B| = (3-1)² × 3^4 = 4 × 81 = 324
# So # apartments = 25920 / (324 × 8) = 25920 / 2592 = 10

# But we found 33 apartments in the full O(5,3):C₂!
# This is because the outer automorphism creates more apartments

# Actually wait - let me recalculate for O(5,3):C₂
# |O(5,3):C₂| = 51840

print(f"\nExpected apartments calculation:")
print(f"  |O(5,3):C₂| = 51840")
print(f"  Each apartment has stabilizer of size 51840/{len(apartments)} = {51840//len(apartments) if len(apartments) > 0 else 'N/A'}")

# =============================================================================
# SYMPLECTIC FRAMES
# =============================================================================
print("\n" + "=" * 70)
print("SYMPLECTIC FRAMES")
print("=" * 70)

# A symplectic frame is an ordered basis (e₁, e₂, f₁, f₂) with
# ⟨eᵢ, fⱼ⟩ = δᵢⱼ

# Let's count them
def is_symplectic_frame(e1, e2, f1, f2):
    """Check if (e1, e2, f1, f2) is a symplectic frame."""
    # Check: ⟨e1, f1⟩ = 1, ⟨e2, f2⟩ = 1, all others = 0
    return (symplectic_form(e1, f1) == 1 and
            symplectic_form(e2, f2) == 1 and
            symplectic_form(e1, e2) == 0 and
            symplectic_form(f1, f2) == 0 and
            symplectic_form(e1, f2) == 0 and
            symplectic_form(e2, f1) == 0)

# The standard symplectic frame
e1 = (1, 0, 0, 0)
e2 = (0, 1, 0, 0)
f1 = (0, 0, 1, 0)
f2 = (0, 0, 0, 1)

print(f"Standard frame check: {is_symplectic_frame(e1, e2, f1, f2)}")

# The apartment from this frame has points:
# [e1], [e2], [f1], [f2] and their isotropic combinations

# For a symplectic frame, the apartment points are:
# The 4 basis vectors plus some combinations
# Actually, for the standard frame:
frame_pts = [
    point_to_idx.get(normalize(e1)),
    point_to_idx.get(normalize(e2)),
    point_to_idx.get(normalize(f1)),
    point_to_idx.get(normalize(f2))
]
print(f"Standard frame points: {frame_pts}")
print(f"  Coords: {[proj_points[p] for p in frame_pts if p is not None]}")

# =============================================================================
# THE TITS CONE AND 81
# =============================================================================
print("\n" + "=" * 70)
print("WHY 81 CYCLES? THE STEINBERG CONNECTION")
print("=" * 70)

print("""
The number 81 = 3⁴ arises from the ROOT SYSTEM of type C₂:

For the root system C₂:
  - 4 positive roots: α₁, α₂, α₁+α₂, 2α₁+α₂
  - Total roots: 8
  
The Steinberg representation has dimension q^N where:
  N = # positive roots = 4
  So dim = 3⁴ = 81 ✓

The 81 independent cycles in H₁ correspond to:
  - The 81 elements of the Sylow 3-subgroup
  - The 81 cosets in some quotient
  - The 81-dimensional irreducible representation

Each generator of π₁ = F₈₁ can be thought of as a 
"twisted apartment path" - a non-contractible loop that
goes through the building in a specific pattern.
""")

# Count how the 33 apartments are related to the 81 cycles
print(f"\n33 apartments × ? = 81 cycles?")
print(f"  81 / 33 ≈ {81/33:.2f}")
print(f"  But 33 doesn't divide 81...")

# Maybe the 81 cycles come from a different structure
# Let's look at pairs of apartments that share something

print("\n" + "=" * 70)
print("APARTMENT OVERLAPS")
print("=" * 70)

# How many apartments share a given point?
point_apt_count = [0] * n
for pts, lns in apartments:
    for p in pts:
        point_apt_count[p] += 1

print(f"Apartments per point: min={min(point_apt_count)}, max={max(point_apt_count)}, avg={sum(point_apt_count)/n:.2f}")

# How many apartments share a given line?
line_apt_count = [0] * len(lines)
for pts, lns in apartments:
    for l in lns:
        line_apt_count[l] += 1

print(f"Apartments per line: min={min(line_apt_count)}, max={max(line_apt_count)}, avg={sum(line_apt_count)/len(lines):.2f}")

# How many apartments share a given (point, line) flag?
flag_apt_count = {}
for pts, lns in apartments:
    for p in pts:
        for l in lns:
            if p in lines[l]:
                flag = (p, l)
                flag_apt_count[flag] = flag_apt_count.get(flag, 0) + 1

print(f"Apartments per flag: {set(flag_apt_count.values())}")
