#!/usr/bin/env sage
"""
Simple check: Is W33 the clique complex of the symplectic graph?
"""

from sage.all import *
import json

# Load W33 data
with open("claude_workspace/data/w33_sage_incidence_h1.json") as f:
    data = json.load(f)

from lib.w33_io import W33DataPaths, load_w33_lines
from pathlib import Path
import sys

here = Path('.').resolve()
sys.path.insert(0, str(here / 'claude_workspace'))

paths = W33DataPaths.from_this_file(str(here / 'claude_workspace' / 'w33_sage_incidence_and_h1.py'))
lines = load_w33_lines(paths)

print("=== Is W33 the Clique Complex of Sp(4,3)? ===")
print()

# Build collinearity graph
edges = set()
for line in lines:
    line_list = sorted(line)
    for i in range(len(line_list)):
        for j in range(i+1, len(line_list)):
            edges.add((line_list[i], line_list[j]))

print(f"Collinearity graph: 40 vertices, {len(edges)} edges")

# Count triangles (3-cliques)
# A triangle exists if three vertices are mutually adjacent
# This means all three are on the same line
triangles = set()
for line in lines:
    line_list = sorted(line)
    # Each line contributes C(4,3) = 4 triangles
    for i in range(len(line_list)):
        for j in range(i+1, len(line_list)):
            for k in range(j+1, len(line_list)):
                triangles.add((line_list[i], line_list[j], line_list[k]))

print(f"Triangles (3-cliques): {len(triangles)}")
print(f"Expected: 40 lines × C(4,3) = 40 × 4 = {40 * 4}")

# Count 4-cliques (maximal cliques = the lines themselves)
four_cliques = set()
for line in lines:
    four_cliques.add(tuple(sorted(line)))

print(f"4-cliques (maximal): {len(four_cliques)}")

# W33 complex data
complex_data = data["simplicial_complex"]
print()
print("W33 Simplicial Complex:")
print(f"  Vertices (0-simplices): {complex_data['n0']}")
print(f"  Edges (1-simplices):    {complex_data['n1']}")
print(f"  Triangles (2-simplices): {complex_data['n2']}")
print(f"  Tetrahedra (3-simplices): {complex_data['n3']}")
print()
print("Clique Complex of Sp(4,3):")
print(f"  Vertices: 40")
print(f"  Edges: {len(edges)}")
print(f"  Triangles: {len(triangles)}")
print(f"  Tetrahedra: {len(four_cliques)}")
print()

if (complex_data['n0'] == 40 and
    complex_data['n1'] == len(edges) and
    complex_data['n2'] == len(triangles) and
    complex_data['n3'] == len(four_cliques)):
    print("★ W33 IS the clique complex of Sp(4,3)! ★")
    print()
    print("This means W33 is the FLAG COMPLEX of the symplectic polar space!")
    print()
    print("The simplicial structure is:")
    print("  - Vertices = points of PG(3,3)")
    print("  - k-simplices = sets of k+1 mutually collinear points")
    print("  - Maximal simplices = totally isotropic lines (4 points each)")
else:
    print("Sizes don't match exactly. Let's see the discrepancy:")
    print(f"  Edges: {complex_data['n1']} vs {len(edges)}")
    print(f"  Triangles: {complex_data['n2']} vs {len(triangles)}")
    print(f"  Tetrahedra: {complex_data['n3']} vs {len(four_cliques)}")

print()
print("=== Solomon-Tits Connection ===")
print()
print("The Solomon-Tits theorem says:")
print("  For a building of dimension n, the top homology H_n")
print("  carries the Steinberg representation.")
print()
print("For the clique complex of Sp(4,3):")
print("  - Maximum clique size = 4")
print("  - So complex dimension = 3 (tetrahedra)")
print("  - But the 'effective' dimension for polar space = 1")
print("    (lines are the maximal totally isotropic subspaces)")
print()
print("The appearance of Steinberg in H_1 (not H_3) suggests")
print("the homology is detecting the BUILDING structure, not")
print("the clique complex structure!")
print()
print("H_1 = Steinberg is the CRITICAL insight.")
