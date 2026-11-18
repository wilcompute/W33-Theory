# Six-front follow-up: Klein charged modes, Wilson selection, modular winding, GQ continuum and photonic falsifiers
Date: 2026-11-18
Status: exact arithmetic plus conditional geometric and effective-theory consequences. No TOE completion or measured experiment.

## Provenance and collision control
Read current master a3408dc: Klein F55 integral topology, C-field torsion and invariant holomorphic functions. Also reviewed commits 3095ad3 and c2f8f23 for the free group, Sasaki-Einstein link and ordinary Dirac bound. Read the separate, still uncommitted 2026-11-18_Klein_C11_Wilson_linking_quantum_orbit.md: it owns the alternative C11 quotient, the order-11 SU5 Wilson line and linking/quantum-double correspondence. We do not stage or republish that work. Read the committed 2026-11-16_D9_iib_conifold_dual.md and 2026-11-16_Tpq_warp_resonance.md; they own the M/IIB winding dictionary, dispersion and geometric scalar harmonics. The new statements below apply independent character resolution, representation counts, modular lattice bounds and graph spectral reasoning. Distinct repository paths prevent collisions.

## 1. Charged holomorphic scalar modes on the Klein link
Take the Klein cubic f=sum_i x_i^2 x_(i+1). The C11 diagonal weights are (1,9,4,3,5); the order-5 group cyclically permutes coordinates. A monomial of degree d is C11-invariant precisely when its weighted exponent sum vanishes modulo 11. Each orbit under the C5 permutation has length one or five. A length-five orbit is one copy of every C5 character.

For each character chi, the quotient by the invariant nonzerodivisor f gives
 H_chi(cone,d)=H_chi(ambient,d)-H_chi(ambient,d-3).
The exact degree-by-degree coefficients for (chi0,chi1,chi2,chi3,chi4) are:
 d0 (1,0,0,0,0); d1,d2 (0,0,0,0,0);
 d3 (0,1,1,1,1); d4 (1,1,1,1,1);
 d5 (3,2,2,2,2); d6 (3,3,3,3,3).
At degree three, five C11-invariant monomials comprise one regular C5 module. Removing f, its one trivial vector, leaves exactly the four nontrivial characters.

With the preceding Ricci=6g and Reeb-charge normalization Q=2d, holomorphic cone harmonics have scalar-link eigenvalue Q(Q+6). The first nonconstant *trivial* F55 mode occurs at degree 4 with eigenvalue 112, whereas every nontrivial flat C5 character has a degree-3 twisted mode with eigenvalue 72. On the alternative C11 quotient, five nontrivial characters first occur at degree 1 (eigenvalue 16), five others at degree 2 (40), and the nonconstant invariant character first appears at degree 3 (72). The new code independently enumerates all monomials and subtracts each cubic ideal component, up to degree 10.

These are exact results for holomorphic flat-line sections, not full scalar KK spectra, fermion masses or experimentally observed particles.

## 2. SU5 Wilson line is not a chiral matter construction
The separate C11 quotient offers W=diag(zeta11^2,zeta11^2,zeta11^2,zeta11^-3,zeta11^-3). Its 20 off-diagonal adjoint roots contain eight invariant roots; with four Cartans its centralizer has dimension 12, SU3 x SU2 x U1. The other twelve root generators are broken. In the full F55 quotient the abelianization is C5. A flat holonomy block-scalar on 3+2 with determinant one obeys 3a+2b=0 mod 5; this forces a=b, hence it is central and cannot produce the desired SU5 breaking.

A single E6 27 decomposes under SU5 as 10+5bar+1+5+5bar+1. The code evaluates all 27 Wilson phases: all 25 nonsinglet components carry a nonzero C11 phase, and only the two SU5 singlet *constant fibers* are invariant. Nonconstant equivariant sections could exist and are not projected away by this count. A massless chiral spectrum has not been obtained.

For the smooth Sasaki-Einstein seven-link with Ricci=6g, the previous ordinary unitary-flat-twisted Dirac theorem gives D^2>=49/4, so ker D=0. A flat Wilson line alone does not produce ordinary massless internal Dirac zero modes or an observed Standard Model. Flux-coupled supercovariant/gravitino operators, singularities, nonflat gauge bundles, and localized sectors are explicitly outside this no-go.

## 3. Universal winding-mode BF obstruction from 2D lattice reduction
The repository's equal-flux M-theory/Type IIB duality report gives the mixed winding-radius branch
 lambda = 3*pi*(N0/N) * |u+v*tau|^2 / Im(tau),
 m_minus^2 * L_AdS^2 = lambda-2-sqrt(4+16*lambda)
for nonzero integer (u,v). The AdS5 BF bound is -4. Direct algebra shows
 m_minus^2*L^2 < -4  if and only if  0<lambda<12.
The bound is distinct from the separate unequal-flux homogeneous-product instability.

The classical two-dimensional Hermite invariant states
 min_(u,v) nonzero |u+v*tau|^2 / Im(tau) <= 2/sqrt(3)
for every tau in the upper half-plane. This follows by SL2(Z) reduction to |Re(tau)|<=1/2, |tau|>=1 and Im(tau)>=sqrt(3)/2. Therefore
 lambda_min <= 2*sqrt(3)*pi*(N0/N).
If 0<N0/N<2*sqrt(3)/pi=1.1026577908435842, a BF-violating mixed winding mode is guaranteed for *every* axiodilaton tau in this quadratic model. Tuning the torus cannot remove it. For ratio N0/N=1:
 - square tau=i: lambda_min=3*pi, m2*L2=-5.016944081307837, BF deficit 1.0169440813;
 - hexagonal tau=exp(i*pi/3): lambda_min=2*sqrt(3)*pi, m2*L2=-4.463541850418785, BF deficit 0.4635418504.
