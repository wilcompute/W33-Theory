# Five physical consistency fronts and the two distinct native 27-radicals of W33

**18 November 2026 — verified mathematical workbench, not a theory of everything.**

This packet extends commit 4a5bc06a299417e68ed671e3016075f831b5780c in wilcompute/W33-Theory. It independently reads the exact native E6 quartic/charge-balanced toy Higgs report, the wire relative cohomology producer and the prior W33 group data before deriving new results. The prior results establish an E6-adjoint-localized representation family 16_-3, a nonzero native quartic two-adjoint Yukawa tensor, a conditional three-point solid-torus relative index, and an abstract W33 pointed-line S3 family triplet. These are *not* actual chiral zero modes of a known compact G2 background or observed particle masses.

This pass deliberately pursues five distinct falsifier fronts plus two independent structural extensions: **(I) a Hermitian finite Hodge-Dirac toy; (II) a factored E6 anomaly and single-axion test; (III) symmetry-invariant flag selection and full S3 flavor splitting; (IV) mass/kinetic/mixing robust BF inequality; (V) history-dependent herald calibration and an anytime qutrit Bell witness; (VI) exact native E6 full spinor gamma bilinear; (VII) point-versus-line PSp4(3) parabolic radicals and a qutrit Weyl representation.**

## Executive findings

1. **Two different 27-element groups live inside W33**. Direct computation in PSp4(3) proves the point-parabolic O3 is the noncommutative exponent-3 Heisenberg H27 (center3, derived subgroup3); the *line-parabolic* O3 is the commuting 3-dimensional ternary vector group C3^3 (center27, derived subgroup1). Both parabolics have order648, both contain Sylow3 groups of order81, and the O3 cores have order27. An ordered pointed-line triplet has stabilizer C3^3, **not H27**. These are distinct exact finite-geometric stabilizers, not arbitrary 27-count coincidences.
2. The point-parabolic H27 has an explicit irreducible qutrit clock/shift representation: 27 distinct operators omega^c X^a Z^b, commutator XZX^-1Z^-1=omega^2 I and 1D joint commutant of X,Z. This is *mathematical representation theory*, not an experiment or a uniquely selected photon encoding.
3. A native W33-invariant finite incidence energy has exactly160 incident point-line pure minima, and an additional exactly S3-invariant polynomial has the six minima given by permutations of (-A,0,+A). Combined there are 960 classical vacua, each a flag plus an ordering of three points. This is one **engineered** classical symmetry-breaking mechanism and does **not** derive a physical local action, Lorentzian gravity or realistic masses.
4. All136 unordered products of the exact E6 16_-3 have been checked. The symmetric second-action map Sym²16 -> 10_-2 has rank10, with SU5 branch pair ranks 10x10=5, 10x5bar=5, 5barx1=5, and the other three combinations zero. The tensor is an exact nonzero E6-equivariant quartic route, not a measured Yukawa.
5. The wire relative complex admits a Hermitian finite Hodge-Dirac with m zero modes and spectral gap exactly1 for all chosen nonzero monodromies when r>=1. For m=3, selecting r=3 relative sphere conditions yields (b1,b2)=(3,0), but selecting r=2 yields (2,1). **The physical spinor operator, APS/eta corrections and gauge covariant boundary conditions remain uncomputed**.
6. For three native E6 adjoint16_-3 families, Tr(a Chi+b Psi)^3=-432 b(5a²+3b²) and Tr(a Chi+b Psi)=-144b. The mixed SU3²-Psi, SU2²-Psi and SU5-normalized 3/5 Y²-Psi coefficients all equal -18. The anomaly polynomial formally factors through Psi; one shifting axion plus local counterterms might repair the 4D reducible anomalies, but **no axion, UV source, coefficient integrality or full inflow is derived**. SM singlet fermions alone cannot cancel the non-Abelian mixed anomalies.
7. The BF inequality survives more than a scalar mass shift: a positive-definite kinetic matrix K=I+E, a Hermitian mass perturbation Delta and arbitrarily strong symmetric off-diagonal mixing cannot eliminate a below-BF generalized mode whenever the original BF deficit B satisfies B>||Delta||+4||E|| (with norm of E below1 so kinetic metric stays positive). This is a precise conditional operator-norm falsifier, not a bound on physical string corrections.
8. A qutrit anytime-valid E-process can use predictable shot-specific herald calibration p0_i=kappa_i/(kappa_i+2) with alternative p1_i=7/(7+8kappa_i). Its Type-I false-positive probability is <=1% by nonnegative supermartingale/Ville reasoning, even with history-dependent calibrated kappa_i. For a periodic illustrative schedule 1.00,1.10,1.05,1.00, Monte Carlo over50,000 simulated accepted traces gives power by600 of 0.99462 (approximate 95% Monte Carlo interval 0.993979 to0.995261) and mean truncated accepted shots 159.586. No real device data exist.

