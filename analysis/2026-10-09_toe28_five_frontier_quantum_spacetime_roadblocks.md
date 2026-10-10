# TOE Round 28: noisy qutrit circuits, high-rate hypergraph-product codes, exceptional E8 branching, graph waves, and Ramsey pulse control

**Date:** 9 October 2026
**Repository:** `wilcompute/W33-Theory`
**Objective:** Execute all five independent next steps from Round27, cross-check against parallel commits and prior-art scripts, test, and publish only reproducible additions. No work on Holotrade was necessary for these W33-only results.

## Provenance and originality

Already established in the repository BEFORE this pass: the W33 Levi graph 80-vertex/160-edge incidence carrier; generalized W(3,q) cell counts and Steinberg H1; exact [[160,1,8]]_3 with 79 Gauss-X and 80 eight-link Wilson-Z generators (Round26); perfect-syndrome ternary radius-three decoder and associated data-only Monte Carlo (Round27); 45 E6 tritangent sectors and symmetry-permitted A2 coupling; the SL9 reducible-carrier E8 obstruction (Round27); normalized graph heat spectral-dimension no-go; and exact 36-state C8 doublon spectrum plus disorder audit (Round26/27).

**New in this pass:** explicit qutrit SUM-gate fault propagation and a non-fault-tolerant circuit benchmark; sparse stabilizer instances and rates of W(3,q)-derived hypergraph-product quantum codes; concrete necessary host sectors for Steinberg-81 under F4×G2/E7×A1 exceptional E8 branchings; finite-step graph-wave cone and an externally supplied 3+1D comparison; and a demodulated complex-IQ spectroscopy-control program with synthetic Fourier peak recovery.

## 1. Actual qutrit syndrome-extraction circuits — a quantitative fault-tolerance warning

Use the existing `[[160,1,8]]_3` stabilizer matrices. Wilson-Z extraction: prepare a qutrit ancilla in |0>, apply `SUM^h` with each of eight data links as control and ancilla as target, measure ancilla in Z. Gauss-X extraction: prepare |+> ancilla, apply `SUM^h` with ancilla as control and each of four data links as target, measure ancilla in X. For every generalized SUM gate, the exact Pauli exponents transform `x_target -> x_target+h*x_control`, `z_control -> z_control-h*z_target` over F3.

**A full single extraction round has 640+316=956 two-qutrit SUMs**, 159 ancilla preparations and 159 ancilla measurements. A single ancilla phase error during Wilson extraction can propagate to seven data Z errors; one ancilla X error during a Gauss extraction can propagate to three data X errors. This *hook mechanism* defeats any claim that code distance8 alone guarantees suppression of single circuit faults.

Stochastic circuit experiment: prepare independent per-site physical Pauli errors with probability `p_data=.002`, choose one of eight nonidentity local qutrit Paulis when faulty. After each SUM insert a uniformly random nontrivial *two-qutrit* Pauli with probability `p_gate`; also perturb ancilla preparation and readout independently with probabilities `p_prep=p_meas=p_gate`. Decode the measured 80+79 syndromes using the pre-existing exact radius-three lookup decoder; count residual logical failure **modulo stabilizers** (i.e., the full cycle and incidence constraints). Seed is frozen. Each parameter point has 160 one-round trials.

| p_gate=p_prep=p_meas | Logical failures /160 | Total injected gate/prep/readout faults in 160 trials |
|---:|---:|---|
| 0 | 0 | 0/0/0 |
| 0.0001 | 13 | 7/5/3 |
| 0.0003 | 58 | 58/8/10 |
| 0.001 | 116 | 153/23/36 |

A single gate error need not itself cause logical failure; faults can create incorrect syndromes, propagated correlated data errors or decoder ambiguity. But the sharp degradation is decisive: **this extraction order is not fault tolerant**. The observed finite Monte Carlo rates are not a fault-tolerance threshold, nor do they prove an alternative schedule impossible. Next investigate flag ancillas, verified cats, detector error models, repeated rounds and actual syndrome circuits.

Reproducer: `analysis/w33_20261009_toe28_qutrit_noisy_extraction.py`.

## 2. Product codes achieve positive RATE, but native W33 girth blocks distance growth

