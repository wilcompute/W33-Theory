# E8 H27 flavor completion: an extra antifamily, an even-index obstruction, and an explicit gapped Dirac escape

18 November 2026. Exact E8 lattice/representation and local-system tests, plus a specified continuum Callias operator. **No physical three-family compactification, G2 solution or theory of everything is established.**

## Why test the full embedding now?

Commit **36eb8d951**, `analysis/2026-11-18_linked_wire_H27_Novikov.md`, gives an exact linked T(2,6) complement and rank-three coefficient bundle with one relative S2 boundary and (b1,b2)=(3,0). It explicitly leaves the flavor bundle's gauge origin unresolved. The parallel **c0ca57dab** report supplies the minimal-seven ancillary representation; the later local producer `analysis/toe_20261118_H27_explicit189_intertwiner_reynolds.py` realizes that mathematical encoder numerically. An H27 encoder does not by itself add a flavor gauge bundle to an E6-adjoint16.

Here we test a standard larger gauge realization instead of silently adjoining three copies. E8 contains Spin10 x SU4, up to its common center quotient, and

    248=(45,1)+(1,15)+(16,4)+(16bar,4bar)+(10,6).

This branching is established literature; see [Donagi, He, Ovrut and Reinbacher](https://arxiv.org/abs/hep-th/0405014). The independent E6 x SU3 comparison uses the representation identities in [Leontaris and Shafi, section2](https://doi.org/10.1140/epjc/s10052-016-4432-y). Only their branching tables are used, not that article's phenomenological proposal.

During this calculation the parallel track published **2e73d03b7**, `analysis/2026-11-18_AdS5_BF_H27_E8_isometries_linked_Higgs_memory_CI.md`. Its explicit248x27 H27 Fourier embedding already proves that an E6-adjoint16_-3 is flavor-singlet and that a regular27 encoder spans inequivalent E6 charge sectors. Its Chi-parity test also obstructs two parallel singlet condensates if the finite sign is identified with the common gauge Chi twist. Those findings are prior work, not discoveries of this packet. The additional test here is the *complete localized E8 charge inventory*, its2nu index restriction, neutral linked complexes, and the explicit gapped finite-energy SU4 Dirac alternative.

## Full E8 root census, tied to the native charge dictionary

The producer generates all240 standard E8 roots: 112 of the form +/-e_i +/-e_j, and128 half-integral sign vectors with even minus parity. It checks every one of57,600 root reflections. Splitting the first five coordinates from the last three gives40 D5 roots,12 D3 roots,60 mixed vector roots and128 spinor roots. Adding eight Cartan generators gives248.

In these coordinates choose

    T=-2(e6+e7+e8).

On the SU4 spinor4, T has eigenvalues (1,1,1,-3). All16 weights in the flavor-singlet Spin10 spinor are matched individually to the existing clock-Albert/Fock certificate `data/toe_20261118_biCayley_Peirce16_SM.json`: chi=2N-5 and the actual 6Y charges agree. The order-seven Wilson phases also agree individually with36eb8d951's native dictionary. This is a concrete charge-level match, not a completed Albert-to-E8 bracket isomorphism.

The full T grading is:

| T | -4 | -3 | -2 | -1 | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Root multiplicity | 3 | 16 | 30 | 48 | 46 | 48 | 30 | 16 | 3 |

The grade-zero algebra has dimension54 after adding the Cartan: Spin10(45), SU3(8) and U1_T(1). Roots orthogonal to the flavor SU3 give the72 roots of E6, whose decomposition is precisely45_0+1_0+16_-3+16bar_3. Thus the T here is the Psi of that E6 branching, rather than a new unexplained charge.

## H27 is a genuine SU4 subgroup, but its commuting Higgs is restricted

Use the certified three-dimensional clock/shift matrices X,Y with [X,Y]=omega I3. Embed them as diag(X,1), diag(Y,1) in SU4. Solving the full matrix commutant constraints gives exactly one traceless complex direction:

    Lie centralizer_SU4(H27) = C * diag(1,1,1,-3).

This does not permit independent triplet and singlet scalar localizers while keeping a parallel commuting H27 background and Spin10 intact. The full branch under SU3 x U1_T is

    4=3_1+1_-3,
    6=3bar_2+3_-2,
    15=8_0+1_0+3_4+3bar_-4.

On the linked complement pi1=<a,c | [a,c^3]=1>, a compact example is

    a=diag(X,1), c=diag(v XY,v^-3), v^5=1.

It generates H27 x C5 of order135, verified by group closure. On any nonzero E8 T grade q, the central fiber c^3 acts as v^(3q) I; it is never1 for q=+/-1,+/-2,+/-3,+/-4. The linked Fox complex is therefore acyclic in each charged sector by the contraction proved in36eb8d951.

The prior Spin10 order-seven Wilson can be appended, giving abstract finite image H27 x C5 x C7 of order945. A charged central-fiber eigenvalue is zeta35^(21q+15k), never1 because its exponent is q modulo5. The same eight invariant D5 roots and six retained Cartan directions give14 candidate gauge generators, including two extra U1s. This is a consistent group/complex calculation, with the geometry, source action and physical fluctuation domains still unspecified.

## The three apparent families include an additional antifamily

Take the earlier one-relative-sphere model with a common harmonic localizer along T. Fix the sign convention so T-positive sectors see the relative sphere and have rank(V) degree-one classes. T-negative sectors see complementary boundary conditions and yield the CPT-conjugate left-chiral representation. Count each conjugate pair once:

| Left-chiral multiplet | T | Copies |
|---|---:|---:|
| Spin10 16 | 1 | 3 |
| Spin10 16bar | 3 | 1 |
| Spin10 10 | 2 | 3 |
| Spin10 singlet | 4 | 3 |

Thus the net Spin10 spinor-family index is **3-1=2**, although the spectrum includes three16s before accounting for the antifamily. The vector10s and singlets are further states, not permission to discard the antifamily.

The two tempting E8 descriptions give the same answer. In E6 x SU3 language, (27,3) contains the desired three16_1. The E6 adjoint also contains16_-3, whose opposite localizer sign supplies one16bar_3. Keeping only(27,3) would omit a sector of the E8 gauge theory without giving it a mass or a different physical domain.

More generally, let nu be the rank-one relative index for the common T localizer on a chosen cut three-manifold. The triplet contributes3nu, while the singlet has opposite charge and complementary domain, contributing-nu. Hence

    I16=2nu, nu integer.

This **restricted commuting-background index cannot be three**. Changing a flat Wilson or lifting vectorlike pairs does not change it. It is not a no-go for all E8 models: noncommuting Higgs backgrounds, different UV source/domain data, flux/APS contributions, extra matter or higher-dimensional index problems can change the premise.

## Neutral directions and anomalies are also still present

Conjugation on traceless End(C3) decomposes the flavor adjoint into the eight nontrivial H27 linear characters. Directly evaluating the linked Fox complex for each gives total absolute Betti numbers(0,6,6,0). Thus the flat flavor connection has six complex infinitesimal SL3 deformations in the stated unconstrained boundary problem, even though no flavor gauge generator remains invariant. No claim is made that these integrate unobstructedly, or that a physical UV boundary condition permits them all.

If T-neutral fields extend through the point cap while both wire tori remain, and no additional boundary holonomy data are fixed, the full grade-zero bundle with the order-seven Wilson has Betti numbers **(14,34,20,0)**. Fourteen invariant gauge directions each see the trivial base line with Betti(1,2,1,0); the flavor adjoint supplies the remaining(0,6,6,0). Neutral higher cohomology is not erased by the charged-sector contraction. Different UV domains must be derived before treating this as a physical massless-scalar census.

For the counted positive-T chiral spectrum, using T(16)=2,T(10)=1, the exact traces are

    Tr T=168, Tr T^3=912, A_(Spin10^2 T)=18.

They require inflow or additional states. Also all counted chiral T charges are positive: at zero FI, their scalar VEVs alone cannot cancel D_T=sum q_i |phi_i|^2. No gauge-invariant holomorphic monomial containing these charged chiral fields exists without opposite-charge fields, transforming spurions or an axionic/nonperturbative completion. Enlarging the gauge algebra has not automatically repaired the vacuum or Yukawas.

## An explicit odd-index escape: replace the scalar commuting profile by a non-Abelian Dirac mass texture

To test an actual way outside the preceding hypothesis, define a different auxiliary continuum operator on R3. Put

    P(x,y,z)=(Re(x+iy)^3, Im(x+iy)^3, z(3r^2+z^2)),
    g=P/sqrt(1+|P|^2),
    Phi=diag(3 g.sigma-I2, I2),
    L=(sigma_i partial_i) tensor I4+I2 tensor Phi.

Here sigma denotes Pauli matrices, and L acts on eight complex components. Phi is a globally smooth, bounded, Hermitian, traceless SU4 mass endomorphism. This is a scalar mass matrix, **not** an identification with a PW Higgs one-form.

An exact polynomial check gives|P|^2=r^2(r^2+3z^2)^2. At infinity Phi has eigenvalues(2,-4,1,1). For r>=1, Phi^2>=I4; its first derivative has the explicit Dirac-commutator bound

    ||sum sigma_i tensor partial_i Phi|| <= (36+18sqrt3)/r.

Consequently both L*L and LL* are coercive outside r=200, with potential at least1-(36+18sqrt3)/200>1/2. Smoothness on compact sets and homogeneity at infinity give bounded second derivatives with O(r^-2) decay. These verify the assumptions of the [Callias theorem in Gesztesy-Waurick](https://arxiv.org/abs/1506.05144): this specified L is Fredholm.

Its asymptotic negative eigenline is a degree-three pullback of the Pauli eigenline. In u=cos(theta) coordinates, the target latitude is

    F(u)=(3u+u^3)/(1+3u^2),
    F'(u)=3(1-u^2)^2/(1+3u^2)^2,
    degree=(3/2)(F(1)-F(-1))=3.

The boundary eigenbundle therefore has Chern-number magnitude3 and **|ind L|=3**. Independent triangulated Berry calculations at two mesh sizes reproduce magnitude1 for the degree-one control and magnitude3 for this texture. This is a genuine specified auxiliary Dirac index, rather than an inference from a finite Hodge matrix or a cell count.

There is also an explicit repair of its A=0 infinite angular-gradient energy. Take the globally smooth SU4 connection

    A_i=diag((i/2)*(P cross partial_i P).sigma/(1+|P|^2),0_2).

Exact vector-algebra identities in the producer give

    D_i Phi=diag(3*(partial_i P).sigma/(1+|P|^2)^(3/2),0_2).

Near the origin A=O(r^5), F=O(r^4), D_A Phi=O(r^2); at infinity A=O(r^-1), F=O(r^-2), D_A Phi=O(r^-7). Consequently the explicit Yang-Mills/adjoint-Higgs kinetic energy integral[-sum_i<j Tr(F_ij^2)+sum_i Tr((D_i Phi)^2)] is finite, with no scalar potential added. This is a **finite-energy variational configuration**. An exact scalar Euler-Lagrange check gives D_iD_i Phi=-27/(4sqrt2) sigma_x in its first block at(1,0,0), so it is demonstrably not a stationary solution of that specified zero-potential energy. The covariant mass commutator is bounded by(36+18sqrt3)/r^7, giving exterior coercivity>1/2 already for r>=3. A_t=tA is a Fredholm homotopy, so the coupled operator retains index magnitude3.

Important limits remain. Index magnitude3 guarantees a net imbalance, not exactly three zero modes with no extra pairs. The degree is supplied, not dynamically selected. The mass vanishes on a compact level surface|P|=1/sqrt8, rather than at three prescribed points. Its angular variation does not commute with fixed H27 holonomies; one cannot superpose it on the flat linked background without solving new gauge-Higgs equations. The supplied connection and mass have not been shown to solve Yang-Mills-Higgs or BPS equations, and no physical G2 source action has been derived. Tensoring a spectator Spin10 spinor gives mathematical index magnitude48, but its interpretation as four-dimensional fermions requires the actual higher-dimensional operator and all E8 sectors.

The existing `analysis/2026-11-10_monopole_core_channels.md` explicitly lacks a gapped Callias problem. The mass above is a new auxiliary background, not a claimed solution of that monopole vacuum. The Callias theorem and degree/Chern relationship are standard mathematics; this packet supplies the concrete bounded SU4 operator and compares its premises with the failed commuting flavor completion.

## A cleaner E8 embedding: place the texture in SU3 flavor and localize whole27s

The same tested texture and connection fit inside the SU3 factor commuting with E6. Set

    Phi3=diag(3g.sigma-I2/2,1),
    A3=diag(A2,0).

This is traceless, with asymptotic eigenvalues(5/2,-7/2,1), exterior mass gap at least1, the same covariant derivative and finite-energy estimates, and index magnitude3 for the six-component flavor/spatial Dirac operator. The nonzero scalar EOM residual persists: changing the constant commuting shift does not make this a stationary configuration.

In E8's(27,3) sector, the mass now acts on the flavor factor uniformly and commutes with the full E6 action. Its auxiliary operator therefore has index magnitude81, a multiplicity index of three whole27s **within that block**. This gives a representation assignment worth testing beyond the common-T profile, which flipped the10_-2 and adjoint16_-3 sectors separately.

There is a crucial conjugate-sector gate. In the usual conjugate gauge representation Abar=A*, Phibar=-Phi*, let C=i sigma2 be the spatial Pauli matrix and let star denote complex conjugation, not the adjoint. Then Lbar=-C L* C^-1; C times complex conjugation is the antiunitary map. Thus the conjugate27bar block has the **same three-dimensional Callias index**, not an automatically opposite index. The identity C sigma_i* C^-1=-sigma_i is checked in the producer. It would be incorrect to declare that only three left-chiral27s remain merely from the single-block index. The actual seven-dimensional Clifford coupling, Majorana reality and four-dimensional chirality assignment must be derived; the neutral E8 sectors are also ungapped, so a full-adjoint Fredholm index is not supplied.

If a valid physical projection selects whole27s, their inventory is16_1+10_-2+1_4. The following are conditional representation-consistency checks, not a derived massless spectrum. Direct traces per27 give

    Tr Psi=16-20+4=0,
    Tr Psi^3=16-80+64=0,
    A_(Spin10^2 Psi)=2-2=0.

The known E6 matter cubic has charge-compatible channels16_1*16_1*10_-2 and1_4*10_-2*10_-2. These standard representation channels are not new Yukawa predictions; profile overlaps, coefficients and physical Higgs zero modes are uncomputed. The three complete27s have the familiar extra vectors and singlets. Their SM-singlet Nc:(chi,Psi)=(-5,1) and S:(0,4) still all have positive Psi, blocking a nonzero zero-FI SM-preserving condensate without further ingredients. Gauge-rank reduction, neutral sectors, anomaly inflow at actual defects, degree-three selection, H27 compatibility and a stationary G2 background remain open.

Thus the fixed commuting E8/H27 model fails the odd-family index, while a concrete non-Abelian SU3 family-sector Dirac model has a block index of three with consistent whole27 charge traces. Whether this can become three physical chiral families is explicitly unproved, especially because of the conjugate-sector gate. The operator classes and field backgrounds are different.

## Parallel correction and reproducibility

The newly appearing parallel `analysis/toe_20261118_AdS_dimension_BF_provenance_falsifier.py` correctly separates the scalar bounds AdS4:-9/4 and AdS5:-4. The original winding branch came from the AdS5/type-IIB problem of [Gubser and Mitra](https://arxiv.org/abs/hep-th/0108239). Earlier references to -4 as an AdS4 scalar bound are incorrect. This report uses no BF instability claim and preserves the parallel correction's authorship.

Run `python analysis/toe_20261118_E8_H27_wire_index_parity.py`. It writes `data/toe_20261118_E8_H27_wire_index_parity.json`. The producer checks all roots/reflections, full native spinor Y/chi and Wilson dictionaries, the actual SU4 commutant, compact group closure, linked neutral complexes, parity controls, anomaly arithmetic, polynomial texture identities, explicit coercivity and two-resolution Berry Chern controls. The report, producer and certificate are the only owned publication files. All parallel files are preserved.

The useful change in direction is concrete: the minimal flat commuting E8 completion fails the desired odd-family index, while an explicit non-Abelian gapped Dirac operator supports one. Connecting the latter to an admissible G2/gauge/source construction is still required.
