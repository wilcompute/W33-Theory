# Five TOE physics-interface probes: H27 seven-manifold, exact Dirac gap, sextic F-flat SIC, E8 torus center, and sequential qutrit memory

**November 18, 2026. Mathematically reproducible effective models, NOT a completed TOE.** No genuine singular G2 background, charged ADE boundary Dirac, E8 ultraviolet flavon or anomaly inflow, physical 11D flux metric, observed photons, or complete three-slot process tensor is claimed.

## Input provenance and novelty check

At intake W33-Theory master on GitHub and TheHeavyCrown were both 52ac4053fb2ce9de8ba49c55bb86269cb7a0237b. The local checkout carried 19 preexisting modified tracked files belonging to other work and many untracked parallel artifacts; this packet owns four uniquely named new files and preserves every unrelated file.

We reopened analysis/2026-11-18_H27_free_Einstein_Hesse_E6_Higgs_PW_GHZ_audit.md and **the original** analysis/PASS20261011_H27_HESSE_CUBIC_F_FLAT_LOCK.md. That older report already proves dim Sym3(3*)^H27=2, the Hesse cubic, and its F-flat stabilizer-ray restriction. We also reopened analysis/2026-11-18_PW_tilt_perfect_Morse.md, which already proves three scalar PW modes, and searched for higher-degree H27 flat vacua. Our genuine increment is a degree-SIX effective F-flat escape with a projective nine-state SIC, not rediscovery of the cubic invariant. Prior static GHZ measurements and fixed-shot statistics are also credited; our increment is a genuinely sequential four-gate state-emission circuit.

Outside mathematics/science consulted:
- https://escholarship.org/uc/item/2x57n1bg — compact torsion-free G2 vs torsionful
- https://arxiv.org/abs/1808.07144 — closed G2 need not be torsion-free
- https://onlinelibrary.wiley.com/doi/10.1002/cpa.70059 — Heisenberg group action and positive Ricci examples in a different construction
- https://www.sciencedirect.com/science/article/pii/S1063520326000540 — finite Heisenberg invariant polynomials
- https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs — genuine quantum-memory processes, causal breaks and interventions.

## Front 1. Exactly 7D with H27 gauge holonomy, but rigorous failure of compact torsion-free G2

Write the Heisenberg group H27={(a,b,c):a,b,c in F3} with multiplication (a,b,c)(A,B,C)=(a+A,b+B,c+C+aB). Its faithful SU3 Schrödinger representation is rho(a,b,c)=omega^c X^b Z^a with ZX=omega XZ. On S5(R) x T2(L1,L2) define

    (a,b,c).(v,theta1,theta2)
       =(rho(a,b,c)v,theta1+2pi*a/3,theta2+2pi*b/3).

This is a FREE isometric 27-element action: if a !=0 the first torus translation has no fixed point (18 elements); else if b!=0 the second has no fixed point (6 elements); else for nonidentity c=1 or2 the scalar matrix omega^c I3 fixes no unit vector on S5 (2 elements). The complete 27² H27 matrix multiplication residual is <1e-12. All actions preserve orientation; the finite odd-order action admits a compatible spin lift.

Thus the quotient Y7=(S5 x T2)/H27 is a smooth oriented spin 7D manifold, carrying a natural epimorphism pi1(Y7)->H27 and therefore actual H27 flat gauge holonomies. Its full pi1 is NOT H27 but fits 1->Z²->pi1(Y7)->H27->1 and is infinite.

Every factor action is homotopic to identity on real cohomology. Transfer through a finite covering gives

    P_Y(t)=(1+t^5)(1+t)^2,
    (b0,b1,b2,b3,b4,b5,b6,b7)=(1,2,1,0,0,1,2,1).

Two independent G2 no-go arguments:
1. Compact torsion-free G2 has a parallel defining 3-form phi. If its cohomology class were zero, phi=deta with d*phi=0 would yield integral(phi wedge *phi)=0 by Stokes, contradicting positive norm. Hence b3>=1. This Y7 has b3=0, ruling out any torsion-free G2 metric.
2. Torsion-free G2 implies Ricci-flat. All harmonic 1-forms are parallel. Two independent parallel 1-forms create a third via the parallel G2 cross product, so b1=2 is impossible. Here b1=2.
Nearly-parallel G2 with nonzero torsion has positive Einstein Ricci and hence b1=0 by Bochner; that is also excluded. The natural product-quotient metric has Ricci 4/R² on five S5 directions and0 on two torus directions, scalar20/R². This does NOT exclude all torsionful/singular G2 structures or a different physical internal seven-space. b4=0 excludes free real 4-form cohomology classes on this candidate, NOT exact flux or torsion/shifted quantization.

