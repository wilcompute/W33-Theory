# Passes 3500–3505 — triangle-free SRG atlas, the μ=4 ladder, and the missing-Moore firewall

## Status

The exact verifier reports

```text
PASS_6_FRONTS e308364dd480970803061b90ab27bf86afa2ae4946399b656292f02682c17fd9
```

This packet was developed after a complete read of the live three-manuscript wrappers, their current bodies and theorem manifest, the public site, and the recent Clebsch/Petersen/Perkel/57-cell packets. It is deliberately conservative: exact arithmetic and necessary graph structure are promoted; literature-dependent existence statements are cited; analogies are fenced off.

---

## 3500 — the seven known non-complete-bipartite triangle-free SRGs

The seven standard examples are:

| graph | parameters `(v,k,λ,μ)` | spectrum |
|---|---:|---:|
| `C5` | `(5,2,0,1)` | `2,(-1±√5)/2` with multiplicities `1,2,2` |
| Petersen | `(10,3,0,1)` | `3^1,1^5,(-2)^4` |
| Clebsch | `(16,5,0,2)` | `5^1,1^10,(-3)^5` |
| Hoffman–Singleton | `(50,7,0,1)` | `7^1,2^28,(-3)^21` |
| Gewirtz | `(56,10,0,2)` | `10^1,2^35,(-4)^20` |
| M22 | `(77,16,0,4)` | `16^1,2^55,(-6)^21` |
| Higman–Sims | `(100,22,0,6)` | `22^1,2^77,(-8)^22` |

The verifier checks the SRG feasibility identity

\[
(v-k-1)\mu=k(k-\lambda-1)
\]

and reconstructs every spectrum from the quadratic restricted-eigenvalue equation.

These graphs are not seven disconnected numerological landmarks. At least two exact descendant chains are standard:

- the second subconstituent of the Clebsch graph is the Petersen graph;
- deleting a vertex and its neighborhood from the Higman–Sims graph gives the M22 graph, while the Gewirtz graph occurs as a distinguished induced subgraph in the Higman–Sims/M22 environment.

That makes a **subconstituent/induced-subgraph atlas** a better organizing object than a list.

---

## 3501 — fixed-μ, fixed-positive-eigenvalue ladder

Set

\[
\mu=4,
\qquad r=2,
\]

and let `λ` vary. The other restricted eigenvalue and the SRG parameters are forced:

\[
s=\lambda-6,
\]

\[
k=16-2\lambda,
\]

\[
v=\frac{(\lambda-7)(3\lambda-22)}2.
\]

The multiplicities are likewise forced:

\[
f_r=\frac{(\lambda-5)(3\lambda-22)}2,
\qquad
f_s=-3(\lambda-7).
\]

For `λ=0,1,2,3,4`, this produces the exact five-rung ladder

\[
\boxed{
(77,16,0,4)
\to
(57,14,1,4)
\to
(40,12,2,4)
\to
(26,10,3,4)
\to
(15,8,4,4).
}
\]

The rungs are:

1. M22;
2. the impossible 57-vertex graph of Wilbrink–Brouwer;
3. the W33 parameter class;
4. the ten Paulus graphs;
5. the triangular graph `T(6)`.

The central discovery is therefore a literal **57-vertex spectral hole between M22 and W33**. It is not the missing degree-57 Moore graph. The two objects share only the integer 57:

\[
\operatorname{SRG}(57,14,1,4)
\quad\text{versus}\quad
\operatorname{SRG}(3250,57,0,1).
\]

This distinction is now frozen in the certificate.

---

## 3502 — W33 and Gewirtz share one restricted functional calculus

The W33 collinearity graph has spectrum

\[
12^1,2^{24},(-4)^{15},
\]

whereas the Gewirtz graph has

\[
10^1,2^{35},(-4)^{20}.
\]

Thus, after removing the constant line, both adjacency operators obey

\[
\boxed{(A-2I)(A+4I)=0.}
\]

Equivalently,

\[
A^2+2A-8I=0
\]

on the augmentation module.

Their complements have restricted eigenvalues `-3` and `+3`, hence the centered complement operator satisfies

\[
\boxed{\widetilde A_{\mathrm{comp}}^2=9I}
\]

on augmentation.

This is an exact bridge: the same degree-two polynomial functional calculus acts on both graphs. It is not an objectwise intertwiner. The multiplicities differ, so no canonical module isomorphism follows.

A useful next comparison is therefore not “identify W33 with Gewirtz,” but:

> compare which W33 constructions depend only on the restricted polynomial `x²+2x−8`, and which depend on the multiplicity pair `(24,15)` or on the symplectic incidence geometry.

That is a clean falsifier boundary.

---

## 3503 — corrected edge-rooted chart for the hypothetical degree-57 Moore graph

Assume only for this section that a Moore graph

\[
M_{57}=\operatorname{SRG}(3250,57,0,1)
\]

exists, and fix an edge `a—b`.

Let

\[
A=N(a)\setminus\{b\},
\qquad
B=N(b)\setminus\{a\}.
\]

Then

\[
|A|=|B|=56.
\]

The remaining vertex set has size

\[
3250-2-56-56=3136=56^2.
\]

For every pair `(A_i,B_j)`, the vertices `A_i` and `B_j` are nonadjacent and therefore have a unique common neighbor. This labels the residual vertices by

