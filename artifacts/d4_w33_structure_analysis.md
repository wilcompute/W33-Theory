# D4 Structure Analysis in W33

## Eigenvalue Structure

- λ = 12: multiplicity 1
- λ = 2: multiplicity 24
- λ = -4: multiplicity 15

## H12 Analysis (neighbor subgraph)

Checked 5 vertices:
- v0: 4 components of sizes [3, 3, 3, 3], 4 triangles
- v1: 4 components of sizes [3, 3, 3, 3], 4 triangles
- v2: 4 components of sizes [3, 3, 3, 3], 4 triangles
- v3: 4 components of sizes [3, 3, 3, 3], 4 triangles
- v4: 4 components of sizes [3, 3, 3, 3], 4 triangles

**H12 is always 4 disjoint triangles: True**

## D4 Root System

- D4 has 24 roots
- Root adjacency degree (|ip|=1): 16

- D4 root graph components: 1
- Component sizes: [24]

## K4,4 Tetrahedral Subgraph

- 8 tetrahedral rays: [24, 25, 26, 27, 32, 33, 34, 35]
- Bipartition: {'0': [24, 26, 33, 35], '1': [25, 27, 32, 34]}

### Tetrahedral rays in H12 decomposition

- v0 neighbors contain 0 tetrahedral rays: []
- v1 neighbors contain 0 tetrahedral rays: []
- v2 neighbors contain 4 tetrahedral rays: [32, 33, 34, 35]

## Key Observations

1. **H12 = 4 disjoint triangles** (verified for all checked vertices)
   - 12 = 4 × 3 matches D4 structure
   - Each triangle might correspond to one of four D4 'octahedra'

2. **D4 has 24 roots = eigenspace dimension for λ=2**
   - 24 = 3 × 8 (triality)
   - 24 = 4 × 6 (four octahedra)

3. **Connection to W(D4) = 192**:
   - |Aut(W33)| = 51840 = 192 × 270
   - 192 = |W(D4)| = Weyl group of D4
   - 270 = 27 × 10 (Albert × SO(10) vector)

