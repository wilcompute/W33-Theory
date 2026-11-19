# Twisted flat geometry: a genuine cup escape with an exact mirror/Higgs obstruction

Status: six conditional mathematical probes, with executable witnesses. No complete compactification, Standard Model spectrum, or TOE is established.

## What changed, and what was actually read

This review follows the twelve commits `cb1a66717..d5edaa9a0`, plus `eaedca990`. All twelve earlier reports, their thirteen producer scripts and thirteen test modules were read; their 250 tests passed in 96.65 seconds with `--noconftest`. All thirteen JSON certificates were regenerated in isolation and matched their published parsed structures exactly; 37 checked repository artifact hashes stayed unchanged. The additional `eaedca990` report, producer and tests were read in full; its sixteen tests passed in 2.93 seconds. These checks cover that committed delta, not every historical file or the unrelated dirty local work.

The new parallel work constructs a renormalizable singlet messenger vacuum, tests actual overlap indices and causal-state gates, and identifies two algebraic Green--Schwarz shift directions. These are conditional results, not one globally consistent physical model. The singlet vacuum is locally isolated in its stated EFT; it does not itself calculate matter localization or Yukawa overlaps. The new two-direction anomaly factorization still needs quantized inflow. This packet leaves all those files intact.

Anchors: `analysis/2026-11-19_balanced_E8_sources_and_bulk_cup_gate.md`, `analysis/toe_20261119_uv_messenger_orbifold_causal_vacuum_followup.py`, `analysis/2026-11-19_TOE_five_physics_fronts_singlet_cups_hierarchy_capacity.md`, `analysis/toe_20261119_causal_exchange_gauge_homerun.py`, and `analysis/2026-11-19_TOE_two_GS_axions_causal_signed_layer_five_gates.md`.

During this work `b9e08278a` and further local extensions arrived. We read the current full causal-topology report, producer and tests, including its Wilson-determinant and normalized-history additions. All 58 tests passed in 2.56 seconds. Calling `combined()` in memory exactly reproduced its eight-gate JSON, SHA256 `21c6f2d1bcf6a82d4d5592dab8228971ecae70a415099a59e7de377d8989c5e7`, without rewriting it. The external topology reproduction receipt was read; its large upstream runs are the parallel track's recorded results, not runs repeated here. We verified that the cited [November 2026 preprint](https://arxiv.org/abs/2611.06102) exists; its proposed cosmological/axion conclusions have not been independently established by this packet. The order-nerve topology work supports using more than the contractible whole order complex; its spin-center selection remains explicitly conditional on the supplied fermions, sector weights and zero-source determinants.

## 1. Separate ordinary adjoint modes from twisted Yukawa classes

The punctured-S3 strict relative bulk cup in the source model vanishes. A punctured T3 can restore a cup but also introduces ordinary adjoint modes. A different test is a closed flat base with zero ordinary first Betti number and nonzero *local-coefficient* first cohomology.

Use the known Hantzsche--Wendt manifold Q=T3/V4 with free affine generators

```
a(x,y,z)=(x+1/2,-y+1/2,-z),
b(x,y,z)=(-x,y+1/2,-z+1/2).
```

The nontrivial elements rotate about the x,y,z axes and translate by half a period along that axis. Thus the action is free. Let chi_x,chi_y,chi_z denote the three nontrivial characters of V4. Parallel dx,dy,dz transform in those characters, respectively. Averaging torus harmonic forms gives

```
H*(Q;C)             : (1,0,0,1),
H*(Q;L_chi_i)      : (0,1,1,0),
chi_x chi_y chi_z  = 1.
```

Consequently the twisted triple cup is nonzero: integral_Q dx dy dz=1/4 for a unit-volume torus cover. With each constant one-form individually L2-normalized the product is 2. This is a chosen metric normalization, not a predicted physical Yukawa coupling.

