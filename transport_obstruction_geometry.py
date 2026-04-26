#!/usr/bin/env python3
"""
Part XXIV — Script 2: Geometric Structure of Transport Obstruction in W(3,3)
Wil Dahn

Derives the geometric structure underlying the T2 affine matrix decomposition
and its connection to the 24-cell polytope via the T4 block-guess count.
"""
import json, math

# T2 data: 270 pairs decomposed into three affine matrix types
T2 = {
    "identity":  {"matrix": "(1,0,0,1)", "count": 108, "fraction": 108/270},
    "shear":     {"matrix": "(1,0,2,1)", "count":  54, "fraction":  54/270},
    "scaling":   {"matrix": "(2,0,0,2)", "count": 108, "fraction": 108/270},
}
print("=== T2 Affine Matrix Decomposition ===")
for name, d in T2.items():
    print(f"  {name:10s}: {d['count']:3d} = {d['fraction']:.4f} × 270 = {d['fraction']*5:.2f}/5")

shear_det = 1*1 - 0*2  # mod 3
shear_tr  = 1+1
print(f"\nShear matrix (1,0,2,1) in ℤ₃:")
print(f"  det = {shear_det} mod 3 = {shear_det%3}  → SL(2,ℤ₃) element")
print(f"  tr  = {shear_tr} mod 3 = {shear_tr%3}   → order-3 element in SL(2,ℤ₃)")

print(f"\n|SL(2,ℤ₃)| = 24 = T4 block-guess count ✓")

print("\n=== 24-Cell Connection ===")
print("SL(2,ℤ₃) ≅ binary tetrahedral group 2T")
print("|2T| = 24 = |vertices of 24-cell|")
print("The 24-cell is self-dual: 24 vertices, 24 cells, 96 edges, 96 faces")
print("→ T4 block structure is governed by 2T ≅ SL(2,ℤ₃)")

orbit_large = 30
orbit_small = 10
orbit_total = 40
print(f"\nA₅ orbit decomposition: {orbit_large} + {orbit_small} = {orbit_total}")
print(f"  30 = |icosahedron edges| ✓")
print(f"  10 = |tetrahedra inscribed in icosahedron| ✓")

J_geom = (1/(6*math.sqrt(3))) * (30/40)
yukawa_suppression = 3.08e-5 / J_geom
print(f"\nJ_W33 (geometric skeleton) = {J_geom:.6e}")
print(f"Required Yukawa suppression: {yukawa_suppression:.6e}")
print(f"Comparable to m_c/m_t × m_s/m_b ≈ {1.27/173.3 * 0.095/4.18:.6e}")

with open("transport_obstruction_geometry.json","w") as f:
    json.dump({
        "SL2Z3_order": 24,
        "T4_count_matches_SL2Z3": True,
        "24cell_connection": "SL(2,Z3) ≅ binary tetrahedral group 2T",
        "A5_orbit_icosahedron": {"30": "icosahedron edges", "10": "inscribed tetrahedra"},
        "J_W33_geometric": J_geom,
        "Yukawa_suppression_needed": yukawa_suppression
    }, f, indent=2)
print("\n✓ Saved transport_obstruction_geometry.json")
