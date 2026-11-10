# Exact neutral Higgs–lepton mixing in the W33 light theory

The original 49-component light theory has an exact rank-four neutral quartic on the down-doublet space. The earlier rank-three Weinberg calculation is its restriction to the three lepton doublets. The full calculation keeps the fourth, down-type Higgs doublet. It shows that the supplied unit-coupling point mixes the lepton and Higgs directions and that the previous one-coupling neutrino fit cannot remove that mixing. [Previous Weinberg matching](2026-11-10_neutrino_matching.md), [Basis-independent lepton–Higgs analysis](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.65.075025)

## Matching and intrinsic Higgs direction

Write the neutral quartic as `W_4 = u² dᵀ K d / 2`, where `u` is the neutral up-Higgs and `d` comprises the four down-doublet components with the opposite weak weight. The four source columns have rank four. They annihilate the broken gauge directions, so solving the same rank-26 neutral Hessian gives a unique pairing for all four. The direct and exchange principal blocks on the leptons independently reproduce the earlier certificate.

The down-quark Yukawa tensor singles out a covector. Its kernel defines the lepton three-plane. With canonical matter and positive relative adjoint scale `t`, the gauge-quotient metric in the raw basis has diagonal `(19,19,(1080t+71)/(54t+4),19)` and one off-diagonal entry `G[L2,Hd] = 1` and its transpose. Preserve the lepton plane and set `h = Hd − p L2`, where `p = (54t+4)/(1080t+71)`. This is the orthogonal Higgs direction, up to scale. At `t=1` its norm squared is `21811/1151` and the up-Higgs norm squared is 21.

Write the quartic in this adapted basis in blocks `K_LL`, `b = K_Lh` and `c = K_hh`. The exact mixed column `b` is nonzero for every positive `t`. Thus the neutral quartic violates the parity that makes the Yukawa-selected Higgs even and all three leptons odd. The previous `T[1,1]` neutrino fit leaves all three entries of the mixed column exactly constant at each `t`. That one-coupling adjustment cannot make the Higgs–lepton quartic block diagonal.

## Neutral electroweak breaking and conditional neutralino matching

The rank-four result also rules out a supersymmetric neutral electroweak-breaking branch emanating from the specified point. On a small neutral D-flat configuration the leading equation equates the squared up-Higgs norm and the summed squared down-doublet norms. The leading down-type F equation is `u² K d = 0`. Any hypothetical sequence of small nonzero D- and F-flat neutral configurations has a normalized convergent subsequence with both up and down components nonzero. Its limiting F equation contradicts invertibility of `K`. This is a local neutral-sector result. A soft-breaking potential or a separate vacuum could change the electroweak analysis.

For a conditional real neutral background with nonzero `u,d` along the up-Higgs and orthogonal down-Higgs, use canonical normalization and set sneutrino VEVs to zero. The neutrino–Higgsino block has columns `2ud b` and `u² b`. The Higgsino submatrix is `c [[d²,2ud],[2ud,u²]]`. With bino and wino masses `M1,M2`, their leading gauge exchange subtracts `α v vᵀ` from that submatrix, with `v=(u,−d)` and `α=(gY²/M1 + g2²/M2)/2` in the convention where `u,d` are field VEVs. The replay verifies the Schur formula

```text
M_neutrino(0) = u² K_LL − (rᵀ N^-1 r) b bᵀ
r = (2ud,u²), N = higgsino − α v vᵀ
```

The zero-momentum correction has rank at most one when the heavy block is invertible. This formula assumes the displayed quartic and no extra μ term or bilinear. It fixes the texture of the leading mixing correction for a supplied background. It does not determine the VEVs, gaugino masses, or pole masses. [Neutralino conventions](https://arxiv.org/abs/hep-ph/9709356)

## Explicit alignment using the existing neutral fields

The earlier three ordinary currents extend to four by using one exotic projector on the down-Higgs component. Use centered meson traces `I=(I_00,I_01,I_02,I_10)`, with `I_jk = Tr(M[j,k])−Tr(M[j,k])_vev`. Three currents are as in the earlier neutrino calculation. The fourth is

```text
J_H = Z[1] : [ A E A(A−3I) X[0] F[1,0]^T ].
```

Here `E` is the exotic internal projector covariant. Its leading light bilinear is supported only on the raw down-Higgs direction. The four currents give an invertible pairing on `(L0,L1,L2,Hd)H_u`. The four centered traces have identity pairing through the exact neutral mass inverse. Thus the optional interaction `Σ T[k,f] I_k J_f` realizes

```text
K(T) = K(0) + Dᵀ D − (TJ−D)ᵀ(TJ−D).
```

The completed square shows that **real rank two is minimal** within this deformation for simultaneous alignment and the benchmark splitting. For a real rank-one matrix write `T = w rᵀ` with `||w||=1`. Its correction is `d_w d_wᵀ − a aᵀ`, where `d_w = Dᵀ w` and `a = Jᵀ r − d_w`. The Higgs entry of `d_w` vanishes for every `w`. Alignment therefore forces `a_L a_h = b`, so the positive lepton mass matrix becomes `−K_LL − d_w,L d_w,Lᵀ + b bᵀ/a_h²`. The replay proves a positive-definite floor `−K_LL − D_Lᵀ D_L` and a largest generalized mass above 48000 in these integral units. On the two-plane `bᵀ v=0` the positive mass Rayleigh quotient stays below 300. The latter check uses Sturm root counts for both leading minors over `1/20 ≤ p ≤ 4/71`. Min-max gives a squared-gap ratio less than `1/25599` for every aligned real rank-one deformation and every positive adjoint scale.

Two rows suffice at unit adjoint normalization. With zero-based labels, set row 1 of `TJ` to `(bᵀ/1000,1000)` and row 2 to `λ J[1,:]`. Both rows of `D` vanish. The first row cancels the mixed column exactly, while the second tunes the ratio without reintroducing it. Exact inertia bounds put the ratio below `37/1250` at `λ = 12/5` and above it at `λ = 5/2`. The two rows are independent throughout that interval. This fit introduces no new fields, starts at cubic order around the original vacuum, and preserves the earlier colored-triplet cancellation because all linear `I_k` sources are neutral and the relevant four charged legs contain no charge-zero pair. It supplies no prediction of mixing angles or a low-energy spectrum. [NuFIT 6.0](https://link.springer.com/article/10.1007/JHEP12%282024%29216)

Run `python analysis/toe_20261110_neutral_higgs_alignment.py` from the repository root. [Exact certificate](../data/toe_20261110_neutral_higgs_alignment.json)