Use the standard ternary Tillich–Zémor hypergraph-product construction on the native (V−1)×E vertex–edge incidence matrix H of the W(3,q) Levi graph. With `m=V−1`, `n=E`, construct sparse commuting CSS checks

`H_X=[H⊗I_n | I_m⊗H^T]`,
`H_Z=[I_n⊗H | −H^T⊗I_m]`.

The minus sign is essential in odd characteristic F3 to ensure `H_X H_Z^T=0`; using the binary sign convention in F3 would be wrong.

The full-row rank m matrix has classical cycle code parameters `[n,n−m,8]_3`, since girth8. The hypergraph product therefore has exact

`[[n²+m²,(n−m)²,8]]_3 = [[E²+(V−1)²,q^8,8]]_3`.

Check using explicit CSR sparse matrices and a weight-eight Z logical witness:

| Base | Physical qutrits | Logical qutrits | Proven exact distance | Rate |
|---|---:|---:|---:|---:|
| W(3,2) | 2866 | 256 | 8 | 8.9323% |
| W(3,3) | 31841 | 6561 | 8 | 20.6055% |

Analytic q-family data additionally evaluate q=5,7,11,31,101. As q grows, rate q^8/[E²+(V−1)²] tends to **1**. Unfortunately the 8-cycle logical witness forces distance EXACTLY eight for all q; generator/check weights can also grow as q+3. Thus **positive rate does not imply asymptotically improving protection**. This is a real negative result for the proposal to obtain both properties by simply tensoring two W33/Levi incidence chains.

Potential escape: replace native building incidence graphs with bounded-degree graph families of provably increasing girth and linear cycle-space rank, giving a hypergraph-product code with positive rate and unbounded (typically logarithmic) distance. This is a DIFFERENT graph assumption and has not been shown W33-canonical.

Reproducer: `analysis/w33_20261009_toe28_hypergraph_product_rate_distance.py`. General HGP reference: https://arxiv.org/abs/0903.0566.

## 3. Exceptional E8 branchings: strict candidate host screening, no fabricated embeddings

Move past SL9 to established maximal-subgroup branching rules:

`E8 -> F4×G2: 248=(52,1)+(1,14)+(26,7)`.

`E8 -> E7×A1: 248=(133,1)+(1,3)+(56,2)`.

`E8 -> Spin(16): 248=120+128`.

These are representation branchings, **not yet homomorphisms from PSp4(3) into those factors**. For a PSp action entirely inside F4 (G2 trivial), all invariant blocks of the E8 adjoint have dimensions 52, 14 copies of1, seven copies of26; hence Steinberg81 cannot occur. Likewise if the action is only in G2, all blocks have dimension at most14. Thus **factor-only embeddings through F4 or through G2 are exact no-go classes for St81**.

The simple 25,920-element PSp4(3) group has no nontrivial homomorphism to SL2(C) (finite projective subgroups have no nonabelian simple order25,920). Hence in the E7×A1 product its A1 projection is trivial. The restricted adjoint has blocks 133,56,56,1,1,1, so St81 can occur *only* in E7's adjoint133, **if** a suitable PSp embedding exists. A diagonal nontrivial action on both F4 and G2 could support St81 only in the mixed 182D (26,7) tensor, also untested. A Spin(16) embedding could place it in 120 or128; dimensional data alone cannot choose.

**Key distinction:** these are necessary-representation-channel constraints. We have constructed *no* new exceptional finite subgroup embedding, intertwiners, invariant brackets, or Standard Model matter representation. The surviving E7-133 and mixed F4×G2-182 are the highest-priority exact character-restriction searches.

Reproducer: `analysis/w33_20261009_toe28_exceptional_e8_branch_screen.py`. Sources for E8 branchings: https://citeseerx.ist.psu.edu/document?doi=d31040221791fece0816c9adfa04522248c27456&repid=rep1&type=pdf and https://en.wikipedia.org/wiki/E8_(mathematics).

## 4. Real finite-step graph waves versus a Lorentzian 3+1D **input** model

Test a finite-difference leapfrog update on W33's 80-node normalized adjacency Laplacian `L=I−A/4`:

`phi_(t+1)=2 phi_t−phi_(t−1)−h² L phi_t`, `h=0.7`.

