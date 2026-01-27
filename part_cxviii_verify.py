"""
W33 THEORY - PART CXVIII: EXPLICIT CONSTRUCTION (Summary)
=========================================================

SageMath verification of the 40 = 1 + 12 + 27 decomposition.
"""

import os, sys
SAGE_DIR = "/mnt/c/Users/wiljd/OneDrive/Documents/GitHub/WilsManifold/external/sage"
os.environ["PATH"] = f"{SAGE_DIR}/bin:" + os.environ.get("PATH", "")
sys.path.insert(0, f"{SAGE_DIR}/lib/python3.12/site-packages")

from sage.all import *
import json

print("=" * 60)
print(" PART CXVIII: THE KEY VERIFICATION")
print("=" * 60)

results = {"verified": {}}

# Build W33
G = graphs.SymplecticPolarGraph(4, 3)
print(f"\nW33 = Sp(4,3) polar graph")
print(f"Vertices: {G.num_verts()}")
print(f"Edges: {G.num_edges()}")
results["verified"]["vertices"] = G.num_verts()
results["verified"]["edges"] = G.num_edges()

# Get automorphism group
Aut = G.automorphism_group()
print(f"|Aut(W33)| = {Aut.order()}")
results["verified"]["aut_order"] = Aut.order()

# THE KEY DISCOVERY: 40 = 1 + 12 + 27
print("\n" + "=" * 60)
print(" THE 40 = 1 + 12 + 27 DECOMPOSITION")
print("=" * 60)

v0 = G.vertices()[0]
neighbors = list(G.neighbors(v0))
non_neighbors = [v for v in G.vertices() if v != v0 and v not in neighbors]

print(f"\nVertex v0: 1")
print(f"Neighbors of v0: {len(neighbors)}")
print(f"Non-neighbors of v0: {len(non_neighbors)}")
print(f"\n1 + {len(neighbors)} + {len(non_neighbors)} = {1 + len(neighbors) + len(non_neighbors)}")

results["verified"]["decomposition"] = {
    "vertex": 1,
    "neighbors": len(neighbors),
    "non_neighbors": len(non_neighbors),
    "total": 1 + len(neighbors) + len(non_neighbors)
}

if len(neighbors) == 12 and len(non_neighbors) == 27:
    print("\n*** VERIFIED: 40 = 1 + 12 + 27 ***")
    print("*** singlet + Reye(12) + Albert(27) ***")
    results["verified"]["decomposition_verified"] = True

# The neighbor subgraph
print("\n" + "=" * 60)
print(" THE 12 NEIGHBORS STRUCTURE")
print("=" * 60)

H12 = G.subgraph(neighbors)
print(f"\nNeighbor subgraph:")
print(f"  Vertices: {H12.num_verts()}")
print(f"  Edges: {H12.num_edges()}")
print(f"  Is regular: {H12.is_regular()}")
if H12.is_regular():
    print(f"  Degree: {H12.degree(neighbors[0])}")

if H12.is_strongly_regular():
    params = H12.is_strongly_regular(parameters=True)
    print(f"  SRG parameters: {params}")
    results["verified"]["neighbor_srg"] = list(params)

# Eigenvalues
print("\n" + "=" * 60)
print(" EIGENVALUE STRUCTURE")
print("=" * 60)

A = G.adjacency_matrix()
char_poly = A.characteristic_polynomial()
roots = char_poly.roots()
print("\nEigenvalues and multiplicities:")
for root, mult in roots:
    print(f"  eigenvalue = {root}, multiplicity = {mult}")
results["verified"]["eigenvalues"] = [(int(r), int(m)) for r, m in roots]

# Check for multiplicity 24
for root, mult in roots:
    if mult == 24:
        print(f"\n*** Found multiplicity 24 = D4 roots! ***")
        print(f"*** eigenvalue = {root} ***")
        results["verified"]["d4_eigenvalue"] = int(root)

# Save results
with open('PART_CXVIII_verified.json', 'w') as f:
    json.dump(results, f, indent=2, default=int)
print("\nResults saved to: PART_CXVIII_verified.json")

print("\n" + "=" * 60)
print(" END OF VERIFICATION")
print("=" * 60)
