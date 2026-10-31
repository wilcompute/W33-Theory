# Eight W33 frontiers with three deliberately speculative physics falsifiers
**Date:** 2026-10-31. **Scope:** finite proof/computation and explicitly supplied experimental models; NOT an established TOE.

Source: analysis/w33_20261031_eight_front_physics_falsifiers.py
Supplemental group module: analysis/w33_20261031_torsion_order5_probe.py
Frozen data: data/w33_20261031_eight_front_physics_falsifiers.json and data/w33_20261031_torsion_order5_probe.json
Tests: tests/test_w33_20261031_eight_front_physics_falsifiers.py

The five investigations are numbered according to the preceding five proposed next steps. Then follow three independent, deliberately unconventional ideas with explicit acceptance/rejection criteria. Every model input and limitation is stated. No experimental data were collected.

## 1. Icosahedral characteristic-five torsion and a genuine group action

The October 31 prior packet already computes a 24x24 integer biadjacency matrix B of the exceptional 48-line W(3,9) orbit, with SNF diag(1^11,5^7,0^6). Its integral cokernel is Z^6 plus (Z/5)^7. The intersection graph has 48 vertices, 240 edges, is connected and has cycle rank 193, distinct from the seven torsion directions.

This round computes the actual action of an explicit **order-five automorphism** of that graph. The 13-dimensional nullspace of B mod5 has a six-dimensional subspace obtained by reducing the rational/integral zero-kernel. Restricting the automorphism P to this quotient defines a seven-dimensional unipotent operator. The modular ranks of (P-I)^j on the quotient are:

r_0=7, r_1=4, r_2=2, r_3=0 (and zero thereafter).

The Jordan decomposition is **J3 plus J3 plus J1**. A separate graph-isomorphism search finds explicit order-two and order-three symmetries as well (all three orders found after 55 graph automorphisms). Their dimensions of the fixed subspace on this seven-dimensional characteristic-five quotient are **4 for order 2, 3 for order 3, and 3 for order 5**; the rank sequences are respectively [7,3,3], [7,4,4,4], and [7,4,2,0,0,0]. These modular invariants constrain any conjectural decomposition: in particular a naive 1+3+3' split into ordinary icosahedral rotation modules would have only three order-two fixed directions, whereas this representative has four. These are exact finite calculations (integer permutations, mod-5 elimination), and an unusually informative representation-theoretic fingerprint beyond the SNF. They are automorphisms of the **abstract intersection graph**; the script does not independently certify these particular permutations as images of symplectic matrices in the Pass12501 stabilizer. Full A5-module identification, full character data and an equivariant map to a physical carrier remain open.

## 2. The 54D interferometer in an explicit phase/noise/loss control

The October 31 compiler supplies two orientations of 27 parallel real three-mode interferometer blocks. We construct every actual 3x3 signed-permutation conjugate to the canonical U=2vv^T-I and independently perturb two Givens angles and two pi phase shifters by iid normal errors of RMS 0.01 rad per block (fixed seed 31031). The resulting unitaries are exactly unitary up to machine precision.

Use the standard d-dimensional unitary average gate fidelity formula

F_avg(U,V) = (|Tr(U^dag V)|^2+d)/(d(d+1)), d=81,

including coherent phases **across different triangles**, rather than averaging block fidelities incorrectly.

The measured **simulation** results are plus F_avg=0.9994014315, minus F_avg=0.9995344028. A coherent same global phase on every block gives F_avg=1, but relative inter-block phases can be observable for a photon coherently spread across triangles.

Separately *assume* homogeneous power survival eta=0.995 at each of five optical circuit stages. The overall survival is eta^5=0.9752487531. This is a power-transmission budget, not inferred from tomography or a validated channel model. No claim is made for a physical fault-tolerance threshold.

The question now becomes how much fabrication error, phase calibration and crosstalk the architecture tolerates; the mathematical ability to compile 54D gate is already established.

## 3. A local clock model and the fatal accidental symmetry

The previously committed October 31 local Gaussian mediator already supplies E(a,b)=3-Tr(Pi_a Pi_b) on the 120 two-qutrit rank-three tick events, with values {0,2,3}. This is a conditional microscopic local interaction, not something derived from the underlying W33 geometry alone.

We explicitly reconstruct the 120x120 transfer matrix T_ab=exp(-0.7 E_ab) and verify its entire exact spectrum:

