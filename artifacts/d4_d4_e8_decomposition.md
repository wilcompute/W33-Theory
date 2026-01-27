# D4×D4 Decomposition Approach to E8 Correspondence

## Root System Comparison

| System | Roots | Dimension |
|--------|-------|-----------|
| D4 | 24 | 4 |
| E8 | 240 | 8 |
| D4×D4 | 576 = 576 | 8 |

### D4 Root Adjacency (|inner product| = 1)

- Degree: 16
- Edges: 192

### E8 Root Types

- Type 1 (D8 roots): 112
- Type 2 (half-spinor): 128
- Total: 240

### Key Number Comparisons

| E8 Structure | Count | W33 Structure | Count |
|--------------|-------|---------------|-------|
| Type 1 roots | 112 | ? | - |
| Type 2 roots | 128 | ? | - |
| Total roots | 240 | Triangle graph edges | 240 |
| Root lines (±pairs) | 120 | Line graph nullspace | 120 |

## Triangle Graph Edge Structure

- Total edges: 240

### Edge Distribution by Position Pair

- Triangles (0, 1): 40 edges
- Triangles (0, 2): 40 edges
- Triangles (0, 3): 40 edges
- Triangles (1, 2): 40 edges
- Triangles (1, 3): 40 edges
- Triangles (2, 3): 40 edges

Total: 6 position pairs × 40 bases = 240 edges ✓

## Splitting 240 = 112 + 128?

E8 splits as 112 (type 1) + 128 (type 2).
Can the 240 triangle edges be similarly partitioned?

### Option 1: By position pair
- 6 groups of 40 each
- No obvious 112+128 split

### Option 2: By base vertex type

W33 vertices by coordinate structure (# non-zero coords):
- 1 non-zero: 4 vertices
- 2 non-zero: 12 vertices
- 3 non-zero: 16 vertices
- 4 non-zero: 8 vertices

### Option 3: By triangle intersection pattern

For base vertex 0, the 4 triangles are:
  T0: (1, 2, 3) - edges to H27: 27
  T1: (13, 14, 15) - edges to H27: 27
  T2: (16, 17, 18) - edges to H27: 27
  T3: (19, 20, 21) - edges to H27: 27

## D4 Triality and 4-Triangle Labeling

D4 has triality: its 3 fundamental 8-dim representations
(vector, spinor+, spinor-) are permuted by an order-3 automorphism.

Question: Do the 4 triangles of H12 correspond to D4 nodes?

D4 Dynkin diagram:
```
    T1
    |
T0--T2--T3
```
Or equivalently (star shape):
```
  T1
  |
  T0
 / \
T2  T3
```

### Connection to W33 Spectrum

W33 eigenvalue structure:
- λ = 12: multiplicity 1
- λ = 2: multiplicity **24** (= D4 root count!)
- λ = -4: multiplicity 15

The 24 eigenvectors with eigenvalue 2 may correspond to D4 roots!

Confirmed W33 spectrum:
- λ = 12.0: multiplicity 1
- λ = 2.0: multiplicity 24
- λ = -4.0: multiplicity 15

## Alternative: 120 and the Nullspace

Both the triangle line graph L(T) and E8 root graph have
eigenvalue 0 with multiplicity 120.

120 = E8 root lines (±pairs)
120 = 240/2

This shared dimension might indicate a deeper connection
at the level of root LINES rather than individual roots.

### Involution on Triangle Edges

Is there a natural pairing of the 240 triangle edges into 120 pairs?

Position pair complement structure:
- (0,1) ↔ (2,3): both have 40 edges
- (0,2) ↔ (1,3): both have 40 edges
- (0,3) ↔ (1,2): both have 40 edges

This gives 3 pairs of position pairs, total 120 + 120 = 240.
Could map to 120 E8 root lines!

## Summary and Hypothesis

### Structural Parallels

| W33 | Count | E8 | Count |
|-----|-------|-----|-------|
| Vertices | 40 | ? | - |
| H12 triangles | 4 per vertex | D4 nodes | 4 |
| Total triangles | 160 | ? | - |
| Triangle edges | 240 | Roots | 240 |
| Eigenvalue-2 mult | 24 | D4 roots | 24 |
| Position pair groups | 6 × 40 | ? | - |
| Nullspace dim (L(T)) | 120 | Root lines | 120 |

### Hypothesis

The correspondence might be:

1. **D4 level**: 24 W33 eigenvectors (λ=2) ↔ 24 D4 roots

2. **E8 level**: 240 triangle edges ↔ 240 E8 roots
   - Not via graph isomorphism (different degrees)
   - Possibly via shared combinatorial structure

3. **Line level**: 120 position-pair orbits ↔ 120 E8 root lines
   - Each base vertex contributes 6 edges
   - 40 bases × 6 = 240
   - Position pairs naturally group into 3 complementary pairs

### Open Questions

1. Can we explicitly construct a bijection 240 edges ↔ 240 E8 roots?
2. What structure is preserved under such a bijection?
3. How does the D4 triality act on the 4 triangles?
4. Is the 112+128 split reflected in the triangle edges?

