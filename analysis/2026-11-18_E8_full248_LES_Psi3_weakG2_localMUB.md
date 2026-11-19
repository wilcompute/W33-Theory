# Complete E8 linked-wire cohomology, minimal Psi Wilson, weak-G2 curvature and local qutrit witness

**2026-11-18. Five-plus independent research gates.** Verified topology and group arithmetic, conditional physical interpretations. No experimentally observed quantum memory, no chiral Dirac index, no sourced 11D compactification, no phenomenological particle spectrum and no Theory of Everything established.

## Repository baseline and external prior art

Reviewed newest GitHub master/local 39b57e3c360fa4bfb09f0003fa2cbf58acc49df4 (matching heads, empty staging, 19 preexisting unrelated tracked modifications). Read the previous C9/T(2,6)/E8 report in entirety relevant sections and its 273-line producer, and rechecked the prior order-seven SU5+Psi Wilson report. The previous C9 packet already proves the genuine SU3 Clifford lift, finite order81 family holonomy, order567 product with W7, and the separate matter (81,0), conjugate matter (81,0) and family-adjoint (12,4) relative cohomology. The earlier f495122c packet already discovered an SO10 order-seven Wilson line and supplementary Psi phase that can leave E6 centralizer dimension14. This pass adds the missing FULL E8 adjoint local-system calculation, corrects a relative-cohomology formula in invariant sectors, determines the uniquely minimizing Psi phase for the **doubled** W7 generator, and supplies a **local four-MUB** qutrit readout instead of assuming a global Bell projection.

Relevant outside sources:
- Standard SU3xE6 E8 adjoint decomposition and generation-index caution: https://assets.press.princeton.edu/chapters/s09_8456.pdf (representation branching is standard).
- E8 global subgroup (E6xSU3)/Z3: https://en.wikipedia.org/wiki/E8_(mathematics).
- Geometric nearly parallel G2 Einstein formula and Killing spinors: https://doi.org/10.1007/s10455-022-09853-1.
- Optimal verification via projective two-designs and MUB: https://doi.org/10.1103/PhysRevA.99.052346.
- Entanglement dimensionality witnessed by local basis correlations: https://doi.org/10.1038/s41534-025-00990-6.

## I. Correct relative S2 LES for a local system with parallel invariant vectors

Let X be the T(2,6) link exterior with pi1=<a,c|[a,c^3]=1>, d=dim_C V and flat representation (A,C). The original one-relator cellular cochains are

    C0(X;V)=V; C1(X;V)=V⊕V; C2(X;V)=V,
    d0=(A-I, C-I)^T,
    d1=(I-C^3, (A-I)(I+C+C^2)).

Write r0=rank d0, r1=rank d1. Then

    (b0,b1,b2)_X=(d-r0,2d-r0-r1,d-r1).

Now remove one open ball from X and impose relative boundary conditions on its S2, leaving the link tori absolute. By excision/long exact sequence, the punctured space has an additional sphere class, and the relative boundary kills C0 rather than automatically adding all d copies to H1. The correct relative complex, up to a cellular equivalence, is

    C0(M,S2;V)=0, C1(M,S2;V)=V⊕V, C2(M,S2;V)=V,

with differential d1 as above. Hence

    (b0,b1,b2)_relative=(0,2d-r1,d-r1),
    b1(relative)=b1(X)+d-b0(X),
    b1(relative)-b2(relative)=d.

The previous generic code in 39b57e3 uses b1(relative)=3d-r0-r1. That is correct when b0(X)=0, as for ALL the reported charged 27 and conjugate 27 representations and the SU3 family adjoint8. It OVERCOUNTS by b0(X) when there are parallel invariant vectors. A trivial rank-one coefficient explicitly has (b0,b1,b2)_X=(1,2,1) and **(0,2,1)** relatively, NOT (0,3,1).

The consequence is methodological: for the acyclic rank-three family local system, (b1,b2)=(3,0) arises because one chooses a rank-three coefficient system and one relative sphere. The net index equals that supplied rank d, for ANY such coefficients. It is not a derivation of precisely three physical generations or a nonzero charged 7D Dirac index.

