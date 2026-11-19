# TOE six-way new physics audit: Pascal/Sierpiński mass hierarchy, relative flux, SU5 Higgs spurion, causal mass, photon dephasing

**November 19, 2026 | Independent calculations and falsifications, not a physical Theory of Everything.** Concrete new-to-repository exact models plus numerical certificates; **the central 3+1 Lorentzian G2/chiral/source problem remains unsolved.**

## Current-repository baseline and outside research

Synced connected Windows clone and GitHub master at c98ed7e23, following dba7c8d10. Read actual master source analysis/toe_20261119_multicopy_particle_ssr_pascal_chsh.py and its complete companion report, plus analysis/toe_20261119_handlebody_W7_topological_trilemma.py and recent H27 SIC-MUB mass/wall commit c98ed7e23. This paper is NEW analysis beyond:
- 25207be19 Lucas/odd-binomial CHSH maximum under local particle-number SSR: S_n=2+(2sqrt2−2)[1−2^(popcount(n)−n)]. No one-photon BQP or mass derivation.
- dba7c8d10 genus-four handlebody cohomology 3 families per Spin10 spinor weight but 148 adjoint H1 components, zero absolute H2 and hence zero ordinary bulk triple-cup; 12 source charge-allowed Yukawas from two tens; split-octet mass projector under a FROZEN H; exact BDG4 smearing variance; ordinary photon-erasure correction.
- c98ed7e23 2026-11-19 H27 sextic global-SUSY toy whose support-two SIC vacua have scalar Hessian mass-squared (0,81,81), support-three MUB vacua have (81,81,81) and a conditional BPS domain wall. This is a distinct mass model, NOT a measured mass prediction.

Web literature checks:
- Actual charged-lepton reference values and other particle data: 2026 PDG https://pdg.lbl.gov/2026/listings/particle_properties.html
- Fractal symmetry in interacting bosons: Pascal's Triangle Fractal Symmetries, PRL128 115301 (2022), https://doi.org/10.1103/PhysRevLett.128.115301 . This existing lattice-fractal physics is PRIOR ART, not a claimed proof of fundamental mass.
- Mathematical fractal *graph Laplacian* spectral decimation depends on an explicitly selected Laplacian and boundary forms: https://arxiv.org/abs/1709.02031 . The mod2 Pascal matrix studied below is **not** itself that graph Laplacian.
- Horodecki 1995 two-qubit CHSH criterion (correlation tensor T^T T) and operational summaries: https://www.nature.com/articles/s41598-023-35015-9 .
- Poincare-Lefschetz relative cohomology with local coefficients: https://encyclopediaofmath.org/wiki/Poincar%C3%A9_duality
- Chiral fermion domain-wall localization and anomaly inflow are established Callan–Harvey physics (1985), https://doi.org/10.1016/0550-3213(85)90489-4 , and Kaplan's 1992 domain-wall lattice construction https://doi.org/10.1016/0370-2693(92)91112-M . The new result below is the CONDITIONAL combination with the repo's H27 wall and Lucas-Pascal Gram, not a discovery of domain-wall fermions.
- Chiral G2 defects and local fermion matter: https://arxiv.org/abs/hep-th/0109152 .
- SUSY SU5 24F and higher-dimensional Higgs operators: contemporary neutrino adjoint models; the mass operator below is a *candidate spurion construction*, not sourced 5D brane physics.
- Known causal-set scalar d'Alembertian and smearing: https://doi.org/10.1007/s41114-019-0023-1 .

## Front 1 (user-prioritized) — An exact Pascal-mod2 hierarchy, and a precise THREE-GENERATION mass falsifier

Take rows/cols 0<=n,k<2^L and let P_L[n,k]=C(n,k) (mod2), regarding parity as the ordinary REAL number 0 or 1. Lucas theorem gives digit factorization

    P_L = A^{tensor L}, A=[[1,0],[1,1]].

All matrices are triangular and have det1. Their singular values can be solved exactly: A has singular values φ and φ^-1, φ=(1+sqrt5)/2, so

    m_j/m0 = φ^(2j−L),  multiplicity C(L,j), j=0,...,L,
    lambda_j(P_L^T P_L)=φ^(4j−2L),
    log det(P_L^T P_L+mu² I)=Σ_j C(L,j) log(mu²+φ^(4j−2L)).

The code independently forms actual dense 2^L matrices for L1..6, checks each Kronecker/parity identity and numerical SVD, and checks the entire massive determinant on levels2..5 at four mu² values. Thus the spectrum is exact and self-similar **IF** one physically imposes this real parity matrix as a canonical Yukawa operator. The global mass scale m0, family selection, 4D gauge representations, canonical Kähler metrics, and actual M2 amplitudes are NOT obtained by Pascal combinatorics.

