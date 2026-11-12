# The closed grand-spin-zero sector of the W33 hedgehog

The canonical color-invariant hedgehog closes a grand-spin-zero fermion sector with 130 Weyl isodoublets. Its regular origin condition is independent of the heavy mass phases. The winding adjoint sectors each have one light channel per radial direction and three heavy channels. The winding triplet sector has four light channels and 45 heavy channels per direction. These dimensions sharpen the smooth-core scattering test and invalidate a strict-contraction shortcut on the full heavy space. [Canonical radial core](2026-11-11_monopole_neutral_core.md) · [Exterior mass winding](2026-11-13_monopole_heavy_phase_flow.md)

## Angular closure

The monopole step and its coroot generate an embedded SU(2). The matter VEV plane is annihilated by it. The six real adjoint singlets of the color-invariant radial ansatz commute with it. The remaining adjoint triplet and magnetic gauge profile are in hedgehog form, so simultaneous spatial and embedded gauge rotations preserve this background. A gauge-invariant quadratic fermion operator on it commutes with grand spin, the sum of orbital, spin and embedded isospin angular momenta. Multiplying the superpotential terms by constant phases preserves this equivariance. The result applies to the stated hedgehog background and its radial variations.

The exact weight counts give six doublets and 15 singlets on the 27. The 78 has 20 doublets, 35 singlets and one triplet. Since orbital angular momentum is integral and spin is one half, grand spin zero can use only half-integral isospin. The only such isospin here is one half. The five bifundamental matter species contribute 90 doublets, the internal adjoint chiral multiplet contributes 20, and the internal gaugino contributes 20. The family gaugino and conjugate decuplet are embedded-isospin singlets. Each of the 130 Weyl doublets contributes two radial coefficients, corresponding to the L=0 and L=1 tensors. [Grand-spin modes of smooth monopoles](https://arxiv.org/abs/2309.00680)

## Radial differential operator and regular origin

Write the spin–isospin singlet as S and use the angular basis `S, σ·rhat S`. Write a left Weyl doublet as `[u(r) S+v(r) σ·rhat S]/r`. In the convention `D=∂−igA` and `g A_i^a=(1−K) ε_aij rhat_j/r`, the grand-spin-zero kinetic operator is

```text
−i [ 0             d/dr + K/r ]
   [ d/dr − K/r    0          ].
```

The free angular derivative gives the terms ±1/r. The exact Pauli contraction on the two angular tensors changes them to ±K/r. To write a covariant mass map, identify conjugate isodoublets by their invariant epsilon tensor and read its north-pole matrices M₊ and M₋ on the two coroot weights. Its singlet and triplet parts are `M0=(M₊+M₋)/2` and `M1=(M₊−M₋)/2`. Equivariance extends the map to `M0⊗I+M1⊗τ·rhat`; on the angular basis this is `M0⊗I−M1⊗σ1`. This gives the angular reduction for the chiral Hessian and gauge-induced mass maps. Their full radial coefficient matrices have yet to be evaluated on the numerical core.

At a smooth origin `K=1+O(r²)` and the mass terms are bounded. The leading radial equations have powers +1 in u and −1 in v. The latter branch is excluded by the radial square norm. The regular branch has `u=r a+O(r²)` and `v=O(r²)`. For example, the regular equation for v gives `(rv)'=O(r u,r v)` and has zero integration constant. This leading regular subspace is independent of a bounded mass phase, also after adjoining the charge-conjugate equations. In the basis diagonalizing the radial flux, v=0 gives a fixed unitary graph. Thus finite-radius flux-preserving transfer gives zero determinant winding for the full regular boundary relation on this sector. [Finite-radius boundary transport](2026-11-13_monopole_heavy_phase_flow.md)

## Charge blocks and the matching criterion

In the Cartan chart `(color1,color2,2T3,6Y)`, the monopole step has weight `α=(0,1,−1,−5)`. A fermion weight w with coroot pairing n=±1 carries doubled perpendicular weight `2w−nα`. Both isospin components have the same perpendicular weight. The exact ledger has 14 such weights and equal UV multiplicities on the two coroot signs. A fixed-charge radial system pairs a block with the charge conjugates of its opposite block. Charge conjugation flips both the weight and the Weyl chirality, so it preserves the radial propagation direction of the corresponding conjugate mode.

| Winding sector | Paired Weyl doublets | Light per direction | Heavy per direction | Winding multiplicity |
| --- | ---: | ---: | ---: | ---: |
| Adjoint color partner, each of two weights | 4 | 1 | 3 | 1 |
| Adjoint weak weight | 4 | 1 | 3 | 1 |
| Triplet | 49 | 4 | 45 | 3 |

For a unitary boundary relation U with h heavy and ℓ light channels per direction, `I−U_hh†U_hh=U_ℓh†U_ℓh` has rank at most ℓ. When h>ℓ at least h−ℓ singular values of the heavy compression are exactly one. The full adjoint blocks therefore have at least two such singular values, and the triplet block has at least 41. This dimension bound leaves the eigenvalues of the product with the decaying exterior graph open.

At matching radius the useful condition is `det(A−U_hh)≠0` for every phase, where A is the unitary decaying exterior graph in the heavy sector. Under this condition, the earlier reflection-winding formula extends to norm-one compression. Scale `U_hh` by s∈[0,1]. For s<1 the two Schur determinant factors are nonsingular by strict contraction, and at s=1 they are nonsingular by the assumed condition and conjugacy. Their winding is therefore zero. With the regular-core graph winding zero, the reflection winding equals the heavy mass winding whenever the condition holds. Evaluating the full radial mass matrices and checking this determinant, or tracking its zeros if present, remains necessary for the smooth-core scattering prediction.

## A finite test for heavy modes that cannot reach the light channels

Set `B=A†U_hh` and `C=U_ℓh` at the same phase. Then `B†B+C†C=I`. The matching condition fails exactly when B has eigenvalue 1. Such an eigenvector necessarily has Cx=0 by flux conservation. For h heavy channels, define

```text
G = sum from k=0 to h−1 of (C B^k)†(C B^k)
  = I − (B^h)†B^h.
```

The second equality telescopes. The kernel of G is B-invariant by Cayley–Hamilton, and B is isometric on it since C vanishes there. Thus the restriction of B to this kernel is unitary. It contains every eigenvector of B with unit-modulus eigenvalue. A complete pointwise test can therefore restrict the eigenvalue-1 check to the kernel of G. A positive definite G suffices to exclude a resonance and allows the one-step compression to have norm one. This is the observability test of a finite unitary input-output system applied to the monopole matching problem. [Characteristic functions of operator colligations](https://arxiv.org/abs/2312.17333)

For a quantitative certificate, if `G ≥ γI` with γ>0 then `σ_min(I−B) ≥ (1−sqrt(1−γ))/h`. Indeed, `||B^h||≤sqrt(1−γ)` and `I−B^h=(I+B+⋯+B^(h−1))(I−B)`, with the sum of powers of norm at most h. The same lower bound applies to `A−U_hh=A(I−B)`. A uniform bound in the heavy phase would certify the entire loop. The bound concerns the specified matching graphs, so a numerical application to the smooth core needs a controlled exterior-tail error as well.

Exact permutation boundaries at the W33 channel sizes give both outcomes with the same one-step singular spectrum. In one boundary, a single light port is linked to every heavy channel in a cycle, giving `G=I` and reflection winding equal to the number of winding masses. In the other controls, d winding channels have isolated self-loops. They give d normalizable exterior zero modes at z=1 and reflection winding r−d, where r is the number of winding masses. The controls realize both adjoint outcomes and all four triplet outcomes. They verify that even the complete one-step singular spectrum leaves the split undetermined.

Run `python analysis/toe_20261113_monopole_grand_spin.py` and `python analysis/toe_20261113_monopole_observability.py` from the repository root. [Channel ledger](../data/toe_20261113_monopole_grand_spin.json) · [Matching controls](../data/toe_20261113_monopole_observability.json)
