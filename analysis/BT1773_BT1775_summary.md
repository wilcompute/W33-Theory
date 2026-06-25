# BT1773-BT1775 summary

Executed all three requested next moves after BT1770-BT1772.

## BT1773: 600-cell BC-ring embedding candidate

Added `analysis/bt1773_600cell_bc_ring_embedding.py`.

The script generates the standard 120-vertex 600-cell, recovers its 720 edges and 600 tetrahedral facets, builds the 4-regular facet-dual graph, and finds a deterministic 30-cycle of face-adjacent tetrahedral facets.

Boundary: this is a real 600-cell facet-level BC-ring candidate. The next step is matching the BT1767 three-strand completion graph to this specific 30-facet cycle.

## BT1774: E8 inversion witness

Added `analysis/bt1774_e8_inversion_witness.py`.

The BT1771 inversion target is realized. Two length-7 conjugation paths meet:

```text
FSEQ = [0,5,6,5,7,6,5]
BSEQ = [0,1,2,0,3,1,2]
h = inverse(word(BSEQ)) * word(FSEQ)
```

Local verification showed:

```text
h C h^{-1} = C^{-1} on 240 E8 roots
h maps all 40 C^5 Coxeter hexagons whole to C^5 hexagons
```

Boundary: realizes r=29 inversion only, not the other six coprime exponent candidates.

## BT1775: stabilizer-fiber solver scaffold

Added `analysis/bt1775_stabilizer_fiber_solver_scaffold.py`.

The stabilizer-fiber problem is now reduced to a finite CSP:

```text
9 Hesse slots
12 compatible PSL(2,7) automorphism choices per slot
raw product size = 12^9 = 5,159,780,352
incumbent choice lies in every slot domain
```

Boundary: full exhaustive enumeration was not completed in this pass. The solver now needs precomputed admissible triples over the 18 Hesse triangle constraints and arc consistency before DFS.
