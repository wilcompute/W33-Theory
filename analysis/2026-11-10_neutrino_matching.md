# Exact Weinberg matching and a neutrino hierarchy test

The published 49-component light vacuum with the Yukawa and triplet operators already generates a rank-three Weinberg matrix. This calculation uses its existing couplings and fields. It also gives a bound on the supplied unit-coupling texture. For unit matter kinetic matrices, varying the relative adjoint kinetic normalization over all positive values cannot make the tree-level splitting ratio of the Weinberg block larger than 1/30000. [Light vacuum and couplings](2026-11-10_light_yukawa_completion.md), [Weinberg operator](https://doi.org/10.1103/PhysRevLett.43.1566)

## Exact tree-level matching

Use the three lepton doublets in the kernel of the down-Higgs covector. For each take the weak weight opposite to the neutral up-Higgs weight. Their bilinears with the up-Higgs have total Standard Model weight zero. The alternative pairing through two same-weight Higgs or two same-weight leptons would need weight `±2(0,0,1,−3)`, which is absent from the full fluctuation space. The family anomaly spectator has a separate quadratic block and supplies no linear source, since its interactions at this point have at least two spectator factors.

The zero-weight Hessian is 38 by 38 and has rank 26. The three exact neutral sources have rank three and annihilate the gauge orbit. The calculation differentiates the published superpotential using commuting square-zero direction variables. This retains the full variation of mesons and the adjoint in the neutral cubic, and the full direct light quartic. The replay checks the original Hessian in the fundamental, conjugate, and adjoint mixed blocks and checks a nonzero up-quark Yukawa against its earlier certificate.

Let `S` contain the three neutral sources and solve `M U = S` for the rank-deficient neutral Hessian `M`. The matching term `−SᵀU` is independent of the arbitrary gauge-kernel component of the solution. In the convention `W = (L H_u)ᵀ κ (L H_u)/2`, the direct term is `diag(117,54,0)` and the full matrix is

```text
[ -30487293/6020       0       -1205280/301 ]
[              0   -3780              -4590 ]
[    -1205280/301   -4590    -294143400/301 ]
```

The negative of this matrix is positive definite. Once the up-Higgs obtains a VEV, the operator supplies a rank-three tree-level Majorana block. The entries are in the integral lift convention.

## An exact failure of the unit-coupling texture

Take unit Hermitian kinetic matrices on the fundamental and conjugate fields and use `t Tr(A†A)` on the adjoint with arbitrary `t > 0`. The lepton metric is obtained by minimizing each norm over its broken gauge orbit. Ignoring the adjoint penalty gives the lower Gram bound `diag(19,19,71/4)`. Using the chosen lift with zero adjoint component without subtracting the orbit gives the upper bound `diag(19,19,20)`. Both are exact. The unit-adjoint quotient is `diag(19,19,1151/58)`.

Since `−κ` is positive definite, the ordered masses of this block up to a common factor are the generalized eigenvalues of `(−κ,G)` for the quotient Gram `G`. The min-max principle and exact inertia checks give `m₂ < 270` and `m₃ > 48000` uniformly over positive `t`. Hence `(m₂²−m₁²)/(m₃²−m₁²) < 1/30000`. The numerical ratio at unit adjoint normalization is about `1.30e−5`. NuFIT 6.0 gives a normal-ordering benchmark of about `0.0296`. An overall scale choice cannot close that gap in the matching-scale block. A comparison with the full low-energy spectrum requires electroweak symmetry breaking, possible Higgsino and gaugino mixing, and running. [NuFIT 6.0, Table 1](https://link.springer.com/article/10.1007/JHEP12%282024%29216)

## What the existing neutral fields allow

There is an explicit deformation that spans all complex symmetric neutrino matrices. Let `I_k = Tr(M[0,k]) − Tr(M[0,k])_vev` for `k = 0,1,2`. Let `F[2,f]` be the previously certified family matrix unit word and let `O` denote the ordinary internal projection covariant. Define

```text
J_f = Z[0] : [ A O A(A−3 I) X[0] F[2,f]^T ]
ΔW = Σ_(k,f) T[k,f] I_k J_f
```

The two endpoint adjoint factors annihilate their respective VEVs, so each `J_f` starts at quadratic order. The centered `I_k` starts at first order. The deformation preserves the original F-flat point and mass matrix. The light `J` pairing on `L H_u` is invertible with nonzero entries of magnitude 162. The factor `A−3I` puts `H_u` on the conjugate leg of the pairing, and the ordinary projection separates the leptons from the down-Higgs. The gradient matrix of the three `I` invariants has exactly the identity as its pairing through the neutral mass inverse.

Let `D` denote the difference of the direct light `I` pairing and its pairing with the baseline neutral sources through the inverse mass. Direct and heavy contributions then combine to

```text
κ(T) = κ(0) + D^T D − (T J − D)^T (T J − D).
```

Every complex symmetric matrix factors as `B^T B` over the complex numbers. Invertibility of `J` therefore makes the image of the deformation the whole complex symmetric three-by-three space. These optional degree-at-most-13 interactions introduce no new particles. Their cubic terms require a neutral linear source, so they do not change the earlier colored-triplet exchange. A direct quartic in either conventional proton-decay channel also vanishes, since none of its external charge pairs sums to zero. The deformation shows that the neutrino texture can be fitted with supplied coefficients and gives no explanation for those coefficients.

Only one real coefficient is needed to reproduce the benchmark gap ratio in the isolated block. With zero-based labels set only `T[1,1] = λ`. The corresponding row of `D` is zero, so this changes `−κ` by a positive rank-one update. At unit adjoint normalization, exact inertia bounds put the ratio below `0.0296` at `λ = 12/5` and above it at `λ = 5/2`. Continuity therefore gives a fitted value inside that interval. The bracket fits one ratio and supplies no prediction for mixing angles or the remaining neutral fermion sector.

Run `python analysis/toe_20261110_neutrino_matching.py` from the repository root. [Exact matching certificate](../data/toe_20261110_neutrino_matching.json)
