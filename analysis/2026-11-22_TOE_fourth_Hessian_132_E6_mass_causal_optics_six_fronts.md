# Exact fourth-stage Witting compiler, constructive 132D E6/H27 bridge, Higgs cubic masses, kinetic causal null, and optical POVM synthesis

Date: **2026-11-22**. Repository: `wilcompute/W33-Theory`, default branch `master`.

## Scientific boundary and related work

This research packet executes the five separate directions requested after the earlier third-stage compiler, and adds an independent 20-outcome Witting measurement. The mathematical results are exact combinatorial calculations or explicitly stated finite-dimensional constructions. Optical loss and causal spectroscopy are **toy numerical models**, not physical measurements or an experimentally verified Theory of Everything.

Earlier repo (not novel here): rank-one Witting 4-mode gates with dense SU4 closure; 648-element Hessian subgroup and normal H27 order27; exact counts 17,496 (one stage), 385,560 (two), 7,793,496 (three); 1+12+27 ray partition; 30/39 rank-one Witting POVMs; E6 singlet model leaving 124 charged F-term tangent directions; 81D E6 representation no-go; causal permutation Metropolis Hamiltonian and 4..7 graph gaps. The classical Hesse cubic, qutrit SIC and MUB, and K-S Witting geometry are established prior work.

