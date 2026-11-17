# Two E6 reflections protect the minimal exchange vertices, and both fail the interval spectrum test

The [first boundary calculation](2026-11-17_E6_orbifold_proton_boundary.md) uses the right-end hypercharge reflection `P = exp(i pi w)` with `w = -6 Y_SM`. The [first spectrum calculation](2026-11-17_E6_interval_R_index.md) fixes that reflection. Here the right endpoint varies over the eight toral SM-commuting sign actions of the exact cubic in the fixed neutral frame. There are exactly two choices that remove both minimal decay mechanisms. Their difference is the Spin(10) matter sign.

## A common parity identity for the two exchange channels

Write `p_Q, p_L, p_U, p_E, p_H` for the five gauge signs on the relevant (Q,L,U^c,E^c,H_u) SM blocks. The intrinsic sign on either sourced spectator field is set to `p_H` to retain its Higgs doublet. Localized matter contains the light components of the same rank-ten matter Hessian. The cubic terms (QQD), (U^c E^cD), (QU^cH_u), and (QLD^c) imply that the sourced (w=+2) triplet has gauge sign +1, (p_U=p_E), (p_H=p_Qp_U), and the sourced (w=-2) triplet has sign (p_Qp_L).

Consequently the two triplet exchange blocks can reach their sourced endpoint values precisely when the corresponding bilinear gauge current is even. These are the two bits

| Triplet block | Effective endpoint sign | Gauge grade and current with the same sign |
|---|---|---|
| (w=+2) | (p_Qp_E) | (+5), (Q^dagger E^c) |
| (w=-2) | (p_Lp_U) | (-1), (L^dagger U^c) |

The exact Lie-algebra nullspaces check the complementary baryon-changing currents and their coupling. Whenever a bit is even, the corresponding grade has a nonzero trace-metric projector witness of magnitude (1/6) coupling two currents whose baryon charges differ by one. These witnesses certify an allowed exchange, without specifying a physical gauge mass matrix. The source scan allows arbitrary mass mixing among chiral fields at a fixed weight. When both bits are odd, every remaining grade of the endpoint Lie algebra has a unique baryon charge among its light currents, and the retained triplet sources cannot form a baryon-violating exchange. These statements concern the minimal vertices. Local chiral contacts and the covariant normal-derivative gauge vertex identified in the first boundary calculation still require their own selection rules.

## The second reflection is a matter-sign partner

Both passing reflections fix a 38-dimensional gauge subalgebra, of type `su(6) + su(2)`. Their product `M` has 46 fixed adjoint directions, of type `so(10) + u(1)`. It is even on the ten lifted matter components and the unused neutral component at index 7. It is odd on the other 16 light components, including the neutral matter coordinate at index 8. It is even on every sourced spectator leg. This is the (16) versus (10+1) sign in the `27` branching. The two reflections agree on light bilinears of the (16) and on the sourced spectators. The exact scan also includes the additional neutral component among light gauge currents.

The two passing reflections have sign pairs `(+,+)` and `(+,-)` on the two neutral Higgs-frame lines. The second requires its own intrinsic parity choice for the second bulk frame field if that field takes a nonzero endpoint value. The background (H_2) is odd under (M), so the product identity is an identity of gauge actions before the VEV and does not establish an unbroken four-dimensional matter parity. The common fixed adjoint dimension is 22 before the frame VEVs. This connects the repo's [Spin(10) matter-sign analysis](2026-09-21_qpsi_matter_parity_e8_d8_bridge.md) to the actual proton-decay tensor. See also [Cornell et al. on exceptional 5D orbifold breakings](https://arxiv.org/abs/2501.13118).

## Spectrum with the 650 included

For each of the two right reflections, the verifier tests all eight inner left-end actions in the interval index calculation. It adds the bulk `650` by taking the parity-resolved character of `27 tensor dual(27)` and removing the singlet and adjoint. It also resolves the neutral color-octet and weak-triplet coordinates. Each of the 16 endpoint pairs has an integer functional that annihilates every index column from the bulk `27, 78, 351, 351', 650` and conjugates, localized `27` parity blocks, and neutral singlets, but is nonzero on the required spectrum after accounting for the gauge tower.

The result tests a fixed toral right-end frame and an unbroken `Z4^R`. It leaves open different charged boundary representations, outer twists, and a changed vacuum and source geometry. It identifies two equivalent ways to project the minimal exchange and a definite failure of the tested bulk spectrum for both. Boundary-localized higher-derivative operators can generate physical proton decay independently of this classification. [Hebecker and March-Russell](https://arxiv.org/abs/hep-ph/0204037)

Reproduce with `python analysis/toe_20261117_E6_reflection_proton_scan.py`. The matching output is `data/toe_20261117_E6_reflection_proton_scan.json`.
