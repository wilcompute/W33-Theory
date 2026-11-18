# W33 / TOE: optimal local three-dimensional propagation, a symmetry-selection obstruction, and four global physics stress tests

18 November 2026. **Scope:** exact finite incidence and representation arithmetic, topological long-exact-sequence analysis, conditional 11D dispersion, and an explicitly modelled quantum-optics witness. None establishes 3+1-dimensional gravity, a physical three-family compactification, a complete gauge vacuum, experimental quantum memory or a theory of everything.

## Concurrent work, sources and provenance

The previous six-file packet on master, commit 50229956d, introduced noncanonical three-voltage W33 Levi covers and their exact low-energy elliptic tensor. During this research pass, the parallel assistant committed analysis/2026-11-18_E6_Morse_relative_families.md and its producer: one native complex E6 local family module, a specified five-spherical-boundary index-three system, C4 flat holonomy, vectorlike charged modes, a full Spin10 centralizer larger than the SM, a surviving anomalous U1_Psi, no complete G2 geometry. That report and its new mode/relative-complex construction were read. **The calculations below are deliberately different:** an exhaustive cycle-selector optimization plus full-symmetry no-go, a general k-boundary relative-index theorem, a minimal Z7 Wilson rescue and topological failure, a modular phase-space fraction, and adaptive photon loss budgets.

Other parent work: analysis/2026-11-18_biCayley_Peirce16_SM.md, analysis/2026-11-18_fivefront_Klein_gauge_F4_RG_winding_quantum_memory_3D_W33.md, analysis/2026-11-18_Klein_Weil_ADE_and_real_Spin7.md, and analysis/2026-11-16_D9_iib_conifold_dual.md. Previously established W33 Levi cycle rank 81 is reused rather than called a discovery.

Sources for the qualitative frameworks: Pantev and Wijnholt https://arxiv.org/abs/0905.1968; Braun et al. https://arxiv.org/abs/1812.06072; PSp and generalized quadrangles https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/simple-groups-product-actions-and-generalized-quadrangles/0C81DBE9664CD88B40616CA7D656E7BC; Minkowski's torsion-free congruence kernel in Serre's lecture https://www.college-de-france.fr/media/jean-pierre-serre/UPL3821667391778701726_6___Bounds_for_the_orders.pdf; modular geometry https://syntagmatic.github.io/moonshine/modular-forms/03-fundamental-domain.html; quantum-memory qualifications https://doi.org/10.1103/r8lf-bb4p and https://doi.org/10.1103/PHYSREVX.8.021033.

## Front I: exhaustive 81-choose-3 voltage census and an exact near-isotropic continuum

Start with the same *native* W(3,3) projective symplectic point-line Levi graph: 40 points,40 lines,80 vertices,160 edges, degree4, girth8, cycle rank81. A fixed BFS spanning tree exposes81 non-tree chords. Orient each chord from point to line. Among the 85,320 unordered triples, assign one independent Z^3 deck voltage to each selected chord, and zero to the other157 edges.

The parent integer Laplacian identity is L H=320 I-4J, with H=-L^3+20L^2-138L+376I, and L=B B^T. For all81 chords let C be the80x81 incidence columns and G_320=320 I-C^T H C. Then the exact vector response for an independent voltage on a chord equals a column of G_320/320. A fresh pure-integer enumeration proves:
- all81 diagonal entries of G_320 equal162;
- over all3240 unordered distinct chord pairs, offdiagonal values are +2 (1620 pairs), -6 (1134), +18 (324) and -54 (162);
- define anisotropy-control score S_ijk=G_ij^2+G_ik^2+G_jk^2. The absolute minimum within this explicitly restricted three-chord class is12, attained by10,152 of85,320 triples (no pair has zero response);
- lexicographically first optimum indices (0,4,8), i.e. edges (1,45),(2,50),(3,55), has G_320 submatrix [[162,2,2],[2,162,2],[2,2,162]].

Thus its exact homogenized diffusion tensor is

    D_new = 1/12800 * [[81,1,1],[1,81,1],[1,1,81]],

with eigenvalues 80/12800 (twice) and 83/12800. Anisotropy ratio is83/80=1.0375; the previous arbitrary three-chord tensor had a substantially worse ratio of approximately2.07. A new independent numerical 80x80 Bloch diagonalization at phases epsilon*(1,-1/2,3/5) checks quadratic dispersion with relative error below0.001 at epsilon=1/16.

