# The W33 triplet phase changes the spectrum and reaches both radial flux slots

The triplet phase has an exact obstruction to the fermion rephasing that solves the adjoint problem. The fourth power sum of the canonical triplet mass-squared spectrum depends on phase. The full triplet grand-spin-zero mass is assembled on the neutral hedgehog, including the charged Yukawa completion and the internal gauginos. [Adjoint phase law](2026-11-13_monopole_adjoint_phase.md) · [Grand-spin-zero ledger](2026-11-13_monopole_grand_spin.md)

## Exact mass-squared invariant

Use the positive-flux weight (0,1,0,−2) in the canonical four-Cartan chart. Its holomorphic block is a 25-by-22 pencil `M(z)=F+zD` with rank-three phase part D. For unit z and kinetic Gram matrices G_L and G_R, the eigenvalues of

```text
G_L^(-1) M(z) G_R^(-1) M(z)†
```

are the physical chiral mass-squared eigenvalues with zeros included. The native matter norm is the identity and the adjoint norm is the trace form in the 27. Exact Laurent multiplication gives the power sums

```text
p1 = 1577/3
p2 = 634543/9
p3 = 334701971/27
p4 = 191325201055/81 − (200/3)(z²+z^(-2)).
```

In particular, p4 differs by 800/3 between z=1 and z=i. The opposite-flux weight (0,0,1,3) is phase independent in the vacuum. The phase part and fixed chiral Hessian annihilate the broken gauge orbit there, and the gauge Yukawa supplies a phase-independent mass on that orbit. Thus the varying fourth moment persists in the full exterior spectrum. Kinetic-preserving left and right unitary rotations preserve the moments and cannot remove the phase from this family. The determinant winding of the earlier rank-three quotient still holds. The varying cosine moment is a spectral obstruction to unitary equivalence. [Exact triplet determinant](2026-11-13_canonical_strong_cp.md)

There is a discrete remnant at infinity. Exact diagonal sign matrices preserve the two kinetic Grams and the fixed mass, and reverse D. Consequently the exterior mass spectrum is invariant under z→−z. The replay freezes the signed native coordinates. This accounts for the half-period of the mass spectrum while allowing the scattering phase to accumulate around the full circle.

## The radial mass construction

At the north pole the matter profiles lie in the first two internal components and the adjoint preserves that plane. The native alternating cubic has zero value when two arguments lie in this plane. Each covariant leg of the split and dressed cubics stays neutral on the background. In their Hessian only the first jets of two distinct legs can contribute. A second derivative of a single leg leaves two neutral background arguments and therefore vanishes. The first meson variations along charged directions vanish. Centered meson trace terms can still contribute through second meson variations, multiplied by the off-vacuum trace shifts.

The producer combines the signed cubic, mixed cubics, adjoint trace polynomial, centered meson trace terms, split cubics, and the charged Yukawa completion. It includes the first variations of the internal covariants and of the adjoint powers in the dressed legs. In both flux slots it reproduces the previously computed canonical holomorphic Hessian and its phase derivative. Direct second differences of the superpotential check the off-vacuum first-jet construction to an absolute discrepancy below 3.8×10⁻⁵ in the tested directions. [Covariant Yukawa operators](2026-11-10_light_yukawa_completion.md)

The split coefficient D has numerical rank six in both slots at all nine sampled core radii. At infinity those ranks become three and zero respectively. The second flux slot therefore participates in the phase response within the core. The triplet phase leaves the neutral bosonic profile stationary within this radial ansatz. Its superpotential term and first variation vanish identically there by the same two-neutral-arguments property, while its second variation supplies the phase-dependent fermion mass.

The orthonormal frames on the two flux slots are aligned by the embedded SU(2) ladder. Pairing with the conjugate block adds one internal gaugino on each side. The resulting north-pole matrices have shape 26-by-23. Their two angular copies give a 98-component Hermitian radial Hamiltonian and an exact flux signature (49,49). At the origin the two mass slots agree, as required when the triplet amplitude vanishes. The exterior mass ranks are 23 and 22, giving 45 decaying heavy solutions and four light channels per direction. [Gauge and angular conventions](2026-11-13_monopole_adjoint_shooting.md)

## Light triplet reflection

The numerical shooting uses the frozen real 160-element bosonic profile, vacuum exterior at r=5 and the same gauge Yukawa normalization as the adjoint calculation. It propagates the 49 regular columns from the origin and the 45 heavy decaying columns from the exterior. The transfer on each logarithmic radial cell is a matrix exponential at its midpoint. QR resets stabilize the two subspaces. A fixed exterior light frame is shared across the phase loop, and the match gives a 4-by-4 unitary light reflection matrix. Its determinant is the winding observable.

The 12-point phase grid gives a sampled winding of +1 on both radial meshes. The 48-point calculations on the 120- and 240-cell radial meshes both give +3. Their largest determinant phase increments are 1.613 and 1.603 radians or less. Keeping every fourth sample gives +1 again on both meshes. The rapid rotation near π explains the missed turns. The smallest sampled matching singular values are 0.000886 and 0.000889, at π. Lowering the origin cutoff from 10⁻⁶ to 10⁻⁸ and regridding gives 0.000888 there. Across the refined samples the largest difference between the radial meshes in determinant phase is 0.01081 radians. The largest reflection unitarity error is below 1.71×10⁻¹⁰. A continuous phase gap bound and control of the infinite-domain tail remain open.

Run `python analysis/toe_20261113_monopole_triplet_mass.py` for the mass certificate. Run `python analysis/toe_20261113_monopole_triplet_shooting.py --counts 60 120 --phase-count 12` for the coarse-phase control or use `--phase-count 48` with a distinct output path for the finer sampling. The origin control uses `--counts 120 --angles 3.141592653589793 --inner 1e-8`. [Exact invariants and radial diagnostics](../data/toe_20261113_monopole_triplet_mass.json) · [Coarse phase sampling](../data/toe_20261113_monopole_triplet_shooting.json) · [Refined phase sampling and origin control](../data/toe_20261113_monopole_triplet_shooting_refined.json)
