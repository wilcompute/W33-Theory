# W33 Theory — Round 30: verified qutrit cat extraction, an explicit girth-10 cover, full F4×G2 exclusion, finite-chronology saturation, and readout feasibility

**Date:** 9 October 2026
**Repository:** `wilcompute/W33-Theory`
**Research question:** Execute the five independent tasks selected after Round29, verify each against parallel commits, and publish exact proofs, finite computation certificates and falsifiable assumptions. No physical device, observed gravitation, full Theory of Everything, measured Standard Model parameters, or circuit-level threshold is claimed.

## Provenance and prior-art checks

Already in the repo before this work:

- Round26: `[[160,1,8]]_3` from 160 W33 Levi incidence-link qutrits, 80 weight-eight Wilson Z generators, 79 weight-four Gauss X generators.
- Round27: ideal-syndrome radius-three lookup decoder and ternary generalized-`W(3,q)` one-logical code theorem. Round28: noisy sequential one-ancilla-per-stabilizer extraction, yielding 956 SUM operations, dangerous hooks; and fixed-distance native hypergraph products. Round29: mathematical **existence** of unbounded-girth graph covers by residual finiteness, unverified transversal cat **data-layer** fault locality, and two synthetic C8 spectroscopy protocols.
- Parallel Pass11831–11833: exact finite 4D F3 tangent-space light cone, 81 vectors, 20 null, Brouwer–Haemers SRG(81,20,1,6), and SL(2,9) observer stabilizer; previous Rounds27–29 showed this is not emergent physical Minkowski spacetime.
- Round28–29: F4-only/G2-only no-go, candidate mixed F4×G2(26,7), conditional E7 subgroup restrictions; no actual embedded Steinberg-81 Lie-bracket model has emerged.
- Current parallel master work reserved Passes11834–11838 for further finite Poincaré/AdS/Dirac singleton and E8 studies, but reservation is **not yet a published proof of those proposed future claims**.

## 1. Complete single-fault conditional qutrit-cat circuit test — with a valid stabilizer-measurement circuit

Round29 established only that one ancilla per data link prevents correlated propagation *during the data-coupling layer*. This pass first exhaustively propagated 147,888 Pauli faults through an unverified GHZ fanout and the earlier SUM orientations, finding up to **two effective data errors per single cat-preparation fault** and one for transversal data faults. The simple unverified design was **not proven to implement the correct stabilizer measurement**: measuring all computational-basis GHZ targets may overmeasure the data. It is retained as a diagnostic, not the accepted protocol.

We then implemented a **physically well-defined Shor-style CZ protocol** for every one of the 159 native W33 checks:

1. Prepare `GHZ_w=(|0^w>+|1^w>+|2^w>)/sqrt3` using root `|+>`, leaves `|0>`, `w−1` fanout SUM gates, for Wilson w8 and Gauss w4.
2. Verify the independent `w−1` GHZ parity stabilizers `Z_0 Z_j^(-1)` with separate `|0>` verifier ancillas, two SUM gates each, postselecting trivial verification syndrome.
3. Couple each GHZ ancilla once, **transversally** by `CZ^{h_j}(cat_j,data_j)`. Because the GHZ is stabilized by `X_0X_1...X_{w−1}`, conjugation turns its product-`X` measurement into nondemolition measurement of the desired data `∏ Z_j^{h_j}` check. Measure every cat in the Fourier `X` basis and sum the outcomes mod3. For Gauss X checks, conjugate the data basis by ideal local qutrit Fourier transforms before and after extraction.
4. Enumerate **all 80 nonidentity two-qutrit Pauli faults after every individual fanout, verifier and data-CZ gate**, and all eight single-qudit nonidentity Pauli faults at every cat initialization site; simulate exact F3 Pauli propagation, ideal verifier acceptance, and final data-error weight *after multiplication by the measured stabilizer*.

**Exhaustive result: 275,408 single faults across the full check list.**

| Stabilizers | Accepted faults | Rejected faults | Max effective data error from accepted single fault |
|---|---:|---:|---:|
| 80 Wilson Z | 79,360 | 111,360 | **1** |
| 79 Gauss X (ideal Fourier basis) | 39,184 | 45,504 | **1** |

The proposed circuit requires **3,347 two-qutrit gates** and **1,753 cat+verifier ancillas per complete round**, vs previous sequential 956 gates/159 ancillas. The result is a genuine **single-fault hook-firewall certificate conditional on perfect verifier and final syndrome readout, ideal basis changes, and postselection**.

It is **not** a complete fault-tolerance theorem: faults in verifier initialization/readout, cat readout or Fourier changes, two simultaneous faults, multiple rounds, noisy detector history, leakage, coupling geometry and decoder/threshold simulation remain open. The prior 13/160 sequential failures at p=1e-4 cannot be directly compared to a physical accepted-cat failure rate. A device may need more economical flagged extraction.