These are exactly three *selected integer period directions*, not a physical mechanism for selecting three spatial dimensions. There are10,152 score minimizers: the chosen criterion does not produce a unique preferred frame. This optimization is exhaustive ONLY over three individual BFS chord voltages, not all integer cochains or interacting actions; it is not a claim that exactly isotropic D is impossible with a more general voltage assignment.

## Front II: full PSp4(3) symmetry actually forbids any such rank-three deck without breaking symmetry

The projective symplectic group G=PSp4(3) has order25920, is simple, and acts flag-transitively on W(3,3). We independently built the40 native symplectic transvections on F3^4 and verified the resulting orbit of a single point-line incidence comprises all160 flags. Since every edge is oriented point->line, every G-invariant edge 1-cochain is constant. But a constant cochain is exactly the coboundary of a vertex potential equal to1 on the40 points and0 on the40 lines. Consequently H^1(Levi,R)^G=0.

Suppose a connected Z^3 voltage cover were equivariant under **all** of G, normalizing the rank-three free Abelian deck translations. The induced deck automorphism is a homomorphism G->GL3(Z). The level-three principal congruence kernel of GL3(Z)->GL3(F3) is torsion-free (Minkowski). Every finite image therefore embeds in GL3(F3), of order11232. Since G is nonabelian simple of order25920>11232, every such homomorphism is trivial. The three deck cohomology classes must then be G-invariant, hence zero; this contradicts their surjectivity/connectedness.

**No full PSp4(3)-symmetric connected Z^3 voltage cover of this type exists.** A theory using these emergent three dimensions must supply spontaneous/explicit finite-geometric symmetry breaking, a different deck group, a different base complex, or a nonlinear/nonstandard symmetry realization. The obstruction does NOT exclude all W33 geometry or physically emergent spacetime. It changes the next task from "choose a beautiful triple" to "derive the choice and its symmetry-breaking dynamics."

## Front III: a general relative-cohomology family-count law and its unavoidable flat-twist vectorlike sector

The parallel E6 Morse packet specified k=5 spherical defects with four negative and one positive boundary, built a twisted local operator, and obtained nu=b1-b2=3 for all C4 flat characters, but b2=1 for nontrivial characters. Here we derive a general structural theorem for ANY k>=3 on M=L(p,1) minus k open balls, with r nonempty negative relative boundary components and s=k-r>=1 nonempty positive components.

For trivial one-dimensional coefficients, the LES of (M,Sigma_-) and H2(M,C)=ker(sum:C^k->C) gives

    b1(M,Sigma_-)=r-1,
    b2(M,Sigma_-)=s-1,
    nu=2r-k.

For any NONTRIVIAL complex flat C_p character, H0(M,V)=H1(M,V)=0 and H2(M,V)=C^k, with the boundary map to the r selected spheres of rank r; hence

    b1(M,Sigma_-;V)=r,
    b2(M,Sigma_-;V)=s,
    nu=2r-k.

The full rank census checks every k=3..12 and every 1<=r<k by explicit integer bases and projection ranks. Crucially, for ANY nontrivial flat character and at least one positive spherical boundary, **b2=s>=1**, regardless of where defects are positioned or the shape of a smooth Higgs potential. That is a topological vectorlike-partner obstruction, not a perturbative potential limitation.

If nu=3, then k is odd and r=(k+3)/2; the smallest allowed mixed-sign example is k=5,r=4,s=1. Its trivial sector has (b1,b2)=(3,0), but each nontrivial flat sector has (4,1). Increasing the number of spherical defects does not eliminate vectorlike partners; for k=7,r=5,s=2 it creates two per twisted sector. A model with a different boundary geometry, nontrivial bulk local-system cohomology, singular/non-Abelian fields, or entirely different compactification may evade the theorem. A net index by itself does not produce a clean three-family particle spectrum.

## Front IV: the smallest diagonal Wilson holonomy that kills Spin10 leptoquark generators has order seven—and both supplied geometries obstruct it

Consider a general block-constant diagonal SU5 cyclic holonomy

    W_n=diag(zeta_n^a I3,zeta_n^b I2),
    3a+2b=0 mod n, a!=b.

Inside SO10, the adjoint decomposes under U5 into u5 (25 real gauge generators) plus Lambda²5 and its conjugate (10+10bar). The SU5-preserving color/weak block retains 13 of the25 U5 generators, including the extra U1chi. The Lambda²5 charges are 2a (multiplicity3), a+b (multiplicity6), and2b (multiplicity1). Thus the SO10 centralizer dimension is exactly

    dim=13+2*[3*[2a=0]+6*[a+b=0]+1*[2b=0]].