Three-family test #1: the upper-left 3x3 Pascal truncation P3=[[1,0,0],[1,1,0],[1,0,1]] has Gram eigenvalues 2−sqrt3,1,2+sqrt3 and singular-value ratio **2+sqrt3=3.73205**. Compare charged-lepton tau/electron ~approximately **3477.37**, using the 2026 PDG tau mass of 1776.93 MeV, mu/electron ~206.77 from quoted PDG reference masses (they are not a universal common high-scale running ratio). The model fails by ~930fold on the largest ratio. A full dyadic block requires L>=9 to span tau/e extremes, giving at least 512 flavor-like coordinates and highly degenerate binomial levels, NOT 3 observed families. A global scale cannot fix these ratios.

Three-family test #2 (novel topology link): in the previous H4 source the three residual handles represent three independent generator cycles. Embed these three generators naturally as one-hot bit labels (1,2,4) of the first nontrivial 8x8 Pascal square. The resulting 3x3 submatrix is exactly **I3**: all three mass singular values are equal and there is NO mixing or hierarchy. This is a possible natural embedding, not a proof that all physically allowed embeddings do this.

### Crucial predictivity check: an arbitrary kinetic metric can fake ANY observed mass spectrum

For any invertible P3 and target positive normalized diagonal D=diag(me/mtau,mmu/mtau,1), choose

    K_R = P3^T D^(-2) P3  > 0.

Then after right-handed canonical normalization Ycanon=P3 K_R^(-1/2),

    Ycanon Ycanon^T = P3 K_R^(-1) P3^T = D².

Therefore the three singular values of Ycanon are **EXACTLY** the observed desired positive masses. This is a tautological construction and demonstrates **zero predictive mass content** once unconstrained Kähler/right-handed kinetic metrics are admitted. In the actual E8 source, different family U1 charges may forbid nontrivial K_R until gauge breaking; the proof is conditional on allowing arbitrary positive K_R. The code constructs an exact rational K_R and checks its positivity and spectrum. It is a counterexample to treating a fitted φ pattern as a real particle-mass derivation.

### A weighted thermal/fractal fingerprint, with missing dynamics

Odd Pascal positions have per-bit options (n_j,k_j)=(0,0),(1,0),(1,1). For positive weights alpha,beta the exact finite fractal partition is

    Z_L(alpha,beta) =
        Σ_{n<2^L} Σ_{k subset n} exp(−alpha*n−beta*k)
      = Π_{j=0}^{L-1} [1+exp(−2^j alpha)+exp(−2^j(alpha+beta))].

At alpha=beta=0, Z=3^L. This is a valid **statistical partition function only if a microscopic model supplies the energy E(n,k)=alpha*n+beta*k**, not a mass from an unexplained thermal parameter. Pascal support's geometric scaling gives Hausdorff exponent log3/log2; do not substitute it for the spectral dimension of a separately chosen Sierpiński graph Laplacian, or for 3+1 spacetime dimension.

## Front 2 — Can the genus-four topology's MISSING Yukawa cup be repaired by a RELATIVE flux?

Previous result: genus-four handlebody H4 retracts to wedge of four circles. For nontrivial flat C7 line χ, d0=(χ−1,0,0,0), H1(H4;Lχ)=C³, H2_absolute=0. In this complex the three residual cycles are the independent family labels. Poincare-Lefschetz duality supplies

    H2(H4,∂H4;Lχ^-1) ≅ (H1(H4;Lχ))* = C³.

The cup pairing H1_absolute(Lχ)×H2_relative(Lχ^-1)->H3_relative is nondegenerate and can be represented by exact I3 on the dual bases. That gives a **nonzero relative-flux-induced bilinear**, even though all ORDINARY 1+1+1 bulk cup Yukawas remain zero. A relative-flux toy with diagonal coefficients (1,2,3) breaks the residual permutation symmetry; its three eigenvalues are distinct. More generally for symmetric Yukawa Y=aI+b(J−I), introducing ε diag(-1,0,1) splits the doubly degenerate family doublet at first order by exactly **2ε/sqrt3**.

This offers a concrete search target in G2 singular geometry: derive the **gauge-compatible relative two-form flux or defect operator**, its quantization, holonomy character χ^-1 and real overlap coefficients, and verify the full chiral matter/adjoint spectrum. **Warning:** a background relative H2 class is NOT the same as a third ordinary H1 field; it does not magically produce a gauge-invariant renormalizable Yukawa or mass a truly isolated Weyl representation without the appropriate conjugate state/Higgs insertion. Extra selection rules are required. This is an algebraic mechanism hypothesis and an exact *topological* pairing, not an actual compact G2 gauge vacuum.

