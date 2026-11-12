# The conventional W33 proton-decay cancellations persist at complex triplet coupling

The heavy-triplet exchanges for `QQQL` and `U^cU^cD^cE^c` vanish identically for every nonzero complex triplet-splitting coefficient `z_T`. The result covers all nine flavor pairs on each side. The same deformation changes the QCD angle by `3 arg z_T`, so the conventional tree-level cancellations place no constraint on that strong-CP contribution. A separate `QQQH_d` calculation gives a nonzero coefficient in the specified light and heavy field coordinates. [Reference Yukawa and proton calculation](2026-11-10_light_yukawa_completion.md) · [Strong-CP phase match](2026-11-13_canonical_strong_cp.md)

## Exact separation of source and propagator dependence

On the 21-dimensional paired heavy quotient write B for the reference mass matrix, P for the triplet-splitting contribution, and `E=B⁻¹P`. The rank-three idempotent E gives the inverse at nonzero z_T as

```text
(B+(z_T−1)P)⁻¹ = [(I−E)+E/z_T]B⁻¹.
```

Each cubic source is affine in z_T. The replay differentiates both the original sources and the z_T-dependent insertion, including terms where the heavy external leg is an adjoint fluctuation. The two conventional channels have source variation ranks (2,2) and (2,3), respectively. Both affine coefficients of each source annihilate the fixed mass nullspaces, so the quotient is valid for every nonzero z_T.

For each of the two conventional channels, the eight contractions formed by taking either source coefficient on each side and either propagator block all vanish separately. Thus the zero holds even when the propagator multiplier and the two source multipliers are treated as independent algebraic parameters in this span. The direct quartic filter from the reference calculation continues to vanish because the individual terms have zero direct light quartic in these charge configurations. This proof concerns the holomorphic tree-level Wilson coefficients. Gauge-vector exchange, soft breaking and radiative effects are separate. [Triplet inverse and dimension-five operators](https://arxiv.org/abs/hep-ph/9807289)

## The down-Higgs channel in a specified light chart

The `QH_d` source overlaps the ordinary light down-antiquark space at rank three, as required by the nonzero Yukawa. Integrating out that source would incorrectly include light propagation. The replay removes the overlap with the full holomorphic kernel using the positive kinetic metric with the 27-trace metric on adjoint components. The heavy inverse can then act on the projected source. The external light representatives are those of the original integral lift chart.

For external Q weights at fundamental indices (3,6,9) and the lower down-Higgs component, the two admissible color-triplet pairings are both included. The pair of two upper weak weights has no intermediate state with the required Cartan charges. The sum over the two admissible pairings has 14 nonzero ordered flavor entries as polynomials in z_T. For flavor indices (0,2,2), its exchange entry in the reference inverse convention is `4112 z_T/813`, nonzero throughout the deformation. The tree elimination contributes the negative of this source-inverse-source contraction in the effective superpotential convention `W_eff=W_light−J_R^T B⁻¹J_L`. No direct light quartic contributes in this channel.

The down Yukawa is invertible. A holomorphic change of the light down-antiquark variables by a color-antisymmetric, weak-singlet QQ bilinear can therefore remove any `QQQH_d` term from the superpotential at this order. In components of flavor space, if the unwanted coefficient has the form `C_k(QQ)(Q_k·H_d)`, use the change in the down-antiquark fields given by `−Y_d⁻¹ C(QQ)` in the convention `(Q·H_d)^T Y_d D^c`. The same change induces higher-dimensional Kähler interactions. The nonzero coefficient in the fixed chart is a matching result, and a basis-independent proton lifetime requires the corresponding Kähler and soft matching.

Run `python analysis/toe_20261113_complex_triplet_proton_decay.py` from the repository root. [Exact output](../data/toe_20261113_complex_triplet_proton_decay.json)
