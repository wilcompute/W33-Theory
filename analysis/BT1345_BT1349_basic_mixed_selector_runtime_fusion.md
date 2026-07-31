# BT1345–BT1349: Modular basic algebras, mixed triality coupling, selectors, and runtime closure

## Scope

This packet concerns finite-dimensional algebras and literal finite permutation modules. It does not promote continuum, cosmological, or hardware claims. Every external-runtime statement is fail-closed.

## BT1345 — Modular basic algebras

For the literal 26-dimensional Hecke algebra, the decomposition matrices are uniquely recovered from dimension and modular trace congruences, and the Cartan matrices satisfy `C = D^T D`.

- Characteristic 2: basic dimension 23, Cartan `diag(1,22)`. The nonsemisimple local vertex has four Ext loops. Minimal homogeneous relations for the associated graded basic algebra occur in degrees 2, 4, and 5 with counts 12, 3, and 1.
- Characteristic 3: basic dimension 26. Its Ext adjacency is `[[1,0,1,0],[0,0,1,0],[1,1,1,0],[0,0,0,0]]`; minimal homogeneous relation counts are 8, 2, and 3 in degrees 2, 3, and 4.
- Characteristic 5: basic dimension 15. The exceptional four-vertex component has arrows `F5→F4`, `F6→F4`, `F4→F5`, `F4→F6`, and four quadratic relations.

These are presentations of the **associated graded** basic algebras. They are not asserted to be filtered presentations of the original reductions, nor Brauer trees of the ambient group algebra.

## BT1346 — Literal 26×4 mixed constants

Each of the 26 Hecke relations is projected to its exact `3×3` species-20 multiplicity block. Multiplying these blocks with the four nine-axis relations yields exact left and right tensors of shape `26×4×18`.

The generated algebra is

\[
M_3(\mathbb Q)\otimes(\mathbb Q\oplus\mathbb Q),
\qquad \dim=18.
\]

It is the complete directed coherent configuration on the three internal axes tensored with the `K_3` association scheme on the triality axes. It has three fibers and is noncommutative; therefore it is a coherent/cellular algebra, not an association scheme. The four-relation nine-axis scheme is its internal-`S_3` orbit fusion.

## BT1347 — Literal cycle-copy observables

The exact length-7 and length-8 cycle shifts, occupation projectors, and Hermitian cosine quadratures are compressed through the literal rank-20 projector inside the 480 directed-edge carrier.

The basis-invariant cosine energies are

\[
E_7=\frac{131}{3456},\qquad E_8=\frac{5}{144}.
\]

Appending the primitive copy projector `E_rr` gives an exact one-hot three-detector signature `E_l e_r`. The cycle modifies the common 20-dimensional operator; the selected copy `r` remains an explicit internal `S_3` gauge choice.

## BT1348 — Runtime closure and manuscript repair

A faithful rational 20-dimensional `W(E6)=U4(2).2` model is reconstructed directly from the 480 carrier. Its standard generator orders are `2,9,10`, and its class traces equal the frozen degree-20 character row exactly.

A genuine GAP/AtlasRep/CTblLib/TomLib/Repsn comparison program is committed. At publication time the GitHub job remained queued, so no external GAP result is promoted.

The concrete Holonet build blocker `analysis/w33_killshot_dashboard_fig.tex` is repaired by deterministic generation from the existing dashboard witness. A build tool may create **temporary, visibly typed** stubs for absent historical Holonet inserts; those stubs never enter the source tree and state that no theorem is promoted.

## BT1349 — Modular triality fusion

The characteristics 2 and 3 degenerate by distinct mechanisms.

- `p=2`: the nine-axis algebra is semisimple `M3(F2)⊕M3(F2)`, but the rational species-20 Hecke de-fusion has denominator `2^6` and does not canonically descend on the integral relation lattice. The primitive transport shadow has rank 2.
- `p=3`: all three transport channels survive, but the species-20 Hecke image is the five-dimensional triangular algebra
  `[[a,0,0],[b,c,0],[d,0,e]]`, while the triality factor is `F3[ε]/(ε^2)`. The combined ten-dimensional algebra has radical-power dimensions `(7,2,0)` and semisimple quotient `F3^3`.
- `p=5`: the mixed algebra is semisimple `M3(F5)⊕M3(F5)`.

The exact certificates, sparse relation bases, mixed constants, and carrier compressions are machine-readable in `data/w33_pass1345_1349_basic_mixed_selector_runtime_fusion.json` and its component files.
