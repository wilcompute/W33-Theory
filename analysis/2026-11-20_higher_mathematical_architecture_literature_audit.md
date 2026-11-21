# Research pivot: W33, exceptional geometry, higher coherence and 4D dynamical candidates (2026-11-20)

**Status:** literature synthesis and independently verified finite calculations, **not** a physical TOE, experimentally validated field theory, new derivation of three generations, or a parameter-free coupling. **Baseline**: master `beb04757b873d39e224b9fdba912f6f57e5b413e`. The full calculations, JSON and ten passing unittests are attached to the associated ChatGPT research packet.

## What the literature now makes possible

1. **Exceptional bridge with geometric content.** `PSp(4,3) ~= PSU(4,2) ~= W(E6)^+` relates W33 and the classical cubic-surface/27-line representation through the same simple group, not through a coincidence of cardinalities. Sergey Grigorian, *Exceptional cubics on 7-manifolds*, arXiv:2611.21589 (Nov. 16, 2026), constructs critical cubic forms on `S²_0 T*M` (rank 27) whose stabilizer has type E6 precisely for `lambda=(1 ± i sqrt(7))/8`. Importantly the Levi-Civita connection preserves these exceptional cubics if the G2 structure is torsion-free. An actual intertwinable connection from finite W33 data to this bundle, with an anomaly-free fermionic sector, remains to be built.
2. **Minuscule/tropical geometry.** Daniel Corey, *The E6-Grassmannian, its minuscule Coxeter matroids, and the lines on a cubic surface*, arXiv:2611.19606 (Nov. 14, 2026), classifies 230 Weyl matroid orbits and 60 toric-degeneration classes. These might organize symmetry-breaking/degeneration strata; there is no automatic scattering or cosmological meaning.
3. **Genuine four-dimensional categorical framework.** Hank Chen, Zhian Jia, Ran Luo and Wei Cui, *Categorical spin-networks: state-sum invariants of 4-manifolds from higher-gauge theory*, arXiv:2609.31365 (Sep. 25, 2026), use pivotal fusion 2-categories, 20j-symbol amplitudes and 4D Pachner invariance. Explore W33 chamber decoration and Postnikov classes `kappa in H³(G,A)` for an appropriate 2-group. These construct topological invariants, **not propagating 4D general relativity** without further constraints and continuum dynamics.
4. **Causal/spectral spacetime.** Finster–Fischer (2026), *The Continuum Limit Analysis of Causal Fermion Systems for Curved Spacetimes*, arXiv:2605.30199, investigates causal dynamics on already-given curved globally hyperbolic Lorentzian spin backgrounds. Test whether a sequence of W33-refined operators has a stable physical Lorentzian continuum; the paper does not establish such a derivation.
5. **BV–BRST / factorization and positive scattering geometry.** Local field theory requires a consistent master equation, renormalization and anomaly checks. Positive/tropical geometries can organize poles and factorization *once* a physical scattering theory is specified. Finite incidence is insufficient to select couplings.

## Exact finite W33 and cohomology audits

Reconstructing the generalized quadrangle W(3,3) gives 40 projective points, 40 isotropic lines, point graph SRG(40,12,2,4), eigenvalues `12^1,2^24,(-4)^15`; point-line incidence integral Smith form `1^25,0^15`. The rank-three permutation action of PSp(4,3) implies every fully invariant one-body point kernel is `aI+bA+cJ`. It has at most three eigenvalues with fixed multiplicities 1,24,15: rich matter dynamics require additional fields/fibers, interactions, refinement or broken symmetry. This is classical association-scheme mathematics applied as an explicit physics gate.

For the additive two-qutrit Pauli-address group `V=(Z3)^4`,
`H³(V,U1)=(Z3)^14`: 4,782,969 ordinary three-cohomology classes (4 type I, 6 type II, 4 type III). **Nothing about the two-cocycle symplectic commutator selects a unique three-cocycle.**