## Front 2. Exact stronger positive Dirac spectral gap with any FLAT H27 Wilson

The ordinary S5(R) spin Dirac spectrum is +/- (k+5/2)/R for nonnegative integer k. On S5 x T2 the product spin Dirac square is the sum of the two nonnegative factor squares. Therefore

    D_A² >=25/(4R²),   |lambda(D_A)| R>=5/2.

A unitary flat-twisted quotient eigenspinor pulls back to an equivariant spinor on the finite cover, and a flat twist trivializes upstairs. Thus the quotient twisted spectrum cannot enter the forbidden gap. At R=2 explicit 49 torus momentum controls give lambda_min²=25/16=1.5625; Lichnerowicz alone gives only Scalar/4=5/R²=1.25. In particular no ordinary massless spinor arises from *flat* H27/E8 Wilson geometry on this Y7. This theorem does NOT extend automatically to nonflat gauge fields, flux-coupled 11D supercovariant operators, singular ADE Dirac, boundary eta corrections, and localized physical chirality.

## Front 3. First allowed higher H27 flavon operator is sextic, and its F-flat vacua form a SIC

Finite H27 center acts by omega on a triplet, so a homogeneous invariant polynomial must have degree divisible by3. The exact Molien dimensions in degree d=3k are

    dim Sym^d(3*)^H27=(binom(d+2,2)+8)/9.

The group-invariant exponent-orbit enumeration agrees for all degrees0..12:

    d=0:1; d=3:2; d=6:4; d=9:7; d=12:11;
    all other degrees from1..12:0.

The four sextic invariants may be chosen as sum x_i^6, sum_(i<j)x_i³x_j³, (xyz)sum x_i³, and (xyz)². Quartic and quintic corrections are forbidden by the H27 center. An explicit dimensionless H27-invariant effective flavon superpotential is

    W=x³+y³+z³ - (x^6+y^6+z^6)/2,
    F_i=partial_i W=3 x_i²(1-x_i³).

Each coordinate can be0 or a cube root of1, giving 4³=64 isolated algebraic stationary vectors. Their nonzero-support census is 1,9,27,27 for supports0,1,2,3. The 27 support-two solutions include (1,1,0). Its normalized ray (1,1,0)/sqrt2 has maximum stabilizer overlap squared 2/3 across all12 qutrit stabilizer states; it is NOT a stabilizer. The earlier October11 cubic-only F-flat stabilizer theorem remains correct, but it cannot be extrapolated to H27-invariant operators of degree6.

**Additional new cross-front connection:** The 27 support-two stationary vectors project onto NINE distinct rays (three positions for the zero coordinate, three cube-root relative phases). These nine rays form a *Weyl-Heisenberg SIC*, obeying

    |<psi_i|psi_j>|²=1/4 for any i!=j,
    (1/3)sum_j |psi_j><psi_j|=I3.

The entire9x9 Gram residual is 6.7e-16; normalized POVM completeness residual is 3.4e-16; the H27 projective orbit is transitive. This SIC is NOT the repo's particular Hesse-pencil base-point SIC: the Hesse doublet norm² is exactly1/6 on these rays, versus0 for the Hesse base points. It belongs to the broader qutrit Weyl-Heisenberg SIC family. That distinction is explicitly verified.

**Physical caveat:** This is an effective single-triplet flavon model with a dimensionful sextic coupling reinstated in physical units. The E8 248 branching has no elementary (1,3), only (78,1)+(1,8)+(27,3)+(27bar,3bar). No UV operator generation, E6 D-flatness, anomaly consistency, potential selection among64 stationary solutions, actual Higgs masses, or observed Yukawa matrix has been derived. The SIC is a calculable toy-vacuum geometry, not yet a particle-physics prediction.

## Front 4. Flat torus clock/shift requires commuting holonomies or compensating projective charge

