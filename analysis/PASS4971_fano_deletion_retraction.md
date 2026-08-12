# Pass 4971 — Fano Deletion Retraction

**Date:** 2026-08-12  
**Status:** RETRACTION of prior session's "Fano-G₂ Deletion Theorem"

## Retracted Claim

The previous session (Pass 4971 proposal) stated:

> **Theorem (Fano–G₂ Deletion):** Let Γ be the unique geometric srg(40,12,2,4).
> There exists a set F ⊂ V(Γ) of 7 vertices forming PG(2,2) such that
> Γ \ F ≅ srg(33,8,2,2).

**This theorem is FALSE.** The retraction is compelled by:

1. **W(3,3) has 40 vertices.** There is no strongly regular graph srg(33,8,2,2)
   arising as a deletion from W(3,3). A 33-vertex induced subgraph of W(3,3)
   exists combinatorially, but it is NOT strongly regular.

2. **BT1779_induced_subgraph_obstruction.md** (committed to this repo) formally
   documents that the 33-vertex induced subgraph of W(3,3) fails the SRG
   regularity conditions: vertices in the 33-subgraph inherit degrees between
   6 and 12 depending on how many of their original 12 neighbors fall among the
   deleted 7, violating the constant-degree requirement.

3. **The collinearity graph of GQ(3,3) IS W(3,3).** They are the same 40-vertex
   object. There is no separate srg(33,8,2,2) in this family.

## Correct Statement About the Fano-7

The Fano plane PG(2,2) embeds inside W(3,3) in the following precise sense:

- The 7 points of PG(2,2) correspond to the 7 isotropic points of a
  fixed totally isotropic plane π ⊂ PG(3,3) under the symplectic form.
- These 7 points form an **ovoid complement** in the 15-point symplectic
  polar space W(1,3) embedded as a subgeometry of W(3,3).
- The stabilizer of this Fano-7 in PSp(4,3) is isomorphic to PSL(2,7),
  order 168 = f × Φ₆ = 24 × 7 (Theorem MCCXXXVIII).

## Correct Physical Interpretation

The Fano-7 in W(3,3) is the kernel of the G₂ subalgebra action inside PSp(4,3),
not a set whose deletion produces a new SRG. The G₂ connection operates at the
level of the automorphism group structure, not vertex deletion.

## Status of Related Claims

| Claim | Status |
|-------|--------|
| srg(40,12,2,4) collinearity graph of GQ(3,3) | ✅ Correct |
| W(3,3) has 40 vertices | ✅ Correct |
| Fano-7 embeds as ovoid complement in W(1,3) ⊂ W(3,3) | ✅ Correct |
| Stab(Fano-7) ≅ PSL(2,7) | ✅ Correct |
| Deletion of Fano-7 gives srg(33,8,2,2) | ❌ RETRACTED |
| 33-vertex Witting hyperplane section | ❌ RETRACTED |
| W33 eigenvalues ±√6 | ❌ RETRACTED (correct: +2, −4) |

## Cross-References

- analysis/BT1779_induced_subgraph_obstruction.md
- passes/pass_992_srg_uniqueness_certificate.md
- BREAKTHROUGH_DCCXCIII Theorem MCCXXXVII