Exhaustive cyclic-order and charge search for n=2..13 finds n=7 the first holonomy with all three bracket indicators zero: (a,b)=(1,2). Its determinant condition 3+2*2=7 is satisfied, and charges2,3,4 mod7 are all nonzero. For C4, the three admissible (a,b) are (0,2),(2,1),(2,3), giving SO10 centralizer dimensions21,19,19. This independently reproduces and generalizes the parallel C4 result.

In E6, the additional adjoint U1psi is always invariant. The spinor 16_-3 and conjugate16_+3 can be checked from the even-Fock charge set 1+Lambda²5+Lambda⁴5. For (n,a,b)=(7,1,2), a U1psi phase c=5 mod7 makes NONE of the16 charged roots invariant. The full compact E6 centralizer then has dimension14, precisely SM12 plus TWO unwanted Abelian generators. A single commuting torus Wilson line cannot reduce rank6 to SM rank4; additional Higgs physics is still required.

**Topological incompatibility:** the parallel punctured lens L(4,1) has pi1=C4. Removing spherical balls does not change pi1, so no C7 line holonomy exists. On the *different* full Klein A1 locus quotient Q/H6, our preceding packet proved an involution acts as -I on H1(Q,R). The corresponding H1(Q,F7)=(F7)^2 also transforms by -I. Here H6=C(S)/<S> is an effective order-six residual symmetry (dihedral-order-twelve centralizer modulo its central involution, so H6 is S3 rather than cyclic C6). Since |H6|=6 is invertible modulo7, finite-group transfer gives H1(Q/H6,F7)=0. Therefore it cannot support a nontrivial ordinary C7 line character either. The orbifold notion and singular-local twists must be separately analysed; this result concerns ordinary Abelian flat holonomy on the quotient.

Even replacing the lens-space order4 with order7 would NOT close the particle-physics gap automatically: the generalized relative complex would retain nontrivial-character b2>=1 and E6 would retain rank-two extra U1s. The present obstruction is for diagonal block SU5 x U1psi cyclic holonomies, not arbitrary noncommuting gauge defects.

### Independently recheck the extra E6 U1 anomaly

The parallel E6 native adjoint supplies a local charge-minus3 spinor16_-3, not the charge-plus1 spinor in the fundamental E6 27. For three net chiral16_-3 modules, direct Standard Model state counting gives

    Tr(Y)=Tr(Y^3)=0 per family,
    Tr(Psi)=-144, Tr(Psi^3)=-1296,
    SU3²-Psi=SU2²-Psi=-18, Y²-Psi=-30.

The producer independently computes these sums from Q,uc,dc,L,ec,nc representations, including color/weak multiplicities. Extra vectorlike pairs contribute zero to consistent chiral anomalies. Simply appending the conventional E6 fundamental branch 16_(+1)+10_(-2)+1_(+4) is NOT a charge-matched anomaly cancellation for these adjoint16_(-3) chiral families. A real model needs an explicit inflow, GS/Stueckelberg sector, broken anomalous U1, or new charged chirals with all anomaly conditions satisfied. No such completion is claimed.

## Front V: modular phase-space stability measure of the parent 11D winding branch

The earlier mixed-mode conditional formula is lambda=3*pi*r*min_(u,v)!=0 |u+v*tau|²/Im(tau), with r=N0/N>0, and BF violation exactly for 0<lambda<12. In the standard SL2(Z) fundamental domain F={|x|<=1/2, x²+y²>=1, y>0}, the shortest nonzero lattice vector has length one. Thus lambda_min=3*pi*r/y, and this entire branch is BF-stable iff y<=Y=pi*r/4. This is a sharp answer for every modulus under the assumed dispersion, without finite lattice truncation.

The invariant hyperbolic area of F is pi/3. Define F_stable(r) as its *normalized hyperbolic area* lying below y=Y. Direct analytic integration gives

    if Y<=sqrt3/2: F_stable=0;
    if sqrt3/2<Y<1:
      F_stable=(6/pi)*(pi/6-asin(sqrt(1-Y²))-(1/2-sqrt(1-Y²))/Y);
    if Y>=1:
      F_stable=1-3/(pi*Y)=1-12/(pi²*r).

An independent 20,001-point numerical integration agrees within2e-7 for8 sample ratios. Examples: r=1 ->0 stable hyperbolic fraction; r=1.2 ->approximately0.01322; r=2 ->1-6/pi²=0.39207; r=10 ->0.87841. No finite r gives100% because the modular cusp y->infinity remains unstable. At the critical 2sqrt3/pi, only a measure-zero hexagonal boundary shape reaches BF equality.

