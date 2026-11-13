# November 13: Five-front TOE execution — chiral prime tower, action, optics, E6 and five-qubit MUB

**Status:** exact finite algebra, verified integer/numerical calculations, conditional physics toy models, and an explicitly undecided size-eight search. No theory of everything, gravitational continuum, observed chirality, or experimentally built apparatus is claimed.

**Context:** The earlier session audited the full 215-page Forty Points PDF and the last week's 400 pre-existing commits, including corrections. This pass checked repo overlap (W33 rank-one cone, oriented triangles, general-q unoriented spectrum and E6/H27 mapping) before developing the following increments.

## 1. Conditional chiral action

The q=3 27-event null graph and 4+4 oriented null-sheet split were already proved in the repo (Passes 11548–11549). For the positive-step matrix T, write A=T+T^T and D=T-T^T. The 24-element congruence group is transitive on each of the two sheets. Thus a translation- and GL2(3)/±I-covariant nearest-null Hermitian Hamiltonian lies in the real span of A and iD (plus a scalar diagonal); iD is the unique inversion-odd such direction up to scale. This is symmetry **permission**, not a dynamical derivation of a nonzero coefficient.

Assume a classical order parameter b, Hamiltonian b*iD, and a phenomenological even stabilizing potential kappa*b^2/2+lambda*b^4/4. Its single-particle thermal partition function is exactly Z(b)=19+8cosh(3sqrt(3)*beta*b); the free-energy curvature at zero is F''(0)=kappa-8beta. At (kappa,lambda,beta)=(8,32,1.25), two numerical equal minima occur at b=±0.25638414, 0.03483138 below b=0. At beta=0.8, b=0 is stable. This is **not** finite-system spontaneous breaking, nor an E8 vacuum or physical CP selection; the order-parameter potential was assumed.

## 2. Constructive chiral-gate compiler and noise

Four commuting rank-one displacement matrices give U3=exp[tD] as a product of four commuting rotations, t=2pi/(9sqrt(3)). Two are local on individual qutrits; the other two can be conjugated from a local qutrit rotation with two controlled-add (SUM) maps and their inverses. The explicit product uses four one-qutrit rotations and eight qutrit SUM gates; no gate-count optimality claimed. Direct 27x27 reconstruction matches the exact integer polynomial gate to 2.3e-16 entrywise. Each elementary rotation has order nine, while the global gate has order three.

For the **global output** depolarizing model rho_p=(1-p)|psi><psi|+pI/27, Wigner negativity survives iff p<3/4 and is N_W(p)=(16/27)(3-4p) below threshold. Opposite-edge output probabilities differ by (1-p)/27. The replay certificate includes conditional iid Hoeffding finite-shot budgets. These are not local per-gate fault/error thresholds, hardware resource estimates or calibration data.

## 3. Exact oriented chiral prime tower and continuum obstruction

For odd prime q=3 mod4, define N_+ as the distinct rank-one matrices vv^T, v∈Fq² nonzero (two-to-one parametrization); N_-=-N_+. Each orbit has (q²-1)/2 elements and they are disjoint because -1 is nonsquare. Define D_q=T_(N+) - T_(N-).

For a dual Fourier character k, let K(k) be the symmetric two-by-two matrix [[k0,k1/2],[k1/2,k2]]. The eigenvalue of D_q is half the difference of Gauss sums of K and -K. On rank-two forms the Gauss sums are real and equal, giving zero. Rank zero also gives zero. On rank-one forms the single-variable Gaussian factor is imaginary for q=3 mod4 and changes sign under negation; the eigenvalue is ±i*q^(3/2), with multiplicities (q²-1)/2 each.

Consequently:
\[
D_q^3=-q^3D_q,\qquad \operatorname{rank}D_q=q^2-1,\qquad
P_{\rm active}=-D_q^2/q^3,\qquad
U_q=\exp(2\pi D_q/q^{5/2}),\quad U_q^q=I.
\]