Reproducers: `analysis/w33_20261009_toe30_cat_prep_faults.py`, `analysis/w33_20261009_toe30_verified_cat_CZ.py`. Independent technical precedents: https://qiskit.qotlabs.org/learning/courses/foundations-of-quantum-error-correction/fault-tolerant-quantum-computing/controlling-error-propagation and https://mqt.readthedocs.io/projects/qecc/en/equivalence-checking/CatStates.html .

## 2. First EXPLICIT W33 finite graph-cover certificate with girth ten and distance ten

**Prior:** Round29 invoked residual finiteness of `pi1(W33 Levi)=F81` to prove abstract arbitrarily large-girth covers. Random cyclic covers of degrees 1,2,3,5,7,11 all had girth exactly eight, and no longer-girth cover voltage assignment was published.

Now explicitly construct a **degree-83 cyclic voltage cover**. The native W33 base has 80 vertices,160 incidence edges,1620 simple oriented 8-cycles, each base edge belonging to exactly81 such cycles. Start all 160 signed voltages at zero modulo83. Repeatedly choose a violated eight-cycle, pick one incident edge, and modify that edge's voltage to a value for which **all 81 eight-cycles containing the edge have nonzero signed holonomy**. Since there are 83 possible residues and at most81 forbidden residues, such a value always exists. Every update reduces the count of zero-holonomy eight-cycles monotonically. The algorithm terminated in **81 updates**.

Emit the complete explicit list of 160 voltages and one length-ten lifted cycle witness. Construct the full **6,640-vertex,13,280-edge connected four-regular** cyclic lift in memory; verify all degrees, all-vertex connectivity, all 1620 base eight-cycle holonomies, and the ten-cycle witness. No shorter lift cycle can occur because every projected reduced walk shorter than8 is impossible in the base, and every length8 projected cycle has forbidden zero holonomy. **Exact cover girth=10**.

Apply the standard ternary hypergraph product to its `(6640−1)×13280` vertex-edge incidence check. This proves a quantum CSS code

`[[220434721,44102881,10]]_3`,

**rate 20.0072%, maximum generator weight six, distance exactly ten**. The quantum check matrices for 220 million qudits are *not explicitly materialized*; parameters, distances and weights follow from the standard full-rank-incidence HGP theorem and a witnessed length-ten logical cycle. The full 6640-vertex lift itself is explicitly built and connectivity/girth checked.

This is an actual compact **graph-level voltage certificate**, not a deployable quantum computer: 220,434,721 physical qutrits remains wildly impractical. It does not produce small efficient covers of arbitrary girth, good physical locality or an experimentally correctable code threshold.

Reproducer + complete 160-integer witness: `analysis/w33_20261009_toe30_explicit_cover_girth10.py`, `data/w33_20261009_toe30_explicit_girth10_cover.json`.

## 3. Entire F4×G2 exceptional E8 route closed for PSp4(3) Steinberg81

The previous work excluded embeddings acting only through F4 or only through G2; the mixed `(26,7)` representation remained nominally possible. Here a representation-theoretic argument, **conditional on standard published ATLAS ordinary characters and the complex G2 vector stabilizer theorem**, rules out ANY nontrivial homomorphism

`PSp4(3) ≅ PSU4(2) -> G2(C)`.

The complex group G2 acts faithfully and orthogonally on its fundamental seven-dimensional vector module. By simplicity, any nontrivial homomorphism of PSp4(3) to G2 is faithful. By the ATLAS character table, all complex irreducibles of dimension at most7 are 1, two mutually complex-conjugate nonreal 5s and one real orthogonal irreducible6; there are no complex irreps of dimensions2,3,4 or7. Thus a **self-dual** seven-dimensional G-module must be either trivial or `1⊕6`; `1⊕1⊕5` is non-selfdual. The 1D invariant summand is nonisotropic under the G2 orthogonal form because its irreducible complement6 is orthogonal and nondegenerate.

The stabilizer in complex G2 of a nonisotropic vector is `SL3(C)`, where the fundamental 7 restricts as `1⊕3⊕3*`. Hence the putative irreducible6 would split as3+3*, a contradiction. This proves every map from PSp4(3) to complex G2 is trivial.

Therefore any PSp4(3) subgroup of `F4(C)×G2(C)` projects trivially to G2. Under the true E8 branching

`248=(52,1)⊕(1,14)⊕(26,7)`,

all PSp-invariant blocks are then 52, fourteen 1s, and seven 26s. By complete reducibility there is **no irreducible Steinberg81 constituent for ANY F4×G2 embedding**, including the previously open mixed action.

This closes a whole E8 subgroup route, but NOT all E8, E7, Spin16 or matter mechanisms. This pass does not calculate a full new group character table from matrices or construct new Lie brackets; it uses external published representation-theory inputs and independently checks all dimension partitions and branching totals.

