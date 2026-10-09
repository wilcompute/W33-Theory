# 2026-10-09 — Five independent TOE fronts: stronger Ritz bound, heterotic Wilson equivalence, T-odd deformation, eighth-moment photonics, spatial-lift falsification

**Ritz erratum (2026-10-09):** Previous five/seven/nine-state floating Hermite current blocks used an incorrect line-side momentum-covariance/derivative sign; those figures are NOT certified upper bounds for the actual Hamiltonian. The independently rationally certified corrected eleven-state bound is **`E0 < 127.595507`**. See [follow-up analysis](2026-10-09_five_more_toe_frontiers.md) and Pass11786. This correction does not invalidate separately verified heterotic, optical or graph calculations.

**Verdict:** Five executed mathematical/computational probes, several new quantitative constraints. None establishes a Standard Model vacuum, a physical mass gap, a 160-current photonic processor, or spontaneous selection of 3+1-dimensional spacetime. Parallel Passes11778–11785 own the existing qualitative compact-resolvent/attained-vacuum/gap theorem; this packet does not rediscover it.

## A. Nine-state collective-Hermite Ritz upper bound

Extend the verified point/line seven-state trial in `w33_20261008_7state_ritz.py` with two independent normalized collective He8 vectors; each degree-n sum has squared norm `N_n = 40(1+12/3^n+27/9^n)` for even n. Different Hermite chaos orders are exactly orthogonal and the point/line 15-mode sectors are independent. The fixed W33 incidence pair types reduce the squared-current quadratic form to four-variate Gaussian polynomial expectations. Products with He8 have polynomial degree at most 20; 11-node and 12-node tensor Gauss–Hermite are both degree-exact in ideal arithmetic.

- Earlier seven-state upper bound: `E0 <= 127.61920315299878`.
- New nine-state upper bound: **`E0 <= 127.595518296517`** (floating quadrature precision, not outward-rounded interval).
- Improvement: `0.02368485648`; maximum quadrature block discrepancy: `5.69e-13`.
- First two **Ritz** energies: `127.5955183`, `142.6418446`. Their difference is **not** an upper or lower certificate on the exact excitation gap. By min–max, each Ritz eigenvalue bounds an ordered exact eigenvalue from above, with possible ground-sector degeneracy.
- The calculation gives no numerical lower bound for the full 78-coordinate Schrödinger operator. The previous compactness proof is qualitative. This remains the central uncompleted part of the original numeric-gap request.

Producer `analysis/w33_20261009_9state_ritz.py` is generated deterministically from the committed seven-state producer by `analysis/w33_20261009_generate_9state_ritz.py`. Output JSON in `data/w33_20261009_9state_ritz.json`.

## B. Exact T-odd current-curvature form bound

Let `h[psi] = sum_e ||J_e psi||²` be the closed nonnegative quadratic form of the proposed Hamiltonian, and define the Hermitian form `c_(e,f)[psi] = i(<J_e psi,J_f psi>-<J_f psi,J_e psi>)` for two edges. By Cauchy–Schwarz,

```
|c_(e,f)[psi]| <= 2||J_e psi|| ||J_f psi||
                 <= ||J_e psi||² + ||J_f psi||² <= h[psi].
```

Thus for real `|eps|<1`, `h_eps=h+eps*c` is a closed positive form with

```
(1-|eps|)*h <= h_eps <= (1+|eps|)*h.
```

It has the **same form domain**, remains compactly embedded as long as the Pass11778 compactness theorem applies, and its ordered eigenvalues obey `(1-|eps|)E_j(0) <= E_j(eps) <= (1+|eps|)E_j(0)`. The dressed antiunitary fixes all currents but reverses `i`, giving `T H(eps) T^-1=H(-eps)`; hence each ordered eigenvalue is even in eps. For a nondegenerate ground ray its first derivative at eps=0 vanishes. A degenerate ground eigenspace can instead split linearly in opposite epsilon directions, so no unproved differentiability or Kramers theorem is asserted. A 2x2 exact SymPy control verifies the factorization `H ± C = (J1 ∓ i J2)(J1 ± i J2)` for this pair and checks spectral reflection.

**New:** a rigorous stability band for `T`-odd curvature perturbations of the full model, rather than a claim that the zero-curvature selection rule forbids breaking in every state. It does **not** determine full ground multiplicity or spontaneous breaking at infinite volume.

## C. Optical fourth-cumulant estimator: eighth-moment correction

The prior single-edge quartic gate is represented by `U=e^{-i theta(X+alpha)^2(P_Y+alpha)^2}`, `alpha=1/sqrt39`. For two independent Gaussian modes conditioned on `Z=P_Y+alpha`, `P_X` has conditional mean `-2 theta alpha Z²` and variance `Var(P_X)_input +4 theta² Var(X)_input Z^4`. Pure optical loss multiplies the conditional mean by `sqrt(eta)`, the excess conditional variance by eta, and adds a vacuum variance `(1-eta)/2`; independent Gaussian electronic noise adds its calibrated variance.

The exact distribution has heavy tails. By rational eighth-moment evaluation, the influence-function asymptotic variance of plug-in *excess kurtosis* at the ideal tau=1/20, eta=1, vacuum input is `514.3503040`, not the **Gaussian-null 24**. Thus, under an alternative-based approximate 5-sigma standard-error criterion,

```
N_optimistic_gaussian_null ~= 3,978
N_alternative_asymptotic  ~= 85,260
```