## Front I — explicit finite Hodge-Dirac spectrum on the wire mapping cone

The supplied auxiliary geometry is M=(solid torus) minus m disjoint 3-balls and the relative boundary is the union of r of the m 2-sphere components, outer T2 absolute. For rank-one nonzero complex holonomy t, the exact relative mapping-cone cochain complex has grades C0=C, C1=C^(1+r), C2=C^m, C3=C^r and differentials

    d0=(t-1,1,...,1)^T, d1=0, d2=[I_r | 0].

They satisfy d1 d0=d2 d1=0. With the chosen standard Euclidean cochain inner products, the finite supersymmetric Hodge operator D=d+d* is Hermitian, with

    dim ker D|C1 = r, dim ker D|C2 = m-r,
    all other harmonic degrees zero,
    total dim ker D=m, formal index r-(m-r)=2r-m.

The nonzero eigenvalues of D are +/-sqrt(|t-1|²+r) (one pair) and +/-1 (r pairs). Thus its smallest positive excitation gap is exactly1 for r>=1, irrespective of t, in this arbitrary cell normalization. Tested for m=3,5 and r=1..m with t=1,-1,i,2,i/4. This is stronger than the previous bare relative Betti count *within this exact finite surrogate*. It is NOT a physical spinor-Dirac spectrum, has no APS eta term, does not calculate a spin structure, carries no 4D chirality, and does not imply perturbative robustness of zero-mode localization under changing the boundary *domain*.

For context: https://link.springer.com/article/10.1007/s00222-024-01310-z studies analytic G2 Dirac boundary/gluing carefully; and https://scoap3-prod-backend.s3.cern.ch/media/files/63082/10.1103/PhysRevD.103.126027.pdf develops localization in G2 orbifold scenarios. We used the mathematically stated distinctions, not numerical data from that PDF.

## Front II — anomaly factorization, and why Higgsing alone is not anomaly cancellation

Three net chiral E6 adjoint spinor16_-3 fermion families split under SU5 x Chi as 10_-1 + 5bar_+3 +1_-5. Direct trace over 48 complex components gives

    Tr(a Chi+b Psi)=-144 b,
    Tr(a Chi+b Psi)^3=-432 b(5a²+3b²),
    A_SU3²Psi=A_SU2²Psi=-18,
    A_Y²Psi=-30, so (3/5)A_Y²Psi=-18.

SM-singlet-only additional fermions have zero SU3/SU2 Dynkin index and hence CANNOT repair nonzero mixed non-Abelian anomalies. The complete factorization in terms of Psi suggests the necessary *form* of a generalized GS counterterm with an axion shifting under Psi plus possible Bardeen/generalized Chern-Simons counterterms assigning mixed Abelian anomalies consistently. The calculation does not determine a consistent compactification, integral axion periods, GS coupling normalization, anomaly-inflow boundary term or allowed particle spectrum.

If a putative axion has Stueckelberg scale k in the Psi direction and a scalar SM singlet with charge q=(-5,-3) has VEV v, their **formal** two-Abelian mass matrix is

    M²~[[25 v²,15 v²],[15 v²,9 v²+k²]];
    det M²=25 k² v²>0 for k,v nonzero.

