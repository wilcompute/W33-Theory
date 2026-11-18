# A harmonic quartic with exactly three local PW chiral modes

18 November 2026. This is a noncompact charged-operator result in the actual exterior-form PW system. It is not a compact G2 solution, a derivation of three observed generations, or a completed Standard Model.

## The operator matters

The previous packet **ccdd3fe07**, `analysis/2026-11-18_E8_H27_index_parity_and_Callias_escape.md`, constructed a bounded non-Abelian scalar mass with auxiliary Callias index magnitude three. It explicitly did not derive the physical seven-dimensional Clifford coupling; its conjugate-block test prevents reading that index as three four-dimensional chiral multiplets. Its finite-energy trial also fails its scalar field equation.

Here we instead use the PW exterior differential on a flat local three-manifold:

    d_f=d+df wedge, D_f=d_f+d_f^dagger,
    D_f=sum_i a_i partial_i+sum_i b_i partial_i f,
    a_i=dx_i wedge-iota_i, b_i=dx_i wedge+iota_i.

The eight-component exterior algebra has grading Gamma=(-1)^form-degree. The producer checks all Clifford anticommutators with integer matrices. In the partially twisted seven-dimensional SYM dictionary, odd forms describe left-handed four-dimensional zero modes and even forms right-handed ones; this identification, including the reality relation, comes from [Braun, Cizel, Huebner and Schaefer-Nameki, equations2.34–2.44](https://arxiv.org/html/1812.06072v2#S2.SS3). We do not impose a new chirality projection.

There is also a useful obstruction to one attempted interpretation of the earlier scalar texture. If that scalar is placed in only one PW Higgs component, the resulting full exterior operator is

    D_single=sum_i a_i nabla_i+b_3 Phi.

The unused constant matrix b_1 anticommutes with D_single and Gamma and satisfies b_1^2=I. It bijects even and odd kernels whenever it preserves the operator domain. Thus this particular full-module construction has zero graded index. Boundary or orbifold projections can invalidate the pairing, but require a specified physical domain. This is not a no-go for three-component Higgs backgrounds, nor a claim that the old auxiliary operator was itself a PW operator.

## An exact harmonic background

Choose w=x+iy and

    f=Re(w^4)/4-(x^2+y^2)/2+z^2.

Then Delta f=0 exactly. For a constant Cartan generator H, A=0 and phi=H df solve F_A-i[phi,phi]=0, d_A phi=0 and d_A^dagger phi=0 on all R3. These are the standard PW equations, not newly proposed field equations. The supplied quartic is an explicit new local test of them against the previous native E6 module.

The full critical set is the origin and (plus/minus1,0,0),(0,plus/minus1,0). At the origin the Hessian eigenvalues are (-1,-1,2), giving Morse index two. Each of the four outer points has (-4,2,2), giving index one. Their signed sum is 1-4=-3. Counting only the four outer Gaussian states would be incorrect.

## Exact L2 count, beyond critical-point counting

Write f=f2(x,y)+z^2. The planar gradient, encoded as a complex number, is conjugate(w)^3-w. For its homotopy conjugate(w)^3-tw, 0<=t<=1, the gradient magnitude is at least r^3-r. It is proper, with winding -3; at r=2 it is at least six uniformly. The Hessian grows only quadratically while the squared gradient grows sextically. These are strongly tame confining operators, with unique self-adjoint closure and compact resolvent.

The noncompact Witten index theorem gives the planar even-minus-odd index -3. The applicable tame framework and index formula are established results of [Dai and Yan, Theorem1.3](https://arxiv.org/html/2011.05468#S1.SS3). In flat two-space its integral is pi^-1 integral exp(-|grad f2|^2) det(Hess f2), the degree of the proper gradient. The producer independently integrates its angular-reduced Bessel expression and obtains -3.0.

This determines the total kernel, not merely a net count: any planar degree-zero zero mode is C exp(-f2), and any degree-two zero mode is C exp(f2) dx wedge dy. Neither is L2, since f2 tends to both signs of infinity in open angular sectors. Consequently the planar kernel is exactly three-dimensional and entirely degree one. The independent z oscillator has one degree-zero ground state proportional to exp(-z^2), with first positive eigenvalue four in the chosen mathematical normalization. Tensor factorization therefore gives

    dim H^k_L2(d_f)=(0,3,0,0).

For negative effective charge, Hodge duality gives (0,0,3,0). This supplies the CPT-conjugate profiles, not three additional independent left-handed mirror multiplets. For the specified charged local operator, there are exactly three left-handed profiles and no opposite-chirality zero modes in that block.

## Independent spectral checks

The producer builds the planar one-form Hamiltonian in a Hermite Galerkin basis. Position powers are evaluated in a padded basis before restriction; taking powers of a prematurely truncated position matrix would give the wrong boundary matrix elements. With V=|grad f2|^2,

    H_scalar=-partial_x^2-partial_y^2+V,
    H_1=[[H_scalar+6(x^2-y^2), -12xy],
         [-12xy, H_scalar-6(x^2-y^2)]],
    H_0=H_scalar+2, H_2=H_scalar-2.

| Basis per coordinate | Largest of first three Ritz values | Fourth Ritz value |
|---|---:|---:|
|16|0.001082|1.036700|
|24|0.00001668|1.036137|
|32|0.0000003401|1.036112|
|40|0.000000007186|1.036111|

Residuals are below 1.2e-10 in these runs. A different oscillator width gives the first three values below 1.1e-6 and fourth1.036113. The even degree-two lowest Ritz value approaches1.036111. These are numerical convergence checks; they do not prove an infinite-dimensional spectral lower bound. The exact count comes from the index and vanishing argument above. No dimensional eigenvalue is asserted to be a measured particle mass.

## A C4 triplet that an untwisted quotient would erase

For f2<-c with c>1/4, the negative sublevel has four contractible ends. Its reduced degree-zero cohomology is three-dimensional, with C4 cycling the ends. The relative-cohomology interpretation of tame Witten theory is given by [Dai and Yan, Theorem1.3 and Corollary1.4](https://arxiv.org/html/2005.04607#S1.SS3). Here it identifies the kernel representation with the reduced regular C4 representation. Equivariant localization or continuation preserves that representation; the critical-point complex has a regular four-state degree-one representation and one invariant degree-two state.

An exact integer matrix on the sum-zero four-end space has characteristic polynomial (u+1)(u^2+1). The numerical low-three-state rotation has eigenvalues (-1,i,-i) at every tested resolution, leakage below7e-15. Thus there is no invariant mode. A simultaneous gauge character i^k would retain respectively (0,1,1,1) profiles for k=(0,1,2,3).

This is a compatibility gate for any proposed C4 projection of THIS axial local model. The axial action has a fixed z-axis; it is not identified with the free lens-space deck action in **580972009**. A global quotient must be built before transplanting these numbers. This triplet is reducible under C4 and is not the irreducible H27 flavor representation.

## Native E6 connection and the remaining physics

The certificate in **580972009**, `data/toe_20261118_E6_Morse_relative_families.json`, already constructs the actual E6-adjoint decomposition 16_-3+46_0+16bar_3 and identifies the first spinor with the native Peirce/Fock family. Choosing H=-Psi/3 makes the 16_-3 effective charge positive. The present localizer supplies three spatial profiles for that same representation, with the dual degree-two profiles required by reality. It improves the earlier local Gaussian construction by establishing the full charged L2 kernel in one explicit smooth harmonic background.

It does not repair the old E6 Psi anomalies, gauge rank, Higgs vacuum or zero bare two-family adjoint cubic. Nor can this be transplanted into all of E8 and declared three families: under the common T hypotheses of ccdd3fe07, nu=3 would give net spinor index2nu=6. That prior obstruction remains.

Most importantly, the number three is still supplied. For every integer m>=3,

    f_m=Re(w^m)/m-|w|^2/2+z^2

is harmonic and has exactly m-1 degree-one L2 profiles by the same argument. The outer critical Hessians are (-m,m-2,2), with m outer points and one origin of index two. Choosing the quartic is choosing m=4; this does not select the observed generation number from W33 or dynamics.

On R3, df grows cubically and its ordinary scalar kinetic integral diverges. Solving the local BPS equations does not supply a finite-energy compact vacuum. Constant unbroken gauge profiles are not L2 here, so normalizable four-dimensional gauge fields require a global completion. The ambient torsion-free G2 metric, source/gluing problem, anomaly inflow, actual Higgs modes and Yukawa overlaps remain unbuilt. Fixed non-Abelian H27 holonomies cannot be appended without verifying the full Higgs bundle compatibility.

Run `python analysis/toe_20261118_PW_Clifford_A3_localizer.py` to regenerate the owned certificate. Only the producer, this report and its JSON are publication scope. Parallel work and shared continuity/index files are preserved.
