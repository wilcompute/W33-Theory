# A2^4 tetracode interfaces: eight E8 gluings, AME states and the seven-dimensional modular fixed space

Date: 2026-11-27. Baseline: 5229e15ac5473490921f8bb3bf0dc1ed6df5d4cd. Exact finite mathematical and conditional 2+1D effective-theory results, not a TOE or hardware demonstration.

## Audit boundary
The master API returned 279 commits between 2026-11-20 15:22 UTC and 2026-11-27 15:22 UTC, 44 with reservation in the message. The complete metadata inventory is archived separately. Eleven commit diff payloads were retrieved (including 12733 and major optical/exceptional/causal fronts); this is not a line-by-line reading of all 279 diffs. The earlier weekly reconciliation 686c6b4ac and current TOE_DECISION_TABLE were consulted, but cannot certify the entire new window. The workstation was offline. Direct cloud git network access was unavailable. Current candidates A, B-prime and Hybrid remain conditional; their latest repository evidence estimates do not exceed the SM. No new RGE or experimental-data fit is claimed. Prior overlapping repo anchor: analysis/PASS11687_11691_TWO_QUTRIT_E8_DICTIONARY.md (centralizer A2^4), and earlier ternary tetracode lattice gluing. Code search did not find the combined boundary/modular/AME certificate; this does not establish priority.

## Finite quadratic module and exact classification
Let A=Z^8 with Gram diag(C_A2,C_A2,C_A2,C_A2), where C_A2=[[2,-1],[-1,2]]. Its discriminant module D=A*/A is F3^4, with quadratic form q(x)=sum x_i^2/3 modulo 1 and bilinear form 2 dot(x,y)/3. There are 33 isotropic vectors including zero. Every nonzero isotropic vector has weight 3. Enumeration gives exactly eight maximal totally isotropic planes L of size 9, all [4,2,3] ternary self-dual codes. They split into two rulings of four: within a ruling distinct planes meet in {0}; across rulings they meet in a line of size 3. The 16 projective null points form the 4x4 grid of Q+(3,3). This is orthogonal geometry, not the symplectic W33 Pauli geometry.

For each L, the overlattice A_L=A+L inside A* has index 9, even integral Gram and determinant 1, hence isometric to E8 by the unique rank-eight positive even unimodular lattice theorem. The executable certificate constructs every inclusion M using integer Hermite normal form. The known 240-root census is 24 roots of A2^4 plus 8*27 from glue cosets.

## Quantum states and modular fixed space
Define |L>=1/3 sum_{x in L}|x> in (C^3)^tensor4. Every projection of L onto two coordinates is a bijection, since any kernel would have weight at most 2. All eight states are AME(4,3); each two-party marginal is I/9. This is the classical MDS-to-AME construction, not new existence of AME.

Their Gram matrix is (1/9)[[8I+J,3J],[3J,8I+J]], with 4x4 blocks. Exact spectrum: 8/3 once, 8/9 six times, 0 once. The sums of the two rulings coincide. After subtracting the common mean the centered vectors are two mutually orthogonal regular tetrahedra, each of rank 3.

Use topological T=diag(exp(2pi i q(x))) without the CFT central-charge phase, and S the normalized Fourier matrix of the bilinear form. Every L indicator is fixed by S and T because L=L^perp. Conversely, a fixed vector is supported on the 33 isotropic vectors and is even by S^2. Thus only 17 coordinates survive; the exact rational S-I system has rank 10. Fixed-space dimension is 7. The eight indicators span the complete invariant space.

Stronger cone result: each of the 16 null rays is in exactly one plane from each ruling, so a fixed vector has ray values a_i+b_j and origin value sum(a_i)+sum(b_j). For a nonnegative integral invariant with origin coefficient 1, choose the gauge a_i->a_i-t, b_j->b_j+t to set min(a)=0; differences are integer and all a,b become nonnegative integers. Their sum is 1, so exactly one of the eight coefficients is 1. Therefore the eight indicators are exactly the nonnegative integral, vacuum-normalized invariant vectors (not a classification of all modular tensor categories).

## Actual interface versus chiral vacuum obstruction
The positive A2^4 K-matrix has signature 8; E8 has signature 8 and trivial discriminant. Condensation of L leaves L^perp/L trivial but does NOT eliminate the physical chiral central charge. A fully gapped boundary to vacuum is excluded. Instead fold an oppositely oriented E8: K_fold=A direct_sum (-Gram(A_L)). It has signature zero. For each L, M satisfies M^T Gram(A_L) M=A. The 16x8 integer graph W=(I;M) is primitive (identity top block), rank eight, W^T K_fold W=0. These are explicit maximal null-vector lattices, subject to the usual edge-interaction assumptions; no microscopic spectral gap is demonstrated. A_L/E8 bases vary by L; they are abstractly isometric, and a fixed common E8 basis can be constructed later.

For a standard Abelian gapped-boundary realization, annulus vacuum degeneracy is |L intersection L'|; the elementary boundary-changing defect quantum dimension is sqrt(9/|L intersection L'|). Consequently same boundary d=1, distinct same ruling d=3, opposite ruling d=sqrt(3). This is a prediction of the specified effective topological model, not a simulation or proof of braiding universality. The category is equivalent as a metric group to two Z3 toric codes (split hyperbolic quadratic form); the physical E8 invertible layer is separate.

Hostile controls: treating all eight boundary states as independent fails (rank 7); treating all four-qutrit superpositions as AME fails (e.g. the difference of two same-ruling states has zero |0000> amplitude and is supported on only 16 words; its two-coordinate reduction cannot be I/9 since the outcome 00 is absent); claiming a gapped chiral vacuum boundary fails by signature. No connection to 3+1D gauge couplings or Einstein dynamics is established.

## Replay
python analysis/toe_20261127_tetracode_boundary.py > tetracode_full_certificate.json
Requires Python 3 and SymPy. Full output includes all eight Gram matrices, inclusion matrices, plane coordinates and pairwise intersection data.

## Literature and scope
- Conway and Sloane, Sphere Packings, Lattices and Groups, complex construction A (classical E8 tetracode).
- https://arxiv.org/abs/1701.03359 (MDS and AME).
- https://arxiv.org/abs/1705.04572 (Weil invariants).
- https://www.sciencedirect.com/science/article/abs/pii/S0022314X23000756 (self-dual isotropic generators for Weil invariants).
- https://arxiv.org/abs/1008.0654 (Abelian Chern-Simons boundaries).
- https://arxiv.org/abs/1305.7203 (boundary defects).
- https://arxiv.org/abs/1306.4254 (boundary-dependent degeneracy).
The combination and exact certificate are a repository continuation; no claim of global literature novelty.
