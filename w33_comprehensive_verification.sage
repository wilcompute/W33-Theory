
#!/usr/bin/env sage
"""
W33 Theory - Comprehensive SageMath Verification
================================================
This script performs rigorous computational verification of W33 Theory.
Run with: sage w33_comprehensive_verification.sage

Author: Wil Dahn
Date: January 2026
"""

from sage.all import *
import json

print("="*70)
print("W33 THEORY: COMPREHENSIVE SAGEMATH VERIFICATION")
print("="*70)

results = {}

# ============================================================================
# PART 1: GROUP STRUCTURE
# ============================================================================

print("\n[1/6] Analyzing Sp(4,3)...")

G = Sp(4, GF(3))
results['group_order'] = int(G.order())
print(f"  Order of Sp(4,3): {G.order()}")
assert G.order() == 51840, "Order mismatch!"

# ============================================================================
# PART 2: W33 GRAPH CONSTRUCTION
# ============================================================================

print("\n[2/6] Constructing W33 graph...")

V = VectorSpace(GF(3), 4)
J = matrix(GF(3), [[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])

def is_isotropic(v):
    return v * J * v == 0

def normalize(v):
    for i in range(4):
        if v[i] != 0:
            return tuple(v / v[i])
    return tuple(v)

# Find all isotropic 1-spaces
iso_vecs = [v for v in V if v != 0 and is_isotropic(v)]
iso_spaces = list(set(normalize(v) for v in iso_vecs))
results['num_isotropic_1spaces'] = len(iso_spaces)
print(f"  Isotropic 1-spaces: {len(iso_spaces)}")

# Build adjacency
def symp_form(u, v):
    return vector(GF(3), u) * J * vector(GF(3), v)

edges = [(i, j) for i in range(len(iso_spaces)) 
         for j in range(i+1, len(iso_spaces)) 
         if symp_form(iso_spaces[i], iso_spaces[j]) != 0]

W33 = Graph(edges)
results['num_vertices'] = W33.num_verts()
results['num_edges'] = W33.num_edges()
print(f"  Vertices: {W33.num_verts()}, Edges: {W33.num_edges()}")

# ============================================================================
# PART 3: SRG VERIFICATION
# ============================================================================

print("\n[3/6] Verifying strongly regular graph parameters...")

srg_params = W33.is_strongly_regular(parameters=True)
results['srg_parameters'] = srg_params
print(f"  SRG parameters: {srg_params}")

expected = (40, 12, 2, 4)
assert srg_params == expected, f"SRG mismatch: got {srg_params}, expected {expected}"
print("  ✓ Confirmed SRG(40, 12, 2, 4)")

# ============================================================================
# PART 4: SPECTRUM ANALYSIS
# ============================================================================

print("\n[4/6] Computing spectrum...")

spectrum = W33.spectrum()
results['spectrum'] = [(float(ev), int(mult)) for ev, mult in spectrum]
print(f"  Spectrum: {spectrum}")

# Check eigenvalue multiplicities
eig_12 = sum(1 for ev, m in spectrum if ev == 12 for _ in range(m))
eig_2 = sum(1 for ev, m in spectrum if ev == 2 for _ in range(m))
eig_m4 = sum(1 for ev, m in spectrum if ev == -4 for _ in range(m))

print(f"  Multiplicities: 12 (x{eig_12}), 2 (x{eig_2}), -4 (x{eig_m4})")

# ============================================================================
# PART 5: AUTOMORPHISM GROUP
# ============================================================================

print("\n[5/6] Computing automorphism group...")

aut = W33.automorphism_group()
results['automorphism_order'] = int(aut.order())
print(f"  |Aut(W33)| = {aut.order()}")
assert aut.order() == 51840, "Automorphism group order mismatch!"
print("  ✓ Confirmed |Aut(W33)| = |Sp(4,3)| = 51840")

# ============================================================================
# PART 6: CLIQUE COMPLEX AND HOMOLOGY
# ============================================================================

print("\n[6/6] Computing clique complex and homology...")

# Find all cliques
all_cliques = W33.cliques()
results['clique_number'] = W33.clique_number()
results['num_max_cliques'] = len(W33.cliques_maximum())
print(f"  Clique number: {W33.clique_number()}")
print(f"  Number of maximum cliques: {len(W33.cliques_maximum())}")

# Build simplicial complex
from sage.topology.simplicial_complex import SimplicialComplex

simplices = [tuple(sorted(c)) for c in all_cliques]
K = SimplicialComplex(simplices)

results['simplicial_dim'] = K.dimension()
results['f_vector'] = K.f_vector()
print(f"  Simplicial complex dimension: {K.dimension()}")
print(f"  f-vector: {K.f_vector()}")

# Betti numbers
betti = [K.betti(i) for i in range(K.dimension() + 1)]
results['betti_numbers'] = betti
print(f"  Betti numbers: {betti}")

# The key check: is β_1 related to 81?
print(f"\n  *** β_1 = {betti[1] if len(betti) > 1 else 'N/A'} ***")
print(f"  (Looking for connection to 81 = 3^4)")

# ============================================================================
# FINAL VERIFICATION
# ============================================================================

print("\n" + "="*70)
print("VERIFICATION SUMMARY")
print("="*70)

checks = [
    ("|W33| = 40", results['num_vertices'] == 40),
    ("|E| = 240", results['num_edges'] == 240),
    ("SRG(40,12,2,4)", results['srg_parameters'] == (40,12,2,4)),
    ("|Aut(W33)| = 51840", results['automorphism_order'] == 51840),
]

all_pass = True
for name, passed in checks:
    status = "✓" if passed else "✗"
    print(f"  {status} {name}")
    all_pass = all_pass and passed

print("\n" + "="*70)
if all_pass:
    print("ALL VERIFICATIONS PASSED!")
else:
    print("SOME VERIFICATIONS FAILED!")
print("="*70)

# Save results
with open('w33_sage_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print("\nResults saved to w33_sage_results.json")
