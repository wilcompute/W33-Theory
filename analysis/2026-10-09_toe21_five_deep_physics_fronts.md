# TOE Round 21 — Five independent physics frontiers, evaluated against the existing W33 mathematics

**9 October 2026.** Repository: `wilcompute/W33-Theory`. Each result distinguishes a mathematical theorem, an assumed physical model, and missing experimental or dynamical input.

## Recent parallel work and prior ownership

The repository already contains:
- **Round20/TOE integral bridge**: `w33_20261009_toe_integral_clique_levi_bridge.py` and the natural real-isometric 81-harmonic cycle correspondence.
- **BT1688**: complex irreducibility of the degree-81 W33 Steinberg representation of PSp(4,3).
- **Pass11681**: an independently implemented complete `E8 = sl(9) + Λ³(9) + Λ³(9)*` Lie bracket with Jacobi checks. We **do not re-claim** an E8 construction.
- **`w33_20261009_w33_cartesian_power_spectral.py`**: already demonstrates lack of a dimension plateau for Cartesian W33 graph replication.
- **Pass11313–11319**: externally parameterized renormalization/scale/portal analyses, prior art for our scale controls.
- **Pass11818–11822**: gamma-corrected heterotic R rules, SU(9) family tensors and constraints. Those distinguish Z6-I vs Z6-II; these new five tracks do **not** alter those worldsheet calculations.
- **Pass398 parallel formula-search freeze** was in progress; no unrelated working tree files were staged, altered or reset.

## 1. Explicit finite W33-symmetric dynamical geometric selection

Let A be the ordinary 80x80 adjacency of the connected 4-regular native W33 incidence graph. Investigate the *newly assumed* real/complex, normalized focusing mean-field functional

`E(psi)=-t psi* A psi-g Σ_v |psi_v|⁴, ||psi||²=1, t,g>0.`

Both terms respect every Levi-graph automorphism, in particular type-preserving PSp(4,3). It is NOT derived from W33 geometry alone; in particular `g` and `t` are externally specified energies.

The uniform normalized state u=(1,...,1)/sqrt80 has E(u)=-4t-g/80. A one-site trial delta_v has E=-g. Therefore whenever

`g/t>320/79 = 4.050632911...`

the global minimizer **cannot** be uniform.

An even stronger exact argument rules out every PSp-invariant minimizer: PSp has precisely two vertex orbits (40 points, 40 lines). By entrywise phase alignment, any minimum may be taken nonnegative; a PSp-invariant candidate must have amplitudes a on all points and b on all lines. With r=sqrt40 a, s=sqrt40 b, r²+s²=1, and p=2rs∈[0,1], its energy is

`-4tp-(g/40)(1-p²/2).`

For g/t<160 this is minimized at p=1, the uniform state. A basis delta_v beats the entire invariant family as soon as g/t>320/79. Therefore **every global minimum breaks PSp** for `320/79<g/t<160` (the upper bound can be relaxed after studying other invariant minima).

Local curvature about u for real transverse A-eigenmode v is

`E(sqrt(1-eps²)u+eps v)-E(u)=[t(4-lambda_v)-4g/80]eps²+O(eps³).`

The highest nontrivial A-eigenvalue is sqrt6, so the uniform state remains a strict local minimum **modulo global phase** for

`g/t<20(4-sqrt6)=31.0102...`.

Thus the **certified coexistence/metastability interval**

`320/79 < g/t < 20(4-sqrt6)`

contains lower-energy symmetry-breaking global minimizers while the invariant state remains locally stable. This is a useful example of an effective *first-order-like* selector, though the actual critical coupling and tunneling are not determined.

Numerical 8-start minimizations for t=1 give best energies/peak probabilities:
`g=0: (-4,0.0125); g=3:(-4.0375,0.0125); g=5:(-5.4064411,0.9568086); g=10:(-10.2007618,0.9898199); g=20:(-20.1000941,0.997489); g=32:(-32.0625229,0.9990218)`.
These are **upper bounds** to a numerical variational minimum, not certified global energies.

At **finite** dimension for the *linear* single-photon Hamiltonian -tA, Perron–Frobenius gives a **unique positive symmetry-invariant ground state** and no exact degenerate selected vacua. Thus the nonlinear toy does not already demonstrate quantum spontaneous symmetry breaking. The mechanism needs a dynamical interaction, scale and quantum limit.

