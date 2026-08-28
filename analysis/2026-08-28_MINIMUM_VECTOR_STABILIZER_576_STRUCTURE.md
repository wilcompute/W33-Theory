# The order-576 minimum-vector stabilizer

The previous trade-lattice pass proved that `PSp(4,3)` is transitive on the 45
antipodal minimum-vector lines and that the stabilizer of one such line has
order 576, while the stabilizer of an oriented minimum vector has order 288.
This note freezes the exact permutation-group structure obtained by enumerating
the stabilizer inside the 25,920-element projective symplectic action.

## Result

Let `H` be the stabilizer of one antipodal minimum-vector line.  Its derived
subgroup has order 32 and is the extraspecial plus-type group

\[
2^{1+4}_+.
\]

The exact invariants of this normal 2-subgroup are:

- order 32;
- centre of order 2;
- derived subgroup of order 2;
- abelianization `C2^4`;
- element-order census: identity + 19 involutions + 12 elements of order 4.

The orientation-preserving subgroup `H^+` has order 288 and splits as

\[
H^+ \cong 2^{1+4}_+\rtimes(C_3\times C_3).
\]

The full unsigned stabilizer contains a complementary order-18 subgroup whose
centre and derived subgroup both have order 3 and whose abelianization is
`C6`; its exact element structure identifies it as `S3 x C3`.  Therefore

\[
\boxed{H\cong 2^{1+4}_+\rtimes(S_3\times C_3)}.
\]

Modulo the central involution of the extraspecial group, the natural action on
the two dual tetrads is equivalently described by

\[
(A_4\times A_4)\rtimes C_2=A_4\wr C_2,
\]

again of order 576 after lifting through the central double cover.

## Why this matters

This is the first occurrence in the current near-ovoid/trade programme where
the repeated integer 576 is attached to a *specific canonical stabilizer*:

\[
25920/45=576.
\]

That makes comparison with the repository's 576 Latin-square/tesseract objects
mathematically meaningful.  It still does **not** prove those 576-object sets
are the same G-set; an explicit equivariant map or matching permutation
character is still required.

## Provenance and boundary

Input carrier and stabilizer counts are from the exact minimum-vector packet
`747a159dea67c6ffea96beaf2560991a4c9f252d` /
`f5837a8abfac436bf8ea061e89daf8fcee928a36`.  The group decomposition recorded
here comes from exact permutation-group enumeration of the stabilizer, not from
order numerology.  No physical interpretation is attached to the group.
