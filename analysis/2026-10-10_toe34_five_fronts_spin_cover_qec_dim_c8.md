# TOE Round 34 — fault-injected GHZ/CZ extraction, p13 near-cover and local repair, faithful spinorial double cover, scaling spectra, and measured cQED tradeoffs

**Date:** 10 October 2026
**Repository:** wilcompute/W33-Theory
**Research boundary:** Five independent steps requested after Round33. This report separates finite exact algebra, numerical simulation, optimization without proof, and physical literature. No claimed gravitational field equations, experimental universal photonic machine, standard-model phenomenology or circuit-level fault-tolerance threshold.

## Source/parallel review

Previously established by repository code:
- Native W33 [[160,1,8]]_3 CSS code, 80 Wilson Z checks of weight8 and 79 Gauss X checks of weight4.
- Round28: sequential ancilla SUM readout (956 gates/round), noisy Pauli simulation, correlated high-weight hooks.
- Round30: 3,347 two-qutrit gates/round for postselected GHZ/CZ verified-cat checks, exhaustive accepted single gate-Pauli fault experiment under ideal verifier and measurement.
- Round33: time-correlated greedy joint decoder (phenomenological), exact connected degree17 W33 girth10 cover and finite 1,360-vertex Laplacian, degree13 CP-SAT UNKNOWN, cyclic-cover girth Moore bounds.
- Parallel Pass11844–11848: faithful bosonic A6 Lorentz has su5 centralizer in E8, discrete hypercharge adds SM algebra su3+su2+u1, central-Z3-extended translations lower commutant to su3+su2. Round33 exact combined-group intersection proved in that specific lift.
- Parallel Pass11849–11853 was a **reserved research packet at the beginning of this pass**, not yet an established fully documented calculation. If published later, its claims should be compared before attributing priority.

## 1. Full 159-check verified-cat CZ multi-round syndrome extraction with stochastic gate Pauli faults

Producer: `analysis/w33_20261010_toe34_verified_cat_multiround_circuit.py`. Certificate: `data/w33_20261010_toe34_verified_cat_multiround_circuit.json`.

Build the complete 80 Wilson and 79 Gauss Shor-style circuits. Each check has GHZ root |+>, w−1 leaves |0>, w−1 SUM fanout, w−1 independent verifier ancillas with two SUM each to interrogate Z_root Z_leaf^(-1), then w transversal CZ^(h_j) cat_j–data_j gates followed by w cat X-basis readouts. Native Gauss X checks are measured by ideal local Fourier basis changes. Inject independent uniform Pauli faults from the 80 nonidentity two-qutrit Pauli operators **after each fanout, verifier, and data CZ gate**. Inject ternary noisy verifier outcomes and final cat X-basis readouts, and retry rejected cats before coupling them to data. Apply F3 Pauli propagation through all SUM/CZ layers, carrying the actual 160-link data error frame through all 159 sequential checks in each of three repeated rounds.

Baseline tests with zero injected faults yield zero failed recoveries, validating ideal input/output calibrations in this model. At gate Pauli probability 0.0001, noisy verifier report 0.001 and per-cat-X readout flip 0.001, on 60 independent seeded three-round trials: **44/60** raw-final-only recovery failures versus **6/60** Round33 joint time-decoder failures; ideal final-state syndrome **0/60**. At 0.0004, verifier report0.003 and cat readout0.003: raw **58/60**, time decoder **20/60**, ideal **0/60**. Baseline zero noise is 0/60 for all three.

The probability model is NOT complete device-level noise. Initial cat |+>,|0> preparations, Fourier rotations, correlated environment, coherent leakage, detector latency and failed-cat retry time are idealized. The joint decoder is greedy rather than optimal, and rejection is postselection before data coupling. These 60-trial simulations do not prove fault-tolerance or thresholds; they demonstrate a concrete substantial suppression of circuit-sourced Pauli/readout failures conditional on assumptions. p_gate denotes per **two-qutrit gate** fault probability; p_verifier and p_final are per individual ternary measurement outcomes.

## 2. p=13 cover: two remaining forbidden eight-cycles, then exact local-repair searches