## II. Full E8 248: the uncounted E6 adjoint reveals extra neutral modes and extra gauge generators

Under E6 x SU3,

    248=(78,1)+(1,8)+(27,3)+(27bar,3bar).

The previous linked holonomy is a=(I_E6,X_family), c=(W7_E6,C9_family), with X qutrit shift, C9^3=omega I3 and W7=diag(zeta7^2,zeta7^2,zeta7^2,zeta7^4,zeta7^4) inside SU5⊂E6.

The SU5 branching of E6 adjoint78 under SO10xPsi is

    78=45_0 + 16_(-3) + 16bar_(+3) + 1_0.
    45|SU5=24+10+10bar+1.
    16|SU5=10+5bar+1.
    16bar|SU5=10bar+5+1.

An explicit SU5 color/weak weight enumeration counts the 78 fixed directions with **the W7 alone** as 16, NOT14: 12 from SU5 adjoint24, 1 from SO10 45 SU5 singlet, 1 from each charged spinor singlet and 1 from E6 extra singlet. The extra pair of charged-spinor SU5-singlet roots forms an extra non-Abelian SU2 factor with their associated Cartan. The unbroken E6 algebra thus has dimension16, schematically

    su3_color ⊕ su2_weak ⊕ su2_extra ⊕ u1^2.

Each of these 16 fixed 1D adjoint weights contributes absolute (1,2,1) and relative (0,2,1). Each of the remaining62 nontrivial order-seven weights contributes absolute (0,0,0), relative (0,1,0). Therefore E6-adjoint78 relative (b1,b2)=(94,16).

Including prior family8 (12,4), matter81 (81,0), conjugate81 (81,0), the FULL E8 adjoint relative census is

    E6 adjoint78        (94,16)
    SU3 adjoint8        (12, 4)
    27x3               (81, 0)
    27barx3bar         (81, 0)
    --------------------------
    TOTAL              (268,20); net index248.

There is no new numerical coincidence: the net Euler index equals the input rank248. The complete X absolute cohomology is (b0,b1,b2)=(16,36,20); rel b1=36+248-16=268, providing an independent LES check.

## III. Unique order-seven Psi phase c=3 fixes the extra non-Abelian SU2, but rank-six extra U1s persist

The preceding f495122c report already found a supplementary Psi phase of 5 with W7 generator (a,b)=(1,2). Our C9 packet chose the DOUBLED SU5 generator (a,b)=(2,4). The corresponding phase must also be doubled: 2*5=10=3 mod7. It cannot be copied unmodified.

For each Psi phase c=0,...,6, assign E6 adjoint weights:
- 45_0: SU5 adj24, 10,10bar, singlet; no Psi shift.
- 16_-3: SU5 10,5bar, singlet with shift -3c.
- 16bar_+3: 10bar,5,singlet with shift +3c.
- extra singlet1_0.

The exact E6 invariant generator counts are

    Psi phase c:           0  1  2  3  4  5  6
    E6 invariant dim:     16 18 26 14 20 16 20

Thus **c=3 is uniquely minimal** in this cyclic order-seven family. It removes both surviving spinor-root singlets, leaving E6 algebra su3_color+su2_weak+u1^3 (dimension14), which is SM dimension12 plus two extra Abelian generators. The full E8 holonomy centralizer has the same dimension because the SU3 family8 has no invariant under X,C9 and neither 27x3 sector has an invariant.

For c=3, E6-adjoint relative (b1,b2)=(92,14), all other sector counts unchanged; FULL E8 relative becomes

    (b1,b2)=(266,18), difference248.

The X absolute Betti values become (14,32,18); LES gives b1relative=32+248-14=266. No additional rank-two gauge breaking, anomaly inflow, mass generation, or physical chiral projection follows from this finite Wilson line alone. Note this 14-dimensional centralizer is not a new discovery independent of the f495122c report; its phase conversion, exhaustive verification and full E8-topology consequences are the new results.

## IV. Conjugation theorem: uniform relative boundary conditions cannot project out 27bar

