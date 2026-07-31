# Pass 1521 — Perkel-Shadow Bridge Falsifier

**Status:** executable exact test added; inherited-action obstruction proved; emergent-relation question delegated to the exact bridge matrices.

## Why the `57+19` observation deserves a sharper test

The 57-cell is the regular self-dual polytope of type \(\{5,3,5\}_5\). It has

\[
(f_0,f_1,f_2,f_3)=(57,171,171,57),
\]

its skeleton is the Perkel graph, and its full rotation group is

\[
\operatorname{PSL}(2,19),\qquad |\operatorname{PSL}(2,19)|=3420.
\]

The Perkel graph is the unique distance-regular graph with intersection array

\[
\{6,5,2;1,1,3\},
\]

and it has a standard vertex model \(\mathbb Z_3\times\mathbb Z_{19}\).

Pass 1502 independently produced

\[
76=57+19
\]

rank-complete apartment bridges: 57 preserve all fourteen Mackey source dimensions, while 19 lose one dimension only in the terminal five-dimensional source.

The arithmetic is therefore stronger than a bare appearance of 57:

\[
76=19\cdot4,
\qquad
57+19=19(3+1).
\]

There are exactly 19 rank-81 sheets, each carrying four sign characters. The exact worker now asks whether the robust/defective split is literally a fiberwise \(3+1\) law and whether the 57 robust bridge matrices carry a natural Perkel relation.

## Correction to the earlier negative argument

The divisibility test is decisive but narrower than previously stated:

\[
19\nmid25920,
\qquad
19\nmid51840.
\]

Hence neither \(\operatorname{PSp}(4,3)\) nor \(\operatorname{PGSp}(4,3)\) contains \(\operatorname{PSL}(2,19)\), and no Perkel action can be inherited from the W33 acting group.

That does **not** exclude an emergent abstract graph on 57 derived bridge objects whose automorphism group is larger than the subgroup induced from W33. An intrinsic relation graph can have accidental automorphisms that do not extend to the ambient geometry. Therefore the correct conclusion is:

> inherited \(\operatorname{PSL}(2,19)\) symmetry is impossible; emergent Perkel symmetry remains a falsifiable graph question.

## Exact falsifier

`analysis/w33_pass1521_perkel_bridge_falsifier.py` recomputes the complete Pass-1502 bridge family and then:

1. verifies the 19-sheet, four-sign-character, 57-robust, 19-defective census;
2. records the defect character on every rank-81 sheet and tests the uniform \(3+1\) fiber law;
3. constructs the standard \(\mathbb Z_3\times\mathbb Z_{19}\) Perkel graph and verifies its order, size, valency, diameter, and intersection array;
4. forms exact pair-relation classes on the 57 robust matrices using Frobenius products, support overlaps, row/column support overlaps, mask/residual coincidence, and sign/mask Hamming data;
5. tests every single class and every union of at most three classes having 171 edges for isomorphism with the Perkel graph;
6. performs the analogous exact search for a 19-cycle on the defective bridges.

A positive hit would be meaningful: the resulting \(\operatorname{PSL}(2,19)\) would be an emergent automorphism group of the derived bridge relation, not a subgroup of the W33 automorphism group.

A negative hit has an equally sharp boundary: it excludes Perkel only for the listed exact intrinsic pair invariants and small unions of their value classes. The search is **not exhaustive** over all conceivable relations on the 57 bridges and does not prove that no more elaborate relation can be Perkel.

## Existing local 57-cell bridge

BT836 remains the established geometric connection. Every regular W33 spread contains an \(A_5\)-controlled Petersen graph on its ten lines, exactly the skeleton of one hemi-dodecahedral cell of the 57-cell. Passes 1472 and 1478 then locate where the containment stops: the local cell embeds, while the 57-vertex skeleton and the full polytope do not embed directly into the 40-point W33 carrier.

Pass 1521 therefore tests a different possibility: whether the *apartment-bridge gauge objects*, rather than W33 points, recover the 57-cell skeleton as an emergent relation.

## References

- H. S. M. Coxeter, “Ten Toroids and Fifty-Seven Hemi-Dodecahedra,” *Geometriae Dedicata* 13 (1982), 87–99.
- P. Vanden Cruyce, “Geometries Related to PSL(2,19),” *European Journal of Combinatorics* 6 (1985), 163–173.
- K. Coolsaet and J. Degraer, “A Computer Assisted Proof of the Uniqueness of the Perkel Graph,” *Designs, Codes and Cryptography* 34 (2005), 155–171.