External sources checked:
- E6 trinification: `78 -> (8,1,1)+(1,8,1)+(1,1,8)+(3,3,3)+(bar3,bar3,bar3)` and `27` splitting into three nine-dimensional blocks: [E6Tensors reference](https://www.researchgate.net/publication/303367338_E6Tensors_A_Mathematica_Package_for_E6_Tensors); [representation-branching discussion](https://mathoverflow.net/questions/337224/branching-rules-for-e6-into-su33).
- Caputo–Liggett–Richthammer (2010), **Proof of Aldous' spectral gap conjecture**: [arXiv:0906.1238](https://arxiv.org/abs/0906.1238). The interchange process has the ordinary random-walk gap on its underlying weighted graph.
- Benincasa–Dowker, **Scalar curvature of a causal set**: [Phys. Rev. Lett. 104, 181301](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.104.181301); this involves causal sets with Lorentzian continuum structures, not the finite orientation toy below.
- [Minimal informationally complete POVMs need at least d^2 effects](https://link.springer.com/article/10.1007/s11128-021-03045-9) (dimension 4 -> lower bound 16).
- Existing repo result `analysis/PASS20261011_H27_HESSE_CUBIC_F_FLAT_LOCK.md` proves the two-dimensional **family** H27 cubic invariant space and an F-flat obstruction for a standalone fundamental qutrit cubic. Our H27 family coupling below *multiplies* an E6 cubic tensor; the pure E6-singlet branch nullifies that cubic, so it is not a counterexample to the older standalone Hesse-potential theorem.

## 1. Fourth exact compiler: 153,160,632 distinct operations

Let `H` be the 648-element Hessian subgroup, `N` its normal order-27 H27 subgroup, and `D` the involutory fixed Witting ray-36 phase gate. A phase-flip stage is `DN`; a product with four stages lies in `H(DN)^4`. Exact coset enumeration from `analysis/toe_20261122_fourth_hessian_census.py` gives:

| Number of D stages | Left-H cosets | Distinct complex matrices |
|---:|---:|---:|
| 1 | 27 | 17,496 |
| 2 | 595 | 385,560 |
| 3 | 12,027 | 7,793,496 |
| 4 | **236,359** | **153,160,632** |

At stage four, there are `12,027*27 = 324,729` candidate right extensions. Each candidate is an exact 4×4 matrix over `Z[omega]/6561`. Compare left-H cosets by the invariant fixed-ray bra as a fast necessary hash and by exact membership of `X Y^dagger` in all 648 matrices of `H` as the complete equivalence test. There are 176,230 signature buckets and 1,010,231 exact comparison operations; 236,359 equivalence classes survive. Multiplying by 648 yields the stated total. Six exact unitarity spot checks are included. This count is for distinct **complex** unitary matrices (not projective classes), and says nothing about efficient approximations at arbitrary precision or shorter alternative circuits. The growth ratio from stage three is 153160632/7793496 ~= 19.65.

## 2. A constructive 81-to-132 E6/H27 isometric embedding

The previous result ruled out a genuine 81D E6 representation whose H27 restriction consists of three regular 27D modules, under the identification of the H27 center with the global E6 center. It left open whether the necessary size **132 = 78 + 27 + bar27** is attainable for an **H27-invariant image** in an honest E6 carrier. It is.

Work in the standard `SU(3)^3` trinification branching. Let `omega^3=1`, `X|j>=|j+1>`, and `Z|j>=omega^j|j>`, so `XZ=omega^-1 ZX`. Embed H27 using first and third SU3 factors:

```
x = (X, I, X),    y = (Z, I, Z^-1),    [x,y] = (omega^-1 I, I, omega I).
```

Inside the E6 adjoint 78, choose the `(3,3,3)` 27D summand, **neutral** under the H27 center. Add the E6 fundamental 27 and antifundamental bar27, with center characters `omega` and `omega^2`, respectively. Their direct sum is an 81D H27-invariant subspace `S` inside the 132D honest E6 representation `78+27+bar27`.

In each of three H27 center-character sectors, build three mutually orthogonal *nine-state* Weyl orbits. For the neutral sector use the fiducials `|0,r> (|0>+|1>+|2>)/sqrt(3)`, `r=0,1,2`. In the charged sector use two maximally entangled two-qutrit fiducials and one complementary shift-Fourier fiducial in the three E6 fundamental 9D blocks; use their conjugates in the anticharged sector. Each orbit consists of `x^a y^b` for `(a,b) in F3^2`. The central inverse Fourier transform converts the 3×(9+9+9) vectors into 3 regular H27 modules.

A concrete 132×81 complex `T` was constructed, with `T^dag T=I_81` and `rho_132(x)T=T L_x`, similarly for `y,z`. Maximum residual: `6.7e-16`.

The E6 adjoint restricted to the center-trivial quotient `H27/Z(H27)=Z3^2` has character 78 at the identity and 6 at nontrivial quotient elements. Thus the trivial quotient character occurs with multiplicity 14 and each of the eight others with multiplicity 8; in particular, it contains the needed three quotient-regular modules. This is another exact group-character check.

**Limitation:** The 81D `S` is **not** full-E6 invariant: its chosen 27D neutral part is a proper H27-stable subspace of irreducible E6 adjoint78. The remaining 51 adjoint components provide an unavoidable leakage channel under generic E6 transformations. This proves existence of the requested center-compatible **carrier** at the lower bound, not an E6-equivariant 81D state encoding, a matter spectrum or a unitary physical device.

## 3. E6 cubic terms lift 60 of 124 charged Higgs tangent directions

At the earlier three `27_H+bar27_H` pure-singlet vacuum, the previous five F constraints remove singlet moduli, but 156 nonsinglet Higgs components leave 124 non-gauge complex quadratic massless tangents. The E6 cubic invariant has SO10 terms `1_4 10_-2 10_-2` and `16_1 16_1 10_-2`. It has **no** `1_4 16_1 16_1` term.

An external family-H27-invariant cubic contraction uses the established symmetric Hesse tensor: diagonal `T_{aaa}=1` and all-six-permutation mixed `T_{012}=k`. With `k=1/2` and the exact singlet VEV `(1,1,omega)`, the family 10-plet Hessian is

```
M = [[1,       omega/2, 1/2],
     [omega/2, 1,       1/2],
     [1/2,     1/2,     omega]].
```

It is invertible with eigenvalues of `M^dag M` equal to `1, 7/4, 7/4`. The antifundamental conjugate gives the same spectrum. Consequently, **all 60** `10+bar10` complex chiral components acquire quadratic superpotential masses in arbitrary units, **while 64** spinor-like 16 components remain massless after the 32 complex spinor gauge-Goldstone directions are removed. The five previous singlet F-term constraints remain satisfied because the E6 cubic has no invariant `1*1*1` term.

This is a partial charged-Higgs mass lift, **not** a realistic E6 supersymmetric vacuum; it still has 64 quadratic zero modes. Also, the family H27 is treated here as an **external flavor symmetry**, which must not be silently conflated with the subgroup of the E6 gauge group in the embedding section. Complete D-flatness, quantum corrections, anomalies, chiral spectra and dynamics are unresolved.

## 4. A sharp causal false-positive control via the Aldous gap

The previously published nested W33-induced causal toy Hamiltonians generated by random adjacent transpositions have first-excitation gaps `0.17822437,0.09157177,0.05070242,0.03147447` at `n=4,5,6,7` total-order vertices. Under the **same transposition dynamics but with geometric interval action identically zero**, the normalized interchange process has exact gap

`gap_0(n)=2*(1-cos(pi/n))/(n-1)`

by the established Aldous spectral-gap theorem. Direct sparse eigenvalue checks agree with the formula to 1e-10. The free gaps are `0.19526215,0.09549150,0.05358984,0.03301038`. Thus the observed decreases are already generated by the **algorithmic update rule alone** and are not evidence for emergent spin-two gravity. The W33-to-free ratios lie between 0.91 and 0.96 at these finite sizes. This does **not** rule out different causal-set models or prove the absence of gravity in a proper continuum theory.

## 5. Explicit optical Naimark synthesis, with rail-local loss

The earlier 30-/39-effect Witting Naimark isometries were numerically completed to arbitrary 30×30/39×39 unitaries, and a generic full mesh was counted as 435/741 two-mode cells. That full completion is unnecessary for implementing a **4-input, m-output isometry**. Adjacent-row complex Givens elimination reconstructs the original isometry exactly (error less than 2e-10); general upper bound `4m-10` two-mode couplers:

| Measurement | Outputs | Constructive adjacent couplers | Observed survival at eta=0.995 per hit |
|---|---:|---:|---:|
| 39-effect | 39 | 138 | 0.90447 |
| 30-effect (basis 0) | 30 | 110 | 0.91018 |
| 30-effect (best of 21 tested orderings) | 30 | 109 | 0.92018 |

Only the **two affected rails** are attenuated by `sqrt(0.995)` after each coupler. The resulting nonunitary 30×4 map satisfies `K^dag K <= I`, defining an input-dependent no-click effect `I-K^dag K`. Average survival is evaluated for maximally mixed four-mode input. Losses from propagation, phase drift, sources, detectors, path crossings and hardware imperfections are excluded. Row ordering matters; the optimization above is a finite 21-candidate search, not a global minimum or measured power budget.

Crucially, raw component reductions do not automatically improve estimation precision: in the earlier five-state linear tomography calculation, the generic-pure-state coefficient was `22.06/N` for 30 outcomes versus `18.71/N` for 39, where N is **detected** photons. Calibrated statistical risk must be compared per *input* photon together with the rail-loss model.

## 6. Independent outside-the-box option: a 20-effect Witting IC POVM

Five pairwise disjoint Witting orthonormal tetrads can be selected:

```
(1,13,21,29), (3,7,27,35), (4,37,38,39),
(8,23,25,26), (9,24,31,34).
```

Assign each projector weight `1/5`. Each tetrad sums to `I_4`, hence the 20 effects sum to `I_4`. Their 20 weighted rank-one projectors span all 16 real dimensions of Hermitian 4×4 operators, verified numerically and over six split finite fields. Thus this is a **20-effect informationally complete** Witting POVM, using only 20 of the 40 available rays.

The 20-effect frame condition number is `87.4264`, much worse than the 30-effect design's `~14.08`. Its seeded-pure-state linear-inversion Hilbert-Schmidt MSE coefficient is `50.36/N` detected photons. A constructive 20×4 adjacent-coupler circuit uses **70** two-mode elements with simulated maximally mixed survival `0.94293` at eta=0.995 per-hit. This lowers channel count and potentially photon loss but more than doubles shot-noise amplification relative to the 30-effect design. Not a d=4 SIC; no global minimality is claimed. The absolute lower bound for d=4 IC-POVM cardinality is 16, and existence within the restricted Witting set at 16–19 outcomes was not resolved. The previous **30-effect minimality** held only under the constraint that **all 27 universal-control rays** retain positive effects; this 20-effect design drops that constraint.

## Reproducibility

Six independent source producers and six JSON result certificates were added:

```
analysis/toe_20261122_fourth_hessian_census.py
analysis/toe_20261122_e6_132_constructive_embedding.py
analysis/toe_20261122_e6_higgs_cubic_mass_lift.py
analysis/toe_20261122_photonic_sparse_isometry_loss.py
analysis/toe_20261122_causal_aldous_null_control.py
analysis/toe_20261122_20effect_Witting_context_POVM.py
```

The dedicated regression file is `tests/test_toe_20261122_frontier4.py` (12 tests); accompanying GitHub Actions workflow installs `numpy scipy sympy networkx pytest`, runs the tests and regenerates the results. Local focused tests pass **12/12**; the preceding 74-test baseline passed in the prior research pass. GitHub Actions remains independently queued until runner completion. The Windows local checkout has not been synchronized in this environment.

## Five independent research extensions

1. Full **Hecke/double-coset spectral compiler**, with proven synthesis error and next-stage growth without exponential storage.
2. Extend the **132D E6 carrier** into an explicit gauge-equivariant code, proving leakage/error-correction capacity under broken versus unbroken E6.
3. Lift the remaining **64 spinor Higgs tangents** using controlled adjoint or higher-dimensional couplings without upsetting F/D equations, anomaly cancellation or chiral phenomenology.
4. Replace the W33 order-swap toy with a **Lorentzian causal-set action** and compare against both Aldous kinetic null and continuum d'Alembertian/BDG benchmarks.
5. Optimize **20/30/39-effect photonic tomography** jointly over row ordering, input-dependent loss, calibrated SPAM and photon-budget fidelity rather than coupler count alone.
