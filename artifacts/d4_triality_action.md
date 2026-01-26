# D4 Triality Action on W33's 4-Triangle Structure

## Triangle Statistics

- W33 vertices: 40
- Unique triangles across all H12 decompositions: 160

### Triangles shared by base vertices

- 160 triangles appear in 1 H12 decompositions

## Triangle Adjacency Graph

- Vertices (unique triangles): 160
- Edges (co-occurrence in H12): 240
- Degree set: [np.int64(3)]

### Triangle Graph Components

- Component sizes: [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
- All components are K4: True

## H12 Intersection Patterns

For W33-adjacent vertices (i, j), how many H12 triangles do they share?

- 240 adjacent pairs share 0 triangles

For W33-non-adjacent vertices (i, j), how many H12 triangles do they share?

- 540 non-adjacent pairs share 0 triangles

## Triangle Vertex Analysis

Triangle (1, 2, 3):
  - Common neighbors: ab=2, bc=2, ac=2, abc=1
Triangle (13, 14, 15):
  - Common neighbors: ab=2, bc=2, ac=2, abc=1
Triangle (16, 17, 18):
  - Common neighbors: ab=2, bc=2, ac=2, abc=1
Triangle (19, 20, 21):
  - Common neighbors: ab=2, bc=2, ac=2, abc=1
Triangle (0, 2, 3):
  - Common neighbors: ab=2, bc=2, ac=2, abc=1

## D4 Connection

The 4-triangle decomposition of H12 suggests D4 structure:

- D4 Dynkin diagram has 4-fold symmetry (3 legs from center)
- D4 has 24 roots = 4 × 6 (4 groups of 6)
- W33 eigenvalue 2 has multiplicity 24
- Each H12 decomposition gives 4 triangles × 3 vertices = 12

### Inter-triangle W33 adjacencies

For v0 = 0, H12 triangles: [(1, 2, 3), (13, 14, 15), (16, 17, 18), (19, 20, 21)]

Inter-triangle edge counts (within H12, should be 0 since disjoint):
  T0: [0, 0, 0, 0]
  T1: [0, 0, 0, 0]
  T2: [0, 0, 0, 0]
  T3: [0, 0, 0, 0]

Each triangle vertex is adjacent to base vertex v0 by definition.

In the full W33, are vertices from different triangles connected?
  T0: [0, 0, 0, 0]
  T1: [0, 0, 0, 0]
  T2: [0, 0, 0, 0]
  T3: [0, 0, 0, 0]

Total inter-triangle edges: 0

