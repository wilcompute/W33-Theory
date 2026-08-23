# Passes 9173–9184 — Rank-24 W(3,3) Root-Shadow Trichotomy

## Status

**Machine-verified.** Canonical executable witness:
`analysis/w33_pass9173_9184_root_shadow_trichotomy.py`.
Frozen result:
`data/PART_W33_PASS9173_9184_ROOT_SHADOW_TRICHOTOMY.json`.

This is the collision-free rehome of the theorem first developed under the superseded 9029–9040 label. The mathematics is unchanged.

## The theorem

Starting from the exhaustive Pass 8989–9012 result that exactly three rank-24 Niemeier lattices carry the required pure `Phi_9^4` order-nine action producing a nondegenerate alternating quotient `L/(I-X)L ~= F_3^4`, the verifier projects **every root** to the projective W(3,3) quotient.

| carrier | roots | quotient-zero roots | visible W33 points | roots / visible point | visible support |
|---|---:|---:|---:|---:|---|
| `E8^3` | 720 | 0 | 40 | 18 | all W(3,3) |
| `E6^4` | 288 | 72 | 4 | 54 | one W33 line |
| `A2^12` | 72 | 0 | 4 | 18 | one W33 line |

For the four-point supports, the verifier checks rank two over `F_3` and pairwise symplectic orthogonality, so the support is exactly one generalized-quadrangle line.

For `E8^3`, each individual E8 factor already hits all 40 W33 points with six roots per point. The three-factor lift therefore triples the fibre to 18 and recovers the earlier E8-to-W33 Eisenstein six-to-one fibration inside the rank-24 carrier.

## New cross-carrier bridge

Each E6 component contributes 18 quotient-zero roots and 54 roots over one visible W33 point. The 18 zero roots are reflection-closed and split into three orthogonal six-root components, hence `A2^3`. Across four E6 factors:

`4 A2^3 = A2^12`.

Therefore

`kernel_roots(E6^4 -> W33) = A2^12`

as a **root-system type**. This is not an identification of the full Niemeier lattice `N(A2^12)` with a sublattice of `N(E6^4)`.

After identifying opposite roots, the visible fibres contain 9 root pairs per point for `E8^3`, 27 for `E6^4`, and 9 for `A2^12`.

## Reproducibility upgrade for A2^12

The executable rebuilds the extended ternary Golay `[12,6,6]_3` code, its 729 words and exact weight enumerator, constructs the index-729 Golay-glued Niemeier lattice, checks the explicit signed `3^4` monomial automorphism, inserts one A2 Coxeter twist per component 3-cycle, and verifies `X^9=I`, `Phi_9(X)=0`, `det(I-X)=81`, `F+F^T=3G`, and quotient rank four.

## Evidence boundary

This is a finite lattice/symplectic-quotient theorem. The phrase “different UV decorations of the same IR quotient” is at most an analogy. No continuum, Standard-Model, mass-spectrum, or dynamical claim follows from this result.