For an arbitrary finite CW pair (M,S), a complex representation V of pi1(M), and its complex conjugate Vbar, the cochain matrices obey d_k(Vbar)=overline(d_k(V)) when the underlying cellular Fox matrices have integer coefficients. If the two sectors use the SAME real relative/absolute boundary prescription, conjugation is a cochain anti-isomorphism:

    H^k(M,S;Vbar) = overline(H^k(M,S;V)).

Their complex dimensions are equal at every degree. This is exact and holds beyond the particular finite H27xC9 link.

Therefore changing only flat holonomy (but keeping complex-conjugate E8 matter sections and identical real cohomological boundary domains) cannot produce (81,0) in (27,3) and zero in (27bar,3bar). More substantial physics must distinguish the sectors: a full odd-dimensional gauge/Higgs Dirac operator with chirality-sensitive normalizable domains, a spinorial defect, orbifold action, spectral-flow boundary data, or other dynamics. This is scoped to the stated topological complex and does not prohibit chiral compactifications.

## V. Weak/nearly-parallel G2 torsion matches Freund-Rubin curvature; no untwisted zero mode

Earlier round S7 work showed a pure-electric unwarped 11D Freund-Rubin product has internal

    Ric_Y7 = (f^2/6)g, F4=f vol_AdS4, f=3/L.

A torsion-free G2 metric is Ricci flat and therefore incompatible with nonzero f in this restricted product. But a nearly parallel G2 structure satisfies

    d(phi)=tau0 star(phi), d(star(phi))=0,
    Ric_Y7=(3/8) tau0^2 g.

Thus the NECESSARY curvature matching in the pure-electric product is

    abs(tau0)=2 abs(f)/3.

At f=3/L, abs(tau0)=2/L. The real Killing spinor has |Dspin|=7 abs(tau0)/8=7/(4L), while the scalar curvature is Scal*L²=21/2 and the Lichnerowicz lower bound is Dspin²L²>=21/8. The spinor is nonzero, but it is NOT a zero-mode of the untwisted geometric Dirac operator. Charged ADE/flux-coupled operators and singularities remain essential for localized chiral matter. This matches standard nearly-parallel G2 geometry; no complete supersymmetric compactification has been constructed.

## VI. Four locally measurable qutrit mutually unbiased bases replace ideal joint Bell detection

The earlier 39b57e3 packet proposed an intrinsic-qutrit channel witness using an IDEAL global qutrit Bell projection. Such a measurement is nontrivial in passive photonics. We replace it with **four local projective measurement settings**.

For qutrit Weyl X,Z, choose MUBs given by eigenbases of Z, X, XZ, XZ². Remarkably, the same C9 link holonomy acts by Clifford conjugation as X -> XZ² -> XZ -> X, while fixing Z. Thus the three noncomputational measurement settings lie in ONE C9-gate orbit. This directly connects the group-theoretic linked-wire construction with a possible qutrit measurement-control circuit (without asserting that a gauge holonomy is literally a laboratory gate). The 12 rank-one local states form a complete projective 2-design. With |Phi3>=(|00>+|11>+|22>)/sqrt3, their exact matrix identity is

    sum_(basis b=1..4; j=0..2) |b,j><b,j| tensor
                              |conj(b,j)><conj(b,j)|
       = I9 + 3 |Phi3><Phi3|.

Numerically reconstructed from qutrit eigenvectors, the operator residual is below2e-12. For ANY bipartite qutrit state rho, randomize the basis independently per trial, measure the reference in b and the memory output in the conjugate basis, then record a binary MATCH if the outcomes are equal:

    P(match) = (1+3*F)/4, F=<Phi3|rho|Phi3>.

Schmidt number <=2 entails F<=2/3, so the null is P(match)<=3/4. The isotropic qutrit channel model rho=t|Phi3><Phi3|+(1-t)I9/9 with t=.75 has F=7/9 and P(match)=5/6.

Using fixed-n independent random basis choices, IID shots, alpha=.01 and 90% power, exact binomial tail inversion (no Gaussian approximation) gives

    minimum accepted trials n=317,
    reject SN<=2 if at least k=256 matches,
    exact type-I probability=0.0092479486264,
    power=0.902452746359.