The qutrit family generators obey ZX=omega XZ; hence X and Z are NONCOMMUTING and cannot simultaneously be holonomies around the fundamental cycles of a bare ordinary flat torus T2, because pi1(T2)=Z² is abelian.

An exact two-qutrit compensator is

    U=Z tensor Z,  V=X tensor X_inverse.

These 9x9 unitary operators commute, have order3, and the eight nonidentity Z3² words have trace0 (identity trace9). They realize the regular representation of commuting Z3². Opposite projective central charges cancel.

This is an A2 x A2 finite-matrix control, NOT an explicit E6 27-dimensional counter-projective embedding or complete (E6 x SU3)/Z3 E8 principal bundle. On the full Y7 above, pi1 is NONABELIAN and surjects onto H27, so genuine noncommuting H27 gauge holonomy is permitted. Do not confuse torus-only Wilson loops with global defect/quotient holonomy.

## Front 5. An actual sequential, four-SUM, three-time qutrit GHZ emitter

Prior repo work supplied an exact STATIC GHZ versus dephased-state witness and a modeled 600-shot threshold. Here an 81-dimensional four-register unitary circuit gives that resource through TIME-ORDERED emission.

Initialize persistent E=(|0>+|1>+|2>)/sqrt3, and fresh A,B,C all in|0>. Apply:

    Session t1: SUM(E->A), emit A, never interact with A again.
    Session t2: SUM(E->B), emit B, never interact with B again.
    Session t3: SUM(E->C); inverse_SUM(C->E), emit C.

Four two-qutrit Clifford SUM gates exactly disentangle E into|0>, leaving (|000>+|111>+|222>)/sqrt3 in the three outputs. All four81x81 matrix unitarity tests pass. Complete dephasing of E between t2 and t3 yields instead sigma=(1/3)sum_j |jjj><jjj|, a classical separable-pair mixture. The coherent and dephased outputs have identical pairwise reduced density matrices, but the triple XXX expectation is1 versus0.

The prior GHZ three-setting witness can now be assigned to an explicit sequential source. Under the same modeled t=.75 coherence and eps=.01 symmetric ternary detector-label error, the 600 accepted trials (200 per setting), reject for >=539 matches, have conservative type-I <=.01 against biseparable output states and exact IID-model power .9930633699216721. This statistical model was calculated previously; new here is the four-gate causal emitter that produces the target.

**Essential limitation:** This is a sequential emitter with FIXED prepared inputs. The pairwise OUTPUT MARGINALS are classically correlated, but arbitrary intervening instruments and pairwise reduced PROCESS TENSORS have not been calculated. Therefore this does NOT yet establish the stronger genuine-three-time-only quantum-memory claim. It is neither a real optical circuit nor an experimentally demonstrated effect.

## Five independent follow-on gates

1. Construct a physically valid seven-dimensional singular/flux-supported ADE background with G2 spin structure, actual charged Dirac domain, index and local anomaly inflow. The S5xT2/H27 candidate fails torsion-free/weak G2 and ordinary massless spinors.
2. Build an E8-legal UV flavon/messenger completion of the H27 sextic potential, with realistic F/D-flat vacuum selection and a predicted Yukawa texture. Explain whether and why the nine-SIC orbit is energetically selected.
3. Construct actual E6 27-dimensional opposite-central-charge Wilson matrices and an honest global (E6 x SU3)/Z3 E8 bundle; cancel the two extra U1s and all anomalies.
4. Derive the true tilted PW continuum Dirac overlap/H27 intertwiner, correct 3-family count, and physical mirror mass gaps without inventing Gaussian hopping.
5. Turn the four-gate sequential emitter into a causality-constrained three-slot process tensor with arbitrary interventions, a true pairwise-classical PROCESS exclusion theorem and photon loss/visibility calibration.

## Reproduction

Four uniquely owned new files are analysis/toe_20261118_H27_S5T2_G2_sextic_center_sequential.py, data/toe_20261118_H27_S5T2_G2_sextic_center_sequential.json, tests/test_toe_20261118_H27_S5T2_G2_sextic_center_sequential.py and analysis/2026-11-18_H27_S5T2_G2_sextic_SIC_E8_center_sequential_qutrit.md (this report). Run the Python producer and then Python unittest discovery using the new test filename. JSON data is normally gitignored; stage only these four additive files and force-add this precise JSON file. Do not stage unrelated dirty repository state.