## Front 3 — Correct the SU5 mass projector: spontaneous Higgs SU5 covariance vs FROZEN boundary breaking

The previous GUT source had 24_H background H=diag(2,2,2,-3,-3) and fixed-color projection Pc=(H+3I)/5. For arbitrary adjoint fermion X define

    P8(X;H)=Pc X Pc − tr(Pc X)*Pc/3.

The rank on the SU5 24 is exactly8 (color octet); corresponding SU2 projector rank3. The previous calculation correctly showed P8(U X U†; H_fixed) ≠ U P8(X;H_fixed) U† when U mixes color and weak indices. But when H is treated as an actual adjoint Higgs **spurion that transforms** H→UHU†, we instead have exactly

    P8(U X U†;U H U†) = U P8(X;H) U†.

We verified this numerically against 40 independently sampled SU5 unitary gauge-frame changes, while the frozen-H transformation has order-one defect. Therefore Tr[P8(24F;24H)^2] is **SU5 gauge invariant as a polynomial Higgs-mass operator** in the full parent theory, although the vacuum selects a broken SU3×SU2×U1 direction. This relaxes the claimed necessity of an explicitly SU5-breaking brane mass for an octet-selective term; it does NOT guarantee that the supersymmetric holomorphic superpotential, heavy UV messengers, G2 Wilson compactification, or full KK spectrum generate the polynomial with the needed coefficients.

P8 is polynomial in up to H² times X, and the mass-square term in up to H⁴ X². That means a collection of nonminimal operators, not one arbitrary renormalizable 24F²24H Clebsch. The unavoidable shared-multiplet Clebsch constraints from minimal renormalizable SU5 are NOT evaded without a genuinely sourced nonminimal interaction and spectrum. Full 2-loop gauge/Yukawa running, anomaly and proton amplitude remain prior tasks, not solved here.

## Front 4 — Mass cannot FIX noisy causal gravity, and a fake mass can be a cutoff sign error

Take previous known BDG4 four-layer operator B_(rho,eps) evaluated on finite 4D Minkowski future cones with exact analytic continuum constant-field expectation (prior script toe_20261119_BDG4_bias_variance_gate.py). Add a local Klein-Gordon mass:

    B_mu[f](x)=B[f](x)+mu² f(x).

For fixed input field f at fixed x, this is a deterministic shift. Thus **Var(B_mu[f])=Var(B[f])** for any mu. It cannot solve stochastic causal fluctuations. 120 independent parent sprinklings for each of three cases verify this exact fact.

If one tries to infer a 'physical mass' by setting the cutoff-BDG constant-field mean to zero, one obtains mu²_counter=-E[B(1)]; at parent rho100 eps.2 the required mu² is approximately **-1.2616** (tachyonic sign), whereas at parent rho200 eps.2 it is **+3.4720**. One fixed universal positive mass cannot represent this density-dependent finite-volume subtraction. The original smearing strongly reduces variance in this toy, but no microscopic Lorentzian quantum-gravitational mass, Einstein spin-two action or renormalization condition is derived. The negative counterterm could be allowed as a regulator subtraction only after a full renormalized field theory; it is NOT evidence for a physical tachyon.

## Front 5 — Pascal-SSR + DIFFERENTIAL energy/mass phases give a concrete decoherence law

Existing 25207be established exact ideal n-copy CHSH under strict local particle number SSR and arbitrary number-preserving joint observables. New extension: in the two-copy setup, the local one-photon sector has total probability1/2 and conditional two-qubit state

    rho_1 = 1/2[|01><01|+|10><10|
                  +c|01><10|+c*|10><01|].

If relative path-phase difference is δ=(DeltaE)(δt1−δt2), with *independent* Gaussian timing jitters δti of variance σt², then |c|=exp[−(DeltaE σt)^2]. The two-qubit correlation tensor has squared singular values (1,|c|²,|c|²). By the Horodecki CHSH criterion S_sector=2sqrt(1+|c|²). The other local-number sectors remain classical at value2. Therefore the exact **SSR-restricted optimum with this noise model** is

    S_2(x)=1+sqrt[1+exp(−2x²)],  x=DeltaE*sigma_t.

