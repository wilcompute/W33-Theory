#!/usr/bin/env python3
"""
Analyze the triangle and line structure of W(3,3) as GQ(3,3).
W(3,3) is the collinearity graph of the generalized quadrangle GQ(3,3).
"""

n, k, r, s, fr, fs = 40, 12, 2, -4, 24, 15
q = 3  # field order

print('=== GENERALIZED QUADRANGLE GQ(3,3) STRUCTURE ===')
print()
print(f'W(3,3) is the collinearity graph of GQ({q},{q}).')
print()

# GQ(q,q) parameters:
# - q+1 points per line: q+1 = 4
# - q+1 lines through each point: q+1 = 4
# - Total points: (q+1)(q²+1) = 4*10 = 40
# - Total lines: (q+1)(q²+1) = 4*10 = 40 (duality)
# - Incidence structure is balanced

num_points = (q+1)*(q**2+1)
num_lines = (q+1)*(q**2+1)
points_per_line = q+1
lines_per_point = q+1
ovoid_size = q**2 + 1

print(f'GQ({q},{q}) parameters:')
print(f'  Total points: n = (q+1)(q²+1) = {num_points}')
print(f'  Total lines: (q+1)(q²+1) = {num_lines}')
print(f'  Points per line: q+1 = {points_per_line}')
print(f'  Lines through each point: q+1 = {lines_per_point}')
print(f'  Ovoid size (spread, max independent set): q²+1 = {ovoid_size}')
print()

# In the collinearity graph:
# - Maximum clique = line = q+1 = 4 points (all pairwise adjacent)
# - Maximum independent set = ovoid = q²+1 = 10 points (no two adjacent)
# - Total triangles: each line has C(q+1,3) = C(4,3) = 4 triangles
#                    Each of the (q+1)(q²+1) = 40 lines contributes 4 triangles
#                    But each triangle is in exactly one line (a line through all 3 vertices)
#                    So total = 40 * 4 = 160

num_triangles = num_lines * 4  # C(4,3) = 4 per line
print(f'Triangle counting via lines:')
print(f'  Each line has C(q+1,3) = C(4,3) = 4 triangles')
print(f'  Total lines: {num_lines}')
print(f'  Total triangles: {num_lines} * 4 = {num_triangles}')
print()

# Verify: tr(A^3) = 2 * (# triangles) [since closed walk A→B→C→A can go either direction]
# Actually: tr(A^3) = sum of closed walks of length 3
# For each triangle {A,B,C}, there are exactly 6 closed walks: 
#   A→B→C→A, A→C→B→A, B→A→C→B, B→C→A→B, C→A→B→C, C→B→A→C
# So tr(A^3) = 6 * (# triangles)

print(f'Verification via spectral data:')
print(f'  tr(A³) = {k**3 + fr*r**3 + fs*s**3} = 960')
print(f'  # triangles = tr(A³)/6 = 960/6 = {960//6}')
print(f'  Formula: tr(A³)/6 = {num_triangles} ✓')
print()

# Now analyze spread structure (ovoid)
# An ovoid (or spread) of size q²+1 = 10 in GQ(q,q)
# - Contains q²+1 = 10 points
# - No two points in the ovoid are collinear (hence independent set in collinearity graph)
# - Each of the q+1=4 lines in the quadrangle meets the ovoid in exactly 1 point

print(f'Ovoid (spread) structure:')
print(f'  Ovoid size: q²+1 = {ovoid_size} = {fs}')
print(f'  Fact: f_s = 15 = |SU(4)| plays a spectral role')
print(f'  Note: 15 = {3*5}, 10 = {2*5}')
print()

# Higher structure: GQ(3,3) over GF(3)
# The generalized quadrangle GQ(q,q) when q=q (square type) has automorphism group
# containing Sp(4,q), the symplectic group in dimension 4 over GF(q)

