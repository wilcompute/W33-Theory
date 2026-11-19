# Five TOE frontiers audited together: H27, weak G2, E8 Higgs, three families, and causal-break qutrit memory

Date: 2026-11-18. **Status: 46 new passing mathematical regression tests, with explicit physical limitations. This is NOT a TOE or a measured quantum device.**

## Provenance: what was already in W33-Theory

At intake remote and local master were e7a5725b1a989072aa8294ea70a9e99b86573576, with an empty stage and 19 preexisting modified tracked files belonging to other workflows. No old files are edited.

The repository already established the H27 representation inventory (analysis/2026-09-22_address_operator_h27_intertwiner_obstruction.md), three scalar PW L2 modes for the quartic tilt (analysis/2026-11-18_PW_tilt_perfect_Morse.md), SWAP/causal-break/SWAP three-qutrit density-matrix controls (analysis/toe_20261116_qutrit_SWAP_causal_break_memory.py), flat ordinary Dirac positivity on a smooth Sasaki-Einstein seven-link (analysis/2026-11-18_sixfront_character_winding_continuum_falsifiers.md), and the E6 c=3 compensated Wilson centralizer dimension14 and the four qutrit MUB dimension witness (analysis/2026-11-18_E8_full248_LES_Psi3_weakG2_localMUB.md). Earlier commuting-adjoint Cartan rank preservation is also known from analysis/2026-11-17_TOE_E6_Klein_11cell_11D_uniform_qutrit_fivefront.md. This packet does not relabel those old results as discoveries. Its contribution is connecting the constraints, proving a free spherical quotient obstruction, detecting a possible 3-times-3 family overcount, and calculating an integrated continuous-noise optical memory falsifier.

## 1. H27 cannot be a free deck-transformation group of a round seven-sphere

Represent H27 exactly as triples (a,b,c) over F3 with multiplication

    (a,b,c)*(A,B,C)=(a+A,b+B,c+C+a*B) mod3.

Exhaustive group multiplication, inverse and character checks reproduce 27 elements, 11 conjugacy classes (three singleton and eight size-three), and all 11 irreducibles: nine 1D plus two 3D. The complete character Gram is identity to numerical residual <1e-12. All 1D representations have trivial center, and the two inequivalent 3D Schrödinger representations carry omega or omega-squared center. So an IRREDUCIBLE family bundle with nontrivial central character must have rank exactly three. This finite Stone-von Neumann input and the 9+2 count were ALREADY known in the repo, not newly discovered here.

New global geometric implication: H27 contains the abelian subgroup A={(0,b,c)} isomorphic to C3 x C3. Every character of A has a kernel containing at least three elements (sizes 9 for trivial, 3 for all other characters). Every finite-dimensional complex representation restricted to A diagonalizes into characters, and therefore some nonidentity A element fixes a nonzero eigenvector. Thus no H27 linear orthogonal action on a round sphere can be free. More generally the periodic group-cohomology theorem forbids any free H27 action on a standard topological sphere, because its noncyclic abelian subgroup violates the cyclic-abelian-subgroup condition.

There is therefore NO smooth free spherical space form S7/H27. This does NOT prohibit H27 GAUGE holonomy on a defect complement, other 7-manifold pi1 quotients, or orbifold/singular fixed-point loci. Standard source: https://loeh.app.uni-regensburg.de/teaching/topologie3_ws0910/prelim.pdf and https://homepages.math.uic.edu/~bshipley/ConMcohomology1.pdf .

## 2. Universal positive-curvature obstruction to ordinary FLAT-twisted spinor zero modes on nearly-parallel G2

Assume a smooth CLOSED spin nearly-parallel G2 seven-manifold with nonzero torsion tau0. Standard identity: Ric=(3/8)tau0^2*g, Scal=(21/8)tau0^2. For the ORDINARY geometric spin Dirac twisted by any unitary FLAT gauge bundle,

    D_A^2 = nabla_A^* nabla_A + Scal/4
          = nabla_A^* nabla_A + (21/32)tau0^2.

For every spinor, the quadratic form is >= (21/32)tau0^2 times its norm squared. Therefore its entire spectrum has eigenvalue squared >=21tau0^2/32 and kernel ZERO. This covers flat E8/H27 Wilson characters on a smooth closed nearly-G2 background, not just the previously studied round S7 or a special Sasaki-Einstein link. At the restricted Freund-Rubin matching tau0=2/L, it gives (D_A)^2 L^2>=21/8.

