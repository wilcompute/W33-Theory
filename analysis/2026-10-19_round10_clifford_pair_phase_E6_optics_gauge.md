# W33 / TOE Round 10 — pair-orbit geometry, hostile phase search, E6 cubic coordinate obstruction, optical readout, gauge action

**19 October 2026.** Five independent directions executed with explicit producers and tests, in an isolated research worktree; the dirty main Windows repository checkout was not edited. The previous pending Round 9 seven-test suite was independently rerun and passed 7/7; those scripts, their five JSON certificates and technical report are part of the committed recovery. Parallel Passes 12071–12075 reviewed: particularly PASS12072 PROVED NO CLIFFORD-EQUIVARIANT TICK–CLOCK BIJECTION and withdrew the Pass12061 tick-condensate/rest-frame physical reading; the 12074 capacity-condensate phase diagram is a DIFFERENT model and should not be confused with the F_T+kappa C interaction analyzed here.

## Front 1: full 2916-stabilizer orbits on TWO discrete E8(-24) vacua
Previously Round8 gave 1440 projectors Q as unordered pairs of orthogonal two-qutrit stabilizer rays in 40 maximal Pauli commuting contexts; |PCliff_2qutrit|=4,199,040 and |Stab(Q0)|=2,916. Round9 provided a 1440-vacuum tight operator-frame spectrum and nonconstant pair overlap invariants.

**NEW exact finite permutation computation:** generate the five Clifford permutations on the 360 context×ray objects and induce permutations on 1440 pair-vacua. Find BFS transversals t_v for every vacuum v. The Schreier maps h_(v,g)=t_(g·v)^(-1) g t_v generate the stabilizer of Q0 and all fix Q0. A union-find orbit search across every resulting permutation partitions ALL 1440 partner vacua into precisely **17 distinct stabilizer orbits**. Orbit sizes, ordered by overlap, are:
  6,18,27,3,6,27,6 (overlap 0);
  162 (overlap 1/3);
  243,729 (overlap 4/9);
  54,54,81 (overlap 2/3);
  2,12 (overlap 1);
  9 (overlap 4/3);
  1 (overlap 2).
They sum to 1440. Exact permutation combinatorics, numeric nine-by-nine Hilbert-Schmidt overlap differences <1e-9 within each orbit.

**Physics implication:** for ANY Clifford-invariant real pair functional V(Q,R), with Q0 held fixed, the interaction is constant on these 17 orbits; the mere scalar Tr(QR) is too coarse (several 17-classes share an overlap value). Dynamics can choose *relative* orbit type only after coefficients and interactions are specified. Absolute vacuum choice remains degenerate under simultaneous Clifford symmetry. No observer rest frame follows, especially in light of Pass12072's tick-to-clock no-go.

## Front 2: adversarial 3-tick challenge to full global phase threshold
Round9 proved exact two-tick convexity at all T>0 with singleton optimal iff kappa>=kappa_2(T)=-3/2(1-exp(-1/T))/(3+6exp(-1/T)); kappa_2(.5)=-0.3402395316. Round8's majorization plus local derivative proves all global minimizers have C>0 below this threshold, but does not certify global singleton above it.

We ran a seeded randomized STRATIFIED three-outcome search with 30 batches of up to 300 triples per batch, outcome directions distinct, rates drawn from multiple Dirichlet concentrations (plus uniform triples); all three patterns of 1,2,3 noncommuting pairs were visited. Matrix Gibbs F was computed by exact 9×9 Pauli projectors with double-precision eigensolvers. The candidate's crossing kappa=(F_single-F_w)/C was evaluated only if C>=1e-5 and F_w-F_single>=1e-9.

**Critical falsification hygiene:** An initial candidate kappa=-1/3 was a FALSE POSITIVE from almost-singleton weights ~1e-14, where subtracting two nearly equal free energies is numerically ill-conditioned. It was rejected after observing this and adding explicit conditioning guards. The best surviving sampled crossing was **-0.3402401726**, LESS than the exact two-tick local threshold **-0.3402395316**; therefore this finite sample found **NO certified or credible triple-tick counterexample**. It DOES NOT prove the full 120-variable threshold or exclude an adversarial >3-support configuration. Directed intervals or validated SDP/branch-bound are still required.

## Front 3: a provable constraint on E6 trinification-to-Jordan change of basis
The ordinary E6 cubic in canonical SU3^3 weight coordinates (A,B,C three 3×3 blocks) has 45 distinct monomials: 3 determinant blocks ×6=18 and Tr(ABC) with 27. The classical Jordan cubic in standard Cayley-Dickson coordinates 27=3 singlets + 8+8+8 octonion coordinates has EXACTLY **89** monomial supports: abc (1), three singlet×octet norm forms (3×8=24), and 64 nonzero octet trilinear basis products 2Re((vw)z). The latter 64 were exhaustively verified with explicit Cayley–Dickson multiplication, each coefficient ±2.

