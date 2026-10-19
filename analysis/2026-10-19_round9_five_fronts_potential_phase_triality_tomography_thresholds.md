# W33 Round 9 — Five frontiers: vacuum frame, exact two-tick phase, triality, photon tomography, scalar thresholds

**19 October 2026.** Research against current master including parallel Passes 12066–12070. Tested in isolated worktree, leaving main checkout untouched. Physics scope: finite mathematics and synthetic optical tests, not a demonstrated TOE or new experimental law.

## 1. Clifford-invariant vacuum potential and operator-frame theorem
Starting from the previous Round 8 orbit of 1440 rank-two stabilizer-pair projectors Q and stabilizer order 2916, construct all Q as sums of rank-one Pauli context states in Mat9(C). They obey

- sum_Q Q = 320 I9;
- the 81-dimensional complex Hermitian operator frame spectrum is **640 once, 28 eighty times**;
- for Qc=Q-2I9/9, the centered frame has spectrum **0 once, 28 eighty times**, and Tr(Qc^4)=182/243 for every orbit point;
- a fixed Q0 has several overlaps Tr(Q0 Q), including 0,1/3,4/9,2/3,1,4/3,2, so two-vacuum interactions are NONTRIVIAL.

**Exact no-selection statement:** The full two-qutrit projective Clifford group acts transitively on these 1440 discrete Q. Therefore any on-site Clifford-invariant scalar potential V(Q) is **constant on that orbit**, whether quadratic, quartic or arbitrary degree. Such a potential CANNOT select a unique rank-two vacuum absent explicit/spontaneous symmetry breaking or extra terms. Interactions between two Q can select relative types but retain group-related degeneracies. This says nothing about dynamics selecting a unique vacuum among continuous SU9 conjugates. Prior generalized Clifford methods: Hostens et al. (2004), https://arxiv.org/abs/quant-ph/0408190.

## 2. Exact two-tick free-energy convexity and the unresolved full phase diagram
For every pair among all **4860** distinct noncommuting outcome-projector pairs P,Q, compute and verify PQP=P/3 in 9x9 matrices. A normalized two-tick mixture M=(1-w)P+wQ has eigenvalues
\[
\lambda_\pm=\frac{1\pm\sqrt{1-\frac83 w(1-w)}}2
\]
each multiplicity 3, plus zero multiplicity 3. Define u=w(1-w), C=4u/3. Then
\[
F_T(u)=1-T\log\left\{3\left[1+2e^{1/(2T)}
\cosh\left(\frac{\sqrt{1-\frac83u}}{2T}\right)\right]\right\}.
\]
It is **strictly convex in u for every T>0**. Proof: set a=8/3, x=sqrt(1-au), z=x/(2T), c=e^(-1/(2T))/2 in (0,1/2). Then F'_T(u)=(a/(8T))g(z), g(z)=sinh(z)/[z(cosh(z)+c)]. Since
\[
-z^2(\cosh z+c)^2 g'(z)
=(1-c)(\sinh z\cosh z-z)
+c(\cosh z+1)(\sinh z-z)\ge0
\]
and z decreases as u increases, F'_T is increasing. Thus F(u)-F(0)>=F'(0)u.

**Theorem:** Within ALL two-tick states (commuting or noncommuting), single tick is optimal exactly for kappa >= -(3/2)(1-e^(-1/T))/(3+6e^(-1/T)). At T=.5 this is **-0.3402395316**. Earlier work derived the one-sided singleton threshold; new here is full two-tick convexity and exact support-two sufficiency. The complete 120-variable global threshold remains OPEN because three-or-more-support states could intervene.

## 3. Two-clock E6 cubic and classical Spin(8) Jordan coordinates
**Prior work explicitly credited:** Parallel Pass12064 already constructed 27=3*1+8_v+8_s+8_c; Pass12067 ALREADY certified the 45 E6 tritangent monomial orbits (one clock 9+36; noncollinear pair one fixed monomial; collinear pair three disjoint fixed monomials). These counts and leading rank-one versus diagonal texture observation are not newly discovered here.

**Independent exact tensor census:** Write the three trinification blocks A=(3,bar3,1), B=(1,3,bar3), C=(bar3,1,3) as three 3x3 matrices. The four SU3-cubed invariant cubic tensors detA,detB,detC,Tr(ABC) contain 18 determinant and 27 cross-sector monomials = **45 distinct E6 cubic weight monomials**. The E6 cubic imposes a specific combination among four generic SU3-cubed invariants.