Start with a delta at one native incidence site and zero initial time derivative. Since `phi_t` is a polynomial in L of degree ≤t, it vanishes exactly beyond graph distance t. Explicit propagation verifies zero beyond the graph cone at all tested steps t=0..6. However, the W33 Levi diameter is **four**: the wave can reach the entire graph within four steps. Its five normalized Laplacian channels are `{0,1−sqrt6/4,1,1+sqrt6/4,2}`. **Finite graph propagation is not a 3+1D relativistic light cone**, and no Einstein action appears.

To make a falsifiable comparison, externally impose `C_N^3` as a physical three-dimensional spatial torus with fixed physical length10, and time as an independent coordinate. Add W33 only as an internal 80-mode operator. The resulting dispersion is

`omega² = (4c²/a²) sum_(i=1)^3 sin²(k_i a/2) + mu² lambda_W33`,

which converges to `c²|k|²+mu²lambda_internal` at small a. Native W33 then supplies **five internal mass-squared channels** (whose physical interpretation is unestablished), while the 3+1D continuum is **assumed** by the imposed external lattice, not emergent from W33.

The single-mode external spatial Laplacian relative error at N=8,16,32,64,128 is approximately −5.04%,−1.28%,−0.321%,−0.0803%,−0.0201%. This validates the illustrative external continuum discretization only.

Reproducer: `analysis/w33_20261009_toe28_wave_geometry_comparison.py`. Prior work: Round21/27 normalized graph heat no-go; October8 repo already supplied an EXTERNAL toroidal factor. No new physical spacetime derivation claimed.

## 5. Executable C8 Ramsey-control sequence with synthetic five-band recovery

Build the full **36-state, two-boson attractive C8 Bose–Hubbard Hamiltonian** at U/t=32, t/h=5MHz (both model assumptions). Diagonalize all 36 states, prepare the |2_0> doublon, isolate its eight bound levels (leakage ≈0.387%), and build the complex phase-sensitive return amplitude `A(t)=sum_(bound j)|<j|2_0>|² exp(-i2pi E_j t/h)`. Heterodyne by an explicitly specified pair binding reference near −161MHz; this avoids resolving the huge carrier and restricts spectral processing to the ±0.7MHz envelope.

Use a **60 μs** evolution sweep at **0.1μs** increments (601 delays), hypothetical coherence `T2=100μs`, and independent quadrature Gaussian shot-noise standard deviation `1/sqrt(8192)`. The synthetic complex-IQ Fourier spectrum reproduces all FIVE bound-band centers with maximum absolute frequency error **0.007615MHz** (one discrete FFT bin ≈0.01664MHz). Band frequencies relative to the reference are approximately `−0.622,−0.440,−0.0006,+0.440,+0.623 MHz`.

The code emits nine abstract instrument-control stages: calibrate eight sites, calibrate eight links, independently measure nonlinear attraction, load a local |2> pair, establish complex reference frame, sweep delays, measure I/Q, fit five bands, independently verify leakage and pair continuum. Estimated experimental expense: `601×2×8192 = 9,846,784` individual quadrature shots. It also separately computes a *probability-only* Fourier spectrum to enforce the prior readout no-go: `|A(t)|²` contains **pairwise energy differences**, not five absolute eigenenergies.

The simulation proves neither feasibility of quantum coherence/reference hardware nor measurement data. It is a runnable, source-calibrated control specification to evaluate with actual experimental partners and device constraints.

Reproducer: `analysis/w33_20261009_toe28_c8_ramsey_control_spec.py`.

## Summary and limits

Best constructive outcomes: an actual one-round qutrit Pauli circuit fault simulator with a demonstrable hook-error problem; positive-rate exact HGP CSS codes from native W33 (but fixed distance8); phase-sensitive synthetic C8 spectroscopy recovering five band centers. Best physics no-go: raw 80-site W33 waves do not generate 3+1D Lorentzian geometry, and finite exceptional E8 representation branching sharply narrows but does not solve the matter-intertwiner route.

Five new standalone Python producers, five JSON result certificates and focused tests support every claim. Nothing here demonstrates a fundamental theory of everything, physical gauge superselection, a Standard Model coupling, a quantum fault-tolerance threshold, a Lorentzian Einstein field equation, or any real hardware experiment.
