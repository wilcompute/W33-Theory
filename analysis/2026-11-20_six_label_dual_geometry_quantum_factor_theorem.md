# Exact six-label W33-versus-dual separation and the 45 two-qutrit tensor frames

**Date: 2026-11-20. Scientific scope: finite classical polar geometry and established quantum Weyl algebra. No Lorentzian dynamics, particle masses, quantum-gravity theory, experimental claim, or parameter-free prediction is established here.**

## Repository cross-check and novelty boundary

Existing work already contains the full E8 sl9+84+84 bracket and Jacobi construction (analysis/w33_pass11681_e8_from_two_qutrits.py), the 81-dimensional Steinberg building homology, all 45 symplectic two-qutrit tensor decompositions (analysis/w33_pass11180_mereology.py), and the non-self-duality of the W33 point and line polar geometries (analysis/w33_levi_duality_defect.py). This work does not claim to rediscover any of these.

The separate question tested here is: **What is the smallest unlabeled induced graph configuration that can distinguish the two cospectral, equally parameterized point-line-dual 40-vertex geometries, and what is its quantum-algebraic interpretation?**

## The exact six-label threshold

Let V=F3^4 with its nondegenerate alternating form. Its 40 one-dimensional subspaces are points of W(3,3); adjacent point labels pair to zero. Its 40 isotropic two-dimensional subspaces are the lines. For the 40x40 point-line incidence matrix M, let

    A_point = M M^T - 4 I_40,
    A_dual  = M^T M - 4 I_40.

The first is the W(3,3) point graph; the second is the point graph of the dual quadrangle Q(4,3). Both have strongly regular parameters (40,12,2,4) and exact adjacency spectrum 12^(1), 2^(24), (-4)^(15). Their full Laplacian spectral heat traces agree for every real t:

    Tr exp[-t(12I-A)] = 1 + 24 exp(-10t) + 15 exp(-16t).

Every trace-only spectral action on A also agrees. This is a rigorous *nonuniqueness* problem for a theory which attempts to reconstruct the intended local quantum geometry using only adjacency eigenvalues.

A complete independent enumeration of every induced unlabeled graph on two, three, four and five vertices gives identical histograms for both graphs. The 5-vertex census is not merely an edge-count test: all 5!=120 vertex permutations are applied to obtain a canonical mask for each of the binomial(40,5)=658,008 subsets in **each graph**. Exactly 23 unlabeled graph classes occur and every class count matches.

A difference first appears at SIX vertices: the induced complete bipartite graph K(3,3) appears **720** times on the W point graph and **zero** times on the Q dual graph. This is a *six-label pattern of 15 pairwise adjacency/commutation facts*, not a six-particle process, six-body Hamiltonian, or sixth-order scattering amplitude.

## Why there are 720: symplectic tensor factors

For any q, the number of nondegenerate alternating 2-spaces in a 4D symplectic vector space is q^2(q^2+1). Their symplectic orthogonal complements pair them into q^2(q^2+1)/2 unordered decompositions V=P+P_perp.

For q=3, this gives 90 nondegenerate planes and **45 unordered orthogonal plane decompositions**. Each plane has four projective rays; all distinct rays within a plane are pairwise *nonorthogonal* (thus noncommuting as Weyl labels), while all points on opposite planes commute. Choosing three rays from each of the four-ray sides gives

    45 * binomial(4,3)^2 = 45 * 16 = 720

induced K(3,3) copies. The six vertices uniquely recover the two planes they span, so there is no further overcounting.

Every such decomposition is a Clifford-compatible two-qutrit tensor-factorization chart: each 2D plane supplies the nine Weyl degrees of an M3(C) matrix algebra; the two factor algebras commute; their products span all 81 complex degrees of End(C9). The producer checks all 45 splits, all pairwise cross-sector Weyl commutators, and full Hilbert-Schmidt orthogonality of the 81 Weyl matrices.

The existing repository has already connected the 45 factorization charts to the 45 classical E6 tritangent planes, but this particular test does not itself construct a new equivariant E6 map. The new finding is their role in the minimal *six-label* dual-geometry discriminator.

## Why the dual has no K(3,3) for odd q

In the dual point graph, three pairwise nonadjacent vertices correspond to three mutually skew totally isotropic 2-spaces L0,L1,L2 in Fq^4. Select L0=U and L1=U* in dual pairing. L2 is the graph of an invertible symmetric linear map T:U to U*. A totally isotropic transversal line M meeting L0 and L1 is spanned by (u,0) and (0,w) with w(u)=0. To meet L2, w must be proportional to Tu, so u has to satisfy

    Q(u) = u^T T u = 0  in projective PG(1,q).