**Classical octonion coordinate formula:** J3(O)=R^3+O^3, dimensions 3+8+8+8=27. The Jordan cubic abc-a||v||²-b||w||²-c||z||²+2Re((vw)z) is cyclic in the three singlets and octets. Checked numerically by explicit 8D Cayley-Dickson multiplication including norm multiplicativity and cyclic triality. Abstract one-versus-three bipartite monomial contributions can support rank-one versus diagonal rank-three textures after suitable VEVs, but **the required W33 E6 weight-to-octonion coordinate change of basis is NOT constructed**, and the example mass matrices are schematic. No Yukawa values, SM generations or observed masses follow.

## 4. Fully specified ideal photon-count complex transfer tomography
Upgrade the previous post-loop transfer-matrix inverse W=R^-1S to a **measurement-level 36-setting design**.

In a balanced single-photon two-path interferometer, put Uref=F3 tensor F3 in the reference arm (all 81 entries modulus 1/3), and the unknown 9x9 lossy transfer T in the signal arm. Prepare each of nine internal basis inputs j; for each use reference phase phi=0 or pi/2. Resolve nine output modes in BOTH paths plus an erasure outcome: 19 possible outcomes per configuration.

The observed path probability difference at output k obeys
\[
D_\phi(k,j)=p_+(k,j;\phi)-p_-(k,j;\phi)
=\operatorname{Re}[e^{i\phi}\overline{U_{\rm ref,kj}}T_{kj}],
\qquad
T_{kj}=\frac{D_0-iD_{\pi/2}}{\overline{U_{\rm ref,kj}}}.
\]
Run two conditions: identity-loop calibration R=M and signal loop S=MW. In all there are **2 conditions x 9 inputs x 2 phases =36 settings**, with all nine outputs counted simultaneously. Solve W=R^-1S.

A synthetic 19-outcome multinomial experiment used 40,000 input photons per setting (**1.44 million total**) and 120 independent repetitions, including coherent crosstalk epsilon=.16 and heterogeneous signal-path amplitude losses .68-.96. Ideal W33 deficit is 8/27≈0.296296. Simulated estimate mean **0.296562**, standard deviation **0.004508**. Noiseless inversion recovers complex transfers. Stale calibration induces phase-drift bias. No device built; real source brightness, thermal phase locking, detector efficiencies/dark counts, phase-gauge alignment and physical chip fabrication remain open.

## 5. Conditional permutation-symmetric scalar vacuum phase and threshold-ratio obstruction
Let x_i=Tr(Phi_i^dag Phi_i)>=0 and take a minimal S3-exchange-invariant radial toy potential
\[
V(x)=-m^2\sum_i x_i + b\sum_i x_i^2 +c\sum_{i<j}x_i x_j,
\quad m^2,b>0,\ c\ge0.
\]
Since V=-m²S+(b-c/2)sum(x_i²)+(c/2)S², at fixed S=sum x_i we have S²/3<=sum x_i²<=S². Its GLOBAL minima are exactly:
- **c<2b:** all x_i=m²/[2(b+c)] (equal VEVs);
- **c>2b:** three symmetry-related single-condensate minima, permutations of (m²/(2b),0,0);
- **c=2b:** an entire flat nonnegative simplex sum x_i=m²/(2b).

Even if symmetry fixes equal VEV magnitudes, physical thresholds M_i=y_i sqrt(x_i) depend on independent Yukawa values unless they too are equated by a justified symmetry. In the earlier one-loop beta pair bUV=9,bIR=11, example y=(1,2,4) creates IR scale ratio (M3/M1)^(2/11)=**1.286665** instead of 1 for equal y. Thus equal gauge couplings and symmetric scalar quartics alone do not predict a unique physical mass ratio. This is NOT a physical E8(-24) Higgs potential; no gauge index orientation, vacuum alignment, ghosts/quantum UV completion or measured particle spectrum modeled.

## Reproduction / evidence hierarchy
Five machine-readable results are produced by the five analysis scripts:
- analysis/w33_20261019_round9_vacuum_frame_potential.py
- analysis/w33_20261019_round9_two_tick_convexity.py
- analysis/w33_20261019_round9_triality_cubic_texture.py
- analysis/w33_20261019_round9_photon_tomography_shots.py
- analysis/w33_20261019_round9_symmetric_higgs_thresholds.py

Tests are in tests/test_w33_20261019_round9.py. Exact finite structure: operator frame, support-two Pauli spectrum, convexity inequality, SU3-cubed monomial count and toy-potential minimizers. Numerical/synthetic: octonionic multiplication checks and photon-count outcomes. Physics still open: a measured parameter-free prediction, unique vacuum dynamics, Yukawa masses, global 120-variable phase criticality, and fabricated optics.