**Scope:** This is a geometric measure on the modular fundamental domain, NOT a dynamical probability distribution of physical vacua. It inherits every approximation of the parent equal-flux 11D mixed-mode model; higher-derivative terms, quantized charges, full KK/string spectra and backreaction remain uncomputed. The result is not a claim that all real IIB vacua are tachyonic.

## Front VI: photonic witness robustness with adaptive trials and calibrated acceptance bias

The preceding simulated causal-break qutrit memory protocol tests effective-channel Choi fidelity F>1/3 against all entanglement-breaking channels, with model target F=7/15. The minimal deterministic, two-error-<=1% binomial accepted-shot test was n292,k117 assuming probabilities p0=1/3 and p1=7/15.

**New operational improvement:** for the null, identical/independent trials are unnecessary if each trial obeys the conditional bound P(success_i|all previous accepted histories)<=p0. Coupling every Bernoulli trial to the same Uniform(0,1) draw shows its total successes are stochastically dominated by Binomial(n,p0) even under adaptive temporal correlations. An analogous conditional lower bound >=p1 controls the alternative false-negative probability. These are stronger per-history *assumptions*, not automatically true for an arbitrary laboratory or process tensor.

**Acceptance bias:** if successful and failed events can have acceptance efficiencies differing in odds by at most kappa in either direction, the conservative accepted null becomes p0'=kappa/(kappa+2), and accepted alternative p1'=7/(7+8*kappa). Both sides remain distinguishable only while kappa<sqrt(7/4)=1.3228756555... . Exact binomial search gives:

| kappa | accepted n | reject null for successes >=k |
|---:|---:|---:|
| 1.00 | 292 | 117 |
| 1.05 | 428 | 171 |
| 1.10 | 664 | 265 |
| 1.20 | 2382 | 949 |
| 1.25 | 7044 | 2805 |

Both one-sided modeled error probabilities are <=0.01 at every listed threshold. These are ACCEPTED trial counts, not photon source launches. They presume an event-ready acceptance rule, calibrated conditional efficiency bounds, trusted reference preparation and joint measurements.

Important conceptual correction to avoid overclaiming: an entanglement-breaking one-time channel is not the same as a fully classical higher-order memory process. Recent research expressly demonstrates that an EB channel can be a quantum memory resource through multitime correlations: https://doi.org/10.1103/r8lf-bb4p. Our witness tests a sufficient entanglement-preserving input-output property, not a complete process-tensor quantum-memory classification. See also https://doi.org/10.1103/PHYSREVX.8.021033.

## Reproducibility and falsifiability

Owned files:
- analysis/toe_20261118_isotropic_Levi_symmetry_no_go.py
- analysis/toe_20261118_fivefront_global_Wilson_modular_photonic.py
- data/toe_20261118_isotropic_Levi_symmetry_no_go.json
- data/toe_20261118_fivefront_global_Wilson_modular_photonic.json
- tests/test_toe_20261118_isotropic_global_Wilson_modular_memory.py
- this report.

Execute each producer directly, then run the focused unittest-discover pattern. The exact graph work checks integer polynomial identities and all 85,320 triples; finite symplectic transvections check flag transitivity; the general defect calculation checks all selected ranges by long-exact-sequence rank arguments; group/charge and anomaly arithmetic is explicit; modular measures have independent quadrature; photon tails use exact binomial distribution evaluations rather than normal approximations.

## Top 5 independent next steps

1. **Find a dynamical three-direction selector:** formulate a W33-invariant microscopic action whose spontaneously broken phases select an ordered rank-three voltage lattice and a Lorentzian causal sector. Test all 10,152 graph-optimal triples and all null ranks.
2. **Produce a global chiral compactification:** replace the spherical-boundary abelian toy model with a verified G2/weak-G2 flux-coupled operator, localized gauge source, full twisted local-system index and a genuine anomaly/inflow cancellation.
3. **Repair the Wilson/Higgs topology jointly:** seek a gauge-supporting singularity with allowable higher-order holonomy, a fully computed E6 adjoint centralizer, broken extra U1s, and no compulsory vectorlike charged zero modes. Do not substitute an order-seven lens for a full solution.
4. **Compute the full winding/string stability operator:** include finite flux quantization, T-dual winding sectors, higher-derivative and brane corrections and a mass-matrix bound; report phase-space measures only after a physical modulus measure is specified.
5. **Build the experimental process-tensor witness:** specify source, detector, Bell-basis measurements, timing, causal breaks, event-ready heralding, and adaptive confidence bounds; test against both EB and genuinely quantum multitime-resource alternatives.
