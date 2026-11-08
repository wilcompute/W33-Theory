# Five deeper W33 fronts: actual E6 mass fibers, weighted clocks, Hodge currents, historical provenance and optical netlist

**Research date: November 8, 2026.** Source: analysis/w33_20261108_deep_fivefronts.py. Regression suite: tests/test_w33_20261108_deep_fivefronts.py. Workflow: .github/workflows/w33_20261108_deep_fivefronts.yml. Generated desktop certificate: data/w33_20261108_deep_fivefronts.json.

**Claim boundary:** Every result here is finite mathematics, a source-conditioned obstruction, a numerical verification, a historical audit, or a synthetic optical control. None establishes a measured physical constant, a three-generation E6 vacuum, a local Lorentzian continuum, an observed photon, or a built optical chip.

## Front 1 — E6: 729 native 3-by-3 blocks, each rank at most two

The signed E6 mass operator already owned by the prior D-flat construction is an 81-by-81 matrix obtained by contracting **1,620 repository tensor records** with a complex field on C^27 tensor C^3. This pass reconstructed those records directly, instead of treating the earlier four-state Nelson–Barr toy as a genuine E6 embedding.

For any fixed pair of E6 indices i,j, the matrix with qutrit indices alpha,beta is alternating. This follows from the symmetric E6 cubic tensor and antisymmetric SL3 epsilon; hence any **direct 3-by-3 fiber-to-fiber mass block has determinant zero and rank at most two** for every scalar field. All 27×27=729 blocks were checked with a deterministic complex field: 270 rank two, 459 rank zero, maximum skew residual zero.

The actual 78 E6 generator matrices from artifacts/e6_27rep_basis_export/E6_basis_78.npy were also used. For each of the 27 direct coordinate-triplet projectors P_i=|i><i| tensor I3, a positive commutator norm with at least one E6 generator was verified. No such projector preserves the *full unbroken E6*. This accords with irreducibility of its fundamental 27 and Schur's lemma. It does **not** exclude mixed projectors after spontaneous symmetry breaking, additional scalar operators, or new vectorlike states; no Standard Model generation assignment is derived.

Previous owners: analysis/w33_20261001_dflat_cartan_mass_loop.py, analysis/w33_pass11218_e8_cubic_cartan_kernel.py and analysis/w33_pass11261_g26_cartan_coordinate_map.py. External representation context: https://www.osti.gov/servlets/purl/2420456 and https://doi.org/10.1140/epjc/s10052-025-15043-7. Nelson–Barr actual loop quality: https://link.springer.com/article/10.1007/JHEP07%282021%29203.

## Front 2 — Escape the higher-q flat-mixing no-go at a cost

The previous theorem excludes uniform mixing at *all times* for the **unweighted null-graph adjacency** family at odd prime powers q>=5. This pass constructs a different, explicitly weighted Hamiltonian over **odd prime** p in 3,5,7,11. Its translation/Fourier momentum eigenvalue is the integer representative in {0,...,p-1} of the finite quadratic form q(k)=k0*k2-k1² mod p. The Hamiltonian is real symmetric, with a nonlocal convolution kernel.

At t=2*pi/p, its unitary is the inverse finite Fourier transform of exp(-2*pi*i*q(k)/p). Completing the square and applying the nondegenerate quadratic Gauss-sum identity proves that **every one of the p^6 input/output transition probabilities equals 1/p^3 exactly**. All four cases passed independent numerical FFT checks near machine precision.

| p | Modes | Native null displacement types | Nonzero weighted off-diagonal types | Weighted types outside null cone |
|---|---:|---:|---:|---:|
| 3 | 27 | 8 | 26 | 18 |
| 5 | 125 | 24 | 100 | 84 |
| 7 | 343 | 48 | 342 | 294 |
| 11 | 1331 | 120 | 1330 | 1210 |

This does **not contradict** the null-only no-go. It reveals the price of the escape: most weighted couplings are non-null, often nearly all pairs. The folded integer momentum dispersion is not a controlled local relativistic continuum. Bounded-range weighted Hamiltonians remain a falsifiable open direction.

## Front 3 — Hodge matter-current selector and a new 23/54 identity

Reconstruct the 27-vertex, 108-edge, 36-triangle complex. Its incidence matrices obey B1 B2=0 and B2^T B2=3I36. The real harmonic projector is

P_H = I108 - B1^T (B1 B1^T)^+ B1 - (1/3) B2 B2^T.

The result is a rank-46 orthogonal projector, annihilated by both B1 and B2^T. The 108 diagonal entries are equal by edge transitivity and their sum is the projector trace. Therefore

**(P_H)ee = ||P_H e||² = 46/108 = 23/54** for every oriented edge e.

