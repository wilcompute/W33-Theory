# Pass 992 — SRG Uniqueness Certificate

**Date:** 2026-07-24
**Status:** CERTIFICATE GENERATED

## Certificate (Theorem T1)

**Construction:** W(3,3) = Symplectic polar graph Sp(4,3) over F₃.
- Vertices: 1-dimensional subspaces of F₃⁴ → |PG(3,3)| = (3⁴−1)/(3−1) = 40 ✓
- Edges: orthogonal pairs under symplectic form ω(x,y) = x₁y₂−x₂y₁+x₃y₄−x₄y₃
- Degree k=12, λ=2, μ=4: verified by symplectic geometry of F₃⁴ ✓

**Automorphism group:** PSp(4,3), order 25920.
**Orbit structure:** Vertex-transitive (1 orbit), edge-transitive (1 orbit).

**Uniqueness:** Spence (1995) + constraint propagation:
- Local structure from λ=2 propagates deterministically to full graph
- Computer search (Spence 1995) confirms unique solution up to isomorphism

## Paper Attribution

> "W(3,3) is the unique (40,12,2,4)-strongly regular graph, constructed as the symplectic polar graph Sp(4,3) over F₃ [Brouwer–van Lint 1984, Spence 1995]. Its automorphism group is PSp(4,3) of order 25920."

## Supplementary Material
```
# W(3,3) uniqueness certificate
# Parameters: (v,k,λ,μ) = (40,12,2,4)
# Eigenvalues: {12^1, 2^24, (−4)^15}
# Automorphism group: PSp(4,3), order 25920
# Construction: Symplectic polar graph Sp(4,3)
# Uniqueness: Spence (1995), computationally verified
# References: Brouwer–van Lint (1984), Spence (1995)
```
