# Pass 12675: the F₈ regulus minimum lives on the 27 lines of a cubic surface — the torus is a regular element of type E₆(a₁) in W(E₆) acting on E₆/2E₆, and the nine bases are a σ-orbit of tritangent planes; three stabiliser types; local rigidity

Claude track. Follows Pass 12674. **Not a theory of everything.** This is a statement about a finite geometry, not a physical claim.

## 1. The bridge (`w33_f8_torus_is_E6a1.py`)

On the 8-dimensional code space of T (Pass 12671), the nine F₈-regulus MUBs reduce to nine three-qubit stabiliser bases, i.e. nine Lagrangians L_t of V = T^⊥/T = F₂⁶. They are cycled by the unique symplectic map σ of order 9 with σ⁶ + σ³ + 1 = 0 (Pass 12672). New here, all checked by exhaustive finite computation:

1. **σ preserves exactly one of the 64 quadratic forms** that polarise to the symplectic form, and that form Q is **elliptic**: 27 singular non-zero points and 36 nonsingular. So (V, Q) ≅ E₆/2E₆ (27 + 36 = 63; the repository already certifies E₆/2E₆ = [1, 27, 36]). σ lies in O⁻(6,2) ≅ W(E₆), and its characteristic polynomial Φ₉ is that of the **regular class E₆(a₁)** of W(E₆) on the reflection representation (Carter's classification).
2. **Each of the nine bases contains exactly three singular points, and they sum to zero.** They are the three lines of a **tritangent plane**. E₆/2E₆ has exactly 45 such triples, the classical 45 tritangent planes.
3. σ acts on the 45 tritangent planes with orbits of sizes 3, 3, 3, 9, 9, 9, 9. **The nine bases are exactly one of the four 9-orbits.**
4. **The coset weights (Pass 12672) are incidence counts.** The weight of a point is the number of the nine bases containing it. The 27 lines fall into three σ-orbits of 9 lines, with weights exactly **0, 1 and 2**. Among the 36 double-sixes (nonsingular points), the weights are 3 (9), 1 (9) and 0 (18).

> **Statement.** On its code space, the minimum c₈ = (47 − 32cos 2π/9)/9 of the nine F₈-regulus MUBs is a problem about nine tritangent planes of a cubic surface, forming one orbit of an order-9 element of type E₆(a₁) in W(E₆) acting on E₆/2E₆. The minimiser is an eigenstate of a Clifford lift of that element (Pass 12672 §1b; exact eigenvalue formula, Pass 12673).

**Why this matters for the repository.** W(E₆) ≅ O⁻(6,2) ≅ PSp(4,3):2 is the symmetry group of the two-qutrit symplectic geometry W(3,3) that the whole W33 programme is built on. The 27 lines and 45 tritangent planes appear throughout its corpus (353 analysis files mention tritangents). Until now the six-qubit F₈ regulus constant was an isolated quantum-information result. It now sits in that same E₆ geometry: cos(2π/9) enters through the order-9 E₆(a₁) element, whose eigenvalues on the reflection representation are the primitive 9th roots of unity.

**Prior art.** "E₆(a₁)" occurs nowhere in the corpus. The files that mention both "regulus" and "tritangent" use "regulus" for depth-3 isotropic reguli in W33 (e.g. `2026-09-01_regulus_e8_completion_bridge.md`), a different object. The other track's F₈ files today (purity law, rational witness, PPT) do not use E₆/2E₆. That W(E₆) ≅ O⁻(6,2), that E₆/2E₆ carries 27 + 36 points, and that E₆(a₁) is regular with characteristic polynomial Φ₉ are classical facts. The identification of the F₈ code-space configuration with them is new here.

**Not claimed.** No physical consequence is derived. Whether the other σ-orbits of tritangent planes (three more 9-orbits, three 3-orbits) correspond to other MUB-type configurations, and whether this explains why q = 8 alone has a non-stabiliser optimum, is open.

## 2. Three types of order-4 stabiliser (`w33_f8_stabiliser_types.py`)

The type of an order-4 group is given by the covered-weight histogram of its cosets in S′^⊥.

| type | weights | where it occurs | degree-6 SOS on its 16-dim code space |
|---|---|---|---|
| A | {1: 63, 2: 36} | 9 of 16 generic global minimisers (Pass 12674); Pass 12660's S | 2.0818 (= other track's PPT dual) |
| B | {1: 99, 2: 18} | 7 of 16 generic global minimisers | 2.4729 |
| C | {1: 54, 2: 27, 3: 9} | never a generic minimiser's stabiliser | **2.4967** (= T code-space value) |

- T's seven order-4 subgroups are **1 of type A, 5 of type B and 1 of type C**.
- A type-B stabiliser attains c₈ for all four sign choices. **6 of its 510** rank-3 extensions attain c₈ (56 for type A).
- Each such extension again splits into 1 A + 5 B + 1 C, and its effective model is T's: weights {1: 18, 2: 9, 3: 9} and degree-6 bound 2.4966773.
- The effective minimum on type C is c₈ (2.4985086471), not lower.

## 3. Local rigidity (`w33_f8_local_rigidity.py`)

The test compares the Hessian null space in C⁶⁴ (128 real dimensions) with its null space restricted to the code space, at minimisers inside each 16-dimensional code space.
- **Generic points on types A and B** (null dimension 3 in both): every flat direction is tangent to the code space, so nearby minimisers stay on it. One type-B sample had a near-zero eigenvalue (10⁻⁶ relative) and is borderline.
- **Points isolated within their code space** (null 2 in the code space, 4 in C⁶⁴; both type-C samples and two of the four type-A samples): two flat directions leave the code space. These are where families from different code spaces cross, consistent with the T points lying in one A, five B and one C space at once.

So the minimum set looks like one-parameter families inside type-A and type-B code spaces, meeting at the torus eigenstates. This is numerical, with no negative directions at any sample.

## 4. q = 32: four classes

The equal-trace torus eigenspace minimum is **12.48962077 for 4 of the 10 trace classes** (traces 29, 20, 25, 22), all identical, consistent with Pass 12672. The 40-digit identification run is in progress (addendum).

## 5. Degree 8 on 16-dimensional code spaces: not attempted

With the Pauli group alone the problem has about 2×10⁶ pair variables and about 10⁸ nonzeros. No monomial (permutation) symmetry exists in the effective coordinates used (checked over GL(4,2) for types A, B and T). A useful reduction would need a basis adapted to the configuration, for example via the E₆(a₁) / tritangent structure of §1. That is now the natural route.

## Addendum A: trinification tested and rejected; the line orbits are trihedra

Motivation: the 27 lines are the mod-2 shadow of the 27 of E₆. Under trinification SU(3)³ ⊂ E₆ the 27 splits as 9 + 9 + 9, which in cubic-surface terms is three Steiner trihedral pairs. The 40 such triples correspond to the 40 points of W(3,3).
- **Test.** Two distinct lines meet iff B(p,q) = 0; every line meets 10 lines, as it must.
- **Result: negative.** Inside each σ-orbit of 9 lines, the meet graph is 4-regular with exactly **3** triangles, all tritangent planes and pairwise disjoint. A Steiner trihedral pair (3×3 grid) would have 6.
- So each σ-orbit of lines is a **trihedron**: three disjoint tritangent planes covering its nine lines. These should be the three σ-orbits of size 3 on the 45 planes (the planes fixed by σ³). A line meets 4 lines of its own orbit and 3 of each other orbit.
- The F₈ minimiser therefore does not select a trinification (a W(3,3) point) in this way. The three orbits of lines are distinguished by their weights 0, 1, 2 relative to the nine chosen planes.
