# Native chiral topology, common-cover interactions and graded real geometry

Baseline: `3249fff103ea775cc123bbaee46db835035c49f5`. A fresh fetch on November 2 found no later commits on GitHub master. The shared checkout still has unrelated local modifications; this packet preserves them. This is a continuation of three open investigations from the preceding packet, with explicit maps and obstructions. It does not claim a completed physical Theory of Everything or completion of the older full-week/PDF reading request.

Producers: `w33_20261102_chiral_surface_development.py`, `w33_20261102_common_cover_interactions.py`, and `w33_20261102_graded_parent_geometry.py`. Their JSON certificates have the same stems. Regression: `tests/test_w33_20261102_topology_interactions_geometry.py`.

## 1. Maximal native chirality becomes a branched tetrahedral cover

The previous `w33_20261031_tick_loop_rigidity.py` already owns the unique positive completion of each ordered noncommuting pair: for

    B_abc = 2 sqrt(3) Im Tr(P_a P_b P_c),

the maximum is 2, and every ordered noncommuting edge (a,b) has exactly one c attaining it. Its 3,240 cyclic triples account for 9,720 ordered faces. The prior tetrahedron producer owns the 810 completions, and the preceding packet owns octahedron frustration. Those are inputs, not new discoveries here.

The new check shows that each of the 4,860 unordered noncommuting edges belongs to exactly one of the 810 tetrahedral quartets. Reversing (a,b) gives the fourth label d, distinct from a,b,c. Consequently, if two coherently oriented maximal faces share an edge, they belong to the same quartet. On a connected closed oriented simplicial triangulated surface, every maximal face therefore uses one global quartet.

This provides an executable criterion: label one oriented face by any maximal native triple and force the remaining labels across the dual graph. A collision or a forced edge without positive completion is a certificate of failure. Every maximal ordered seed has the same oriented tetrahedron rule; consistency is independent of which of the 9,720 seeds is used.

When development succeeds, sending each vertex to its quartet label gives an orientation-preserving simplicial branched covering of the tetrahedron boundary sphere. At a vertex, the oriented link repeatedly winds around the target's three-cycle link. Thus

    local degree at v = deg(v)/3,
    cover degree d = F/4,
    chi = 2d - sum_v(deg(v)/3 - 1).

Every vertex degree must be divisible by three. This local condition is not sufficient: global development can have nontrivial holonomy.

| Native test surface | Local degrees | Development | Cover degree | Total ramification |
|---|---|---|---:|---:|
| Tetrahedron boundary | 3 | succeeds | 1 | 0 |
| Octahedron boundary | 4 | fails | — | — |
| Periodic triangular 4x4 torus | 6 | succeeds | 8 | 16 |
| Periodic triangular 3x4 torus | 6 | fails globally | — | — |
| Periodic triangular 4x6 torus | 6 | succeeds | 12 | 24 |

Tests additionally check all periods m,n in {3,4,5,6}: these rectangular triangular tori develop exactly when both periods are even. A direct native 9-by-9 matrix evaluation verifies every bond and face of the 4x4 witness.

