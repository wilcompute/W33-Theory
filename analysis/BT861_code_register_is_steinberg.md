# BT861 — The Code Register IS the Steinberg Module

**Status: PROVEN (complete character computation over all 25920 group elements, `analysis/bt861_code_register_is_steinberg.py`, data `data/bt861_code_register_is_steinberg.json`)**

The single-photon paper's CSS code [[240, 81, 4, 3]]₃ stores its 81 logical
qutrits in H₁ of the W(3,3) 2-complex (40 vertices, 240 edges, 160 triangles
— all triangles live inside the 40 line-K₄s). The holonet's protected memory
is the Steinberg module — the **unique** 81-dimensional irreducible of U₄(2)
(BT742). BT861 proves they are the same object.

## The proof (exhaustive, exact)

- **T1**: rank(∂₀) = 39, rank(∂₁) = 120, so dim H₁ = 240 − 39 − 120 = **81**
  (and dim H₂ = 40).
- **T2**: the character of PSp(4,3) on H₁⊗C, computed exactly for **all
  25920 elements** (signed-permutation trace against the H₁ projector),
  has norm ⟨χ, χ⟩ = **1.000** — H₁ is **irreducible**. Since U₄(2) has
  exactly one 81-dimensional irreducible, **H₁ is the Steinberg module**.
- **T3**: cross-check — for every group element,
  χ_H₁(g) = #fixflags − #fixpoints − #fixlines + 1, the **Solomon–Tits
  alternating sum** over the rank-2 building (chambers − both vertex types
  + 1). Identity check: 160 − 40 − 40 + 1 = 81 ✓. (Refutation en route: the
  shorthand "fixflags − fixpoints + 1" remembered from BT742-era notes is
  wrong — both vertex types must be subtracted.)

## Consequence: one 81, one protection mechanism

> **The QECC logical space and the holonet's Schur-protected register are
> the same PSp-representation.** Any equivariant operator on the code's
> logical space is a scalar (Schur's lemma): symmetry-protection extends
> from the abstract Steinberg memory to the concrete [[240,81,4,3]]₃ code.
> The code's logical errors that commute with the substrate symmetry are
> trivial — only symmetry-breaking noise can corrupt the register, and the
> sentinel/clock layers are precisely the symmetry monitors.

This also retroactively explains the single-photon paper's observation that
the "matter sector" H₁ = 81 = q⁴ equals the mode-space threshold and the
two-photon GHZ dimension: all of these are the same Steinberg 81.

## Open

- H₂ (dim 40) as a PSp-module: irreducible? Which 40-dim object (points
  rep? lines rep? reflection rep ⊕ ...)? One more character sweep.
- The three-generation split 81 = 27+27+27 (single-photon paper §
  generations) inside the Steinberg module: identify the order-3
  automorphism's eigenspace structure representation-theoretically.