The hexagon maximizes the shortest-vector invariant and is therefore the least unstable shape for this branch, yet still violates BF at ratio one.

This is a new conditional mathematical corollary of the *existing* mixed-mode mass formula, not a string-theory stability theorem. In the IIB dual these are wound-string sectors omitted from a point-field supergravity truncation. Complete string dispersion, corrections, supersymmetry, Page charges, branes and the regime of validity remain open. The supersymmetric N=1 conifold at large N0/N lies outside the forced-unstable range.

## 4. The raw W(3,q) point graphs cannot themselves approximate continuum spacetime
For prime-power q, the collinearity graph of the symplectic generalized quadrangle W(3,q) is strongly regular with v=(q+1)(q^2+1), degree k=q(q+1), lambda=q-1 and mu=q+1. Its adjacency eigenvalues are exactly k, q-1, -(q+1). At q=3 these are (12,2,-4) with multiplicities (1,24,15), confirming W33 (40,12,2,4).

The normalized Laplacian I-A/k has only two distinct positive eigenvalues:
 1-(q-1)/(q(q+1)),  1+1/q.
Both tend to 1 as q grows, while the multiplicity of the lower one diverges. For each fixed ordered nonzero eigenvalue index, the first arbitrarily many eigenvalues eventually coincide. Consequently NO uniform scalar rescaling of these *raw unweighted point-graph Laplacians* can converge to the ordered Laplace spectrum of any fixed connected positive-dimensional compact smooth manifold with compact resolvent, whose eigenvalues have finite multiplicity. The point-graph diameter remains two and likewise fails as a direct geodesic lattice.

This does not exclude multiscale incidence or flag complexes, bounded-degree refinements, weighted/nonlocal operators or a nontrivial dynamical continuum. It is a precise no-go for one naive identification, not for emergent spacetime altogether.

## 5. A finite-shot, calibration-aware photonic test
For independent accepted photons, compare a declared binary output null p0=0.50 against p1=0.65. A deterministic one-sided binomial decision rule rejects the null for at least k positive outputs. Exhausting n and integer k gives the minimum n meeting both type-I and type-II <=0.01:
  n=235, k=136; alpha=0.00933211659; beta=0.00982937784.
No *deterministic integer threshold* at n<=234 meets both constraints.

With a relative plus/minus detector-efficiency ratio constrained to [1/1.1,1.1], the worst-case accepted probabilities become p0=0.5238095238 and p1=0.6280193237, requiring
  n=490, k=283; alpha=0.00959731643; beta=0.00958748117.
This is a protocol model for planning a W33 optical channel test, NOT data from a real experiment. Accepted counts do not equal source launches. IID sampling, efficiency bounds, randomization, drift controls, leakage and process-tensor interventions must be established physically. This binary control does not certify quantum temporal entanglement or causal memory.

## 6. Torsion sectors versus local flux stability
For the full order-55 quotient, the prior exact H4 torsion is Z15, equivalent by Chinese remaindering to Z3 x Z5. The new script enumerates and verifies its 15 labels. A flat degree-four differential C-field has zero de Rham G4 curvature. Merely choosing a different flat label, while holding the smooth metric and local two-derivative fields fixed, cannot repair a local homogeneous BF tachyon by changing the classical curvature equations. Torsion can still affect wrapped-brane observables, global boundary conditions, Page charges and quantum sectors; these are uncalculated.

Independently reran the existing uniform eleven-dimensional Rayleigh certificate:
 analysis/toe_20261117_11D_certified_uniform_Rayleigh_BF_0p05.py
which reports its conditional classical deficit 0.05254373018549747. This belongs to an older *different* 11D product background, not the Klein SE quotient and not the T11 winding branch above. Keep the three distinct geometries and mode sectors separate.

## Executable evidence and limitations
Producer:
 python analysis/toe_20261118_fivefront_spectral_wilson_falsifiers.py
Tests:
 python -m unittest discover -s tests -p test_toe_20261118_fivefront_spectral_wilson_falsifiers.py -v
Certificate:
 data/toe_20261118_fivefront_spectral_wilson_falsifiers.json

The producer checks six numerical/algebraic tracks and seven independent test cases. Geometric hypotheses and quantum field-theory assumptions are written explicitly; arithmetic PASS alone is not experimental proof. The collection neither derives chirality, an anomaly-free E6 vacuum, full KK or string spectra, dynamical gravity, or a theory of everything.

External mathematical/physics references:
 - Gubser and Mitra, Tpq BF bound: https://arxiv.org/abs/hep-th/0108239
 - Nguyen and Vallee, The LLL Algorithm, Hermite constants: https://www.ionica.nl/wp-content/uploads/2019/04/the-LLL-Algorithms.pdf
 - Brouwer and Haemers, spectra of generalized quadrangles: https://aeb.win.tue.nl/2WF02/spectra.pdf
 - Process-tensor operational guide: https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs

## Top five independent next tests
1. Compute full flux-coupled 11D spinor/KK operators on both Klein quotients, including Wilson-sector equivariance, charged scalar tower and anomalies.
2. Attack the universal winding result with exact full-torus momentum modes, IIB wound-string alpha-prime corrections and a controlled N,N0,tau validity diagram.
3. Derive a globally coherent E6 gauge-Higgs-matter vacuum and rigorous proton/chirality predictions; do not count SU5 centralizer as evidence of a Standard Model.
4. Implement a randomized, loss-calibrated photonic process-tensor experiment with predeclared timetag nulls and degree-matched hardware controls.
5. Build an actually local incidence/flag refinement sequence with a bounded-degree kinetic operator and prove spectral/metric continuum convergence.