## 2. An independent large-q spacetime-emergence stress test

For the classical symplectic generalized quadrangle W(3,q), let k=q+1 and `n=(q+1)(q²+1)`. Its 2n-vertex Levi graph has normalized combinatorial Laplacian L/k with *exact* spectrum:

- `0^1, 2^1`;
- `[1-sqrt(2q)/k]^f, [1+sqrt(2q)/k]^f`, `f=q(q+1)^2/2`;
- `1^(2h)`, `h=q(q²+1)/2`.

With `P_q(s)=(1/2n)Tr[e^{-sL/k}]`, the empirical normalized Laplacian eigenvalue distribution tends to the **point mass at 1** as q→infinity. Hence, for every fixed s>0,

`P_q(s) -> e^{-s}`; `d_s(s)=-2 d ln P_q/d ln s -> 2s`.

A four-dimensional heat-kernel continuum would instead require `P∝s^{-2}` over a genuine scaling window, i.e. d_s≈4 across times, not a single crossing at s=2. The raw unweighted **single-W(3,q) family therefore lacks the necessary scale-invariant diffusion plateau**. The normalized spectral gap tends to 1.

The exact spectra were checked for q=2,3,5,11,31,101,1001 and analytically at q=1000001 to approach the limit. This tests *different graphs* from the already completed Cartesian-power replication study. It is not a universal no-go for weighted/refined graph systems, nonlocal limits, or Lorentzian dynamics; and heat diffusion is Euclidean, not yet causality.

## 3. E8-compatible cubic space on the 81 Steinberg carrier: **one after outer similitude**

The known E8 decomposition under E6×A2 is `248=(78,1)+(1,8)+(27,3)+(27*,3*)`: its charged pieces are two **81-dimensional** modules. The repository already constructs E8 by another sl9/three-form route. No group-intertwining identification between these charged 81 pieces and the W33 Steinberg-81 has yet been derived.

We calculate a **new necessary representation-theory test** rather than infer a bracket from equal dimensions. For every one of all **25,920 PSp(4,3) elements**, use the exact natural Levi-cycle character

`chi(g)=#fixed flags - #fixed point vertices - #fixed line vertices +1`,

then evaluate character averages:

`dim (Λ³ V)^G = (1/(6|G|)) Σ_g [chi(g)^3-3chi(g)chi(g²)+2chi(g³)] = 5`.

Other multiplicities:
- `dim (Sym³ V)^G = 4`;
- `dim Hom_G(Λ² V,V)=11`;
- `dim (Schur_(2,1)V)^G=6`;
- `dim End_G(V)=1`, as a control for prior irreducibility.

**Additional outside-the-box full-symmetry test:** adjoin the projective symplectic similitude induced by the determinant-minus-square GSp(4,3) multiplier, explicitly verifying it lies outside PSp, squares to 1 and normalizes the five PSp generators. The resulting order-**51,840** projective group has **exactly ONE invariant alternating cubic**: `dim(Λ³ V)^PGSp=1`, compared with 5 under PSp. Other extended dimensions: `dim(Sym³V)^PGSp=3`, `dim Hom(Λ²V,V)^PGSp=4`, `dim Schur_(2,1)(V)^PGSp=3`, and `dim End(V)^PGSp=1`. All numbers come from complete integer character sums over 51,840 elements.

Since V is self-dual with an invariant positive metric, this is a **unique (up to scalar) metric-compatible equivariant alternating bracket candidate** under the larger group. This is materially stronger than the five-dimensional family under the connected PSp subgroup. Nevertheless, a nonzero invariant cubic has not yet been materialized as structure constants. **Jacobi, rank, E6×A2 grading, real form, positive-energy action, and locality are all open.** The unique cubic might fail Jacobi; it must not be called an E8 Lie algebra without checking that.

This also prevents false identification of the regular H27 address representation, the H27 Schrödinger operator representation, and the PSp Steinberg-81: these are distinct G-modules until mapped explicitly.

Literature anchor: E8 branching `(78,1)+(1,8)+(27,3)+(27bar,3bar)` is standard, e.g. Slansky, *Physics Reports* 79 (1981), and the repository's own Pass11681.

## 4. Full canonical doubled 81-qutrit Weyl phase space and its obstruction

