# Cohomology of the Witting Non-Orthogonality 2-Complex

We treat the non-orthogonality graph on the 40 Witting rays as a 2-complex:
- **Vertices**: 40
- **Edges (non-orth pairs)**: 540
- **Triangles (non-orth triples)**: 3240

We compute cohomology over GF(2) and GF(3) using the standard coboundary maps
`d0: C^0 -> C^1` and `d1: C^1 -> C^2` with oriented edges/triangles.

## Results
```
GF(2): rank(d0)=39, rank(d1)=501
  H^0 dim = 1
  H^1 dim = 0
  H^2 dim = 2739

GF(3): rank(d0)=39, rank(d1)=501
  H^0 dim = 1
  H^1 dim = 0
  H^2 dim = 2739
```

## Interpretation
- **H^1 = 0** (over both GF(2) and GF(3)): every 1-cocycle is a coboundary. There are
  **no nontrivial edge-phase cohomology classes**.
- **H^2 is enormous** (dimension 2739): the triangle layer supports a vast space of
  independent 2-cocycles. This makes it unsurprising that the Pancharatnam triangle
  phases define a **nontrivial** class - they live in a very high-dimensional 2-cohomology.

This cleanly separates the hierarchy:
- Edge-level invariants are trivial (H^1 = 0)
- Triangle-level invariants are abundant (H^2 large)

Script: `tools/witting_triangle_cohomology.py`
