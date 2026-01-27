# Triangle Graph ↔ E8 Correspondence Investigation

**Key Observation**: The W33 triangle co-occurrence graph has 240 edges,
the same as the number of E8 roots!

## W33 Triangle Structure

- Unique triangles: 160

## Triangle Co-occurrence Graph

- Vertices: 160
- **Edges: 240** (= E8 root count!)
- Degree: 3

### Triangle Graph Spectrum

- λ = 3.0: multiplicity 40
- λ = -1.0: multiplicity 120

## E8 Root System

- Roots: 240

### E8 Root Adjacency (|inner product| = 1)

- Degree: 112
- Edges: 13440

## The 240 = 240 Connection

| Object | Count |
|--------|-------|
| Triangle graph edges | 240 |
| E8 roots | 240 |

**EXACT MATCH!**

This suggests a potential bijection:
- Triangle graph edges ↔ E8 roots

## Line Graph Analysis

The line graph L(T) of the triangle graph T has:
- Vertices = edges of T = 240
- Edges = pairs of T-edges sharing a T-vertex

### Line Graph L(T) Properties

- Vertices: 240
- Edges: 480
- Degree: 4

### Comparison with E8

| Property | L(T) | E8 root graph |
|----------|------|---------------|
| Vertices | 240 | 240 |
| Degree | 4 | 112 |
| Edges | 480 | 13440 |

Degree mismatch: L(T) has degree [np.int64(4)], E8 has degree 112

### Line Graph Spectrum

- λ = 4.0: multiplicity 40
- λ = -0.0: multiplicity 120
- λ = -2.0: multiplicity 80

### E8 Root Graph Spectrum

- λ = 112.0: multiplicity 1
- λ = 16.0: multiplicity 35
- λ = -0.0: multiplicity 120
- λ = -8.0: multiplicity 84

Spectra do not match exactly.

## Alternative: E8 Root Lines

E8 has 120 root lines (±pairs). Compare to 160 triangles.

- E8 root lines: 120
- W33 triangles: 160

## Summary

| W33 Structure | Count | E8 Structure | Count |
|---------------|-------|--------------|-------|
| Triangles | 160 | Root lines | 120 |
| Triangle graph edges | 240 | Roots | 240 |
| L(T) vertices | 240 | Roots | 240 |