Under the complete linear symplectic group Sp(4,3), all 40 projective transvection tests show no fixed vectors in either the 10-dimensional `Sym²(V*)` or the 4-dimensional `Lambda³(V*)` low-degree integral-cohomology pieces. Consequently the **only fully Sp(4,3)-fixed ordinary H³ class is trivial** (this is not a no-go for higher-group extensions, nontrivial coefficients, projective covariance or smaller symmetries).

A constructive *orientation ladder* gives:
`Sp(4,3)` (order 51840): invariant dimension 0, 1 class;
projective-point stabilizer (order 1296): dimension 1, 3 classes;
nonzero **oriented vector** stabilizer (order 648): dimension 2, 9 classes.
The ray admits a quadratic invariant `s(u,x)^2`; choosing the lift additionally permits the odd-under-`u->-u` 3-form `i_u vol_4`. This precisely locates a possible *mathematical* symmetry-breaking channel for higher coherence; it does not predict physical handedness.

## Caution: an apparently relevant published three-family proposal needs corrections

Andrei T. Patrascu, *Coherence obstructions and family triplication*, EPJ C 86 703 (2026), DOI:10.1140/epjc/s10052-026-15900-z, has several **as-displayed** inconsistencies in the published HTML (independently checked on Z3):

- The paper gives a normalized 3-cocycle and then claims `omega(1,0,1)=exp(2 pi i/3)`; every normalized 3-cocycle requires `omega(a,0,c)=1` and its own printed formula gives 1.
- Appendix D.1's displayed n=3,m=1 formula is an *exact coboundary*: the normalized 2-cochain `nu(2,2)=exp(2 pi i*8/9)`, all other `nu(a,b)=1`, reproduces the appendix formula on all 27 triples under a standard coboundary convention. It therefore cannot be the generator as printed; the familiar main-text floor-function cocycle *is* a generator.
- A strong ordinary Hilbert-space monoidal fiber functor on a full pointed subcategory `Vec_G^omega` requires `[omega]=0`, because the tensorator on invertible 1D objects explicitly trivializes omega. A claimed strong monoidal functor coexisting with a nonzero obstruction requires revised categorical assumptions.
- The whole Deligne product category `(Vec_G^omega)^{Deligne N}` has |G|^N simple objects and cannot equal `Vec_G^{omega^N}` which has |G|; a carefully specified diagonal subcategory may be intended instead.

This is a mathematical source audit, **not** a rejection of categorical flavor mechanisms in general. Any public critique should verify the author's typeset original/corrections.

## Selection rule for progress

The proposed architecture must provide *separately*:
`W33 incidence -> equivariant fibers and coherent higher-gauge rules -> a local physical action -> a Lorentzian continuum and propagating degrees of freedom -> anomaly-free chiral matter -> a dimensionful, unfitted prediction.`

Ranked independent next experiments:
1. Construct a W33-to-E6 rank-27 **connection** preserving the Grigorian cubic, measure holonomy obstruction and compare against existing 40-to-27 intertwiners.
2. Formulate an oriented symplectic-stabilizer 2-group with `kappa in H³(G,A)`; test coherence, anomaly, and parity reversal, avoiding scalar H³(V,U1) shortcuts.
3. Import Chen et al. fusion-2-category 20j data into a W33 4D chamber state sum, test Pachner moves and pinpoint where propagating degrees of freedom fail.
4. Define W33-dependent causal/spectral operators along a **refinement sequence**, demand stable dimension/Lorentzian dispersion and a dynamical metric, not finite graph incidence renamed gravity.
5. Build an explicit BV–BRST local action with E6 chiral field content and anomaly checks, then ask for a preregistered scattering or coupling prediction.

**Primary URLs:** https://arxiv.org/abs/2611.21589 ; https://arxiv.org/abs/2611.19606 ; https://arxiv.org/abs/2609.31365 ; https://arxiv.org/abs/2605.30199 ; https://link.springer.com/article/10.1140/epjc/s10052-026-15900-z ; https://math.mit.edu/~etingof/tenscat1.pdf
