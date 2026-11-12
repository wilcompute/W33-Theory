# Exact colored threshold phases in the canonical W33 vacuum

Two independent phases in the supplied canonical superpotential shift the low-energy QCD angle while preserving the flat vacuum and all light tree-level Yukawa matrices. The adjoint potential phase contributes three times its angle through one heavy color octet. The triplet-splitting phase also contributes three times its angle through the determinant of a 21-pair triplet block. Thus the CKM data and the tree-level massless spectrum leave a continuous strong-CP parameter. This is a relative phase match at fixed canonical Higgs background, with electroweak and soft masses inserted below the supersymmetric heavy threshold. [Canonical vacuum](2026-11-09_canonical_sm_flatness.md) · [Light Yukawa completion](2026-11-10_light_yukawa_completion.md)

## Color embedding and heavy fermions

The canonical color coroot has squared trace 12 on the 27. The E6 basic form is `Tr_27/6`, so this gives coroot norm two and color embedding index one. The color group embeds in the E6 factor, with trivial family projection. In the liftable low-energy QCD sector the parent continuous angle therefore enters with coefficient one for `θ_E` and zero for `θ_f`. [Parent basic trace and center glue](2026-11-12_parent_theta_lattice.md)

Use a fixed color weight of the fundamental and pair it with its opposite. This counts each massive triplet–antitriplet pair once. After removing gauge directions and massless light modes, the four nonzero ranks of the colored chiral blocks are 6, 21, 6 and 6. There are 39 heavy Dirac triplet pairs and one chiral color octet. Each triplet pair contributes the phase of its Dirac determinant. The octet is a real representation and contributes three times its Majorana mass phase, since `T_color(8)=3` and `T_color(3)=1/2`. These coefficients follow by making each mass real with a Weyl rephasing and including the fermion-measure Jacobian. [Fermion-measure phase](https://doi.org/10.1103/PhysRevLett.42.1195)

There are also nine triplet gauge-orbit directions per fundamental color weight. Together with the broken colored gauginos they form 18 additional triplet pairs. Their masses come from the gauge Yukawa couplings evaluated on the fixed VEVs. At every F-flat point in the deformations below, the holomorphic Hessian annihilates the gauge orbit, so these gauge-Higgs masses contribute zero to the relative phase shift. The constant phase of the full reference determinant depends on the basis and reference threshold convention.

## Two independent deformations

Multiply the entire adjoint trace polynomial by `z_A≠0`. The polynomial is separately stationary at the vacuum. On the nonzero color-root weights its Hessian entry is 480 in a real trace metric with entry six. Only the octet changes among colored fields. The other adjoint Hessian directions it changes are color neutral. In a fixed positive kinetic convention the octet mass ratio is exactly `z_A`. Every light representative has zero adjoint variation, so this deformation contributes no light cubic. It also leaves the previously computed tree-level color-triplet exchange unchanged, since the adjoint polynomial supplies no cubic vertex with two light legs. [Tree-level triplet exchange](2026-11-10_light_yukawa_completion.md)

Independently multiply the triplet-splitting operator, the term using `M[1,2]` and `A²−9I`, by `z_T≠0`. It is separately stationary. At quadratic order its entire support is in the weak-singlet color-triplet and antitriplet sectors with `6Y=±2`. Write B for the reference invertible 21-by-21 matrix on the paired massive quotient and P for this operator's contribution there. The replay verifies that P annihilates both original nullspaces. The exact matrix `B⁻¹P` is idempotent with trace three. Therefore

```text
det(B + (z_T−1)P) / det(B) = z_T³.
```

The light and gauge kernels are unchanged for all `z_T≠0`. This term has zero cubic on the fixed light slice, as in the original light-Yukawa calculation. The separately supplied up and down Yukawas therefore stay fixed under either deformation. This calculation leaves the triplet-mediated proton-decay amplitude at general `z_T` open.

## Relative strong-CP match

For a fixed reference mass chart and nonzero light quark and gluino masses, the phase shift to leading order in decoupling the heavy supersymmetric thresholds is

```text
Δ θ̄_3 = Δ θ_E + 3 arg z_A + 3 arg z_T
       + Δ arg det(M_u M_d) + 3 Δ arg m_gluino    (mod 2π).
```

Here `M_u` and `M_d` are the light quark masses, including Higgs VEV phases. The gluino term assumes a soft Majorana mass supplied below the heavy threshold. Electroweak corrections to heavy masses, soft phases in the heavy sector, loop matching and nonliftable parent sectors require separate calculations. [Supersymmetric strong CP and gluino phases](https://arxiv.org/abs/2002.04204)

As a check, multiplying the entire chiral superpotential by one common phase gives 42 times the angle from the heavy chiral thresholds and six more from the two light three-by-three Yukawa determinants. With the Higgs VEV phases held fixed the total is 48. Under a pure superspace redefinition by angle r, the parent gauge angle shifts by `+90r`, the superpotential phase by `−2r`, and the gluino mass phase by `+2r`. The matched angle is invariant since `90−2·48+2·3=0`. The parent invariant independently gives `24−21=3` for the common phase of the two adjoint terms A⁵ and A⁶. [Parent rephasing anomaly](2026-11-12_theta_rephasing.md)

The two independent unit-modulus deformations can move the low-energy strong angle at fixed light Yukawas and canonical vacuum. A symmetry or dynamics that fixes those heavy phases is therefore required for this action to explain a small strong angle. Run `python analysis/toe_20261113_canonical_strong_cp.py` from the repository root. [Exact output](../data/toe_20261113_canonical_strong_cp.json)
