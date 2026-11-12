# The W33 adjoint monopole phase is an exact fermion rephasing on a fixed core

Each of the three winding adjoint charge blocks is made entirely of adjoint chiral fermions and internal gauginos. The holomorphic mass and the gauge Yukawa coupling in each block obey an exact opposite-rephasing symmetry. For a fixed smooth core this removes the entire adjoint phase from the radial spectral problem and transfers one unit of winding to the light reflection in each block. A separate calculation shows why holding the bosonic core fixed is a substantive restriction. [Grand-spin reduction](2026-11-13_monopole_grand_spin.md)

## Native radial mass

Use the north-pole gauge, with adjoint scalar A(r). Each charged block contains one internal adjoint root vector at each monopole weight n=±1, together with the opposite-weight root vectors. These four weight spaces are one-dimensional in the 78 and absent in both the 27 and its dual. The absence of matter weights also implies that the root matrices annihilate the entire neutral matter plane and its dual. Since A preserves that plane, insertions of these matrices in the matter-dependent operators give zero in the two-adjoint variation. The three mixed cubics are linear in A. The family gaugino is an embedded-isospin singlet. Thus the chiral–chiral entries come from the trace polynomial alone, and the gauge Yukawa couples the adjoint chiral fermion to its gaugino. There is no gaugino Majorana term in the supersymmetric radial model. [Gauge Yukawa convention](https://arxiv.org/abs/hep-ph/9709356)

For opposite generators X and Y, the unnormalized holomorphic entry is

```text
h(X,Y) = Tr[X Df(A)[Y]]
f(A) = A^5 − 3A^4 − 283A.
```

The Fréchet derivative inserts Y into every position of each power. The gauge entries are proportional to the trace pairings of the generators with [A†,Y] or [A†,X]. The replay uses the native real generators and computes these entries on the nine frozen neutral-core samples. Its gauge entries use the commutator convention [Y,A†] and omit the common gauge coupling and constant phase. The two generators in each doublet have squared trace norm six. In this chart the asymptotic chiral entries on the positive-flux slot are 480, 480 and −180. The gauge pairing there vanishes. On the negative-flux slot the chiral entry vanishes and the gauge commutator entry is 30 in all three blocks. This independently recovers one light gaugino per direction. [Neutral profile and trace potential](2026-11-11_monopole_neutral_core.md) · [Asymptotic phase matching](2026-11-13_sm_threshold_theta.md)

## Entire phase loop at fixed background

Let z=e^(iφ) multiply the adjoint superpotential. In the Weyl flavor order (adjoint chiral, gaugino), put T=diag(e^(iφ/2),e^(−iφ/2)). Each holomorphic mass block has the form

```text
M(z) = [ z h     y_L ] = T M(1) T.
       [ y_R      0  ]
```

For a fixed profile, the substitution ψ_z=T†ψ_1 on left Weyl fields and the conjugate substitution on their conjugates maps the two radial equations exactly, including the regular origin condition and decay or scattering conditions at infinity. It commutes with the angular kinetic and gauge terms because it is a constant scalar on each fermion species. The common sign change of T after one phase period has no effect on the mass or the reflection. The bound spectrum and the dimension of the localized zero-mode space are constant along this fixed-profile loop. Any localized state at zero persists through the loop, so the adjoint phase drives no isolated bound-level crossing in this calculation.

In the positive magnetic flux block and with the physical left-Weyl sign `i∂tψ=iσ·Dψ`, the outgoing light gaugino is left Weyl and the incoming one is its opposite-weight conjugate. Their phases are respectively e^(iφ/2) and e^(−iφ/2). The incoming-to-outgoing light reflection therefore obeys `R(z)=z R(1)` wherever the reflection exists. Its winding is +1 per block, with the same orientation as the exterior positive-flux mass winding. The two color partners and the weak block give +3 in total. This covariance also holds at a phase-independent localized zero mode whenever reflection is defined by a scattering limit, since the unitary substitution holds at nonzero energy as well. The reference reflection phase and the existence of such a zero mode still require one radial solve. [Weyl channel convention](https://arxiv.org/abs/2408.04577) · [Exterior phase winding](2026-11-13_monopole_heavy_phase_flow.md)

## A self-consistent core can respond to the phase

The bosonic F energy contains the interference term `2 Re(z <F_mixed,F_trace>)`. The frozen real core has nonzero overlap, approximately 17.715 at r=0.002 in the repo normalization, with a sign change by r=0.1. Thus the phase dependence of the bosonic energy cannot be dropped on that profile. This also gives a conditional extension. If a continuous family of real radial profiles is chosen as a single-valued function of cos φ, its reference reflection retraces itself during a full phase loop. Provided that reference reflection exists continuously, the explicit fermion phase then supplies the entire winding on the varying real family as well. Complex self-consistent cores and quantum rotor scattering are separate problems.

Run `python analysis/toe_20261113_monopole_adjoint_phase.py` from the repository root. [Mass coefficients and profile overlap](../data/toe_20261113_monopole_adjoint_phase.json)