Producer: `analysis/w33_20261010_toe34_p13_breakout_voltage.py`. Certificate: `data/w33_20261010_toe34_p13_breakout_voltage.json`. Additional complete CP-SAT model and local-repair certificate: `analysis/w33_20261010_toe34_p13_local_exact_repair.py`, `data/w33_20261010_toe34_p13_local_exact_repair.json`.

The W33 Levi graph has 80 vertices, 160 incidence edges and exactly 1,620 native eight-cycle signed voltage constraints. Round31 achieved degree17 with all 1,620 constraints nonzero; Round32 degree13 best was eight failures, Round33 full global 81-chord CP-SAT was UNKNOWN. Here a 45,000-update, fixed-seed, weighted breakout/multiplicative clause-rescaling search over all 160 mod13 edge voltages **improves degree13's best residual to exactly TWO bad eight-cycle holonomies**. Freeze all 160 integers for independent verification. Two is **not zero**: NO girth10 certificate or quantum code distance10 at p13 is claimed.

Around the 15 edge variables directly on those two failed cycles, formulate a new exact CP-SAT problem, preserving all 1,620 holonomy disequalities while holding other voltages fixed. Broader locally coupled neighborhoods of 28, 48 and72 candidate variables are also explored. Each local solver infeasibility proves only that THAT particular frozen complement admits no correction, not that globally p13 cannot work. The final local-repair ledger records exact FEASIBLE/INFEASIBLE/UNKNOWN outcomes.

If a fully checked assignment with all 1,620 nonzero holonomies and connected p13 lift is eventually found, its HGP would have n=(2080)^2+(1039)^2=**5,405,921**, k=(1041)^2=**1,083,681**, code distance ≥10 by verified cover girth. Do not report this as an existing code without the actual witness and girth check. Current validated girth10 construction remains p17 [[9245281,1852321,10]]_3.

## 3. Genuine spinorial SL(2,9) central double cover, exact Clifford computation

Producer: `analysis/w33_20261010_toe34_spin_sl29_exact_clifford.py`; certificate `data/w33_20261010_toe34_spin_sl29_exact_clifford.json`.

Previous parallel finite Lorentz lift acts only through bosonic A6 of order360; to model spinorial actions we must use its nontrivial central extension 2.A6=SL2(F9), order720. The standard permutation A6 inside SO6 lifts to Spin6 through normalized roots `r_ij=(e_i−e_j)/√2` in real Euclidean Clifford algebra `Cl6`. Implement exact rational basis-mask multiplication of `lift(ijk)=r_ij r_jk` for (0,1,2), (0,1,3), (0,1,4), (0,1,5). The irrational normalizations CANCEL pairwise, giving rational Clifford coefficients. Exhaustively close the four generators and prove exactly **720 distinct even Clifford elements**, each generator of order3. Exactly the scalar identities **+1 and −1** are present. The map down to permutation A6 has 360 elements. This is a genuine central spin lift, not merely a projective label.

Spin(6)≅SU4 has complex chiral half-spin dimension4, on which central −1 acts as −I4. The block-diagonal `4_spin ⊕1` is a faithful five-dimensional unitary determinant-one representation in SU5. The maximal-rank SU5_L×SU5_G subgroup of compact E8 supplies a candidate structural embedding for spinorial finite Lorentz inside SU5_L while SU5_G commutes.

**Limits:** No independent 248×248 E8 matrix representation, complete centralizer, chirality/generation calculation, compatible semidirect action of Z3.M translations, fermion spin-statistics or experimentally predictive matter interactions is yet computed. In particular, the new SL2(9) lift must not be silently equated with the parallel Tits bosonic A6 realization. ATLAS separately catalogs characteristic-zero 4D spin representations for 2.A6: https://brauer.maths.qmul.ac.uk/Atlas/v3/alt/A6/ .

## 4. Controlled cover-size and hopping-weight variations: spectral dimension still not robust

Producer: `analysis/w33_20261010_toe34_weighted_cover_dimensional_scaling.py`; certificate `data/w33_20261010_toe34_weighted_cover_dimensional_scaling.json`.

