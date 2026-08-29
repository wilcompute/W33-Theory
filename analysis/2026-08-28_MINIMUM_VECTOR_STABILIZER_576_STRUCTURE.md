# The order-576 minimum-vector stabilizer

The trade-lattice pass proved that `PSp(4,3)` is transitive on the 45
antipodal minimum-vector lines and that the stabilizer of one such line has
order 576, while the stabilizer of an oriented minimum vector has order 288.
This note records the exact permutation-group structure obtained by enumerating
the stabilizer inside the 25,920-element projective symplectic action.

## Corrected result

Let `H` be the stabilizer of one antipodal minimum-vector line.  Its largest
normal 2-subgroup is the extraspecial plus-type group

\[
O_2(H)\cong 2^{1+4}_+
\]

of order 32.  The exact invariants of this normal 2-subgroup are:

- order 32;
- centre of order 2;
- derived subgroup of order 2;
- abelianization `C2^4`;
- element-order census: identity + 19 involutions + 12 elements of order 4.

The full stabilizer has

\[
|Z(H)|=2,\qquad |H'|=96,
\]

and exact element-order census

\[
1^1\,2^{43}\,3^{80}\,4^{84}\,6^{272}\,12^{96}.
\]

The earlier version of this note incorrectly called the order-32 extraspecial
normal subgroup the *derived subgroup*.  Direct recomputation of all 576
permutations, independently checked with a permutation-group derived-subgroup
calculation, gives `|H'|=96`.  The structural decomposition itself remains

\[
\boxed{H\cong 2^{1+4}_+\rtimes(S_3\times C_3)}.
\]

The orientation-preserving subgroup `H^+` has order 288 and is

\[
H^+\cong 2^{1+4}_+\rtimes(C_3\times C_3).
\]

Modulo the central involution of the extraspecial group, the natural action on
the two dual tetrads is

\[
H/Z(H)\cong (A_4\times A_4)\rtimes C_2=A_4\wr C_2,
\]

of order 288.

## Why this matters

The repeated integer 576 is attached here to a specific canonical stabilizer,

\[
25920/45=576.
\]

The corrected invariants make comparison with other 576-element groups much
sharper: a prospective bridge must match the center, derived order, element
orders and action, not merely the group order.

## Provenance and boundary

Input carrier and stabilizer counts are from the exact minimum-vector packet
`747a159dea67c6ffea96beaf2560991a4c9f252d` /
`f5837a8abfac436bf8ea061e89daf8fcee928a36`.  The correction is an exact
permutation-group recomputation.  No physical interpretation is attached to
the group.