Unlike the original ideal Bell-projection design n=214, this n=317 protocol uses only local qutrit measurements in four controlled settings. It remains a mathematical design, NOT a measured apparatus.

Detector/readout model: each ternary label independently misclassifies with probability epsilon, split equally among the other two outcomes. For a true matching probability p, observed probability is

    a=(1-eps)^2+eps^2/2,
    b=eps*(1-eps)+eps^2/4,
    p_obs=b+(a-b)p.

With conservative **uncalibrated** SN2 null P(match)<=.75, required accepted n at90% power are: eps0 ->317, eps.01 ->472, eps.02 ->790. If the confusion model and epsilon are KNOWN EXACTLY and the null bound is transformed with it, n respectively317,348,389; in practice uncertainty of the calibration must be propagated before asserting 99% confidence. All trials are ACCEPTED/qualified, not necessarily source launches, and fair heralding/instrument memory must be established.

This certifies at most that an effective reference-to-carrier memory channel retains genuinely three-dimensional Schmidt-number-three entanglement; it does **NOT** certify an irreducible three-time process tensor with all two-time reductions classical. That stronger problem remains open.

## Seven cross-checks connecting the above

(1) The topology fixes net Euler index to coefficient rank, not observed generations. (2) H27/Clifford family operators survive E8 subgroup restrictions, but the full E8 adjoint contains neutral cohomology. (3) The corrected Wilson Psi phase3 removes the extra non-Abelian E6 SU2, but not the two unwanted U1s. (4) Charge-conjugate matter survives any conjugate-symmetric flat cochain domain. (5) A near-parallel rather than torsion-free G2 Einstein metric is necessary for the restricted FR product. (6) A real Killing spinor in such geometry is not an untwisted Dirac zero mode. (7) The SAME qutrit Weyl/Clifford basis supports a local experimental Schmidt-number witness, but does not by itself identify photons with E8 gauge matter.

## Reproducibility

One additive producer, exact certificate, independent unit tests, and this report:
- analysis/toe_20261118_E8_248_relative_Psi_G2_MUB.py
- data/toe_20261118_E8_248_relative_Psi_G2_MUB.json
- tests/test_toe_20261118_E8_full248_Psi_relative_G2_localMUB.py
- analysis/2026-11-18_E8_full248_LES_Psi3_weakG2_localMUB.md

Run:
    python analysis/toe_20261118_E8_248_relative_Psi_G2_MUB.py
    python -m unittest discover -s tests -p test_toe_20261118_E8_full248_Psi_relative_G2_localMUB.py -v

The report and exact JSON separate source-derived E8 branching, established 2-design/nearly-G2 mathematics, our computed relative local-system ranks, and physical hypotheses. Preexisting dirty shared files remain untouched.

## Five independent strongest next physical investigations

1. **Complete a genuine chiral E8/ADE spinor operator.** On a specified sourced 7D geometry, compute its domain, spectral flow, charge-conjugation action and net localized (27,3) vs conjugate modes. No flat-cohomology count substitutes for this.

2. **Build a globally defined E8 Higgs sector respecting (E6xSU3)/Z3.** Solve the coupled linked-wire and Pantev-Wijnholt gauge/Higgs fields, break the two remaining Abelian generators, control scalar moduli and cancel gauge anomalies.

3. **Construct a weak-G2/FR 11D background, not merely match Ricci tensors.** Include flux quantization, Killing-spinor equations, Chern-Simons constraints, realistic ADE singularities and full mixed KK spectrum with a physical massless chiral sector.

4. **Find a dynamical three-generation selection theorem.** Identify a *derived* action or topological constraint choosing rank3, the T(2,6) linking, and the quartic Morse localizer instead of entering all three as correlated design inputs.

5. **Establish genuinely three-time, intrinsically qutrit memory.** Combine the practical four-MUB dimension witness with a physical process-tensor test whose two-time reductions admit classical implementations but three-time correlations do not; pre-register instrument/calibration/error tests and exact finite-shot power.

**Status:** Mathematics verified for specified models. No completed TOE, no new fundamental constant derived, no physical chirality/global vacuum claimed.