Diagonalize the FULL weighted Laplacians using cyclic Bloch reduction to 80×80 Hermitian matrices per deck momentum: native p1 (80 points), connected p17 (1360), p17 with alternating positive edge weights 0.8/1.2, p17 with weights 0.5/1.5, and the explicit p83 girth10 cover (6640). In each case require the unique zero Laplacian mode, positive gap, and evaluate running spectral dimension from heat-trace eigenvalue sums with 240 logarithmic time samples. Define a dimension plateau as a sustained >= one decade of diffusion time with running d_s within ±0.25 of 3 or4.

Full spectrum first nonzero gaps are approximately 1.550510, 0.671941, 0.634253, 0.509969, 0.129273 for the five scenarios. None shows a one-decade d_s≈3 or d_s≈4 plateau; longest near3 ratios are 1.53,1.47,1.41,1.36,1.47. Enlarging p can shrink the finite spectral gap but still does not produce a stable continuum spectral dimension in this tested family. Edge weights were externally selected toy couplings, **not** dynamically ordered by an energy minimization. A larger thermodynamic sequence, interacting fields and coarse graining remain open.

## 5. Concrete cQED engineering architecture: bosonic storage cavity+flux-tunable transmon

Producer `analysis/w33_20261010_toe34_c8_specific_cavity_transmon_tradeoff.py`; certificate `data/w33_20261010_toe34_c8_specific_cavity_transmon_tradeoff.json`.

Choose a proposed engineering architecture: eight high-Q storage cavities with one flux-tunable transmon nonlinear element per site and eight externally tunable coherent links forming a C8 ring. This is a **design**, not an actual fabricated 8-site machine. Separate published component measurements:

- A 2024 bosonic cQED experiment achieved **average cavity energy lifetime ~200 μs** with nanosecond transmon tuning and reported cavity–transmon coupling `g/2π=6.65MHz`, https://www.nature.com/articles/s41467-024-50201-7 .
- A different 2018 tunably coupled two-transmon device reported **15–40μs transmon T1**, https://www.nature.com/articles/s41534-018-0088-9 .
- A 2020 superconducting Bose-Hubbard paper describes an indicative **transmon anharmonicity near −250MHz**, https://www.nature.com/articles/s41534-020-0269-1 . This number is an example and NOT measured for the 2024 cavity/transmon system.

Hypothetical dispersive-participation calculation: if transmon energy participation is r, inherited storage Kerr scales as `K_eff≈250MHz·r²`, while independent exponential energy loss is `1/T_eff≈(1−r)/200μs+r/T1_transmon`. To obtain the desired `|K_eff|=160MHz` needs `r≥sqrt(160/250)=0.8`, a huge nonlinear-element admixture invalidating far-detuned perturbative approximations. To retain >=50% no-loss TWO-particle survival at 60μs needs `T_eff≥120/ln2=173.12μs`, forcing `r` close to zero for 15–100μs transmon lifetimes. For reference T1_transmon=15,40,100μs, the maximum inherited Kerr compatible with survival in this toy mixing model is only **0.040, 0.377, 6.025MHz**, respectively—far below 160.

This is an explicit **conditional engineering conflict** for simple dispersive Kerr inheritance, not an absolute no-go for all parametric couplers, high-order nonlinear oscillators, direct transmon nonlinear states, distinct fixed microwave cavities, or shortened interrogation protocols. No physical experiment has been commissioned or device numbers measured here.

## Scientific verdict

The strongest constructive result is the exact **720-element Clifford spinorial double cover**, a demonstrably faithful candidate distinct from the parallel 360-element bosonic Lorentz lift. The most actionable computational result is a three-round circuit-level qutrit noisy-readout improvement, while the degree13 cover search reaches TWO unremoved constraints without falsifying degree13 feasibility. The physical controls are restrictive: size/weight alone did not yield stable dimension, and naive Kerr inheritance fails the required lifetime-bandwidth tradeoff under clearly labeled assumptions. No observed Standard Model generations, Lorentzian gravity, particle masses or universal quantum hardware follow.

The report's source code, certificates and tests are reproducible from the current repo. Avoid unrelated dirty files and integrate parallel commits before publication.
