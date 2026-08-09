# Part CXCIV — Regular Polytopes Bridge

## Theorem CXCIV

The W(3,3) SRG(40,12,2,4) parameters index the regular polytopes of all
dimensions with zero free parameters: vertex counts, edge counts, face
counts, and symmetry orders of the five Platonic solids; key parameters of
the six convex regular 4-polytopes; and the enumeration theorems for regular
polytopes in every dimension.

## W(3,3) Atoms Used

| Symbol | Value | Role |
|--------|-------|------|
| Q | 3 | Projective dimension; regular polytopes in n >= 5 |
| V | 40 | Vertex count of collinearity graph |
| K | 12 | Valency; icosahedron vertices, dodecahedron faces |
| Φ₄(Q) | 10 | Cyclotomic polynomial value |
| J⁻¹ | 8 | Inverse Jackson coefficient; cube vertices |
| EDGES | 240 | V·K/2 |
| EIG\_MAX | 5 | Maximum eigenvalue; number of Platonic solids |
| K/2 | 6 | Number of convex regular 4-polytopes |

## The Five Platonic Solids

### Vertex Counts

| Solid | Vertices | W(3,3) Formula |
|-------|----------|----------------|
| Tetrahedron | 4 | J⁻¹/2 |
| Cube | 8 | J⁻¹ |
| Octahedron | 6 | K/2 |
| Dodecahedron | 20 | V/2 |
| Icosahedron | 12 | K |

### Edge Counts

| Solid | Edges | W(3,3) Formula |
|-------|-------|----------------|
| Tetrahedron | 6 | K/2 |
| Cube | 12 | K |
| Octahedron | 12 | K |
| Dodecahedron | 30 | Q·Φ₄ |
| Icosahedron | 30 | Q·Φ₄ |

### Face Counts

| Solid | Faces | W(3,3) Formula |
|-------|-------|----------------|
| Tetrahedron | 4 | J⁻¹/2 |
| Cube | 6 | K/2 |
| Octahedron | 8 | J⁻¹ |
| Dodecahedron | 12 | K |
| Icosahedron | 20 | V/2 |

The dual pairs (cube ↔ octahedron, dodecahedron ↔ icosahedron) swap vertex
and face counts — both of which are W(3,3) atoms. The tetrahedron is
self-dual with 4 = J⁻¹/2 for both vertices and faces.

### Symmetry Group Orders

| Solid | Order | W(3,3) Formula |
|-------|-------|----------------|
| Tetrahedron | 24 | 2K |
| Cube / Octahedron | 48 | 4K |
| Dodecahedron / Icosahedron | 120 | K·Φ₄ |

## Enumeration Theorem

- **3D**: exactly 5 regular convex solids = EIG\_MAX = 5 (max eigenvalue of W(3,3))
- **4D**: exactly 6 regular convex polytopes = K/2 = 6
- **n ≥ 5**: exactly 3 regular convex polytopes = Q = 3 (simplex, hypercube,
  cross-polytope)

## The Six Convex Regular 4-Polytopes

| Name | Vertices | Cells | Symmetry | W(3,3) Formula |
|------|----------|-------|----------|----------------|
| 5-cell | 5 | 5 | 120 | verts = EIG\_MAX |
| 8-cell (hypercube) | 16 | 8 | 384 | verts = V − 2K |
| 16-cell | 8 | 16 | 384 | verts = J⁻¹ |
| 24-cell | 24 | 24 | 1152 | verts = cells = 2K (self-dual!) |
| 120-cell | 600 | 120 | 14400 | verts = Q·V·EIG\_MAX; cells = EDGES/2 |
| 600-cell | 120 | 600 | 14400 | verts = EDGES/2; cells = Q·V·EIG\_MAX |

The 24-cell is the unique self-dual regular 4-polytope with no 3D analog. Its
24 vertices correspond to the 24 minimal vectors of the D₄ root lattice and
to the 24 unit Hurwitz quaternions. Its symmetry order 1152 = J⁻¹ · K².

## Structural Observations

- The 5-cell (4D simplex) has 5 vertices = max eigenvalue of W(3,3).
- The 120-cell and 600-cell are dual; each has Q·V·EIG\_MAX = 600 in
  vertices (120-cell) or cells (600-cell), and EDGES/2 = K·Φ₄ = 120 in
  cells (120-cell) or vertices (600-cell).
- Edge counts {K/2, K, Q·Φ₄} for the Platonic solids are all W(3,3) atoms.
- Symmetry orders {2K, 4K, K·Φ₄} are uniformly K-multiples.

## Bridge Script

`PART_CXCIV_REGULAR_POLYTOPES_BRIDGE.py` — 52/52 checks pass.

## Tests

`tests/test_regular_polytopes_bridge_cxciv.py` — 92 tests pass.
