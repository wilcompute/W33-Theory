# Passes 5720–5724 — affine face-complex 3-torsion and the exact GL(2,3) torsion action

**Status:** EXECUTED 2026-08-17. Exact integer linear algebra and exhaustive finite-group verification. This packet refines the Pass5691 affine `su(3)` gauge-complex census; it does **not** infer a physical coupling, confinement, a continuum limit, or a new charge quantum.

## 5720 — the mod-3 rank defect is exactly integral 3-torsion

Let `X_P` be the nine-vertex `AG(2,3)` complex with complete 1-skeleton `K9` and the 54 translation-parallelogram 2-cells from Pass5691. Let `X` add the 12 affine-line triangular 2-cells.

Choose the star spanning tree at vertex `0`. The 28 non-tree edges give an integral fundamental-cycle basis, hence an isomorphism

\[
Z_1(K_9;\mathbb Z)\cong\mathbb Z^{28}.
\]

In that basis the plaquette boundary lattice has Smith form

\[
\operatorname{SNF}(\partial_2^P)=1^{24},
\]

while the full 66-face boundary lattice has

\[
\boxed{\operatorname{SNF}(\partial_2)=1^{26}\oplus3^2.}
\]

Therefore

\[
\boxed{H_0(X;\mathbb Z)=\mathbb Z,\qquad H_1(X;\mathbb Z)\cong(\mathbb Z/3)^2,\qquad H_2(X;\mathbb Z)\cong\mathbb Z^{38}.}
\]

The plaquette-only complex is torsion-free:

\[
\boxed{H_1(X_P;\mathbb Z)\cong\mathbb Z^4,\qquad H_2(X_P;\mathbb Z)\cong\mathbb Z^{30}.}
\]

So Pass5691's `rank_R=28` but `rank_F3=26` discrepancy is not a floating-point accident and not a hidden real harmonic sector. It is the reduction of two genuine integral order-three classes.

## 5721 — the 12 affine lines kill four real modes with index nine

Because the plaquette lattice is primitive in the integral cycle lattice, quotienting by it gives exactly `H1(X_P;Z)=Z^4`. The line triangles induce a rank-four map into this quotient whose nonzero Smith invariants are

\[
\boxed{1,1,3,3.}
\]

Equivalently, the line-triangle image has index

\[
\boxed{9=3^2}
\]

inside the four-dimensional plaquette homology lattice. This is the mechanism behind the field dependence:

\[
\mathbb Z^4\xrightarrow{\text{12 line faces}}\mathbb Z^4
\quad\leadsto\quad
\operatorname{coker}\cong(\mathbb Z/3)^2.
\]

Thus the E6-selected affine-line faces do more than kill the four real plaquette modes: two independent attachment directions close only after multiplication by three.

## 5722 — universal-coefficient/Bockstein reading

The integral result immediately gives

\[
H^1(X;\mathbb Z)=0,
\qquad
\boxed{H^2(X;\mathbb Z)\cong\mathbb Z^{38}\oplus(\mathbb Z/3)^2.}
\]

Over fields,

\[
\dim H_1(X;\mathbb F_3)=2,
\qquad
\dim H_1(X;\mathbb F_p)=0\quad(p\ne3),
\]

and

\[
\dim H_2(X;\mathbb F_3)=40,
\qquad
\dim H_2(X;\mathbb F_p)=38\quad(p\ne3).
\]

The producer explicitly rechecks `p=2,3,5,7,11,13`; the Smith form proves the all-prime statement. The two `F3` one-cohomology modes are therefore torsion/Bockstein modes. They have no `R`-valued harmonic lift.

This is exactly the kind of distinction that matters in a finite gauge model. Homology-sensitive lattice gauge theories on simplicial complexes and discrete graph Yang–Mills formalisms are established ideas; the project-specific result here is the exact integral homology of this particular 9-site/66-face complex.

Primary prior-art anchors used for scope, not novelty claims:

- Shuhan Jiang, *Gauge theory on graphs*, arXiv:2211.17195 — graph connection 1-forms, curvature 2-forms and a discrete Yang–Mills functional.
- Mark Rakowski and Siddhartha Sen, *Homology in Abelian Lattice Models*, arXiv:hep-th/9512212 — homology modes in lattice gauge theory on arbitrary simplicial complexes.
- David H. Adams, *R-torsion and linking numbers from simplicial abelian gauge theories*, arXiv:hep-th/9612009 — simplicial gauge theory and torsion homology/linking pairings.

No priority claim is made for “torsion in lattice gauge theory”; the theorem is the exact Smith/homology calculation and symmetry action for the repository's affine complex.

## 5723 — the torsion doublet carries the full GL(2,3) linear quotient

The full affine group

\[
\operatorname{AGL}(2,3)=\mathbb F_3^2\rtimes GL(2,3),
\qquad |\operatorname{AGL}(2,3)|=9\cdot48=432,
\]

preserves both the 54 plaquette cells and the 12 line cells, up to orientation.

Exhausting all 432 affine transformations gives the induced action on

\[
H_1(X;\mathbb F_3)\cong\mathbb F_3^2.
\]

The kernel is exactly the translation subgroup:

\[
\boxed{\ker=\mathbb F_3^2,\qquad |\ker|=9,}
\]

and the image has order 48:

\[
\boxed{\operatorname{im}\cong GL(2,3).}
\]

In the deterministic quotient basis represented by chord edges `(6,8)` and `(7,8)`, with

\[
P=\begin{pmatrix}0&1\\1&1\end{pmatrix},
\]

the affine transformation `(M,b)` acts by

\[
\boxed{Q(M,b)=P^{-1}\bigl(\det(M)M^T\bigr)P\pmod3,}
\]

independent of the translation `b`. The `det` twist is essential: the torsion pair is not merely an untyped two-count; it is an explicit 2-dimensional `GL(2,3)` module.

## 5724 — separation firewall and what this does *not* mean

The repository already contains another integral order-three defect, Pass5121. They are **not the same object**:

- Pass5121: an `81 x 108` incidence carrier, with a **one-dimensional** `Z/3` saturation quotient and a `U81 ⋊ V4` module analysis.
- Pass5720–5724: the `9`-vertex, `36`-edge affine face chain complex, with **two-dimensional** `(Z/3)^2` first homology and an `AGL(2,3) -> GL(2,3)` action.

No chain map between those carriers is exhibited here, so no identification is claimed.

Likewise, the torsion theorem does **not** determine the Yang–Mills coupling `g`; Pass5691's old vertical `Z3` connection remains adjoint-trivial; and no continuum QCD, confinement, matter representation, mass gap, spacetime, or experimentally observed discrete gauge symmetry follows from this calculation.

### Outside-box probe: why q=3 may be exceptional here

A non-promoted q=5 experiment generalized the face construction using **all unoriented displacement classes** (needed because for q>3 projective directions no longer exhaust those classes). The resulting q=5 complex has cycle rank 276, full face rank 270 in characteristic zero but 266 mod 5. Thus it retains six free modes and gains four additional mod-5 modes. This is only a field-rank fingerprint, not an integral theorem, but it strongly argues against naively extrapolating the compact q=3 result. The next useful computation is the q=5 integral Smith form followed by q=7.

## Reproduction

Run:

```bash
python analysis/w33_pass5720_5724_affine_torsion_homology.py
```

The producer asserts the chain condition, the integral cycle basis, both Smith forms, the characteristic table, preservation of all 66 faces by all 432 affine transformations, the exact kernel/image orders, and the determinant-twisted action formula. It writes the frozen certificate:

`data/PART_W33_PASS5720_5724_AFFINE_TORSION_HOMOLOGY.json`.