A NONFLAT gauge connection changes the Weitzenbock formula by a curvature Clifford-endomorphism. A necessary condition for an ordinary zero mode is a negative curvature contribution strong enough to cancel Scal/4 somewhere; any uniform bound on that term strictly less than 21tau0^2/32 still forbids zero modes. We do not derive an explicit physical field strength.

Positive Ricci also implies by Bonnet-Myers that the global pi1 is FINITE, and by Bochner the real first Betti number vanishes. With Ric=6k*g, k=tau0^2/16, diameter <=4pi/|tau0|=2pi L at tau0=2/L. Thus the infinite pi1 of a wire-complement cannot be the pi1 of the whole smooth closed positive-Einstein Y7. Similarly, a globally smooth closed AND coclosed source-free real Abelian Higgs one-form must vanish.

None of this prohibits flux-coupled 11D supercovariant fermion operators, nonflat ADE fields, singular G2 defects, boundary Dirac projectors or eta/inflow: those are exactly the necessary missing physical ingredients. Sources: https://doi.org/10.1007/s10455-022-09853-1 , https://mural.maynoothuniversity.ie/id/eprint/10069/1/Davidwraithscalar2021.pdf , https://d-nb.info/1123465274/34 .

## 3. After the concrete c=3 E8 Wilson holonomy, *any collection* of parallel adjoint VEVs preserves the extra Abelian rank

The previous verified order-seven SU5 Wilson with Psi phase c=3 leaves E6 algebra

    h = su3_color (8) + su2_weak (3) + u1^3 (3), dim14.

The full E8 family part has no extra invariant adjoint under the order-nine Clifford/H27 holonomy. Its remaining gauge algebra is therefore h, whose center z(h)=u1^3 has dimension three. EVERY globally covariantly PARALLEL E8 adjoint Higgs VEV fixed by the Wilson loops lies in h, so it commutes with ALL THREE central U1 generators. Their common stabilizer always contains z(h), even when the various parallel adjoint Higgs VEVs do not commute with each other.

The Standard Model requires only one U1, so this entire restricted parallel-adjoint class cannot remove the two extra U1s. Earlier rank-preservation observations had already noted the Cartan problem; the sharper statement here applies to all parallel adjoint VEVs under the specifically certified E8 H27 Wilson algebra. Nonparallel Higgs, charged matter representations, localized sources, different global bundles or Green-Schwarz/Stueckelberg physics can evade the stated scope but must be constructed.

## 4. Hidden family multiplicity: 3 scalar PW modes times an independent H27 fiber of dimension3 gives 9, not3

Earlier tilted harmonic PW quartic has a scalar L2 kernel of dimension3. Independently, a nontrivial-center irreducible H27 Schrödinger coefficient bundle has fiber dimension3. If the Dirac/Witten operator factorizes with trivial fiber action, then

    D_total = D_PW tensor I3,
    ker D_total = ker(D_PW) tensor C3,
    dim ker(D_total)=3*3=9.

An exact finite-matrix nullspace control uses Q=diag(0,0,0,2,5): dim ker Q=3 whereas dim ker(Q tensor I3)=9. An incorrect construction that simultaneously treats the three spatial modes and three family fiber states as independent generations will overcount by a factor3. Actual non-Abelian gluing and Wilson sectors can break this tensor-product assumption; the check is a necessary accounting control, not a theorem of a charged 7D compactification.

We also independently re-solved the tilted quartic a=1 critical equations. The three critical points form an isosceles NON-EQUILATERAL triangle, with distances about 1.88708005,1.88708005,2.14865267 (ratio1.13861236). Hence no rigid Euclidean C3 isometry cycles those three sites. This does not exclude a nonlocal/projective H27 action on the ZERO-MODE HILBERT SPACE, but that action must be built and shown to commute with the physical operator.

A credible three-family completion must either identify the 3D scalar kernel ITSELF with the H27 triplet and prove a compatible action, or add a genuine coupling that lifts the six spurious product modes without reversing chirality or violating anomalies.

## 5. Three-time causal-break qutrit memory: explicit continuous noise, four local MUBs and finite-shot falsifier

