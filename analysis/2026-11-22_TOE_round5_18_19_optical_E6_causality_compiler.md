# TOE round five — constructive 18/19-effect Witting POVMs, exact E6 leakage, spinor selection, Lorentzian nulls, and exhaustive fourth-stage compiler

Research date: **22 November 2026**. The repository is an exploratory mathematical/physical hypothesis workbench. The outcomes below are verified finite algebra, explicitly scoped numerical calculations, or negative controls. Nothing below constitutes a Standard Model derivation, quantum gravity, photonic hardware measurement, or a Theory of Everything.

## Source provenance and independently surveyed prior art

Built on earlier W33-Theory `analysis/toe_20261122_fourth_hessian_census.py`, `analysis/toe_20261122_e6_132_constructive_embedding.py`, `analysis/toe_20261122_e6_higgs_cubic_mass_lift.py`, `analysis/toe_20261122_photonic_sparse_isometry_loss.py`, and associated previous reports/tests. Pre-existing fourth-stage **153,160,632** count and 132-dimensional E6 carrier **are not newly claimed**. Recent parallel commits were inspected before authoring. The independently observed **18- and 19-outcome Witting-supported IC POVMs** are new *relative to these prior repo reports*, not an unqualified claim of first discovery in all published literature.

Context literature: E6 representation branchings 78 = 45_0+16_-3+16bar_3+1_0 and 27=16_1+10_-2+1_4 are standard, as discussed at https://www.mdpi.com/2571-712X/6/1/8 and in the E6 trinification literature https://inspirehep.net/files/4bd2ad587c4c9313ea9faa3f62dead1a . The causal-set ordering fraction/Myrheim–Meyer estimator and interval counting predate this project: https://doi.org/10.1007/s41114-019-0023-1 . For the kinetic null, Aldous' conjecture was proved by Caputo, Liggett and Richthammer: https://arxiv.org/abs/0906.1238 . These are prior art, not our theorems.

## Frontier 1 — exact full-stage-4 fixed-alphabet compilation (new performance benchmark)

The prior exact result |H (DN)^4| = 236359 × 648 = **153160632** was rerun in integer-pair arithmetic over Z[omega]. `analysis/toe_20261122_round5_hessian_stage4_compiler.py` now performs a *full exhaustive three-target Haar comparison*, using 648 left H elements for each of 236359 exact coset representatives, with batched complex BLAS and independent best-word overlap checks. Errors (normalized projective Frobenius distance):

| Haar target | Exactly 3 phase flips, prior | Exactly 4 phase flips, this pass |
|---|---:|---:|
| 0 | 0.32833946 | 0.33640583 |
| 1 | 0.45381312 | 0.36384494 |
| 2 | 0.46534539 | 0.38757521 |

**Depth-parity caution:** exactly-four-D products need not contain exactly-three-D products. Optimize the *union* of allowed depths; never claim per-depth monotonicity. The separate 3-dimensional diagonal SU4 torus packing computation gives a deliberately weak rigorous no-uniform-epsilon bound for the 153M-element set; it does not imply polynomial-depth universal synthesis.

## Frontier 2 — the 51 E6 adjoint directions are algebraically necessary

For the Z3-graded E6 adjoint algebra, g0=sl3^3 (dimension 24), g1=3⊗3⊗3 (dimension 27), g2=3bar⊗3bar⊗3bar (dimension 27), elementary tensor bracket maps have **exact integer ranks 27 and 24**:

- wedge²(g1) -> g2: the antisymmetric triple epsilon contraction has rank 27;
- g1⊗g2 -> g0: traceless partial contractions have rank 24.

Therefore the 27-dimensional g1 piece that served as the neutral part of the constructed E6 carrier **generates all 78 adjoint directions under full E6 closure**. The extra 51 cannot be consistently deleted while demanding the full symmetry. No rate, amplitude, protection gap or physical evolution is inferred.

## Frontier 3 — singlet-only cubic Higgs selection rule and a conditional adjoint escape

The standard 27=16_1+10_-2+1_4 allows gauge-neutral E6 cubic sectors **16×16×10** and **10×10×1**, but excludes **16×16×1** by U1 charge and SO10 representation content. Consequently singlet-only VEVs in the E6 cubic cannot give quadratic masses to the 96 spinor chirals of three vectorlike 27+bar27 Higgs pairs; 32 complex Goldstone directions are gauged away, leaving **64 unlifted spinor directions** in that restricted model.

An algebraically allowed `bar27 * 78 * 27` Cartan deformation produces mass coefficient `m + lambda*a*q`. Setting `m=-4lambda*a` makes the singlet coefficient zero while giving `-3lambda*a` on 16 and `-6lambda*a` on 10. This is an **operator-level potential escape only**: the full 78-field F/D-flat equations, gauge Goldstones, chiral matter masses, and vacuum stability must be solved. Do not call it a successful E6 vacuum.