This corrects the earlier optimistic photonic shot estimates by a factor of 21.43, for this measurement regime. This is **still not a finite-N power guarantee** and does not model a gate synthesis, experimental shot correlations or variance drift.

Example pure squeezed input `Var(X)=1/4, Var(P_X)=1`, `Var(P_Y)=1/2`, electronics variance 1/100 gives the following alternative-aware heuristic at tau=1/20: eta=1: ~841,233; eta=1/4: ~24,883,738; eta=1/25: ~17,288,872,984 samples. This squeezing is one illustrative choice, not an optimized resource.

A Gaussian mixture of time-varying shot variance `v` can itself generate `kappa4=3 Var(v)` at zero mean; a high-significance kurtosis observation without drift calibration is insufficient evidence of the quartic interaction. Producer `analysis/w33_20261009_optical_eighth_moment_power.py`.
## D. Full Wilson-line benchmark screening — necessary gauges, not universal equivalence

The earlier fixed-shift sieve left only the W33 Z6-II base `Z6II_34`, whose 15 Standard Model entries now have their complete original eight-row orbifolder gauge embeddings recovered from `~/orb/scan/cp2/out/*.model`. All 15 were frozen with source SHA-256 hashes in `data/w33_20261009_heterotic_full_models_15.json`. The original 215-model charge ledger and 29 base-shift fixture remain separate inputs, not overwritten.

Literature (external): Lebedev et al., *The Heterotic Road to the MSSM with R parity*, Phys. Rev. D 77 046013 (2008), https://arxiv.org/abs/0708.2691, appendices E.1 and F.1. The identical gauge shift of both benchmark models is `(1/3,-1/2,-1/2,0,0,0,0,0) (1/2,-1/6,-1/2,-1/2,-1/2,-1/2,-1/2,1/2)`; their W2 and W3 embeddings differ.

Three independent exact-arithmetic tests:

| Tested necessary condition | Benchmark 1 | Benchmark 2 |
| --- | ---: | ---: |
| Unbroken-root counts match both E8 factors | 3 W33 models | 0 |
| Full joint root-phase distributions match with *fixed* V,W2,W3 | 0 | 0 |
| Allow 48 declared generator sign/shift choices per W33 model | **1** | **0** |

The W33 three root-count matches are `Z6II_34__SM_20260917_1558`, `...2068`, `...292`. The only survivor after the 48 declared transformations is **`...1558`**. The tested transformations are V↦±V, W2↦±W2+3aV for a=0,1, and W3↦±W3+2bV for b=0,1,2. The joint histogram tallies the triples of all 240 root phases separately in each E8, admitting exchange of the factors. It is invariant under E8 Weyl permutations of roots and root-lattice shifts.

**Important firewall:** Those 48 transforms are not an exhaustive Z6-II space-group automorphism search, nor are all hypercharge, matter and singlet maps compared. No model equivalence or inequivalence is claimed outside this tested orbit. Passing a histogram is merely necessary, not sufficient; the selected W33 matter-even D-flat no-go cannot be transferred to a published external mini-landscape benchmark without model identification.

Producers: `analysis/w33_20261009_heterotic_benchmark_full_roots.py`, `analysis/w33_20261009_joint_root_phase_sieve.py`, `analysis/w33_20261009_wilson_generator_phase_orbit.py`, with source fixture `analysis/w33_20261009_freeze_heterotic_full_models_15.py`.

## E. W33 internal finite geometry does not select the spatial dimension

The native W33 Levi incidence graph is connected, 4-regular, has 80 vertices and Laplacian spectrum `0^1, (4-sqrt6)^24, 4^30, (4+sqrt6)^24, 8^1`. To test whether a continuum can arise by adding translations, define the **explicitly supplied** Cartesian product family `G_d = Levi(W33) square Z^d`. Its on-diagonal continuous-time heat kernel obeys

```
P_d(t) = [1 + 24 exp(-(4-sqrt6)t) +30 exp(-4t)
          +24 exp(-(4+sqrt6)t)+exp(-8t)]/80
         * [exp(-2t) I0(2t)]^d .
```

The running spectral dimension `d_s(t)=-2 d log P_d(t)/d log t` tends to the **supplied integer d**, as the native W33 internal modes equilibrate. Numerical checks at t=500 give `d_s≈1.00025,2.00050,3.00075,4.00100` for d=1..4. Finite W33 supplies the cell and internal spectrum but **does not select d=3**; propagation velocities also depend on added spatial kinetic couplings. This is a specific negative test of a tempting "W33 automatically gives 3D space" inference, not a no-go for *all* possible emergent W33 spacetime constructions. A dynamically selected family with testable geometry is still required.

Producer: `analysis/w33_20261009_spatial_product_spectral_dimension.py`.

## Source integrity and open tests

- Exact model fixtures are verbatim rational gauge vectors extracted from original orbifolder outputs; preserve source raw SHA-256 metadata and the original ledger.
- The proof of compact resolvent and the qualitative positive gap are from parallel Pass11778. Only the nine-state **upper** estimate and perturbative spectral enclosures are added here.
- Full antiunitary normalizer classification, ground-sector multiplicity and physical CP map remain open.
- A full Wilson-line gauge automorphism and selection-rule equivalence test remains open. Compare actual orbit representatives, not only invariants.
- Real photon implementations, drift-robust finite-sample tests, and Einstein/spacetime predictions remain open.

All five fronts have small reproducible producers; `tests/test_w33_20261009_five_frontiers.py` exercises nine-state quadrature, exact perturbation controls, rational eighth moments, full heterotic root and phase classes, and the arbitrary-dimensional product-family heat kernel.
