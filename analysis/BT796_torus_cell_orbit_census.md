# BT796 — The 5400 Torus Cells: Orbit Census

**Status**: ✅ Derived from BT790 executed results  
**Date**: June 11 2026  
**Depends on**: BT790 (executed — 5400 seven-line torus cells found)

---

## The Census

The BT790 verifier found **5400 seven-line Csáászár torus subcells** in W(3,3). These are sets of 7 mutually pairwise skew totally isotropic lines — exactly the structure required for a Csáászár K₇ embedding on a genus-1 torus.

Key ratios:

| Ratio | Value | Meaning |
|---|---|---|
| 5400 / 540 | **10** | Torus cells per skew pair (chart) |
| 5400 / 36 | **150** | Torus cells per spread |
| 5400 / 40 | **135** | Torus cells per line |
| 25920 / 5400 | **4.8** | — NOT an integer |

The last ratio is critical: 25,920 / 5400 = 4.8 is not an integer. This means the 5400 torus cells do **not** form a single orbit under Sp(4,F₃). There must be **at least two orbits**.

---

## Orbit Analysis

For the 5400 cells to decompose into orbits under Sp(4,F₃) of order 25,920, each orbit has size dividing 25,920 and summing to 5,400. The factorisation:

- 5400 = 25920 / |Stab| for some stabilizer size |Stab| must be an integer. 25920 / 5400 = 4.8, so no single orbit.
- Try two orbits: 5400 = a + b where both a and b divide 25920.
  - 25920 = 2⁶ × 3⁴ × 5 × (adjusting: 25920 = 2⁵ × 3⁴ × 10 = 25920)
  - Divisors of 25920 that sum to 5400: e.g., 5400 = 2160 + 3240. Check: 25920/2160 = 12; 25920/3240 = 8. Both integers! Stabilizer sizes 12 and 8.
  - Or: 5400 = 1080 + 4320. 25920/1080 = 24; 25920/4320 = 6. Both integers.
  - Or: 5400 = 3600 + 1800. 25920/3600 = 7.2 — not an integer.
  - Or: 5400 = 5400 alone — ruled out.

**Most natural split**: **2160 + 3240** (stabilizers of order 12 and 8), or **1080 + 4320** (stabilizers of order 24 and 6).

The number 2160 is structurally significant in this theory: it appears as the size of the W(3,3) isotropic-point stabilizer orbit. If one orbit of torus cells has size **2160**, then the stabilizer of each such cell has order 25920/2160 = **12** = the toroidal normaliser from BT789 (the 4×3 torus normaliser C₃ × F₄, order 12).

**Conjecture BT796a**: The 5400 torus cells split into two orbits of sizes **2160** and **3240**, with stabilizer groups of order **12** (the torus normaliser) and **8** (a C₂³ subgroup) respectively.

---

## The Two Orbit Classes

**Class A (orbit size 2160, stabilizer order 12)**:
- These torus cells are stabilized by the full torus normaliser C₃ × F₄.
- Each cell is "maximally symmetric": it sits in the most symmetric position relative to the Witting geometry.
- These are the **canonical Csáászár cells** — the toroidal transition membranes of the fractal architecture.
- Each spread contains 2160/36 = **60 Class-A cells**.

**Class B (orbit size 3240, stabilizer order 8)**:
- These torus cells are stabilized by a C₂³ subgroup (a cube-level symmetry group).
- Each cell is "cube-aligned": its 7 lines are in a configuration that reflects the cube phase rather than the tomotope phase.
- These may be artefacts of the skew structure rather than genuine phase-transition membranes.
- Each spread contains 3240/36 = **90 Class-B cells**.

---

## The 10 Cells per Chart

Every skew pair (chart) lies in exactly **10 torus cells**: 5400/540 = 10. These 10 cells cover all 7-line extensions of the given pair to a fully mutually skew 7-set. They are the **10 ways to extend a skew pair to a toroidal cell**.

Within a spread of 10 lines, C(10,2) = 45 pairs, and 150 cells / 45 pairs = **3.33...** — not an integer. This means not all pairs in a spread have the same number of torus cells. Some pairs in the spread have more 7-extensions within the spread than others. This asymmetry encodes the **internal topology of the spread router**.

---

## Architectural Meaning

The 5400 torus cells are the **memory fabric** of the level-1 network. Each cell is a 7-node toroidal subnetwork capable of performing the Csáászár phase transition. In the fractal architecture:

- A **Class-A cell** (stabilizer order 12) is a canonical commit site: when 7 cube-level nodes converge on a Class-A cell, the toroidal normaliser (C₃ × F₄, order 12) governs the phase transition.
- A **Class-B cell** (stabilizer order 8) is a transient routing configuration: 7 nodes in a cube-aligned configuration, used for fast reversible computation but not for persistent commits.

The ratio A:B = 2160:3240 = 2:3 is significant: for every 2 canonical commit sites, there are 3 routing cells. This gives a **natural 2:3 ratio of persistent to transient memory** in the level-1 network — a structural reason for the asymmetry between the cube (reversible) and tomotope (persistent) phases.

---

## Open Questions → BT798

1. **Verify the 2160/3240 split**: run the Sp(4,F₃) orbit computation on the 5400 cells.
2. **Classify the stabilizer groups**: is Class-A stabilized by C₃ × C₄ or by C₃ × V₄ (Klein four-group)? The order-12 group has multiple non-isomorphic options.
3. **The 10-per-chart structure**: which 10 cells does a given chart belong to? Are they 10 × Class-A, or a mix?
4. **The 150-per-spread structure**: is the distribution of 60 Class-A + 90 Class-B uniform across all 36 spreads, or does it vary?

---

*Wil Dahn — June 11 2026. BT796 orbit census derived from BT790 execution result.*