Direct 4x4 density-matrix correlation-tensor diagonalization verifies the result at x=0,.25,.5,1,2,3. At zero differential phase noise S=1+sqrt2~2.4142; x1 gives~2.0655; x2 gives~2.00017, approaching the classical bound2.

**Important:** common unknown phase cancels in the relative phase δ and does not decohere this two-copy resource. Distinguishable photons can have optical frequency/energy splitting, not a claimed nonzero photon REST mass. The parameters DeltaE and σt are externally supplied, and optical measurement compilation, loss, heralding and calibration remain missing. This is standard QM's measurable *mass/energy-related dephasing*, not a new Born-rule prediction or evidence that Pascal fractals create mass.

## Front 6 (outside-box, strongest constructive toy) — Pascal Gram eigenchannels on the prior H27 SIC→MUB BPS wall produce EXACTLY three gapped chiral zero modes

The concurrent repo commit **c98ed7e23** produced a *global SUSY toy* wall interpolating between H27 sextic F-flat support-two SIC and support-three MUB configurations. Its real scalar follows

    W(x)=x³−x⁶/2, F=W'(x)=3x²(1−x³),  x'(z)=F(x(z)),
    W''(x)=6x−15x⁴,
    x(-infty)=0, x(+infty)=1, W''(-infty)=0, W''(+infty)=−9.

Now construct the **hypothetical** five-dimensional first-order Dirac domain-wall mass operator

    D = partial_z − [m0 I + W''(x(z)) K_L],
    K_L=P_L^T P_L,

where P_L is the canonical *real* mod2 Pascal matrix from Front1, K_L is positive Hermitian, and m0>0 is one input common bulk mass. The eigenmasses of K_L are λ_j=φ^(4j−2L), multiplicity C(L,j). Each eigenchannel has profile

    m_λ(z)=m0+λ W''(x(z)),
    m_λ(-infty)=m0>0,  m_λ(+infty)=m0−9λ.

