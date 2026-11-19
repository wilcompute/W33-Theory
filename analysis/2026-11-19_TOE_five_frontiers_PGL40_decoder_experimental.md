# TOE research packet: PGL(4,3) logical symmetry, optimal 40-qutrit checks and five physical falsifiers

**Date:** 2026-11-19. **Status:** exact finite algebra and reproducible numerical tests; explicitly separated from speculative physical extrapolation. **This is not a Theory of Everything, not a UV-complete SIC sector, not a G2 compactification, and not a hardware fault-tolerance demonstration.**

## Starting point / novelty firewall

Continued from `22a122ec8dd2761a61739eef5cd5698ebe1eab51`, with local and GitHub master initially synchronized and pre-existing uncommitted work preserved. Relevant already-committed source files:

- `analysis/toe_20261119_w33_40_qutrit_css.py` constructs the point-CSS code `[[40,19,4]]_3`, independently of the separate W33 **240-edge** CSS code; it previously proved `d_X=4,d_Z=6`.
- `analysis/toe_20261119_five_frontier_bridge.py` constructs a classical anomaly-free 9-pair SU3 Hesse-SIC EFT and models a SWAP causal-break qutrit memory experiment.
- Parallel commit `867f70b` independently constructs a **renormalizable**, anomaly-free **10-pair** SU3 SIC model. We do not claim its work as new.
- Pass4948 proves the modular identity `(I+A)^2=J` over F3. Pass7733-7740 already proves the classical polarisation-independent row codes `C11=[40,11,13]_3` and `C10=[40,10,18]_3` and the census of 1560 quadratic minimum-weight words. We do not reattribute them.

**Parallel-collision update:** during this pass, independent commit `3edb3b9` landed on GitHub, explicitly deriving the same nine-versus-ten-pair beta comparison and torus-only magnetic Dirac obstruction. It also supplies a stronger no-go for arbitrary site-dependent T9 powers plus diagonal Clifford corrections, a related low-weight CSS decoder, and an encoded-resource injection discussion. Those are **parallel findings, not our exclusive novelty**. Our distinct increments here are the exact PGL4 action on the 19 logical qutrits and its Jordan form, the geometrically optimal 323-support check basis, an independent uniformly depolarizing guarantee, and the four-MUB finite-shot witness and explicit cycle-factor refinement. The latter adds spatial cycles by hand and is not emergent gravity. No unverified literature-priority claim is made.

## 1. An exact PGL(4,3) symmetry acting on physical and logical qutrits

Let `P=PG(3,3)` be 40 projective 1-spaces of F3^4, and let `A` be the W(3,3) collinearity graph from any nonsingular alternating form. Define the CSS checks

`H_X=I+A` and `H_Z=I+A-J` over F3.

Every row of `H_X` is the incidence vector of a **projective hyperplane**:
`N(p)={q:<p,q>=0}`. Nondegeneracy sends the 40 projective points bijectively to the 40 projective hyperplanes. Therefore the X-check row space is intrinsic to PG(3,3) and preserved by **all** projective linear transformations, not merely the fixed symplectic subgroup.

Moreover each hyperplane indicator has coordinate sum `13=1 mod3`. Differences of two such indicators span the 10-dimensional augmentation subcode `C10=row(H_Z)`, so that space is PGL invariant too. These two facts prove that PGL4 acts by **physical-qutrit permutations preserving both CSS stabilizer spaces**.

An independent machine certificate checks every elementary transvection `E_ij(1)` (12) and `diag(-1,1,1,1)` (one), generators of GL4(3), on both check spaces. The projective scalar kernel is `{+I,-I}`, yielding

`|PGL(4,3)| = ((81-1)(81-3)(81-9)(81-27))/2 = 12,130,560`.

This is **468 times** the order 25,920 of PSp4(3) preserving a fixed W33 symplectic structure. The enlarged symmetry belongs to the code, not necessarily to any chosen W33 adjacency matrix.

The resulting 19-dimensional logical X quotient is `ker(H_Z)/row(H_X)`. A coordinate transvection produces a nonidentity order-3 logical action `T`, with

`rank(T-I)=10, rank((T-I)^2)=3, (T-I)^3=0`.

Hence its characteristic-three Jordan block multiplicities are **size1:2, size2:4, size3:3**, summing to 19 logical qutrit dimensions. This is a faithful demonstration of a nontrivial encoded gate action by a geometrically defined wire permutation; it does not guarantee a low-depth or low-noise circuit layout.

## 2. Optimal 21-generator CSS check basis, 90 supports saved

Each plane indicator has weight 13. Any two different projective hyperplanes in PG3(3) intersect in a four-point projective line, so their difference has weight `2*(13-4)=18`.

