# Related work (E8 → E6 × SU(3), E6 27, spreads/double-sixes)

This repo’s computations lean on standard, well-established structural facts about exceptional Lie algebras and classical line configurations, plus a few less-common finite-geometry correspondences.

> Boundary note: this page collects structural background and related literature. It should not be read as a proof that the repo’s exact qutrit kernel already functorially yields the full global `E8`/physics closure. The strongest exact bridge currently audited in-repo is local and `E6`-side.

## E8 → E6 × SU(3) branching

- Standard maximal subalgebra statement: `E8 ⊃ E6 × SU(3)` with adjoint branching
  \[
    248 = (78,1) \oplus (1,8) \oplus (27,3) \oplus (\overline{27},\overline{3}).
  \]
- Explicit constructions of the same decomposition via division algebras:
  - Dray–Manogue–Wilson (JMP 2024): https://pubs.aip.org/aip/jmp/article-abstract/65/3/031702/3278070/

- Embedding surveys / discussion of SM-in-E8 approaches:
  - R.A. Wilson, “Embeddings of the Standard Model in E8” (arXiv:2507.16517): https://arxiv.org/abs/2507.16517

## E6 and the 27 representation

- Standard GUT decomposition:
  \[
    27 \to 16 \oplus 10 \oplus 1 \quad \text{under } SO(10)\times U(1),
  \]
  and further `SU(5)`-based decompositions are the usual E6-GUT dictionary.
  - Example lecture notes (CERN): https://indico.cern.ch/event/353377/contributions/832064/attachments/693593/952152/hurmuz_e6.pdf

## Finite-qutrit / symplectic geometry

- Two-qutrit Pauli commutation geometry and its finite-geometric shell:
  - Planat–Saniga, “On the Pauli graphs of N-qudits” (2007): https://arxiv.org/abs/quant-ph/0701211
- Computational geometry software documenting the classical symplectic quadrangle as `W(3,q)` with collineation group `PGammaSp(4,q)` and isometry group `PSp(4,q)`:
  - FinInG manual: https://docs.gap-system.org/pkg/fining/doc/manual.pdf

For `q = 3`, the projective symplectic subgroup therefore has order `25920` by the standard symplectic group formula, and adjoining the graph/duality extension gives the order-`51840` full collinearity-graph symmetry package used throughout the repo.

## 27 lines, Schläfli graph, and 45 tritangent planes

- The 27 lines on a smooth cubic surface form a classical configuration.  Two lines are either skew or meet.
- The Schläfli graph is the graph on the 27 lines where adjacency can be taken as “skew”; the complement graph is then the “intersection graph”.  Triangles in the intersection graph correspond to tritangent planes (a plane section splitting as three lines).
- Manivel, “Configurations of lines and models of Lie algebras” (2005): https://arxiv.org/abs/math/0507118
- Green, “Full heaps and representations of affine Weyl groups” (2006): https://arxiv.org/abs/math/0608123
- A concise notes-style reference that enumerates the 45 tritangent trios and states W(E6) transitivity:
  - https://dept.math.lsa.umich.edu/~idolga/CAG-2.pdf
- A modern reference explicitly notes: tritangent planes correspond to the 45 triangles in the Schläfli intersection graph.
  - Sturmfels et al., “The Schläfli Fan”, DCG (2021): https://link.springer.com/article/10.1007/s00454-020-00215-x

## Unification normalization: sin²θ_W = 3/8 (baseline consistency check)

If the symmetry breaking passes through an SU(5)-type normalization of hypercharge, the tree-level GUT-scale relation
\[
  \sin^2\theta_W = 3/8
\]
is the standard result of hypercharge normalization inside SU(5) (and carried through many GUT embeddings, including E6).

Two accessible references:
- Harvey Mudd / Caltech notes: https://www.math.umd.edu/~immortal/Spring2015/extra_material/su5unification.pdf
- York University lecture notes: https://www.physics.yorku.ca/~lildave/phys4235/gut03.pdf
