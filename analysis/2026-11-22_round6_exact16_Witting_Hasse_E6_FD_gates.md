# Round 6: globally minimal Witting IC-POVM, sharp W33 Hasse cut, Hessian synthesis, and E6 falsifiers

**Research date:** 2026-11-22. **Repository:** `wilcompute/W33-Theory`, `master`. **Research boundary:** exact finite-dimensional geometry and conditional numerical/model-building results; none of the claims establishes quantum gravity, a Standard Model vacuum, or a Theory of Everything.

## Source audit / prior art

Read the live master and the prior Round 3–5 source/certificates, including `toe_20261122_witting_qutrit_sic_mub30.py`, `toe_20261122_round5_18effect_optical.py`, `toe_20261122_round5_e6_grade_leakage.py`, `toe_20261122_e6_132_constructive_embedding.py`, and the exact Hessian compiler. Witting/Penrose 40-ray orthogonality and Kochen–Specker properties are prior art (Aravind et al., https://users.wpi.edu/~paravind/Publications/penrosedodec.pdf). Minimal informationally complete POVMs with d^2 effects are established in general (https://doi.org/10.1142/S0219749920400055; https://journals.aps.org/pra/abstract/10.1103/PhysRevA.102.032221). **Our scoped new result is this explicitly verified weighted 16-ray support inside the repository's canonical Witting 40 rays. We claim no exhaustive literature priority.** The W33 generalized quadrangle and its strongly regular parameters are classical (https://homepages.cwi.nl/~aeb/math/srg/rk3/srgw.pdf). Solovay–Kitaev theory predates these compilations (https://arxiv.org/abs/quant-ph/0505030).

## 1. Exact 16-effect Witting MIC: global outcome-count optimum

Let the canonical zero-indexed ray projectors be `P_j`, `j=0,...,39` as defined in `toe_20261122_witting_one_phase_three_fixed.py`, each normalized to trace one. Choose

```
S = (1,2,5,6,7,8,9,16,17,22,28,29,30,31,34,35)
H = (6,9,17,30)
E_j = (2/5) P_j for j in H; (1/5) P_j otherwise.
```

**Exact normalization:** `sum_{j in S} P_j + sum_{j in H} P_j = 5 I_4` in Q(omega), so the effects are positive and sum to the identity. There are precisely sixteen positive rank-one effects.

**Exact informational completeness:** the unweighted 16-by-16 rational Hilbert–Schmidt Gram matrix `G_ij = tr(P_i P_j)` has diagonal entries 1, 90 ordered off-diagonal zeros, and 150 ordered off-diagonal entries 1/3. Its exact determinant is

`det G = 25 / 3^10 = 25/59049 > 0`.

Thus the sixteen projectors linearly span all Hermitian 4-by-4 operators. Six independent finite-field projector-rank checks, over primes `7,13,19,31,37,43`, all return 16. Sixteen is **globally minimal in outcome count**, because a 4-dimensional quantum state has a 16-dimensional real Hermitian operator space; fewer outcomes cannot have full-rank linear statistics. This result does **not** imply a symmetric SIC: the pairwise overlaps are 0 or 1/3 rather than constant, and the effect weights are unequal. The ideal weighted superoperator condition number is approximately **48.6269**.

A reproducible LP discovery script uses random objective seed 481 and obtains the above 16-index support after 356 earlier objective draws. Random LP does not prove optimality; the exact determinant and dimension bound do.

## 2. Direct 16-port photonic Naimark isometry and finite-loss benchmark

Take the 16-by-4 isometry with rows `sqrt(w_j) <v_j|`. Its conjugate transpose times itself is the identity. The existing row-local adjacent Givens decomposition reconstructs the isometry and uses **54 two-mode couplers**. With **illustrative** per-affected-mode intensity transmission `eta=0.995`, the baseline seeded pure-state detection probability is about **0.950958**, the source-photon squared Hilbert–Schmidt error coefficient is about **39.8043/N**, and the analytic Haar-pure average error coefficient is **46.4360/N**. Among 61 tested output orderings, the best Haar-average coefficient is **46.1959/N**; this is *not* a global hardware-routing optimum.

The earlier **19-outcome** design has more couplers (65–66 in a tested implementation) but better Haar-pure average error, about **36.5/N**. The 16-effect design is mathematically minimal by output count and wins the tested default circuit-depth comparison, **not** necessarily reconstruction fidelity per source photon. The model includes no-click events and output-state-dependent loss, but omits actual laboratory coupling, source/detector inefficiencies, phase drift, and multiphoton constraints.

## 3. Sharp W33 causal-cover obstruction and constructive 20+20 cut

Construct W33 from symplectic orthogonality on the 40 points of PG(3,3). It has `(v,k,lambda,mu)=(40,12,2,4)`, 240 edges and exactly 160 triangles; every edge lies in two triangles. No triangle may occur in the underlying cover (Hasse) graph of a partial order, as an acyclic orientation of a triangle always contains a transitive shortcut. Therefore at least **160/2=80 edges must be deleted** if W33 adjacencies are to be used as direct causal covers.

The source contains an **explicit binary vector of length 40 with twenty 0s and twenty 1s** and proves for the W33 adjacency matrix A that

`A^2 = 8I - 2A + 4J`, and `A (2c-1) = -4(2c-1)`.

Hence exactly **160** edges cross the 20+20 partition, with crossing degree eight for every vertex. Orienting all crossing edges 0-to-1 yields a valid **height-two poset**, so the lower bound of 80 deletions is attained. The minimum number of W33 edges needing deletion to make a *some* Hasse graph is **exactly 80**. The adjacency spectrum is `{12^1, 2^24, (-4)^15}`. The general max-cut spectral bound `m/2 - lambda_min v/4 = 120+40 = 160` proves the partition is also an optimal W33 cut.

**Physical limitation:** the constructed poset has no proper causal intervals with interior elements. It is not manifoldlike or a Lorentzian continuum; the theorem merely restricts interpreting *all* graph edges as elementary causal links. W33 can still enter more elaborate enriched causal models as auxiliary or spacelike structure.

## 4. E6/H27 complete-twirl physical null

The previously certified H27-equivariant 81-to-132 isometry maps three regular H27 address modules into `78_adj + 27 + 27bar`; its 81-dimensional image is H27-invariant but not E6-invariant. Compact E6 group averaging acts by Schur's lemma on three inequivalent multiplicity-one irreducible summands. The resulting twirling channel is

`T(rho) = Tr(P_78 rho) I_78/78 + Tr(P_27 rho) I_27/27 + Tr(P_bar27 rho) I_bar27/27`.

It has a three-dimensional operator image and is measure-and-prepare, therefore entanglement-breaking with zero quantum capacity. Each of the **81 canonical regular-H27 address basis vectors** constructed in the Fourier isometry has the same three irrep populations, exactly `1/3,1/3,1/3`; after full E6 twirl, all 81 become the identical density matrix `diag(I_78/234, I_27/81, I_bar27/81)`.

**Crucial limitation:** full E6 Haar-twirling is an intentionally severe conditional noise model, not implied by E6 covariance, gauge invariance, or any actual experiment. It does not rule out error correction under physically restricted channels or use of a larger E6 carrier. It does show that treating a full-symmetry twirl as innocuous would erase all canonical address labels.

## 5. E6 F/D-flat adjoint–singlet vacuum, with its family-modulus obstruction

For a toy **vectorlike** three-family `27_i + bar27_i` coupled to an E6 adjoint `A`, take E6-invariant renormalizable

`W = m sum_i barH_i H_i + lambda sum_i barH_i A H_i + (M/2) Tr_27(A^2)`.

Under the standard SO(10)-singlet ansatz `H_i=u_i |1_4>`, `barH_i=v_i <1_4|`, `A=a Q`, where `27=16_1+10_-2+1_4` and `Tr_27 Q^2=72`, the restricted superpotential is

`W_s = (m+4lambda a) s + 36 M a^2`, where `s=sum_i u_i v_i`.

Its nonzero F-flat solution is

`a = -m/(4lambda)`, `s = 9 M m/(2 lambda^2)`.

For real positive `m=M=lambda=1`, `a=-1/4`, `u_0=v_0=sqrt(9/2)`, and other u_i,v_i zero, the singlet F-terms vanish and the conjugate 27+bar27 choice plus real Cartan adjoint makes all gauge D-terms vanish. SO(10) invariance ensures the adjoint F-source points along Q for this singlet ansatz.

**But it is not an isolated vacuum.** In the seven complex variables `(u_i,v_i,a)`, the F-term Jacobian has rank two, leaving five complex tangent directions. Quotienting the broken complex U(1) gauge orbit leaves **four complex family moduli**. The uniform bilinear/adjoint couplings have an accidental complex GL(3) family symmetry even if H27 is also imposed. The full nonsinglet mass spectrum, Goldstones, chiral families and potential dynamical lifting are not solved.

## 6. Compact Hessian gate-word compiler: explicit failure controls

A bounded-width beam searches the exact normal form `H(DN)^k`, where `|H|=648` is the Hessian group, `N` is the normal Heisenberg subgroup of order 27, and D is a Witting phase flip. It stores 81 candidate right-words after each depth, then tests single-site replacements through coordinate descent over all 27 Heisenberg choices. Each candidate has a corresponding explicit primitive generator word, but this is a *heuristic*, not a Solovay–Kitaev implementation.

For three reproducible Haar U(4) targets, beam-search depth-eight errors are approximately `(0.48159, 0.42193, 0.46579)`; 81-start local refinement improves these to `(0.43254, 0.41337, 0.37046)`. The earlier exact stage-four distances `(0.3364, 0.3638, 0.3876)` beat the refined heuristic on the first two targets, demonstrating that **longer heuristic words need not be better**. The first two beam stages reproduce the previously enumerated `H D H` and `H D H D H` optima for their target; later depths are incomplete. Dense-gate compilability follows from known Solovay–Kitaev results under the previously certified density hypothesis; this search does not establish polylog runtime or fault-tolerant overhead.

## Tests and provenance

Run `OPENBLAS_NUM_THREADS=1 python -m pytest -q tests/test_toe_20261122_round6_five_and_more.py` in a checkout that contains preceding analysis files. **Thirteen focused tests pass locally.** Run `python analysis/toe_20261122_round6_execute_all.py` to regenerate seven source-backed JSON certificates and one manifest. Prior remote GitHub Actions jobs were queued at audit time; a queued job is not a pass. The user Windows directory has not been synchronized.

### Recommended independent next fronts

1. Classify **all** symmetry orbits of 16-ray Witting MIC supports, and seek optimal-conditioned and minimal-coupler representatives.
2. Replace bounded beam synthesis by a certified **Solovay–Kitaev/commutator compiler** with a compact Hessian net and precision-dependent resource bounds.
3. Study full E6-invariant error channels and explicit active-recovery conditions on the 132D carrier, not only full Haar twirling.
4. Break the accidental flavor GL(3) with **H27-invariant higher tensors** and solve the complete E6 F/D-flatness and chiral-spectrum problem.
5. Develop a genuine **multi-layer Lorentzian causal-order model** on an enriched W33 scaffold and distinguish it from the sharp 160-edge height-two null using interval abundances and propagation.
