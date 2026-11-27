# Split quadratic boundary states: genus-two closure and optimal unambiguous discrimination

Date: 2026-11-27. Companion to tetracode interface certificate ba0f928. No assumption of W33 and no claim of 3+1D gravity.

## General prime theorem
For a prime p, let D=M2(F_p), q(X)=det(X)/p mod 1. This split finite quadratic module is isometric to a hyperbolic double of F_p^2. The nonzero null matrices have rank one: X=u v^T. Maximal totally null vector subspaces have dimension two and are exactly fixed-column-direction and fixed-row-direction planes. Indeed, the sum of two rank-one matrices with independent column AND row directions is rank two. The rulings each have p+1 planes and partition the projective null quadric into a (p+1)^2 grid; cross-ruling intersections have size p, same-ruling intersections size 1. Every plane has p^2 vectors.

The normalized uniform plane states have Gram matrix with diagonal 1, same-ruling off-diagonal 1/p^2 and cross-ruling 1/p. Its eigenvalues are 2(p+1)/p once, (p^2-1)/p^2 with multiplicity 2p and zero once. The unique linear dependence is the difference between the two ruling sums. Rank 2p+1.

For the hyperbolic double of G=F_p^2, partial Fourier transform of the magnetic factor converts the topological genus-one S,T action to simultaneous SL2(F_p) action on two row vectors in F_p^2. There is one zero orbit, p+1 rank-one orbits (projective proportionality labels), and p-1 rank-two orbits (nonzero determinants). Consequently the modular fixed dimension is exactly 2p+1, spanned by the plane states. Each fixed vector has constant values a_i+b_j on the (p+1)^2 nonzero projective null directions, with origin value sum(a_i)+sum(b_j); the same min(a) gauge proof as the ternary case gives the 2(p+1) vacuum-normalized nonnegative integral invariants. This is a specific elementary realization of standard Weil-invariant theory.

## Higher genus: the missing direction returns
Consider the untwisted Abelian quantum double of G=F_p^2. On genus g the Hilbert space is functions on H^1(Sigma_g,G), after the electric/magnetic partial Fourier change of basis. Mapping class action factors through Sp(2g,F_p) acting simultaneously on a pair of row vectors a,b in F_p^(2g). Witt extension classifies the orbits:
- rank zero: one;
- rank one: p+1, labeled by proportionality;
- rank two with nonzero symplectic product: p-1;
- rank two with product zero: one extra orbit iff g>=2.

Thus fixed dimension 2p+1 for g=1, 2p+2 for all g>=2. Orbit sizes are respectively 1, p^(2g)-1 per rank-one orbit, (p^(2g)-1)p^(2g-1) per nonzero pairing, and (p^(2g)-1)(p^(2g-1)-p) for the independent isotropic orbit. These sum to p^(4g).

The plane tensors |L>^tensor g are fixed by the mapping class representation: single-handle Fourier transformations preserve L=L^perp, quadratic shears have phase 1 on tuples in L, and handle basis changes preserve L^g. These elementary symplectic transformations generate the finite action. Their Gram matrix is the entrywise gth power of the genus-one Gram. Its eigenvalues:
- 1+p/p^(2g)+(p+1)/p^g (one);
- 1+p/p^(2g)-(p+1)/p^g = (1-p^(-g))(1-p^(1-g)) (one);
- 1-p^(-2g) (2p).
For g>=2 all are positive, so the plane tensors span the whole fixed space and are independent. The missing genus-one direction is restored precisely when independent isotropic pairs can occur. This theorem is for the untwisted finite gauge theory (or equivalent split metric-group modular data with the invertible framing anomaly handled separately); it is not a general assertion about arbitrary TQFT.

Server Python executed all six prime checks (2,3,5,7,11,13) and five genus checks (2,1),(2,2),(2,3),(3,1),(3,2), using explicit orbit generation and modular Gram ranks. These finite checks are independent of the analytic dimension proof. For p=3 genus two the 6561 states split into orbits 1, four of size 80, one of size 1920 and two of size 2160.

## Operational consequence: exact optimal USD
For uniformly chosen plane states, consider error-free unambiguous state discrimination (USD), allowing a failure output. One copy cannot unambiguously identify even one label: the unique linear relation has every coefficient nonzero, so each vector lies in the span of the others. For g>=2 copies, the Gram G_g is positive definite. A necessary and sufficient USD condition for success probabilities s_i is G_g-diag(s_i) positive semidefinite (use reciprocal vectors on their span). The normalized difference-of-rulings vector has components +/-1/sqrt(2(p+1)), so it upper bounds mean success by the smallest eigenvalue. Equal success probabilities at that eigenvalue attain the bound. Hence
  P_USD(p,g)=(1-p^(-g))(1-p^(1-g))
for all g>=1, zero at g=1. For the ternary tetracode AME states: g=2 gives 16/27, g=3 gives 208/243. The two-copy result is an ideal joint POVM on eight physical qutrits if implemented as AME states; no locality, optical resource, or braiding universality claim is made. The topological genus-g state and the g-copy quantum circuit are separate realizations of the same Gram data.

## Replay
python analysis/toe_20261127_split_boundary_general.py

## References
- https://arxiv.org/abs/1705.04572 (invariant Weil representation calculations)
- https://www.sciencedirect.com/science/article/abs/pii/S0022314X23000756 (isotropic generators)
- https://arxiv.org/abs/1008.0654 (Abelian Chern-Simons boundaries)
- https://arxiv.org/abs/1305.7203 (boundary-changing defects)
- Standard Witt extension lemma and reciprocal-vector USD criterion.
No literature priority claim. This follows the first packet's scope: modular algebra and a conditional topological model, not derivation of physical E8, relativistic spacetime or measured coupling constants.
