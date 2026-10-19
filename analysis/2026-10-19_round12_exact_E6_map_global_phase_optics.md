# W33 Round 12 — Exact E6 cubic map, Wedderburn matrices, global-phase counterexample, optics and compact-gauge viability

**19 October 2026.** Main W33 repository, isolated research worktree; original dirty checkout left untouched. Current parallel Pass 398 reviewed; Pass 12072 forbids a Clifford-equivariant map of 120 Pauli ticks onto 120 E8 clock involutions. Nothing below restores that invalid physical identification. Mathematical exact certificates must not be represented as physical TOE predictions.

## 1. Eight exact central idempotents and rational 2x2 matrix representations

Round 11 established the 17-class noncommutative vacuum orbital algebra with 4,913 exact integer structure constants and center dimension 8. Here we construct explicit matrices. Solve the center exactly over Q and choose central integer linear combination with coefficients 1,2,3,5,7,11,13,17. Its regular characteristic polynomial has eight distinct RATIONAL roots with multiplicities:
- eigenvalues 34322, 5306, 554, -1798, -8014, each multiplicity one
- eigenvalues 1742, -427, -499, each multiplicity four.

Apply polynomial Lagrange interpolation to form all eight primitive rational central idempotents. Verify precisely E_i E_j=delta_ij E_i, sum E_i=I_17 and [E_i,L_j]=0 for all orbital generators. Thus the decomposition splits over Q, not only C. For each rank-four ideal find a rational 2D eigenspace of an appropriate RIGHT multiplication map. Restrict all seventeen left multiplication matrices to obtain **3 sets of 17 explicit 2x2 rational matrices**, satisfying all orbital products by exact arithmetic. The complex algebra is C^5 direct sum M2(C)^3; these are representation blocks, not observed qubits.

Sources: analysis/w33_20261019_round12_central_spectrum.py and analysis/w33_20261019_round12_M2_representations.py; machine-readable exact projectors and generator matrices in corresponding JSON.

## 2. Explicit 27x27 invertible CUBIC norm isomorphism between the first Tits and Cayley–Dickson Albert charts

Round 11 identified the classical first Tits Albert cubic on three 3x3 matrices:
N_T(A,B,C)=det A+det B+det C-Tr(ABC).
Round 10 proved that a permutation-and-independent-rescaling of the original 27 coordinates cannot be the standard Cayley–Dickson coordinate change (45 versus 89 nonzero monomials in the original charts).

This round **constructs the actual full complex 27x27 transformation**. Split the Tits 27 into three diagonal singlets and three 8D Peirce planes V_ij. For V_ij (k the remaining index), take A_ij,A_ji and B_kl,C_lk for l=0,1,2. Four hyperbolic pairs give a quadratic norm; change each pair by (u+iv,u-iv), converting its product to u²+v². This yields 24 orthonormal octet directions and 3 diagonal singlets, with a nonzero 27x27 determinant -4096.

Extract all 512 coefficients in the three-octet trilinear tensor: only 64 nonzero, all ±2, identical support to the Cayley–Dickson 8-vector octonion scalar triple. A GF2 linear system over 24 independent signs aligns all 64 coefficients with the standard octonion product; all three 8-element index permutations can be IDENTITY. The resulting exact Gaussian-integer 27x27 matrix T, stored completely in JSON, obeys

N_Tits(Tx)=abc-a||v||²-b||w||²-c||z||²+2 Re((vw)z),

checking abc, all 24 quadratic terms, and all 512 possible octet triples exactly; determinant -4096. This settles the **classical norm/cubic coordinate problem**, not physical Yukawa magnitudes or an intertwiner between inequivalent tick and clock actions (Pass12072 explicitly obstructs the latter). First Tits and Albert equivalence are classical prior art; the signed explicit matrix is a reproducible project contribution.

Sources: analysis/w33_20261019_round12_peirce_27_map.py and analysis/w33_20261019_round12_full_octonion_intertwiner.py with corresponding JSON.

## 3. EXACT RATIONAL seven-tick counterexample to extrapolating local stability globally at T=1

The Round9 theorem exactly determines the optimal singleton criterion restricted to any TWO-tick face: kappa_local(T)=-(3/2)(1-e^-1/T)/(3+6e^-1/T). Round11 sampled >100k three-tick points at T=0.5 without finding a counterexample, but that was NEVER a global proof. Already in an early numerical pass the uniform seven-tick heptad was seen to cross the singleton around kappa=-0.181113 at T=1 while the local threshold was more negative (~-0.182088). We credit that earlier discovery; the NEW contribution is a rigorous arithmetic certificate.

At T=1, kappa_local=-(e-1)/(2(e+2)). Choose seven pairwise noncommuting W33 projective points [0,23,27,28,34,36,39] with outcome labels [2,2,2,1,2,0,1]. Choose exactly rational weights six times 1473/10000 and 1162/10000 on the final point. All seven pairwise noncommute and C=4/3 sum_{i<j} w_i w_j is rational.

Represent the cyclotomic field Q(omega), omega²+omega+1=0, by **2x2 rational matrix** for omega [[0,-1],[1,-1]]. The physical 9x9 Pauli projectors then become EXACT rational 18x18 matrices. Compute rational traces Tr Q^n through n=12. Since 0<=Q<=I, omitted terms from Tr exp Q are nonnegative, giving a certified lower bound on its partition function. Bound e by rational truncated Taylor series with explicit upper tail; the function kappa(e) is decreasing. The even fourth-order exp Taylor polynomial gives an exact UPPER bound on exp(kappa_upper C) for negative arguments.