When q is odd, the invertible symmetric T defines a nondegenerate binary quadratic form. It has either ZERO or TWO projective zeros, never three. Hence an independent triple in the dual line graph has at most two common neighbors; an induced K(3,3) would require three. Therefore there are no induced K(3,3) in this graph for any odd prime power q.

The corresponding point-graph formula for all odd prime powers is

    N_K33(W(3,q)) = q^2(q^2+1)/2 * binomial(q+1,3)^2,
    N_K33(Q(4,q)) = 0.

The numerical code directly checks the *prime* fields q=2,3,5, including the even-characteristic case where the classical polar GQ is self-dual.

| Field order q | W point K(3,3) | Q dual K(3,3) |
| ---: | ---: | ---: |
| 2 | 10 | 10 |
| 3 | 720 | 0 |
| 5 | 130,000 | 0 |

## Why lower-order counts agree

Let c(T) be the number of common neighbors of any independent triple T. Exhaustive independent-triple census for q=3:

| c(T) | W point: #triples | Q dual: #triples |
| ---: | ---: | ---: |
| 0 | 0 | 1,080 |
| 1 | 2,880 | 0 |
| 2 | 0 | 2,160 |
| 4 | 360 | 0 |

Both graphs contain 3,240 independent triples. The first two binomial moments sum_T c(T) and sum_T binomial(c(T),2) equal 4,320 and 2,160 for both. The **third** moment sum_T binomial(c(T),3) differs: 1,440 on W and 0 on Q. Each induced K(3,3) is counted once from each of its two three-point sides, giving precisely 720 versus zero.

This provides a compact low-order correlation explanation for the equality of all smaller unlabeled motif distributions, while the producer independently verifies all 23 five-vertex graph classes.

## Corrected repository error

The older analysis/w33_pauli_cartans.py and its frozen data/w33_pauli_cartans.json previously labeled the 40 line-Cartan intersection graph as "isomorphic to W(3,3) point/line graph by self-duality". That is false for q=3. Its actual graph is the dual Q(4,3) point graph. The code and data certificate are corrected in this pass. Same SRG parameters or adjacency spectrum do not imply isomorphism.

## Implications and blockers for a TOE

A finite spectral action consisting solely of functions of the adjacency eigenvalues cannot distinguish these two geometries, even though only one encodes the concrete 45 two-qutrit tensor decompositions by these six-label K(3,3) subgraphs. Any candidate emergence mechanism must preserve richer incidence/tensor-factorization information, or provide another independent physical selection mechanism.

This is an exact mathematical constraint, NOT a derivation of 3+1 Lorentzian spacetime, Einstein dynamics, a unique gauge coupling, three fermion generations, or physical chirality. Nor does a six-vertex configuration require six physically separate photons. It is accessible as a collection of ordinary pairwise qutrit Pauli commutation relations.

## Reproduction

    python analysis/w33_20261120_six_label_dual_quantum_geometry.py
    python -m unittest discover -s tests -p test_w33_20261120_six_label_dual_quantum_geometry.py -v

The source script computes the q=2,3,5 field controls and writes a frozen detailed JSON to data/w33_six_motif_duality_quantum_frames.json (some repo checkouts ignore generated data files by default).

## External context

- Classical polar GQ and the W/Q point-line duality: https://link.springer.com/article/10.1007/s10623-024-01385-y
- Triad-center distinction in finite generalized quadrangles: https://www.researchgate.net/publication/317736451_On_the_metric_dimension_of_affine_planes_biaffine_planes_and_generalized_quadrangles
- Finite classical geometry primer: https://cage.ugent.be/geometry/Theses/61/PhDDeBoeck.pdf

### Five independent next research fronts

1. Identify a physically justified *relational* action sensitive to six-label tensor factorization data that still respects appropriate gauge invariances.
2. Derive the 45-frame to E6-tritangent identification without choosing an arbitrary anchor, or prove its equivariance/obstruction under the entire Weyl group.
3. Extend the minimal graph motif threshold to q=7 and to other classical polar spaces (including the G2 hexagon and triality-related D4 geometries).
4. Build a sequence of causal geometries/refinements preserving the symplectic factorization selector, and prove or falsify a Lorentzian field-theory continuum limit.
5. Derive one coupling or mass ratio from an independent consistent local action, not from post-hoc finite-graph numerology.