Reproducer: `analysis/w33_20261009_toe30_G2_full_subgroup_nogo.py`. Authoritative inputs:
- ATLAS `U4(2)` complex representations: https://brauer.maths.qmul.ac.uk/Atlas/v3/clas/U42/
- Non-real `5a`: https://brauer.maths.qmul.ac.uk/Atlas/v3/matrep/U42G1-Ar5aB0
- Non-real `5b`: https://brauer.maths.qmul.ac.uk/Atlas/v3/matrep/U42G1-Ar5bB0
- Real orthogonal 6: https://brauer.maths.qmul.ac.uk/Atlas/v3/matrep/U42G1-Zr6B0
- G2 7D, stabilizer and 1+3+3* model: https://math.univ-cotedazur.fr/~pauly/G2Theta.pdf

## 4. Nonperiodic AdS clock exists, but light-cone propagation saturates in two ticks

Round29 proved that an F3^4 additive translation-invariant strict chronology cannot exist: if 0<v, repeated translation forces a 3-cycle back to 0. To construct **one** mathematically valid orientation, introduce an **external nonperiodic** integer clock and event set `Z×F3^4`, with future directed edges

`(t,x) -> (t+1,x+v)`

for each of the 20 nonzero null vectors of the already-established finite AdS tangent geometry. This is acyclic, but time is assumed, not derived.

Because the 81-state light-cone graph is `SRG(81,20,1,6)`, its exact two-step adjacency identity is

`A²=20I+A+6(J−I−A)`.

Thus every spatial position is reachable after **exactly two future null moves**: 20 two-step returns to the same location, one path to each of 20 adjacent positions and six paths to each of 60 nonadjacent positions. Spatial future size goes `1 ->20 ->81` in two ticks, after which it remains all 81. Its stochastic null-step operator `P=A/20` has spectrum `1^1,(0.1)^60,(-0.35)^20` and quickly mixes rather than producing an expanding local continuum.

This provides an exact **no-go for this elementary external-clock extension as scale-extensive physical 3+1D causal propagation**. There is a chronology but no expanding spatial light cone at larger scales, dynamical metric, Einstein field equation or speed of light. The new parallel Pass11831–11833 finite-AdS representation is respected as prior exact kinematics, not relabeled as a physics discovery.

Reproducer: `analysis/w33_20261009_toe30_finite_ads_Z_clock.py`.

## 5. Realistic-readout sensitivity: lower synthetic shot count is NOT always faster

Round29 compared ~2.96 million ideal direct-scan shots against ~9.85 million ideal two-quadrature IQ shots for a hypothetical 8-site C8 two-boson device. Those counts assume comparable contrast and no differences in interrogation/reset overhead, neither experimentally grounded.

This pass tests **27 transparent what-if cases**:

- `T2` =25,50,100 microseconds.
- Per-shot reset =5,50,500 microseconds, plus separately assumed 5us readout.
- Intrinsic direct/IQ readout contrast pairs (0.2,0.6), (0.6,0.6), (1,1).
- Assumed mean interrogation time direct20us, IQ30us; decoherence penalty exp(-t/T2).
- To target the same baseline statistical sensitivity, per-point shots scale as `8192/[contrast exp(-t/T2)]²`. Total wall time = number of points * adjusted shots * (reset+readout+interrogation).

**Results:** direct scan was faster in **19 of 27** conditional scenarios, IQ was faster in the remaining **eight**; worst sampled direct/IQ wall-time ratio was **2.17**. Neither protocol is universally better. Readout contrast can reverse the earlier apparent 70% shot reduction. For all sampled T2 values, the simple Lorentzian width `1/(pi*T2)` remains smaller than the ideal first pair-band gap (~0.182MHz), although this is not a complete resolution or signal-detection criterion.

**No physical chip, measured T2, pair-selective addressability, signal contrast, frequency drift, loss or reset time is supplied**. Treat these as explicit experimental planning inequalities, not data.

Reproducer: `analysis/w33_20261009_toe30_C8_readout_feasibility.py`.

## Scientific conclusion and acceptance limits

**Constructive:** The explicit 83-fold girth-ten W33 cover closes the gap between a free-group existence argument and a reproducible finite graph witness; a genuine verified-GHZ CZ syndrome circuit passes exhaustive accepted single-fault data-propagation tests. **Obstruction:** The group action in complex G2 is impossible for PSp4(3), eliminating the entire F4×G2 Steinberg81 route, while the proposed external AdS clock saturates its spatial future within two steps. **Engineering:** Actual C8 protocol preference depends on measured contrast/coherence/reset parameters.

There is no experimental universal computer, actual theory of gravity, experimentally derived Standard Model parameter, proven noisy quantum threshold, or physical 3+1D spacetime from these results.

The six producers, six machine-readable JSON certificates, one consolidated research report and automated regressions record exact reproducibility. Existing parallel changes and unrelated dirty local files were not edited.
