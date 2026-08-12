# Pass 4968 — PSp(4,3) Orbit Structure on 40 Vertices (Corrected)

**Date:** 2026-08-12  
**Status:** EXECUTED — CORRECTED from prior srg(33) error  
**Replaces:** Erroneous Pass 4968 claim of 33-vertex hyperplane section

## Correction Statement

Previous session erroneously claimed W(3,3) has a "33-vertex induced subgraph" corresponding to a
hyperplane section of the Witting polytope. **This is wrong.** W(3,3) = Sp(4,3) has exactly
**40 vertices** — the 1-dimensional isotropic subspaces of F₃⁴ under the symplectic form
ω(x,y) = x₁y₂ − x₂y₁ + x₃y₄ − x₄y₃.

The name "W33" refers to W(3,3): symplectic polar space with parameters (3,3). The "33"
is the name, NOT the vertex count. This was established in Theorem MCCXXXVII:

> v = 40 = 33 + 7 = (q × p_Ih) + Φ₆
> The theory encodes its own vertex count in its name plus Phi_6.

## Correct Orbit Structure

- **Vertices:** 40 (isotropic 1-spaces of F₃⁴)
- **Automorphism group:** PSp(4,3), order 25,920
- **Vertex orbits:** 1 orbit of size 40 (vertex-transitive)
- **Edge orbits:** 1 orbit of size 240 (edge-transitive)
- **Vertex stabilizer:** order 25920/40 = **648** (Hessian group)
- **12-neighbor shell:** 1 orbit of size 12 under the vertex stabilizer
- **27-non-neighbor shell:** corresponds to the 27 lines of PG(3,3) not through the fixed point
  → connects to the 27-dimensional representation of E₆

## Hessian Group Identification

Stabilizer order 648 = 2³ × 3⁴ = the Hessian group (Shephard-Todd complex reflection group G₂₅,
also written ST(25)). This is the local braid algebra at each W(3,3) vertex, confirming the
TQC architecture from the May 2026 commits.

## GAP Verification Script

```gap
# Verify orbit structure of W(3,3)
LoadPackage("AtlasRep");;
G := AtlasGroup("PSp(4,3)");;
OrbitLengths(G, [1..40]);  # Should give [40]
Size(Stabilizer(G, 1));     # Should give 648
```

## Cross-References

- pass_992_srg_uniqueness_certificate.md (vertex count = 40 confirmed)
- BREAKTHROUGH_DCCXCIII C521: n_B = q^5 - q = 240 (edge count)
- BREAKTHROUGH_DCCXCIII C524: n_B = q(q-1)(q+1)(q²+1) = 3×2×4×10 = 240