A normalizable chiral zero mode of D f=0 exists exactly if **0<m0<9λ** (strict endpoints), with profile

    f_λ(z)=const*exp(m0*z) [x'(z)]^λ.

Its opposite-chirality partner has no normalizable zero mode in that sign regime. For **L=2**, K2 has FOUR eigenvalues

    λ=(φ^-4,1,1,φ^4)=(0.145898,1,1,6.854102).

Choose ANY common bulk mass in the OPEN interval

    9φ^-4≈1.313082 < m0 < 9.

Then the λ=φ^-4 channel has equal positive signs at the two ends and does NOT localize, while λ=1 (twice) and λ=φ^4 have opposite signs and DO localize: **exactly THREE left-chiral 3+1 zero modes out of four 5D starting channels**. This count is stable against localized perturbations leaving both asymptotic spectral gaps open, because the first-order domain-wall index counts asymptotic sign changes. This is a genuine Fredholm 1D toy (not the earlier non-Fredholm zero-offset case). Code checks the exact mass eigenvalues, analytic wall equation, count across multiple open-interval masses and outside the interval.

An essential adversarial test: At m0=0, the same model *appears* to yield three normalizable profiles because x'~|z|^-2 at the SIC end, and the exact norm is

    ||f_λ||² = 3^(2λ−2) B((4λ−1)/3,2λ), convergent iff λ>1/4.

However m(-infty)=0 makes the Dirac operator **non-Fredholm**. A small positive m0 below the first λ threshold changes the count to FOUR; a small negative constant mass has no selected left-chiral modes. This is NOT a topologically protected chiral count until the common asymptotic mass gap is supplied.

**Physics verdict: a concrete mathematical mechanism to obtain three normalizable 4D chiral zero modes from one Pascal-derived 5D mass matrix plus the existing H27 wall, over an OPEN parameter interval.** Still NOT three observed Standard Model families: the 5D action, common m0, coupling K2, scalar wall field/representation, 4D gauge reps, anomaly inflow, E8/G2 embedding, observed charged masses and precise field normalizations are not derived. The two λ=1 modes remain degenerate. The 4D zero modes are massless before electroweak Higgs overlaps. If each channel were hypothetically a complete Spin10 16, three copies contain 12 SM SU2 Weyl doublets and pass that one Witten parity check, but this does not solve all local/global anomalies or source E8 holonomy.

**Quantitative index-preserving flavor split:** at m0=2 the spectral threshold is m0/9=2/9. The distance of the nearest Pascal Gram eigenvalue to this threshold is about0.076324. Weyl's eigenvalue perturbation bound therefore guarantees that any Hermitian flavor perturbation ΔK with operator norm <0.076324 leaves exactly three localized chiral modes. One explicit **rank-one positive** deformation of norm0.05 in the original four-bit basis gives four distinct eigenvalues (splitting the twofold λ=1 degeneracy) while retaining the same index3. This exhibits an open **index-preserving flavor-breaking direction**, not a derived mechanism for observed masses. It makes the next missing object a sourced defect coupling ΔK with the right gauge and anomaly properties.

**Additional rank caution:** a single rank-one, factorized defect/Higgs coupling produces at most rank-one charged-mass matrices regardless of the number of chiral zero modes. To obtain three independent nonzero charged eigenmasses, one must derive several independent overlap channels or a nonfactorizing microscopic coupling, and explicitly lift the λ=1 degeneracy without losing the 3-mode index. A second source of chirality or symmetry breaking is necessary; the new wall only supplies a family-number *selector*.

Producer: analysis/toe_20261119_pascal_H27_BPS_wall_chiral_selector.py
Certificate: data/toe_20261119_pascal_H27_domainwall_three_chiral_modes.json
Tests: tests/test_toe_20261119_pascal_H27_BPS_wall_three_chiral.py

## Front 7 (independent synthesis) — Which actual missing input would make these bridges predictive?

For particle masses:
  (1) A compact chiral 3+1 G2/Spin10 source with physical gauge and Higgs reps and full SUSY anomaly closure;
  (2) a selected relative-flux/defect class that genuinely couples χ and χ^-1 local systems;
  (3) canonical source kinetic/overlap metrics (not arbitrary fitted positive K), a family projection and L/R Yukawas;
  (4) a nonminimal 24F/24H UV operator spectrum and proton-safe two-loop/KK thresholds.
Only THEN can Pascal self-similarity, if dynamically sourced, be judged against the charged-lepton and quark hierarchy.

For geometry/gravity:
  a normalized quantum causal measure, first-class constraint algebra, Lorentzian spinor transport, positive propagating spin2, bias+variance control for arbitrary fields.

For single-photon quantum computing:
  finite polynomial mode/gate/ancilla overhead, fault-tolerant logical entanglers and an independently predicted deviation from ordinary quantum process theory. Pascal CHSH already follows from established QM and is not evidence for a TOE.

## Reproduce

    python analysis/toe_20261119_pascal_sierpinski_mass_spectrum.py
    python analysis/toe_20261119_TOE_relative_flux_SU5_mass_causet.py
    python analysis/toe_20261119_pascal_H27_BPS_wall_chiral_selector.py
    python -m pytest --noconftest -q tests/test_toe_20261119_pascal_mass_relative_flux_photon.py

JSON certificates:
- data/toe_20261119_pascal_sierpinski_mass_spectrum.json
- data/toe_20261119_relative_flux_SU5_covariant_mass_cutoff.json

Code tests exact matrix/SVD, positive metric, low rank source pairing, SU5 covariance, mass+causal stochastic invariance and 4x4 CHSH density-matrix criteria. Relevant nearby earlier Pascal/causal/particle test suites should also pass; broad all-date regression may contain parallel files and requires running on current master.

### Top five *independent* next research experiments

1. Derive a dynamical **three-family projection of the dyadic Pascal tensor**, ideally from E8/Spin10 G2 gauge/defect chirality rather than selecting 3 of 2^L labels, then prove it does/does not produce real mass ratios without freely fitted Kähler metrics.
2. Quantize the **relative H2(M,∂M;Lχ^-1) flux** at the singular gauge locus, calculate a nonzero physically gauge-invariant overlap/instantonic Yukawa, and check adjoint-exotic lifting, holomorphic selection, true F/D-flatness and mass splittings.
3. UV-complete the **SU5-covariant Higgs-spurion octet projector** with renormalizable heavy messengers or explicit compactification modes and calculate complete 5D SUSY multiplet masses, KK thresholds, two-loop flavor RG, discrete anomalies and dimension-five proton decay.
4. Construct a **finite-state causal quantum gravity operator** whose measured field mass and spectral density survive density refinements, have bounded fluctuations, provide a healthy Lorentzian spin2 sector and satisfy quantum first-class gravitational constraints, rather than interpreting cutoff bias as a mass.
5. Compile an **event-ready optical mass/energy-dephasing SSR witness** with calibrated differential timing noise and compare to standard quantum-process theory. Its measured spectrum is a consistency baseline; a genuine TOE falsifier needs a separate derivation of how this prediction differs from QM.

**Claim discipline:** exact finite linear algebra and statistical physics are established; none of the required full dynamical physical completions has been constructed in this pass. The Pascal mass matrix is a useful falsifiable toy, not a derivation of observed physical masses.
