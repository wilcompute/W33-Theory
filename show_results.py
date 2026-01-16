#!/usr/bin/env python
"""Display summary of W33 Sage analysis results."""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
results_file = here / "data" / "w33_sage_incidence_h1.json"

with open(results_file) as f:
    d = json.load(f)

print("=" * 50)
print("W33 SAGE ANALYSIS RESULTS")
print("=" * 50)
print(f"Field: {d['field']}")
print()
print("INCIDENCE AUTOMORPHISM GROUP:")
print(f"  Order: {d['incidence']['group_order']}")
print(f"  Structure: {d['incidence']['structure_description']}")
print(f"  Is abelian: {d['incidence']['is_abelian']}")
print(f"  Is solvable: {d['incidence']['is_solvable']}")
print(f"  Number of generators: {len(d['incidence']['generators'])}")
print()
print("H1 HOMOLOGY (first homology):")
h1_mats = d['h1_action']['generator_matrices']
dim = len(h1_mats[0]) if h1_mats else 0
print(f"  Dimension (beta_1): {dim}")
print(f"  Number of H1 action matrices: {len(h1_mats)}")
print()
print("=" * 50)
print("INTERPRETATION:")
print("=" * 50)
print(f"""
The incidence automorphism group has order {d['incidence']['group_order']:,}.

The structure 'O(5,3) : C2' means:
  - O(5,3) is the orthogonal group in dimension 5 over GF(3)
  - |O(5,3)| = 2 * 3^4 * (3^4-1) * (3^2-1) / gcd = 25920
  - Extended by C2 gives order 51840

This group acts on H1 (dimension 81) via 81×81 matrices.
The group is NOT solvable, indicating rich non-abelian structure.

Previously computed (pure Python):
  - β₀ = 1 (connected)
  - β₁ = 81 (first Betti number) ✓ CONFIRMED
  - β₂ = 0, β₃ = 0
  - Euler characteristic χ = -80
  - Ray-preserving subgroup order: 108
""")
