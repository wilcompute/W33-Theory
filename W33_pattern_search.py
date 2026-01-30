"""
W33 THEORY - CREATIVE PATTERN SEARCH
====================================

This script systematically searches for new, nontrivial equitable partitions and substructures in the W33 (SymplecticPolarGraph(4,3)) graph.
It analyzes induced subgraphs, automorphism groups, and spectral properties, looking for new patterns or correspondences with known mathematical objects.
"""

from itertools import combinations

from sage.all import *

# Build W33

# Store interesting partitions
interesting_partitions = []


# Print only the first 5 cliques and cocliques of size 4


# Save results
import json


def main():
    G = graphs.SymplecticPolarGraph(4, 3)
    print(f"W33: {G.num_verts()} vertices, {G.num_edges()} edges")
    print("Searching for cliques of size 4...")
    for i, clq in enumerate(G.cliques(4)):
        if len(clq) == 4:
            print(f"Clique {i+1}: {clq}")
            if i >= 4:
                break
    print("Searching for cocliques of size 4...")
    for i, ccq in enumerate(G.cocliques(4)):
        if len(ccq) == 4:
            print(f"Coclique {i+1}: {ccq}")
            if i >= 4:
                break
    with open("W33_pattern_search_results.json", "w") as f:
        json.dump(interesting_partitions, f, indent=2, default=str)
    print("Results saved to: W33_pattern_search_results.json")


if __name__ == "__main__":
    main()