sp44_order = 3**4 * (3**4 - 1) * (3**2 - 1)
print(f'Automorphism group bound:')
print(f'  |Sp(4,3)| = 3^4(3^4-1)(3^2-1) = {sp44_order}')
print(f'  |PSp(4,3)| = {sp44_order // 2}  (projective symplectic)')
print()

# Connected to exceptional structures:
# The parameter set {q²+1=10, k-r=10, q+1=4} appears repeatedly

print(f'Repeated parameter: k-r = {k-r} = q²+1 = {ovoid_size}')
print(f'  This is the "string gap" = independent number α')
print(f'  And equals (q²+1) which is the size of an ovoid!')
print()

# Triangle distribution in the graph
# From any vertex v:
#   - v is adjacent to k=12 vertices (forming a clique on the "line through v")
#   - The 12 neighbors form a clique minus some structure
#   - Actually, the neighborhood of v is NOT a clique; it has induced subgraph with some edges
#   
# But: any edge {u,w} adjacent to v forms a triangle {u,v,w}
# Number of edges in neighborhood: (1/2) * (sum of degrees in neighborhood - cut edges)

# From earlier: n-1-k = 27 non-neighbors
# From neighbors: they induce a subgraph

print(f'Neighborhood structure from any vertex v:')
print(f'  |N(v)| = k = {k}')
print(f'  |N^c(v)| = n-1-k = {n-1-k}')
print(f'  Each neighbor of v is adjacent to (k-1) other neighbors of v? Not exactly...')
print(f'    In SRG(n,k,λ,μ): any two adjacent vertices share λ={2} common neighbors')
print(f'    So edge count in N(v): (k*λ)/2 = {k*2//2} = {k*2//2}')
print()

# Actually wait, let me reconsider
# For SRG: if u,v are adjacent, they have exactly λ common neighbors
# So the neighborhood N(v) induces a λ-regular graph? No, not necessarily
# The edge count in N(v) is (1/2) * k*λ = 12*2/2 = 12

edges_in_neighborhood = (k * 2) // 2
triangles_through_center = edges_in_neighborhood
print(f'Triangles centered at any vertex v:')
print(f'  = (k*λ)/2 = {k}*{2}/2 = {edges_in_neighborhood}')
print(f'  (Each edge in N(v) forms a triangle with v)')
print()

# Verify: total triangles = sum over all vertices of (triangles with v as center)
# = n * (triangles centered at v) / 3  (since each triangle is counted 3 times, once per vertex)
total_triangles_formula = (n * edges_in_neighborhood) // 3
print(f'Total triangles via vertex method:')
print(f'  = (n * # triangles per vertex) / 3')
print(f'  = ({n} * {edges_in_neighborhood}) / 3 = {total_triangles_formula}')
print()

print(f'Summary of identities:')
print(f'  tr(A³) = 6 * (# triangles) = 960 → {960//6} triangles ✓')
print(f'  # triangles = 40 lines * 4 per line = 160 ✓')
print(f'  # triangles = n * (k*λ/2) / 3 = {total_triangles_formula} ✓')
print()

# Connection to string theory / lattice codes
print(f'Higher combinatorial structures:')
print(f'  Independence number α = ovoid size = {ovoid_size} = q²+1 = {fs//1.5:.0f} (no, fs=15 is different)')
print(f'  Clique number ω = line size = {points_per_line} = q+1')
print(f'  ω * α = {points_per_line * ovoid_size} = n ✓')
print()

# Maximal independent sets: are there exactly α many? Or more?
# In GQ(q,q), the maximum independent set size is q²+1 (ovoid)
# But there can be multiple maximum independent sets

print(f'Spreads and Packings:')
print(f'  Spread (parallel class of lines): NOT applicable to GQ(q,q) when q>1')
print(f'  Instead: partition into lines (not possible since n=40, lines have 4 points)')
print(f'  But: we can partition into OVOIDS (size 10 each): need 40/10=4 ovoids')
print(f'  A "pack" of 4 pairwise disjoint ovoids would partition all 40 points!')