A purely rational inequality then holds:

Z(Q)_lower > (3 e_upper +6) Taylor_4(kappa_upper C),

with positive rational gap approximately **0.0092152625116**, implying
F_1(Q)+kappa_local C(Q) < F_1(single)
strictly, with estimated energy gap **-0.0007221988**.

This disproves ANY claim that the two-tick local threshold equals the 120-variable GLOBAL singleton transition at every T. A seven-tick state pre-empts singleton global optimality at T=1 while singleton is stable along infinitesimal two-tick directions. The exact full 120-rate critical kappa is STILL unknown; no true thermodynamic singularity is asserted for finite 9D Gibbs models. A separate 48-minimization SLSQP numerical audit at T=0.2,0.5,1 projects EVERY candidate back onto the feasible simplex before energy evaluation; unprojected solver error previously gave false wins.

Sources: analysis/w33_20261019_round12_exact_rational_heptad_counterexample.py and analysis/w33_20261019_round12_global_phase_multistart.py, JSON certificate includes rational trace bounds.

## 4. Synthetic experimentally preregistered-style photonic discriminant with darks and phase drift

Starting from Round11's full 36-setting trace covariance, test three conditions under a 54-setting protocol: R identity reference, S noncommuting W33 commutator loop, and N commuting null, nine inputs each and two quadrature phases. Include calibrated coherent mode-preparation mixing (0.01 radians), output loss/mode crosstalk, multinomial detected photons and erasures, additive Poisson dark clicks (~0.18% relative source-photon fraction), sequential afterpulsing (~0.1% of prior gate counts), and shared Gaussian phase drift std .03 radians plus condition-specific std .006. Each experiment uses 15,000 input photons per setting, **810,000 photons total**.

Train a decision threshold on 90 independent NO-SIGNAL repetitions only: mean(delta_signal-delta_null)+5*null_sample_std. Hold out 100 fresh null trials and 100 fresh true W33 trials. Measured synthetic null sigma≈0.0069489, threshold≈0.033307, zero held-out false positives (0/100), signal mean≈0.296703 and 100/100 signal detections. This is synthetic Monte Carlo, NOT fabricated optics or validated physical Type-I/Type-II rates; dark count physics, dead time, chip fabrication, long-term calibration and photon source statistics need actual instrument inputs. Zero false positives in 100 tests does not imply a zero physical false-positive rate.

Source: analysis/w33_20261019_round12_optical_falsification.py with JSON.

## 5. Compact E7×SU2 Hamiltonian / anomaly / Weyl-mass obstruction

Round11 showed full noncompact E8(-24) Yang–Mills has wrong-sign modes with its constant Killing metric. Gauging only maximal compact K=E7_compact×SU2 (133+3=136 dimensions) and treating p=(56,2) as 112 real scalars admits a positive K-invariant Cartan kinetic form, but need to check physical constraints.

At quadratic order around unbroken K and trivial vacuum, Gauss constraints leave **2×136=272 transverse massless gauge modes**, plus 112 positive-mass scalar oscillators, giving 384 bosonic propagating modes in this toy sector. The positive Hamiltonian formula H2=1/2∫(E_T²+B²+pi²+|grad phi|²+m²phi²) was audited with 500 strictly positive numerical field samples. This is classical/free-field positivity, NOT unitarity/ghost-free quantum completion.

One left Weyl multiplet in (56,2) has 56 SU2 doublets, even Witten parity, and no perturbative E7/SU2 cubic anomaly. BUT E7's fundamental 56 and SU2 fundamental 2 are both pseudoreal. Their tensor product is a REAL 112-dimensional representation, possessing an invariant symmetric nondegenerate bilinear Omega56⊗epsilon2. The symmetric 112×112 mass matrix was constructed explicitly and verified rank112. Therefore a gauge-invariant Weyl Majorana mass is ALLOWED: gauge anomaly consistency alone cannot protect three light chiral Standard Model families in this simple construction. The E8 global symmetry, physical chiral spectrum and mass ratios remain unresolved.

Source: analysis/w33_20261019_round12_compactE7_chiral_mass.py and JSON.

## Reproducibility, status and prior art

Eight independent producers and their eight machine-readable JSON certificates:
- analysis/w33_20261019_round12_central_spectrum.py
- analysis/w33_20261019_round12_M2_representations.py
- analysis/w33_20261019_round12_peirce_27_map.py
- analysis/w33_20261019_round12_full_octonion_intertwiner.py
- analysis/w33_20261019_round12_exact_rational_heptad_counterexample.py
- analysis/w33_20261019_round12_global_phase_multistart.py
- analysis/w33_20261019_round12_optical_falsification.py
- analysis/w33_20261019_round12_compactE7_chiral_mass.py
- tests/test_w33_20261019_round12.py

Classical prior art: First Tits construction of Albert algebra, Cartan E8(-24) maximal compact, E7 symplectic 56, and two-qutrit Clifford geometry. Novel to THIS round are explicit rational matrices/certificates, a full signed 27x27 first-Tits/Cayley cubic coordinate transformation, and the rigorously bounded rational seven-tick global-boundary counterexample. Physics has NOT advanced to a parameter-free TOE.