**Rigorous restricted-coordinate obstruction:** a monomial linear map on C^27 (independent nonzero coordinate rescalings and a permutation) preserves monomial support cardinality of a cubic polynomial. 45 !=89, so no such SIMPLE signed permutation and scaling of trinification coordinates produces the standard Jordan cubic. A genuine complex E6-equivariant change of basis MUST mix coordinates; this does NOT rule out an arbitrary invertible 27×27 E6 intertwiner. The latter remains OPEN, and no W33 weight-to-octonion map, Yukawa magnitude, or SM mass matrix was derived. Parallel Pass12073 already resolved 12 family-diagonal+33 cross monomials in a different clock-pair basis; those prior findings are credited, not repeated as novelty.

## Front 4: photon-count noise and detector/phase-drift falsification
Round9 recovered the ideal commutator trace contrast 8/27 using 36 settings, complex reference F3⊗F3, two phases, and inverse W=R^-1 S. The new producer introduces a **transparent synthetic detector false-click replacement channel**: each photon has probability d of a uniformly random detection among 18 path×mode ports rather than its intended path, mode or erasure. Then the measured interferometric port difference is scaled by 1-d. Matching stationary d in calibration R and signal S cancels in the transfer ratio, while mismatch d_R=0.005 vs d_S=0.015 shifts the ideal deficit by **+0.0070724**. Relative phase drift 0.03 rad produces **+0.00031664** in the tested W.

Monte Carlo: 36 settings, 12,000 photons per setting = 432,000 source photons per run, 70 independent multinomial repetitions under each of three scenarios. Means agree with the analytic prediction to within ~0.002. This is NOT a detector physical noise model: uniform false-click replacement overlooks independent Poisson multi-click events, afterpulsing, gate dead-time, mode-dependent detection, correlated errors and actual photonic chip imperfections. Valid hardware must time-interleave R/S calibration and measure phase noise.

## Front 5: true SU3^3 gauge-invariant scalar tensors and noncompact E8(-24) kinetic obstruction
Construct actual complex bifundamental scalar fields A~(3,bar3,1), B~(1,3,bar3), C~(bar3,1,3), transforming A'=U_C A U_L†, B'=U_L B U_R†, C'=U_R C U_C†. All U are SU3 matrices. Verify explicit random SU3 unitary gauge transformations preserve:
- Tr(AA†), Tr(BB†), Tr(CC†);
- complex cubic det A, det B, det C, Tr(ABC), plus conjugates;
- (Tr XX†)^2, Tr[(XX†)^2] and products of quadratic invariants.
Maximum invariance residual ~2.05e-12 in 120 samples. An explicit renormalizable SU3³-invariant radial + determinant + trace-cubic scalar action is given in the producer certificate. However its couplings m², eta_i, lambda_i are independent unless a higher symmetry supplies relations; a generic SU3³-invariant action is NOT automatically a full E6 or E8-invariant action.

**Important physical firewall:** A simple noncompact real Lie algebra has an invariant symmetric bilinear form unique up to scale; E8(-24) has Killing form signature (112 positive,136 negative). An ordinary constant-coefficient Yang–Mills kinetic term gauging ALL 248 generators with that form has wrong-sign gauge-vector polarisations for one sector, whichever overall sign is chosen. A compact gauged subgroup, field-dependent kinetic tensor, constraints or other physical mechanism is necessary before claiming a positive-energy full E8(-24) gauge theory. This does NOT rule out E8(-24) global or gravitational symmetries or more sophisticated formulations. It also does not derive a parameter-free coupling or mass ratio.

## Reproduction and evidence firewall
Recovered Round9 artifacts: five producers with their five JSON results, one technical report and 7 regressions; all seven rerun successfully after desktop reconnection.
New Round10 artifacts:
- analysis/w33_20261019_round10_pair_orbit_schreier.py -> data/w33_20261019_round10_pair_orbit_schreier.json
- analysis/w33_20261019_round10_three_tick_falsification.py -> data/w33_20261019_round10_three_tick_falsification.json
- analysis/w33_20261019_round10_E6_sparse_intertwiner_obstruction.py -> data/w33_20261019_round10_E6_sparse_intertwiner_obstruction.json
- analysis/w33_20261019_round10_optical_detector_and_drift.py -> data/w33_20261019_round10_optical_detector_and_drift.json
- analysis/w33_20261019_round10_gauge_invariant_action.py -> data/w33_20261019_round10_gauge_invariant_action.json
- tests/test_w33_20261019_round10.py

**No fundamental TOE has been derived.** Exact group orbit, monomial obstruction and gauge covariance are mathematics; three-tick and optics are synthetic numerical studies; negative-kappa sign/magnitude, full global phase boundary, unique real physical vacuum, SM spectrum and dimensional mass scale remain open.