\[
C\cong A\times B.
\]

Every residual vertex `(i,j)` has:

- one neighbor `A_i`;
- one neighbor `B_j`;
- exactly 55 neighbors inside `C`.

No two adjacent residual vertices may share a row or a column, because that would create a triangle through `A_i` or `B_j`. Since there are 55 other rows and 55 residual neighbors, every vertex has exactly one neighbor in every other row. The same holds for columns.

Therefore the residual graph has **two orthogonal 56-fibre decompositions**, and between every two distinct fibres lies a perfect matching.

Writing the matching from row `i` to row `j` as a permutation `σ_ij∈S56`, necessary constraints include

\[
\sigma_{ji}=\sigma_{ij}^{-1},
\]

\[
\sigma_{ij}\text{ is fixed-point-free},
\]

and, for distinct `i,j,k`,

\[
\sigma_{ki}\sigma_{jk}\sigma_{ij}
\]

must also be fixed-point-free, or else the three rows contain a triangle.

This is the useful content of the proposed constructive picture: not `56!` automorphisms, but a coupled system of 1-factor permutations with short-product derangement constraints.

### Corrections to the proposed automorphism argument

1. The number

   \[
   \frac{3250\cdot57}{2}=92{,}625
   \]

   is the edge count, not the automorphism-group order.
2. Relabelling the 56 rows and induced columns changes coordinates on the construction. It does not automatically give an automorphism of one fixed completed graph.
3. A regular bipartite graph need not be complete bipartite.
4. The safe edge-transitivity argument is different: a connected regular edge-transitive but non-vertex-transitive graph is bipartite, whereas a Moore graph of girth five is not bipartite. Combined with the known non-vertex-transitivity theorem, this excludes edge transitivity.

---

## 3504 — the four-way “57 firewall”

The repository now uses four distinct 57-objects, and they must never be conflated:

| object | size/degree | status |
|---|---:|---|
| missing Moore graph `M57` | 3250 vertices, degree 57 | existence open |
| `μ=4,r=2,λ=1` ladder hole | 57 vertices, degree 14 | proved nonexistent |
| Perkel graph | 57 vertices, degree 6 | exists |
| regular 57-cell | 57 cells; `PSL(2,19)` symmetry of order 3420 | exists |

The current repo already proved that the Perkel/57-cell object is not an inherited transitive quotient of the W33 cover or affine instruction groups and retained only a common rational 20-plane comparison.

A June 2026 preprint adds a sharper conditional firewall for the missing Moore graph: it claims that any such graph has no involutory automorphisms. If correct, its automorphism group has odd order. Since

\[
|PSL(2,19)|=3420
\]

is even, the 57-cell/Perkel symmetry cannot embed into the automorphism group of `M57`.

This is not a nonexistence proof for `M57`, and the no-involution result remains a recent preprint. It does, however, rule out the most tempting global symmetry identification if the preprint survives review.

---

## 3505 — public and manuscript integration

The exact theorem insert is routed through the shared current-frontier manifest, so all three canonical manuscripts receive the same evidence-bounded statement:

- `w33_paper.tex`;
- `photonic_holonet.tex`;
- `holonet_machine_blueprint.tex`.

The public site receives a compact summary and a dedicated graph-atlas page. The page emphasizes the two most important distinctions:

\[
57\text{ vertices}\neq57\text{-regular},
\]

and

\[
\text{coordinate relabelling}\neq\text{fixed-graph automorphism}.
\]

---

## Reproduction

```bash
python analysis/bt3500_3505_triangle_free_srg_m57_bridge.py
pytest -q tests/test_bt3500_bt3505_triangle_free_srg_m57_bridge.py
```

Expected output:

```text
PASS_6_FRONTS e308364dd480970803061b90ab27bf86afa2ae4946399b656292f02682c17fd9
```

---

## Evidence boundary

Promoted exactly:

- the seven parameter/spectrum checks;
- the five-rung `μ=4,r=2` formulas;
- the W33/Gewirtz restricted polynomial;
- the edge-rooted `56×56` double-fibration constraints;
- the arithmetic separation of the four 57-objects;
- the correction of the three invalid automorphism inferences.

Not promoted:

- existence or nonexistence of the degree-57 Moore graph;
- a canonical W33–Gewirtz intertwiner;
- a Perkel/57-cell/M57 identification;
- peer-reviewed status for the June 2026 no-involution preprint;
- sufficiency of the displayed permutation constraints.

## Literature used

- H. A. Wilbrink and A. E. Brouwer, “A (57,14,1) strongly regular graph does not exist,” *Indagationes Mathematicae* 86 (1983), 117–121, DOI `10.1016/1385-7258(83)90047-1`.
- V. Faber and J. Keegan, “Existence of a Moore graph of degree 57 is still open,” arXiv:`2210.09577`.
- Y. Ishida, “No involutions in the missing Moore graph,” arXiv:`2606.29183` (preprint, June 2026).
- D. H. Smith and R. Montemanni, “The Moore Graph of Diameter 2 and Degree 57 via Cyclic Derangements,” *Axioms* 15 (2026), 332.
- DistanceRegular.org entries for the Clebsch and Petersen second-subconstituent relation.
- A. E. Brouwer’s/standard graph references for the Higman–Sims, M22, and Gewirtz induced-subgraph constructions.
