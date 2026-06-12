# BT863 — Three Generations From Steinberg Vanishing

**Status: PROVEN (exhaustive over all 25920 elements, `analysis/bt863_generations_from_steinberg_vanishing.py`, data `data/bt863_generations_steinberg_vanishing.json`)**

With BT861 (matter register = Steinberg), the classic question "why three
fermion generations?" gets its sharpest substrate answer: **the split is
representation-theoretically forced.**

## The theorems

1. **Vanishing (verified exhaustively):** χ_St(g) = 0 **iff** 3 | ord(g),
   for every one of the 25920 group elements — the classical p-singular
   vanishing of the Steinberg character, machine-checked in our model.
2. **Three generations (corollary):** for *any* order-3 symmetry σ, the
   eigenspace multiplicities of σ on the 81-dim matter register are
   m_j = (χ(1) + χ(σ) + χ(σ²))/3 = (81 + 0 + 0)/3 = **27 each**. The
   single-photon paper's generation split 81 = 27+27+27 holds for *every*
   choice of σ — no triality element is privileged; the generations are
   kinematic, not dynamical.
3. **Sub-generations:** every order-9 element (5760 of them) splits the
   register into **nine 9-dimensional eigenspaces** — generations carry
   exactly q² sub-generations under the deeper cyclic symmetries.
4. **Mod-3 survival:** in the code's defining characteristic,
   rank₃(∂₀) = 39 and rank₃(∂₁) = 120 (no rank drop), so
   dim H₁(F₃) = 81 and the **[[240, 81, 4, 3]]₃ parameters survive** —
   UCT-consistent with the torsion-free integral homology.

## Reading

The chain is now: master equation → q = 3 → W(3,3) → 2-complex → H₁ =
Steinberg (BT861) → χ_St vanishes on 3-singular classes → **any** ternary
symmetry of the substrate organizes matter into exactly three equal
generations of dimension 27 = q^q, each refining into three 9-dim
sub-blocks under order-9 symmetries. The number of generations is not an
input, a vacuum choice, or a fit — it is the defining-characteristic
degeneracy of the protected register.

## Open

- The physical generation map: which order-3 class (there are several) is
  the physical triality, and do the CKM/PMNS textures (Pillar 68's exact
  grading theorem) distinguish it?
- Order-6 and order-12 elements: mixed eigenvalue structure (χ ≠ 0 on the
  2-part) — the "generation + chirality" joint grading.
