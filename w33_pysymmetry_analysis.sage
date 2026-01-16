
# W33 Theory - pysymmetry Analysis
# Requires SageMath with pysymmetry installed

import sys
sys.path.insert(0, '/path/to/pysymmetry')

from sage.all import *
from pysymmetry import FiniteGroup, representation

print("="*60)
print("W33 THEORY: pysymmetry Character Analysis")
print("="*60)

# Create Sp(4,3)
G_matrix = Sp(4, GF(3))
print(f"\nSp(4,3) order: {G_matrix.order()}")

# Convert to permutation group for pysymmetry
G_perm = G_matrix.as_permutation_group()
print(f"Permutation degree: {G_perm.degree()}")

# Create FiniteGroup object
G = FiniteGroup(G_perm)
print(f"\nFiniteGroup created with {G.order()} elements")

# Get regular representation
print("\nComputing regular representation...")
reg = G.regular_representation()
print(f"Regular representation dimension: {G.order()}")

# Decompose into irreducibles
print("\nDecomposing regular representation...")
# This will give us all irrep multiplicities

# Character table
print("\nCharacter table:")
ct = G.character_table()
print(ct)

# Look for special dimensions
print("\nSearching for W33-related dimensions in irreps...")
dims = [ct[i,0] for i in range(ct.nrows())]
print(f"Irrep dimensions: {sorted(dims)}")

# Check for dimensions related to W33
w33_nums = [27, 40, 56, 78, 81, 133]
for d in w33_nums:
    if d in dims:
        print(f"  {d} IS an irrep dimension!")
    else:
        print(f"  {d} not an irrep dimension")

# Check if 81 can be constructed as sum of irreps
print("\n81 as sum of irreps:")
from itertools import combinations_with_replacement
for r in range(1, 6):
    for combo in combinations_with_replacement(dims, r):
        if sum(combo) == 81:
            print(f"  81 = {' + '.join(map(str, combo))}")

print("\n*** pysymmetry analysis complete ***")
