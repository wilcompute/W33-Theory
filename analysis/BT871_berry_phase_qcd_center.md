# BT871 — Where the Z₃ Actually Lives (A Berry-Phase Correction)

**Status: PROVEN (exact F₃ linear algebra, `analysis/bt871_berry_phase_qcd_center.py`, data `data/bt871_berry_phase_qcd_center.json`)**

Mined from W33_FOR_EVERYONE.tex §"Z₃ Berry phase as W(3,3) topological
invariant", which reads the per-triangle Z₃ phase as "a global Z₃
topological invariant, the structural origin of the Z₃ centre of SU(3)."
Tested rigorously, the *cohomological* reading is **corrected**, and the Z₃
is placed where it genuinely lives.

## What holds

- **T1 (confirmed):** every vertex lies on exactly 4 lines, and its 12
  neighbours partition into 4 disjoint triangles (the q+1 lines, λ=2
  structure) — the combinatorial backing of "four triangles meet at a
  vertex" is exact.
- **T2 (confirmed):** the F₃ homological dictionary is H₀ = 1, H₁ = 81
  (Steinberg), H₂ = 40 — matching the integral result (BT861/862), no
  3-torsion.

## What is corrected

- **T2′ (refutation):** the uniform Berry 2-cochain ω (value 1 on every
  triangle) is a **coboundary** — [ω] = 0 in H²(;F₃). Two independent
  proofs: ω pairs to 0 with every one of the 40 tetrahedron-boundary
  2-cycles (the alternating face sum 1−1+1−1 = 0), and δ¹f = ω is solvable
  over F₃ (rank 120 → 120). So the uniform Berry phase is **exact, not a
  topological obstruction**. The per-vertex "4 ≡ 1 (mod 3)" and global
  "40 ≡ 1 (mod 3)" are genuine arithmetic, but they are vertex/Euler-count
  statements mod 3, not an H² class.

## Where the Z₃ really is

- **T3 (correct placement):** the physical Z₃ — the three generations and
  the SU(3) centre — is the **order-3 group action on the Steinberg
  register H₁** (BT863: χ_St vanishes on every 3-singular class, forcing
  the 27+27+27 split). It is a representation-theoretic eigengrading, which
  is exactly why it is *trivial as a cochain* (no curvature 2-form carries
  it) yet *physically real as a symmetry* (it permutes the generation
  eigenspaces). The Z₃ is in the **G-action on cohomology**, not in the
  cohomology of a curvature class.

## Reading

The honest picture: W(3,3)'s 2-complex has no nonzero uniform Z₃ Berry
curvature — the "discrete second Chern class" reading does not survive exact
computation. The substrate's Z₃ structure is group-theoretic (the order-3
symmetry acting on Steinberg) rather than cohomological (a 2-cocycle). This
sharpens the generation story of BT863: generations are an *eigenvalue
degeneracy under a symmetry*, full stop — not a Berry-phase winding. The
correction is logged in the corpus ethos: a more-substrate-natural placement
(the Steinberg action) replaces a cohomological overclaim.

## Open

- Propagate the correction into W33_FOR_EVERYONE.tex §1840 (mark the Berry
  cochain as exact; the Z₃ is the order-3 Steinberg action).
- The genuine torsion question: is there *any* nonzero F₃ characteristic
  class on the substrate complex (H²(;F₃) is 40-dim — which of its classes,
  if any, is G-invariant)?