This geometry and its gauge/geometric interpretation are **prior art**. [Barbosa, section 5.2](https://arxiv.org/html/1910.10742) studies its G2 orbifold and flat SL2 character variety. [Acharya--Baldwin](https://arxiv.org/html/2312.12311) relate flat ADE connections on compact flat three-manifolds to ALE-fibered G2 structures. The contribution here is an explicit higher-rank spectrum/deformation test against the repo's cup/adjoint problem. Searches for the named geometry, those arXiv IDs, the resulting Betti sequences, and the formulas below found no earlier matching packet in the searched index, dashboard, analysis Python and Markdown. This is a scoped corpus search, not proof of literature novelty.

Ordinary b1=0 does not prohibit twisted desingularizations: the [Joyce--Karigiannis construction](https://arxiv.org/abs/1707.09325) includes a twisted setting. A global torsion-free compact ADE construction with the desired matter is still required; no such construction is asserted here.

## 2. Full E8 detects the misleading three-family count

Embed V4 into SU4 using rho=diag(1,chi_x,chi_y,chi_z). Its determinant is one. Under Spin10 x SU4,

```
248=(45,1)+(1,15)+(16,4)+(16bar,4bar)+(10,6).
```

At zero Higgs field the twisted H1 components are 3(16)+3(16bar)+6(10)+12(1), dimension 168. There are three spinor labels **and three mirrors**, with net chirality zero. These can equally organize as three 27/27bar pairs plus six E6 singlets; the unbroken gauge algebra is enhanced.

The full H0 has 80 generators: 45+3+16+16bar. Checking all 240 standard E8 roots, the fixed roots number 72, span rank six and each have twenty dot-product-one neighbors, identifying E6; the remaining two Cartans are Abelian. Thus the algebra is e6+u1+u1, rather than the naive Spin10 plus three Cartans. The global gauge group is not specified just by that algebra. Ordinary adjoint H1 for this unbroken algebra is absent because b1(Q)=0.

The twisted cup permits off-diagonal 16_i 16_j 10_(i xor j) contractions. A diagonal pair repeats the same one-form and has zero bulk wedge. Hence even the nonzero topology does not automatically generate arbitrary physical flavor textures. Most importantly it has not removed mirrors.

## 3. Try a globally non-split Higgs field, then count every sector

Index the SU4 basis by V4. Define P_i e_j=e_(j xor i) for i=1,2,3. These are commuting traceless Hermitian involutions, P_1 P_2=P_3, and rho(g) P_i rho(g)^(-1)=chi_i(g) P_i. Therefore

```
phi=a_x dx P_1+a_y dy P_2+a_z dz P_3
```

is a globally defined parallel Higgs one-form with d_A phi=d_A*phi=0 and [phi wedge phi]=0. Its eigenbasis is only locally labelled; the deck group permutes the eigenlines. The complex differential convention is d_A+phi with the displayed Hermitian matrices. This is a concrete way around an argument that assumes a globally fixed Cartan coefficient and ordinary b1. It uses the established spectral-cover framework cited above.

For arbitrary real nonzero values on each selected axis, the torus-cover Hodge operator is a positive sum of momentum squares and Higgs-generator squares. Only constant forms in their joint kernel survive. We compute that kernel in 4, wedge2(4) and End(4), remove the scalar identity, and average over V4; a separate Walsh-basis calculation checks the joint weights.

| Number of active axes | Number of subsets | Full E8 twisted Betti dimensions H0,H1,H2,H3 |
| --- | --- | --- |
| 0 | 1 | 80,168,168,80 |
| 1 | 3 | 46,46,46,46 |
| 2 | 3 | 45,23,23,45 |
| 3 | 1 | 45,3,3,45 |

Every P_i is invertible in the fundamental, so **any nonzero real axis deformation removes all the 16 and 16bar cohomology together**. With three axes active the vectors also disappear, leaving the Spin10 gauge algebra and three singlet H1 moduli. This family does not retain three chiral generations, and its generic endpoint is not an isolated vacuum. Nonparallel singular fields or changed operator domains could alter this conclusion; they are different models requiring their own calculation.

There is also no ordinary parallel spinor on this flat three-manifold. Spin lifts of the a,b rotations square to -1, forcing antiperiodic spin transport on all three cover translations; the ordinary Dirac square is bounded below by 3*pi^2 for unit lengths. Twisted gauge-theory form zero modes must not be presented as ordinary untwisted spinor zero modes. A genuine ADE/G2 construction must supply the required twist.

## 4. Strengthen the flavor constraint and quantify the kinetic escape

For a complex symmetric hollow 3x3 Yukawa matrix the repo established s1<=s2+s3. In fact equality holds: **s1=s2+s3**. Three diagonal field rephasings make all off-diagonal entries nonnegative real. The resulting real symmetric matrix has zero trace and, when all edges are nonzero, positive determinant: one positive and two negative eigenvalues. Perron--Frobenius makes the positive eigenvalue largest in absolute value; trace zero proves the equality. Vanishing edges follow by continuity. This is elementary matrix theory, not a new general theorem.

We checked 256 random complex examples and the disconnected/zero-edge limits. The exact reasoning, not those examples, is the proof. For positive kinetic metrics,

```
Yphys=KL^(-1/2) Y KR^(-1/2),
s1(Yphys)/s2(Yphys) <= 2 sqrt(kappa(KL) kappa(KR)).
```

This follows from extremal singular-value bounds for multiplication by invertible matrices. If both fields share K, a ratio 100000 needs kappa(K)>=50000. That is a necessary bound, not a sufficient construction. Mild kinetic corrections cannot silently generate an enormous hierarchy from this texture. The newer diagonal singlet/messenger operators change the hollow premise; their actual physical overlaps and light-Higgs projection remain open, as the parallel report correctly states.

## 5. Unbiased causal response has a separate noise gate

The charged causal-kernel producer constructs a Poisson falling-factorial estimator: replace s^n by (2/rho)^n (N)_n with N~Poisson(rho*s/2). Its expectation is the desired supplied-background radial kernel. For a **real finite polynomial** f, exact factorial-product moments give

```
Var[fhat]=sum_(r>=1) (2s/rho)^r/r! [f^(r)(s)]^2.
```

The r=0 contraction is the squared mean. An independent direct second-moment contraction verifies the identity with exact rational coefficients. It is a finite case of established [Poisson chaos/Fock-space methods](https://arxiv.org/abs/0909.3205), not a new stochastic theorem.

For the full massless constant-electric-field kernel f(s)=J0(qE*s/4), one need not assume convergence of every chaos term to obtain a useful necessary bound. Any regular square-integrable **count-only** estimator unbiased for all positive volumes has Cov(fhat,N)=lambda*(2/rho)*f'(s); Cauchy--Schwarz gives Var>=2s[f'(s)]^2/rho. Infinite variance does not improve this bound. With s=4 and qE=1, the mean is about 0.7652 and the variance is at least 0.0968223/rho. At rho=0.001 its coefficient of variation is therefore at least 12.8. Exact unbiasedness alone cannot establish a useful low-density continuum estimator. This is a lower bound, not an evaluation of the full variance or a claim about the newer signed-layer observable's correlated noise.

Sprinkling noise is not quantum vacuum noise. It neither selects a Wightman state nor supplies fluctuation-dissipation physics. Likewise, the new signed causal-layer expectation in `eaedca990` does not by itself bound its variance; interval counts are correlated and need their own pair-interval calculation.

## 6. Follow the new anomaly factorization down to its integral shift lattice

The two shifts in `eaedca990` are (2,1,1) and (0,1,-5). Their 2x3 integer matrix has Smith factors (1,2). For an independent product U1^3 with 2*pi angles and two 2*pi axions, that shift map has a Z2 group of disconnected kernel components in addition to its continuous U1. Its primitive continuous direction is (-3,5,1). This is the standard integer-lattice description of compact axion gauging; see [the Stückelberg EFT discussion](https://doi.org/10.1007/JHEP04(2015)175). Other fields or the actual E8 central quotient can change the final gauge group.

An explicit saturated lattice in the same rational plane has basis u=(1,0,3), v=(0,1,-5). The previous shifts equal (2u+v,v), an index-two sublattice, so these are **different periodic axion models**, not equivalent integral changes of axion coordinates. Their Smith factors are (1,1). Moreover the new formal anomaly decomposition has entirely integer polynomial coefficients:

```
P=(a+3c)*(20a^2+2ab+2ac+17b^2+34bc+29c^2)
 +(b-5c)*(10a^2+ab+ac+16b^2+23bc+13c^2),
2a+b+c=2(a+3c)+(b-5c).
```

Thus two shifts can still factor the original cubic and mixed anomalies without half-integral coefficients in this *formal normalization*. Tests reconstruct P independently from the original charged fermions and verify the identity, primitive kernel and maximal-minor gcds. This does not establish correctly normalized quantized WZ couplings or supersymmetry, and does not predict a physical Z2 symmetry. It identifies a concrete global-periodicity choice the eventual UV inflow calculation must distinguish. The vector [1,0,3] alone already occurs in unrelated repo matrices; searching its role and the combined shifts found no earlier equivalent anomaly-lattice calculation in the searched corpus.

## Reproduction and the next independent tests

Run `python analysis/toe_20261119_twisted_flat_E8_higgs_and_noise.py`, then `python -m pytest --noconftest -q tests/test_toe_20261119_twisted_flat_E8_higgs_and_noise.py`. The JSON stores all eight branches, the root census, exact polynomial variance witness and full-Bessel score bounds. Tests also check non-diagonal kinetic metrics and zero-edge limits. Numerical residuals can vary at floating-point roundoff across BLAS implementations.

The final combined run of this packet's fourteen tests and the parallel anomaly packet's sixteen tests passed all thirty in 11.00 seconds. The separate 58-test causal-topology suite also passed, as recorded above. The earlier 250-test regression was not rerun without a new failure or affected dependency. These checks cover 338 distinct tests across the stated suites, not the entire repository test collection.

Five independent next tests: (1) add an explicitly defined singular matter/defect domain to this base and compute its index and cups together; (2) construct an ADE fibration realizing the V4 monodromy and test compact torsion-free gluing; (3) derive the kinetic metric and light-Higgs projections in the existing messenger model; (4) compute quantized inflow for the parallel two-axion anomaly factorization; (5) compute correlated pair-interval variance for the signed causal-layer observable. Each addresses a different missing physical input.