- lambda0 = 1+2x^3+117x^2, multiplicity 1;
- lambda1 = 1+2x^3-3x^2, multiplicity 39;
- lambda2 = 1-x^3, multiplicity 80;
- x=exp(-0.7).

The one-dimensional correlation length is 0.28288174 sites and the finite-temperature transfer state is uniquely symmetric. We also explicitly swap two entire three-outcome event directions and verify E is unchanged. There are **arbitrary S40 permutations of the forty event directions** and S3 permutations within each, an enlarged S3 wreath S40 symmetry.

Thus this mathematically local mediator cannot distinguish two tick directions solely according to their W33 collinearity. A geometry-selecting clock needs new operator data / interactions, not merely a stronger coupling of the same overlap form. The unconditional E8 real form, physical time direction, and N/M entropy ratio are not derived.

## 4. A real two-dimensional topological index, with the input exposed

Our older paired balanced finite W33 regulators had zero chiral index. As a positive *external control* we implement the standard two-band Qi-Wu-Zhang lattice Hamiltonian:

H(k)=sin kx sigma_x + sin ky sigma_y + (m+cos kx+cos ky) sigma_z.

A discretized Brillouin-zone lattice-gauge Berry calculation (Fukui-Hatsugai-Suzuki method) gives lower-band Chern values

m=-3:0, m=-1:-1, m=1:+1, m=3:0,

on N=21. Refinements N=11,17,25 agree for m=-1. Defining the antiunitary partner H_minus(k)=H_plus^*(-k) reverses the Chern sign for every tested mass without closing the gap.

This demonstrates an explicit local and spectrally gapped route to an integer topological index, but the crucial 2D lattice Hamiltonian, complex hopping and mass are *externally supplied*. It does not generate a Standard Model Weyl fermion, a four-dimensional anomaly, nor a physical CP sign from W33.

## 5. A finite-speed growing periodic carrier with native acoustic metric

The earlier Pass12192 and October 23 Round 9 files derive the metric Q=G/rho, reused unchanged here:

Q=[[5,5/2,-3,0],[5/2,5,0,-3],[-3,0,6,-3],[0,-3,-3,6]].

Define the exact positive lattice symbol lambda(k) = p(k)^dag Q p(k), p_mu=e^(ik_mu)-1, and the *supplied leapfrog equation*:
u(t+1)=2u(t)-u(t-1)-dt^2 L u(t), L>=0.

The analytic bound lambda(k) <= 4 sum_{mu,nu}|Q_{mu,nu}| yields a sufficient stable time step dt <= 2/sqrt(4 sum |Q|), namely 0.1490711985. We choose half this bound, dt=0.0745355992 and test the full 8^4 momentum grid. The nonzero stencil contains only offsets 0, +/- e_mu, +/- (e_mu-e_nu). Consequently the explicit update has **strict finite influence** of Manhattan radius at most two sites per discrete step.

On fixed integer momentum m=(1,2,1,0), the scaled symbol converges to m^T Q m=35 with relative errors 0.16956, 0.04499, 0.01142, 0.002865 for refinements 8,16,32,64.

This is a constructed, anisotropic 4D spatial lattice with one *externally supplied discrete time*. It supplies a mathematically well-defined local propagating field and an acoustic cone in the long-wavelength limit, but it DOES NOT derive physical c, general covariance, Einstein equations, or a Lorentzian spacetime from bare W33.

## 6. Outside-box physics idea: does Z5 torsion turn into a synthetic photon?

A graph connection with values in Z5 can be constructed, but it is not unique. Choose a spanning tree of the 48-line intersection graph; the 193 remaining chords index 193 fundamental cycles. Put one primitive fifth root of unity on a selected chord, unit phases on every other edge. Under arbitrary site gauge rephasings by Z5, its four-edge Wilson loop remains unchanged to ~1e-16.

This is a **positive synthetic gauge-control construction** and a negative answer to the claim that the seven 5-torsion generators *automatically* specify seven flux quanta. The raw graph has 193 possible independent cycle flux choices, and no canonical equivariant injection from the incidence torsion has been specified. A physical photon also requires an action, kinetic term and coupling to charged probes, none derived.

## 7. Outside-box physics idea: single-photon directional-gate experiment