At q=3 this recovers the previous rational U3. Exact integer convolution checks and Fourier controls pass for q=3,7,11,19: (states,active,frozen)=(27,8,19),(343,48,295),(1331,120,1211),(6859,360,6499). Opposite-character controls q=5,13 give inversion-stable positive rank-one orbits and zero antisymmetric full-congruence orbit difference, **not** a no-go for every symmetry-breaking chiral Hamiltonian.

The active fraction (q²-1)/q³ tends to zero, giving a severe continuum obstruction for **this** chiral tower. The earlier repository already proved an independent normalized-Laplacian continuum firewall for the unoriented general-q null graph; neither construction derives gravity.

## 4. Explicit E6 cubic compatibility falsifier

The repository stores the actual signed 45-term E6 cubic and the current 27-coordinate E6-to-H27 address dictionary. Under a **specific, non-equivariant** coordinate identification of an affine-history address (a,b,c) with an H27 normal-form address of the same triple, all input basis vectors have cubic norm zero, while every transformed basis vector under U3 has nonzero cubic norm. For the history origin e0:
\[
N(e_0)=0,\quad N(9U_3e_0)=46,\quad N(U_3e_0)=46/729.
\]
So this *naive address transport* does not preserve the signed E6 cubic. The affine group F3³ is abelian and the physical Heisenberg H27 is nonabelian; equal 27-element address sets are not automatically equivalent representations. This does not exclude a different, properly specified intertwiner, nor make any prediction about physical Yukawa couplings.

## 5. Five-qubit eight-basis MUB frontier

Replayed the repository's DLX rank-code search with four workers, 120 seconds per orbit, plus its three-qubit size-five positive and size-seven negative controls. All eight five-qubit orbit jobs timed out after a combined 4,310,000 search nodes (245.5 seconds wall). The result is **UNDECIDED**, with no eight-basis witness, *not* a proof that eight is impossible.

Separately reran the repository's positive nine-basis verifier. Its seven symmetric rank-code matrices are [980,30085,20322,22520,4690,21838,7411], together with two complementary fixed Lagrangians. The code checks isotropy, pairwise disjointness and all 13,888 nonsingular symmetric extensions, finding zero. Pass12649 previously established the lower bound eight; hence the strict supported interval remains 8 or 9. The 2021 Mathematics 9(12) 1388 study also found nine-basis examples without ruling out eight.

## Reproducibility

- Prime family: analysis/toe_20261113_chiral_prime_tower.py; data/toe_20261113_chiral_prime_tower.json
- Action, circuit and noise: analysis/toe_20261113_chiral_action_compiler_noise.py; data/toe_20261113_chiral_action_compiler_noise.json
- Exceptional cubic test: analysis/toe_20261113_chiral_e6_cubic_compatibility.py; data/toe_20261113_chiral_e6_cubic_compatibility.json
- MUB status audit: analysis/toe_20261113_five_qubit_eight_audit.py; data/toe_20261113_five_qubit_search_boundary.json
- Standalone regression: python tests/test_toe_20261113_five_fronts.py (five passing checks, q5/q13 negative controls, no timeout promotion).

Literature anchors: Gross 2006, DOI 10.1063/1.2393152 (finite Wigner Hudson theorem); Enhanced quantum transport in chiral quantum walks, DOI 10.1007/s11128-024-04331-y (loop-phase gauge invariants); Unextendible Sets of Mutually Unbiased Basis Obtained from Complete Subgraphs, Mathematics 9(12) 1388, https://www.mdpi.com/2227-7390/9/12/1388.

**The TOE-level missing principles remain:** select a Hamiltonian from physics, define real temporal signature and a continuum, derive masses/forces/gravity with a falsifiable vacuum, and implement/test the finite gate with measured noise. The results above are mathematical closure and direct physical-model falsifiers, not a claim to have solved those larger tasks.