Take the perfectly paired `V=H1(Levi,F3)` from the previous integral Gram certificate and `V*=Hom(V,F3)`. Then

`W=V⊕V*, dim_F3 W=162,`
`Omega[(x,z),(x',z')]=z·x'-z'·x.`

This has a **nondegenerate** alternating symplectic form. Its finite Heisenberg group has `3^163` elements and (for a fixed nontrivial central character) the Schrödinger Hilbert-space irrep has dimension `3^81`, very different from 81.

Actual five W33 PSp transvections were computed on the integer 81 fundamental-cycle coordinate basis, yielding matrices A with A³=I. The block transformation

`(x,z)→(Ax,A^{-T}z)`,

where `A^{-T}=(A²)^T mod 3`, preserves Omega **exactly**. Also the prior cycle Gram G satisfies A^T G A=G mod3; all 5 tests passed. Direct 3×3 qutrit Weyl matrices validate `Z X=omega X Z` and `X^a Z^b X^c Z^d=omega^{bc} X^{a+c} Z^{b+d}` with maximum tested floating residual ≈1.3e-15.

A **single-qutrit illustration**, *not* an 81-qutrit simulation, with independent electric/magnetic coefficients a=b=1 has an isolated ground-state gap exactly 2 sqrt3 (numerical eigenvalue checked). This numerical gap is parameter-selected and does NOT prove fault-tolerant hardware or a physical mass.

**Obstruction:** a canonical symplectic *algebra* does not supply a group-invariant, local many-body Hamiltonian. Local coordinates are spanning-tree/basis dependent and generic PSp transforms mix them. Any proposed interacting qutrit H must explicitly resolve locality, commutation with PSp, Gauss constraints and time evolution.

## 5. Physical scale and hierarchy firewall

The previous exact one/two-star geometric quadratic operators yield **positive nonzero** eigenvalues in the closed rational range

`9/20 ≤ lambda_i ≤ 9/10`.

Consequently the **largest to smallest nonzero eigenvalue ratio across every one- or two-star selector is at most 2**, and actual pair-type ratios are <=2. With one arbitrary overall coupling scale C, the eigenvalues of `H=C Q` become `C lambda_i`; W33 geometry does **not** fix C in eV or GeV. A single pair-star defect thus cannot produce widely hierarchical nonzero **mass-squared ratios** without mixing other operators, exact zeros, baseline subtraction/tuning, or additional physics. No Standard Model mass fit is claimed.

Textbook dimensional transmutation illustrates the absent datum. **If** someone additionally postulates `beta(g)=dg/d ln mu = -b g³`, then

`Lambda/mu0=exp[-1/(2b g(mu0)²)]`.

Neither the beta coefficient b, nor bare coupling g(mu0), nor reference scale mu0 is fixed by the W33 graph. Holding g0=1, b=1/20 gives ~4.54e-5 while b=1/10 gives ~6.74e-3: a >100-fold shift from freely varied input. The older Pass11313–11319 already explores radiative models, so this is explicitly a **non-identifiability control**, not an original RG derivation.

## What was accomplished vs what remains a TOE

**Exact proven mathematical results:** character averages and invariant dimensions; full symmetry-breaking mean-field coexistence inequalities; analytic heat-kernel limit of one natural graph sequence; finite Heisenberg/PSp covariance; exact rational two-star hierarchy bound. Conditional numeric results: focusing variational localizations and one-qutrit Hamiltonian control. No physics measured.

**Still missing:** a physically derived action principle and nonlinear quartic, a continuum local Lorentzian limit, a canonical E8-compatible bracket with Jacobi, an invariant local many-body Hamiltonian, an objective running coupling / physical scale and independent quantitative predictions.

These deficiencies are *selection rules for future research*, not reasons to call finite mathematical results an experimentally demonstrated TOE.

### Reproducers and tests

- `analysis/w33_20261009_toe21_dynamical_selector_bifurcation.py`
- `analysis/w33_20261009_toe21_qfamily_heat_nogo.py`
- `analysis/w33_20261009_toe21_steinberg_cubic_invariants.py`
- `analysis/w33_20261009_toe21_doubled_qutrit_heisenberg.py`
- `analysis/w33_20261009_toe21_mass_scale_firewall.py`
- `tests/test_w33_20261009_toe21_five_theory_fronts.py`
- matching five `data/w33_20261009_toe21_*.json` certificates.