Previous repo work already had SWAP -> trace/reprepare S -> SWAP with an entangled reference and E memory, plus dephasing and no-return controls. This packet independently constructs FULL 27x27 density-matrix channels with arbitrary middle reset k=0,1,2 and introduces a continuously depolarized E memory:

    Delta_t(E-rho) = t*(E-rho) +(1-t)*I_E*Tr_E(E-rho)/3.

Start with Phi3 on reference R and system S and memory E=|0>. SWAP(S,E), then apply Delta_t to E, then perform a causal break (discard S and independently prepare |k>, one of0,1,2), then SWAP(S,E) again. The output R:S is independent of k and EXACTLY

    rho_RS = t |Phi3><Phi3| + (1-t) I9/9.

At t=3/4, F=<Phi3|rho_RS|Phi3>=7/9 and the four local MUB average same-outcome probability is P_match=(1+3F)/4=5/6. The full 9x9 four-MUB 2-design identity was rebuilt independently with residual <2e-12. The coherent t=1 control returns F=1. Classical dephasing of E yields F=1/3, and fully depolarizing E gives F=1/9.

Under a genuine isolated-reference causal break with NO other R-to-S information path, any CLASSICAL measure-and-reprepare memory E yields an entanglement-breaking reference-to-output channel: F<=1/3 or P_match<=1/2. To certify *intrinsic qutrit* Schmidt number3 instead, the stricter null is F<=2/3 or P_match<=3/4.

Exactly inverted one-sided fixed-n binomial statistics at confidence99% and design-point power>=90% for the t=3/4 output:

    null type                  p_match null      minimum accepted n   reject for >=k matches
    classical/EB memory       <=1/2             27                   20
    rank-at-most2 memory      <=3/4             317                  256

At n=27,k=20, exact type-I=0.00957864523 and model power=0.93225965948. At n=317,k=256, exact type-I=0.00924794863 and power=0.90245274636. The n=27 coincidence with H27 group order is statistical ONLY and is NOT a derived relation.

For independent symmetric ternary detector label error epsilon per measurement, with errors split equally among two wrong labels, if the confusion matrix is KNOWN EXACTLY then the rank3 witness needs n=317 at epsilon0, n=348 at1%, n=389 at2%. In reality calibration uncertainty, source launches vs accepted trials, losses, herald bias, reference leaks, drift and true process tomography must be controlled.

This is a constructive quantum-environment-memory process across a middle causal break. It does NOT solve the stronger genuine-three-time-only problem of Beyer et al in which pairwise reductions are classical: here the early-to-late channel already retains quantum entanglement. See https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs and https://doi.org/10.22331/q-2021-04-26-440 .

## Next five independent PHYSICAL steps

1. Construct an actual nonflat/singular E8-ADE 7D charged Dirac with physically admissible boundary projectors, real-spinor chirality and local anomaly inflow. Plain flat Wilson lines on smooth positive-scalar Y7 cannot work.
2. Build global E8-descending nonparallel/charged Higgs sections and show the two additional U1s obtain physical masses, while removing exotics and stabilizing full Higgs moduli.
3. Solve the 11D weak-G2/FR geometry, full KK/flux equations and quantization on a geometry that can actually carry the defect topology; abandon the impossible free spherical H27 quotient.
4. Choose ONE physical realization of the family triplet; demonstrate that PW zero modes and H27 irreducibility are IDENTIFIED or coupled so the total spectrum contains three, not nine.
5. Upgrade the noisy controlled qutrit model into an event-ready experiment and a genuinely pairwise-classical but globally quantum three-time process-tensor witness.

## Reproduction

- analysis/toe_20261118_H27_G2_flat_Higgs_qutrit_break.py
- data/toe_20261118_H27_G2_flat_Higgs_qutrit_break.json
- tests/test_toe_20261118_H27_G2_flat_Higgs_qutrit_break.py
- analysis/2026-11-18_H27_G2_sphere_Higgs_family_multiplicity_qutrit_memory.md (this report)

The producer writes the exact/numeric JSON certificate. New independent unit tests cover 27^3 group associativity, 11 irreducible characters and conjugacy classes, free-sphere obstruction, G2 gap and H1, actual E6 c3 Wilson invariants, 3x3 family degeneracy, non-equilateral critical points, all three causal break resets, full 27x27 density positivity and two finite-shot null models. No external numerical constants were fitted. All strong physics claims remain conditional on the precise model domains above.