On the actual canonical weighted skew triangle F=[[0,1,-3],[-1,0,2],[3,-2,0]], define the two quarter turns U_pm = I+F^2/14 +/-F/sqrt14. Prepare one photon in mode 1, measure one of three output modes.

The two ideal output probabilities differ, with exact one-shot total variation:

D_TV(P_plus,P_minus)=12/(7 sqrt14)=0.45816212899.

An additional *exact finite multinomial Bayes decision calculation* assumes equal orientation priors, independently prepared photons, fixed calibrated gates, and ideal output-port measurements. The minimum equal-prior probability of error is one half the sum, over all three-port outcome histograms, of the lesser of the plus and minus likelihoods. At one photon it is 0.2709189355. To make the error strictly below 0.001 requires **23 detected photons** (error 0.00093918765); strictly below 1e-6 requires **54 detected photons** (error 9.4964e-7). If instead each of the five optical stages independently transmits photon power eta=0.995 and a lost photon is a heralded uninformative no-click, mixing the exact binomial detection count into the Bayes errors increases those thresholds to **24 and 56 injected photons**, respectively. These are *ideal benchmark sample sizes*, not detector-inclusive experimental guarantees. Arbitrary memory, detector dark counts, phase drift, mode-dependent loss, imperfect state preparation and non-IID errors are absent.

The reciprocal compiled pi pulse I+F²/7 is exactly independent of F sign, furnishing a matched negative control. This is a proposed operational directional readout in a *declared fixed optical basis*, NOT a spontaneous handedness selection, observed CP violation or identified microscopic arrow of time.

## 8. Outside-box physics idea: can W33 internal multiplicity bootstrap a Chern band?

Tensor the external 2D topological Hamiltonian with the real W33 adjacency:

H_total(k)=H_QWZ(k) tensor I_40 + epsilon I_2 tensor A_W33, epsilon=0.01.

W33 A has eigenvalues 12^1,2^24,(-4)^15. The two sectors remain gapped for the chosen m=-1 because the external gap is 2 while the maximum occupied/unoccupied band-offset overlap is only 16 epsilon=0.16. The 40 occupied bands have total Chern number 40 times the external two-band Chern: -40; the antiunitary partner has +40.

This is an **exact tensor-product decomposition**, not a discovered 40-fold intrinsic anomaly. W33 contributes internal multiplicity but does not choose chirality or generate nonzero Chern number without an already chiral external spatial Hamiltonian. This is a control against false claims that internal geometry alone predicts the particle spectrum.

## Scientific audit

**Five original fronts tested** and **three new independent model/obstruction ideas tested**, with exact algebra where possible. "Executing" a test is not the same as completing the open problem of real-form selection, manufacturing a real device or deriving gravity. The code prints named results and stops on false assertions. Validation is in a dedicated pytest file; numerical tolerances and randomized seeds are fixed.

Relevant literature:
- Fukui, Hatsugai, Suzuki (2005), J. Phys. Soc. Japan 74, 1674, DOI 10.1143/JPSJ.74.1674, lattice-gauge Chern method.
- Qi, Wu and Zhang (2006), Phys. Rev. B 74, 085308, DOI 10.1103/PhysRevB.74.085308, topological two-band lattice prototype.
- Ginsparg and Wilson (1982), Phys. Rev. D 25, 2649, DOI 10.1103/PhysRevD.25.2649. A Chern insulator does not circumvent the four-dimensional gauge-index/anomaly requirements of chiral fermions.
- Older W33 Passes 11062, 12192, 12501; October 23 Round 9; October 31 rate entropy, local tick mediator and ideal 54D beam-splitter compiler.

## Best independent next work

1. Establish an actual 5-modular character module for the exact Pass12501 A5 stabilizer and prove or disprove 1+3+3 structure beyond the order-five Jordan fingerprint.
2. Run hardware-realistic coupled-mode simulations with imperfect ports, detector dark counts and nonuniform losses; then propose a chip geometry and measurable falsifier.
3. Replace the geometry-blind tick overlap with an H27/W33-dependent gauge-invariant local term and prove the accidental S40 symmetry is truly broken without a gratuitous chosen direction.
4. Couple the *native* 40-mode/81-mode logical operation to a gapped topological band through an explicitly gauge-covariant interaction, then test anomalies and locality.
5. Promote the artificial periodic wave equation to a dynamical metric theory with a quantitative low-energy observable; reject it if generic perturbations destroy continuum scaling.