A vertex-charge gradient J=B1^T rho has zero overlap with H1. So does a contractible triangular face boundary. A divergence-free cycle source obtained by projecting an edge away from gradients has a nonzero harmonic component of exactly 23/54 squared norm.

This is a physically useful source-selection obstruction, not the discovery of 46 photons or the electromagnetic coupling. A light, propagating, uniquely normalized gauge sector still requires matter representations, a Lorentzian action, dynamics and a chosen vacuum.

## Front 4 — Actual historical pickaxe rather than a misleading current-file date

The authorized desktop ran bounded, rename-following Git pickaxe queries using complete local repository history. Five literal/file-history investigations were recorded:

| Literal | File | Earliest count-changing commit along that file's history |
|---|---|---|
| 137+1/28+4/14045 | 2026-11-07 constants catalog | 0e87357a, Nov 7 |
| 137+880/24445 | same catalog | 0e87357a, Nov 7 |
| 3/13+1/2200 | same catalog | 0e87357a, Nov 7 |
| Nelson | Forty Points physics TeX | cf3e9386, Oct 17 |
| Weber | Forty Points physics TeX | dbe3a411, Oct 12 |

The first two alpha strings had two count-changing commits in that source (the later one is a7132f9), the weak-angle string one, the Nelson text four and the Weber text five.

**These are not the original dates on which the formulas were discovered.** The constants catalog is explicitly retrospective. File-scoped literal history does not traverse all older files, conceptual equivalents, deleted branches, TeX syntactic variants or physical scheme definitions. The program refuses to claim historical priority from a shallow GitHub Actions checkout. A separate regression creates a real tiny Git repository and verifies the first literal-introduction query.

## Front 5 — Full 27-port logical netlist and synthetic calibration

The simulation creates four complete 27-port reversible routing maps, followed by the exact three local qutrit chirp/Fourier layers:

1. c <- c+2a, modulo three.
2. a <- a+2c, using updated c.
3. Apply H+ on one qutrit, H- on each of the other two, as 27 disjoint 3-port-gate instances across the three layers.
4. Undo the second SUM with a <- a+c, then undo the first with c <- c+a.

All 27 input/output mode indices are explicitly enumerated. There are **27 tritters, four 27-port permutation schedules** and an upper bound of **81 internal two-mode beam-splitter interactions** if each arbitrary tritter is decomposed into three; generic 27-port unitary meshes require up to 351 such interactions. These counts **exclude physical routing**, crossings, waveguide path length, losses and phase stabilization. The composed 27x27 unitary matches the exact quadratic W33 clock with residual 2.24e-16.

A deterministic detector calibration fixture includes distinct mode efficiencies, 0.5% cyclic neighbor crosstalk, and 5000 synthetic accepted counts for one input. Before correction, its probabilities depart from the uniform ideal by about 0.0011683 at worst; inverting the *perfectly known synthetic* calibration recovers the ideal to numerical precision. Real independent calibration uncertainty is not simulated. The phase-plaquette tests require interferometry: a flat intensity matrix is insufficient.

Interferometer prior art: https://github.com/clementsw/interferometer ; integrated tritter: https://www.nature.com/articles/ncomms2616 .

## Verification and scientific interpretation

The initial desktop source execution passed all five gates and wrote its full JSON; a suite of focused tests and an independent GitHub Actions workflow cover native E6 records, prime-field FFT construction, source-current Hodge response, toy Git history, 27-port netlist and loss/crosstalk correction. The GitHub run's current outcome should be checked before saying it passed.

The actual **positive mathematical results** are: an exact higher-prime Gaussian flat transform with demonstrably non-null interactions; a uniform Hodge edge leverage 23/54; and a complete synthetic optical port schedule. The strongest **negative result** is the rank-two ceiling on every direct E6 qutrit-fiber mass block. Physical particle assignments, locality, symmetry-breaking, strong CP radiative corrections and laboratory measurements remain open.

## Top five independent following experiments

1. Determine a symmetry-broken E6 projection mixing the 27 coordinates, and test its genuine Standard Model quantum numbers, Yukawa masses and loop-induced strong CP phase.
2. Optimize strictly bounded-range weighted finite light-cone Hamiltonians and test analytically for flat mixing versus the explicit nonlocal Gaussian control.
3. Specify a normalized gauge-matter kinetic operator on the 46-dimensional Hodge space and test unique long-lived modes against gradients and nontrivial cycles.
4. Create a rename-aware cross-file mathematical provenance graph, with original theorem witnesses, RG schemes, physical units and pre-registered holdouts.
5. Map the 27-port logical netlist onto a specific photonic process/design-rule geometry and characterize the real phase, insertion-loss and crosstalk budgets.