## Frontier 4 — actual Lorentzian partial-order benchmarks and geometric nulls

Uniform samples of (u,v) in [0,1]^2, ordered only when both lightcone coordinates increase, model 1+1 Minkowski causal diamonds. For n=40,80,160, 40 seeded sprinklings per size give ordering fractions around 1/2 and growing chain height. An all-to-all two-layer poset also has ordering fraction approaching **1/2**, but **every chain has at most two elements and all comparable pairs have empty interiors**. Hence the relation fraction alone does *not* establish Lorentzian dimension or geometry.

Separately, at n=40, 80 matched random orientations give W33 mean ordering fraction **~0.828** versus **~0.810** for random degree-12-regular graphs. This tells us the imposed total-order orientation of the undirected W33 graph fails a basic Minkowski-diamond null; no physical Lorentzian order or spin-two mode has been derived.

## Frontier 5 — an exact 18-effect Witting rank-one informationally complete POVM

Let zero-based Witting ray indices

- `A = {1,3,5,7,12,13,18,19,27,29,33,39}`;
- `B = {5,6,7,8,10,15,16,18,27,29,33,36}`.

Each has **12** rays and satisfies **sum_{j in A} P_j = sum_{j in B} P_j = 3I4** *exactly in Q(omega)*. The intersection has six rays, so their equal mixture yields **18 positive rank-one effects** with weight 1/3 on common rays and 1/6 elsewhere. The 18 projectors have rank **16** over six prime fields. This is an *upper bound* on Witting-supported IC rank-one POVM support, not a global minimality proof; 16 is the general d=4 lower bound.

The 18 effect measurement uses **62 adjacent two-mode QR couplers** in the implemented loss model, has **0.9513** pure-state detection probability, and gives calibrated source-photon Hilbert–Schmidt risk coefficient **51.57** (i.e. MSE≈51.57/N_launched).

## Frontier 6 — a 19-effect Pareto alternative and source-photon calibration

Two other 12-ray tight frames,

- `C={1,5,6,13,15,16,17,29,30,31,32,33}`;
- `D={1,3,5,7,12,13,18,19,27,29,33,39}`

intersect in five rays and yield an **exact 19-outcome IC** POVM. Each individually also sums to 3I4. Benchmark at equal mixture and a 0.5% illustrative intensity loss per hit:

| Design | Outputs | Adjacent QR couplers | Pure-state detection probability | Source-photon reconstruction risk coefficient |
|---|---:|---:|---:|---:|
| 18 effects | 18 | 62 | 0.9513 | 51.57 |
| **19 effects** | **19** | **66** | **0.9527** | **36.18** |
| prior 20 effects | 20 | 70 | 0.9405 | 53.15 |
| 30 effects | 30 | 110 | 0.9075 | 24.42 |
| 39 effects | 39 | 138 | 0.9001 | 21.59 |

The **19-effect dominates the earlier 20-effect design in all three metrics** on the single tested input with the chosen routing. Moreover, the *analytically Haar-averaged pure-state* launched-photon reconstruction risk coefficients are 43.35 (18), 36.48 (19), 52.26 (20), 25.29 (30) and 21.83 (39). This expectation follows exactly from E_Haar[rho]=I/4 and Tr(rho²)=1; it is not a Monte Carlo fit. These results are not a universal all-state Pareto proof. Loss is modeled with explicit physical POVM effects `E_j=A_row† A_row` and `E_no-click=I-A†A`, and dual-frame inversion includes clicks and no-clicks. All risk values are calculated per launched photon with an unbiased linear estimator under *perfectly known* loss calibration; they are not measured detector efficiencies.

Optimizing one continuous mixture weight for the fixed ordering and testing 81 seeded permutations gives a best observed **65-coupler** 19-outcome routing and **~35.86/N_launched** risk for that one state. This search is not globally optimal and omits polarization, phase drift, detector dark counts, input production, mode mismatch, and two-photon entanglement.

## Reproducibility and physical validity limits

Reproduce from repo root with:

```bash
OPENBLAS_NUM_THREADS=1 python -m pytest -q tests/test_toe_20261122_round5_sixfronts.py
```

Every analysis has `verify()` and writes a machine-readable `data/toe_20261122_round5_*.json` certificate when invoked as a standalone script. Continuous gates and physical propagation have not been validated. No energy/complexity advantage, general SU4 compiler, realistic E6 vacuum, Lorentzian quantum gravity, or actual experiment follows from these six bounded computations.

## Test and CI status on publication

The new isolated 17-test six-front regression passed locally. A separate attempt to run the entire archival `test_toe_20261122_*` selection exceeded the execution window after 57 earlier successful test reports; **no full-suite success is claimed**. The isolated GitHub Actions workflow should be checked for its own actual completion status.