This is the minimal algebraic rank-two alternative to relying on two independent Higgs charge vectors. But a single charged scalar violates zero-FI D-flatness in the simplest SUSY model, while the axion's D-term and UV completion are not supplied. The previous native 78+27bar+27 charge-balanced toy remains a separate algebraic D/F-flat candidate. **Breaking a gauge boson's mass does not remove the need to cancel its gauge anomaly.**

## Front III — the W33 flag and family-label selection potential

Let A be the native 40x40 incidence matrix, A_pL=1 exactly when p lies on L. Each of40 points lies on4 lines; each line has4 points; A contains exactly160 ones.

For probability simplex coordinates p in Delta_39 and l in Delta_39, define a fully W33 automorphism-invariant classical energy

    H(p,l)=-J p^T A l-kappa (sum p_i²+sum l_j²), J,kappa>0.

Since p^T A l<=1 and both squared norms<=1, H>=-J-2kappa. Equality requires both simplex vectors to be pure vertices and the chosen pair to be incident. Thus **all and only the160 flags are global minima**. This furnishes a precise toy symmetry-preserving microscopic expression with symmetry-broken classical minima, rather than manually singling out one flag. It is not a local lattice Hamiltonian or a derivation from gravity; at finite size there is no thermodynamic phase transition statement.

Each selected flag has an S3 action on the other three collinear points. A separate exactly S3-invariant real scalar potential

    V(s1,s2,s3)=(s1+s2+s3)²
               +(s1s2+s1s3+s2s3+A0²)²
               +(s1s2s3)²

has exactly the six zero-energy minima given by permutations of (-A0,0,+A0). Proof: its elementary symmetric functions force the polynomial with roots s_i to be t³-A0² t, whose roots are distinct. Its Hessian at (-1,0,1), A0=1 has exact eigenvalues 4-2sqrt2,4,4+2sqrt2, all positive. The minima fully break permutation S3 as a **classical** field order parameter. The toy combined vacuum labels number160x6=960. The exact ordered flag stabilizer in PSp4(3) has size25920/960=27. Their physical interpretation as three smooth G2 defects, actual Yukawa profile overlaps, masses, or spatial directions is not known; no measured fermion hierarchy follows from the equally spaced toy VEVs.

## Front IV — two *different* 27-subgroup constructions inside PSp4(3)

Rebuilt the 40 native F3^4 symplectic transvections, their action on W33's40 projective points, and on its40 isotropic lines. Both permutation groups have exact order25920.

For a representative point or line, the stabilizer is a maximal parabolic subgroup of order25920/40=648. Its Sylow3 group has order81. The core of that Sylow subgroup, obtained by checking all648 conjugations, is the largest normal 3-subgroup O3 of the parabolic. Both have order27, **but:**

| Property | Point (Klingen) parabolic O3 | Isotropic-line (Siegel) parabolic O3 |
|---|---:|---:|
| Order | 27 | 27 |
| center order | 3 | 27 |
| derived group order | 3 | 1 |
| identity/other element orders | 1x1,3x26 | 1x1,3x26 |
| isomorphism type | non-Abelian extraspecial Heisenberg H27, exponent3 | Abelian C3 x C3 x C3 |

These identifications are certified by enumerated group multiplication, commutators and centers. In particular, one must not mistake the **C3^3** pointwise stabilizer of a complete ordered line for the noncommuting H27. The line-parabolic radical is the familiar additive group of symmetric 2x2 ternary matrices, Sym²(F3²), whose dimension is three. The point-parabolic radical is the 3-dimensional Heisenberg group.

Going one step further, choose actual noncommuting point-radical elements x,y with z=[x,y] central of order3; every x^a y^b z^c, a,b,c in F3, is distinct. With omega=exp(2 pi i/3), define the shift X and clock Z on a 3-level Hilbert space. Their commutator is X Z X^-1 Z^-1=omega² I3. The Pauli-Heisenberg matrix group has27 distinct elements, and the joint commutant of X and Z is exactly one-dimensional: the representation is irreducible. This is an explicit faithful 3D Schroedinger model for the *native point radical*, not an arbitrary group-order match.