Choose **11 linearly independent** incidence vectors `X_0,...,X_10`. Then define **10** checks `Z_i=X_(i+1)-X_0 mod 3`. Their row space is exactly `row(H_Z)`, and all are weight 18. The X checks have weight 13. The optimal stabilizer-generator total support is therefore

`11*13 + 10*18 = 323` nonzero entries, versus `11*13+10*27=413` for independent rows selected directly from the original matrices.

This is a **90 entry / 21.79% reduction**, with explicit lists of positions and qutrit coefficients saved in JSON. Exhaustively checking all `3^11` words in C11 and all `3^10` in C10 independently certifies their minimum weights `13,18` and the respective minimum-weight word counts `80,1560`. Those minimum distances prove 323 is the *global minimum over independent ordinary CSS generator bases*. This does **not** prove a minimum number of physical entangling gates, fault-tolerant readout depth, or immunity to hook errors.

Certificate `analysis/toe_20261119_w33_40_sparse_css_checks.py`.

## 3. Guaranteed biased-noise decoder, and a logical ninth-root gate obstruction

For the 40-qutrit code with `d_X=4,d_Z=6`, an exact, nondegenerate low-weight syndrome lookup has:

- X part: `1 + 40*2 = 81` syndromes for X weight at most 1.
- Z part: `1 + 40*2 + choose(40,2)*2^2 = 3,201` syndromes for Z weight at most 2.

All those syndromes are distinct because any collision would yield an undetectable vector of weight at most 2 (X) or 4 (Z), contradicting the certified classical kernel distances. Lookup corrects **every mixed Pauli error with X-weight <=1 and Z-weight <=2**, even when X and Z overlap at a site. For an independent qutrit depolarizing channel assigning probability p to one of 8 uniformly distributed nonidentity Pauli errors per site, the exact probabilities of being in the guaranteed-correctable set are:

| physical Pauli error p/site | guaranteed correction probability lower bound |
|---|---|
| 0.001 | 0.999568 |
| 0.005 | 0.989906 |
| 0.01 | 0.962875 |
| 0.02 | 0.874639 |
| 0.05 | 0.529223 |

These are **guaranteed recoverable pattern probabilities**, not simulated logical failure rates under a noisy syndrome-extraction circuit. Unknown higher-weight errors may also be correctable.

**Magic gate counterexample:** Let `T9=diag(zeta9^(j^3))` for j=0,1,2, `zeta9=e^(2pi i/9)`. For any weight-13 all-ones X stabilizer row `h`, the CSS zero logical coset includes `|0...0>` and `|h>` with equal amplitude. The uniform gate `T9^tensor40` changes their relative phase by `zeta9^13=zeta9^4 !=1`. It consequently **does not preserve the CSS codespace**. This rules out that straightforward transversal implementation, not nonuniform transversal gates, injection, distillation or compiled gates. The concurrently published `3edb3b9` independently proves a **stronger** obstruction for arbitrary site-dependent T9 powers together with single-site diagonal Clifford phases; our one-row calculation is a transparent corollary, not a claimed new no-go theorem.

Certificate `analysis/toe_20261119_pgl40_five_frontier_falsifiers.py`.

## 4. SUSY SIC ultraviolet audit

Our prior holomorphic SU3 SIC model has **nine fundamental/antifundamental flavor pairs**; the parallel renormalizable model has **ten pairs**. For massless N=1 SU(Nc) SQCD the one-loop gauge coefficient is `b0=3Nc-Nf`. With Nc=3,

- 9-pair model: **b0=0**, at the upper boundary `Nf=3Nc` of the conventional SQCD conformal window.
- 10-pair parallel model: **b0=-1**, not perturbatively asymptotically free.

This is a decisive RG diagnostic but **not a UV completion** of either model. The nine-pair EFT contains irrelevant `S*det(Q)/Lambda` terms and an explicit physical cutoff; one-loop b0=0 does *not* force the exact NSVZ beta numerator to vanish, because `(1/2)*sum gamma_i` remains at this boundary. The renormalizable ten-pair model is weak-coupling IR-free in the usual gauge-sector approximation, not automatically UV safe. No new E8 dynamics, realistic particle spectrum or naturally chosen 19 baryonic parameters is derived.

Background: https://qft.org/models/supersymmetry/sqcd/ .

## 5. Nonflat magnetic flux still cannot remove the product seven-dimensional Dirac gap

For the specific smooth H27 quotient `Y7=(S5(R)*T2)/H27`, the earlier work excluded zero modes for the ordinary Dirac operator with **flat** unitary twists. A more general analytic identity now extends the obstruction to any gauge connection pulled back entirely from the torus, **even if its torus magnetic curvature is nonzero**:

`D_product,A^2 = D_round_S5^2 tensor I + I tensor D_T2,A^2 >= (25/(4R^2)) I.`