The mathematical background is established. [Izmestiev and Joswig](https://arxiv.org/abs/math/0108202) study combinatorial projectivities and branched coverings. [Mod 3 arithmetic on triangulated Riemann surfaces](https://doi.org/10.1016/S0304-3975(00)00236-X) connects mod-three face labels with four-colouring. Neither reference is claimed to prove this native Pauli-tensor application; the development rule and its identification with the repository's quartets are supplied here. Riemann-Hurwitz itself is classical.

The repository also already has `BT804_trio_pillow_fano_theorem.md`, describing different degree-two torus-to-sphere pillow quotients, and `2026-10-08_eight_front_TOE_genus53_CY_index3_duality.md`, constructing a different 240-vertex chiral CW surface with an F20 orbifold quotient. Those are not the present120-tick triangular-face model. No first discovery of a torus cover, a chiral surface or Riemann-Hurwitz is claimed here.

### Exact ground counting and removal of extensive ground entropy

Consider the previous supplied pair energy and a positive chiral face term, with J>0, K>3J/2 and lambda>0. If development succeeds, every edge and face simultaneously attains its separate lower bound. Therefore

    E_min = |edges|(2J-4K/3) - lambda |faces|/sqrt(3).

The ground count is exactly 9,720: any one of the 9,720 maximal ordered seed faces determines the whole connected surface, and every seed has the same successful abstract development. At J=1,K=2,lambda=sqrt(3), the 4x4 torus has 48 edges, 32 faces and ground energy -64.

Along growing even-period tori this ground count stays constant, so the zero-temperature ground entropy per vertex tends to zero. This contrasts with the earlier externally specified nearest-neighbour chain's ln(81) residual entropy in `2026-11-01_five_plus_three_w33_physics_continuation.md`. The difference comes from supplied face interactions and the global completion constraint; it is not a spontaneous origin of time or a proof of a finite-temperature phase transition. For failed development, the separate lower bound is unattainable; the exact frustrated energy of odd-period tori remains open.

## 2. The common cover permits only a singlet alternating mixed tensor

The preceding packet built the minimal compatible cover of order 61,440 for the prescribed signed 27-coordinate action and the prescribed unitary four-dimensional spinor action. A common group alone says nothing about an interaction. Here we compute the invariant space linear in the scalar coordinate and bilinear in two independent spinor vectors:

    P(phi,psi,eta) = sum_i phi_i psi^T B_i eta.

For each actual paired generator, the scalar action is `e_j -> (-1)^b_j e_p(j)` and the spinor action is U. The exact equations are

    (-1)^b_j U^T B_p(j) U = B_j.

The entire signed kernel of order 32 acts trivially on the spinor. Reconstructing all 30,720 signed elements shows that only scalar coordinate 0 is fixed by every kernel element. Every other scalar coordinate has a nontrivial kernel character and is forbidden at this degree. This is stronger than looking at the centre alone: an initial guess based on the 16-coordinate central sign would have left too many coordinates. The full kernel calculation rejects that guess. All 32 actual kernel elements are exported with generator words for independent reconstruction.

The remaining coefficient space has dimension 16. Enumerating all 1,920 exact dyadic Gaussian spinor matrices gives an integer Reynolds projector. Its image is checked against every generator. Reducing the generator constraints modulo 1009 with i=469 gives rank 15, an upper bound of one on the characteristic-zero invariant dimension. An exact nonzero Reynolds column attains it. Hence the result is exact over Q(i), not a numerical singular-value estimate.

There is exactly one alternating invariant and no symmetric invariant. Up to scale it is

    phi_0 psi^T Omega eta,
    Omega = [[0,0,1,0], [0,0,0,1], [-1,0,0,0], [0,-1,0,0]].

Omega is nonsingular and every actual U obeys U^T Omega U=Omega. For identical commuting vectors, psi^T Omega psi vanishes identically. Thus the symmetric scalar-times-quadratic-spinor polynomial space is zero; the one-dimensional answer refers to two independent spinors or an appropriately typed alternating tensor. Grassmann statistics and Lorentz contractions are additional data.

The symplectic-form preservation itself is already certified in `w33_20261031_unitary_stabilizer_lift.py`. The present result is the full signed-kernel selection and the exhaustive dimension of the mixed invariant space, not a new discovery of that form.

This does not forbid arbitrary E6 Yukawas, enlarged representations, different quotient maps or higher-degree operators. It says that the actual 27 and 4 actions just constructed cannot generate a general family-dependent interaction at this lowest degree while preserving the full common cover. No mass, coupling magnitude, vacuum or physical fermion identification has been supplied. Symplectic invariant theory and Reynolds averaging are established methods; the contribution is the exact answer and witness for these actual prescribed maps.

## 3. A graded real completion with KO6 signs, and its remaining obstructions

The previous packet constructs `D0(M)=[H,M]` on the Hilbert-Schmidt module Mat9 with `J0(M)=M dagger`, and proves that this 81-dimensional module has no even grading commuting with the full left Mat9 action for this nonconstant H. Merely assigning it a desired KO-dimension would not repair that obstruction.

An explicit completion is now built on C2 tensor C2 tensor Mat9, dimension 324. With Pauli matrices sigma_x,sigma_y,sigma_z, define

    D = sigma_x tensor I2 tensor D0,
    Gamma = sigma_z tensor I2 tensor I81,
    J = (sigma_y tensor sigma_y tensor transpose81) K,

where K is ordinary conjugation in the displayed vectorised basis. Mat9 acts through the unchanged left multiplication on the final factor. The construction satisfies

    J^2=+1, JD=+DJ, JGamma=-GammaJ,
    Gamma^2=1, D Gamma=-Gamma D,
    [Gamma,L_a]=0, [L_a,R_b]=0, [[D,L_a],R_b]=0.

Direct random operator-vector tests independently verify the anti-linear identities. D has spectrum -1 with multiplicity 72, zero with multiplicity 180, and +1 with multiplicity 72.

Two spin components are insufficient **within this tensor ansatz**: the spin antiunitary reversing both sigma_x and sigma_z is proportional to sigma_y K and squares to -1. It produces KO2 rather than KO6 signs. More generally the complex Cl2 module has dimension 2r; the required antiunitary has form `(sigma_y tensor B)K`. Its square can be +1 only if `B conjugate(B)=-I_r`. Taking determinants forces r even. Four spin components attain the minimum, giving 4x81=324. This is not a minimum over all algebras, representations or Dirac operators.

Two further tests prevent over-reading this success:

- Every zero-dimensional orienting cycle built from this algebra and its opposite action is identity on the external spin factor. It cannot equal the nontrivial spin grading Gamma. Orientability in that sense fails.
- For the sole K0 generator e of complex Mat9, `Tr(Gamma L_e R_e)=0`. The one-by-one intersection form is zero, so the chosen Poincare-duality condition fails.

These are familiar distinctions in finite spectral geometry; [Cacic's structure theory](https://arxiv.org/abs/0902.2068) explicitly accommodates arbitrary KO-dimension and failures of orientability and duality. The contribution here is the actual parent-based construction and its checked boundaries. KO6 refers to algebraic reality signs, not six physical spacetime dimensions. The new spectral action is `180 f(0)+144 f(1/Lambda^2)` and remains blind to the 810 conjugate parents. External multiplicity does not create three observed generations or Lorentzian gravity.

## Audit and reproducibility

Fourteen focused tests cover actual matrix traces, unique edge completion, the torus energy, inconsistent global development, seed independence, small torus periods, malformed orientation, all kernel words, exact Omega covariance, alternating-statistics limitations, an independent modular rank and random anti-linear KO6 identities. The publication validation replays these together with the preceding 19 native tests and the 11 loop/tetrahedron tests, for 44 connected tests. The three producer certificates and actual validation logs are archived with hashes.

The source/results were searched across the repository and RESULTS_INDEX. The prior unique-completion, tetrahedral, common-cover and operator-module work is explicitly credited above. General topology, invariant theory and noncommutative geometry are credited to established work; no external priority claim is made. GitKraken tools were unavailable, so Git CLI was used as the fallback for capabilities unavailable through those tools. Continuity log attempts and session notes record the changes; unrelated local work is outside this packet.

Five independent next investigations:

1. Compute the lowest higher-degree mixed operators that neutralise the signed-kernel characters, with exact interaction tensors rather than a group-order analogy.
2. Find and classify the minimal chiral defects forced by odd-period torus holonomy, including their energy and mobility.
3. Extract the actual holonomy representation of general triangulations into tetrahedral permutations and compare its kernel with the native Clifford action.
4. Test enlarged finite algebras and bimodules that admit a nonzero intersection pairing while retaining an explicit parent-based Dirac operator.
5. Build charge projectors and F-move dictionaries for the repaired 27-dimensional Markov carrier, keeping it distinct from the E6 coordinate module.