**Interpretation boundary:** This gives a mathematically nontrivial *address/operator dual parabolic pair* in W33, highly relevant to attempts to connect geometry and quantum information. It does **not** identify the cubic-surface Heisenberg action, E6 27-dimensional trinification, photons, 3+1D spacetime or a uniquely selected physical state. Such connections require an explicitly compatible intertwiner and experimental predictions.

Literature context for the standard distinction between the Sp4 Siegel symmetric-matrix radical and the other parabolic: https://link.springer.com/article/10.1007/s00209-016-1840-5 and https://arxiv.org/abs/2401.16933. Our q=3 subgroup identification is independently recomputed, not borrowed from those references.

## Front V — native full E6 spinor bilinear tensor, beyond the previous 10x10 check

Rebuilt the E6 algebra as78 exact 27x27 matrices from the repo's native clock-Albert triple product, projected the Psi=-3 spinor16 and its Chi charge sectors: ten 10_-1, five 5bar_3, one 1_-5. For each of the136 unordered pairs of16 matrices, computed their symmetric two-step action on the E6 27 singlet of Psi charge+4. All generators commute in the relevant grade -3 subspace, but their products do not vanish. The combined image is the full10-dimensional Psi=-2 vector of SO10, giving the native symmetric gamma-bilinear map

    Sym²(16_-3) -> 10_-2, exact image rank10.

The exact SU5-sector pair image ranks are:

    10 x 10 -> 5bar_-2, rank5
    10 x 5bar -> 5_+2, rank5
    5bar x 1 -> 5bar_-2, rank5
    10 x 1, 5bar x 5bar, 1 x 1 -> zero.

This verifies the earlier quartic Yukawa proposal has a richer invariant tensor structure. It also provides falsifiable operator selection rules: arbitrary pairings do not generate couplings merely because both come from16. The number of individually nonzero matrix entries depends on the selected native basis, whereas the image ranks are intrinsic to the equivariant tensor. No physical 4D Yukawa coefficient, mass fit, gauge symmetry violation or wavefunction overlap is inferred.

## Front VI — generalized BF instability with mass, kinetic and mixing uncertainty

In the *conditional* previously implemented 11D effective winding model, the lowest dimensionless scalar mass squared is

    m_light² L²=lambda-2-sqrt(4+16lambda),

the AdS4 BF threshold is -4, and the BF deficit at lambda is

    B=sqrt(4+16lambda)-lambda-2, maximum9/4 at lambda=15/4.

Let an unknown mass correction be any Hermitian matrix Delta of operator norm<=delta; let the kinetic matrix K=I+E>0 with ||E||<=eps<1, and allow arbitrary Hermitian couplings to other modes. The generalized BF test is M+4K. Evaluating its Rayleigh quadratic form on the trial vector of the original unstable mode gives

    e1*(M+4K)e1 <= -B + delta + 4 eps.

If B>delta+4 eps, some generalized eigenvalue is below -4, **regardless of coupling strength to higher modes**. This is a strict matrix inequality, not a numerical accident. Two hundred seeded random 3x3 mixing matrices and independently norm-bounded mass/kinetic corrections verify the predicted instability at lambda=15/4, delta=.5, eps=.125.

For the standard modular domain tau=x+i y and r=N0/N, lambda=3 pi r/y, the robustly unstable hyperbolic area fraction is the exact earlier cumulative-area expression with effective correction budget delta+4eps. At r=2,delta=.5,eps=.125, 45.312210837% remains robustly unstable *in this branch*. This **does not** provide a physical bound on delta or eps, does not encompass all fields, changes of the AdS radius, non-Hermitian/dissipative modes or string corrections beyond the model.

Relevant caution from recent physics: https://arxiv.org/abs/2610.27058 discusses both instability of simple toroidal 11D flux vacua and a distinct tachyon-free AdS4 compactification, so one must not turn a one-branch BF calculation into a universal M-theory instability claim.

## Front VII — predictable herald calibration for the sequential qutrit witness

The earlier Bell-projection witness compared the entanglement-breaking effective input-output null p0<=1/3 to the simulated qutrit alternative p1=7/15. With accepted-event success/failure efficiency odds uncertainty kappa_i (known before trial i, possibly adapted to earlier trials), the conservative accepted success bounds are

    p0_i=kappa_i/(kappa_i+2), p1_i=7/(7+8kappa_i).