The 2D torus Dirac index equals an integer magnetic flux `m`; `|m|` chiral zero modes may exist **on the torus** while the seven-dimensional product Dirac has zero kernel. In particular, fluxes `m=9,18,-9` have ordinary magnetic-translation commutator phase `exp(2pi i m/9)=1`, compatible with the two one-third torus translations at this abelian lift level. This is conditional on the assumed smooth equivariant product-pullback connection. Even though the torus factor carries zero modes, the S5 gap remains `5/(2R)`.

**Physical inference (also independently obtained in parallel commit `3edb3b9`):** Adding *torus-only* U1 or unitary pulled-back gauge curvature will not produce massless charged bulk Dirac modes for this product candidate. A sphere-dependent nonproduct gauge field, singular ADE locus, torsionful/supercovariant operator or different compactification remains open. No actual four-dimensional chirality or anomaly inflow is derived.

## 6. Four-MUB finite-shot three-time qutrit memory witness

Use maximally entangled reference-output qutrits `|Phi3>` and the four qutrit mutually unbiased bases: eigenbases of `Z, X, XZ, XZ^2`. Measure R in each basis and final S in the **conjugate basis**. Let `C_b` denote same-label probability.

The exact, independently tested operator identity is

`sum_b P_same,b = I9 + 3|Phi3><Phi3|`, so `F_Phi=(sum_b C_b-1)/3`.

Every separable R:S output has `F_Phi<=1/3` and thus `sum_b C_b<=2`, equivalently average coincidence at most 1/2. Under isotropic depolarization of the stored qutrit by p, the coincidence probability in every basis is `q=1-2p/3`.

At p=0.5, q=2/3. With an independent identically prepared output state and independent trials, **83 detections per basis, 332 detected pairs total**, meet a conservative one-sided Hoeffding design: 1% maximum false positive under separability and at least 99% guaranteed detection probability for the specified isotropic alternative. Under independent 70% collection probability, **509 launched pairs** suffice for at least 99% probability of collecting 332 detections; this is a statistical collection calculation, not a detection-loophole cure.

If the source drifts with measurement choice, detector efficiencies are state-dependent, or the reference was not isolated, the witness interpretation can fail. Randomize the choice of basis *after* output preparation and certify causal-break operations; a proper loss-aware, potentially loophole-free test still requires additional work.

Background: https://doi.org/10.22331/q-2021-04-26-440 and https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs .

## 7. A controlled 3D continuum refinement — and the reason it is not derived gravity

The 40-point W33 graph Laplacian has spectrum `0^1,10^24,16^15`; by itself it has a fixed gap and no spatial continuum. Define a **model chosen by hand**, the Cartesian product `W33 x C_m x C_m x C_m`, with the three cycle Laplacians scaled by `m^2`.

The first nonzero spatial eigenvalue is `4 m^2 sin²(pi/m)`, converging to `4pi²` as `m->infinity`. Its relative errors at `m=8,12,24,48` are respectively **5.04%, 2.26%, 0.570%, 0.143%**. The fiber-constant sector approaches a 3D torus scalar-wave continuum, while the other 39 fiber modes carry finite internal mass squares 10 and 16 at fixed fiber coupling.

This is an explicit test of how **adding external spatial refinement** would permit a 3+1-dimensional wave limit, and a sharp demonstration that W33 alone does not establish such an emergence. We have derived neither an Einstein-Hilbert action nor a diffeomorphism/ADM constraint algebra. No TOE claimed.

## Executables and data

```powershell
python analysis/toe_20261119_pgl40_five_frontier_falsifiers.py
python analysis/toe_20261119_w33_40_sparse_css_checks.py
python -m unittest discover -s tests -p test_toe_20261119_pgl40_five_frontier_falsifiers.py -v
python -m unittest discover -s tests -p test_toe_20261119_w33_40_sparse_css_checks.py -v
```

JSON: `data/toe_20261119_pgl40_five_frontiers.json` and `data/toe_20261119_w33_40_sparse_css_checks.json`.

## Five independent next falsifiers

1. Derive SIC-flavon couplings from a specified anomaly-consistent E8 representation and analyze full NSVZ beta functions and threshold corrections, not just one-loop b0.
2. Compute a charged nonproduct/singular seven-dimensional Dirac zero-mode index with explicit connection, boundary conditions, and anomaly inflow.
3. Translate the four-MUB memory witness to a loss-aware photon/qutrit interferometric circuit, with randomized measurement settings and an explicit detection-loophole treatment.
4. Construct a refinement process from W33 incidence itself, rather than adjoining three arbitrary cycle factors; then test the Hamiltonian constraint algebra for GR.
5. Implement a noisy, hook-error-aware ancilla measurement schedule using the optimal 323-support CSS basis, then benchmark decoder and magic-state injection thresholds.