For p1_i>p0_i, choose the trial-specific likelihood multiplier p1_i/p0_i on success, (1-p1_i)/(1-p0_i) on failure. Conditional expected multiplier under null<=1, so E_n is a nonnegative test supermartingale and Ville's inequality bounds the chance of ever crossing100 by1%. This null error guarantee is analytic, applies at arbitrarily chosen stopping times, and does NOT rely on trial independence. The bound on p0_i must actually be certified **conditionally on the previous history** in a physical experiment.

A seeded 50,000-history Monte Carlo *for power only* under a specified independent accepted alternative and illustrative cycle kappa=(1,1.10,1.05,1) gives

    n=200: detection0.74614
    n=292: detection0.89916
    n=600: detection0.99462
    nominal 95% simulation-error interval by600: 0.9939788..0.9952612
    mean accepted trials to threshold or cutoff600: 159.58622.

These simulations do not verify the null with physical detectors, nor replace full multitime process-tensor witnesses. Important 2025–2026 literature: https://journals.aps.org/prresearch/abstract/10.1103/r8lf-bb4p (entanglement-breaking one-time channels can still be a quantum multitime resource); https://journals.aps.org/pra/abstract/10.1103/ssf1-j2j8 (2026, higher-order protocol-dependent memory); https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs (2026 guide to higher-order operations). No optical hardware was controlled.

## Reproduction and audit

All scripts are additive; original works on the shared Windows tree remain unmodified. New files:

- analysis/toe_20261118_post_quartic_fivefront_hodge_GS_selector_BF_optics.py
- analysis/toe_20261118_W33_ordered_flag_H27_kernel.py
- analysis/toe_20261118_W33_dual_parabolic_radicals_27.py
- analysis/toe_20261118_E6_full_spinor_symmetric_gamma10.py
- data/toe_20261118_post_quartic_fivefront_hodge_GS_selector_BF_optics.json
- data/toe_20261118_W33_ordered_flag_H27_kernel.json
- data/toe_20261118_W33_dual_parabolic_radicals_27.json
- data/toe_20261118_E6_full_spinor_symmetric_gamma10.json
- tests/test_toe_20261118_postquartic_W33_parabolics_gamma_Hodge_BF_optics.py
- this report.

Each producer can be run directly with Python from repo root; new suite via Python unittest discover. Compare the earlier named tests in the repo. Never stage other assistants' dirty files, and never use a force push.

## Five independent next research targets

1. **Actual physical chirality and boundaries:** construct the fully coupled 7D gauge/Higgs spinor Dirac operator on a genuine singular G2 space, specify selfadjoint gauge-covariant boundary projectors, compute APS/eta/inflow and test that all three relative sectors survive.
2. **UV anomaly and vacuum completion:** derive a quantized, compactification-supported GS axion and its couplings, plus the full allowed E6 superpotential/Higgs fields and Yukawa overlaps; verify D- and F-flatness, rank reduction and anomaly cancellation jointly.
3. **Explicit PSp-to-E6/photonic intertwiner and dynamic family action:** compare the native point-parabolic H27 qutrit representation and line-parabolic C3^3 address radical to previously established cubic-surface and trinification actions with exact matrices; construct a physical, not engineered, selector of a flag and viable mass hierarchies.
4. **Full corrected AdS stability spectrum:** compute actual mass/kinetic perturbation operator norms, flux quantization and backreaction, and test the entire KK/string mass-matrix spectrum against BF, rather than assume delta or eps.
5. **Real qutrit/process-tensor experiment:** build an event-ready qutrit circuit, independently certify herald odds and reference-state integrity, run an anytime e-process and add a multitime temporal instrument witness to avoid conflating one-time entanglement preservation with quantum memory.

**Falsifiable takeaway:** The finite mathematics has a new exact address/operator dual-parabolic structure and a full native 16x16 Yukawa bilinear; the physics is still contingent upon global G2 boundary conditions, UV inflow and genuine dynamical selection. None of the achieved algebraic equalities alone proves a theory of everything.
